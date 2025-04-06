import paramiko

def search_files(host, port, username, password, remote_path, keyword):
    transport = paramiko.Transport((host, port))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    
    files = sftp.listdir(remote_path)
    
    matches = [file for file in files if keyword.lower() in file.lower()]
    
    if matches:
        print(f"\n[+] Files matching '{keyword}':")
        for match in matches:
            print(f" - {match}")
    else:
        print(f"[!] No files found matching '{keyword}'.")
    
    sftp.close()
    transport.close()

if __name__ == "__main__":
    host = input("Enter SFTP host: ").strip()
    port = int(input("Enter SFTP port (default 22): ").strip() or "22")
    username = input("Enter SFTP username: ").strip()
    password = input("Enter SFTP password: ").strip()
    remote_path = input("Enter remote path on server (e.g., /home/user/uploads/): ").strip()

    keyword = input("Enter search keyword: ").strip()
    search_files(host, port, username, password, remote_path, keyword)