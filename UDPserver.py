import socket
import os
import threading
import random
import base64


class FileTransferThread(threading.Thread):
    def __init__(self, filename, client_addr, server_port):
        super().__init__()
        self.filename = filename
        self.client_addr = client_addr
        self.port = random.randint(50000, 51000)
        self.server_port = server_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', self.port))
        self.sock.settimeout(5.0)
        self.file_path = os.path.join(os.getcwd(), filename)

    def run(self):
        try:
            file_size = os.path.getsize(self.file_path)
            response = f"OK {self.filename} SIZE {file_size} PORT {self.port}"
            self.sock.sendto(response.encode(), self.client_addr)

            with open(self.file_path, 'rb') as f:
                while True:
                    try:
                        data, addr = self.sock.recvfrom(1024)
                        message = data.decode().split()

                        if message[0] == "FILE" and message[2] == "GET":
                            start = int(message[4])
                            end = int(message[6])
                            f.seek(start)
                            chunk = f.read(end - start + 1)
                            b64_data = base64.b64encode(chunk).decode()
                            response = f"FILE {self.filename} OK START {start} END {end} DATA {b64_data}"
                            self.sock.sendto(response.encode(), addr)

                        elif message[0] == "FILE" and message[2] == "CLOSE":
                            response = f"FILE {self.filename} CLOSE_OK"
                            self.sock.sendto(response.encode(), addr)
                            break

                    except socket.timeout:
                        continue

        except FileNotFoundError:
            response = f"ERR {self.filename} NOT_FOUND"
            self.sock.sendto(response.encode(), self.client_addr)
        finally:
            self.sock.close()
            
def main():
    if len(os.sys.argv) != 2:
        print("Usage: python3 UDPserver.py <PORT>")
        return

    port = int(os.sys.argv[1])
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', port))
    print(f"Server listening on port {port}")

    while True:
        data, addr = sock.recvfrom(1024)
        message = data.decode().split()

        if message[0] == "DOWNLOAD":
            filename = message[1]
            print(f"Download request for {filename} from {addr}")
            thread = FileTransferThread(filename, addr, port)
            thread.start()


if __name__ == "__main__":
    main()




