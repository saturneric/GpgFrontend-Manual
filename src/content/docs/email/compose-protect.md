---
title: Write and Protect a Message
description: "Write an email in GpgFrontend, then sign it, encrypt it, or both. Covers the header fields, replies, attachments, the raw source and the Security menu."
sidebar:
  label: Write and Protect
  order: 2
---

This page shows how to write an email in GpgFrontend and how to protect it.

- **Signing** proves the message came from you and was not changed on the way.
- **Encrypting** hides the message so only the people you choose can read it.

You can do one, the other, or both. Everything happens on your own computer.

On a Mac, press Cmd where this page says Ctrl, and Option where it says Alt.

## Start a New Message

1. Click **File** > **Workspace** > **Mail Editor**.
2. A new tab opens with an empty message.

Each message is an `.eml` file. You can save it with **File** > **Save File** or
**File** > **Save As...**, like any other file.

## Fill In the Header Fields

The header fields sit at the top of the message:

- **From:** who the message is from. This is you.
- **To:** who the message is for.
- **Subject:** what the message is about.

To add more people:

1. Click **Cc/Bcc** at the end of the **To:** row (or press Ctrl+Shift+C).
2. Two more rows appear: **Cc:** and **Bcc:**.

What these mean:

- **Cc** (carbon copy) sends a copy to someone. Everyone can see who was in Cc.
- **Bcc** (blind carbon copy) sends a copy in secret. The other people do not
  see this name.

To add several people in one field, put a semicolon (`;`) between the
addresses. For example: `alice@example.com; bob@example.com`.

Each address can be written as `alice@example.com` or as
`Alice <alice@example.com>`.

### Address Suggestions

As you type an address, GpgFrontend suggests matching addresses:

- In **From:**, it suggests your mail accounts first, then the addresses on
  your own private keys.
- In **To:**, **Cc:** and **Bcc:**, it suggests the addresses on the keys in
  your key database.

### About Bcc

Names in **Bcc:** are never written into the message itself. If they were,
every reader could see who got a secret copy.

GpgFrontend still uses them in two ways:

- When you encrypt, it can use them to pick the keys to encrypt to.
- When you send, it gives them to your mail server, so they still get the
  message.

They are not saved in the `.eml` file.

:::note[New in v2.2.3]

The header fields are now part of the message tab. The old pop-up window that
asked for From, To and Subject is gone.

:::

## Write the Body

Click in the large area below the header fields and type your message. It shows
**Write your message here.** until you start typing.

## Attach Files

1. Click **Attach File...** (or press Ctrl+Shift+A).
2. Pick one or more files and confirm.

You can also drag files from your computer and drop them onto the message.

Each file can be up to 48 MiB. Folders cannot be attached. If a file is refused,
a window tells you which one and why.

Your attachments are listed under the message. To learn more about the list, see
[Work With Attachments](/email/reading-imap/#work-with-attachments).

## Reply, Reply All and Forward

When you open a message you received, the action row shows three buttons:

- **Reply** (Ctrl+R): write back to the sender.
- **Reply All** (Ctrl+Shift+R): write back to
  the sender and everyone else who was addressed. People in Bcc are not
  included.
- **Forward** (Ctrl+L): pass the message on to someone
  else, with its attachments.

Each one opens a **new tab** with a new message. The original message is not
changed.

On a message you are still writing, these buttons are not on the row. You find
**Send...** and **Attach File...** there instead. Other actions are under
**More**.

## Message and Raw Source

Above the body you can switch between two views:

- **Message** (Alt+1): the normal view, with header
  fields, body and attachments.
- **Raw Source** (Alt+2): the full message as plain text,
  exactly as it is stored in the file.

The raw source is read-only at first. To change it by hand:

1. Switch to **Raw Source**.
2. Click **Edit Raw Source**.
3. Make your changes. What you type here is the message itself.
4. Click **Stop Editing** when you are done.

Most people never need the raw source. It is there for checking or fixing a
message by hand.

## Sign or Encrypt the Message

First pick your keys in the [Key Toolbox](/guides/understand-interface/#key-toolbox)
on the right:

- **To sign:** check your own private key.
- **To encrypt:** check the public key of each person who should read the
  message. Check your own key too if you want to read it later.

Then use the **Security menu**:

1. Find the status button at the right end of the action row. On a new message
   it says **Not signed or encrypted**.
2. Click it. A menu opens.
3. Choose one:
   - **Sign...**: sign the message.
   - **Encrypt...**: encrypt the message.
   - **Encrypt and Sign...**: do both at once. This is the best choice for a
     private message.

The result shows in the **Status Panel**. The status button changes to tell you
what the message is now, for example **Encrypted**.

You can also use the **Sign** and **Encrypt** buttons on the main toolbar. They
do the same thing. **Encrypt & Sign** is in the **Encrypt** button's list:
right-click the button to find it.

### What the Security Menu Offers

The menu changes with the message. This is what you see:

| The message is...       | The menu offers                                                                                             |
| ----------------------- | ----------------------------------------------------------------------------------------------------------- |
| Not signed or encrypted | **Sign...**, **Encrypt...**, **Encrypt and Sign...**                                                        |
| Signed                  | **Verify Signature**, **Signature Details...**, **Sign Again With Another Key...**, **Remove Signature...** |
| Encrypted               | **Decrypt**, **Decrypt and Verify**, **Encryption Details...**                                              |
| Encrypted and signed    | **Decrypt and Verify**, **Decrypt**, **Details...**, **Remove Signature...**                                |
| Broken                  | **What Is Wrong With This Message?**, **Try to Verify Anyway**, **Try to Decrypt Anyway**                   |

"Broken" means the message says it uses OpenPGP, but it is not built the right
way. To learn how to check a message you received, see
[Verify and Inspect a Message](/email/verify-inspect/).

## Signed and Encrypted Messages Are Locked

Once a message is signed or encrypted, you cannot edit it. A notice above the
body tells you why:

- **Signed:** a change under a signature would look like a forgery. To edit,
  first remove the signature with **Remove Signature...** in the Security menu.
- **Encrypted:** decrypt it first.
- **Encrypted and signed:** decrypt it, then remove the signature.

If you try to change a signed message anyway, GpgFrontend asks: **Remove the
signature and make it an ordinary message?** Click **Yes** to remove it, or
**Cancel** to keep it.

Removing a signature cannot be undone. The text of the message is kept as it
is.

### Lock a Message Yourself

You can also lock a message you received, so nobody changes it by accident:

1. Click **More**.
2. Click **Read-only**.

A **Read-only** label appears. **Reply** and **Forward** still work, and they
make new messages. To unlock, click **More** > **Read-only** again.

## Send or Save the Message

You have two choices:

- **Send it from GpgFrontend.** Click **Send...** (or press
  Ctrl+Enter). You need a mail account for this. See
  [Mail Accounts and Sending](/email/accounts-sending/).
- **Send it with another email app.** Save the message as an `.eml` file with
  **File** > **Save As...**. Then open or import that file in your usual email app
  and send it from there.

Before the file is saved, GpgFrontend takes a last look at the message. If
something looks risky, it shows a **Check before exporting** window. See
[Check Before Exporting](/email/verify-inspect/#check-before-exporting).

## Understand the Results

After you sign, encrypt, verify or decrypt, the **Status Panel** shows the
result as a set of cards:

- **E-Mail**: the message headers: **From**, **To**, **Subject**, **CC**,
  **BCC** and **Date**.
- **OpenPGP**: two technical values about the signature:
  - **Digest of Signed MIME Entity (SHA-256)**: a fingerprint of the exact part
    of the message that the signature covers. If two copies show the same
    value, the signed part is the same in both.
  - **Declared Signature Hash (micalg)**: the hash method the message says its
    signature uses. This is only what the message claims.
- **Attachments**: each file in the message. It also says when a file is an
  OpenPGP key, or when it is **not covered by the signature**.
- **Recipient Check**: for encrypted mail, whether each person in the headers
  can really read it. A warning here means someone was addressed but not
  encrypted to, so they cannot open it.
- **Encryption Recipient**: who each copy was encrypted to, shown as the key's
  name and **Key ID**.

## Tips and Troubleshooting

- **Send... is grayed out.** Hover over it. It tells you what is missing, for
  example a subject or a recipient.
- **A signature shows as bad, but the text looks fine.** A signature covers the
  exact bytes of the message. Some programs change line endings or re-encode a
  message when they save or forward it. When you can, save the original `.eml`
  file instead of a copy.
- **You cannot decrypt a message.** Check that the matching private key is in
  the key database you are using right now.
- **The reader cannot open your message.** Make sure their email app supports
  PGP/MIME. Apps that only know older "inline PGP" may not open it.
- **Keep private keys safe.** Never upload them to an email provider.

## Good to Know (Technical Details)

You can skip this section.

- GpgFrontend follows the OpenPGP standards ([RFC 4880][rfc4880] and
  [RFC 3156][rfc3156]). The messages work with Thunderbird and other OpenPGP
  email apps.
- It makes **PGP/MIME** messages, not inline PGP. A signed message has its
  signature in a separate part. An encrypted message is wrapped as one
  encrypted part. This keeps the body, attachments and formatting intact.
- `.eml` files work almost everywhere. You can always move a message to or from
  another email app.

[rfc4880]: https://www.rfc-editor.org/rfc/rfc4880
[rfc3156]: https://www.rfc-editor.org/rfc/rfc3156
