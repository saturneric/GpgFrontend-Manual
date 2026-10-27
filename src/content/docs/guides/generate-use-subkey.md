---
title: Generate and Use Subkey(s)
description: "Add and manage OpenPGP subkeys in GpgFrontend for signing, encryption, or authentication while keeping your primary key secure."
sidebar:
  order: 11
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
3. Click **New Subkey**. The **Add Subkey** window opens.

![][img-1]

### Step 1: Choose What the Subkey Is For

Under **What is the subkey for?**, click one choice:

- **Encryption** (picked for you): for messages and files others send to you.
- **Signing**: for everyday signing, so the primary key can be kept somewhere
  safer.
- **Authentication**: for logging in, for example over SSH. Skip it unless you
  need it.

Each choice shows the algorithm it will use, matched to your primary key. A
choice that does not fit your key says **Not available for this key.**

Then pick when the subkey **Expires**. The default is **2 years**. You can
pick another period, **Never**, or **Custom date**.

To choose everything yourself, turn on the **Expert Mode** switch. You then
pick the **Algorithm**, **Key length** and **Usage** (**Encrypt**, **Sign**,
**Authenticate**). For hybrid algorithms, such as the post-quantum ML-KEM
ones, **Paired with** and **Its key length** also appear. You can also tick
**Without a passphrase**, if the engine allows it.

Post-quantum subkeys are only offered for keys in the v6 format. For a v4 key,
the window tells you so.

:::note[Changed in v2.2.4]

The window used to be called **Generate New Subkey** and showed every option
at once (**Usage**, **Algorithm**, **Key Length**, **Expire Date**, **Non
Expired**). Now you pick what the subkey is for, and the detailed choices are
under **Expert Mode**.

:::

:::tip[Plan ahead]

When you set up a key, it helps to make a few subkeys at once, one for each job
(signing, encryption, login). That way you have what you need later, even if you
keep your primary key offline.

:::

### Step 2: Generate

- Click **Generate**.
- When asked, enter your key's **passphrase** to confirm. With GnuPG, the new
  subkey is protected by the same passphrase as the key pair.
- A **Subkey Added** message confirms it. The new subkey appears under the
  **Keychain** tab.

![][img-2]

That's all you need to add a subkey.

:::tip[Change one subkey's passphrase on its own]

Since v2.2.2 you can give a single subkey a new passphrase without touching the
others. Open the key's details, go to the **Keychain** tab, right-click the
subkey, and choose **Change Passphrase**.

GpgFrontend asks for the current passphrase first. Only after you enter it
correctly does it ask you to pick a new one.

:::

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

![][img-3]

### Step 2: Import the Subkey into Another Database

1. **Pick the key database**: choose the right key database in the **Key ToolBox**.

![Switch Key Database][img-4]

2. **Import the file**: click **Import** in the top toolbar and choose
   **File**. Browse to the exported subkey file.

   ![Import the Subkey][img-5]

3. **Select the file**: pick the subkey file and click **Open** to import it into
   the chosen key database.
4. **Check it**: find the subkey in the **Key ToolBox**, then click it to open its
   **Key Details** (Key ID, Algorithm, Key Size, Usage).

   ![Verify Imported Subkey][img-6]

### Step 3: Use a Key Without Its Primary Key

Once the subkey is in its own database, you can move your primary key somewhere
safe and delete it from GpgFrontend. The key still works for everyday tasks, with
a few limits.

In the **Key ToolBox**, a `#` next to the **Type** (for example, **pub/sec#**)
means the primary key isn't in this key database. This is expected when you have
removed the primary key on purpose and kept the subkeys for daily use.

![Meaning of '#' Symbol][img-7]

To confirm, open the subkey's **Key Details**. The **Primary Key Existence**
section should say **Not Exists**.

![Primary Key Not Exists][img-8]

**What still works** with only subkeys present:

- You can still **encrypt and decrypt** (for example, emails or files).
- You can **sign**, but only if you kept a signing subkey. So make a signing
  subkey when you first create the key, if you'll need one later.

![Use Subkey to Encrypt][img-9]

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
| DSA                             | Sign / Auth            | GnuPG only       |
| ElGamal (`ELG-E`)               | Encrypt                | GnuPG            |
| Ed25519                         | Sign / Auth            | GnuPG, rPGP      |
| Ed448                           | Sign / Auth            | rPGP only        |
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

[img-1]: https://image.cdn.bktus.com/i/2026/10/25/3d80f37afdcba716f159e71845e4061579fd1f42-0.webp
[img-2]: https://image.cdn.bktus.com/i/2026/10/25/78a292d6564af52d3d3eea1cb075ec1049cd3594-0.webp
[img-3]: https://image.cdn.bktus.com/i/2026/10/25/b81c094eeb21ab2960363edfc0e3d0a0d59cade2-0.webp
[img-4]: https://image.cdn.bktus.com/i/2026/10/25/1fa8f6a2ad0da9c2a71ca2863f240989e3ef73d7-0.webp
[img-5]: https://image.cdn.bktus.com/i/2026/10/25/b6f773ca4059abe8a98eff10277dd7b3efd93490-0.webp
[img-6]: https://image.cdn.bktus.com/i/2026/10/25/f22c7532447bd6871215688ad6fa0cbda92434cb-0.webp
[img-7]: https://image.cdn.bktus.com/i/2026/10/25/b82131ba65e55baf29d58c15870d2763a34a165d-0.webp
[img-8]: https://image.cdn.bktus.com/i/2026/10/25/33d147efb4b19d95e25b9affae748fbd9638a20b-0.webp
[img-9]: https://image.cdn.bktus.com/i/2026/10/25/95c95c3b8efcf06171c881bcea380b96aa977b44-0.webp
