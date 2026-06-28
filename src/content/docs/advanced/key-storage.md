---
title: How Keys Are Stored (GnuPG vs rPGP)
description: Understand how GpgFrontend's GnuPG and rPGP engines store OpenPGP keys differently, and what it means for backups, security, and interoperability.
sidebar:
  label: Key Storage
  order: 3
---

GpgFrontend supports two OpenPGP engines, and they store your keys in
fundamentally different ways. Understanding this difference matters for backups,
security expectations, and interoperability with other tools. This page explains
where each engine keeps key material and what protects it.

For managing multiple databases and choosing an engine per database, see
[Multi-Key Database](/advanced/key-database).

## Quick Comparison

| Aspect              | GnuPG engine                                  | rPGP engine                                        |
| ------------------- | --------------------------------------------- | -------------------------------------------------- |
| Who stores the keys | GnuPG, through its own home directory         | GpgFrontend, in its own key database               |
| Storage format      | GnuPG keyring (`pubring.kbx`) and `private-keys-v1.d/` | A SQLite database, `gf_keydb.sqlite`      |
| Secret key handling | Managed by `gpg-agent`                        | Stored directly by GpgFrontend                     |
| Protection at rest  | GnuPG's own mechanisms plus passphrase        | OS file permissions plus the key's own passphrase  |
| External tools      | The `gpg` command line and other GnuPG tools can use the same home directory | rPGP keys are managed only by GpgFrontend |

## GnuPG Engine

When a key database uses the GnuPG engine, GpgFrontend does not store the keys
itself. It talks to GnuPG through GPGME, and GnuPG owns the key material:

- **Public keys** live in the GnuPG keyring (the keybox, `pubring.kbx`) inside
  the GnuPG home directory for that database.
- **Secret keys** are held by `gpg-agent` under `private-keys-v1.d/`, and all
  private-key operations (signing, decryption) go through the agent.
- **Passphrase caching** is handled by `gpg-agent`.

Because the keys live in a standard GnuPG home directory, the same directory can
be used by the `gpg` command line and other GnuPG-based tools. For a GnuPG
database, GpgFrontend's own `gf_keydb.sqlite` file holds only GpgFrontend
metadata (such as key groups) and may be empty of key material.

To back up a GnuPG database, back up its GnuPG home directory and your
revocation certificates.

## rPGP Engine

When a key database uses the rPGP engine, GpgFrontend manages the keys directly,
without GnuPG or `gpg-agent`. Keys are stored in a SQLite database named
`gf_keydb.sqlite` in the database directory, alongside its `-wal` and `-shm`
sidecar files (the database uses WAL journaling).

The database holds both metadata (fingerprints, key IDs, algorithms,
capabilities, user IDs, subkeys) and the actual OpenPGP public and secret key
blocks.

### How rPGP Key Material Is Protected

The SQLite database itself is **not encrypted**. The secret key blocks are
stored as OpenPGP key packets, which are protected only by the passphrase you
set on the key (if any). To keep other local users from reading the key
material, GpgFrontend restricts the storage to the current user through
operating-system file permissions:

- The database directory is set to owner-only access (`0700`).
- The `gf_keydb.sqlite` file and its `-wal` / `-shm` sidecars are set to
  owner-only read and write (`0600`).

:::caution[Set a passphrase for rPGP secret keys]

Because the rPGP database does not add its own encryption layer, a secret key
generated **without** a passphrase is protected at rest only by file
permissions. For sensitive keys, set a passphrase so the secret key packet is
encrypted inside the database.

:::

To back up an rPGP database, back up the database directory that contains
`gf_keydb.sqlite`, because it contains the rPGP-managed key material.

## Interoperability

The storage difference is closely tied to key compatibility:

- GnuPG keys can be imported into and used by the rPGP engine.
- rPGP-generated 25519 and post-quantum keys are not compatible with GnuPG. See
  the compatibility notes in [Generate Key Pair](/guides/generate-key) and
  [Comparison of Algorithms](/extra/algorithms-comparison).

For this reason, keep keys that need maximum interoperability in a GnuPG-backed
database, and use rPGP-backed databases for testing newer OpenPGP features.

## Related Topics

- [Multi-Key Database](/advanced/key-database)
- [Application Data Storage](/advanced/app-data-storage)
- [Memory Security](/advanced/memory-security)
