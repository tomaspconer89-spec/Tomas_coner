from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

MEMORY_LIMIT = 4

class Chatbot:
    def __init__(self, notes, system_prompt):
        self.messages = [
            {
                "role": "system",
                "content": (
                    f"{system_prompt}\n\n"
                    "Answer ONLY using the notes.\n"
                    f"NOTES:\n{notes}"
                )
            }
        ]

    def build_messages(self):
        return [self.messages[0]] + self.messages[1:][-MEMORY_LIMIT:]

    def ask(self, question):
        self.messages.append({"role": "user", "content": question})

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=self.build_messages(),
            max_tokens=150
        )

        answer = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": answer})

        return answer