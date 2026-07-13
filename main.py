import scratchattach as sa
import os
import time
import logging

SCRATCH_SESSION = os.getenv("SCRATCH_SESSION")
PROJECT_ID = os.getenv("PROJECT_ID")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Attempting to login with session ID...")

session = sa.Session(SCRATCH_SESSION)
cloud = session.connect_cloud(PROJECT_ID)

logger.info("Server started successfully!")

while True:
    time.sleep(30)
    logger.info("Server is alive")
