# Secure File Transfer

A desktop-based secure file transfer prototype demonstrating hybrid encryption, data integrity verification, tampering detection, and ML-based file-transfer anomaly detection using AES-256-GCM, RSA-3072, RSA-OAEP, SHA-256, and Isolation Forest.

## Overview

This project implements a secure file transfer workflow in which a selected file is analyzed, encrypted before transfer, verified for integrity after transfer, and decrypted only after successful integrity verification.

The system combines cryptographic security with an additional machine-learning monitoring layer.

The project uses:

- **AES-256-GCM** for file encryption
- **RSA-3072** for secure AES key protection
- **RSA-OAEP** for RSA-based key encryption
- **SHA-256** for independent integrity verification
- **Isolation Forest** for file-transfer anomaly detection
- **Tkinter** for the desktop graphical user interface

The prototype simulates file transfer using the local filesystem rather than a real network connection.

---

## System Workflow

```text
                         USER
                           │
                           ▼
                      Select File
                           │
                           ▼
                  ML Security Analysis
                           │
                    ┌──────┴──────┐
                    │             │
                  NORMAL       ANOMALOUS
                    │             │
                    │          Warning /
                    │          Log Event
                    │             │
                    └──────┬──────┘
                           ▼
                        SENDER
                           │
                  ┌────────┴────────┐
                  │                 │
                  ▼                 ▼
             AES-256-GCM       RSA-3072/OAEP
             File Encryption   AES Key Protection
                  │                 │
                  └────────┬────────┘
                           ▼
                    Secure Package
                           │
                           ▼
                 Simulated Transfer
                           │
                           ▼
                       RECEIVER
                           │
                           ▼
                   Verify SHA-256
                      Integrity
                           │
                    ┌──────┴──────┐
                    │             │
                 INVALID         VALID
                    │             │
                    ▼             ▼
               Block Access    Decrypt
                                  │
                                  ▼
                           Recovered File
Features
1. File Selection

The user selects a file through the graphical interface.

After selection, the application performs an ML-based security analysis of the file and reports whether its characteristics are considered normal or anomalous.

2. ML-Based File Transfer Anomaly Detection

An additional machine-learning layer monitors file-transfer characteristics and identifies unusual behavior.

How It Works
File / Transfer Characteristics
              │
              ▼
       Feature Extraction
              │
              ▼
       ML Anomaly Detector
          ↙          ↘
       NORMAL      ANOMALOUS
          │             │
          ▼             ▼
      Continue        Warning
      Existing Flow   / Log Event
ML Technique

The prototype uses Isolation Forest, an unsupervised anomaly-detection algorithm.

The ML layer:

Learns patterns associated with normal file activity
Extracts characteristics from files
Assigns an anomaly score to new files
Classifies activity as NORMAL or ANOMALOUS
Provides warnings through the GUI
Does not replace cryptographic security controls

The ML detector is advisory and does not block encryption or decryption by itself.

3. Hybrid Encryption

The selected file is encrypted using AES-256-GCM.

A randomly generated AES key is then encrypted using the receiver's RSA-3072 public key with RSA-OAEP.

This provides a hybrid encryption design:

Original File
     │
     ▼
AES-256-GCM
     │
     ▼
Encrypted File Data

Random AES Key
     │
     ▼
RSA-3072 + OAEP
     │
     ▼
Encrypted AES Key
4. Secure Package Creation

The encrypted file data and required cryptographic information are stored inside a secure package.

The package contains:

secure_package/

├── encrypted_package.json
└── metadata.json

The original plaintext file is not included in the package.

5. SHA-256 Integrity Verification

A SHA-256 hash of the encrypted ciphertext is stored in the package metadata.

When the package is received, the receiver calculates the SHA-256 hash again and compares it with the stored value.

Stored SHA-256 Hash
        │
        │
        ▼
Received Ciphertext
        │
        ▼
Calculate SHA-256
        │
        ▼
     Compare
      /     \
     /       \
 MATCH     MISMATCH
   │           │
   ▼           ▼
 VALID       INVALID
6. Tampering Detection

If the encrypted ciphertext is modified after transfer, the calculated SHA-256 hash will differ from the stored hash.

The application then:

Detects the modification
Marks integrity verification as invalid
Blocks further decryption

This provides an independent integrity-verification layer in addition to the authenticated encryption provided by AES-GCM.

7. File Recovery

After successful integrity verification, the receiver:

Uses the RSA private key to recover the AES key.
Uses the recovered AES key to decrypt the encrypted file.
Saves the recovered plaintext file to the receiver output directory.

Decryption is only allowed after successful integrity verification.

8. Graphical User Interface

The application provides a Tkinter-based desktop interface containing:

File selection
ML security analysis
Encryption and package preparation
Secure package sending
Package receiving
SHA-256 integrity verification
File decryption and recovery
Security status messages
Scrollable interface for the complete workflow
Security Relationship

The security components serve different purposes:

ML Anomaly Detector
        │
        ▼
Behavioral Monitoring
        │
        ▼
AES-256-GCM
        │
        ▼
Confidentiality + Authenticated Encryption
        │
        ▼
RSA-3072/OAEP
        │
        ▼
AES Key Protection
        │
        ▼
SHA-256
        │
        ▼
Independent Integrity Verification

The ML component is an additional monitoring layer and does not replace encryption, authentication, or integrity verification.

Technology Stack
Component	Technology
Programming Language	Python
GUI	Tkinter
Symmetric Encryption	AES-256-GCM
Asymmetric Encryption	RSA-3072
Key Encryption	RSA-OAEP
Integrity Verification	SHA-256
ML Anomaly Detection	Isolation Forest
Cryptography Library	PyCryptodome
Transfer Method	Simulated filesystem transfer
Project Structure
secure-file-transfer/

│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── package_manager.py
│   ├── receiver.py
│   └── sender.py
│
├── encryption/
│   ├── __init__.py
│   ├── aes.py
│   ├── rsa.py
│   ├── hybrid.py
│   └── file_crypto.py
│
├── security/
│   ├── __init__.py
│   └── member2_security.py
│
├── ml/
│   └── anomaly_detector.py
│
├── keys/
│   ├── private.pem
│   └── public.pem
│
├── storage/
│   ├── sender_output/
│   ├── receiver_input/
│   └── receiver_output/
│
├── tests/
│   ├── test_aes.py
│   ├── test_rsa.py
│   ├── test_hybrid.py
│   ├── test_file_crypto.py
│   ├── test_integrity.py
│   ├── test_end_to_end.py
│   ├── test_tampering.py
│   └── generate_project_keys.py
│
├── .gitignore
└── README.md
Installation

Make sure Python is installed.

Install the required cryptography library:

python -m pip install pycryptodome

If the ML module requires additional dependencies, install them according to the project's ML environment requirements.

RSA Project Keys

The project requires an RSA-3072 key pair.

Generate the project keys using:

python -m tests.generate_project_keys

This creates:

keys/

├── private.pem
└── public.pem

The private key must be kept confidential and must not be committed to a public repository.

Running the Application

From the project root:

cd D:\secure-file-transfer

python -m app.main

The graphical interface provides the following workflow:

Choose File
     ↓
ML Security Analysis
     ↓
Encrypt & Prepare
     ↓
Send Secure Package
     ↓
Receive Package
     ↓
Verify Integrity
     ↓
Verify & Decrypt
Testing

The individual cryptographic modules can be tested using:

python -m tests.test_aes

python -m tests.test_rsa

python -m tests.test_hybrid

python -m tests.test_file_crypto

python -m tests.test_integrity

The complete workflow can be tested using:

python -m tests.test_end_to_end

Tampering detection can be tested using:

python -m tests.test_tampering

The ML anomaly detector can be evaluated using:

python -m tests.test_ml_detector
Security Design
AES-256-GCM

AES-256-GCM provides authenticated symmetric encryption.

It provides:

Confidentiality
Authentication
Ciphertext integrity protection

The AES key is randomly generated for the encryption operation.

RSA-3072

RSA-3072 is used to protect the randomly generated AES key.

The receiver's public key is used during encryption, while the corresponding private key is required to recover the AES key during decryption.

RSA-OAEP is used for RSA-based key encryption.

SHA-256

SHA-256 is used to independently verify the integrity of the encrypted ciphertext before decryption.

The application requires successful integrity verification before allowing the decryption operation.

Isolation Forest

Isolation Forest is used as an additional anomaly-detection mechanism.

It analyzes extracted file characteristics and produces an anomaly score that is used to classify activity as normal or anomalous.

The ML layer is intended for behavioral monitoring and does not replace cryptographic verification.

Security Failure Handling
Security Event	System Response
ML detects unusual characteristics	Warning/log event
Ciphertext modified	SHA-256 mismatch detected
Integrity verification fails	Decryption blocked
Valid package	Decryption permitted
Missing/invalid package	Operation reported as failed
Important Note

This is an academic prototype intended to demonstrate cryptographic concepts, anomaly detection, secure package handling, and secure file-transfer workflow.

The current transfer mechanism uses the local filesystem to simulate communication between sender and receiver. It does not implement an actual network transport protocol.

The ML anomaly detector provides an additional monitoring layer and should not be treated as a replacement for cryptographic security mechanisms.

For a production system, additional protections would be required, including secure key management, authenticated network transport, access control, secure storage, logging, and appropriate operational security practices.

Authors

Developed as a college project demonstrating:

Hybrid cryptography
AES-256-GCM file encryption
RSA-3072/OAEP key protection
SHA-256 integrity verification
Tampering detection
ML-based anomaly detection
Secure package handling
GUI-based application integration