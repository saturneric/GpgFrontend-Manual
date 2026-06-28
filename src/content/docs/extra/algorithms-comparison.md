---
title: Comparison of Cryptographic Algorithms
description: Compare OpenPGP cryptographic algorithms supported by GpgFrontend, including RSA, ECC, and post-quantum options, across the GnuPG and rPGP engines.
sidebar:
  label: Comparison of Algorithms
---

When choosing cryptographic algorithms for OpenPGP key management and data
security, it is important to consider not only security strength, but also
engine support, OpenPGP version, and interoperability. GpgFrontend supports both
the mature GnuPG backend and the experimental rPGP backend, so some algorithms
are available only in specific engines or workflows.

## RSA (Rivest-Shamir-Adleman)

- **Key Characteristics**: [RSA](https://en.wikipedia.org/wiki/RSA_cryptosystem)
  is one of the most widely used public key algorithms. It was introduced in
  1977 and is based on the difficulty of factoring large prime numbers.
- **Key Sizes**: Typically, RSA keys are 2048 bits or larger. For higher
  security, keys up to 4096 bits are used.
- **Use Cases**: RSA is versatile and can be used for both encryption and
  digital signatures. It is widely supported in legacy systems and remains a
  standard for SSL/TLS certificates.
- **Performance**: RSA operations, particularly key generation and decryption,
  can be slower compared to elliptic curve algorithms due to larger key sizes.
- **Security**: Provides strong security, but larger key sizes are required as
  computational power increases.

## ElGamal Encryption (ELG-E)

- **Key Characteristics**: [ElGamal encryption
  (ELG-E)](https://en.wikipedia.org/wiki/ElGamal_encryption) is an asymmetric
  encryption algorithm used for public-key cryptography. It is based on the
  Diffie-Hellman problem and is used for encryption, not for digital
  signatures in OpenPGP.

- **Key Sizes**: Like DSA, ElGamal typically uses large key sizes, often 2048
  bits or more, to ensure a high level of security.

- **Use Cases**: ElGamal is used in encryption and key exchange protocols. It is
  particularly valued for its ability to generate different ciphertexts for the
  same plaintext each time it is encrypted, providing semantic security.
  However, it is less commonly used than RSA or ECC-based methods.

- **Performance**: ElGamal encryption is computationally intensive, especially
  when compared to RSA or ECC algorithms. The encryption process is relatively
  slow, and the resulting ciphertexts are significantly larger than the
  plaintext.

- **Security**: ElGamal offers strong security, especially when large key sizes
  are used. However, its performance drawbacks and the complexity of managing
  larger ciphertexts have limited its widespread adoption.

## Understanding ECDH and ECDSA

[Elliptic Curve Cryptography
(ECC)](https://en.wikipedia.org/wiki/Elliptic-curve_cryptography) is a powerful
cryptographic method that provides robust security with relatively small key
sizes, making it ideal for environments where computational power and storage
are limited. ECC is commonly used in two main algorithms: ECDH and ECDSA.

### ECDH and ECDSA: Core Differences

- [ECDH (Elliptic Curve
  Diffie-Hellman)](https://en.wikipedia.org/wiki/Elliptic-curve_Diffie%E2%80%93Hellman)
  is a key exchange algorithm that enables two parties to securely establish a
  shared secret over an insecure channel. This shared secret can then be used
  for encryption. ECDH is not directly used for encryption or signing; instead,
  it is crucial for securely setting up encryption keys.

- [ECDSA (Elliptic Curve Digital Signature
  Algorithm)](https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm)
  is used for creating digital signatures, allowing one party to sign a message
  and another to verify its authenticity. ECDSA ensures that the message has not
  been tampered with and that it originates from the claimed sender.

### Common ECC Algorithms and Their Use Cases

Elliptic Curve Cryptography (ECC) offers a range of algorithms and curves
tailored to different cryptographic needs. Below is an overview of commonly used
ECC algorithms and their specific applications.

- [NIST Curves (P-256, P-384,
  P-521)](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.186-5.pdf):
  Standardized by the National Institute of Standards and Technology (NIST),
  these curves are widely utilized in secure communication protocols. For
  example:
  - **ECDH NIST P-256**: Provides approximately 128-bit security, making it
    suitable for most encryption scenarios.
  - **ECDSA NIST P-256**: Commonly employed for digital signatures, offering
    robust security for authentication purposes.
  - **Higher Key Sizes**: P-384 and P-521 increase security levels
    proportionally, with P-521 offering around 256-bit security, making it ideal
    for high-security environments.

- [BrainPool Curves (P-256, P-384,
  P-512)](https://www.rfc-editor.org/rfc/rfc5639): BrainPool curves serve
  as alternatives to NIST standards, providing similar security levels but with
  independently developed parameters.
  - **Use Cases**: Often used in regions or industries that prefer non-NIST
    curves for compliance or operational reasons.
  - **Examples**: **ECDH BrainPool P-256** and **ECDSA BrainPool P-256** offer a
    balance between security and performance, catering to scenarios where NIST
    standards are not desired.

- **CV25519 and X448**: These curves are optimized for performance and are
  widely used in modern cryptographic applications.
  - [ECDH CV25519](https://en.wikipedia.org/wiki/Curve25519): A counterpart to
    [Ed25519](https://en.wikipedia.org/wiki/EdDSA#Ed25519), this curve is
    designed for key exchange and offers approximately 128-bit security. It is
    highly efficient in secure communications.
  - [ECDH X448](https://en.wikipedia.org/wiki/Curve448): A higher-security
    variant providing 224-bit security, suitable for applications requiring more
    robust encryption. However, it comes with a slight trade-off in
    computational efficiency.

- [SECP256K1](https://www.secg.org/sec2-v2.pdf): Defined by the Standards for
  Efficient Cryptography Group (SECG), SECP256K1 is distinct from NIST curves
  and has gained significant traction due to its adoption in blockchain
  technologies.
  - **Key Use Case**: Widely used for cryptographic operations in Bitcoin and
    other blockchain systems, where efficient signature verification is crucial.
  - **Performance**: Optimized for computational efficiency, making it an
    excellent choice for environments requiring rapid cryptographic operations.

### EdDSA (Edwards-Curve Digital Signature Algorithm)

EdDSA is a modern digital signature algorithm based on elliptic curve
cryptography. It is specifically designed to be more efficient, secure, and
resistant to common implementation errors compared to older algorithms like DSA
or ECDSA.

#### Key Characteristics

- **Deterministic Signature Generation**: Unlike ECDSA and DSA, which require
  secure random numbers for each signature, EdDSA uses deterministic methods,
  reducing the risk of vulnerabilities caused by poor randomness.
- **Elliptic Curves Used**: EdDSA supports two primary curves:
  - [Ed25519](https://en.wikipedia.org/wiki/EdDSA#Ed25519): Provides 128-bit
    security and is optimized for speed and compact key sizes.
  - [Ed448](https://en.wikipedia.org/wiki/Curve448): Provides higher 224-bit
    security for environments requiring greater protection but at the cost of
    performance.

#### Use Cases

- **Ed25519**: Ideal for secure messaging (e.g., Signal), blockchain, and other
  modern cryptographic protocols where performance and efficiency are critical.
- **Ed448**: Used in environments requiring stronger security, such as highly
  sensitive communications or systems with long-term security needs.

### OpenPGP v6 Ed25519 and X25519 Compatibility

OpenPGP v6, as defined by RFC 9580, introduces new public-key algorithm
identifiers and wire formats for modern elliptic-curve algorithms such as
**Ed25519**, **Ed448**, **X25519**, and **X448**.

This is important because these modern algorithm identifiers are not encoded in
the same way as the older OpenPGP 25519 keys commonly generated by GnuPG.
Existing GnuPG workflows use the legacy encodings (EdDSA over Ed25519 and ECDH
over Curve25519), while the modern RFC 9580 algorithms use the newer Ed25519 and
X25519 identifiers.

The rPGP engine used by GpgFrontend always generates 25519 keys with the modern
Ed25519 / X25519 encoding, even when you select the v4 key format. It does not
produce the legacy GnuPG encoding. In GpgFrontend, this means:

- **rPGP can import and use 25519 keys generated by GnuPG**, including existing
  legacy Curve25519/Ed25519 OpenPGP keys.
- **rPGP-generated 25519 keys cannot currently be imported into GnuPG**,
  regardless of whether you chose the v4 or v6 key format, because they use the
  modern Ed25519/X25519 encoding rather than the legacy one. These keys should
  be treated as rPGP-only.
- If you need interoperability with existing GnuPG users or older OpenPGP tools,
  generate 25519 keys through the GnuPG engine rather than the rPGP engine.
- If you want to test the modern Ed25519/X25519 or OpenPGP v6 key generation,
  use the rPGP engine, but do not expect those generated keys to work in GnuPG.

For most users, the practical rule is simple: **GnuPG-generated 25519 keys can be
used by rPGP, but rPGP-generated 25519 keys should be considered rPGP-only for
now.**

### Why ECDH Cannot Be Used as a Primary Key Algorithm

**ECDH (Elliptic Curve Diffie-Hellman)** is a key exchange algorithm used to
establish shared secrets between two parties. It is not designed for signing
or verification, which are essential for primary key functionalities.

**ECDSA (Elliptic Curve Digital Signature Algorithm)** and **EdDSA** are
signature algorithms, specifically designed for identity verification and
creating/verifying digital signatures, making them suitable for primary keys.

Primary keys are used to:

1. **Sign Other Keys**: Establish trust relationships by signing subordinate
   keys.
2. **Verify Identities**: Sign and verify data, proving ownership of the key.

Since ECDH does not provide signature functionality, it cannot be used for these
purposes. Instead, it is commonly used for subkeys dedicated to encryption or
key exchange tasks.

## Recommended Algorithms for Compatibility and Security

Cryptographic key selection is critical to ensuring both robust security and
practical interoperability across diverse systems. With a wide array of
algorithms available, it is important to balance compatibility, performance, and
future-proof security when designing a cryptographic infrastructure. The
following recommendations highlight widely accepted algorithms suitable for most
scenarios, from legacy environments to modern applications.

### RSA (2048-bit or 3072-bit)

- **Why**: RSA offers the broadest compatibility across legacy systems,
  libraries, and cryptographic protocols.
- **When to Use**: Choose RSA when you need to ensure interoperability with
  older clients or systems that may not support newer elliptic curve algorithms.

### Curve25519

- **Why**: Curve25519 is highly efficient, secure, and compact, making it a great
  choice for modern cryptographic applications.
- **When to Use**: Use Curve25519 in environments where compatibility with
  modern systems is sufficient, and you want to benefit from its speed and
  smaller key sizes.

### Combining RSA and Curve25519

For the best balance between compatibility and performance, consider using RSA
for the **primary key** (for identity verification and signing other keys) and
Curve25519 for **subkeys** (used for signing, encryption, or authentication).
This approach ensures:

- **Maximum Compatibility**: RSA as the primary key ensures interoperability
  with older systems.
- **Modern Efficiency**: Curve25519 as subkeys provides better performance for
  modern operations.

## Post-Quantum Cryptography and OpenPGP PQC Drafts

Post-Quantum Cryptography (PQC) refers to cryptographic algorithms designed to
remain secure against attacks by large-scale quantum computers. In the OpenPGP
ecosystem, PQC support is still emerging and is currently based on draft
specifications rather than long-established deployment practice.

GpgFrontend v2.2 introduces experimental PQC-related key generation options
through the new multi-engine architecture, especially through the experimental
Rust-based **rPGP** engine.

### ML-DSA

**ML-DSA** is a post-quantum digital signature algorithm derived from Dilithium.
It is designed for signing and verification.

In GpgFrontend, ML-DSA is currently available only through the experimental
**rPGP** engine. It is exposed as a hybrid signature option rather than as a
traditional standalone GnuPG-compatible signing key.

Currently supported rPGP hybrid ML-DSA signature combinations include:

- **ML-DSA-65 + Ed25519**
- **ML-DSA-87 + Ed448**

These keys are intended for experimental OpenPGP v6 and rPGP-based workflows.
They should not be used when GnuPG interoperability is required.

### SLH-DSA

**SLH-DSA** is a stateless hash-based post-quantum digital signature algorithm
derived from SPHINCS+. Compared with many traditional signature algorithms,
SLH-DSA signatures can be significantly larger and may be less suitable for
everyday message signing.

In GpgFrontend, SLH-DSA is currently available only through the experimental
**rPGP** engine.

Currently supported rPGP-only SLH-DSA variants include:

- **SLH-DSA-SHAKE-128S**
- **SLH-DSA-SHAKE-128F**
- **SLH-DSA-SHAKE-256S**

These options are mainly useful for testing, research, and evaluating future
OpenPGP v6 workflows.

### Kyber / ML-KEM Hybrid Encryption

**Kyber**, now standardized as **ML-KEM**, is a post-quantum key encapsulation
mechanism used for encryption-related workflows. In OpenPGP, it is always used
in hybrid form as an encryption subkey, pairing a post-quantum KEM component
with a classical ECDH component.

Unlike the ML-DSA and SLH-DSA signature algorithms above, the Kyber hybrid KEM
is **not rPGP-only**. It is supported by both engines:

- **GnuPG** (version 2.5.0 or later). The GnuPG bundled with GpgFrontend v2.2.1
  is 2.5.20, so these options are available out of the box with the GnuPG
  engine.
- **rPGP** (version 0.1.2 or later).

The available subkey sizes are:

- **Kyber-768**
- **Kyber-1024**

Each is paired with a classical ECDH partner curve. Under the GnuPG engine the
full set of partner curves (Curve25519, the NIST P-curves, the BrainPool curves,
and X448) is available, while the rPGP engine currently pairs Kyber-768 with
Curve25519 and Kyber-1024 with X448.

In practical terms, hybrid KEM support is more interoperability-sensitive than
classic RSA or Curve25519 keys, and the two engines do not encode these keys
identically. Users who need maximum compatibility with older clients should
still prefer classic RSA or Curve25519 keys.
