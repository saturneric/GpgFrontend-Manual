---
title: Generate Key Pair
description: "Create GnuPG-compatible OpenPGP key pairs in GpgFrontend, from simple templates to advanced control over algorithm, key size, and expiry."
sidebar:
  order: 3
---

GpgFrontend makes it easy to create OpenPGP key pairs that work with GnuPG. **If
you're new, click New Keypair, type your name, and click Continue until you
reach Generate.** GpgFrontend fills in safe defaults for everything else.

## Open the Key Generation Window

In the **Main Window**, click **New Keypair**. You can also open the **Keys**
menu and choose **New Keypair**. The **Generate Key** window opens.

![][img-1]

The window walks you through four steps: **Identity**, **Key Type**,
**Validity & Protection** and **Review**. Click **Continue** to go to the next
step, or **Back** to change something.

:::note[Changed in v2.2.4]

Making a key is now a guided window with steps. It used to be one window with
the tabs **Easy Mode**, **Primary Key** and **Subkey**. The choices that were
on the **Primary Key** and **Subkey** tabs are now under **Expert Mode**. See
[Choose Everything Yourself](#choose-everything-yourself-expert-mode).

:::

## Step 1: Identity

Type who the key is for. Others see this name and address when they look up
your key.

- **Name**: Required. Your full name.
- **Email**: Optional. If you fill it in, it must be a valid email address.
- **Comment**: Optional. Helps tell this key apart from others, for example
  `Work`.

**Fill In Anonymously** makes up a name and an address that reach nobody. This
is handy for throwaway or test keys, when you don't want to link the key to a
real name or address. How the made-up identity looks is set in
[Settings](/guides/settings/#the-key-generation-page).

A few rules apply to what you can type here:

- **Continue** stays greyed out until you type a name.
- The name and comment cannot contain `(`, `)`, `<`, `>` or control
  characters.
- A name shorter than five characters is allowed, but GpgFrontend asks you to
  confirm it first. Short names are usually a typo, and they make your key
  harder for other people to recognise.

At the bottom, the window says which key database the key will be saved in.
To use another one, close the window, switch to that
[key database](/advanced/key-database/), and start again.

## Step 2: Key Type

Choose what kind of key to make. If you are unsure, keep the one marked
**Recommended**.

- **Modern** (**Recommended**): small, fast keys for signing and encryption.
  All current OpenPGP software understands them.
- **Compatibility**: an RSA key, for older systems and software that only
  accept RSA. Larger and slower to use.
- **Hybrid encryption**: messages sent to you are also protected against
  future quantum computers. Only recent software can encrypt to this key. This
  choice only shows up when your engine supports it. See
  [Post-Quantum Cryptography](/guides/post-quantum/).

![The Key Type step][img-2]

For other key types, open **Advanced options** and pick one from **Other
profile**. A **profile** is a saved set of key choices, such as the algorithm
and how long the key is valid. You can manage profiles in
[Settings](/guides/settings/#the-key-generation-page).

## Step 3: Validity & Protection

- **Valid for**: how long the key can be used. The default is **2 years**. You
  can pick a period, **Never**, or **Custom date**. A key that expires stops
  being usable on its own if you lose it. You can extend it at any time before
  then.
- **Protect the secret key with a passphrase**: on by default. Keep it on.
  You are asked for the passphrase while the key is made. With GnuPG, GnuPG
  asks in a window of its own. For a post-quantum or hybrid key, it may ask
  a second time for the subkey.

If you turn the passphrase off, a warning reminds you that anyone who gets
your secret key file can then sign and decrypt as you.

![The Validity & Protection step][img-3]

## Step 4: Review and Generate

1. Check the summary: your user ID, the key type, when it expires, and whether
   it has a passphrase.
2. Click **Generate**.

   ![The Review step, with the Generate button][img-4]

3. If asked, type a strong **passphrase**, and type it again to confirm.
4. A **Key Generated** message shows your new key's fingerprint. Click **OK**.

## Make a Key in One Click

**Quick Generate** makes a key straight away, with no questions. It uses the
default profile and a made-up identity, both from
[Settings](/guides/settings/#the-key-generation-page). This is handy for test
keys.

To use it, open the **Keys** menu and choose **Quick Generate**. You can also
hold down or right-click the **New Keypair** button and choose it there.

![Quick Generate under the New Keypair button][img-5]

If the default profile or the identity pattern in Settings cannot be used,
GpgFrontend asks if you want to make the key step by step instead.

:::note[New in v2.2.4]

**Quick Generate** and the **Key Generation** settings page are new.

:::

---

## Choose Everything Yourself (Expert Mode)

You can skip this. GpgFrontend's defaults are a safe choice.

Turn on the **Expert Mode** switch at the bottom left of the window, on step 1
or 2. Step 2 then becomes **Key Details**, where you choose:

- **Start from**: begin with **Custom** or with any profile, then change what
  you need.
- **Primary key**: the **Algorithm**, **Key length**, **Usage** (**Encrypt**,
  **Sign**, **Authenticate**) and when it **Expires**. For hybrid algorithms,
  **Paired with** and **Its key length** also appear.
- **Key format**: **v4 (Compatible)** or **v6 (Modern)**. This is only shown
  with the rPGP engine. Post-quantum algorithms always use v6.
- **Add a subkey**: tick it to add a second key under the primary one, usually
  for encryption. It gets the same choices as the primary key.

![The Key Details step with Expert Mode on][img-6]

With Expert Mode on, the expiry is set for each key here, so step 3 only asks
about the passphrase.

To keep your choices for later, click **Save as Profile…** and give them a
name. GpgFrontend remembers whether Expert Mode was on for next time.

## Advanced Options

You can skip this section unless you need fine control. It covers the full list of
algorithms and some compatibility notes.

### Supported Algorithms for the Primary Key

A primary key stands for your identity and certifies your user IDs, so it must be
able to sign or certify. That's why the primary key list only shows
signing-capable algorithms. Encryption-only algorithms (such as ECDH, X448,
Curve25519, ElGamal, or Kyber/ML-KEM) are used for subkeys instead.

The algorithms you see depend on the engine, its version, and the key format.

| Algorithm group                 | Purpose                      | Engine                          |
| ------------------------------- | ---------------------------- | ------------------------------- |
| RSA                             | Sign / Encrypt / Auth / Cert | GnuPG, rPGP (3072 bits or more) |
| DSA                             | Sign / Auth / Cert           | GnuPG only                      |
| Ed25519 / Ed448                 | Sign / Auth / Cert           | GnuPG, rPGP                     |
| NIST P-256 / P-384 / P-521      | Sign / Auth / Cert           | GnuPG, rPGP                     |
| Brainpool P-256 / P-384 / P-512 | Sign / Auth / Cert           | GnuPG 2.3+                      |
| secp256k1                       | Sign / Auth / Cert           | GnuPG 2.3+                      |
| SLH-DSA-SHAKE variants          | PQC Sign / Auth              | rPGP only                       |
| ML-DSA hybrid variants          | Hybrid PQC Sign / Auth       | rPGP only                       |

:::note[Some old choices are gone on rPGP]

Since v2.2.2, the rPGP engine will not make weak keys any more, following
RFC 9580:

- **DSA** cannot be made at all.
- **RSA below 3072 bits** is no longer offered.
- **secp256k1** is no longer offered. The current OpenPGP standard does not
  include this curve.

This only affects making new keys. Old RSA-1024, RSA-2048, DSA, and secp256k1
keys still import and still work. The GnuPG engine still offers all of them,
for compatibility with older setups.

:::

:::note[Changed in v2.2.3]

On rPGP, the smallest RSA key for a new key went up from 2048 to 3072 bits. New
secp256k1 keys can now only be made with GnuPG. GpgFrontend also no longer
deletes the last UID of a v4 key.

:::

### Compatibility Notes

Some keys made by one engine can't be used by the other. Keep these points in
mind before you share a key:

- **rPGP 25519 keys are rPGP-only.** rPGP can import 25519 keys made by GnuPG, but
  not the other way around. When rPGP makes an Ed25519 or Curve25519 key, it uses
  the modern RFC 9580 encoding, not the older encoding GnuPG uses, so GnuPG can't
  read it, even if you pick the v4 format.
- **rPGP post-quantum keys are rPGP-only too.** ML-DSA, SLH-DSA, and hybrid KEM
  keys made by rPGP always use the OpenPGP v6 format. They are meant for testing
  and rPGP-based work, not for use with GnuPG.
- **GnuPG chooses its own key format.** When you use the GnuPG engine, GnuPG picks
  the format based on its version and settings. GpgFrontend doesn't set it, so
  the **Key format** choice is not shown. Current releases make **v4** keys, but
  newer versions (such as the 2.5.x line) may make **v5** keys.
- **A v4 key always keeps at least one UID.** A v4 key stores its usage and
  expiry with its UIDs (User IDs, the name and email on the key). So GpgFrontend
  will not let you delete the last UID of a v4 key. Add a new UID first if you
  want to replace it. v6 keys do not have this limit.
- **v5 keys are LibrePGP, not RFC 9580.** LibrePGP is a separate standard that
  split off from OpenPGP. A v5 key works with GnuPG and other LibrePGP tools,
  but the rPGP engine cannot read one, and neither can many other OpenPGP
  tools. Keep v5 keys in a GnuPG key database.

:::caution[Check the format before sharing widely]

If you need your key to work with as many tools as possible, check what format
your engine and version actually produce before you share the key.

:::

[img-1]: https://image.cdn.bktus.com/i/2026/10/25/95cc2834979501ae38df682d66247dc014cd829e-0.webp
[img-2]: TODO
[img-3]: TODO
[img-4]: TODO
[img-5]: TODO
[img-6]: TODO
