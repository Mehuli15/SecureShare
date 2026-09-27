from encryption.file_crypto import (
    encrypt_file,
    decrypt_file
)


# Encrypt the original file
encrypt_file(
    "mem2/sample.txt",
    "mem1/encrypted_package.json"
)

print("✓ File encryption and package saving successful")


# Decrypt the encrypted package
decrypt_file(
    "mem1/encrypted_package.json",
    "mem1/recovered_sample.txt"
)

print("✓ File decryption successful")


# Compare original and recovered files
with open("mem2/sample.txt", "rb") as original:
    original_data = original.read()

with open("mem1/recovered_sample.txt", "rb") as recovered:
    recovered_data = recovered.read()


if original_data == recovered_data:
    print("✓ Original and recovered files are identical")
else:
    print("✗ File verification failed")
from encryption.file_crypto import load_encrypted_package
from encryption.hybrid import hybrid_decrypt
from encryption.rsa import load_private_key


print("\nTesting package tampering...")

# Load the encrypted package
package = load_encrypted_package(
    "mem1/encrypted_package.json"
)

# Make a copy so the original package remains unchanged
tampered_package = package.copy()

# Modify one byte of the ciphertext
tampered_ciphertext = bytearray(
    tampered_package["ciphertext"]
)

tampered_ciphertext[0] ^= 1

tampered_package["ciphertext"] = bytes(
    tampered_ciphertext
)

# Load receiver's private key
private_key = load_private_key(
    "mem1/keys/private.pem"
)

# Try to decrypt the modified package
try:
    hybrid_decrypt(
        tampered_package,
        private_key
    )

    print("✗ Tampering was not detected")

except Exception:
    print("✓ Package tampering detected successfully")