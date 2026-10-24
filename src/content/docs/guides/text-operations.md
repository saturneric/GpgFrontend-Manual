---
title: Text Operations
description: "Encrypt, decrypt, sign, and verify text in GpgFrontend using OpenPGP public key cryptography with simple, intuitive workflows."
sidebar:
  order: 4
---

GpgFrontend lets you do four things with text: **encrypt** it (hide it),
**decrypt** it (read it), **sign** it (prove it came from you), and **verify** a
signature (check it really did). This page walks through each one.

![][img-1]

## Before You Start

These tasks use a pair of keys:

- **Public key**: used to **encrypt** a message for someone, or to **verify** their
  signature.
- **Private key**: used to **decrypt** a message sent to you, or to **sign** your
  own.

So before you begin, [make your own key pair](/guides/generate-key/) and swap
public keys with the people you write to. You encrypt with their public key; they
decrypt with their private key.

## Find the Buttons

Every task on this page works on the text in the current **Text Editor** tab.
You can start each task in three ways. They all do the same thing:

| Task               | Toolbar button                   | **Operations** menu  | Shortcut     |
| ------------------ | -------------------------------- | -------------------- | ------------ |
| Encrypt            | **Encrypt**                      | **Encrypt**          | Ctrl+E       |
| Encrypt and sign   | in the **Encrypt** button's list | **Encrypt & Sign**   | Ctrl+Shift+E |
| Decrypt            | **Decrypt**                      | **Decrypt**          | Ctrl+D       |
| Decrypt and verify | in the **Decrypt** button's list | **Decrypt & Verify** | Ctrl+Shift+D |
| Sign               | **Sign**                         | **Sign**             | Ctrl+Shift+I |
| Verify             | **Verify**                       | **Verify**           | Ctrl+Shift+V |

On macOS, press Cmd instead of Ctrl.

To see a button's list, right-click the button, or press and hold it. See
[Buttons With More Than One Action](/guides/understand-interface/#buttons-with-more-than-one-action).

To pick a key, tick the box in front of it in the **Key ToolBox**, the key list
on the right side of the main window.

## Encrypt Text

Encrypting hides a message so that only the person you write to can read it.
You need **their public key** in your key list.

1. **Open a text tab.** Click **File**, then **Workspace**, then
   **New Text Editor** (or press Ctrl+N). A new, empty tab opens.
2. **Write your message.** Type it, or paste it in.
3. **Pick the recipient.** In the **Key ToolBox**, tick the box in front of the
   person's public key. To send to several people, tick each of their keys.
4. **Click Encrypt.** Or press Ctrl+E.
5. **Answer any questions.** GpgFrontend may stop to check your recipients, for
   example when a key has expired. See [Checks Before Encrypting](#checks-before-encrypting).
6. **See the result.** The text in the tab is replaced by a block that starts
   with `-----BEGIN PGP MESSAGE-----`. The **Status Panel** at the bottom shows
   whether it worked.
7. **Send it.** Copy the whole block, from the `BEGIN` line to the `END` line,
   and paste it into your email or chat. Or save it with **File**, **Save**.

![][img-2]

:::caution

If you tick **no key at all** and click **Encrypt**, GpgFrontend does not stop.
It asks you for a password instead and encrypts with that. This is called
[symmetric encryption](/guides/symmetric-encrypt-decrypt/). If you meant to
encrypt for a person, click **Cancel** and tick their key first.

:::

:::tip

Tick your **own** key too if you want to be able to read the message later.
Without it, only the recipient can open it, not you.

:::

The encrypted message does not show who sent it. If you also want to prove that
it came from you, use [Encrypt and Sign](#encrypt-and-sign-at-once).

### If You Are Asked to Pick a Subkey

Some people have more than one encryption subkey on their key. When that
happens, GpgFrontend opens **Select Encryption Key(s)** and asks which one to
use. Expand a key to see its subkeys.

If you have no reason to prefer one, just confirm the selection GpgFrontend
offers. This dialog does not appear when there is only one sensible choice.

### Sending to a Chat App

A normal encrypted message is a large block of text, and chat apps often break
it. GpgFrontend has a second kind of encryption made for exactly that case. You
find it in the **Operations** menu. See
[Instant Messaging](/guides/instant-messaging/).

### Checks Before Encrypting

GpgFrontend checks your recipients before it encrypts. For example, it tells
you when a key has expired, and it can ask you to confirm when you encrypt to
more than one person. See [Encryption Safety](/guides/encryption-safety/).

## Decrypt Text

Decrypting turns an encrypted message sent to you back into readable text. You
need **your private key**, the one that matches the public key the sender used.

1. **Open a text tab.** Click **File**, then **Workspace**, then
   **New Text Editor** (or press Ctrl+N).
2. **Paste the message.** Paste the whole block, including the
   `-----BEGIN PGP MESSAGE-----` and `-----END PGP MESSAGE-----` lines.
3. **Click Decrypt.** Or press Ctrl+D. You do **not** need to tick any key.
   GpgFrontend finds the right private key by itself.
4. **Enter your passphrase.** A window asks for the passphrase that protects
   your private key. Type it and confirm.
5. **Read the message.** The block in the tab is replaced by the readable text.
   The **Status Panel** shows whether it worked.

![][img-3]

If it fails, the **Status Panel** turns red and says why. The most common
reasons:

- **You don't have the right private key.** The message was encrypted for
  someone else, or for a key you no longer have.
- **Part of the block is missing.** Copy the message again, from the very first
  `-----BEGIN` line to the very last `-----END` line.
- **The message was changed on the way.** GpgFrontend will not show text it
  cannot trust. See [Encryption Safety](/guides/encryption-safety/).

:::note

If the message was also signed, the plain **Decrypt** does not check the
signature. Use [Decrypt and Verify](#decrypt-and-verify-at-once) instead.

:::

## Sign Text

Signing proves that a message came from you and that nobody changed it. It does
**not** hide the message: anyone can still read it. You need **your private
key**.

1. **Open a text tab** and write your message.
2. **Pick your key.** In the **Key ToolBox**, tick the box in front of **your
   own** key. Pick a key that can sign: its **Usage** column shows an `S`.
3. **Click Sign.** Or press Ctrl+Shift+I.
4. **Choose a key, if asked.** If you ticked no key that can sign, or your key
   has more than one signing subkey, a window called **Select Signing Key(s)**
   opens. Tick the key or subkey to use and click **Confirm**.
5. **Enter your passphrase.** Type the passphrase of your private key.
6. **See the result.** Your text now sits between two lines:
   `-----BEGIN PGP SIGNED MESSAGE-----` at the top and a
   `-----BEGIN PGP SIGNATURE-----` block at the bottom. Your message stays
   readable in the middle.
7. **Send it.** Copy everything, from the first `-----BEGIN` line to the last
   `-----END` line, and send it.

![][img-4]

:::caution

After signing, do not change anything in the text, not even a space or an empty
line. Any change, however small, makes the signature fail.

:::

## Verify a Signature

Verifying checks that a signed message really came from the person it claims,
and that nobody changed it. You need **the sender's public key** in your key
list.

1. **Open a text tab.** Click **File**, then **Workspace**, then
   **New Text Editor** (or press Ctrl+N).
2. **Paste the signed message.** Paste all of it, from
   `-----BEGIN PGP SIGNED MESSAGE-----` down to `-----END PGP SIGNATURE-----`.
3. **Click Verify.** Or press Ctrl+Shift+V. You do not need to tick any key.
4. **Read the result in the Status Panel.**
   - **Green**: the signature is good. The message is unchanged and was signed
     by the key shown.
   - **Orange**: the signature is good, but there is something to check, for
     example a key you have not marked as trusted.
   - **Red**: the signature is bad. The message was changed, or it was not
     signed by that key. Do not trust it.

The text in the tab is not changed when you verify.

![][img-5]

### If the Sender's Key Is Missing

If you don't have the sender's public key, a window called **Missing Keys**
opens. It lists the fingerprints of the missing keys and asks whether to fetch
them from the key server.

- Click **Yes** to search the key server for the key.
- Click **No** to stop. You can
  [import the key](/guides/import-export-key-pair/) yourself and verify again.

:::tip

Check the name and fingerprint shown in the result against what you know about
the sender. A good signature only proves the message matches **that** key. It
does not prove the key belongs to the person you think.

:::

## Encrypt and Sign at Once

This makes a message that is both **secret** and **proven to be from you**. It is
the best choice for private messages.

1. **Open a text tab** and write your message.
2. **Pick the recipient.** Tick the box in front of the recipient's public key
   in the **Key ToolBox**.
3. **Start it.** Open the **Operations** menu and choose **Encrypt & Sign**, or
   press Ctrl+Shift+E. On the toolbar, it is in the **Encrypt** button's list.
4. **Choose your signing key.** The **Select Signing Key(s)** window always
   opens here. Tick **your own** key and click **Confirm**.
5. **Enter your passphrase.**
6. **See the result.** The text becomes a `-----BEGIN PGP MESSAGE-----` block,
   just like normal encryption. The signature is hidden inside it.

Unlike plain **Encrypt**, this one needs at least one ticked recipient key.

## Decrypt and Verify at Once

Use this when you receive a message that was encrypted **and** signed.

1. **Paste the message** into a text tab.
2. **Start it.** Open the **Operations** menu and choose **Decrypt & Verify**,
   or press Ctrl+Shift+D. On the toolbar, it is in the **Decrypt** button's
   list.
3. **Enter your passphrase.**
4. **Read the result.** The readable text appears in the tab. The **Status
   Panel** shows both results: whether decryption worked, and whether the
   signature is good.

If the sender's public key is missing, the same **Missing Keys** window opens as
when you [verify](#if-the-senders-key-is-missing).

## Your Text Is Kept Exactly as Typed

GpgFrontend works on the exact text in the editor tab. It does not change line
endings, and it does not swap special spaces for normal ones. This matters for
signatures: a signature only checks out if the text is exactly the same,
character for character.

Pressing **Shift+Enter** now starts a normal new line, the same as **Enter**.

:::note[Changed in v2.2.3]

Earlier versions sometimes changed line endings and special spaces before an
operation. Because v2.2.3 keeps the text exactly, a signature may now check
differently than it did in v2.2.2. If a signature made with an older version
fails to verify, ask the sender to sign the text again.

:::

## Undo After an Operation

By default, you cannot undo an encrypt or decrypt with Ctrl+Z. This keeps your
plain text from staying in memory. You can turn undo on in **Settings**. See
[Memory Security](/advanced/memory-security/#undo-after-an-operation).

## Safety Tips

- **Verify before you trust.** Check a signature before you act on a message.
- **Share only your public key.** Never give out your private key.
- **Encrypt and sign together** for messages that should be both private and
  proven.
- **Sign only** (no encryption) for public documents that need to be trusted but
  not hidden.

[img-1]: https://image.cdn.bktus.com/i/2026/10/25/c907844a077196ac1863fd0555febb222e7af009-0.webp
[img-2]: https://image.cdn.bktus.com/i/2026/10/25/b35cf459fb95b156a99489dc098b694925f2f07b-0.webp
[img-3]: https://image.cdn.bktus.com/i/2026/10/25/1700acb9bf24d4221a6803d5ced85e276aa2c728-0.webp
[img-4]: https://image.cdn.bktus.com/i/2026/10/25/1eaf74f27c05412471bb5213357296ed8acd4928-0.webp
[img-5]: https://image.cdn.bktus.com/i/2026/10/25/e2bd1c117432909b8d5d55545e55d068650eccc3-0.webp
