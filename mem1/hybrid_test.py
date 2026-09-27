from encryption.hybrid import hybrid_encrypt, hybrid_decrypt
from encryption.rsa import generate_rsa_key_pair


# Generate receiver's RSA key pair
private_key, public_key = generate_rsa_key_pair()

print("✓ RSA key pair generated")


# Original data
original_data = b"Hello! This is a secure file transfer test."

print("Original data:")
print(original_data)


# Encrypt
package = hybrid_encrypt(
    original_data,
    public_key
)

print("\n✓ Hybrid encryption successful")


# Decrypt
decrypted_data = hybrid_decrypt(
    package,
    private_key
)

print("\n✓ Hybrid decryption successful")

print("Decrypted data:")
print(decrypted_data)


# Verify
if decrypted_data == original_data:
    print("\n✓ Hybrid encryption/decryption test successful")
else:
    print("\n✗ Data verification failed")
# Test tampering detection
print("\nTesting tampering detection...")

tampered_package = package.copy()

# Modify one byte of the ciphertext
tampered_ciphertext = bytearray(tampered_package["ciphertext"])
tampered_ciphertext[0] ^= 1

tampered_package["ciphertext"] = bytes(tampered_ciphertext)

try:
    hybrid_decrypt(
        tampered_package,
        private_key
    )

    print("✗ Tampering was not detected")

except Exception:
    print("✓ Hybrid tampering detected successfully")