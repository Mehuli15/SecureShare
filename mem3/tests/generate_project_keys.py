import os

from encryption.rsa import (
    generate_rsa_key_pair,
    save_rsa_keys
)


PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

KEYS_DIR = os.path.join(
    PROJECT_ROOT,
    "keys"
)

PRIVATE_KEY = os.path.join(
    KEYS_DIR,
    "private.pem"
)

PUBLIC_KEY = os.path.join(
    KEYS_DIR,
    "public.pem"
)


def main():

    os.makedirs(
        KEYS_DIR,
        exist_ok=True
    )

    private_key, public_key = generate_rsa_key_pair()

    save_rsa_keys(
        private_key,
        public_key,
        PRIVATE_KEY,
        PUBLIC_KEY
    )

    print("✓ RSA-3072 project key pair generated")
    print()
    print(f"Private key: {PRIVATE_KEY}")
    print(f"Public key:  {PUBLIC_KEY}")
    print()
    print("⚠ Keep private.pem private.")


if __name__ == "__main__":
    main()