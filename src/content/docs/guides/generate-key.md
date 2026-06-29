---
title: Generate Key Pair
description: "Create GnuPG-compatible OpenPGP key pairs in GpgFrontend, from simple templates to advanced control over algorithm, key size, and expiry."
sidebar:
  order: 3
---

GpgFrontend makes it easy to create OpenPGP key pairs that work with GnuPG. **If
you're new, you can make a key in three quick steps: open the dialog, enter your
name and email, and click Generate.** GpgFrontend fills in safe defaults for
everything else. You can change those defaults later if you want (see
[Customize Your Key](#customize-your-key-optional)).

## Step 1: Open the Generate Key Dialog

In the **Main Window**, click **New Keypair**. This opens the
**Generate Key** window, where you set your identity and key options.

![](https://image.cdn.bktus.com/i/2026/06/30/398635c90c069535c343216224f5fa4d881dd605.webp)

## Step 2: Enter Your Information

- **Name**: Required. Your full name (at least 5 characters).
- **Email**: Required. Must be a valid email address.
- **Comment**: Optional. Helps tell this key apart from others.

The refresh button next to these fields fills in a **random anonymous identity**.
This is handy for throwaway or test keys, when you don't want to link the key to a
real name or address.

## Step 3: Generate the Key

GpgFrontend already picks safe defaults for you, including the recommended
**Ed25519** key type. So once you've entered your name and email, you can make
your key right away:

- Check the summary in the lower panel.
- Click the **Generate** button.
- When asked, enter a strong **passphrase** (and type it again to confirm). This
  protects your private key, so pick something strong and don't forget it.
- GpgFrontend creates the key and tells you when it's done.

That's all you need to get started. Want to change the key type or how long it
lasts? See [Customize Your Key](#customize-your-key-optional) before you click
**Generate**.

---

## Customize Your Key (Optional)

You can skip this. GpgFrontend's defaults are a safe choice. Use these settings
only if you want to change the key type, how long it lasts, or its structure
before you generate.

Easy Mode uses ready-made **profiles** instead of showing every option. It has two
parts:

**Profile**

- **Name**: Pick a profile from the dropdown. Profiles are grouped by algorithm
  type:
  - **(Classical)**: older profiles such as RSA.
  - **ECC**: elliptic-curve profiles. The Ed25519 (Curve25519) profile is the
    recommended modern default and is picked for you when available.
  - **Post-Quantum**: quantum-resistant profiles (rPGP engine only).
- **Save / Delete / Reset**: Manage the profile list. **Save** stores your current
  settings as a new named profile, **Delete** removes the selected profile, and
  **Reset** restores the default list. The built-in `Custom` profile cannot be
  deleted.

Only profiles that work with your current engine and key database are shown.

**Basic**

- **Validity Period**: Pick how long the key stays valid (for example, 3 months, 2
  years, 10 years, or _Never Expires_).
- **Combination**:
  - **Primary Key Only**
  - **Primary Key With Subkey**: useful for keeping signing and encryption
    separate.

:::note

When the rPGP engine is selected, the expiration options are hidden, because the
engine has limited support for setting how long a key stays valid.

:::

For full control over the algorithm, key length, and format, switch to Advanced
Mode (the **Primary Key** and **Subkey** tabs). The supported algorithms and
compatibility notes are below.

## Advanced Options

You can skip this section unless you need fine control. It covers the full list of
algorithms and some compatibility notes.

### Supported Algorithms for the Primary Key

A primary key stands for your identity and certifies your user IDs, so it must be
able to sign or certify. That's why the primary key list only shows
signing-capable algorithms. Encryption-only algorithms (such as ECDH, X448,
Curve25519, ElGamal, or Kyber/ML-KEM) are used for subkeys instead.

The algorithms you see depend on the engine, its version, and the key format.

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

### Compatibility Notes

Some keys made by one engine can't be used by the other. Keep these points in
mind before you share a key:

- **rPGP 25519 keys are rPGP-only.** rPGP can import 25519 keys made by GnuPG, but
  not the other way around. When rPGP makes an Ed25519 or Curve25519 key, it uses
  the modern RFC 9580 encoding, not the older encoding GnuPG uses, so GnuPG can't
  read it, even if you pick the v4 format.
- **rPGP post-quantum keys are rPGP-only too.** ML-DSA, SLH-DSA, and hybrid KEM
  keys made by rPGP always use the OpenPGP v6 format. They are meant for testing
  and rPGP-based work, not for use with GnuPG.
- **GnuPG chooses its own key format.** When you use the GnuPG engine, GnuPG picks
  the format based on its version and settings; GpgFrontend doesn't set it, and
  the Key Format selector doesn't apply. Current releases make **v4** keys, but
  newer versions (such as the 2.5.x line) may make **v5** keys, which many other
  OpenPGP tools can't read.

:::caution[Check the format before sharing widely]

If you need your key to work with as many tools as possible, check what format
your engine and version actually produce before you share the key.

:::
