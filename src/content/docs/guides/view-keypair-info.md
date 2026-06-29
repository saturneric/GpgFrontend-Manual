---
title: View Key Pair Details
description: "Inspect OpenPGP key pair details in GpgFrontend, including owner UIDs, primary key, subkeys, algorithms, and validity information."
sidebar:
  label: Key Pair Details
  order: 7
---

The **Key Details** window shows everything about a key: who it belongs to, its
primary key and subkeys, the signatures on it, and the actions you can take.

To open it, right-click a key in the **Key Toolbox** or the **Key Management**
window and choose **Show Key Details**. Double-clicking a key also opens this window.

![](https://image.cdn.bktus.com/i/2025/06/24/707eab9708c7cf9af472a5e05295d132d831f223.webp)

## General Info

This part of the window helps you manage the key. Here is what each piece means.

### Owner

Who the key belongs to. This isn't fixed: you can change it by creating a new UID
in the UID section and setting it as the primary UID. OpenPGP splits this into
**Name**, **Email**, and **Comment**.

![](https://image.cdn.bktus.com/i/2025/06/24/a648820ee997bce65d3b65ebb7c3056b37e1597d.webp)

### Primary Key

The primary key is the heart of the key pair. Without its private part you can't do
management tasks like adding or revoking subkeys, much like not being able to open
the keyring. To learn more, see [Fundamental Concepts](/guides/fundamental-concepts).

A "missing" primary key means the _private part_ of the primary key is absent, not
that the whole key is gone. Remember: the primary key and every subkey is itself a
pair of a public and a private key.

![](https://image.cdn.bktus.com/i/2025/06/24/8b3235e625749d20effc4a7f334e7dacd2688923.webp)

#### Key ID

A short, unique ID for the key, fixed when the key is made. This is the primary
key's ID. It is shorter and easier to read than the fingerprint.

#### Algorithm

The algorithm the primary key was made with. It decides what the key can do. For
example, RSA can encrypt and sign, while DSA can only sign. Modern elliptic-curve
algorithms like ECDH (for key exchange) and ECDSA (for signatures) give strong
security with shorter keys.

#### Algorithm Detail

Shows the key type and length together, and is sometimes more exact than the
Algorithm field, naming the specific method such as ED25519 or NISTP256.

![](https://image.cdn.bktus.com/i/2025/06/24/1a4c3220e4952de2ba8bbdfc01a42d48dce6337c.webp)

#### Key Size

The length of the primary key. Longer keys are harder to break but slower to use.
For RSA, 2048 bits is generally safe enough.

#### Usage

What the key pair can do, combining the abilities of the primary key and all
subkeys. The possible abilities are **Certify**, **Encrypt**, **Sign**, and
**Auth**. For example, if any subkey can sign, **Sign** is listed here.

#### Owner Trust Level

How much you trust this key's owner to correctly verify and sign other keys, part
of the web-of-trust model. This field is shown only when the active engine reports
owner trust (GnuPG); engines that don't support it hide the field.

#### Create Date

When the primary key was made, shown in your local time.

#### Expires On

When the primary key expires. After that it can't be used for any operation, and
its subkeys stop working too. You can change the expiration time whenever you like,
or set it to never expire, as long as the primary key's private part exists.

#### Key Format Version

The OpenPGP packet format of the primary key, shown as `v4` or `v6`. `v4` is the
widely compatible default; `v6` is the modern RFC 9580 format used for
post-quantum and other newer keys.

This field is shown only when the active engine can report it. The rPGP engine
reads the key packet and shows the format version, while GnuPG/GPGME does not, so
it is hidden for keys loaded through the GnuPG engine.

#### Last Update

When the key pair's content last changed. Adding a UID or subkey counts as a
change.

#### Primary Key Existence

Whether the primary key's actual content is present, shown as **Exists** or **Not
Exists**. If it is missing but the key pair still has usable subkeys, you can keep
using the key for normal tasks. You just can't change its content (no adding UIDs
or subkeys) or use it to sign other keys.

### Fingerprint

![](https://image.cdn.bktus.com/i/2025/06/24/bc688aa06bc3db294001b429018e5a79e888be44.webp)

The fingerprint is a unique code people use to quickly check that a key is the one
they expect. It is unique for every key in the world. (You can also compare the
Key ID above.) This is the primary key's fingerprint.

## UID Info

A User ID (UID) is the label that says who a key belongs to, like a name tag on a
keyring. It gives you a rough idea whether a key is the one you expect, but for
sure identification you should compare fingerprints or key IDs. A key can have
several UIDs, but only one **primary UID**, which is always shown first.

![View Key Pair Details UID](https://image.cdn.bktus.com/i/2025/06/24/6ba422bf970ce94533b798e9ebb24e2465f3d45e.webp)

Each UID has three parts: **Name**, **Email**, and **Comment**. The name should be
at least five characters and the email must be a valid format; comments are
flexible.

### Signatures on a UID

The lower part of the window shows the signatures on the selected UID (the one you
clicked, not the one ticked). Signatures are how trust is built: when someone
receives your public key, they can sign your UID with their key to vouch for it,
then share the signed key on a key server. The more people who do this, the more
trustworthy the key looks.

![](https://image.cdn.bktus.com/i/2025/06/24/c79c00d20a087f7a123fbbbf65bd1fd5e7c22bee.webp)

You can also sign a UID with the primary key of another key pair. A primary UID
with many valid signatures is generally seen as more trustworthy.

Some signatures may not show the signer's UID, as in the image above. To identify
them, import the matching key from another source, such as a key server. The Key
ID is shown, which helps you find and import the right key.

## Subkey Info

Subkeys are a core GnuPG feature that improves both security and flexibility. They
can feel complex at first, so here are the basics:

- **Keyring model**: think of your key pair as a keyring, with one primary key and
  zero or more subkeys.
- **Primary key vs subkeys**: the primary key is the root of trust. It certifies
  subkeys and is kept for critical actions like signing other keys or adding UIDs.
- **Daily work**: subkeys handle tasks like signing and encryption, even when the
  primary key is absent or unavailable.
- **Overlap**: if two subkeys can both sign, the earlier one is used.
- **More algorithms**: subkeys can use more algorithms than the primary key, but
  for daily use the effect is the same.
- **Security isolation**: if a subkey is compromised, you revoke just that one and
  the trust anchored by the primary key stays intact. But if the primary key is
  compromised, the whole key structure is at risk.

The Key Details window lists the primary key and all subkeys with their properties
(algorithm, size, usage, and so on), so you can manage them at a glance.

![](https://image.cdn.bktus.com/i/2025/06/24/3b87a8d639d8be4cf99d6fc4fc1b5d8c4168be3d.webp)

### Key on a Smart Card

Shows whether a (sub)key's private part has been moved to a hardware smart card.

- When a key is moved to a smart card, its private part is physically transferred
  to the card and removed from your local key database.
- This can't be undone. The private key now lives only on the card and can't be
  pulled back.
- It is strong protection against malware and key theft: using that key to sign or
  decrypt now needs the card present and unlocked.

:::tip

Moving your encryption or signing subkey to a smart card is a great choice if you
want the strongest security.

:::

## Operations

What you can do here depends on whether the key pair has only a public key, or a
private key too.

### On a Public Key

These are the actions available for a public key.

![](https://image.cdn.bktus.com/i/2025/06/24/56b96c1420da618873ca707c6e7da4ab6e1d7a25.webp)

#### Export Public Key

Saves the public key to a file, ready to share with others, upload to a key
server, or back up.

#### Key Server Operations

A dropdown for working with key servers (a place where public keys are stored and
shared). For example, you can refresh your copy of the public key with updates from
the server.

#### Set Owner Trust Level

Sets how much you trust this key's owner to correctly verify and sign other keys,
part of the web-of-trust model. This affects how your system judges the signatures
that owner makes.

:::note

Owner trust is a GnuPG concept, available only with the GnuPG engine. With the
rPGP engine, this button (and the Owner Trust Level field in General Info) is
hidden.

:::

### On a Private Key

When the key pair includes a private key, you get more actions, covering both the
public and private parts.

![](https://image.cdn.bktus.com/i/2025/06/24/55ac60792266c3e13254b53a47fe468cdba93048.webp)

#### Export Public Key

Saves the public key to a file, for sharing, uploading to a key server, or backup.

#### Export Private Key

Exports the private key. There are usually two modes:

- **Export Complete Private Key**: the entire private key with all its
  information. Use this for a full backup or to move the key to another system.
- **Export Minimal Private Key**: only the essential parts, with less data. Useful
  for more secure transfers or environments with strict requirements.

#### Modify Expiration Datetime (Primary Key)

Changes the expiration date and time of the primary key. This helps you manage the
key's lifecycle and keep it valid for as long as you need.

#### Change Password

Changes the password that protects the private key. Worth doing if you think the
current one may be exposed, or as part of regular good habits.

#### Key Server Operations

A dropdown for working with key servers using the public key, such as uploading it
or refreshing it from the server.

#### Revoke Certificate Operation

A dropdown to create a revocation certificate for the key, or import an existing
one. Revoke a key if it is compromised or no longer needed: this marks it invalid
so it can't be misused. The revocation is usually uploaded to a key server so
others learn the key is revoked.
