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