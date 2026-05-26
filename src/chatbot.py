import json
import openai
from config import client, DEPLOYMENT
from database import get_balance, get_all_users_raw
from security import generate_system_prompt

class ChatbotSession:
    def __init__(self, user_session: dict, rag_engine):
        self.user_session = user_session
        self.rag_engine = rag_engine
        self.history = []  # Holds conversation history (excluding active system prompt)

    def send_message(self, user_query: str) -> str:
        # 0. Content Moderation Check
        try:
            # Attempt to use standard OpenAI moderation API to detect harmful inputs.
            moderation_response = client.moderations.create(input=user_query)
            if moderation_response.results[0].flagged:
                return "I cannot answer this query as it violates safety guidelines."
        except Exception:
            # Fallback: Azure OpenAI doesn't support the /moderations endpoint by default.
            # It instead relies on built-in Content Safety filters running automatically.
            pass

        # 1. Retrieve context via SimpleRAG
        rag_context = self.rag_engine.retrieve(user_query, k=2)

        # Retrieve the raw users database representation for testing
        try:
            users_db = get_all_users_raw()
            db_context = f"Vulnerability Testing Database Dump (DEBUG ONLY):\n{json.dumps(users_db)}"
        except Exception as e:
            db_context = f"Vulnerability Testing Database Dump Failed: {e}"

        # 2. Build the secure system prompt with latest context and session info
        system_prompt = generate_system_prompt(
            username=self.user_session["username"],
            account_number=self.user_session["account_number"],
            rag_context=rag_context,
            db_context=db_context
        )


        # 3. Assemble messages for Azure OpenAI API
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(self.history)
        messages.append({"role": "user", "content": user_query})

        # Define tools. Note: check_balance has NO inputs.
        # This is a critical security design pattern preventing parameter-tampering prompt injection.
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "check_balance",
                    "description": "Checks the current account balance for the logged-in user. Requires no arguments.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            }
        ]

        # 4. Request completion
        try:
            response = client.chat.completions.create(
                model=DEPLOYMENT,
                messages=messages,
                tools=tools,
                tool_choice="auto",
                temperature=0.2,
                max_completion_tokens=500
            )
        except openai.BadRequestError as e:
            if "content_filter" in str(e).lower() or "safety" in str(e).lower():
                return "I cannot answer this query as the content triggered safety filters."
            raise e

        response_message = response.choices[0].message

        # 5. Handle tool call requests if any
        if response_message.tool_calls:
            # Add user query and assistant's intent to history
            self.history.append({"role": "user", "content": user_query})
            
            assistant_history_msg = {
                "role": "assistant",
                "content": response_message.content,
                "tool_calls": [
                    {
                        "id": tc.id,
                        "type": tc.type,
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    } for tc in response_message.tool_calls
                ]
            }
            self.history.append(assistant_history_msg)
            
            # Prepare second completion request message list
            # It needs system prompt + history + assistant_msg + tool_msg
            second_messages = [{"role": "system", "content": system_prompt}]
            second_messages.extend(self.history[:-1]) # add previous history and user query
            second_messages.append(response_message)  # add the original assistant response with tool_calls

            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                if function_name == "check_balance":
                    # SECURE STEP: Ignore LLM inputs. Get balance for the session's user account directly.
                    balance_val = get_balance(self.user_session["account_number"])
                    if balance_val is not None:
                        tool_content = f"Success. Current balance for account {self.user_session['account_number']} is ${balance_val:,.2f}."
                    else:
                        tool_content = "Error: Account not found."
                    
                    tool_history_msg = {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function_name,
                        "content": tool_content
                    }
                    self.history.append(tool_history_msg)
                    second_messages.append(tool_history_msg)

            # Request final LLM response incorporating tool results
            try:
                second_response = client.chat.completions.create(
                    model=DEPLOYMENT,
                    messages=second_messages
                )
            except openai.BadRequestError as e:
                if "content_filter" in str(e).lower() or "safety" in str(e).lower():
                    return "I cannot answer this query as the content triggered safety filters."
                raise e
            final_reply = second_response.choices[0].message.content
            self.history.append({"role": "assistant", "content": final_reply})
            return final_reply
        else:
            # 6. Regular conversational response
            self.history.append({"role": "user", "content": user_query})
            self.history.append({"role": "assistant", "content": response_message.content})
            return response_message.content
