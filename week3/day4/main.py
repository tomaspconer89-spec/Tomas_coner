from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from ai import Chatbot

app = FastAPI()
app.mount("/", StaticFiles(directory="static", html=True), name="static")
# allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# global chatbot instance (simple version)
chatbot = None

def load_notes():
    with open("notes/python.txt", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/")
def root():
    return {"message": "API is running"}

@app.post("/start")
def start_chat():
    global chatbot

    notes = load_notes()
    chatbot = Chatbot(notes, "You are a helpful assistant")

    return {"message": "Chat started"}

@app.post("/chat")
def chat(user_input: dict):
    question = user_input.get("message")

    if not chatbot:
        return {"error": "Start chat first"}

    answer = chatbot.ask(question)

    return {"response": answer}