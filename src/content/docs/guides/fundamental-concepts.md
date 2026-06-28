---
title: Fundamental Concepts for Beginners
sidebar:
  label: Fundamental Concepts
  order: 1
---

Every day you trust other people with your private information: emails, files,
backups, identity documents, passwords. OpenPGP lets you protect that
information yourself, so only the people you choose can read it, and so others
can prove that a message or file genuinely came from you. It works offline, it
relies on no company or account, and it has protected journalists, developers,
and privacy-conscious people for decades.

If you're new to **OpenPGP**, **GPG (GNU Privacy Guard)**, or **PGP (Pretty Good
Privacy)**, this guide explains the fundamental concepts step by step.

:::tip[You don't need to memorize all of this]

Skim this page once to get the big picture, then come back to it when you need
it. You can start using GpgFrontend with just two ideas: you have a **private
key** you keep secret, and a **public key** you share with others. The rest will
make sense as you go.

:::

## What Is OpenPGP, GPG, and PGP?

**OpenPGP** is a standard for encrypting data, creating digital signatures, and
managing public/private keys. It is commonly used to protect emails, files,
software releases, and other sensitive information.

OpenPGP is mainly used for two purposes:

- **Encryption**: keeping messages and files private.
- **Digital signatures**: proving who created something and checking that it has
  not been modified.

The names can be confusing at first:

- **PGP** was the original commercial software that introduced this style of
  public-key encryption.
- **OpenPGP** is the open standard derived from PGP.
- **GnuPG**, often called **GPG**, is the most widely used free implementation of
  OpenPGP.
- **rPGP** is a newer Rust-based OpenPGP implementation used experimentally by
  GpgFrontend for newer features such as OpenPGP v6.

For normal daily use, most users still rely on **GnuPG/GPG** because it has the
broadest compatibility with existing OpenPGP tools.

## Understanding Key Pairs

OpenPGP is built around pairs of cryptographic keys:

- **Public Key**: Shared with others. They can use it to encrypt messages to you
  or verify your signatures.
- **Private Key**: Kept secret. You use it to decrypt messages sent to you and
  to sign messages or files.

A simple analogy: your public key is like a locked mailbox. Anyone can put mail
inside, but only your private key can open it.

A complete OpenPGP key usually includes:

- A **primary key** representing your identity.
- One or more **subkeys** for specific tasks such as encryption, signing, or
  authentication.
- One or more **user IDs**, usually containing a name and email address.
- Metadata such as creation date, expiration date, algorithm, and usage
  permissions.
- Optional signatures from yourself or other people.

This structure separates identity from daily cryptographic operations. It makes
key management more flexible and can reduce risk when subkeys are used for
routine work.

## Generating Your First Key Pair

When generating a key pair, you usually choose:

- A **cryptographic algorithm**, such as RSA or an elliptic-curve algorithm.
- A **key size or security level**, depending on the selected algorithm.
- A **user ID**, usually your name and email address.
- An **expiration date**, so the key does not remain valid forever.
- A strong **passphrase** to protect your private key.

A strong passphrase is important. If someone obtains a copy of your private key,
the passphrase helps prevent them from using it.

For beginners, the safest choice is usually the default algorithm recommended by
GpgFrontend and the selected OpenPGP engine. Advanced users can choose specific
algorithms when they need compatibility, performance, or experimental OpenPGP v6
features.

## Primary Keys and Subkeys Explained

Your **primary key** represents your OpenPGP identity. It is commonly used to:

- Bind user IDs, such as your name and email address, to your key.
- Certify or manage subkeys.
- Sign other people's keys when using trust-based workflows.

**Subkeys** are used for everyday tasks:

- **Encryption subkey**: used to decrypt messages or files encrypted to you.
- **Signing subkey**: used to sign messages, files, or text.
- **Authentication subkey**: used for authentication workflows, such as SSH-like
  use cases when supported.

Using subkeys for everyday work can reduce the risk of exposing your primary
key. Advanced users may keep their primary key offline and use only subkeys on
daily-use devices.

## Encryption and Digital Signatures

### Encryption: Keeping Data Private

To send someone an encrypted message:

1. You encrypt the message using the recipient's **public key**.
2. The recipient decrypts it using their **private key**.

This means only the holder of the matching private key can read the message.

Encryption protects confidentiality, but it does not automatically prove who
created the message. For that, use a digital signature.

### Digital Signatures: Proving Authenticity

Digital signatures help answer two questions:

- **Who signed this?**
- **Has it been changed since it was signed?**

To sign something:

1. You create a signature using your **private key**.
2. Others verify the signature using your **public key**.

A valid signature shows that the data has not been modified since it was signed
and that the signer had access to the corresponding private key.

For sensitive communication, encryption and signing are often used together:
encryption protects privacy, while signing provides authenticity and integrity.

## Practical Examples of OpenPGP Usage

Common real-world uses of OpenPGP include:

- **Secure email**: encrypting sensitive messages and signing email content.
- **File encryption**: protecting personal documents, backups, archives, and
  shared files.
- **Cloud storage protection**: encrypting files before uploading them to
  services such as Dropbox, Google Drive, OneDrive, or iCloud.
- **Software verification**: checking downloaded software, source archives, or
  package releases using digital signatures.
- **Team secrets sharing**: securely sharing passwords, credentials, or
  confidential documents with trusted recipients.
- **Long-term personal data protection**: encrypting tax records, identity
  documents, private notes, and other important files.

## Public Key Certificates and Trust

When you share your public key, you are usually sharing an OpenPGP
**certificate**. A certificate can include:

- Your public key.
- Your user IDs, such as name and email address.
- Metadata such as creation date, expiration date, algorithm, and usage
  permissions.
- Signatures that connect the user IDs and subkeys to the primary key.
- Optional certifications from other people.

A user ID is not proof of identity by itself. Anyone can create a key with any
name or email address. Before trusting a public key, you should confirm that it
really belongs to the person or project you expect.

You can verify a key by checking its fingerprint through a trusted channel, such
as an official website, a signed release page, an in-person exchange, or another
communication method you already trust.

In OpenPGP, trust is not automatic. A valid signature only proves that the
signature matches the key. You still need to decide whether the key itself
belongs to the right person or organization.

## Security Best Practices

For secure and effective OpenPGP usage:

- **Back up your private keys and revocation certificates**: Keep secure offline
  backups. If you lose your private key, encrypted data may become permanently
  inaccessible.
- **Use a strong passphrase**: A passphrase protects your private key if the key
  file is copied or exposed.
- **Protect your primary key**: Use subkeys for everyday encryption and signing
  when possible. Advanced users may keep the primary key offline.
- **Revoke compromised keys immediately**: If a private key is lost, stolen, or
  exposed, revoke it and notify your contacts.
- **Check compatibility before sharing new keys**: Newer OpenPGP v6 or
  post-quantum keys may not work with older tools.
- **Verify signatures when downloading software**: Signature verification helps
  confirm that downloaded files have not been tampered with.

If you use **GpgFrontend Lite** or an rPGP key database, key material may be
stored inside an application-managed database or sandboxed application data
directory. Always export and back up your keys after creating or importing them.

## OpenPGP Compatibility and Engines

OpenPGP is a standard, not a single application. GnuPG, rPGP, Sequoia PGP, RNP,
and other tools are different implementations of OpenPGP.

Most OpenPGP tools can work together when they use compatible key formats,
message formats, and algorithms. However, compatibility is not automatic. Newer
features such as OpenPGP v6, post-quantum cryptography, and hybrid algorithms
may not be supported by older tools.

GpgFrontend supports multiple OpenPGP engines:

- **GnuPG**: the default and recommended engine for daily use and maximum
  interoperability.
- **rPGP**: an experimental Rust-based engine for testing newer OpenPGP
  features, including OpenPGP v6 and selected post-quantum algorithms.

For beginners, the safest choice is to use the **GnuPG engine** unless you
specifically want to test rPGP, OpenPGP v6, or post-quantum features.

## GpgFrontend: Simplifying OpenPGP

Command-line OpenPGP tools can be difficult for new users. **GpgFrontend**
provides a graphical interface for common OpenPGP operations while still keeping
advanced users in control.

With GpgFrontend, you can:

- Create and manage OpenPGP keys visually.
- Encrypt and decrypt text, files, and folders.
- Sign data and verify digital signatures.
- Import, export, and organize public and private keys.
- Work with the mature GnuPG backend by default.
- Experiment with the rPGP backend, OpenPGP v6, and selected post-quantum
  algorithms when supported.

For normal daily use, GpgFrontend recommends the GnuPG engine for compatibility
and stability. The experimental rPGP engine is available for users who want to
try newer OpenPGP features or use the sandbox-friendly GpgFrontend Lite edition.

## Where to Go Next

You now know enough to start. A good first path is:

1. [Install GpgFrontend](/overview/getting-started/) for your platform.
2. [Generate your first key pair](/guides/generate-key/), then back it up safely.
3. [Encrypt your first file](/guides/file-operations/) or
   [text message](/guides/text-operations/).
4. [Import and export keys](/guides/import-export-key-pair/) so you can exchange
   public keys with others.

If you ever feel stuck, the [FAQ](/overview/faq/) answers the most common
questions from new users.
