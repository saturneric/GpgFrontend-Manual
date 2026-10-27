---
title: View Key Pair Details
description: "Inspect OpenPGP key pair details in GpgFrontend, including owner UIDs, primary key, subkeys, algorithms, and validity information."
sidebar:
  label: Key Pair Details
  order: 10
---

The **Key Details** window shows everything about a key: who it belongs to, its
primary key and subkeys, the signatures on it, and the actions you can take.

To open it, right-click a key in the **Key ToolBox** or the **KeyPair Management**
window and choose **Show Key Details**. Double-clicking a key also opens this window.

![][img-1]

## General Info

This part is on the **KeyPair** tab. It helps you manage the key. Here is what
each piece means.

### Owner

Who the key belongs to. This isn't fixed: you can change it by creating a new UID
in the UID section and setting it as the primary UID. OpenPGP splits this into
**Name**, **Email**, and **Comment**.

![][img-2]

### Primary Key

The primary key is the heart of the key pair. Without its private part you can't do
management tasks like adding or revoking subkeys, much like not being able to open
the keyring. To learn more, see [Fundamental Concepts](/guides/fundamental-concepts).

A "missing" primary key means the _private part_ of the primary key is absent, not
that the whole key is gone. Remember: the primary key and every subkey is itself a
pair of a public and a private key.

![][img-3]

#### Key ID

A short, unique ID for the key, fixed when the key is made. This is the primary
key's ID. It is shorter and easier to read than the fingerprint.

Click the Key ID to copy it. A small note, **Copied to clipboard**, confirms
it.

#### Algorithm

The algorithm the primary key was made with. It decides what the key can do. For
example, RSA can encrypt and sign, while DSA can only sign. Modern elliptic-curve
algorithms like ECDH (for key exchange) and ECDSA (for signatures) give strong
security with shorter keys.

#### Algorithm Detail

Shows the key type and length together, and is sometimes more exact than the
Algorithm field, naming the specific method such as ED25519 or NISTP256.

![][img-4]

#### Key Size

The length of the primary key. Longer keys are harder to break but slower to use.
For RSA, 2048 bits is generally safe enough.

#### Usage

What the key pair can do, combining the abilities of the primary key and all
subkeys. The possible abilities are **Certificate** (it can sign other keys and
its own subkeys), **Encrypt**, **Sign**, and **Auth** (it can prove who you are,
for example to log in). For example, if any subkey can sign, **Sign** is listed
here.

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

Which key format the primary key uses, shown as `v4`, `v5`, or `v6`.

- `v4` is the widely compatible default, from the older OpenPGP standard.
- `v6` is the format from the current OpenPGP standard, RFC 9580. Post-quantum
  keys need it.
- `v5` is the format from **LibrePGP**, a separate standard that split off from
  OpenPGP. GnuPG 2.5 and later can make and use v5 keys.

The two standards are not compatible with each other. A v5 key works with
GnuPG and other LibrePGP tools, and a v6 key works with RFC 9580 tools. Many
tools support only one of the two.

:::caution[The rPGP engine cannot read v5 keys]

rPGP follows RFC 9580 only. It cannot use a v5 key. If you work with v5 keys,
use a GnuPG key database for them. See [Multi-Key Database](/advanced/key-database/).

:::

#### Last Update

When the key pair's content last changed. Adding a UID or subkey counts as a
change.

#### Primary Key Existence

Whether the primary key's actual content is present, shown as **Exists** or **Not
Exists**. If it is missing but the key pair still has usable subkeys, you can keep
using the key for normal tasks. You just can't change its content (no adding UIDs
or subkeys) or use it to sign other keys.

### Fingerprint

![][img-5]

The fingerprint is a unique code people use to quickly check that a key is the one
they expect. It is unique for every key in the world. (You can also compare the
Key ID above.) This is the primary key's fingerprint.

Click the fingerprint to copy it. The copy has no spaces, even though the
window shows the fingerprint in groups.

## UID Info

This part is on the **UIDs** tab. A User ID (UID) is the label that says who a key belongs to, like a name tag on a
keyring. It gives you a rough idea whether a key is the one you expect, but for
sure identification you should compare fingerprints or key IDs. A key can have
several UIDs, but only one **primary UID**, which is always shown first.

![View Key Pair Details UID][img-6]

Each UID has three parts: **Name**, **Email**, and **Comment**. The name should be
at least five characters and the email must be a valid format; comments are
flexible.

You cannot delete the primary UID. On a v4 key you also cannot delete the last
UID, because the key needs it to keep working. Add a new UID first if you want
to replace it. This rule is new in v2.2.3.

### Certifications on a UID

The lower part of the window, **Certifications of Selected User ID**, shows the
signatures (certifications) on the selected UID (the one you clicked, not the
one ticked). Signatures are how trust is built: when someone
receives your public key, they can sign your UID with their key to vouch for it,
then share the signed key on a key server. The more people who do this, the more
trustworthy the key looks.

![][img-7]

You can also certify a UID with one of your own private keys: right-click the
UID and choose **Certify User ID...**. To take back a certification you made,
right-click it in the lower part and choose **Revoke Certification...**. See
[Trust Chain Management](/guides/openpgp-trust-manage/). A primary UID with
many valid certifications is generally seen as more trustworthy.

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
- **Overlap**: if more than one subkey can sign, GpgFrontend asks which one to
  use when you sign text or a file.
- **More algorithms**: subkeys can use more algorithms than the primary key, but
  for daily use the effect is the same.
- **Security isolation**: if a subkey is compromised, you revoke just that one and
  the trust anchored by the primary key stays intact. But if the primary key is
  compromised, the whole key structure is at risk.

The **Keychain** tab lists the primary key and all subkeys. For each one, the
list shows its **Key ID**, **Key Type**, **Algorithm** and **Usage**. If there
are more than five, scroll the list.

Click a row to see all its details below the list, such as its size, dates and
fingerprint. Here, too, you can click the Key ID or the fingerprint to copy it.

![][img-8]

### Key in Smart Card

The **Key in Smart Card** field shows **Yes** if a (sub)key's private part has
been moved to a hardware smart card, and **No** if not.

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

### What You Can Do to a Single Subkey

Right-click a subkey in the list for actions that apply to just that one:

- **Change Passphrase**: set a new passphrase for this subkey alone, leaving
  the others as they are. New in v2.2.2.
- **Move to Card**: move this subkey onto a smart card. See
  [OpenPGP Smart Cards](/guides/smart-card/).
- **Edit Expire Date**: give this subkey its own expiry date.

:::note[Setting an expiry now works on rPGP too]

Until v2.2.2, changing an expiry date needed the GnuPG engine. The rPGP engine
can now do it as well, for both primary keys and subkeys.

:::

## Operations

These actions are on the **Operations** tab. What you can do here depends on whether the key pair has only a public key, or a
private key too.

### On a Public Key

These are the actions available for a public key.

![][img-9]

#### Export Public Key

Saves the public key to a file, ready to share with others, upload to a key
server, or back up.

#### Key Server Operations

A dropdown for working with key servers (a place where public keys are stored and
shared). It has three choices:

- **Publish Public Key to Key Server**: upload the public key.
- **Refresh Public Key From Key Server**: get the latest copy of the public key.
- **Check Publication Status**: ask the key server whether it has this key.

See [Key Server Operations](/guides/key-server-operations/) for details.

:::note[Changed in v2.2.3]

The Key Details window no longer checks the key server by itself, and no longer
shows a notice that the key is published. Use **Check Publication Status**
when you want to know.

:::

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

![][img-10]

#### Export Public Key

Saves the public key to a file, for sharing, uploading to a key server, or backup.

#### Export Private Key

Exports the private key. There are two choices:

- **Export Full Secret Key**: the entire private key with all its information.
  Use this for a full backup or to move the key to another system.
- **Export Shortest Secret Key**: only the essential parts, with less data.
  Useful for more secure transfers or environments with strict requirements.

#### Modify Expiration Datetime (Primary Key)

Changes the expiration date and time of the primary key. This helps you manage the
key's lifecycle and keep it valid for as long as you need.

#### Modify Password

Changes the password that protects the private key. Worth doing if you think the
current one may be exposed, or as part of regular good habits.

#### Key Server Operations

The same key server dropdown as for a public key: publish, refresh, or check
the public key on the key server.

#### Revoke Certificate Operation

A dropdown with two choices: **Generate Revoke Certificate** creates a
revocation certificate for the key, and **Import Revoke Certificate** imports an
existing one. See [Key Revocation](/advanced/key-revocation/). Revoke a key if it is compromised or no longer needed: this marks it invalid
so it can't be misused. The revocation is usually uploaded to a key server so
others learn the key is revoked.

## How a Key Shows Up in Results

After you verify a signature or decrypt a message, the result panel says what
happened. Some lines there come from the key's details on this page.

- **Valid**: the signature is correct. With the rPGP engine you see **Valid**,
  not **Fully Valid**. rPGP has no owner trust, so it does not say how much you
  trust the signer. Check the fingerprint to be sure who signed.
- **Signing Key Not Authorized**: the signature is correct, but the key that
  made it does not have **Sign** in its usage. The signature is not accepted.
- **Signing Key Expired**: the key has expired. With the rPGP engine, if the key
  had already expired _when the signature was made_, the result says so and the
  signature fails.
- **Symmetric Encryption Algorithm**: after you decrypt a message with a key,
  this line names the cipher and its mode, for example `AES256.OCB`. The rPGP
  engine now shows this line too.

:::note[Changed in v2.2.3]

These result lines are new or clearer for the rPGP engine.

:::

[img-1]: https://image.cdn.bktus.com/i/2026/10/25/92db1358322ffa54f09c03e1987992036ccbe535-0.webp
[img-2]: https://image.cdn.bktus.com/i/2026/10/25/7436a873ef7c37c2cfb3d45d60455135c55c868c-0.webp
[img-3]: https://image.cdn.bktus.com/i/2026/10/25/5655ee4b9ebc6ff66c2dbb40b85e47e0193f7794-0.webp
[img-4]: https://image.cdn.bktus.com/i/2026/10/25/e52f93629923e0939157d70ccbb58dc05d730420-0.webp
[img-5]: https://image.cdn.bktus.com/i/2026/10/25/cbc63a372425aef80aa9d271174294208381bfe7-0.webp
[img-6]: https://image.cdn.bktus.com/i/2026/10/25/953b4f647f0f8324f973cdcf4483fc63edc7c3fd-0.webp
[img-7]: https://image.cdn.bktus.com/i/2026/10/25/0cdd4f431999095ea958f8d2fd5ce0bbb0ce0902-0.webp
[img-8]: https://image.cdn.bktus.com/i/2026/10/25/6edf084823f685aad6e9c92c01faf16a2e4e5a32-0.webp
[img-9]: https://image.cdn.bktus.com/i/2026/10/25/765b3e3054c7b1a0dadf9f539ee9b3c3f09dc939-0.webp
[img-10]: https://image.cdn.bktus.com/i/2026/10/25/806f6e0bab705122dfc3b5e524b484b93912ec4a-0.webp
