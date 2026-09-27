from encryption.aes import generate_aes_key, encrypt_data, decrypt_data

# Generate AES key
key = generate_aes_key()

# Data to encrypt
message = b"Hello! This is a secret message."

# Encrypt
ciphertext, nonce, authentication_tag = encrypt_data(
    message,
    key
)

print("AES encryption successful.")
print("Original message:", message)
print("Ciphertext:", ciphertext.hex())
print("Nonce:", nonce.hex())
print("Authentication tag:", authentication_tag.hex())

# Decrypt
decrypted = decrypt_data(
    ciphertext,
    key,
    nonce,
    authentication_tag
)

print("\nDecrypted message:", decrypted)

# Verify
if decrypted == message:
    print("✓ AES decryption successful")
else:
    print("✗ Decryption failed")
# Test tampering
tampered_ciphertext = bytearray(ciphertext)

# Change one byte
tampered_ciphertext[0] ^= 1

try:
    decrypt_data(
        bytes(tampered_ciphertext),
        key,
        nonce,
        authentication_tag
    )

    print("✗ Tampering was NOT detected")

except Exception:
    print("✓ Tampering detected successfully")