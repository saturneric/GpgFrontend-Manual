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

## Understanding the Basics

Public key cryptography relies on key pairs:
- **Public Key**: Used to encrypt or verify.
- **Private Key**: Used to decrypt or sign.

Before performing encryption or signing operations, users must generate their
own key pair and exchange public keys with their communication partners.

## Encrypting Text

### Only Encrypt
Use the recipient's **public key** to encrypt plaintext. This method:
- Produces a shorter ciphertext.
- Does **not** reveal the sender's identity.
- Is ideal when anonymity is preferred.

> 🔐 Tip: Don’t use your own public key to encrypt unless you're sending a
> message to yourself.

![](https://image.cdn.bktus.com/i/2023/11/16/07c99019-318a-3b85-ea63-0d473ebcd7ec.gif)

### Encrypt & Sign
This method encrypts the message with the recipient's public key and signs it
with **your own private key**, ensuring:
- Confidentiality
- Message authenticity
- Proof of origin

To use this method:
- Choose the recipient’s public key.
- Select **your private key** with signing capability (`Usage = S`).

> 📄 The resulting ciphertext is longer due to the signature. The Info Board
> will display signature details after encryption.

![](https://image.cdn.bktus.com/i/2023/11/16/cb4ac40a-9830-7429-8447-7ada6bc6571b.gif)

## Signing Text

### Signature Only
Use your **private key** to sign text without encrypting it:
- This confirms authorship.
- Anyone with your public key can verify it.

Check the key’s `Usage` column for `S` to confirm it's suitable for signing.

![Signature
Only](https://image.cdn.bktus.com/i/2023/11/16/9c95a381-52b9-4d2b-c21d-38fdc6cbc76d.gif)

### Sign with Encryption
Sign and encrypt together by selecting the recipient's public key and your own
private signing key:
- Ensures both confidentiality and authenticity.
- Common in secure messaging or business communication.

![](https://image.cdn.bktus.com/i/2023/11/16/fd98e968-5e59-7bee-abea-99ab234be7a6.gif)

---

## Decrypting Text

### Decrypt Only
Paste or load the ciphertext into GpgFrontend. The tool will:
- Automatically use the correct **private key**.
- Notify you if no valid key is available.

> ✅ No need to check `Usage` manually; the tool handles key matching.

![](https://image.cdn.bktus.com/i/2023/11/16/a4ded61d-fb5b-cbf2-f0ec-e3b26e79f172.gif)

### Decrypt & Verify
If the message was signed, GpgFrontend will:
- Verify the signature using the **sender’s public key**.
- Display whether the signature is valid.

Use this for added assurance of sender authenticity and message integrity.

![](https://image.cdn.bktus.com/i/2023/11/16/9e06ce22-f98d-47f1-ea76-e4e23b6dd32d.gif)

---

## Verifying Signatures

To verify a detached or embedded signature:
- Use the sender’s **public key**.
- Paste or load the signed message.

GpgFrontend will:
- Check the integrity.
- Report any mismatch or missing public keys.

> 📥 If the required public key is missing, GpgFrontend prompts you to import
> it.

![](https://image.cdn.bktus.com/i/2023/11/16/fbde7130-72c3-1fce-8366-47643fc0e804.gif)

## Best Practices

- Always verify a message **before** decrypting when possible.
- Share only your **public key**, and **never** your private key.
- Use **Encrypt & Sign** for secure and authenticated communication.
- Use **Sign Only** for publishing documents or messages that require integrity
  but not secrecy.