import base64


filename = "mem2/test_file.txt"


# Read the file as bytes
with open(filename, "rb") as file:
    file_data = file.read()


# Convert bytes to Base64
encoded_data = base64.b64encode(file_data).decode("utf-8")

print("Base64 encoded data:")
print(encoded_data)


# Convert Base64 back to bytes
decoded_data = base64.b64decode(encoded_data)


# Save decoded data
with open("mem2/recovered_test_file.txt", "wb") as file:
    file.write(decoded_data)


print("\n✓ File successfully encoded and decoded")