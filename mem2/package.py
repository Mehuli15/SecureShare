import base64
import json


def encode_data(data):
    return base64.b64encode(data).decode("utf-8")


def decode_data(data):
    return base64.b64decode(data)


def create_package(encrypted_file, encrypted_aes_key, nonce, authentication_tag):
    package = {
        "encrypted_file": encode_data(encrypted_file),
        "encrypted_aes_key": encode_data(encrypted_aes_key),
        "nonce": encode_data(nonce),
        "authentication_tag": encode_data(authentication_tag)
    }

    return package


def save_package(package, filename):
    with open(filename, "w") as file:
        json.dump(package, file, indent=4)


print("Package module ready")