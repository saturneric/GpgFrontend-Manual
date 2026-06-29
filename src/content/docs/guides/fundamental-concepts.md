---
title: Fundamental Concepts for Beginners
description: "A beginner's guide to OpenPGP, GPG, and PGP: learn public and private keys, encryption, and digital signatures before using GpgFrontend."
sidebar:
  label: Fundamental Concepts
  order: 1
---

Every day you trust other people with private things: emails, files, backups, ID
documents, and passwords. OpenPGP lets you protect those things yourself, so only
the people you choose can read them. It works offline and needs no account.

New to **OpenPGP**, **GPG**, or **PGP**? This guide starts with the few ideas you
really need. Extra detail waits at the end, for when you want it.

:::tip[The whole idea in two sentences]

You have a **private key** that you keep secret, and a **public key** that you
share with others. That's the core of OpenPGP. Everything else builds on it.

:::

## What OpenPGP Does

OpenPGP lets you do two things:

- **Encrypt (lock)** messages and files, so only the right person can read them.
- **Sign** messages and files, so others can prove they came from you and weren't
  changed.

People use it for secure email, protecting files and backups, locking files
before uploading to cloud storage, sharing passwords with people they trust, and
checking that downloaded software is genuine.

## The Two Keys

You have two keys that work as a pair:

- **Public key**: You give this out. Others use it to lock messages for you and to
  check your signatures.
- **Private key**: You keep this secret. You use it to unlock messages sent to
  you and to sign things.

Think of a mailbox. Your **public key** is the slot anyone can drop mail into.
Your **private key** is the only key that opens it.

Keep your private key safe. If you lose it, you can't unlock your data. If someone
steals it, they can read your messages.

## Encrypting and Signing

**Encrypting (for privacy):** You lock a message with the other person's public
key. Only their private key can unlock it.

**Signing (for proof):** You sign a message with your private key. Anyone can use
your public key to check that it really came from you and wasn't changed.

You can do both at once: lock a message and sign it, so it's private and proven.

## Making Your First Key

When you make a key, GpgFrontend asks you to choose a few things: an algorithm
(the math it uses), a key size, your name and email, an expiration date, and a
passphrase.

**If you're new, just accept the defaults GpgFrontend suggests.** They are a safe
choice.

Pick a strong **passphrase**. It is your last line of defense: if someone copies
your private key file, the passphrase stops them from using it.

## Checking That a Key Is Real

A name and email on a key prove nothing. Anyone can make a key with any name. So
before you trust someone's public key, make sure it is really theirs.

The usual way is to compare the key's **fingerprint** (a unique ID code) using a
source you already trust: an official website, a signed release page, or in
person.

## A Few Safety Rules

- **Back up your private key** (and its revocation certificate) somewhere safe and
  offline. Lose it, and your encrypted data may be gone for good.
- **Use a strong passphrase.**
- **Revoke a key right away** if it is lost or stolen, and tell your contacts.
- **Check signatures** when you download software, to be sure the files weren't
  changed.

If you use **GpgFrontend Lite** or an rPGP key database, your keys live in the
app's own storage. Always export and back them up after you create or import them.

## Where to Go Next

You now know enough to begin. A good first path is:

1. [Install GpgFrontend](/overview/getting-started/) for your platform.
2. [Generate your first key pair](/guides/generate-key/), then back it up safely.
3. [Encrypt your first file](/guides/file-operations/) or
   [text message](/guides/text-operations/).
4. [Import and export keys](/guides/import-export-key-pair/) so you can exchange
   public keys with others.

If you ever feel stuck, the [FAQ](/overview/faq/) answers the most common
questions from new users.

---

## Going Deeper (Optional)

You can stop above and start using GpgFrontend. The sections below add detail for
when you're curious or need it.

### The Names: PGP, OpenPGP, GPG, rPGP

These names get mixed up a lot:

- **PGP** was the first paid program that started this style of encryption.
- **OpenPGP** is the open standard based on PGP.
- **GnuPG**, often called **GPG**, is the most widely used free program that
  follows OpenPGP.
- **rPGP** is a newer program (written in Rust) that GpgFrontend uses to try out
  newer features like OpenPGP v6.

For everyday use, most people use **GnuPG/GPG** because it works with the widest
range of other tools.

### Inside a Full Key: Primary Key and Subkeys

A full OpenPGP key is made of a few parts:

- A **primary key** that stands for your identity. It ties your name and email to
  the key and creates and manages the subkeys.
- One or more **subkeys** that do the daily jobs:
  - **Encryption subkey**: unlocks messages and files sent to you.
  - **Signing subkey**: signs your messages, files, or text.
  - **Authentication subkey**: proves who you are for logins, such as SSH (when
    supported).
- One or more **user IDs**, usually a name and email address.
- Extra details, such as when it was made, when it expires, the algorithm, and
  what it can be used for.

This keeps your identity separate from everyday tasks. Using subkeys for daily
work lowers the risk to your primary key. Advanced users keep the primary key
offline and use only subkeys on their everyday devices.

### What's in a Certificate

When you share your public key, you usually share an OpenPGP **certificate**. It
can include your public key, your user IDs, the extra details above, signatures
that link the user IDs and subkeys to the primary key, and optional
certifications from other people.

Remember: trust is not automatic. A valid signature only proves the signature
matches the key. You still have to decide whether the key really belongs to the
right person.

### Engines and Compatibility

OpenPGP is a standard, not one single app. GnuPG, rPGP, Sequoia PGP, RNP, and
others are different programs that follow it. They can usually work together when
they use matching formats and algorithms, but it isn't guaranteed. Newer features
like OpenPGP v6 and post-quantum algorithms may not work with older tools.

GpgFrontend supports more than one engine:

- **GnuPG**: the default, recommended engine for daily use and the best
  compatibility.
- **rPGP**: an experimental engine for trying newer OpenPGP features, including
  OpenPGP v6 and some post-quantum algorithms.

If you're new, use the **GnuPG engine** unless you specifically want to try the
newer features.
