import scratchattach as sa
from supabase import create_client, Client
import os
import time
import logging

# ================= CONFIG =================
SCRATCH_USER = os.getenv("SCRATCH_USER")
SCRATCH_PASS = os.getenv("SCRATCH_PASS")
PROJECT_ID = os.getenv("PROJECT_ID")

SUPABASE_URL = "https://ymoxugsclllkjjtdiicg.supabase.co"
SUPABASE_KEY = "sb_publishable_nOjCAW-rL2OvLfeYwYXYMQ_t4prs3j7"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Encoder / Decoder
KEY = r"abcdefghijklmnopqrstuvwxyz1234567890 @-_.,:'`\"~+=*&#$%?!/\\(){}[]<>©®℗™×÷"

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
session = sa.login(SCRATCH_USER, SCRATCH_PASS)
cloud = session.connect_cloud(PROJECT_ID)

logger.info("Server started - Simple mode")

@cloud.event
def on_set(activity):
    var = activity.var
    value = str(activity.value).strip()

    try:
        if var == "request":
            # Format: username:project_id:action
            parts = value.split(":", 2)
            if len(parts) == 3:
                username, project_id, action = parts
                game_key = f"{username}:{project_id}"

                if action == "write":
                    # The project will send the data in another variable or same request
                    # For simplicity, assume data is in another cloud var or combined
                    # You can adjust this
                    data = "temp_data"  # Replace with actual data from cloud var
                    encoded = encode(data)
                    supabase.table("player_rewards").upsert({
                        "username": game_key,
                        "data": encoded
                    }).execute()
                    cloud.set_var("status", "saved")
                    logger.info(f"Saved for {username} in project {project_id}")

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
