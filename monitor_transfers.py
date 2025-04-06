import json
import time
import os

LOG_FILE = "transfer_log.json"

def check_last_transfer():
    if not os.path.exists(LOG_FILE):
        print("[!] No transfers found.")
        return
    
    with open(LOG_FILE, 'r') as f:
        logs = json.load(f)
        
    if not logs:
        print("[!] Transfer log is empty.")
        return
    
    last_transfer = logs[-1]
    filename = last_transfer["filename"]
    status = last_transfer["status"]
    timestamp = last_transfer["timestamp"]
    
    if status.lower() != "success":
        print(f"[ALERT] Last transfer FAILED!\nFile: {filename}\nTime: {timestamp}")
    else:
        print(f"[OK] Last transfer succeeded.\nFile: {filename}\nTime: {timestamp}")

if __name__ == "__main__":
    while True:
        check_last_transfer()
        time.sleep(60)