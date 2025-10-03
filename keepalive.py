import os
from flask import Flask
import threading
import subprocess
from collections import deque

app = Flask(__name__)

# Keep last 200 lines of logs in memory
logs = deque(maxlen=200)


@app.route("/")
def home():
    return "Lichess bot is running!"


@app.route("/logs")
def show_logs():
    return "<pre>" + "".join(logs) + "</pre>"


def run_bot():
    process = subprocess.Popen(
        ["python", "user_interface.py", "matchmaking"],
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


if __name__ == "__main__":
    # Start the bot in a background thread
    threading.Thread(target=run_bot, daemon=True).start()

    # Run Flask server to satisfy Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
