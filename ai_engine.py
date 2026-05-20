from datetime import datetime

def generate_response(user, message):

    msg = message.lower()

    if "hello" in msg:
        return f"Hello {user}, welcome to Responsive AI."

    elif "time" in msg:
        return f"Current server time: {datetime.now()}"

    elif "weather" in msg:
        return "Weather intelligence module can be integrated here."

    elif "ai" in msg:
        return "Responsive AI adapts dynamically to user interactions."

    elif "help" in msg:
        return "Available commands: hello, time, weather, ai"

    else:
        return "I am continuously learning from interactions."
