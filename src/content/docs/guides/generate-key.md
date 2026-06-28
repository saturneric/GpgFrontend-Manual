---
title: Generate Key Pair
description: "Create GnuPG-compatible OpenPGP key pairs in GpgFrontend, from simple templates to advanced control over algorithm, key size, and expiry."
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
- **Key Format** (Primary Key tab, **rPGP engine only**): Choose the OpenPGP
  packet format:
  - **v4 (Compatible)**: the interoperable default, supported across the wider
    OpenPGP ecosystem.
  - **v6 (Modern)**: the RFC 9580 format. It is opt-in because v6 support is
    still limited in parts of the ecosystem, and is required for post-quantum
    algorithms.

  This selector is hidden when the GnuPG engine is active. GnuPG ignores the
  requested format and decides the key version itself (see the caution below).
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

:::caution[rPGP 25519 Keys Are Not GnuPG-Compatible]

The rPGP engine can import existing 25519 keys generated by GnuPG, but the
reverse does not hold. When rPGP generates an Ed25519 or Curve25519 key, it uses
the modern RFC 9580 Ed25519 / X25519 algorithm encoding, not the legacy EdDSA /
ECDH-Curve25519 encoding that GnuPG uses. As a result, rPGP-generated 25519 keys
are not compatible with GnuPG, **even when you choose the v4 key format**. Treat
rPGP-generated 25519 keys as rPGP-only.

All PQC-related keys generated by rPGP additionally use the OpenPGP v6 format.
This includes ML-DSA, SLH-DSA, and rPGP-generated hybrid KEM keys. These keys
are intended for testing, evaluation, and rPGP-based workflows, and should not
be used when GnuPG interoperability is required.

:::

:::caution[GnuPG Key Format Is Decided by GnuPG]

When the **GnuPG engine** is used, the OpenPGP key format is chosen by GnuPG
itself, based on the GnuPG version and its configuration. GpgFrontend does not
set or override it, and the Key Format selector above does not apply.

Current GnuPG releases generate **v4** keys. Be aware that newer GnuPG versions
(for example, the 2.5.x development line) may, depending on their behavior and
configuration, generate keys in a newer format such as **v5**, which is **not
compatible with many other OpenPGP tools**. The exact conditions under which
GnuPG emits such a format are determined by GnuPG and are outside GpgFrontend's
control. If you require maximum interoperability, verify the key format your
GnuPG version produces before distributing the key.

:::
