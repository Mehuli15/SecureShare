from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


# ============================================================
# AES KEY GENERATION
# ============================================================

def generate_aes_key():
    """
    Generates a 256-bit AES key.

    Returns:
        bytes: 32-byte AES key
    """

    return get_random_bytes(32)


# ============================================================
# AES-GCM ENCRYPTION
# ============================================================

def encrypt_data(data, key):
    """
    Encrypts data using AES-256-GCM.

    Args:
        data (bytes): Data to encrypt.
        key (bytes): 32-byte AES key.

    Returns:
        tuple:
            ciphertext (bytes)
            nonce (bytes)
            authentication_tag (bytes)
    """

    if not isinstance(data, bytes):
        raise TypeError(
            "data must be bytes."
        )

    if not isinstance(key, bytes):
        raise TypeError(
            "key must be bytes."
        )

    if len(key) != 32:
        raise ValueError(
            "AES-256 key must be exactly 32 bytes."
        )

    cipher = AES.new(
        key,
        AES.MODE_GCM
    )

    ciphertext, authentication_tag = cipher.encrypt_and_digest(
        data
    )

    return (
        ciphertext,
        cipher.nonce,
        authentication_tag
    )


# ============================================================
# AES-GCM DECRYPTION
# ============================================================

def decrypt_data(
    ciphertext,
    key,
    nonce,
    authentication_tag
):
    """
    Decrypts AES-256-GCM encrypted data.

    Args:
        ciphertext (bytes): Encrypted data.
        key (bytes): 32-byte AES key.
        nonce (bytes): AES-GCM nonce.
        authentication_tag (bytes): Authentication tag.

    Returns:
        bytes: Decrypted plaintext.

    Raises:
        ValueError:
            If authentication fails or inputs are invalid.
    """

    if not isinstance(ciphertext, bytes):
        raise TypeError(
            "ciphertext must be bytes."
        )

    if not isinstance(key, bytes):
        raise TypeError(
            "key must be bytes."
        )

    if not isinstance(nonce, bytes):
        raise TypeError(
            "nonce must be bytes."
        )

    if not isinstance(authentication_tag, bytes):
        raise TypeError(
            "authentication_tag must be bytes."
        )

    if len(key) != 32:
        raise ValueError(
            "AES-256 key must be exactly 32 bytes."
        )

    cipher = AES.new(
        key,
        AES.MODE_GCM,
        nonce=nonce
    )

    plaintext = cipher.decrypt_and_verify(
        ciphertext,
        authentication_tag
    )

    return plaintext