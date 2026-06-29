---
title: Post-Quantum Cryptography
description: "Generate and use post-quantum OpenPGP keys in GpgFrontend, including ML-KEM (Kyber), ML-DSA, and SLH-DSA quantum-resistant algorithms."
sidebar:
  label: Post-Quantum Keys
---

GpgFrontend is one of the first desktop apps that lets you make and use
**post-quantum keys** with a few clicks, no command line needed. This page explains
in plain words what that means, why it might matter to you, and how to make your
first one.

## Why You Might Need This

Today's encryption is safe because breaking it would take even the fastest normal
computer billions of years. The math is just too hard. Think of it as a lock that
no machine on Earth can pick.

**Quantum computers** are a new and very different kind of computer. A big enough
one could do that hard math quickly, and pick today's locks. Machines that powerful
don't exist yet. But there is a catch:

> Someone can copy your locked messages **today**, save them, and wait. When a
> strong quantum computer finally arrives, they unlock everything they saved, even
> messages from years ago.

This is called **"harvest now, decrypt later."** So the real question isn't "can
anyone read this today?" It's "does this need to stay secret for many years?"

If the answer is yes, it makes sense to start using new, **quantum-proof**
encryption now, before quantum computers catch up. This is why the experts at NIST
created a new set of these algorithms, and why OpenPGP is starting to use them.

:::tip[Do you actually need this?]

- **Probably not yet, for everyday use.** If your secrets only matter for a short
  while, today's normal keys are perfectly safe.
- **Worth a head start** if you protect things that must stay private for a decade
  or more, like medical, legal, or personal records.
- **Still experimental.** See the warning at the bottom of this page before you
  rely on these keys.

:::

## What You Can Make

GpgFrontend offers the new NIST-approved post-quantum algorithms. They come in two
jobs, just like normal keys: some are for **encryption** (locking messages) and
some are for **signing** (proving a message is really from you).

A quick plain-words guide:

- **ML-KEM** (once called Kyber): for **encryption**. GpgFrontend always pairs it
  with a classic key, so your protection is never weaker than today's, even if one
  part is later found to have a flaw.
- **ML-DSA** (once called Dilithium): for **signing**, also paired with a classic
  key.
- **SLH-DSA** (SPHINCS+): also for **signing**. It is built on a very simple,
  well-trusted idea (hashing), which makes it the most cautious, safe-bet choice.

These all need the newer **version 6 (v6)** key format. The table below lists the
exact options for reference:

| Algorithm                  | OpenPGP Type | Purpose    | Engine support          |
| -------------------------- | ------------ | ---------- | ----------------------- |
| ML-KEM (Kyber768 + X25519) | Hybrid KEM   | Encryption | GnuPG 2.5.0, rPGP 0.1.2 |
| ML-KEM (Kyber1024 + X448)  | Hybrid KEM   | Encryption | GnuPG 2.5.0, rPGP 0.1.2 |
| ML-DSA-65 (+ Ed25519)      | Hybrid sign  | Signing    | rPGP 0.1.2              |
| ML-DSA-87 (+ Ed448)        | Hybrid sign  | Signing    | rPGP 0.1.2              |
| SLH-DSA-SHAKE-128S         | Hash-based   | Signing    | rPGP 0.1.2              |
| SLH-DSA-SHAKE-128F         | Hash-based   | Signing    | rPGP 0.1.2              |
| SLH-DSA-SHAKE-256S         | Hash-based   | Signing    | rPGP 0.1.2              |

## Make a Post-Quantum Key

1. Open **Key Management** and click **New Keypair** to open the **Generate Key**
   dialog.
2. Choose a post-quantum algorithm:
   - **Easy Mode**: open the **Profile** dropdown and pick a profile under the
     **Post-Quantum** heading.
   - **Advanced Mode** (the **Primary Key** / **Subkey** tabs): open the
     **Algorithm** dropdown and pick an option under the **Post-Quantum** heading.
     The list is grouped (classical, **ECC**, **Post-Quantum**), so the
     quantum-proof options are easy to spot.
3. Pick by job:
   - For **encryption**, choose an **ML-KEM (Kyber)** option.
   - For **signing**, choose **ML-DSA** or **SLH-DSA**.
4. Make sure the active engine supports your choice. Most of these options come from
   the **rPGP** engine, so switch engines if one isn't available.
5. Fill in your name, email, and validity period, then generate the key.

These algorithms need the **v6** key format. In Advanced Mode, GpgFrontend switches
to v6 and locks it automatically once you pick a post-quantum algorithm, so you
don't have to set it yourself.

That's it. You now hold a post-quantum OpenPGP key.

:::caution[Experimental, by design]

Post-quantum OpenPGP is based on a **draft standard** that is still changing, and
support here is **experimental**.

- These keys **don't work with classic PGP tools yet**, and most of these options
  are only in the **rPGP** engine.
- Treat them as a way to **try out and prepare for** the quantum-safe future, not
  as a replacement for protecting critical secrets today.
- The file format may change as the standard is finished.

For long-term signing and identity that must work everywhere, keep using a classic
key (such as Ed25519) alongside your post-quantum experiments.

:::

## Further Reading

- [Comparison of Cryptographic Algorithms](/extra/algorithms-comparison/)
- [NIST Post-Quantum Cryptography](https://csrc.nist.gov/projects/post-quantum-cryptography)
