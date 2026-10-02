from encryption.aes import (
    generate_aes_key,
    encrypt_data,
    decrypt_data
)

from encryption.rsa import (
    encrypt_aes_key,
    decrypt_aes_key
)


def hybrid_encrypt(
    data,
    public_key
):
    """
    Encrypt data using AES-256-GCM and
    encrypt the AES key using RSA-3072.

    Returns:
        {
            "ciphertext": bytes,
            "encrypted_aes_key": bytes,
            "nonce": bytes,
            "authentication_tag": bytes
        }
    """

    if not isinstance(data, bytes):
        raise TypeError(
            "data must be bytes."
        )

    # --------------------------------------------------------
    # Generate AES-256 key
    # --------------------------------------------------------

    aes_key = generate_aes_key()

    # --------------------------------------------------------
    # Encrypt data using AES-256-GCM
    # --------------------------------------------------------

    ciphertext, nonce, authentication_tag = encrypt_data(
        data,
        aes_key
    )

    # --------------------------------------------------------
    # Encrypt AES key using RSA public key
    # --------------------------------------------------------

    encrypted_aes_key = encrypt_aes_key(
        aes_key,
        public_key
    )

    # --------------------------------------------------------
    # Create hybrid package
    # --------------------------------------------------------

    package = {
        "ciphertext": ciphertext,
        "encrypted_aes_key": encrypted_aes_key,
        "nonce": nonce,
        "authentication_tag": authentication_tag
    }

    return package


def hybrid_decrypt(
    package,
    private_key
):
    """
    Decrypt a hybrid AES + RSA package.

    Returns:
        plaintext bytes
    """

    required_keys = {
        "ciphertext",
        "encrypted_aes_key",
        "nonce",
        "authentication_tag"
    }

    if not isinstance(package, dict):
        raise TypeError(
            "package must be a dictionary."
        )

    if set(package.keys()) != required_keys:
        raise ValueError(
            "Package must contain exactly: "
            "ciphertext, encrypted_aes_key, "
            "nonce, authentication_tag."
        )

    # --------------------------------------------------------
    # Recover AES key using RSA private key
    # --------------------------------------------------------

    aes_key = decrypt_aes_key(
        package["encrypted_aes_key"],
        private_key
    )

    # --------------------------------------------------------
    # Decrypt data using AES-256-GCM
    # --------------------------------------------------------

    plaintext = decrypt_data(
        package["ciphertext"],
        aes_key,
        package["nonce"],
        package["authentication_tag"]
    )

    return plaintext