import logging
from openai import OpenAI
from config import OPENAI_API_KEY
import json

logging.basicConfig(
    filename="chatbot.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

client = OpenAI(api_key=OPENAI_API_KEY)

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

messages = [
    {
        "role": "system",
        "content": get_system_prompt()
    }
]

MEMORY_LIMIT = 4  # last 4 non-system messages

def build_messages():
    system_message = messages[0]
    recent_messages = messages[1:][-MEMORY_LIMIT:]
    return [system_message] + recent_messages

def load_notes(file_path):
    try:
        with open(file_path, "r") as f:
            notes = f.read()
        return notes
    except Exception as e:
        logging.error(f"Error loading notes: {str(e)}")
        return ""

def ask_ai(notes,user_question):
    global messages

    try:
        messages.append({"role": "user", "content": f"{notes}\n\nQuestion: {user_question}"})
        save_chat(messages)

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
            delta = chunk.choices[0].delta.content
            if delta:
                print(delta, end="", flush=True)
                full_response += delta

        print()
        messages.append({"role": "assistant", "content": full_response})

    except Exception as e:
        logging.error(f"Chatbot error: {str(e)}")
        print("Something went wrong. Check chatbot.log")

def main():
    notes = load_notes("notes.txt")
    if not notes:
        print("No notes found. Please create a notes.txt file with your study notes.")
        return
    
    print("Notes loaded successfully. Ask questions about the file content. Type 'q' to quite.")
    
    while True:
        user_input = input("\nYou: ")

        if user_input.lower() == "q":
            print("Goodbye!")
            break

        if not user_input.strip():
            print("Please enter a valid question.")
            continue

        ask_ai(notes, user_input)

if __name__ == "__main__":
    main()