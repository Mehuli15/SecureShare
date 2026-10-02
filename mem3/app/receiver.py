import os

from app.package_manager import (
    received_package_exists,
    read_metadata,
    verify_package_integrity,
    RECEIVER_INPUT,
    RECEIVER_OUTPUT,
    PRIVATE_KEY
)

from encryption.file_crypto import (
    decrypt_file
)


class Receiver:

    def __init__(self):

        self.package_path = None
        self.metadata = None
        self.integrity_verified = False
        self.output_path = None

    # ========================================================
    # RECEIVE PACKAGE
    # ========================================================

    def receive_package(self):

        if not received_package_exists():
            raise FileNotFoundError(
                "No secure package found."
            )

        self.package_path = RECEIVER_INPUT

        return self.package_path

    # ========================================================
    # LOAD METADATA
    # ========================================================

    def load_metadata(self):

        if not self.package_path:
            raise ValueError(
                "Please receive the package first."
            )

        self.metadata = read_metadata(
            self.package_path
        )

        return self.metadata

    # ========================================================
    # VERIFY INTEGRITY
    # ========================================================

    def verify_integrity(self):

        if not self.package_path:
            raise ValueError(
                "Please receive the package first."
            )

        result = verify_package_integrity(
            self.package_path
        )

        self.integrity_verified = result

        return result

    # ========================================================
    # DECRYPT FILE
    # ========================================================

    def decrypt_file(self):

        if not self.package_path:
            raise ValueError(
                "Please receive the package first."
            )

        if not self.integrity_verified:
            raise ValueError(
                "Integrity must be verified before decryption."
            )

        if not os.path.exists(PRIVATE_KEY):
            raise FileNotFoundError(
                "Receiver private key not found."
            )

        if self.metadata is None:
            self.load_metadata()

        filename = self.metadata.get(
            "original_filename",
            "recovered_file"
        )

        encrypted_package = os.path.join(
            self.package_path,
            "encrypted_package.json"
        )

        os.makedirs(
            RECEIVER_OUTPUT,
            exist_ok=True
        )

        self.output_path = os.path.join(
            RECEIVER_OUTPUT,
            filename
        )

        decrypt_file(
            encrypted_package,
            self.output_path,
            PRIVATE_KEY
        )

        return self.output_path