import base64
import json
import os

from encryption.hybrid import (
    hybrid_encrypt,
    hybrid_decrypt
)

from encryption.rsa import (
    load_private_key,
    load_public_key
)


# ============================================================
# ENCRYPT FILE
# ============================================================

def encrypt_file(
    input_file,
    output_package,
    public_key_path
):
    """
    Encrypt a file using hybrid AES-256-GCM + RSA-3072.

    The encrypted package is stored as JSON.

    Returns:
        output_package path
    """

    if not os.path.exists(input_file):
        raise FileNotFoundError(
            f"Input file not found: {input_file}"
        )

    if not os.path.exists(public_key_path):
        raise FileNotFoundError(
            f"Public key not found: {public_key_path}"
        )

    # --------------------------------------------------------
    # Read original file
    # --------------------------------------------------------

    with open(
        input_file,
        "rb"
    ) as file:

        file_data = file.read()

    # --------------------------------------------------------
    # Load receiver public key
    # --------------------------------------------------------

    public_key = load_public_key(
        public_key_path
    )

    # --------------------------------------------------------
    # Hybrid encryption
    # --------------------------------------------------------

    encrypted_package = hybrid_encrypt(
        file_data,
        public_key
    )

    # --------------------------------------------------------
    # Convert bytes → Base64 strings
    # --------------------------------------------------------

    package = {
        "original_filename": os.path.basename(input_file),

        "ciphertext": base64.b64encode(
            encrypted_package["ciphertext"]
        ).decode("utf-8"),

        "encrypted_aes_key": base64.b64encode(
            encrypted_package["encrypted_aes_key"]
        ).decode("utf-8"),

        "nonce": base64.b64encode(
            encrypted_package["nonce"]
        ).decode("utf-8"),

        "authentication_tag": base64.b64encode(
            encrypted_package["authentication_tag"]
        ).decode("utf-8")
    }

    # --------------------------------------------------------
    # Create output directory
    # --------------------------------------------------------

    output_directory = os.path.dirname(
        os.path.abspath(output_package)
    )

    if output_directory:
        os.makedirs(
            output_directory,
            exist_ok=True
        )

    # --------------------------------------------------------
    # Save JSON package
    # --------------------------------------------------------

    with open(
        output_package,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            package,
            file,
            indent=4
        )

    return output_package


# ============================================================
# LOAD ENCRYPTED PACKAGE
# ============================================================

def load_encrypted_package(
    package_path
):
    """
    Load an encrypted JSON package and convert
    Base64 values back into bytes.

    Returns:
        Hybrid encryption package dictionary.
    """

    if not os.path.exists(package_path):
        raise FileNotFoundError(
            f"Encrypted package not found: {package_path}"
        )

    with open(
        package_path,
        "r",
        encoding="utf-8"
    ) as file:

        package = json.load(file)

    required_fields = {
        "original_filename",
        "ciphertext",
        "encrypted_aes_key",
        "nonce",
        "authentication_tag"
    }

    if set(package.keys()) != required_fields:
        raise ValueError(
            "Invalid encrypted package structure."
        )

    return {
        "original_filename": package["original_filename"],

        "ciphertext": base64.b64decode(
            package["ciphertext"]
        ),

        "encrypted_aes_key": base64.b64decode(
            package["encrypted_aes_key"]
        ),

        "nonce": base64.b64decode(
            package["nonce"]
        ),

        "authentication_tag": base64.b64decode(
            package["authentication_tag"]
        )
    }


# ============================================================
# DECRYPT FILE
# ============================================================

def decrypt_file(
    package_path,
    output_file,
    private_key_path
):
    """
    Decrypt an encrypted JSON package using
    RSA-3072 private key + AES-256-GCM.

    Returns:
        output_file path
    """

    if not os.path.exists(package_path):
        raise FileNotFoundError(
            f"Encrypted package not found: {package_path}"
        )

    if not os.path.exists(private_key_path):
        raise FileNotFoundError(
            f"Private key not found: {private_key_path}"
        )

    # --------------------------------------------------------
    # Load encrypted package
    # --------------------------------------------------------

    package = load_encrypted_package(
        package_path
    )

    original_filename = package.pop(
        "original_filename"
    )

    # --------------------------------------------------------
    # Load receiver private key
    # --------------------------------------------------------

    private_key = load_private_key(
        private_key_path
    )

    # --------------------------------------------------------
    # Hybrid decryption
    # --------------------------------------------------------

    decrypted_data = hybrid_decrypt(
        package,
        private_key
    )

    # --------------------------------------------------------
    # Create output directory
    # --------------------------------------------------------

    output_directory = os.path.dirname(
        os.path.abspath(output_file)
    )

    if output_directory:
        os.makedirs(
            output_directory,
            exist_ok=True
        )

    # --------------------------------------------------------
    # Write recovered file
    # --------------------------------------------------------

    with open(
        output_file,
        "wb"
    ) as file:

        file.write(
            decrypted_data
        )

    return output_file