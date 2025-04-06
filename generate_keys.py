from cryptography.fernet import Fernet
import time
import os

KEY_FOLDER = "keys"  # Folder to store all keys

def generate_key():
    if not os.path.exists(KEY_FOLDER):
        os.makedirs(KEY_FOLDER)

    key = Fernet.generate_key()
    timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"secret_{timestamp}.key"
    
    with open(os.path.join(KEY_FOLDER, filename), 'wb') as key_file:
        key_file.write(key)
    
    with open('secret.key', 'wb') as latest_key_file:
        latest_key_file.write(key)

    print(f"[+] New encryption key generated and saved as '{filename}'.")
    print("[+] 'secret.key' updated as the latest active key.")

if __name__ == "__main__":
    generate_key()