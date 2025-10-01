import os
from flask import Flask
import threading
import asyncio
import subprocess

app = Flask(__name__)

@app.route("/")
def home():
    return "Lichess bot is running!"

def run_bot():
    # Start your bot as a subprocess
    subprocess.run(["python", "user_interface.py", "matchmaking"])

if __name__ == "__main__":
    # Start the bot in a background thread
    threading.Thread(target=run_bot, daemon=True).start()
    
    # Run Flask server to satisfy Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
