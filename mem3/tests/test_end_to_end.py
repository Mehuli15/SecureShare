import os
import filecmp

from app.sender import Sender
from app.receiver import Receiver

from app.package_manager import (
    SECURE_PACKAGE,
    RECEIVER_INPUT,
    RECEIVER_OUTPUT
)


# ============================================================
# TEST PATHS
# ============================================================

TEST_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

TEST_FILE = os.path.join(
    TEST_DIR,
    "e2e_test_file.txt"
)


def main():

    print("=" * 60)
    print("SECURE FILE TRANSFER - END-TO-END TEST")
    print("=" * 60)
    print()

    # ========================================================
    # CREATE TEST FILE
    # ========================================================

    original_content = (
        "Secure File Transfer End-to-End Test\n"
        "AES-256-GCM + RSA-3072 + SHA-256\n"
        "This file should survive the complete workflow."
    )

    with open(
        TEST_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            original_content
        )

    print("1. Test file created")
    print(f"   File: {TEST_FILE}")
    print()

    # ========================================================
    # SENDER
    # ========================================================

    sender = Sender()

    sender.set_file(
        TEST_FILE
    )

    print("2. Sender selected file")
    print()

    # ========================================================
    # CREATE SECURE PACKAGE
    # ========================================================

    package_path = sender.prepare_package()

    print("3. Secure package created")
    print(f"   Package: {package_path}")
    print()

    assert os.path.exists(
        SECURE_PACKAGE
    )

    encrypted_package = os.path.join(
        SECURE_PACKAGE,
        "encrypted_package.json"
    )

    metadata_file = os.path.join(
        SECURE_PACKAGE,
        "metadata.json"
    )

    assert os.path.exists(
        encrypted_package
    )

    assert os.path.exists(
        metadata_file
    )

    print("   ✓ encrypted_package.json exists")
    print("   ✓ metadata.json exists")
    print()

    # ========================================================
    # VERIFY ORIGINAL FILE IS NOT IN PACKAGE
    # ========================================================

    original_filename = os.path.basename(
        TEST_FILE
    )

    original_inside_package = os.path.join(
        SECURE_PACKAGE,
        original_filename
    )

    assert not os.path.exists(
        original_inside_package
    )

    print("   ✓ Original plaintext file is NOT in package")
    print()

    # ========================================================
    # SEND PACKAGE
    # ========================================================

    receiver_path = sender.send_package()

    print("4. Secure package transferred")
    print(f"   Receiver path: {receiver_path}")
    print()

    assert os.path.exists(
        RECEIVER_INPUT
    )

    # ========================================================
    # RECEIVER
    # ========================================================

    receiver = Receiver()

    receiver.receive_package()

    receiver.load_metadata()

    print("5. Receiver received package")
    print(
        f"   Original filename: "
        f"{receiver.metadata['original_filename']}"
    )
    print()

    # ========================================================
    # VERIFY INTEGRITY
    # ========================================================

    integrity_result = receiver.verify_integrity()

    assert integrity_result is True

    print("6. Integrity verification")
    print("   ✓ SHA-256 verification successful")
    print()

    # ========================================================
    # DECRYPT
    # ========================================================

    recovered_file = receiver.decrypt_file()

    print("7. File decrypted")
    print(f"   Recovered file: {recovered_file}")
    print()

    assert os.path.exists(
        recovered_file
    )

    # ========================================================
    # COMPARE FILES
    # ========================================================

    files_identical = filecmp.cmp(
        TEST_FILE,
        recovered_file,
        shallow=False
    )

    assert files_identical

    print("8. File comparison")
    print("   ✓ Original and recovered files are identical")
    print()

    # ========================================================
    # FINAL RESULT
    # ========================================================

    print("=" * 60)
    print("✓ END-TO-END TEST SUCCESSFUL")
    print("=" * 60)
    print()
    print("Complete workflow verified:")
    print()
    print("Original File")
    print("     ↓")
    print("AES-256-GCM")
    print("     ↓")
    print("RSA-3072")
    print("     ↓")
    print("SHA-256")
    print("     ↓")
    print("Simulated Transfer")
    print("     ↓")
    print("SHA-256 Verification")
    print("     ↓")
    print("RSA-3072 Decryption")
    print("     ↓")
    print("AES-256-GCM Decryption")
    print("     ↓")
    print("Recovered File")
    print()


if __name__ == "__main__":
    main()