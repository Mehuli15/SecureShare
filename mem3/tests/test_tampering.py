import os
import json

from app.sender import Sender
from app.receiver import Receiver

from app.package_manager import (
    SECURE_PACKAGE,
    RECEIVER_INPUT
)


TEST_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

TEST_FILE = os.path.join(
    TEST_DIR,
    "tampering_test_file.txt"
)


def main():

    print("=" * 60)
    print("SECURE FILE TRANSFER - TAMPERING TEST")
    print("=" * 60)
    print()

    # ========================================================
    # 1. CREATE TEST FILE
    # ========================================================

    with open(
        TEST_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            "Original secure file content."
        )

    print("1. Test file created")
    print()

    # ========================================================
    # 2. CREATE SECURE PACKAGE
    # ========================================================

    sender = Sender()

    sender.set_file(
        TEST_FILE
    )

    sender.prepare_package()

    print("2. Secure package created")
    print()

    # ========================================================
    # 3. TRANSFER PACKAGE
    # ========================================================

    sender.send_package()

    print("3. Secure package transferred")
    print()

    # ========================================================
    # 4. VERIFY ORIGINAL PACKAGE
    # ========================================================

    receiver = Receiver()

    receiver.receive_package()

    original_result = receiver.verify_integrity()

    assert original_result is True

    print(
        "4. Original package integrity: VALID ✓"
    )
    print()

    # ========================================================
    # 5. TAMPER WITH ENCRYPTED CIPHERTEXT
    # ========================================================

    encrypted_package_path = os.path.join(
        RECEIVER_INPUT,
        "encrypted_package.json"
    )

    with open(
        encrypted_package_path,
        "r",
        encoding="utf-8"
    ) as file:

        package = json.load(file)

    # Change one character in ciphertext
    ciphertext = package["ciphertext"]

    if ciphertext[0] == "A":
        replacement = "B"
    else:
        replacement = "A"

    package["ciphertext"] = (
        replacement +
        ciphertext[1:]
    )

    with open(
        encrypted_package_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            package,
            file,
            indent=4
        )

    print("5. Encrypted ciphertext modified")
    print("   ⚠ Simulated tampering performed")
    print()

    # ========================================================
    # 6. VERIFY TAMPERED PACKAGE
    # ========================================================

    tampered_result = receiver.verify_integrity()

    assert tampered_result is False

    print(
        "6. Tampered package integrity: INVALID ✓"
    )
    print(
        "   ✓ SHA-256 successfully detected modification"
    )
    print()

    # ========================================================
    # 7. ENSURE DECRYPTION IS BLOCKED
    # ========================================================

    try:

        receiver.decrypt_file()

        raise AssertionError(
            "Decryption should NOT be allowed "
            "after integrity failure."
        )

    except ValueError as error:

        assert (
            "Integrity must be verified"
            in str(error)
        )

        print(
            "7. Decryption blocked successfully ✓"
        )
        print(
            "   ✓ Tampered package cannot be decrypted"
        )
        print()

    # ========================================================
    # FINAL RESULT
    # ========================================================

    print("=" * 60)
    print("✓ TAMPERING TEST SUCCESSFUL")
    print("=" * 60)
    print()

    print("Security behavior verified:")
    print()
    print("Valid Package")
    print("     ↓")
    print("SHA-256 → VALID ✓")
    print("     ↓")
    print("Decryption allowed")
    print()
    print("Tampered Package")
    print("     ↓")
    print("SHA-256 → INVALID ✗")
    print("     ↓")
    print("Decryption blocked ✓")
    print()


if __name__ == "__main__":
    main()