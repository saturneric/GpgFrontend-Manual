---
title: Fundamental Concepts for Beginners
sidebar:
  label: Fundamental Concepts
  order: 1
---

If you're new to **GPG (GNU Privacy Guard)** or **PGP (Pretty Good Privacy)**,
this guide is for you. GPG is a free, open-source system for **encrypting
information** and **verifying identity**. It's widely used for secure
communication, file protection, and digital signing.

Let’s walk through the core concepts in a beginner-friendly way.

## 🔐 What Is a Key Pair?

At the heart of GPG is the **key pair**: two mathematically linked keys.

- **Public Key**: Share this with anyone. Others use it to:
  - Send you encrypted messages.
  - Verify your digital signature.
  
- **Private Key**: Keep this secret. You use it to:
  - Decrypt messages sent to you.
  - Sign data so others know it’s really from you.

> 🧠 Think of it like a mailbox:
> - Your public key is the address — people can send you letters.
> - Your private key is the key to open the mailbox — only you can read what’s
>   inside.

## 🔧 Generating a Key Pair

To use GPG, you first create a key pair. During creation, you’ll choose:

- A **cryptographic algorithm** (e.g., RSA, ECC).
- A **key size** (larger sizes are more secure but slower).
- A **passphrase** to protect the private key.

> 🔒 Your passphrase adds a layer of protection — even if someone gets your key
> file, they can’t use it without this password.

## 🧩 What Are Subkeys?

A GPG identity doesn’t stop at one key pair. You can create **subkeys** under
your primary key. These are used for specific tasks:

- **Encryption Subkey**: Used to encrypt/decrypt data.
- **Signing Subkey**: Used to create/verifiy digital signatures.

Subkeys are tied to your identity, but they can be revoked or replaced
independently.

> ✅ Tip: Use subkeys for everyday tasks and keep your **primary key offline** or
> backed up securely.

## 🧱 Understanding the Primary Key

Your **primary key** is your core identity. It:
- Links to your user ID (usually name + email).
- Signs your subkeys.
- Can certify other people's public keys (used to build trust networks).

### Why Is It So Important?

If someone gains access to your **primary private key**, they can impersonate
you. That’s why:

- It should be **backed up** securely.
- It’s best to use **subkeys** for daily operations.
- Some people even keep their primary key **offline** for maximum safety.

## ✉️ How Encryption Works

Imagine you want to send a private message to someone:

1. You encrypt the message using their **public key**.
2. Only their **private key** can decrypt it.
3. You can also add your **signature** using your private key.
4. They can **verify your signature** with your public key.

This ensures:
- **Privacy**: No one but the intended recipient can read the message.
- **Authenticity**: The recipient knows the message is from you.

## 🖋️ What Is Digital Signing?

Signing is like sealing a document with your unique fingerprint. It allows
others to:

- Confirm the message hasn’t been changed.
- Confirm that **you** are the sender.

Digital signatures are used to:
- Sign emails.
- Sign files or software packages.
- Sign other people's public keys (to build trust).

## 📦 Real-Life Use Cases

### Secure Email

You want to email a sensitive document:
- Encrypt it using the recipient’s public key.
- Sign it with your private key.
- The recipient decrypts and verifies it.

### Software Publishing

You release a file or program online:
- You sign it.
- Users can verify the signature before using it.

### Building Trust

You meet someone at a conference:
- You exchange and sign each other’s keys.
- Anyone who trusts your key may now also trust theirs.

## ✅ Best Practices for New Users

1. **Back Up Your Keys**: Store your private key and revocation certificate in a
   secure, offline location.
2. **Use Strong Passphrases**: The private key is only as safe as the password
   protecting it.
3. **Separate Daily and Master Keys**: Use subkeys for regular work; keep your
   primary key protected.
4. **Update When Needed**: Cryptography evolves — review and rotate keys as
   needed.
5. **Revoke If Compromised**: If your private key is stolen or lost, revoke it
   immediately and inform your contacts.
6. **Understand the Web of Trust**: GPG builds trust by people signing each
   other's keys — this forms a decentralized trust model.

## 🧭 Summary

GPG is a powerful tool for privacy and digital identity. By learning:
- How keys work,
- When to encrypt vs. sign,
- And how to protect your credentials,

You’re taking a big step toward securing your digital life.

## 🧰 Where Does GpgFrontend Fit In?

While GPG/PGP itself is powerful, it is mostly command-line based — which can be
intimidating for beginners.

This is where **GpgFrontend** comes in.

GpgFrontend is a graphical interface built on top of GnuPG. It helps users
perform key operations such as:

- Generating and managing key pairs
- Encrypting and decrypting messages or files
- Signing and verifying content
- Uploading and fetching keys from key servers
- More...

All of this can be done through a **clear and user-friendly interface**, making
GPG accessible without needing to learn complex commands.

Whether you're just starting to explore encrypted communication or already
managing multiple keys, GpgFrontend acts as a bridge — combining the strength of
GPG with simplicity and clarity.

> 🧩 You focus on **secure communication** — let GpgFrontend handle the
> complexity behind it.