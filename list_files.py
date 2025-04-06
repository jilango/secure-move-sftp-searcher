import paramiko

def list_files(host, port, username, password, remote_path):
    transport = paramiko.Transport((host, port))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    
    files = sftp.listdir(remote_path)
    
    print("\n[+] Files on SFTP Server:")
    for file in files:
        print(f" - {file}")
    
    sftp.close()
    transport.close()

if __name__ == "__main__":
    host = input("Enter SFTP host: ").strip()
    port = int(input("Enter SFTP port (default 22): ").strip() or "22")
    username = input("Enter SFTP username: ").strip()
    password = input("Enter SFTP password: ").strip()
    remote_path = input("Enter remote path on server (e.g., /home/user/uploads/): ").strip()

    list_files(host, port, username, password, remote_path)