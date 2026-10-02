import os

from encryption.file_crypto import (
    encrypt_file,
    decrypt_file,
    load_encrypted_package
)

from encryption.rsa import (
    generate_rsa_key_pair,
    save_rsa_keys
)


# ============================================================
# TEST PATHS
# ============================================================

TEST_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

TEST_KEYS_DIR = os.path.join(
    TEST_DIR,
    "test_file_keys"
)

INPUT_FILE = os.path.join(
    TEST_DIR,
    "sample_test_file.txt"
)

ENCRYPTED_PACKAGE = os.path.join(
    TEST_DIR,
    "encrypted_test_package.json"
)

RECOVERED_FILE = os.path.join(
    TEST_DIR,
    "recovered_test_file.txt"
)

PRIVATE_KEY = os.path.join(
    TEST_KEYS_DIR,
    "private.pem"
)

PUBLIC_KEY = os.path.join(
    TEST_KEYS_DIR,
    "public.pem"
)


def main():

    print("Testing file-level AES + RSA encryption...")
    print()

    # ========================================================
    # CREATE TEST FILE
    # ========================================================

    original_text = (
        "This is a real file-level encryption test.\n"
        "Secure File Transfer Project\n"
        "AES-256-GCM + RSA-3072"
    )

    with open(
        INPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            original_text
        )

    print("✓ Test file created")

    # ========================================================
    # GENERATE RSA KEYS
    # ========================================================

    os.makedirs(
        TEST_KEYS_DIR,
        exist_ok=True
    )

    private_key, public_key = generate_rsa_key_pair()

    save_rsa_keys(
        private_key,
        public_key,
        PRIVATE_KEY,
        PUBLIC_KEY
    )

    print("✓ RSA-3072 test keys generated")

    # ========================================================
    # ENCRYPT FILE
    # ========================================================

    encrypt_file(
        INPUT_FILE,
        ENCRYPTED_PACKAGE,
        PUBLIC_KEY
    )

    print("✓ File encrypted")

    # ========================================================
    # VERIFY PACKAGE EXISTS
    # ========================================================

    assert os.path.exists(
        ENCRYPTED_PACKAGE
    )

    print("✓ Encrypted JSON package created")

    # ========================================================
    # LOAD PACKAGE
    # ========================================================

    package = load_encrypted_package(
        ENCRYPTED_PACKAGE
    )

    assert isinstance(
        package["ciphertext"],
        bytes
    )

    assert isinstance(
        package["encrypted_aes_key"],
        bytes
    )

    assert isinstance(
        package["nonce"],
        bytes
    )

    assert isinstance(
        package["authentication_tag"],
        bytes
    )

    print("✓ Encrypted package decoded successfully")

    # ========================================================
    # DECRYPT FILE
    # ========================================================

    decrypt_file(
        ENCRYPTED_PACKAGE,
        RECOVERED_FILE,
        PRIVATE_KEY
    )

    print("✓ File decrypted")

    # ========================================================
    # COMPARE ORIGINAL AND RECOVERED FILE
    # ========================================================

    with open(
        INPUT_FILE,
        "rb"
    ) as file:

        original_data = file.read()

    with open(
        RECOVERED_FILE,
        "rb"
    ) as file:

        recovered_data = file.read()

    assert recovered_data == original_data

    print("✓ Original and recovered files are identical")

    # ========================================================
    # FINAL RESULT
    # ========================================================

    print()
    print("✓ FILE-LEVEL CRYPTO TEST SUCCESSFUL")


if __name__ == "__main__":
    main()