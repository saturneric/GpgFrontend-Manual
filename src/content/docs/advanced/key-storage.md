---
title: How Keys Are Stored (GnuPG vs rPGP)
description: "Understand how GpgFrontend's GnuPG and rPGP engines store OpenPGP keys differently, and what it means for backups, security, and interoperability."
sidebar:
  label: Key Storage
  order: 5
---

GpgFrontend can use two different OpenPGP engines: **GnuPG** and **rPGP**. They
store your keys in very different places, and that difference matters for three
practical questions:

- **What do I need to back up?**
- **What protects my secret keys on disk?**
- **Can other tools (like the `gpg` command line) see my keys?**

This page answers those questions for each engine. To learn how to set up
databases and pick an engine for each one, see
[Multi-Key Database](/advanced/key-database/).

:::note[Keys can also live inside a profile]

Since v2.2.2, a [profile](/advanced/profiles/) can hold its own keys instead of
sharing the ones on your computer. When it does, the key database sits inside
the profile folder and travels with it.

Everything on this page still applies. Only the location changes.

:::

## Where the Key Database Folders Are

Each key database is one folder. Where that folder is depends on the kind of
key database:

- **The built-in key database**: normally your GnuPG home directory. When your
  [profile](/advanced/profiles/) keeps its own keys, it is a folder inside the
  profile instead. To see the exact path, open the **Key Databases** settings
  page and look at **Location:** in the **Built-in Key Database** box.
- **A key database on the In Profile tab**: a folder inside your profile,
  named after the database. The settings page shows it as
  `@profile/dbs/<Name>`, where `@profile` means "your profile folder". Renaming
  the database renames this folder.
- **A key database on the Local Only tab**: the folder you chose yourself.

Whichever engine a key database uses, its keys are in that folder. With the
rPGP engine, look for the `gf_keydb.sqlite` file there.

:::note[Changed in v2.2.3]

The **Automatic** and **Manual** choices are gone. What used to be
**Automatic** is now the **In Profile** tab, and the folder is still
`@profile/dbs/<Name>`. What used to be **Manual** is now the **Local Only**
tab. See [Multi-Key Database](/advanced/key-database/).

:::

## Quick Comparison

| Aspect              | GnuPG engine                                                   | rPGP engine                                    |
| ------------------- | -------------------------------------------------------------- | ---------------------------------------------- |
| Who stores the keys | GnuPG, in its own home directory                               | GpgFrontend, in its own database file          |
| Storage format      | GnuPG keyring (`pubring.kbx`) and `private-keys-v1.d/`         | A SQLite database, `gf_keydb.sqlite`           |
| Secret key handling | Managed by `gpg-agent`                                         | Stored directly by GpgFrontend                 |
| Protection at rest  | GnuPG's own mechanisms plus passphrase                         | File permissions plus the key's own passphrase |
| Other tools         | The `gpg` command line and other GnuPG tools see the same keys | Only GpgFrontend can use these keys            |
| What to back up     | The GnuPG home directory                                       | The folder that contains `gf_keydb.sqlite`     |

## GnuPG Engine

With the GnuPG engine, GpgFrontend does not store your keys at all. It asks
GnuPG to do the work (through the GPGME library), and GnuPG owns the keys.

**Where the keys live:**

- **Public keys** are in the GnuPG keyring file (`pubring.kbx`) inside the
  GnuPG home directory of that database.
- **Secret keys** are held by `gpg-agent` under `private-keys-v1.d/`. Every
  operation that needs a private key (signing, decryption) goes through the
  agent, and the agent also handles passphrase caching.

**What this means for you:**

- Other GnuPG tools, including the `gpg` command line, can use the exact same
  keys, because they all read the same home directory.
- GpgFrontend's own `gf_keydb.sqlite` file in a GnuPG database holds only
  GpgFrontend metadata (such as key groups). It contains no key material and
  may be empty.

**What to back up:** The GnuPG home directory of the database, plus your
revocation certificates.

## rPGP Engine

With the rPGP engine, GpgFrontend stores and manages the keys itself. GnuPG
and `gpg-agent` are not involved at all.

**Where the keys live:**

- Everything is in one SQLite database file, `gf_keydb.sqlite`, inside the
  database folder. Next to it you may see `-wal` and `-shm` helper files;
  they belong to the database too.
- The file holds both the key details (fingerprints, key IDs, algorithms,
  user IDs, subkeys) and the actual public and secret key blocks.

**What protects the secret keys:**

The database file itself is **not encrypted**. Two things protect your keys:

1. **File permissions**: GpgFrontend limits access to your user account only.
   The database folder is set to owner-only access (`0700`), and the database
   files to owner-only read and write (`0600`). This keeps other users on the
   same computer out.
2. **The key's own passphrase**: A secret key with a passphrase is stored
   encrypted inside the database, just like in a normal OpenPGP key file.

:::caution[Always set a passphrase for rPGP secret keys]

A secret key created **without** a passphrase sits in the database with no
encryption of its own. File permissions are then its only protection. For any
key you care about, set a passphrase, so the secret key stays encrypted even
if someone gets a copy of the database file.

:::

**What to back up:** The whole database folder that contains
`gf_keydb.sqlite`. Remember that this backup contains your secret keys, so
store it somewhere safe and encrypted.

## Working with Other Tools

The storage difference goes hand in hand with key compatibility:

- Keys made with GnuPG can be imported into an rPGP database and used there.
- The other direction is limited: 25519 and post-quantum keys generated by
  rPGP do **not** work with GnuPG. See the compatibility notes in
  [Generate Key Pair](/guides/generate-key) and
  [Comparison of Algorithms](/extra/algorithms-comparison).

The simple rule: keep the keys you use with other people and other tools in a
**GnuPG** database, and use **rPGP** databases for testing newer OpenPGP
features.

## Related Topics

- [Multi-Key Database](/advanced/key-database)
- [Application Data Storage](/advanced/app-data-storage)
- [Memory Security](/advanced/memory-security)
