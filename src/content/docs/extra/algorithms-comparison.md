---
title: Comparison of Cryptographic Algorithms
description: "Compare OpenPGP cryptographic algorithms supported by GpgFrontend, including RSA, ECC, and post-quantum options, across the GnuPG and rPGP engines."
sidebar:
  label: Comparison of Algorithms
---

GpgFrontend supports many algorithms across two engines: the mature **GnuPG**
backend and the experimental **rPGP** backend. When you pick one, it helps to
weigh four things: how strong it is, which engine supports it, the OpenPGP version
it needs, and whether other tools can read it.

This page starts with simple guidance and a quick comparison table, then explains
each algorithm in detail.

## Which Should You Choose?

Most people don't need to think hard about this. If you're not sure:

- **Just use the default.** GpgFrontend picks **Ed25519 / Curve25519** (a modern
  elliptic-curve key) with the GnuPG engine. It is fast, strong, and works with
  most tools.
- **Need to work with old systems?** Use **RSA 3072**. It has the broadest support
  across legacy clients and protocols.
- **Want to try post-quantum or OpenPGP v6?** Switch to the **rPGP engine**. These
  options are experimental and may not work with other tools yet.

### A Good Balance: RSA + Curve25519

For the best mix of compatibility and speed, you can use **RSA** for the
**primary key** (identity and signing other keys) and **Curve25519** for the
**subkeys** (signing, encryption, or authentication). RSA keeps you compatible with
older systems, while Curve25519 stays fast for everyday work.

## At a Glance

| Algorithm                | Group       | Used for         | Engines         | Notes                                  |
| ------------------------ | ----------- | ---------------- | --------------- | -------------------------------------- |
| RSA                      | Classical   | Sign + Encrypt   | GnuPG, rPGP     | Best compatibility; slower             |
| ElGamal (ELG-E)          | Classical   | Encrypt only     | GnuPG           | Rarely needed today                    |
| ECDSA (NIST curves)      | Elliptic    | Sign             | GnuPG, rPGP     | Standardized by NIST                   |
| EdDSA (Ed25519 / Ed448)  | Elliptic    | Sign             | GnuPG, rPGP     | Modern default for signing             |
| ECDH (Curve25519 / X448) | Elliptic    | Encrypt          | GnuPG, rPGP     | Modern default for encryption          |
| Brainpool curves         | Elliptic    | Sign + Encrypt   | GnuPG 2.3+      | Non-NIST alternative                   |
| secp256k1                | Elliptic    | Sign             | GnuPG 2.3+, rPGP| Used in blockchain                     |
| ML-DSA                   | Post-Quantum| Sign             | rPGP only       | Experimental, OpenPGP v6               |
| SLH-DSA                  | Post-Quantum| Sign             | rPGP only       | Experimental; large signatures         |
| Kyber / ML-KEM           | Post-Quantum| Encrypt          | GnuPG 2.5+, rPGP| Experimental; always hybrid            |

The exact choices you see depend on the engine, its version, and the key format.

## Classical Algorithms

### RSA (Rivest-Shamir-Adleman)

- **What it is**: one of the most widely used public key algorithms. Introduced in
  1977, it relies on the difficulty of factoring large prime numbers.
  ([more](https://en.wikipedia.org/wiki/RSA_cryptosystem))
- **Key sizes**: usually 2048 bits or larger; 4096 bits for higher security.
- **Used for**: both encryption and signing. The standard for SSL/TLS certificates
  and well supported on legacy systems.
- **Trade-off**: slower than elliptic-curve algorithms, especially key generation
  and decryption, because of its larger key sizes. As computers get faster, larger
  keys are needed to stay secure.

### ElGamal (ELG-E)

- **What it is**: an encryption-only algorithm based on the Diffie-Hellman problem.
  In OpenPGP it is used for encryption, not signing.
  ([more](https://en.wikipedia.org/wiki/ElGamal_encryption))
- **Key sizes**: usually 2048 bits or more.
- **Strength**: it produces a different ciphertext each time, even for the same
  message, which gives semantic security.
- **Trade-off**: slow, and its ciphertext is much larger than the plaintext. It is
  far less common than RSA or ECC today.

## Elliptic Curve Cryptography (ECC)

[Elliptic Curve Cryptography](https://en.wikipedia.org/wiki/Elliptic-curve_cryptography)
gives strong security with much smaller keys than RSA, which makes it a good fit
when computing power or storage is limited. OpenPGP uses ECC in a few forms.

- [**ECDH**](https://en.wikipedia.org/wiki/Elliptic-curve_Diffie%E2%80%93Hellman)
  (key exchange): lets two sides agree on a shared secret over an open channel,
  which is then used for encryption. It does not sign.
- [**ECDSA**](https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm)
  (signing): creates and checks digital signatures, so a reader can confirm a
  message came from you and wasn't changed.
- **EdDSA** (signing): a newer signature scheme, covered below.

### Common Curves

- [**NIST curves (P-256, P-384, P-521)**](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.186-5.pdf):
  standardized by NIST and widely used in secure communication. P-256 gives about
  128-bit security (enough for most uses); P-384 and P-521 raise this, with P-521
  giving around 256-bit security for high-security needs.
- [**Brainpool curves (P-256, P-384, P-512)**](https://www.rfc-editor.org/rfc/rfc5639):
  an alternative to the NIST curves with similar strength but independently chosen
  parameters. Often used where non-NIST curves are preferred for compliance.
- **Curve25519 and X448**: optimized for speed and common in modern apps.
  - [**Curve25519**](https://en.wikipedia.org/wiki/Curve25519): used for key
    exchange (the partner of [Ed25519](https://en.wikipedia.org/wiki/EdDSA#Ed25519)),
    with about 128-bit security. Very efficient.
  - [**X448**](https://en.wikipedia.org/wiki/Curve448): a higher-security option
    (about 224-bit), at a small cost in speed.
- [**secp256k1**](https://www.secg.org/sec2-v2.pdf): a non-NIST curve best known
  for its use in Bitcoin and other blockchains, where fast signature checking
  matters.

### EdDSA (Ed25519 and Ed448)

EdDSA is a modern signature algorithm built on elliptic curves. It is designed to
be faster, safer, and harder to misuse than older schemes like DSA or ECDSA.

- **Deterministic**: unlike ECDSA and DSA, it doesn't need a fresh random number
  for each signature, which avoids a common source of bugs and weak signatures.
- **Curves**:
  - [**Ed25519**](https://en.wikipedia.org/wiki/EdDSA#Ed25519): about 128-bit
    security, fast, with small keys. Great for secure messaging, blockchain, and
    most modern uses.
  - [**Ed448**](https://en.wikipedia.org/wiki/Curve448): about 224-bit security for
    cases that need stronger or longer-term protection, at some cost in speed.

### Why ECDH Can't Be a Primary Key

A **primary key** has to sign: it signs other keys to build trust, and it signs
data to prove ownership. **ECDH** is only a key-exchange algorithm, so it can't
sign and can't be a primary key. Signature algorithms like **ECDSA** and **EdDSA**
can, which is why they are used for primary keys. ECDH is used instead for
encryption subkeys.

### OpenPGP v6 and the 25519 Compatibility Catch

OpenPGP v6 ([RFC 9580](https://www.rfc-editor.org/rfc/rfc9580)) adds new algorithm
identifiers and formats for modern curves like **Ed25519**, **Ed448**, **X25519**,
and **X448**. These are encoded differently from the older 25519 keys that GnuPG
usually makes (EdDSA over Ed25519 and ECDH over Curve25519).

The rPGP engine always makes 25519 keys in the modern Ed25519 / X25519 encoding,
even when you choose the v4 format. It never makes the legacy GnuPG encoding. In
practice:

- **rPGP can import and use GnuPG's 25519 keys**, including older
  Curve25519/Ed25519 keys.
- **rPGP-made 25519 keys can't be imported into GnuPG yet**, in either v4 or v6
  format, because of the modern encoding. Treat them as rPGP-only.
- For compatibility with GnuPG users or older tools, make 25519 keys with the
  **GnuPG engine**.
- To test modern Ed25519/X25519 or OpenPGP v6 keys, use the **rPGP engine**, but
  don't expect those keys to work in GnuPG.

The simple rule: **GnuPG-made 25519 keys work in rPGP, but rPGP-made 25519 keys
should be treated as rPGP-only for now.**

## Post-Quantum Cryptography (PQC)

Post-Quantum Cryptography is a set of algorithms meant to stay secure even against
future large-scale quantum computers. In OpenPGP, PQC support is still new and
based on draft specifications, not settled practice.

GpgFrontend v2.2 adds experimental PQC key generation through its multi-engine
design, mainly via the Rust-based **rPGP** engine.

### ML-DSA (signing)

**ML-DSA** is a post-quantum signature algorithm derived from Dilithium, for
signing and verification.

In GpgFrontend it is available only through the experimental **rPGP** engine, and
only as a **hybrid** option (paired with a classical algorithm), not as a standard
GnuPG-compatible signing key. Supported combinations:

- **ML-DSA-65 + Ed25519**
- **ML-DSA-87 + Ed448**

These keys are for experimental OpenPGP v6 and rPGP work. Don't use them when you
need GnuPG compatibility.

### SLH-DSA (signing)

**SLH-DSA** is a stateless, hash-based post-quantum signature algorithm derived
from SPHINCS+. Its signatures can be much larger than usual, which makes it less
practical for everyday message signing.

In GpgFrontend it is available only through the experimental **rPGP** engine.
Supported variants:

- **SLH-DSA-SHAKE-128S**
- **SLH-DSA-SHAKE-128F**
- **SLH-DSA-SHAKE-256S**

These are mainly for testing, research, and trying out future OpenPGP v6 workflows.

### Kyber / ML-KEM (encryption)

**Kyber**, now standardized as **ML-KEM**, is a post-quantum key-encapsulation
mechanism used for encryption. In OpenPGP it is always used in **hybrid** form as
an encryption subkey, pairing a post-quantum part with a classical ECDH part.

Unlike ML-DSA and SLH-DSA above, Kyber is **not rPGP-only**. Both engines support
it:

- **GnuPG** 2.5.0 or later. The GnuPG bundled with GpgFrontend v2.2.1 is 2.5.20, so
  it works out of the box with the GnuPG engine.
- **rPGP** 0.1.2 or later.

Available sizes:

- **Kyber-768**
- **Kyber-1024**

Each is paired with a classical ECDH partner curve. Under GnuPG you get the full
set of partners (Curve25519, the NIST curves, the Brainpool curves, and X448).
Under rPGP, Kyber-768 pairs with Curve25519 and Kyber-1024 pairs with X448.

Hybrid KEM keys are more sensitive to compatibility than classic RSA or Curve25519
keys, and the two engines don't encode them the same way. If you need the widest
compatibility, prefer classic RSA or Curve25519 keys for now.
