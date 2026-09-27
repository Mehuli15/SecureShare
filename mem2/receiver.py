import socket
import json
import base64

HOST = "127.0.0.1"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Receiver is waiting for sender...")

connection, address = server.accept()
print("Sender connected:", address)

data = b""

while True:
    chunk = connection.recv(4096)
    if not chunk:
        break
    data += chunk

package = json.loads(data.decode())

# Decode Base64 data back into bytes
encrypted_file = base64.b64decode(package["encrypted_file"])
encrypted_aes_key = base64.b64decode(package["encrypted_aes_key"])
nonce = base64.b64decode(package["nonce"])
authentication_tag = base64.b64decode(package["authentication_tag"])

print("\n✓ Secure package received and decoded")
print()
print("Encrypted file:", encrypted_file)
print("Encrypted AES key:", encrypted_aes_key)
print("Nonce:", nonce)
print("Authentication tag:", authentication_tag)

connection.close()
server.close()