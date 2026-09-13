def chat(sender, message):
    print(f"Chat tool is running: {sender} says {message}")
    return sender, message
def attack():
    print("Attack tool is running")
    return "Attacking!"