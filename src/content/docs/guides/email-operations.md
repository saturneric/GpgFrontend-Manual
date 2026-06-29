---
title: Email Functionality
description: "Sign, encrypt, verify, and decrypt emails offline in GpgFrontend using the .eml format and the built-in OpenPGP Email module."
sidebar:
  label: Email Operations
  order: 8
---

GpgFrontend can **sign**, **encrypt**, **verify**, and **decrypt** email, all on
your own computer. It does this with `.eml` files, a standard email file format
that almost every email app understands.

## How It Works

The key thing to understand: **GpgFrontend does not send or receive email.** It
only does the encryption and signing part, offline. Your normal email app still
handles sending and receiving. Your private keys never leave your computer.

So the flow is simple:

- **To send a secure email**: write and protect it in GpgFrontend, save it as an
  `.eml` file, then open that file in your email app and send it.
- **To read a secure email**: save the email as an `.eml` file from your email app,
  then open it in GpgFrontend to decrypt or verify it.

## Open the Email Tools

Email support comes from the built-in **Email module**, which ships with the
regular GpgFrontend desktop edition and loads on its own. There is nothing to set
up in Settings.

There are two ways in:

- Click **New E-Mail** to write a message, protect it, and save it as an `.eml`
  file.
- Open an existing `.eml` file (for example, one saved from your email app) to
  verify or decrypt it. GpgFrontend shows the email headers (From, To, Subject,
  Date) next to the OpenPGP result.

:::note[Don't see the email buttons?]

You are probably running an edition without the Email module, or a build with
modules excluded.

:::

## Write and Send a Secure Email

### Step 1: Write and Sign

1. Click **New E-Mail** to open a blank message.
2. Type your message in the editor.
3. Pick your **private key** in the **Key Toolbox**.
4. Click **Sign**.
5. In the dialog, fill in **From**, **To**, and **Subject**. Use the **CC** and
   **BCC** buttons to show those fields if you need them.

GpgFrontend fills in **From** for you, taken from your signing key. When you
encrypt, it can also suggest recipients from the encryption keys you picked.

:::note[Address format]

Each address must be a plain address (`alice@example.com`) or the
`Name <alice@example.com>` form. Separate several recipients in **To**, **CC**, or
**BCC** with a semicolon (`;`). Bad entries are flagged before the email is built.

:::

![](https://image.cdn.bktus.com/i/2025/06/24/84f732220b3a967aa5d3986f79475bdfcf53454e.webp)

![](https://image.cdn.bktus.com/i/2025/06/24/610ba60f2cd8eeddbcfbbc57aa602cff61197065.webp)

![](https://image.cdn.bktus.com/i/2025/06/24/fea933e12bf46516d6a1385698b6afa94e7543a0.webp)

![](https://image.cdn.bktus.com/i/2025/06/24/ee90e5bb25c7accdccf70f17c1986e53e0b4e81f.webp)

### Step 2: Encrypt (Optional)

To hide the content so only the recipient can read it:

1. Pick the recipient's **public key** in the **Key Toolbox**.
2. Click **Encrypt**.

You can sign and encrypt together for a message that is both private and proven to
be from you.

![](https://image.cdn.bktus.com/i/2025/06/24/f8fe32d6e3502a1ba3503189fa40e4348bd4cc81.webp)

### Step 3: Save and Send

1. Save the message as an `.eml` file with **File > Save As**.
2. In your email app or webmail, open that `.eml` file (for example, drop it into
   your drafts), then send it as usual.

Remember, GpgFrontend doesn't send the email. Your email app does.

## Read a Secure Email

1. In your email app, save or export the message as an `.eml` file (or copy the raw
   email source).
2. Open the `.eml` file in GpgFrontend.
3. Choose what to do:
   - **Decrypt Verify**: decrypt and check the signature at the same time.
   - **Verify**: check the signature only, without decrypting.
   - **Decrypt**: decrypt only, without checking the signature.

A signed email shows a **Good Digital Signature** message. An encrypted email is
shown decrypted.

![](https://image.cdn.bktus.com/i/2025/06/24/64b84451fd044cfd0c081161dad3057c5fde25a4.webp)

### Understand the Results

After you verify or decrypt an `.eml` file, GpgFrontend shows the outcome as a set
of result cards:

- **E-Mail card**: the message headers, including **From**, **To**, **Subject**,
  **CC**, **BCC**, and **Date**.
- **OpenPGP card**: details of the OpenPGP/MIME structure, including the **Signed
  EML Data Hash (SHA1)** that the signature covered, and the **Message Integrity
  Check Algorithm** (the `micalg` named in the message).
- **Encryption Recipient cards**: for encrypted mail, who each copy was encrypted
  to, shown as the key's user ID and **Key ID**.

These cards let you confirm that the signature covers the message you actually
received, and that it was encrypted to the keys you expect.

## Tips and Troubleshooting

- **Signature shows as invalid.** A PGP/MIME signature covers the exact bytes of
  the signed part. If a mail server or app rewraps or re-encodes the message in
  transit, the check can fail even when the text looks fine. When you can, save the
  original `.eml` source rather than a re-rendered copy.
- **The email buttons are missing.** The email tools come from the Email module. If
  they aren't there, you are likely running an edition without it, such as
  GpgFrontend Lite. See [Open the Email Tools](#open-the-email-tools).
- **An address is rejected.** Make sure each address is `alice@example.com` or
  `Name <alice@example.com>`, and separate several recipients with a semicolon
  (`;`).
- **Can't decrypt a received email.** Check that the matching private key is in the
  active key database, and that you picked the database whose keys match the
  recipients.
- **The recipient can't read your message.** Make sure your app kept the `.eml`
  exactly as is, and that their email app supports PGP/MIME. Apps that only support
  inline PGP may not be able to read it.
- **Use trusted keys.** Import public keys only from sources you trust, and check
  them before you rely on them.
- **Keep private keys safe.** Never upload them to email providers; store them on
  encrypted storage.

## Good to Know (Technical Details)

You can skip this section. It explains the formats and choices behind the email
tools.

- **Standards**: GpgFrontend follows the OpenPGP standards (RFC 4880 and RFC 3156),
  so the output works with Thunderbird and other OpenPGP email apps.
- **PGP/MIME, not inline**: it produces **PGP/MIME** messages. A signed message is
  wrapped as `multipart/signed` with a detached signature; an encrypted one as
  `multipart/encrypted`. This keeps the body, attachments, and formatting intact,
  and it is the format modern clients like Thunderbird expect.
- **Why `.eml` and not IMAP/SMTP**: `.eml` is supported almost everywhere and is
  easy to export, import, and process offline. Building in full mail protocols
  would add complexity and risk, and pull the app away from its focus on local
  encryption.
- **Offline by design**: every operation runs on your computer. Your private keys
  and message contents are never sent to outside servers.
