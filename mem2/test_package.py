from package import create_package, save_package


# Fake binary data
encrypted_file = b"This represents encrypted file data"
encrypted_aes_key = b"Fake AES key"
nonce = b"Fake nonce"
authentication_tag = b"Fake authentication tag"


# Create package
package = create_package(
    encrypted_file,
    encrypted_aes_key,
    nonce,
    authentication_tag
)


# Save package
save_package(package, "mem2/test_secure_package.json")

print("✓ Test secure package created")