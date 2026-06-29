---
title: Generate and Use Subkey(s)
description: "Add and manage OpenPGP subkeys in GpgFrontend for signing, encryption, or authentication while keeping your primary key secure."
sidebar:
  order: 6
---

A **subkey** is an extra key attached to your main key (the **primary key**).
Subkeys do the everyday jobs, like encryption, signing, and login. The primary
key proves who you are and manages your keys, so you can keep it tucked away
somewhere safe.

Making a subkey takes only a few clicks. This guide shows that first. The "why"
and the more advanced setups come later, so you can skip them until you need them.

## Make a Subkey

1. Double-click the key pair in the **Key ToolBox** list.
2. Open the **Keychain** tab.
3. Click **Generate A New Subkey**.

![](https://image.cdn.bktus.com/i/2026/06/30/3d94fa5ca42185abee5dfdfc1530961902fbe680.webp)

### Step 1: Choose What the Subkey Is For

The one choice that really matters is what the subkey will do:

- **Key Usage**: pick `Encrypt` (to lock messages and files sent to you) or
  `Sign` (to prove things came from you). Most people want one of these. There is
  also `Authenticate`, used for logins like SSH, but you can skip it unless you
  need it.

Everything else has a safe default. You can leave these alone, or change them if
you know you need to:

- **Algorithm**: the type of key. The default is fine for most people. Choices
  include RSA, DSA, and ECC types such as ED25519, ED448, CV25519, SECP256K1,
  Brainpool, and NIST curves.
- **Key Length**: bigger is stronger but slower. For curve types this is set by the
  curve (for example, ED25519 = 256 bits). For RSA/DSA you can pick 2048, 3072, or
  4096 bits.
- **Expiration Date**: how long the subkey lasts. Pick a preset (like 1 or 2
  years), an exact date, or **Non Expired** to never expire. (Only for GnuPG engine)
- **Second Algorithm**: shown only for **hybrid** algorithms (such as the
  post-quantum ML-KEM/Kyber options). It lets you pick the classical part that is
  paired with the hybrid one (you also get a **Second Key Length** field).
- **No Passphrase**: make the subkey without its own passphrase, if the engine
  allows it.

:::tip[Plan ahead]

When you set up a key, it helps to make a few subkeys at once, one for each job
(signing, encryption, login). That way you have what you need later, even if you
keep your primary key offline.

:::

### Step 2: Generate

- Check your choices in the summary (if shown).
- Click **Generate**.
- When asked, enter your key's **passphrase** to confirm.
- The new subkey appears under the **Keychain** tab.

![](https://image.cdn.bktus.com/i/2026/06/30/66dbd8460933ec7cd6bfece33daa84e2d622d90f.webp)

That's all you need to add a subkey.

## Why Subkeys Help

A key pair is one **primary key** plus one or more **subkeys**. Splitting the work
between them keeps you safer:

- **The primary key is your identity.** It signs (certifies) your subkeys and
  other people's keys. You rarely need it day to day.
- **Subkeys do the daily work.** Each one handles a single job, like signing or
  encryption.

Because the jobs are split, you get:

- **Better security**: use subkeys day to day. If one is exposed, revoke just that
  subkey and keep the rest.
- **Flexibility**: give each job its own subkey, and renew or revoke them on their
  own.
- **Easy rotation**: swap signing or encryption subkeys when you like, without
  rebuilding the trust tied to your primary key.

Advanced users go one step further and keep the primary key offline entirely. The
rest of this page shows how, along with some reference notes. You can stop here and
come back when you need it.

---

## Keep Your Primary Key Offline (Optional)

Everything below is optional. It covers a more secure setup: moving your subkeys
into a separate key database and keeping your primary key safe and offline.

Why bother? If your subkeys and primary key always travel together, every
signature or decryption puts the primary key at risk. Keeping the primary key
offline (or in a hardware security module) means a stolen laptop only exposes the
subkeys, which you can revoke and replace. Losing the primary key, though, puts
your whole identity at risk, so **back it up safely first**.

The setup has three steps:

1. Export a subkey to its own file.
2. Import that file into another key database.
3. Remove the primary key, and use the subkeys on their own.

:::note[Needs the GnuPG engine]

Exporting a single subkey, and removing the primary key to leave only subkeys,
works with the **GnuPG engine** only. With the rPGP engine the **Export Subkey**
button is hidden and shows the tooltip "Exporting subkeys is not supported by the
current OpenPGP backend." Use a GnuPG-backed key database for this.

:::

### Step 1: Export a Subkey

1. **Open Key Details**: in the key database section, select the key to open the
   **Key Details** view.
2. **Open the Keychain tab**: here you see the primary key (first row) and all its
   subkeys.
3. **Select a subkey**: click the subkey you want. Its details (Key ID, Algorithm,
   Key Size, Usage) appear in the lower half of the window.
4. **Export it**: click **Export Subkey** on the right. (If the selected row is the
   primary key, the button is labeled **Export Primary Key** instead.)
5. **Save the file**: choose a secure folder and save the subkey as its own file.

![](https://image.cdn.bktus.com/i/2025/06/24/b4f1dc5e6eb6f683300564a4ba998e48d22b75b4.webp)

### Step 2: Import the Subkey into Another Database

1. **Pick the key database**: choose the right key database in the **Key Toolbox**.

![Switch Key Database](https://image.cdn.bktus.com/i/2024/11/29/0e8ff19e-4189-65db-5732-1a2e79d9b8a6.webp)

2. **Import the file**: click **Import Key** in the top toolbar and choose
   **File**. Browse to the exported subkey file.

   ![Import the Subkey](https://image.cdn.bktus.com/i/2024/11/29/8f3456ba-6275-4ef9-8e41-49b9b6bc0dfa.webp)

3. **Select the file**: pick the subkey file and click **Open** to import it into
   the chosen key database.
4. **Check it**: find the subkey in the **Key Toolbox**, then click it to open its
   **Key Details** (Key ID, Algorithm, Key Size, Usage).

   ![Verify Imported Subkey](https://image.cdn.bktus.com/i/2024/11/29/ac01142d-1ffa-ba32-daac-36ddf0729ff1.webp)

### Step 3: Use a Key Without Its Primary Key

Once the subkey is in its own database, you can move your primary key somewhere
safe and delete it from GpgFrontend. The key still works for everyday tasks, with
a few limits.

In the **Key Toolbox**, a `#` next to the **Type** (for example, **pub/sec#**)
means the primary key isn't in this key database. This is expected when you have
removed the primary key on purpose and kept the subkeys for daily use.

![Meaning of '#' Symbol](https://image.cdn.bktus.com/i/2024/11/29/78d9bc07-8b96-302b-25d1-cbb88815f16a.webp)

To confirm, open the subkey's **Key Details**. The **Primary Key Existence**
section should say **Not Exists**.

![Primary Key Not Exists](https://image.cdn.bktus.com/i/2024/11/29/05594a4b-cdad-7ad4-070b-58e24701cce3.webp)

**What still works** with only subkeys present:

- You can still **encrypt and decrypt** (for example, emails or files).
- You can **sign**, but only if you kept a signing subkey. So make a signing
  subkey when you first create the key, if you'll need one later.

![Use Subkey to Encrypt](https://image.cdn.bktus.com/i/2024/11/29/20047766-48ab-f4a3-175c-241c7d5c0dbf.webp)

**What you can't do** without the primary key:

- **Create new subkeys.**
- **Add a user ID (UID).**
- **Certify other keys** (sign them as trusted).
- **Make a revocation certificate** for the subkey or primary key.

This setup is great when exposing the primary key would be a risk. Keep the primary
key away and use only subkeys, and you balance everyday use with security.

## Add a Decryption Subkey (ADSK)

The **Keychain** tab also has an **Add ADSK(s)** button. An Additional Decryption
Subkey lets you attach another key's encryption subkey to your key, so messages
encrypted to you can also be read by the ADSK holder (for example, an
organization's escrow or backup key).

:::note[Requires the GnuPG engine]

ADSK needs the **GnuPG engine** (GnuPG 2.4.1 or later). The button shows only for
a primary key whose secret part is available, and it is hidden when the active key
database uses an engine or GnuPG version that doesn't support ADSK.

:::

## Common Questions About Subkeys

When you export only a subkey and import it elsewhere, you may notice that:

- The listing still shows the **primary key's ID** as the main identifier.
- The keyring still shows the original structure (the primary key and any other
  subkeys), even though only the exported subkey can actually be used.
- The usage flags (such as CESA: Certify, Encrypt, Sign, Authenticate) can change
  under certain conditions.

This is not a bug. It is just how OpenPGP and GnuPG represent keys.

### Why does the full key structure show up?

Even when you export only a subkey's secret part, you are really exporting a full
public key (a certificate) with only some private parts:

- The public key block still holds the primary key's info, all user IDs, and all
  subkey definitions.
- The primary key's secret part is missing, so you can't certify, revoke, or make
  more subkeys.
- The file has to include the primary key's public info, because the subkey's
  trust depends on the primary key having certified it.

:::tip[Analogy]

Exporting a subkey is like sending the contents of a letter but still including
the envelope, address, and signature. The recipient (the app) needs all of these
to know who sent it and to trust it.

:::

The primary key is the anchor for the whole structure. Subkeys are trusted because
the primary key certified them. Without the primary key's public info and
signatures, other OpenPGP tools wouldn't see the subkey as trustworthy.

### Why is the Key ID still the primary key's?

OpenPGP tools (GpgFrontend, Thunderbird, and others) identify the whole structure
by the primary key ID. This keeps things consistent across tools. You can't make a
"standalone" subkey with its own identity: a subkey only has value through its link
to the primary key.

### Can I use only a subkey for everything?

Yes, as long as you made the subkeys you need for signing, encryption, and login.
But some actions, like certifying other keys or adding user IDs, still need the
primary key.

## Subkey Algorithms

Subkeys offer more algorithm choices than primary keys, because they are made for
specific jobs. A primary key mainly proves identity and certifies, so it needs a
signing-capable algorithm. Subkeys can also use encryption-only algorithms (such
as ECDH types like Curve25519, X448, NIST, or Brainpool curves), which is why
those appear as subkey options.

The algorithms you see depend on the engine, its version, and the key format.
GnuPG is the recommended default for the widest compatibility, while rPGP adds
experimental support for OpenPGP v6 and some post-quantum algorithms. For more
detail, see [Comparison of Cryptographic Algorithms](/extra/algorithms-comparison).

| Algorithm                       | Purpose                | Engine           |
| ------------------------------- | ---------------------- | ---------------- |
| RSA                             | Encrypt / Sign / Auth  | GnuPG, rPGP      |
| DSA                             | Sign / Auth            | GnuPG, rPGP      |
| ElGamal (`ELG-E`)               | Encrypt                | GnuPG            |
| Ed25519                         | Sign / Auth            | GnuPG, rPGP      |
| Ed448                           | Sign / Auth            | GnuPG 2.3+, rPGP |
| Curve25519 / CV25519            | Encrypt                | GnuPG, rPGP      |
| X448                            | Encrypt                | GnuPG 2.3+, rPGP |
| NIST P-256 / P-384 / P-521      | Encrypt / Sign / Auth  | GnuPG, rPGP      |
| Brainpool P-256 / P-384 / P-512 | Encrypt / Sign / Auth  | GnuPG 2.3+       |
| secp256k1                       | Encrypt                | GnuPG 2.3+       |
| Kyber / ML-KEM hybrid variants  | Hybrid PQC Encrypt     | GnuPG 2.5+, rPGP |
| SLH-DSA-SHAKE variants          | PQC Sign / Auth        | rPGP only        |
| ML-DSA hybrid variants          | Hybrid PQC Sign / Auth | rPGP only        |

### Compatibility Notes

Keep these points in mind before you share a key made with the rPGP engine:

- **rPGP 25519 keys are rPGP-only.** rPGP can import 25519 keys made by GnuPG, but
  not the other way around. rPGP-made 25519 keys use the OpenPGP v6 format, which
  GnuPG can't import yet.
- **rPGP post-quantum keys are rPGP-only.** ML-DSA, SLH-DSA, and hybrid KEM keys
  made by rPGP use the OpenPGP v6 format. They are meant for testing and
  rPGP-based work, not for use with GnuPG.
- **Kyber / ML-KEM hybrid encryption isn't rPGP-only.** It may also work with
  GnuPG 2.5+, depending on the key database engine, its version, and the OpenPGP
  version. The current rPGP engine supports only some hybrid pairings, such as
  **Kyber-768 + Curve25519** and **Kyber-1024 + X448**. Other pairings may need
  GnuPG 2.5+ or may not be available.
