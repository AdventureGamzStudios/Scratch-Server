import scratchattach as sa
import os
import time
import logging

# Environment Variables (add these in Replit Secrets)
# SCRATCH_USER
# SCRATCH_PASS
# PROJECT_ID

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Starting server...")

session = sa.login(os.getenv("SCRATCH_USER"), os.getenv("SCRATCH_PASS"))
cloud = session.connect_cloud(os.getenv("PROJECT_ID"))

logger.info("Logged in and connected to cloud!")

@cloud.event
def on_set(activity):
    logger.info(f"Received: {activity.var} = {activity.value}")
    # Add your logic here later

while True:
    time.sleep(30)
    logger.info("Server is alive")
