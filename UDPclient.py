import socket
import os
import base64
import sys
import time
#graph TD
    #A[启动客户端] --> B[解析命令行参数]


    #B --> C[读取文件列表]
    #C --> D[遍历文件列表]
    #D --> E[下载单个文件]
    #E --> F[发送DOWNLOAD请求]
    #F --> G{收到响应?}
    #G --> |是| H[解析OK响应]
    #G --> |否| I[重试或放弃]
    #H --> J[创建传输套接字]
    #J --> K[循环请求数据块]
    #K --> L[发送FILE GET请求]
    #L --> M{收到数据响应?}
    #M --> |是| N[解码并保存数据]
    #M --> |否| O[重试或放弃]
    #N --> P{下载完成?}
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


import socket
import sys


def main():
    host = sys.argv[1]
    port = sys.argv[2]
    filelist = sys.argv[3]

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    f = open(filelist)
    for line in f:
        filename = line

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