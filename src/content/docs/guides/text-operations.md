---
title: Text Operations
description: "Encrypt, decrypt, sign, and verify text in GpgFrontend using OpenPGP public key cryptography with simple, intuitive workflows."
sidebar:
  order: 4
---

GpgFrontend lets you do four things with text: **encrypt** it (hide it),
**decrypt** it (read it), **sign** it (prove it came from you), and **verify** a
signature (check it really did). This page walks through each one.

![](https://image.cdn.bktus.com/i/2026/06/30/8a3b4ad29fce3f6969e8cdb2a10f9efcb06f7ba0.webp)

## Before You Start

These tasks use a pair of keys:

- **Public key**: used to **encrypt** a message for someone, or to **verify** their
  signature.
- **Private key**: used to **decrypt** a message sent to you, or to **sign** your
  own.

So before you begin, [make your own key pair](/guides/generate-key/) and swap
public keys with the people you write to. You encrypt with their public key; they
decrypt with their private key.

## Encrypt Text

To hide a message so only one person can read it, encrypt it with **their public
key**. Only their private key can open it.

This way:

- The result is short.
- It does **not** reveal who sent it, which is good when you want to stay
  anonymous.

:::tip

Don't encrypt with your own public key unless the message is meant for you. Use
the recipient's public key, or only you will be able to read it.

:::

![](https://image.cdn.bktus.com/i/2025/06/24/19483c04524fd94afff85cac502a1030bdb4c477.gif)

## Decrypt Text

To read an encrypted message sent to you, paste or load the ciphertext into
GpgFrontend. The tool then:

- Picks the correct **private key** for you.
- Tells you if it can't find a matching key.

You don't need to choose a key by hand. GpgFrontend matches it for you.

![](https://image.cdn.bktus.com/i/2025/06/24/5e16d1a75fb7e7bfb4d14f7fadd57144494b131c.gif)

## Sign Text

To prove a message came from you, sign it with **your private key**. The text stays
readable; signing adds proof, not secrecy.

- It confirms you wrote it.
- Anyone with your public key can check it.

Before you sign, look at the key's `Usage` column for an `S`, which means the key
can sign.

![](https://image.cdn.bktus.com/i/2025/06/24/8c6db160d26f94e75138134d319c29bd2c3736b7.gif)

## Verify a Signature

To check that a signed message is genuine, use the **sender's public key**. Paste
or load the signed message, and GpgFrontend will:

- Check that the message wasn't changed.
- Report any mismatch or a missing public key.

:::note

If you don't have the sender's public key yet, GpgFrontend asks you to import it
first.

:::

![](https://image.cdn.bktus.com/i/2025/06/24/6ccba3133341e6e6ea095a2dc00bf23c63ed8f56.gif)

## Safety Tips

- **Verify before you trust.** Check a signature before you act on a message.
- **Share only your public key.** Never give out your private key.
- **Encrypt and sign together** for messages that should be both private and
  proven.
- **Sign only** (no encryption) for public documents that need to be trusted but
  not hidden.
