import socket
import json


HOST = "127.0.0.1"
PORT = 5000


# Read the secure package
with open("mem2/test_secure_package.json", "r") as file:
    package = json.load(file)


# Convert package to JSON text
message = json.dumps(package)


# Create socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((HOST, PORT))

# Send package
client.sendall(message.encode())

print("✓ Secure package sent successfully")

client.close()