import paramiko
from cryptography.fernet import Fernet
import os

def load_key():
    return open('secret.key', 'rb').read()

def download_file(host, port, username, password, remote_path, filename, local_folder):
    if not os.path.exists(local_folder):
        os.makedirs(local_folder)
        
    transport = paramiko.Transport((host, port))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    
    local_path = os.path.join(local_folder, filename)
    remote_file_path = remote_path + filename
    
    sftp.get(remote_file_path, local_path)
    print(f"[+] File downloaded to: {local_path}")
    
    sftp.close()
    transport.close()
    
    return local_path

def decrypt_file(encrypted_file_path):
    key = load_key()
    fernet = Fernet(key)
    
    with open(encrypted_file_path, 'rb') as enc_file:
        encrypted_data = enc_file.read()
    
    decrypted_data = fernet.decrypt(encrypted_data)
    
    original_file_path = encrypted_file_path.replace(".enc", "")
    
    with open(original_file_path, 'wb') as dec_file:
        dec_file.write(decrypted_data)
    
    print(f"[+] File decrypted: {original_file_path}")

if __name__ == "__main__":
    host = input("Enter SFTP host: ").strip()
    port = int(input("Enter SFTP port (default 22): ").strip() or "22")
    username = input("Enter SFTP username: ").strip()
    password = input("Enter SFTP password: ").strip()
    remote_path = input("Enter remote path on server (e.g., /home/user/uploads/): ").strip()
    local_folder = input("Enter local download folder (default 'downloads/'): ").strip() or "downloads"

    filename = input("Enter the filename to download and decrypt (including .enc): ").strip()
    downloaded_file = download_file(host, port, username, password, remote_path, filename, local_folder)
    decrypt_file(downloaded_file)