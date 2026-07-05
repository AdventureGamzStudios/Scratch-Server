import os
import time
from flask import Flask
import threading

print("=== SERVER STARTING ===")
print("SCRATCH_USER is set:", "Yes" if os.getenv("SCRATCH_USER") else "No")
print("PROJECT_ID is set:", "Yes" if os.getenv("PROJECT_ID") else "No")

app = Flask(__name__)

@app.route('/')
def home():
    return "Scratch Rewards Server is running!"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 10000)))

# Run Flask in background
threading.Thread(target=run_flask, daemon=True).start()

print("Server is running...")

while True:
    time.sleep(30)
