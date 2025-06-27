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

## PGP and GPG: What’s the Difference Today?

When people talk about “PGP,” they usually mean the OpenPGP standard for
encrypted communication—not the original commercial PGP software. GPG (GNU
Privacy Guard) is the free, open-source tool most people use today. It fully
supports the OpenPGP standard and is available for all major platforms.

In short:

- PGP was the original software, now rarely used.
- GPG is the open-source standard tool for modern encrypted email, files, and
  signatures.

If you’re just starting out, you almost always want to use GPG or a tool built
on top of GPG.able, but if you prefer open-source freedom and regular updates,
GPG is the usual choice.

## What Is a Key Pair?

In GPG, a **key pair** consists of a public key and a private key that are
mathematically linked.

**Public Key**: Think of it as a locked mailbox. Anyone can drop a letter (your
encrypted message) into the mailbox and lock it.

- Others use it to encrypt messages they send to you.
- Others use it to verify your digital signature.

**Private Key**: This is the only key that opens the locked mailbox. You—and
only you—can retrieve and read the letters inside.

- Decrypt messages sent to you.
- Sign your own messages or files so others know they truly came from you.

:::tip[Everyday Analogy]

Imagine you’ve installed a mailbox on the street. Anyone can deposit letters
into it (encrypt information), but only you—holding the mailbox key—can open it
and read what’s inside.

:::

## Generating a Key Pair

To use GPG, you first create a key pair. During creation, you’ll choose:

- A **cryptographic algorithm** (e.g., RSA, ECC).
- A **key size** (larger sizes are more secure but slower).
- A **passphrase** to protect the private key.

:::caution
🔒 Your passphrase adds a layer of protection — even if someone gets your key
file, they can’t use it without this password.
:::

## What Are Subkeys?

A GPG identity doesn’t stop at one key pair. You can create **subkeys** under
your primary key. These are used for specific tasks:

- **Encryption Subkey**: Used to encrypt/decrypt data.
- **Signing Subkey**: Used to create/verifiy digital signatures.

Subkeys are tied to your identity, but they can be revoked or replaced
independently.

> Tip: Use subkeys for everyday tasks and keep your **primary key offline** or
> backed up securely.

## Understanding the Primary Key

Your **primary key** is your core identity. It:

- Links to your user ID (usually name + email).
- Signs your subkeys.
- Can certify other people's public keys (used to build trust networks).

:::caution

If someone gains access to your **primary private key**, they can impersonate
you. That’s why:

- It should be **backed up** securely.
- It’s best to use **subkeys** for daily operations.
- Some people even keep their primary key **offline** for maximum safety.

:::

## How Encryption Works

Imagine you want to send a private message to someone:

1. You encrypt the message using their **public key**.
2. Only their **private key** can decrypt it.
3. You can also add your **signature** using your private key.
4. They can **verify your signature** with your public key.

This ensures:

- **Privacy**: No one but the intended recipient can read the message.
- **Authenticity**: The recipient knows the message is from you.

## What Is Digital Signing?

Signing is like sealing a document with your unique fingerprint. It allows
others to:

- Confirm the message hasn’t been changed.
- Confirm that **you** are the sender.

Digital signatures are used to:

- Sign emails.
- Sign files or software packages.
- Sign other people's public keys (to build trust).

## Real-Life Use Cases

GPG is useful in many situations beyond email or software. Here are some
practical examples where encryption and digital signatures can protect your
privacy, secure your data, or build trust with others.

### Protecting Cloud Backups

You store sensitive files (like financial records or personal photos) in the
cloud. Before uploading, you encrypt them with your GPG public key. Even if the
cloud provider is hacked, only you can decrypt and access your data.

### Sharing Passwords Securely

You need to share a server password with a remote teammate. Instead of sending
it as plain text, you encrypt the password file with their public key. Only they
can decrypt and read it.

### Verifying Software Downloads

You want to install open-source software from the internet. Before running the
installer, you check the author’s digital signature with GPG. If the signature
is valid, you know the file wasn’t tampered with.

### Securing Personal Notes

You keep a journal or confidential notes on your laptop. You encrypt these notes
with your own public key. Even if your device is stolen, no one else can read
your information.

### Proving Document Authenticity

You sign a PDF contract before sending it to a business partner. They can verify
your digital signature to confirm the document really came from you and hasn’t
been altered.

### Open Source Contributions

You contribute code to an open-source project on GitHub. You sign your commits
and tags with your GPG key, so everyone knows the code changes are really from
you.

## Public Key Certificates

A public key in GPG/PGP is not just a raw cryptographic key. It is always
packaged as a certificate, which contains more than just the key itself.

A public key certificate includes:

- The public key data (for encryption and verifying signatures)
- The User ID (your name and email address)
- Signatures made by your own primary key and, optionally, by other people

### Why Are Certificates Important?

- Binding Identity: The certificate links your key to your identity, such as
  your name and email. This way, people can verify that the key truly belongs to
  you.
- Establishing Trust: Others can “sign” your public key, vouching for your
  identity. This signature acts as a recommendation, forming a “Web of Trust.”
- Subkey Relationship: If you use subkeys (for encryption or signing), their
  certificates include signatures from your primary key. This proves that each
  subkey really belongs to your primary identity, and not to someone else.

### Example

When you share your public key, you are actually sharing a certificate that:

- Includes your identity and any subkeys
- Shows cryptographic proof that the subkeys are authorized by your primary key
- May be signed by other people who trust your identity

This is why you should always distribute your full public key certificate—not
just the bare key!

## Best Practices for New Users

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

## Where Does GpgFrontend Fit In?

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

:::tip

You focus on **secure communication** — let GpgFrontend handle the complexity
behind it.

:::
