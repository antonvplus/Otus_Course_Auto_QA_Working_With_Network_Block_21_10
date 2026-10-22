import socket
from http import HTTPStatus

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.bind(('127.0.0.1', 5000))
my_socket.listen()
while True:
    message = ''
    clientConnection, clientAddress = my_socket.accept()
    message += clientConnection.recv(1024).decode()
    if not message.split('\n')[0].split()[1][-3:].isdigit():
        status_line = f"HTTP/1.1 {HTTPStatus.OK} {HTTPStatus.OK.phrase}\r\n"
        headers = (
            f"Request Method: {message.split('\n')[0].split()[0]}\r\n"
            f"Request Source: {clientAddress}\r\n"
            f"Response Status: {HTTPStatus.OK} {HTTPStatus.OK.phrase}\r\n"
            f"header-name: {message.split('\n')[2:]}\r\n"
            f"\r\n"  # ВАЖНО: пустая строка отделяет заголовки от тела
        )
    else:
        status_line = f"HTTP/1.1 {HTTPStatus(int(message.split('\n')[0].split()[1][-3:]))} {HTTPStatus(int(message.split('\n')[0].split()[1][-3:])).phrase}\r\n"
        headers = (
            f"Request Method: {message.split('\n')[0].split()[0]}\r\n"
            f"Request Source: {clientAddress}\r\n"
            f"Response Status: {HTTPStatus(int(message.split('\n')[0].split()[1][-3:]))} {HTTPStatus(int(message.split('\n')[0].split()[1][-3:])).phrase}\r\n"
            f"header-name: {message.split('\n')[2:]}\r\n"
            f"\r\n"
        )
    response_bytes = status_line.encode() + b"\r\n" + headers.encode()
    clientConnection.send(response_bytes)
    clientConnection.close()