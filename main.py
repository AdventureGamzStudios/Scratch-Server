import scratchattach as sa
import os
import time
import logging

# Secrets in Replit (lock icon)
SCRATCH_SESSION = os.getenv("SCRATCH_SESSION")
PROJECT_ID = os.getenv("PROJECT_ID")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Starting server...")

# Login with Session ID
session = sa.Session(SCRATCH_SESSION)
cloud = session.connect_cloud(PROJECT_ID)

logger.info("Logged in and connected to cloud successfully!")

# Test comment (you can remove this later)
try:
    project = session.connect_project(PROJECT_ID)
    project.post_comment("Server is online - " + time.strftime("%Y-%m-%d %H:%M:%S"))
    logger.info("Test comment posted successfully!")
except Exception as e:
    logger.error(f"Comment error: {e}")

while True:
    time.sleep(30)
    logger.info("Server is running...")
