import socket
import os
import base64
import sys
import time


def send_and_receive(sock, message, address, max_retries=5):
    timeout = 1.0
    for attempt in range(max_retries):
        try:
            sock.sendto(message.encode(), address)
            sock.settimeout(timeout)
            response, _ = sock.recvfrom(2048)
            return response.decode()
        except socket.timeout:
            print(f"Timeout (attempt {attempt + 1}), retrying...")
            timeout *= 2
    return None


def download_file(client_sock, filename, server_addr, server_port):
    # Send DOWNLOAD request
    message = f"DOWNLOAD {filename}"
    response = send_and_receive(client_sock, message, (server_addr, server_port))

    if not response:
        print("Server not responding. Aborting download.")
        return False

    if response.startswith("ERR"):
        print(f"Error: {response.split(' ', 1)[1]}")
        return False

    # Parse OK response
    parts = response.split()
    file_size = int(parts[parts.index("SIZE") + 1])
    port = int(parts[parts.index("PORT") + 1])
    print(f"Downloading {filename} ({file_size} bytes)")

    # Create file transfer socket
    transfer_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    received = 0
    blocks = 0

    with open(filename, 'wb') as f:
        while received < file_size:
            start = received
            end = min(start + 999, file_size - 1)

            # Request file chunk
            request = f"FILE {filename} GET START {start} END {end}"
            response = send_and_receive(transfer_sock, request, (server_addr, port))

            if not response:
                print("Transfer failed. Aborting.")
                return False

            if "OK" in response:
                data_start = response.find("DATA ") + 5
                b64_data = response[data_start:]
                chunk = base64.b64decode(b64_data)
                f.write(chunk)
                received += len(chunk)
                blocks += 1
                print('*', end='', flush=True)

        # Close transfer
        close_msg = f"FILE {filename} CLOSE"
        close_resp = send_and_receive(transfer_sock, close_msg, (server_addr, port))

        if close_resp and "CLOSE_OK" in close_resp:
            print(f"\n{filename} download complete ({blocks} blocks)")
            return True

    return False


def main():
    if len(sys.argv) != 4:
        print("Usage: python3 UDPclient.py <HOST> <PORT> <FILELIST>")
        return

    host = sys.argv[1]
    port = int(sys.argv[2])
    filelist = sys.argv[3]

    client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    with open(filelist, 'r') as f:
        for line in f:
            filename = line.strip()
            if filename:
                download_file(client_sock, filename, host, port)

    client_sock.close()


if __name__ == "__main__":
    main()
