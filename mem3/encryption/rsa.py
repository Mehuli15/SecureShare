from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


# ============================================================
# RSA KEY GENERATION
# ============================================================

def generate_rsa_key_pair():
    """
    Generates a 3072-bit RSA key pair.

    Returns:
        tuple:
            private_key
            public_key
    """

    key = RSA.generate(3072)

    private_key = key
    public_key = key.publickey()

    return private_key, public_key


# ============================================================
# SAVE RSA KEYS
# ============================================================

def save_rsa_keys(
    private_key,
    public_key,
    private_path,
    public_path
):
    """
    Saves RSA private and public keys as PEM files.
    """

    with open(
        private_path,
        "wb"
    ) as file:

        file.write(
            private_key.export_key()
        )

    with open(
        public_path,
        "wb"
    ) as file:

        file.write(
            public_key.export_key()
        )


# ============================================================
# LOAD PRIVATE KEY
# ============================================================

def load_private_key(path):
    """
    Loads an RSA private key from a PEM file.
    """

    with open(
        path,
        "rb"
    ) as file:

        key_data = file.read()

    return RSA.import_key(
        key_data
    )


# ============================================================
# LOAD PUBLIC KEY
# ============================================================

def load_public_key(path):
    """
    Loads an RSA public key from a PEM file.
    """

    with open(
        path,
        "rb"
    ) as file:

        key_data = file.read()

    return RSA.import_key(
        key_data
    )


# ============================================================
# ENCRYPT AES KEY WITH RSA
# ============================================================

def encrypt_aes_key(
    aes_key,
    public_key
):
    """
    Encrypts an AES key using RSA-OAEP.

    Args:
        aes_key (bytes): 32-byte AES key.
        public_key: RSA public-key object.

    Returns:
        bytes: RSA-encrypted AES key.
    """

    if not isinstance(aes_key, bytes):
        raise TypeError(
            "aes_key must be bytes."
        )

    cipher = PKCS1_OAEP.new(
        public_key
    )

    return cipher.encrypt(
        aes_key
    )


# ============================================================
# DECRYPT AES KEY WITH RSA
# ============================================================

def decrypt_aes_key(
    encrypted_aes_key,
    private_key
):
    """
    Decrypts an RSA-encrypted AES key.

    Args:
        encrypted_aes_key (bytes):
            RSA-encrypted AES key.

        private_key:
            RSA private-key object.

    Returns:
        bytes: Original AES key.
    """

    if not isinstance(
        encrypted_aes_key,
        bytes
    ):
        raise TypeError(
            "encrypted_aes_key must be bytes."
        )

    cipher = PKCS1_OAEP.new(
        private_key
    )

    return cipher.decrypt(
        encrypted_aes_key
    )