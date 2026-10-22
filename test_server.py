import socket
from http import HTTPStatus

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.bind(('127.0.0.1', 5000))
my_socket.listen()
while True:
    message = ''
    clientConnection, clientAddress = my_socket.accept()
    message += clientConnection.recv(1024).decode()
    try:
        status_line = f"HTTP/1.1 {HTTPStatus(int(message.split('\n')[0].split()[1][-3:]))} {HTTPStatus(int(message.split('\n')[0].split()[1][-3:])).phrase}\r\n"
        body = (
            f"Request Method: {message.split('\n')[0].split()[0]}\r\n"
            f"Request Source: {clientAddress}\r\n"
            f"Response Status: {HTTPStatus(int(message.split('\n')[0].split()[1][-3:]))} {HTTPStatus(int(message.split('\n')[0].split()[1][-3:])).phrase}\r\n"
        )
    except ValueError:
        status_line = f"HTTP/1.1 {HTTPStatus.OK} {HTTPStatus.OK.phrase}\r\n"
        body = (
            f"Request Method: {message.split('\n')[0].split()[0]}\r\n"
            f"Request Source: {clientAddress}\r\n"
            f"Response Status: {HTTPStatus.OK} {HTTPStatus.OK.phrase}\r\n"
        )
    for body_line in message.split('\n')[2:]:
        body += (f"{body_line}\n")
    headers = (
        "Content-Type: text/plain; charset=utf-8\r\n"
        "Connection: close\r\n"
    )
    response_bytes = status_line.encode() + headers.encode() + b"\r\n" + body.encode()
    clientConnection.send(response_bytes)
    clientConnection.close()