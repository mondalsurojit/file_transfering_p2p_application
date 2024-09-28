import socket
import tqdm
import os

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096  # Send 4096 bytes each time step
class Transfer:
    def establish_connection(host, port, is_sender):
        s = socket.socket()
        if is_sender:
            print("[*] Waiting for the receiver to connect...")
            s.bind((host, port))
            s.listen(5)  # Allow up to 5 connections
            client_socket, address = s.accept()
            print(f"[+] Connected to {address}.")
            return client_socket
        else:  # Receiver connects to the sender
            print(f"[+] Connecting to {host}:{port}...")
            s.connect((host, port))
            print("[+] Connected.")
            return s

    def send_file(s, filename):
        filesize = os.path.getsize(filename)
        s.send(f"{filename}{SEPARATOR}{filesize}".encode())
        
        # Start sending the file
        progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        
        with open(filename, "rb") as f:
            while True:
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    break
                s.sendall(bytes_read)
                progress.update(len(bytes_read))
        
        print("[+] File sent successfully.")
        s.close()

    def receive_file(s):
        received = s.recv(BUFFER_SIZE).decode()
        filename, filesize = received.split(SEPARATOR)
        
        filesize = int(filesize)

        # Prompt the receiver to enter a directory to save the file
        save_directory = input("Enter the directory where you want to save the file: ")

        # Construct full save path using the original filename from sender
        save_path = os.path.join(save_directory, os.path.basename(filename))

        # Ensure the directory exists or create it
        os.makedirs(save_directory, exist_ok=True)

        with open(save_path, "wb") as f:
            progress = tqdm.tqdm(range(filesize), f"Receiving {os.path.basename(filename)}", unit="B", unit_scale=True, unit_divisor=1024)

            while True:
                bytes_read = s.recv(BUFFER_SIZE)
                if not bytes_read:
                    break
                f.write(bytes_read)
                progress.update(len(bytes_read))
        
        print("[+] File received successfully.")
        s.close()

def main():
    my_transfer=Transfer()
    mode = input("Do you want to send or receive a file? (send/receive): ").strip().lower()
    
    if mode == "receive":
        host = input("Enter the sender's IP address: ")
        port = int(input("Enter the sender's port number: "))
        
        s = my_transfer.establish_connection(host, port, is_sender=False)
        
        my_transfer.receive_file(s)

    elif mode == "send":
        host = input("Enter your IP address (or '0.0.0.0' to listen on all interfaces): ")
        port = int(input("Enter your desired port number: "))
        
        s = my_transfer.establish_connection(host, port, is_sender=True)
        
        filename = input("Enter the path of the file to send: ")
        
        my_transfer.send_file(s, filename)

    else:
        print("Invalid option. Please enter 'send' or 'receive'.")

if __name__ == "__main__":
    main()