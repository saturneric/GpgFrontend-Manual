---
title: Generate Key Pair
sidebar:
  order: 3
---

GpgFrontend provides a flexible and user-friendly interface for generating
GnuPG-compatible key pairs. The updated **Generate Key** dialog introduces
multiple configuration levels from simplified templates to advanced
cryptographic control, catering to both normal and expert users.

## Launch the Generate Key Dialog

In the **Key Management** interface, click on the **“New Keypair”** button. This
opens the **Generate Key** window, where you can define your identity and
configure key parameters.

![](https://image.cdn.bktus.com/i/2025/06/24/79fe9ef30cbc5e10e7eda6aca7ee22616e874267.webp)

## Enter User Information

- **Name**: Required. Enter your full name (minimum 5 characters).
- **Email**: Required. Must be in a valid email format.
- **Comment**: Optional. Helps distinguish this key from others.

The refresh button next to the identity fields fills in a **random anonymous
identity**. This is handy for throwaway or test keys when you don't want to tie
the key to a real name or address.

## Choose Key Database

Select the **Key Database** where the generated key pair will be stored (e.g.,
`0: TEST`).

## Configure Key Settings

The **Generate Key** dialog offers two configuration modes:

### Easy Mode

Easy Mode simplifies key generation using ready-made **profiles** instead of
exposing every cryptographic option. It is split into two sections:

**Profile**

- **Name**: Pick a profile from the dropdown. Profiles are grouped by algorithm
  family under section headers:
  - **(Classical)**: traditional profiles such as RSA.
  - **ECC**: elliptic-curve profiles. The Ed25519 (Curve25519) profile is the
    recommended modern default and is pre-selected when available.
  - **Post-Quantum**: quantum-resistant profiles (rPGP engine only).
- **Save / Delete / Reset**: Manage the profile list. **Save** stores your
  current configuration as a new named profile, **Delete** removes the selected
  profile, and **Reset** restores the profile list to its default set. The
  built-in `Custom` profile is reserved and cannot be deleted.

Only profiles whose algorithms are supported by the currently selected engine
and key database are listed.

**Basic**

- **Validity Period**: Choose from preset options (e.g., 3 months, 2 years, 10
  years, or _Non Expired_).
- **Combination**:
  - **Primary Key Only**
  - **Primary Key With Subkey**: Useful when separating signing and encryption
    functions.

> Recommended for users who prefer a faster and more guided setup process.

:::note

When the rPGP engine is selected, expiration options are hidden because the
backend currently has limited support for setting key validity periods.

:::

### Advanced Mode (Primary Key & Subkey Tabs)

Switch to the **Primary Key** and **Subkey** tabs for detailed cryptographic
control. Available options include:

- **Algorithm**: RSA, DSA, ED25519, ED448, Brainpool, NIST, CV25519, and others.
- **Key Length**: Adjustable for applicable algorithms (e.g., RSA: 2048, 3072,
  4096 bits).
- **Key Format** (Primary Key tab): Choose the OpenPGP packet format:
  - **v4 (Compatible)**: the interoperable default, supported across the wider
    OpenPGP ecosystem.
  - **v6 (Modern)**: the RFC 9580 format. It is opt-in because v6 support is
    still limited in parts of the ecosystem, and is required for post-quantum
    algorithms.
- **Expiration**: Set a specific expiry date or mark the key as non-expiring.
- **Usage Flags**:
  - Encrypt
  - Sign
  - Authenticate
  - Certify (for primary keys)
- **Passphrase Protection**: Enable or disable passphrase requirement via the
  **No Passphrase** option.

> When a post-quantum algorithm is selected, the **v6** key format is required
> and is enforced automatically.

> Ideal for experienced users who require full control over key structure and
> behavior.

## Generate the Key Pair

Once configuration is complete:

- Review the summary in the lower panel.
- Click the **“Generate”** button.
- GpgFrontend will begin the generation process and confirm when complete.

## Primary Key Supported Algorithms

Primary keys are mainly used to represent identity, certify user IDs, and
establish trust. For this reason, primary key algorithms are limited to
algorithms that can perform signing or certification operations. Encryption-only
algorithms such as ECDH, X448, Curve25519, ElGamal, or Kyber/ML-KEM are used as
subkey algorithms instead.

Available algorithms depend on the selected OpenPGP engine, engine version, and
key format.

| Algorithm group                 | Purpose                      | Engine           |
| ------------------------------- | ---------------------------- | ---------------- |
| RSA                             | Sign / Encrypt / Auth / Cert | GnuPG, rPGP      |
| DSA                             | Sign / Auth / Cert           | GnuPG, rPGP      |
| Ed25519 / Ed448                 | Sign / Auth / Cert           | GnuPG, rPGP      |
| NIST P-256 / P-384 / P-521      | Sign / Auth / Cert           | GnuPG, rPGP      |
| Brainpool P-256 / P-384 / P-512 | Sign / Auth / Cert           | GnuPG 2.3+       |
| secp256k1                       | Sign / Auth / Cert           | GnuPG 2.3+, rPGP |
| SLH-DSA-SHAKE variants          | PQC Sign / Auth              | rPGP only        |
| ML-DSA hybrid variants          | Hybrid PQC Sign / Auth       | rPGP only        |

:::caution[OpenPGP v6 Format and GnuPG Compatibility]

The rPGP engine can import existing 25519 keys generated by GnuPG. However,
rPGP-generated 25519 keys use the OpenPGP v6 format and are not currently
importable by GnuPG.

All PQC-related keys generated by rPGP use the OpenPGP v6 format. This includes
ML-DSA, SLH-DSA, and rPGP-generated hybrid KEM keys. These keys are intended for
testing, evaluation, and rPGP-based workflows, and should not be used when GnuPG
interoperability is required.

:::
