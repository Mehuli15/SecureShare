from encryption.hybrid import (
    hybrid_encrypt,
    hybrid_decrypt
)

from encryption.rsa import (
    generate_rsa_key_pair
)


def main():

    print("Testing Hybrid AES + RSA encryption...")
    print()

    # ========================================================
    # GENERATE RSA KEY PAIR
    # ========================================================

    private_key, public_key = generate_rsa_key_pair()

    print("✓ RSA-3072 key pair generated")

    # ========================================================
    # ORIGINAL DATA
    # ========================================================

    original_data = (
        b"This is a test message for hybrid AES and RSA encryption."
    )

    # ========================================================
    # HYBRID ENCRYPTION
    # ========================================================

    package = hybrid_encrypt(
        original_data,
        public_key
    )

    print("✓ Hybrid encryption successful")

    # ========================================================
    # CHECK PACKAGE STRUCTURE
    # ========================================================

    expected_keys = {
        "ciphertext",
        "encrypted_aes_key",
        "nonce",
        "authentication_tag"
    }

    assert set(package.keys()) == expected_keys

    print("✓ Package structure verified")

    # Check that all encrypted components are bytes
    assert isinstance(package["ciphertext"], bytes)
    assert isinstance(package["encrypted_aes_key"], bytes)
    assert isinstance(package["nonce"], bytes)
    assert isinstance(package["authentication_tag"], bytes)

    print("✓ All package components are bytes")

    print(
        f"Encrypted AES key length: "
        f"{len(package['encrypted_aes_key'])} bytes"
    )

    # RSA-3072 encrypted data should be 384 bytes
    assert len(package["encrypted_aes_key"]) == 384

    print("✓ RSA-3072 encrypted AES key size verified")

    # ========================================================
    # HYBRID DECRYPTION
    # ========================================================

    decrypted_data = hybrid_decrypt(
        package,
        private_key
    )

    print("✓ Hybrid decryption successful")

    # ========================================================
    # VERIFY ORIGINAL DATA
    # ========================================================

    assert decrypted_data == original_data

    print("✓ Original data recovered successfully")

    # ========================================================
    # TAMPERING TEST
    # ========================================================

    tampered_package = package.copy()

    tampered_ciphertext = bytearray(
        tampered_package["ciphertext"]
    )

    tampered_ciphertext[0] ^= 1

    tampered_package["ciphertext"] = bytes(
        tampered_ciphertext
    )

    try:

        hybrid_decrypt(
            tampered_package,
            private_key
        )

        print("✗ Tampering was NOT detected")

    except Exception:

        print("✓ Ciphertext tampering detected")

    # ========================================================
    # FINAL RESULT
    # ========================================================

    print()
    print("✓ Hybrid AES + RSA test successful")


if __name__ == "__main__":
    main()