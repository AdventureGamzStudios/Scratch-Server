import scratchattach as sa
import os
import time
import logging

# Environment Variables (set these in the panel)
SCRATCH_USER = os.getenv("SCRATCH_USER")
SCRATCH_PASS = os.getenv("SCRATCH_PASS")
PROJECT_ID = os.getenv("PROJECT_ID")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Starting server...")

# Login with username + password
session = sa.login(SCRATCH_USER, SCRATCH_PASS)
cloud = session.connect_cloud(PROJECT_ID)

logger.info("Successfully logged in and connected to cloud!")

# Test comment (optional - remove later)
try:
    project = session.connect_project(PROJECT_ID)
    project.post_comment("Server is online - " + time.strftime("%Y-%m-%d %H:%M:%S"))
    logger.info("Test comment posted!")
except Exception as e:
    logger.error(f"Comment error: {e}")

# Keep the server running
while True:
    time.sleep(30)
    logger.info("Server is still running...")
