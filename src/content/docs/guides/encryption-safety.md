---
title: "Encryption Safety"
description: "The checks GpgFrontend makes so you do not encrypt to the wrong person, trust a damaged message, or lose a file: what each warning means and what to do."
sidebar:
  order: 6
  label: Encryption Safety
---

GpgFrontend has several checks that stop common mistakes. Some are always on.
Some you can turn on in **Settings**. This page explains each one: when it
appears, what it means, and what to do.

You do not need to set anything up. The defaults are safe. Read on if a
message surprised you, or if you want extra checks.

:::note[New in v2.2.3]

Most of the checks on this page were added or changed in GpgFrontend v2.2.3.

:::

## Turn On Extra Checks

Two extra checks are off by default. Turn them on if you often write to
different people and want to be sure each message goes to the right one.

1. Open **Settings** and go to **General**.
2. Find the **Operation** box.
3. Tick the checks you want (see below).
4. Click **OK**. On macOS, close the window instead.

### Allow only one checked key in the key list

With **Allow only one checked key in the key list.** ticked, checking a key in
the key list unchecks all the others. So a recipient from your last message
is not added to the next one by mistake.

While this is on, the **Check All** button is hidden.

### Ask before encrypting to more than one recipient

With **Ask before encrypting to more than one recipient.** ticked, GpgFrontend
stops when two or more keys are checked and shows **Confirm Recipients**.

- It asks **Encrypt to 2 recipients?** (or however many there are), and lists
  each name, email and key ID. A key group shows how many keys it holds.
- It reminds you that each recipient will be able to see the key IDs of all
  the others.
- Click **Encrypt** to go ahead, or **Cancel** to stop and change your choice.

## When Encryption Is Not Possible

Some keys cannot be used to encrypt. When one of the checked keys is like
that, the **Encrypt** and **Encrypt & Sign** buttons are greyed out.

To find out why, point at the greyed-out button. Its tooltip names the key
and the reason. If you try anyway, a **Cannot Encrypt** message shows the
same reason.

The reason is one of these:

- **The key of ... has been revoked.** The owner has cancelled this key. Ask
  them for their new one.
- **The key of ... expired on ....** The key is past its end date. Ask the
  owner to extend it, then
  [refresh it](/guides/key-server-operations/) or import it again.
- **The key of ... has no subkey that can encrypt.** This key can only sign.
  Ask the owner for a key that can encrypt.
- **The encryption subkey of ... expired on ....** The part of the key used for
  encrypting has expired, even though the main key has not. Ask the owner to
  extend it.
- **The encryption subkey of ... has been revoked or disabled.** The part of
  the key used for encrypting has been cancelled.

Dates are shown as year, month, day, for example `2026-03-08`.

## Mixing Post-Quantum and Classical Recipients

Some new keys use **post-quantum** encryption. This is built to stay safe even
against future quantum computers. Older keys use **classical** encryption. See
[Post-Quantum Cryptography](/guides/post-quantum/).

If you encrypt one message to both kinds of key at once, GpgFrontend shows
**Mixed Recipient Types**. It warns that some recipients use post-quantum
encryption and others do not.

Why it matters: one message is locked so that every recipient can open it.
Anyone who can break the classical recipients' encryption can read the whole
message. So the post-quantum protection does not hold for it.

- Click **Encrypt Anyway** to send it like this.
- Click **Cancel**, then encrypt the message twice: once for the post-quantum
  recipients, and once for the others.

## Weak Recipient Keys (rPGP Engine)

The rPGP engine follows the current OpenPGP rules. It will not encrypt to
keys that those rules call too weak:

- **DSA** keys.
- **RSA** keys shorter than **2048 bits**.

If only some of the checked keys are like that, GpgFrontend skips them and
encrypts to the rest. The result says **Encrypted with warnings. Some
recipients could not be added. Please review the invalid recipient list.**
The details list each skipped key under **Invalid Recipients**, with its
fingerprint and the reason.

The people whose keys were skipped **cannot** read the message. Ask them for a
newer, stronger key.

If none of the checked keys can be used, nothing is encrypted.

## Messages With No Tamper Check

Modern encrypted messages include a check that shows whether anyone changed
them on the way. Some very old messages do not have it.

GpgFrontend will not show you the text of such a message. The result says:
**The output was withheld: this message has no integrity protection, so
tampering with it cannot be detected. It may be a legacy message.**

Ask the sender to encrypt the message again with up-to-date software.

:::note[Changed in v2.2.3]

In v2.2.2, the text of such a message was still shown. It is now held back,
because there is no way to know if someone changed it.

:::

## Signed by a Key You Do Not Have

When you decrypt or verify a signed message, you need the signer's public key
to check the signature. If you do not have it, GpgFrontend now treats this as
a **warning**, not a failure:

- You still get the decrypted text or file.
- The result says **Verification incomplete. The signing key is not in your
  keyring. Please import the signer's public key.**

Until you import that key and check again, you do not know who signed the
message. See [Import & Export Key Pair](/guides/import-export-key-pair/).

:::note[Changed in v2.2.3]

A missing signer key used to count as a failure, and the output was not kept.

:::

## Files Are Only Written When the Operation Works

When you encrypt, decrypt or sign a file, GpgFrontend writes the result to a
temporary file first. It only puts the result in place once the whole
operation has worked.

- If the operation fails, you get **no** output file. You never get a
  half-written or damaged one.
- If a file with the same name already exists, GpgFrontend asks first. It
  explains that the old file will only be replaced after the operation
  succeeds.
- Your input file is never changed.

See [File Operations](/guides/file-operations/).

## Results Go Back to Their Own Tab

When an operation on text finishes, the result goes back into the editor tab
you started it from. This is true even if you switched to another tab while
it was running.

If you closed that tab in the meantime, the result is thrown away. It is never
written into a different tab.

## Undo After an Operation

By default, you cannot undo an encrypt, decrypt or other operation in the text
editor. This is on purpose: to allow undo, the program has to keep the old
text in memory, and after encrypting, that old text is your plain text.

To turn undo on, tick **Allow undoing encrypt, decrypt and other operations in
the text editor.** in **Settings**, **General**, **Operation**. See
[Memory Security](/advanced/memory-security/#undo-after-an-operation).
