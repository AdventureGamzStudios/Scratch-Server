import scratchattach as sa
from supabase import create_client, Client
import os
import time
import logging

# ================= CONFIG =================
SCRATCH_USER = os.getenv("SCRATCH_USER")
SCRATCH_SESSION = os.getenv("SCRATCH_SESSION")  # Add this in Render
PROJECT_ID = os.getenv("PROJECT_ID")

SUPABASE_URL = "https://ymoxugsclllkjjtdiicg.supabase.co"
SUPABASE_KEY = "sb_publishable_nOjCAW-rL2OvLfeYwYXYMQ_t4prs3j7"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Encoder / Decoder
KEY = r"abcdefghijklmnopqrstuvwxyz1234567890 @-_.,:'`~+=*&#$%?!/\\(){}[]<>©®℗™×÷"

def encode(string):
    if not string:
        return "99"
    encoded = ""
    i = 0
    while i < len(string):
        char = string[i]
        try:
            pos = KEY.index(char) + 1
        except ValueError:
            pos = 1
        value = pos + 9
        encoded += str(value)
        i += 1
    encoded += "99"
    return encoded

def decode(encoded):
    encoded = str(encoded)
    if not encoded or not encoded.endswith("99"):
        return ""
    decoded = ""
    i = 0
    while i < len(encoded) - 2:
        num_str = encoded[i:i+2]
        if num_str == "99":
            break
        try:
            num = int(num_str)
            pos = num - 9
            if 1 <= pos <= len(KEY):
                decoded += KEY[pos - 1]
            else:
                decoded += "?"
        except ValueError:
            decoded += "?"
        i += 2
    return decoded

# ================= SERVER =================
session = sa.Session(SCRATCH_SESSION, username=SCRATCH_USER)
cloud = session.connect_cloud(PROJECT_ID)

logger.info("Server started successfully")

@cloud.event
def on_set(activity):
    var = activity.var
    value = str(activity.value).strip()

    try:
        if var == "request":
            parts = value.split(":", 2)
            if len(parts) == 3:
                username, project_id, action = parts
                game_key = f"{username}:{project_id}"

                if action == "write":
                    # You will send data in another variable or extend this
                    data = "temp"  # Replace with actual data
                    encoded = encode(data)
                    supabase.table("player_rewards").upsert({
                        "username": game_key,
                        "data": encoded
                    }).execute()
                    cloud.set_var("status", "saved")

                elif action == "read":
                    response = supabase.table("player_rewards").select("data").eq("username", game_key).execute()
                    if response.data:
                        cloud.set_var("user_data", response.data[0]["data"])
                        cloud.set_var("status", "loaded")
                    else:
                        cloud.set_var("status", "no_data")
    except Exception as e:
        logger.error(f"Error: {e}")
        cloud.set_var("status", "error")

while True:
    time.sleep(5)
