import scratchattach as sa
import os
import time
import logging

SCRATCH_USER = os.getenv("SCRATCH_USER")
SCRATCH_PASS = os.getenv("SCRATCH_PASS")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Attempting login...")

session = sa.login(SCRATCH_USER, SCRATCH_PASS)
logger.info("Logged in successfully!")

# Test comment
try:
    project = session.connect_project(123456789)  # Change to your project ID
    project.post_comment("Test from server - " + time.strftime("%Y-%m-%d %H:%M:%S"))
    logger.info("Comment posted!")
except Exception as e:
    logger.error(f"Error: {e}")

while True:
    time.sleep(30)
    logger.info("Server is running...")
