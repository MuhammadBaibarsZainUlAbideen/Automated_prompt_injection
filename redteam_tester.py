import os
import sys
import json

# Ensure src directory is in python search path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from database import init_db, register_user, authenticate_user
from rag import SimpleRAG
from chatbot import ChatbotSession

def run_query(payload, username="red_team_hacker", password="redteam_pass"):
    """
    Simulates a single chat turn with a specific payload.
    Automatically handles registration/authentication.
    """
    init_db()
    
    # Try to authenticate, register if it fails
    user_session = authenticate_user(username, password)
    if not user_session:
        try:
            user_session = register_user(username, password, initial_balance=0.0)
        except ValueError:
            # Username exists but password might be different, 
            # for testing we'll just try to get the user by username
            from database import get_user_by_username
            user_session = get_user_by_username(username)

    # Initialize engines
    rag_engine = SimpleRAG()
    
    print(f"\n--- Testing Payload ---")
    print(f"Payload: {payload}")
    print("[Security] PIGuard DECOMMISSIONED.")
    
    # 2. Process message
    print("[BankBot] is thinking...")
    chatbot = ChatbotSession(user_session, rag_engine)
    reply = chatbot.send_message(payload)
    
    print(f"Response: {reply}")
    return reply

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Red-Team Tester (Security Removed)")
    parser.add_argument("payload", nargs="?", help="The payload to send to the chatbot")
    args = parser.parse_args()

    if args.payload:
        # Run a single query from command line
        run_query(args.payload)
    else:
        # Interactive loop for rapid testing
        print(f"Red-Team Tester Active. Security: DECOMMISSIONED")
        print("Type 'exit' to quit.")
        while True:
            try:
                query = input("\nQuery > ").strip()
                if query.lower() in ['exit', 'quit']:
                    break
                if not query:
                    continue
                run_query(query)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")
