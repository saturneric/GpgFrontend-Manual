---
title: Symmetric Encryption & Decryption
sidebar:
  label: Symmetric Crypto
---

## 🔐 What Is Symmetric Encryption?

**Symmetric encryption** is a method of securing data where the **same
password** is used to both encrypt and decrypt information.

Unlike **asymmetric encryption**, which uses a public/private key pair,
symmetric encryption relies on a single shared secret (the password). This
approach is:

- ✅ Fast and efficient
- ✅ Ideal for large files or quick one-time sharing
- ❗ Best used when both parties can safely share the password

> 📌 If someone intercepts the password, the encrypted data is no longer secure
> — so always handle password exchange carefully.

## 🔄 How It Works

1. You choose a **strong password**.
2. That password is used to **encrypt** the data.
3. Anyone with the **same password** can **decrypt** it.
4. No key pair is required — only the shared password.

> 📎 Encryption security depends entirely on the strength and secrecy of the
> password used.

## ✍️ Encrypting Data Symmetrically

To encrypt text using symmetric encryption in GpgFrontend (v2.1.9 and later):

Enable Symmetric Encryption Feature

1. Go to the Settings.
2. Under the Appearance tab, check the `Sym. Encrypt` checkbox to enable symmetric encryption functionality.

Access the Symmetric Encryption Button

1. After enabling, you’ll see a dedicated `Sym. Encrypt` button on the main interface.

Enter the Text or Select a File

- Input the plaintext you wish to protect in the text editor.
- Select a file to encrypt using the file panel.

Symmetric Encryption

1. Without selecting any public key, click the `Sym. Encrypt` button.
2. When prompted, enter a strong, unique password.
3. This password becomes your encryption key.
4. The text or file will be encrypted into ciphertext.
5. You can save or share the encrypted result.

> 🔐 The recipient will need the **exact same password** to decrypt the message.

## 🔓 Decrypting Symmetric Encrypted Data

To decrypt content that was encrypted symmetrically:

1. Paste the Ciphertext: The message should begin with `-----BEGIN PGP MESSAGE-----` and end with `-----END PGP MESSAGE-----`.
2. Initiate Decryption: Choose to decrypt the message.
3. Enter the Password: Input the **same password** that was used for
   encryption.
4. View the Plaintext: If the password is correct, the original message will be revealed.

> 🧠 If the password is incorrect or mistyped, decryption will fail.

## 💡 When to Use Symmetric Encryption?

Symmetric encryption is a great choice when:

- You’re encrypting something **for yourself** (e.g. storing private notes or
  backup files).
- You’re sharing data over a **secure channel**, and can **safely provide the
  password**.
- You don’t want to manage public/private key infrastructure.

However, it is **not ideal** for public communication where secure password
exchange is difficult.

## 🛡️ Tips for Better Security

- Always use a **strong, complex password** (longer is better).
- Never send passwords through insecure channels (e.g., unencrypted email).
- Consider using symmetric encryption as a supplement to public-key encryption —
  e.g., encrypt a file symmetrically, then encrypt the password with the
  recipient’s public key.
