import os
import time

print("=== SERVER STARTING ===")
print("SCRATCH_USER is set:", "Yes" if os.getenv("SCRATCH_USER") else "No")
print("PROJECT_ID is set:", "Yes" if os.getenv("PROJECT_ID") else "No")

print("Server is running...")

while True:
    time.sleep(30)
