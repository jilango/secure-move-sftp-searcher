import paramiko
import os
import time
import json
from cryptography.fernet import Fernet

MAX_RETRIES = 3
KEY_ROTATE_INTERVAL = 5
LOG_FILE = "transfer_log.json"
BACKOFF_DELAYS = [5, 10, 20]

upload_count = 0

def load_key():
    return open('secret.key', 'rb').read()

def encrypt_file(file_path):
    key = load_key()
    fernet = Fernet(key)
    
    with open(file_path, 'rb') as file:
        original = file.read()
        
    encrypted = fernet.encrypt(original)
    
    encrypted_file_path = file_path + ".enc"
    with open(encrypted_file_path, 'wb') as enc_file:
        enc_file.write(encrypted)
        
    print(f"[+] File encrypted: {encrypted_file_path}")
    return encrypted_file_path

def upload_file(local_file, remote_file, host, port, username, password):
    retries = 0
    while retries < MAX_RETRIES:
        try:
            transport = paramiko.Transport((host, port))
            transport.connect(username=username, password=password)
            sftp = paramiko.SFTPClient.from_transport(transport)
            
            sftp.put(local_file, remote_file)
            print(f"[+] Upload successful: {local_file} -> {remote_file}")
            
            sftp.close()
            transport.close()
            return True
        except Exception as e:
            print(f"[!] Upload failed (Attempt {retries + 1}/{MAX_RETRIES}): {str(e)}")
            delay = BACKOFF_DELAYS[min(retries, len(BACKOFF_DELAYS) - 1)]
            print(f"[*] Retrying in {delay} seconds...")
            time.sleep(delay)
            retries += 1
    return False

def log_transfer(filename, status):
    log_entry = {
        "filename": filename,
        "status": status,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    if not os.path.exists(LOG_FILE):
        logs = []
    else:
        with open(LOG_FILE, 'r') as f:
            logs = json.load(f)
    
    logs.append(log_entry)
    
    with open(LOG_FILE, 'w') as f:
        json.dump(logs, f, indent=4)
        
    print("[+] Transfer logged.")

def rotate_key():
    from generate_keys import generate_key
    generate_key()
    print("[*] Encryption key rotated.")

if __name__ == "__main__":
    host = input("Enter SFTP host: ").strip()
    port = int(input("Enter SFTP port (default 22): ").strip() or "22")
    username = input("Enter SFTP username: ").strip()
    password = input("Enter SFTP password: ").strip()
    remote_path = input("Enter remote path on server (e.g., /home/user/uploads/): ").strip()

    file_to_upload = input("Enter path of file to upload: ").strip()
    
    encrypted_file = encrypt_file(file_to_upload)
    
    remote_filename = os.path.basename(encrypted_file)
    
    success = upload_file(encrypted_file, remote_path + remote_filename, host, port, username, password)
    
    log_transfer(remote_filename, "Success" if success else "Failure")
    
    upload_count += 1
    if upload_count % KEY_ROTATE_INTERVAL == 0:
        rotate_key()