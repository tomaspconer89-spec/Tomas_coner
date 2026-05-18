import logging
import json
from openai import OpenAI
from config import OPENAI_API_KEY
import re
import os

MAX_INPUT_LENGTH = 200 # Max characters for user input

logging.basicConfig(
    filename="chatbot.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

client = OpenAI(api_key=OPENAI_API_KEY)
messages = [{"role": "system","content":""}]
MEMORY_LIMIT = 4  # last 4 non-system messages
system_prompt = ""

def get_system_prompt():
    mode = input("Choose mode (teacher / friend / mentor): ").lower()

    if mode == "teacher":
        return "You are a patient Python teacher. Explain simply with examples."
    elif mode == "friend":
        return "You are a friendly coding buddy. Keep things casual and encouraging."
    elif mode == "mentor":
        return "You are a strict coding mentor. Be direct and concise."
    else:
        print("Invalid choice. Defaulting to teacher.")
        return "You are a helpful Python teacher."

def save_chat(messages):
    try:
        with open("chat_history.json", "w") as f:
            json.dump(messages, f, indent=4)
    except Exception as e:
        logging.error(f"Error saving chat history: {str(e)}")

def build_messages():
    system_message = messages[0]
    recent_messages = messages[1:][-MEMORY_LIMIT:]
    return [system_message] + recent_messages


def load_notes(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            notes = f.read()
        return notes
    except Exception as e:
        logging.error(f"Error loading notes: {str(e)}")
        return ""

def list_files(folder="./notes"):
    try:
        files = [f for f in os.listdir(folder) if f.endswith(".txt")]
        return files
    except Exception as e:
        logging.error(f"Error listing files: {str(e)}")
        return []
    
def choose_file():
    files = list_files()

    if not files:
        print("No files found in notes folder. Please add some .txt files.")
        return None
    
    print("\n Available files:")
    for i, file in enumerate(files, 1):
        print(f"{i}. {file}")

    while True:
        choice = input("Select file number: ")

        if not choice.isdigit():
            print("Enter a valid number.")
            continue
        choice = int(choice)

        if 1 <= choice <= len(files):
            return f"notes/{files[choice - 1]}"
        else:
            print("Invalid choice. Try again.")

    try:
        choice = int(input("Choose a file (enter the number): "))
        if 1 <= choice <= len(files):
            return files[choice - 1]
        else:
            print("Invalid choice.")
            return None
    except ValueError:
        print("Please enter a valid number.")
        return None


def ask_ai(notes, user_question):
    global messages

    try:
        messages.append({"role": "user", "content":user_question})
        
        final_messages = build_messages()

        stream = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=final_messages,
            temperature=0.7,
            max_tokens=150,
            stream=True
        )

        print("\nAI:", end=" ", flush=True)

        full_response = ""

        for chunk in stream:
            try:
                delta = chunk.choices[0].delta.content
                if delta:
                    print(delta, end="", flush=True)
                    full_response += delta
            except (AttributeError, IndexError):
                continue


        print()
        messages.append({"role": "assistant", "content": full_response})
        save_chat(messages[-10:])  # Save last 10 messages for context

    except Exception as e:
        logging.error(f"Chatbot error: {str(e)}")
        print("Something went wrong. Check chatbot.log")

def is_valid_input(user_input):
    if not user_input.strip():
        print("Please enter a valid question.")
        return False
    if len(user_input) > MAX_INPUT_LENGTH:
        print(f"Input too long. Please limit to {MAX_INPUT_LENGTH} characters.")
        return False
    
    if not re.search("[a-zA-Z]", user_input):
        print("Please include some text in your question.")
        return False
    
    return True

def main():
    file_path = choose_file()
    if not file_path:
        return
    system_prompt = get_system_prompt()
         
    notes = load_notes(file_path)
    if not notes:
        print("No notes found in the selected file.")
        return

    messages[:] = [messages[0]] # reset memory

    if len(notes) > 3000:
        print("Notes too large. Trimming...")
        notes = notes[:3000]
    print("Notes loaded successfully. Ask questions about the file content. Type 'q' to quit.")

    messages[0]["content"] = f"{system_prompt}\nAnswer ONLY using the provided notes. \nIf the answer is not in the notes, say: 'I couldn't find the answer'" f"NOTES:\n{notes}\n"
    while True:
        user_input = input("\nYou: ")

        if user_input.lower() == "q":
            print("Goodbye!")
            break
        if user_input.lower() == "reset":
            messages[:] = [messages[0]]
            print("Memory cleared. You can start fresh.")
            continue
        if user_input.lower() == "history":
            for msg in messages[1:]:
                print(f"{msg['role']}: {msg['content']}")
            continue
        if user_input.lower() == "change file":
            file_path = choose_file()
            if not file_path:
                continue

            notes = load_notes(file_path)

            messages[:] = [messages[0]]  # reset memory

            messages[0]["content"] = (
                f"{system_prompt}\n\n"
                "You are a helpful assistant.\n"
                "Answer ONLY using the selected notes.\n"
                "If not found, say: 'I could not find that in the notes.'\n\n"
                f"NOTES:\n{notes}"
            )

            print("Switched file successfully.")
            continue
        
        if not is_valid_input(user_input):
            continue
        

        ask_ai(notes, user_input)


if __name__ == "__main__":
    main()

