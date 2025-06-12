import socket
import os
import threading
import random
import base64

#graph TD
    #A[启动服务器] --> B[绑定主端口]
    #B --> C[等待客户端请求]
    #C --> D{收到DOWNLOAD请求?}
    #D --> |是| E[创建传输线程]
    #E --> F[线程初始化]
    #F --> G[检查文件存在性]
    #G --> |存在| H[发送OK响应]
    #G --> |不存在| I[发送ERR响应]
    #H --> J[等待数据请求]
    #J --> K{收到FILE GET?}
    #K --> |是| L[读取文件块]
    #L --> M[Base64编码]
    #M --> N[发送数据响应]
    #N --> J
    #K --> |收到CLOSE| O[发送CLOSE_OK]
    ##O --> P[关闭连接]
    #I --> P


def main():
    # 检查参数
    if len(os.sys.argv) != 2:
        print("Usage: python3 UDPserver.py <PORT>")
        return

    port = int(os.sys.argv[1])

    # 创建主socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', port))
    print(f"Server listening on port {port}")

    while True:
        # 接收请求
        data, addr = sock.recvfrom(1024)
        message = data.decode().split()

        # 处理下载请求
        if message[0] == "DOWNLOAD":
            filename = message[1]
            print(f"Download request for {filename} from {addr}")
            # 这里会创建传输线程


if __name__ == "__main__":
    main()