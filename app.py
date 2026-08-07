import scratchattach as sa
from dotenv import load_dotenv
import os
import time
import json
import logging

# Load environment variables
load_dotenv()

SCRATCH_USER = os.getenv("SCRATCH_USER")
SCRATCH_PASS = os.getenv("SCRATCH_PASS")
PROJECT_ID = os.getenv("PROJECT_ID")
PROJECT_TOKEN = os.getenv("PROJECT_TOKEN")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATA_FILE = "data.json"

# Load existing data
def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

# Save data
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

players = load_data()

logger.info("Starting Scratch Server...")

try:
    session = sa.login(SCRATCH_USER, SCRATCH_PASS)
    cloud = session.connect_cloud(PROJECT_ID)
    
    if PROJECT_TOKEN:
        cloud.project_token = PROJECT_TOKEN
        
    logger.info("Successfully logged in and connected to cloud!")
except Exception as e:
    logger.error(f"Login failed: {e}")
    raise

@cloud.events
def on_set(activity):
    var = activity.var
    value = str(activity.value).strip()

    try:
        if var == "request":
            # Format: username:project_id:action
            parts = value.split(":")
            if len(parts) >= 3:
                username = parts[0]
                project_id = parts[1]
                action = parts[2]

                key = f"{username}:{project_id}"

                if action == "read":
                    if key in players:
                        cloud.set_var("user_data", players[key])
                        cloud.set_var("status", "loaded")
                        logger.info(f"Loaded data for {username}")
                    else:
                        cloud.set_var("status", "no_data")
                        logger.info(f"No data found for {username}")

                elif action == "write":
                    # You will send the actual data in another variable later
                    # For now this is just the structure
                    data = "example_data"
                    players[key] = data
                    save_data(players)
                    cloud.set_var("status", "saved")
                    logger.info(f"Saved data for {username}")

    except Exception as e:
        logger.error(f"Error: {e}")
        cloud.set_var("status", "error")

logger.info("Server is ready and listening for requests...")

while True:
    time.sleep(30)
