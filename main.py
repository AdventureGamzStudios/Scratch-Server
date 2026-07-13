import scratchattach as sa
import os
import time
import logging

SCRATCH_SESSION = os.getenv("SCRATCH_SESSION")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Testing session ID...")

try:
    session = sa.Session(SCRATCH_SESSION)
    logger.info("Login successful!")
    logger.info("Session ID length:", len(SCRATCH_SESSION))
except Exception as e:
    logger.error("Login failed: " + str(e))

while True:
    time.sleep(30)
