---
title: Post-Quantum Cryptography
description: Generate and use post-quantum OpenPGP keys in GpgFrontend, including ML-KEM (Kyber), ML-DSA, and SLH-DSA quantum-resistant algorithms.
sidebar:
  label: Post-Quantum Keys
  order: 7
---

GpgFrontend is one of the first desktop OpenPGP applications that lets you
generate and use **post-quantum keys** from a graphical interface, no command
line required. This guide explains what post-quantum cryptography is, why it
matters today, and how to create your first quantum-resistant key.

## Why Post-Quantum Matters

Classical public-key algorithms such as RSA and elliptic curves (ECDSA, EdDSA,
ECDH) rely on math problems that a sufficiently large quantum computer could
solve. Such a computer does not exist yet, but the threat is already real
because of **"harvest now, decrypt later"**: an adversary can record your
encrypted messages today and decrypt them years later once quantum hardware
matures.

For anything that must stay confidential for a long time, switching to
**quantum-resistant** algorithms now is the only reliable defense. This is why
NIST standardized a new post-quantum (PQC) suite, and why the OpenPGP ecosystem
is adopting it.

## Supported Algorithms

GpgFrontend exposes the NIST-standardized PQC suite through the OpenPGP draft.
These algorithms require **version 6 (v6) keys**.

| Algorithm                  | OpenPGP Type | Purpose    | Engine support          |
| -------------------------- | ------------ | ---------- | ----------------------- |
| ML-KEM (Kyber768 + X25519) | Hybrid KEM   | Encryption | GnuPG 2.5.0, rPGP 0.1.2 |
| ML-KEM (Kyber1024 + X448)  | Hybrid KEM   | Encryption | GnuPG 2.5.0, rPGP 0.1.2 |
| ML-DSA-65 (+ Ed25519)      | Hybrid sign  | Signing    | rPGP 0.1.2              |
| ML-DSA-87 (+ Ed448)        | Hybrid sign  | Signing    | rPGP 0.1.2              |
| SLH-DSA-SHAKE-128S         | Hash-based   | Signing    | rPGP 0.1.2              |
| SLH-DSA-SHAKE-128F         | Hash-based   | Signing    | rPGP 0.1.2              |
| SLH-DSA-SHAKE-256S         | Hash-based   | Signing    | rPGP 0.1.2              |

A quick primer on the families:

- **ML-KEM** (formerly Kyber) is the standardized key-encapsulation mechanism
  used for **encryption**. GpgFrontend uses it in a _hybrid_ construction,
  combining it with a classical curve (X25519 or X448) so your security is at
  least as strong as the classical part even if one scheme is later weakened.
- **ML-DSA** (formerly Dilithium) is a lattice-based **signature** algorithm,
  also offered as a hybrid with Ed25519/Ed448.
- **SLH-DSA** (SPHINCS+) is a **stateless hash-based signature** scheme. It
  relies only on the security of hash functions, making it a conservative
  choice with very strong assurances.

## Generate Your First Post-Quantum Key

1. Open **Key Management** and click **New Keypair** to open the **Generate Key**
   dialog.
2. Choose how to pick a post-quantum algorithm:
   - **Easy Mode**: open the **Profile** dropdown and select a profile listed
     under the **Post-Quantum** section header.
   - **Advanced Mode** (the **Primary Key** / **Subkey** tabs): open the
     **Algorithm** dropdown and choose an entry under the **Post-Quantum**
     section header. The algorithm list is grouped into family tiers
     (classical, **ECC**, and **Post-Quantum**) so the quantum-resistant options
     are easy to find.
3. Pick an algorithm:
   - For **encryption**, choose an **ML-KEM (Kyber)** option (a subkey
     algorithm).
   - For **signing**, choose **ML-DSA** or **SLH-DSA**.
4. Make sure the active engine supports your choice. Most PQC algorithms are
   provided by the **rPGP** engine; you can switch engines if an option is not
   available.
5. Fill in your name, email, and validity period, then generate the key.

Post-quantum algorithms require the **v6** key format. In Advanced Mode the
**Key Format** is switched to v6 and locked automatically once a post-quantum
algorithm is selected, so you don't need to set it manually.

That's it, you now hold a post-quantum OpenPGP key.

:::caution[Experimental, by design]

Post-quantum OpenPGP is based on a **draft specification** that is still
evolving, and support here is **experimental**.

- These keys are **not yet interoperable** with classical PGP tools, and most
  PQC algorithms are currently available only through the **rPGP** engine.
- Treat PQC keys as a way to **experiment with and prepare for** the
  quantum-safe future, not as a drop-in replacement for protecting critical
  production secrets today.
- The on-disk format may change as the standard is finalized.

For long-lived signing and identity needs that must interoperate widely, keep
using a classical key (for example Ed25519) alongside your PQC experiments.

:::

## Further Reading

- [Comparison of Cryptographic Algorithms](/extra/algorithms-comparison/)
- [NIST Post-Quantum Cryptography](https://csrc.nist.gov/projects/post-quantum-cryptography)
