import os
from flask import Flask
import threading
import subprocess
from collections import deque

app = Flask(__name__)

# Keep last 200 lines of logs in memory
logs = deque(maxlen=200)

# Prevent multiple launches
bot_started = False


@app.route("/")
def home():
    return "Lichess bot is running!"


@app.route("/logs")
def show_logs():
    return "<pre>" + "".join(logs) + "</pre>"


def run_bot():
    process = subprocess.Popen(
        ["python3", "user_interface.py", "matchmaking"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    for line in iter(process.stdout.readline, ''):
        logs.append(line)
        print(line, end="", flush=True)

    process.stdout.close()
    process.wait()


def start_bot_once():
    """Start the bot only once per process."""
    global bot_started
    if not bot_started:
        bot_started = True
        threading.Thread(target=run_bot, daemon=True).start()


if __name__ == "__main__":
    # Start the bot once
    start_bot_once()

    # Run Flask server to satisfy Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
