from security.member2_security import (
    calculate_file_hash,
    verify_file_hash,
    calculate_data_hash,
    verify_data_hash
)


def main():

    print("Testing SHA-256 integrity protection...")
    print()

    # ========================================================
    # TEST DATA
    # ========================================================

    original_data = (
        b"Secure File Transfer Project - "
        b"Integrity Test"
    )

    # ========================================================
    # HASH BYTES
    # ========================================================

    original_hash = calculate_data_hash(
        original_data
    )

    print("✓ SHA-256 hash calculated")
    print(f"Hash: {original_hash}")

    # ========================================================
    # VERIFY ORIGINAL DATA
    # ========================================================

    result = verify_data_hash(
        original_data,
        original_hash
    )

    assert result is True

    print("✓ Original data integrity verified")

    # ========================================================
    # TAMPERING TEST
    # ========================================================

    tampered_data = (
        b"Secure File Transfer Project - "
        b"Modified Data"
    )

    result = verify_data_hash(
        tampered_data,
        original_hash
    )

    assert result is False

    print("✓ Tampered data detected")

    # ========================================================
    # FILE HASH TEST
    # ========================================================

    test_file = "tests/integrity_test_file.txt"

    with open(
        test_file,
        "wb"
    ) as file:

        file.write(
            original_data
        )

    file_hash = calculate_file_hash(
        test_file
    )

    print("✓ File SHA-256 hash calculated")

    # ========================================================
    # VERIFY FILE
    # ========================================================

    assert verify_file_hash(
        test_file,
        file_hash
    ) is True

    print("✓ File integrity verified")

    # ========================================================
    # MODIFY FILE
    # ========================================================

    with open(
        test_file,
        "ab"
    ) as file:

        file.write(
            b" MODIFIED"
        )

    assert verify_file_hash(
        test_file,
        file_hash
    ) is False

    print("✓ Modified file detected")

    # ========================================================
    # FINAL RESULT
    # ========================================================

    print()
    print("✓ SHA-256 INTEGRITY TEST SUCCESSFUL")


if __name__ == "__main__":
    main()