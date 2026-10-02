import os
import shutil
import json

from encryption.file_crypto import (
    encrypt_file,
    load_encrypted_package
)

from security.member2_security import (
    calculate_data_hash,
    verify_data_hash
)


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

SENDER_OUTPUT = os.path.join(
    PROJECT_ROOT,
    "storage",
    "sender_output"
)

RECEIVER_INPUT = os.path.join(
    PROJECT_ROOT,
    "storage",
    "receiver_input"
)

RECEIVER_OUTPUT = os.path.join(
    PROJECT_ROOT,
    "storage",
    "receiver_output"
)

SECURE_PACKAGE = os.path.join(
    SENDER_OUTPUT,
    "secure_package"
)


# ============================================================
# KEY PATHS
# ============================================================

KEYS_DIR = os.path.join(
    PROJECT_ROOT,
    "keys"
)

PUBLIC_KEY = os.path.join(
    KEYS_DIR,
    "public.pem"
)

PRIVATE_KEY = os.path.join(
    KEYS_DIR,
    "private.pem"
)


# ============================================================
# PACKAGE FILES
# ============================================================

ENCRYPTED_PACKAGE = os.path.join(
    SECURE_PACKAGE,
    "encrypted_package.json"
)

METADATA_FILE = os.path.join(
    SECURE_PACKAGE,
    "metadata.json"
)


# ============================================================
# CREATE METADATA
# ============================================================

def create_metadata(
    file_path,
    encrypted_package
):

    encrypted_data_hash = calculate_data_hash(
        encrypted_package["ciphertext"]
    )

    filename = os.path.basename(
        file_path
    )

    metadata = {
        "package_version": "2.0",

        "original_filename": filename,

        "encryption": {
            "algorithm": "AES-256-GCM",
            "key_encryption": "RSA-3072",
            "status": "encrypted"
        },

        "integrity": {
            "algorithm": "SHA-256",
            "hash_target": "encrypted_ciphertext",
            "hash": encrypted_data_hash,
            "status": "protected"
        }
    }

    with open(
        METADATA_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            metadata,
            file,
            indent=4
        )

    return METADATA_FILE


# ============================================================
# CREATE SECURE PACKAGE
# ============================================================

def create_secure_package(file_path):

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            "Selected file does not exist."
        )

    if not os.path.exists(PUBLIC_KEY):
        raise FileNotFoundError(
            "Receiver public key not found.\n"
            f"Expected: {PUBLIC_KEY}"
        )

    # Remove previous package
    if os.path.exists(SECURE_PACKAGE):
        shutil.rmtree(
            SECURE_PACKAGE
        )

    # Create fresh package directory
    os.makedirs(
        SECURE_PACKAGE,
        exist_ok=True
    )

    # --------------------------------------------------------
    # AES-256-GCM encryption
    # RSA-3072 encryption of AES key
    # --------------------------------------------------------

    encrypt_file(
        file_path,
        ENCRYPTED_PACKAGE,
        PUBLIC_KEY
    )

    # Load encrypted package so we can hash ciphertext
    encrypted_package = load_encrypted_package(
        ENCRYPTED_PACKAGE
    )

    # --------------------------------------------------------
    # Create metadata + SHA-256 integrity hash
    # --------------------------------------------------------

    create_metadata(
        file_path,
        encrypted_package
    )

    return SECURE_PACKAGE


# ============================================================
# SEND SECURE PACKAGE
# ============================================================

def send_secure_package():

    if not os.path.exists(SECURE_PACKAGE):
        raise FileNotFoundError(
            "Secure package does not exist."
        )

    # Remove previous received package
    if os.path.exists(RECEIVER_INPUT):
        shutil.rmtree(
            RECEIVER_INPUT
        )

    # Simulated transfer
    shutil.copytree(
        SECURE_PACKAGE,
        RECEIVER_INPUT
    )

    return RECEIVER_INPUT


# ============================================================
# CHECK SENDER PACKAGE
# ============================================================

def package_exists():

    return os.path.exists(
        SECURE_PACKAGE
    )


# ============================================================
# CHECK RECEIVER PACKAGE
# ============================================================

def received_package_exists():

    return os.path.exists(
        RECEIVER_INPUT
    )


# ============================================================
# READ METADATA
# ============================================================

def read_metadata(package_path):

    metadata_path = os.path.join(
        package_path,
        "metadata.json"
    )

    if not os.path.exists(metadata_path):
        raise FileNotFoundError(
            "Package metadata not found."
        )

    with open(
        metadata_path,
        "r",
        encoding="utf-8"
    ) as file:

        metadata = json.load(
            file
        )

    return metadata


# ============================================================
# VERIFY PACKAGE INTEGRITY
# ============================================================

def verify_package_integrity(package_path):

    # Load metadata
    metadata = read_metadata(
        package_path
    )

    encrypted_package_path = os.path.join(
        package_path,
        "encrypted_package.json"
    )

    if not os.path.exists(
        encrypted_package_path
    ):
        raise FileNotFoundError(
            "Encrypted package not found."
        )

    # Load encrypted package
    encrypted_package = load_encrypted_package(
        encrypted_package_path
    )

    # Expected SHA-256 hash
    expected_hash = metadata[
        "integrity"
    ][
        "hash"
    ]

    # Actual encrypted ciphertext
    ciphertext = encrypted_package[
        "ciphertext"
    ]

    # Compare hashes
    return verify_data_hash(
        ciphertext,
        expected_hash
    )