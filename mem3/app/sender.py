import os

from app.package_manager import (
    create_secure_package,
    send_secure_package
)


class Sender:

    def __init__(self):

        self.selected_file = None
        self.package_path = None

    # ========================================================
    # SELECT FILE
    # ========================================================

    def set_file(self, file_path):

        if not file_path:
            raise ValueError(
                "No file selected."
            )

        if not os.path.exists(file_path):
            raise FileNotFoundError(
                "Selected file does not exist."
            )

        self.selected_file = file_path

    # ========================================================
    # ENCRYPT + PREPARE
    # ========================================================

    def prepare_package(self):

        if not self.selected_file:
            raise ValueError(
                "Please select a file first."
            )

        self.package_path = create_secure_package(
            self.selected_file
        )

        return self.package_path

    # ========================================================
    # SEND PACKAGE
    # ========================================================

    def send_package(self):

        if not self.package_path:
            raise ValueError(
                "Please prepare the package first."
            )

        receiver_path = send_secure_package()

        return receiver_path