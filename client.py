#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 文件名：tcpclient.py
 
import socket
import time
MaxBytes=1024*1024
host ='127.0.0.1'
port = 9998

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.settimeout(30)
client.connect((host,port))
# recvData = client.recv(MaxBytes)
# if recvData:
#     localTime = time.asctime( time.localtime(time.time()))
#     print(localTime, ' 接收到数据字节数:',len(recvData))
#     print(recvData.decode())
while True:
    inputData=input();          #等待输入数据
    sendBytes = client.send(inputData.encode())
    if(inputData=="quit" or inputData =="exit"):
        print("我要退出了，再见")
        break
    if sendBytes<=0:
        break
    recvData = client.recv(MaxBytes)
    if not recvData:
        print('接收数据为空，我要退出了')
        break
    localTime = time.asctime( time.localtime(time.time()))
    print(localTime, ' 接收到数据字节数:',len(recvData))
    print(recvData.decode())
client.close()
print("我已经退出了，后会无期")