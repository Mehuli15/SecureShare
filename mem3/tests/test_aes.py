from encryption.aes import (
    generate_aes_key,
    encrypt_data,
    decrypt_data
)


def main():

    print("Testing AES-256-GCM...")

    # Generate AES-256 key
    key = generate_aes_key()

    print("✓ AES-256 key generated")
    print(f"Key length: {len(key)} bytes")

    # Original data
    original_data = (
        b"This is a test message for AES encryption."
    )

    # Encrypt
    ciphertext, nonce, authentication_tag = encrypt_data(
        original_data,
        key
    )

    print("✓ Data encrypted")
    print(f"Ciphertext length: {len(ciphertext)} bytes")
    print(f"Nonce length: {len(nonce)} bytes")
    print(f"Authentication tag length: {len(authentication_tag)} bytes")

    # Decrypt
    decrypted_data = decrypt_data(
        ciphertext,
        key,
        nonce,
        authentication_tag
    )

    print("✓ Data decrypted")

    # Verify
    assert decrypted_data == original_data

    print("✓ Original data recovered successfully")

    # --------------------------------------------------------
    # TAMPERING TEST
    # --------------------------------------------------------

    tampered_ciphertext = bytearray(ciphertext)

    # Modify one byte
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

        print("✓ Ciphertext tampering detected")

    print()
    print("✓ AES-256-GCM test successful")


if __name__ == "__main__":
    main()