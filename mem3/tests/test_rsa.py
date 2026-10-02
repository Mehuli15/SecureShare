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


# ============================================================
# TEST DIRECTORY
# ============================================================

TEST_KEY_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "tests",
    "test_keys"
)

os.makedirs(
    TEST_KEY_DIR,
    exist_ok=True
)


PRIVATE_KEY_PATH = os.path.join(
    TEST_KEY_DIR,
    "private.pem"
)

PUBLIC_KEY_PATH = os.path.join(
    TEST_KEY_DIR,
    "public.pem"
)


# ============================================================
# GENERATE KEYS
# ============================================================

private_key, public_key = generate_rsa_key_pair()

print("✓ RSA-3072 key pair generated")


# ============================================================
# SAVE KEYS
# ============================================================

save_rsa_keys(
    private_key,
    public_key,
    PRIVATE_KEY_PATH,
    PUBLIC_KEY_PATH
)

print("✓ RSA keys saved")


# ============================================================
# LOAD KEYS
# ============================================================

loaded_private_key = load_private_key(
    PRIVATE_KEY_PATH
)

loaded_public_key = load_public_key(
    PUBLIC_KEY_PATH
)

print("✓ RSA keys loaded")


# ============================================================
# GENERATE AES KEY
# ============================================================

aes_key = get_random_bytes(32)

print(
    "AES key length:",
    len(aes_key),
    "bytes"
)


# ============================================================
# ENCRYPT AES KEY
# ============================================================

encrypted_aes_key = encrypt_aes_key(
    aes_key,
    loaded_public_key
)

print("✓ AES key encrypted using RSA")


# ============================================================
# DECRYPT AES KEY
# ============================================================

decrypted_aes_key = decrypt_aes_key(
    encrypted_aes_key,
    loaded_private_key
)

print("✓ AES key decrypted using RSA")


# ============================================================
# VERIFY
# ============================================================

if decrypted_aes_key == aes_key:

    print(
        "✓ RSA encryption/decryption successful"
    )

else:

    print(
        "✗ RSA verification failed"
    )