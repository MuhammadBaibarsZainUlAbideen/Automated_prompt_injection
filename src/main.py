import os
import sys

# Ensure Src directory is in python search path
sys.path.append(os.path.dirname(__file__))

from database import init_db, register_user, authenticate_user
from rag import SimpleRAG
from database import init_db, register_user, authenticate_user
from rag import SimpleRAG
from chatbot import ChatbotSession

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
    print("=" * 60)
    print("      Welcome to ExampleBank Secure Assistant CLI      ")
    print("=" * 60)

def chat_session_loop(user_session, rag_engine):
    clear_console()
    print("=" * 60)
    print(f" Chat session active for: {user_session['username']}")
    print(f" Account Number: {user_session['account_number']}")
    print(f" Type 'exit' or 'quit' to log out.")
    print("=" * 60)

    # Initialize a new chatbot session
    chatbot = ChatbotSession(user_session, rag_engine)

    while True:
        try:
            user_input = input(f"\n[{user_session['username']}] > ").strip()
            if not user_input:
                continue

            if user_input.lower() in ['exit', 'quit']:
                print("\nLogging out of session. Goodbye!")
                break

            # 2. Process message through Chatbot Session
            print("[BankBot] is thinking...", end="\r")
            reply = chatbot.send_message(user_input)
            
            # Print response
            print(f"\r[BankBot] > {reply}")

        except KeyboardInterrupt:
            print("\nSession interrupted. Returning to main menu.")
            break
        except Exception as e:
            print(f"\n[Error] Something went wrong: {e}")

def main():
    # Initialize DB tables
    init_db()

    clear_console()
    show_banner()
    print("\nInitializing AI models. Please wait...")
    
    # Initialize AI engines
    rag_engine = SimpleRAG()
    
    while True:
        clear_console()
        show_banner()
        print("\n1. Login to Account")
        print("2. Register New Account")
        print("3. Exit System")
        
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == '1':
            clear_console()
            show_banner()
            print("\n--- ACCOUNT LOGIN ---")
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            
            if not username or not password:
                print("\nError: Username and password cannot be empty.")
                input("\nPress Enter to return to menu...")
                continue
                
            user = authenticate_user(username, password)
            if user:
                print("\nAuthentication successful!")
                input("\nPress Enter to enter chat session...")
                chat_session_loop(user, rag_engine)
            else:
                print("\nError: Invalid username or password.")
                input("\nPress Enter to return to menu...")
                
        elif choice == '2':
            clear_console()
            show_banner()
            print("\n--- REGISTER NEW ACCOUNT ---")
            username = input("Choose Username: ").strip()
            password = input("Choose Password: ").strip()
            
            if not username or not password:
                print("\nError: Username and password cannot be empty.")
                input("\nPress Enter to return to menu...")
                continue
                
            try:
                # Set up initial balance of $1000.0
                user = register_user(username, password, initial_balance=1000.0)
                print("\nAccount registered successfully!")
                print(f"Generated Account Number: {user['account_number']}")
                print(f"Starting Balance: ${user['balance']:.2f}")
                input("\nPress Enter to enter chat session...")
                chat_session_loop(user, rag_engine)
            except ValueError as e:
                print(f"\nError: {e}")
                input("\nPress Enter to return to menu...")
                
        elif choice == '3':
            print("\nThank you for using ExampleBank Secure CLI. Goodbye!")
            break
        else:
            print("\nInvalid choice. Please select 1, 2, or 3.")
            input("\nPress Enter to continue...")


RED_TEAM_USERNAME = "red_team_hacker"
RED_TEAM_ACCOUNT_NUMBER = 999999999 # Dummy account for red team activities

def run_chatbot_query(query: str) -> str:
    # Ensure DB and models are initialized once
    init_db()
    rag_engine = SimpleRAG()

    # Register a dummy user if they don't exist
    try:
        user_session = register_user(RED_TEAM_USERNAME, "redteam_pass", initial_balance=0.0)
    except ValueError:
        # User already exists, authenticate
        user_session = authenticate_user(RED_TEAM_USERNAME, "redteam_pass")
    
    # Simulate a single chat turn
    chatbot = ChatbotSession(user_session, rag_engine)
    
    # Override print statements for cleaner output during red team
    original_print = __builtins__.print
    def red_team_print(*args, **kwargs):
        # Filter out bankbot status messages
        if "[BankBot]" not in str(args[0]):
            original_print(*args, **kwargs)
    __builtins__.print = red_team_print

    reply = chatbot.send_message(query)
    __builtins__.print = original_print # Restore print
    return reply

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "red_team_mode":
        # This mode is for direct API-like interaction for red teaming
        if len(sys.argv) > 2:
            query = sys.argv[2]
            response = run_chatbot_query(query)
            print(response)
        else:
            print("Usage: main.py red_team_mode \"Your query\"")
    else:
        main()

