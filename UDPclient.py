import socket
import os
import base64
import sys
import time
#graph TD

    #P --> |否| K
    #P --> |是| Q[发送CLOSE请求]
    #Q --> R{收到CLOSE_OK?}
    #R --> |是| S[文件下载成功]
    #R --> |否| T[重试或放弃]
    #S --> U[下载下一个文件]
    #T --> U
    #U --> V{更多文件?}
    #V --> |是| D
    #V --> |否| W[关闭套接字退出]

def main():
    # 基本参数检查
    if len(sys.argv) != 4:
        print("Usage: python3 UDPclient.py <HOST> <PORT> <FILELIST>")
        return

    host = sys.argv[1]
    port = int(sys.argv[2])
    filelist = sys.argv[3]

    # 创建UDP套接字
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 读取文件列表并处理
    with open(filelist, 'r') as f:
        for line in f:
            filename = line.strip()
            if filename:
                # 这里会调用下载函数
                pass

    client_sock.close()


if __name__ == "__main__":
    main()

    

def send_and_receive(sock, message, address, max_retries=5):
    for i in range(max_retries):
        try:
            sock.sendto(message, address)
            data, addr = sock.recv(65535)
            return data
        except:
            print("Error happened")
            continue

    return -1


def download_file(client_sock, filename, server_addr, server_port):
    client_sock.sendto(f"GET {filename}".encode(), (server_addr, server_port))
    data, _ = client_sock.recvfrom(1024)
    file_size = int(data.split()[1])

    f = open(filename, 'wb')

    received = 0
    while received < file_size:
        chunk, _ = client_sock.recvfrom(file_size)
        f.write(chunk)
        received += len(chunk)

    def main():
        # ... (之前的参数检查代码不变)

        client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:
            with open(filelist, 'r') as f:
                for line in f:
                    filename = line.strip()
                    if filename:
                        if not download_file(client_sock, filename, host, port):
                            print(f"Failed to download {filename}")
        finally:
            client_sock.close()