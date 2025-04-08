---
title: Generate Key Pair
sidebar:
  order: 3
---

GpgFrontend provides a flexible and user-friendly interface for generating
GnuPG-compatible key pairs. The updated **Generate Key** dialog introduces
multiple configuration levels—from simplified templates to advanced
cryptographic control—catering to both casual and expert users.

## Launch the Generate Key Dialog

In the **Key Management** interface, click on the **“New Keypair”** button. This
opens the **Generate Key** window, where you can define your identity and
configure key parameters.

## Enter User Information

- **Name**: Required. Enter your full name (minimum 5 characters).  
- **Email**: Required. Must be in a valid email format.  
- **Comment**: Optional. Helps distinguish this key from others.

## Choose Key Database

Select the **Key Database** where the generated key pair will be stored (e.g.,
`0: TEST`).

## Configure Key Settings

The **Generate Key** dialog offers two configuration modes:

### Easy Mode

Easy Mode simplifies key generation using common templates. You can configure:

- **Algorithm**: RSA, DSA, ECC (Curve25519), or other supported types.
- **Validity Period**: Choose from preset options (e.g., 3 months, 2 years, 10
  years, or *Non Expired*).
- **Combination**:
  - **Primary Key Only**
  - **Primary Key with Subkey** — useful when separating signing and encryption
    functions.

> Recommended for users who prefer a faster and more guided setup process.

### Advanced Mode (Primary Key & Subkey Tabs)

Switch to the **Primary Key** and **Subkey** tabs for detailed cryptographic
control. Available options include:

- **Algorithm**: RSA, DSA, ED25519, ED448, Brainpool, NIST, CV25519, and others.
- **Key Length**: Adjustable for applicable algorithms (e.g., RSA: 2048, 3072,
  4096 bits).
- **Expiration**: Set a specific expiry date or mark the key as non-expiring.
- **Usage Flags**:
  - Encrypt
  - Sign
  - Authenticate
  - Certify (for primary keys)
- **Passphrase Protection**: Enable or disable passphrase requirement.

> Ideal for experienced users who require full control over key structure and
> behavior.

## Generate the Key Pair

Once configuration is complete:

- Review the summary in the lower panel.
- Click the **“Generate”** button.
- GpgFrontend will begin the generation process and confirm when complete.

## Primary Key Supported Algorithms

- RSA
- DSA
- ECDSA ED25519
- EdDSA ED448 (GnuPG >2.3.0)
- ECDSA SECP256K1 (GnuPG >2.3.0)
- ECDSA NIST P-256
- ECDSA NIST P-384
- ECDSA NIST P-521
- ECDSA BrainPool P-256 (GnuPG >2.3.0)
- ECDSA BrainPool P-384 (GnuPG >2.3.0)
- ECDSA BrainPool P-512 (GnuPG >2.3.0)
