import hashlib


# ============================================================
# CALCULATE SHA-256
# ============================================================

def calculate_file_hash(filename):
    """
    Calculate the SHA-256 hash of a file.

    Returns:
        hexadecimal SHA-256 hash string
    """

    sha256 = hashlib.sha256()

    with open(
        filename,
        "rb"
    ) as file:

        while True:

            chunk = file.read(4096)

            if not chunk:
                break

            sha256.update(chunk)

    return sha256.hexdigest()


# ============================================================
# VERIFY FILE HASH
# ============================================================

def verify_file_hash(
    filename,
    expected_hash
):
    """
    Compare a file's SHA-256 hash
    with an expected hash.

    Returns:
        True if hashes match
        False otherwise
    """

    actual_hash = calculate_file_hash(
        filename
    )

    return actual_hash == expected_hash


# ============================================================
# CALCULATE BYTES HASH
# ============================================================

def calculate_data_hash(data):
    """
    Calculate SHA-256 hash directly from bytes.

    This is useful for our secure package because
    we ultimately want to verify the encrypted payload.
    """

    if not isinstance(data, bytes):
        raise TypeError(
            "data must be bytes."
        )

    sha256 = hashlib.sha256()

    sha256.update(data)

    return sha256.hexdigest()


# ============================================================
# VERIFY BYTES HASH
# ============================================================

def verify_data_hash(
    data,
    expected_hash
):
    """
    Verify SHA-256 hash of bytes.
    """

    actual_hash = calculate_data_hash(
        data
    )

    return actual_hash == expected_hash