from datetime import datetime

def log_action(message):
    with open("organizer.log", "a") as f:
        f.write(f"{datetime.now()} - {message}\n")