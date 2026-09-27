from encryption.rsa import (
    generate_rsa_key_pair,
    save_rsa_keys,
    load_private_key,
    load_public_key,
    encrypt_aes_key,
    decrypt_aes_key
)

from Crypto.Random import get_random_bytes
import os


# Create keys folder
os.makedirs("mem1/keys", exist_ok=True)


# Generate RSA keys
private_key, public_key = generate_rsa_key_pair()

print("✓ RSA key pair generated")


# Save keys
save_rsa_keys(
    private_key,
    public_key,
    "mem1/keys/private.pem",
    "mem1/keys/public.pem"
)

print("✓ RSA keys saved")


# Load keys again
loaded_private_key = load_private_key(
    "mem1/keys/private.pem"
)

loaded_public_key = load_public_key(
    "mem1/keys/public.pem"
)

print("✓ RSA keys loaded")


# Generate AES key
aes_key = get_random_bytes(32)


# Encrypt AES key using loaded public key
encrypted_aes_key = encrypt_aes_key(
    aes_key,
    loaded_public_key
)

print("✓ AES key encrypted")


# Decrypt AES key using loaded private key
decrypted_aes_key = decrypt_aes_key(
    encrypted_aes_key,
    loaded_private_key
)

print("✓ AES key decrypted")


# Verify
if decrypted_aes_key == aes_key:
    print("✓ Saved/loaded RSA keys work successfully")
else:
    print("✗ Key verification failed")