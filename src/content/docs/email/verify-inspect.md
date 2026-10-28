---
title: Verify and Inspect a Message
description: "Check a message you received in GpgFrontend: what each security badge means, whether you can open it, and what the Message Details window shows."
sidebar:
  label: Verify and Inspect
  order: 3
---

When you get a message, you want to know two things:

- **Can I trust it?** Did it really come from the sender, and was it changed on
  the way?
- **Can I read it?** If it is encrypted, do you have the key to open it?

This page shows where GpgFrontend answers these questions.

On a Mac, press Cmd where this page says Ctrl.

## Open the Message

Open the message in a mail tab. You can:

- open an `.eml` file, for example from the
  [File Panel](/guides/understand-interface/#file-panel), or
- fetch it from your mail server. See
  [Read Mail from Your Server](/email/reading-imap/).

## Read the Security Badge

At the right end of the action row there is a status button. We call it the
**badge**. It tells you, in a few words, what kind of message this is. Click it
to open the Security menu.

| Badge                                | What it means                                                                                                         |
| ------------------------------------ | --------------------------------------------------------------------------------------------------------------------- |
| **Not signed or encrypted**          | An ordinary message. Nothing proves who sent it. This is normal for most email.                                       |
| **Encrypted**                        | The message is hidden. It has no signature.                                                                           |
| **Signature not checked**            | The message has a signature, but it has not been checked yet. This says nothing good or bad so far.                   |
| **Encrypted, signature not checked** | The same, for an encrypted message.                                                                                   |
| **Signature verified**               | The signature was checked and it is good. The message was not changed since it was signed.                            |
| **Encrypted, signature verified**    | The same, for an encrypted message.                                                                                   |
| **Signed by a different address**    | The signature is good, but the key belongs to a different address than the one in **From**. Be careful.               |
| **Signature or key expired**         | The signature matches, but the signature or the key has expired.                                                      |
| **Signed by an unknown key**         | You do not have the sender's public key, so the signature cannot be checked. Import their key, then check again.      |
| **Signature could not be checked**   | The check ran, but it could not give an answer. Trying again may help.                                                |
| **Signing key not authorized**       | The signature is correct, but the key that made it is not allowed to sign. Do not trust it.                           |
| **Bad signature**                    | The signature does not match the message, or the key was revoked. The message may have been changed. Do not trust it. |
| **Malformed OpenPGP structure**      | The message says it uses OpenPGP, but it is not built the right way. It may not verify or decrypt.                    |

### Check the Signature

A signature is not checked by itself when you open a message. To check it:

1. Click the badge.
2. Click **Verify Signature**.

For an encrypted and signed message, click **Decrypt and Verify** instead.

The badge changes to show the result. The details also appear in the **Status
Panel**.

![A signed message after Verify Signature][img-1]

## Can I Open This Encrypted Message?

When a message is encrypted, the body is hidden. In its place you see a panel
that says **This message is encrypted** (or **This message is encrypted and
signed**). Below it, GpgFrontend tells you what it knows:

- **Addressed to ...**: who the message was sent to, from its headers.
- Whether you hold the right private key. For example: "You hold the private
  key for alice@example.com, so this message can be opened here."
- If you do not: "This message is encrypted to keys you do not hold the private
  half of, so it cannot be opened on this computer."
- Sometimes it cannot tell. Some senders hide who the message is for. Then the
  only way to know is to try.

To open it, click **Decrypt** on the panel.

## The Message Details Window

The **Message Details** window shows everything GpgFrontend knows about a
message. To open it, do one of these:

- Click **More** > **Details...**.
- Press Ctrl+Shift+D, or Alt+3.
- Click the badge, then a details item, such as **Signature Details...** or
  **Encryption Details...**.

The window has three tabs.

![The Message Details window on its Security tab][img-2]

### Security

The top line says what the message is, for example **This message carries a
signature.** Below it are up to four groups:

- **Signatures**: each signature, who made it, and whether it is good. You also
  see the key **Fingerprint**, when it was signed (**Signed at**), and the hash
  method used.
- **Recipients**: for an encrypted message, who it was encrypted to.
- **Keys for these addresses**: for each address in the message, which keys
  you have for it and whether they are usable. **no key found** means you have
  no key for that address.
- **What stands out**: things worth knowing about this message. See the list
  below.

Right-click a row for more actions:

- **Copy Value**, **Copy Fingerprint**, **Copy Address**.
- **Import the Key in This Message**: when you have no key for an address, but
  the message carries one.
- **Verify Signatures** (or **Verify Again**): check the signatures now.

### Structure

An email is built from parts: the text, any attachments, and the signature.
This tab lists every part, with its **Name**, **Size** and **Encoding**.

The **Covered by** column says which signature protects each part. **not
covered** means that part is outside the signature. Anyone could have added or
changed it.

Right-click a part to **Save Part...**, **Import This Key** (if it is a key),
**Copy Content-Type**, **Copy Name** or **Copy SHA-256**.

### Headers

Headers are the lines at the top of an email, such as From, To, Date and
Subject. This tab lists all of them, with their **Name** and **Value**.

Type in **Filter headers** to show only the headers that contain some text.
Right-click a header to **Copy Value** or **Copy Whole Field**.

### Warnings in "What Stands Out"

These are the warnings you may see, in plain words:

- **Signed part no longer in canonical form**: a program changed the message
  after it was signed, usually the line endings. The signature may fail even
  though nobody meant harm.
- **Duplicate ... header**: a header that should appear once appears more than
  once. Different email apps may show different values.
- **Address may be disguised**: an address uses letters that can look like a
  different, familiar address. Check it closely.
- **Replies go somewhere else**: if you reply, your answer goes to a different
  domain than the sender's.
- **Malformed signed section** or **Malformed encrypted section**: the message
  is not built the right way.
- **Not everything is signed**: some parts are outside the signature. Anyone
  could have added them.
- **Signature covers the encrypted data only**: the signature shows who sent
  the encrypted block, not who wrote what is inside. Anyone can sign a copy of
  someone else's encrypted message.
- **Public key attached**: the message carries a public key. A key in a message
  proves nothing about who sent it. Anyone can make a key with any name.
- **Detached signature attached**: the message carries a signature file for
  something else. Opening the message does not check it.
- **Blind recipients are visible**: the message has a Bcc header, so every
  reader can see who got a secret copy.

## Check Before Exporting

When you save a message to an `.eml` file, GpgFrontend takes a last look at it.
If it finds a real risk, a **Check before exporting** window opens. It says:
"Something about this message is worth checking before you save it." and lists
what it found.

It can warn you about:

- **Bcc header present**: the message has a Bcc header. Sending it would tell
  every reader who got a secret copy.
- **Recipient may be disguised**: an address uses letters that can look like a
  different address. Check it before sending.

Smaller notes, such as **Some parts are not signed** or **No recipients**, are
under the details button in the same window.

You decide what to do:

- Click **Save** to save the file anyway.
- Click **Cancel** to go back and fix the message.

**Cancel** is the default, so pressing Enter does not save by accident.

## HTML Messages Open as Source

Some messages are written in HTML, the language of web pages. GpgFrontend
first shows the HTML code as plain text, with this notice: "This message was
written in HTML. It is shown as its source rather than rendered: nothing here
loads images or follows links."

This is safer:

- **No hidden tracking.** Images in an email can tell the sender when and where
  you opened it. Here, no images are loaded.
- **No surprise links.** Nothing opens a website on its own.
- **What you see is what is there.** HTML can hide text, or make one link look
  like another. As plain text, nothing is hidden.

This only happens when a message has no plain-text version. If it has one,
GpgFrontend shows that instead.

![An HTML message shown as its source][img-3]

### Preview an HTML Message

To read the message the way it was laid out, click **Show Preview** on the
notice. The message is then shown formatted, still safely:

- Nothing is loaded from the internet. Pictures from the web stay blank. Only
  pictures sent inside the message are shown.
- Scripts in the message never run.
- Clicking a link asks **Open Link?** first, and shows the full address. Click
  **Open** to open it in your browser. Links that are not web or mail links
  are never opened.

Click **Show Source** to go back to the HTML code. Each message opens as
source again the next time.

**Show Preview** is only there when your system can show HTML:

- **macOS**: always.
- **Windows**: when the Microsoft Edge WebView2 Runtime is installed.
- **Linux**: only in builds that include the optional WebEngine module.

If the button says **Restart to Show Preview**, the preview was just
installed. Restart GpgFrontend to use it.

:::note[New in v2.2.4]

HTML messages can now be previewed.

:::

## Messages Are Checked Again When Your Keys Change

A check result depends on the keys you have. So GpgFrontend checks open
messages again when:

- you import a key, for example the sender's public key, or
- you switch or reload your [key databases](/advanced/key-database/).

For example, a message that said **Signed by an unknown key** can turn into
**Signature verified** right after you import the sender's key.

:::note[New in v2.2.3]

Open messages are now checked again by themselves after your key databases are
reloaded.

:::

[img-1]: TODO
[img-2]: TODO
[img-3]: TODO
