import json
import os

DATABASE = "conversation_memory.json"

def save_interaction(user, message, response):

    data = {
        "user": user,
        "message": message,
        "response": response
    }

    if not os.path.exists(DATABASE):
        with open(DATABASE, "w") as file:
            json.dump([], file)

    with open(DATABASE, "r") as file:
        existing = json.load(file)

    existing.append(data)

    with open(DATABASE, "w") as file:
        json.dump(existing, file, indent=4)
