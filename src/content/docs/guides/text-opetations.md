---
title: Text Operations
sidebar:
  order: 5
---

GpgFrontend is a user-friendly graphical interface for GnuPG that simplifies the
core cryptographic operations: **encryption**, **decryption**, **signing**, and
**verification**. It supports secure communication through public key
cryptography and provides intuitive workflows for both beginners and advanced
users.

![](https://image.cdn.bktus.com/i/2025/06/24/a08c744eff9339df43a39a22d948c806e473a6c8.webp)

## Understanding the Basics

Public key cryptography relies on key pairs:

- **Public Key**: Used to encrypt or verify.
- **Private Key**: Used to decrypt or sign.

Before performing encryption or signing operations, users must generate their
own key pair and exchange public keys with their communication partners.

## Encrypting Text

Use the recipient's **public key** to encrypt plaintext. This method:

- Produces a shorter ciphertext.
- Does **not** reveal the sender's identity.
- Is ideal when anonymity is preferred.

> 🔐 Tip: Don’t use your own public key to encrypt unless you're sending a
> message to yourself.

![](https://image.cdn.bktus.com/i/2025/06/24/19483c04524fd94afff85cac502a1030bdb4c477.gif)

## Signing Text

Use your **private key** to sign text without encrypting it:

- This confirms authorship.
- Anyone with your public key can verify it.

Check the key’s `Usage` column for `S` to confirm it's suitable for signing.

![](https://image.cdn.bktus.com/i/2025/06/24/8c6db160d26f94e75138134d319c29bd2c3736b7.gif)

## Decrypting Text

Paste or load the ciphertext into GpgFrontend. The tool will:

- Automatically use the correct **private key**.
- Notify you if no valid key is available.

> ✅ No need to check `Usage` manually; the tool handles key matching.

![](https://image.cdn.bktus.com/i/2025/06/24/5e16d1a75fb7e7bfb4d14f7fadd57144494b131c.gif)

## Verifying Signatures

To verify a detached or embedded signature:

- Use the sender’s **public key**.
- Paste or load the signed message.

GpgFrontend will:

- Check the integrity.
- Report any mismatch or missing public keys.

> 📥 If the required public key is missing, GpgFrontend prompts you to import
> it.

![](https://image.cdn.bktus.com/i/2025/06/24/6ccba3133341e6e6ea095a2dc00bf23c63ed8f56.gif)

## Best Practices

- Always verify a message **before** decrypting when possible.
- Share only your **public key**, and **never** your private key.
- Use **Encrypt & Sign** for secure and authenticated communication.
- Use **Sign Only** for publishing documents or messages that require integrity
  but not secrecy.
