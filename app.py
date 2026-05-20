from fastapi import FastAPI
from pydantic import BaseModel
from ai_engine import generate_response
from memory import save_interaction

app = FastAPI(
    title="Responsive AI",
    description="Real-Time Responsive AI Framework",
    version="1.0"
)

class UserInput(BaseModel):
    username: str
    message: str

@app.get("/")
def home():
    return {
        "status": "Responsive AI Running",
        "message": "Welcome to Responsive AI"
    }

@app.post("/chat")
def chat(user_input: UserInput):

    response = generate_response(
        user_input.username,
        user_input.message
    )

    save_interaction(
        user_input.username,
        user_input.message,
        response
    )

    return {
        "user": user_input.username,
        "response": response
    }
