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


def send_and_receive(sock, message, address, max_retries=5):
    timeout = 1.0  # 初始超时1秒
    for attempt in range(max_retries):
        try:
            sock.sendto(message.encode(), address)
            sock.settimeout(timeout)
            response, _ = sock.recvfrom(2048)
            return response.decode()
        except socket.timeout:
            print(f"Timeout (attempt {attempt+1}), retrying...")
            timeout *= 2  # 每次超时后等待时间翻倍
    return None


def download_file(client_sock, filename, server_addr, server_port):
    # 1. 发送下载请求
    message = f"DOWNLOAD {filename}"
    response = send_and_receive(client_sock, message, (server_addr, server_port))

    if not response:
        print("Server not responding. Aborting download.")
        return False

    if response.startswith("ERR"):
        print(f"Error: {response.split(' ', 1)[1]}")
        return False

    # 2. 解析服务器响应 (OK SIZE 1234 PORT 5678)
    parts = response.split()
    file_size = int(parts[parts.index("SIZE") + 1])
    port = int(parts[parts.index("PORT") + 1])
    print(f"Downloading {filename} ({file_size} bytes)")

    # 3. 创建专门用于文件传输的套接字
    transfer_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    received = 0  # 已接收字节数
    blocks = 0  # 接收的块数

    try:
        with open(filename, 'wb') as f:
            # 4. 循环下载文件块
            while received < file_size:
                # 计算当前块的起始和结束位置
                start = received
                end = min(start + 999, file_size - 1)

                # 请求文件块
                request = f"FILE {filename} GET START {start} END {end}"
                response = send_and_receive(transfer_sock, request, (server_addr, port))

                if not response:
                    print("Transfer failed. Aborting.")
                    return False

                if "OK" in response:
                    # 提取并解码Base64数据
                    data_start = response.find("DATA ") + 5
                    b64_data = response[data_start:]
                    chunk = base64.b64decode(b64_data)

                    # 写入文件并更新状态
                    f.write(chunk)
                    received += len(chunk)
                    blocks += 1
                    print('*', end='', flush=True)  # 进度显示

            # 5. 传输结束处理
            close_msg = f"FILE {filename} CLOSE"
            close_resp = send_and_receive(transfer_sock, close_msg, (server_addr, port))

            if close_resp and "CLOSE_OK" in close_resp:
                print(f"\n{filename} download complete ({blocks} blocks)")
                return True
    finally:
        transfer_sock.close()

    return False


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