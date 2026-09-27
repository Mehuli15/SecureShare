import hashlib


def calculate_file_hash(filename):
    sha256 = hashlib.sha256()

    with open(filename, "rb") as file:
        while chunk := file.read(4096):
            sha256.update(chunk)

    return sha256.hexdigest()


def verify_file_hash(filename, expected_hash):
    actual_hash = calculate_file_hash(filename)

    return actual_hash == expected_hash


filename = "mem2/sample.txt"

# Calculate the original hash
original_hash = calculate_file_hash(filename)

print("Original SHA-256:")
print(original_hash)

# Verify the file
if verify_file_hash(filename, original_hash):
    print("\n✓ File integrity verified")
else:
    print("\n✗ File has been modified")