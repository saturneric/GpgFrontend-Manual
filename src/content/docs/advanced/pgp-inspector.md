---
title: "OpenPGP Structure Inspector"
description: "Look inside an encrypted message, signature or key to see what it is made of, without decrypting anything."
sidebar:
  label: OpenPGP Structure Inspector
  order: 13
---

An encrypted message, a signature or a key looks like a block of random letters.
The **OpenPGP Structure Inspector** shows what that block is made of. It opens a
window that lists the parts one by one, in plain labels.

It only reads. It never decrypts anything, and it never asks for your password.

:::note[New in v2.2.3]

The OpenPGP Structure Inspector was added in GpgFrontend v2.2.3.

:::

## Why You Might Use It

You do not need this tool for everyday work. It helps when you want to answer a
question such as:

- "Is this text really an encrypted message, a signature, or a key?"
- "Which key was this message encrypted for?" Look for **Recipient Key ID** or
  **Recipient Fingerprint**.
- "Who signed this?" Look for **Issuer Key ID** or **Issuer Fingerprint**.
- "Why won't this message open?" Damaged parts are shown in a warning colour,
  with a **Problem** line that says what is wrong.

It is also a good way to learn how OpenPGP works.

## Open the Inspector

1. Put the OpenPGP data in a tab of the Text Editor. For example, paste an
   encrypted message, or open a key file.
2. Choose one of these:
   - Click **Advanced** in the menu bar, then **Open OpenPGP Structure
     Inspector**.
   - Right-click inside the text, then choose **Open OpenPGP Structure
     Inspector**.

The **OpenPGP Structure** window opens and shows the current tab.

The menu item is greyed out when the current tab holds no OpenPGP data. It is
also greyed out when the tab holds more than 16 MiB, because the inspector does
not read data that large.

:::note[Flatpak and Mac App Store Lite]

These versions hide the **Advanced** menu. Use the right-click menu in the Text
Editor instead.

:::

## Read the Window

The window has a search box at the top, a tree in the middle and a summary line
at the bottom.

### The Tree

The tree has two columns: **Structure** and **Value**. It has three levels:

1. **Blocks.** One for each piece of OpenPGP data in the tab. A block line says
   what kind it is, for example "Block 1: armored, ..." for text that starts
   with `-----BEGIN PGP`, or "Block 1: cleartext-signed message" for a signed
   text that you can still read.
2. **Packets.** The parts inside a block. A packet line looks like
   `#1  Signature (tag 2)  v4  @0x0000  189 B`. It gives the packet's number,
   its kind, its version, where it starts in the data, and its size.
3. **Fields.** The details of each packet, as a label and a value.

Here is what some common words mean:

| Word                                                     | Meaning                                                                                              |
| -------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| **Public-Key Encrypted Session Key**                     | A locked copy of the message key, for one recipient. There is one per recipient.                     |
| **Symmetric-Key Encrypted Session Key**                  | A copy of the message key locked with a password.                                                    |
| **Symmetrically Encrypted and Integrity Protected Data** | The encrypted message itself.                                                                        |
| **Signature**                                            | A signature. **Issuer Key ID** and **Issuer Fingerprint** name the key that made it.                 |
| **One-Pass Signature**                                   | A note at the start of a signed message that a signature follows.                                    |
| **Literal Data**                                         | The actual content, such as text or a file.                                                          |
| **Compressed Data**                                      | Packed data. The inspector opens it and shows the packets inside.                                    |
| **Public Key**, **Public Subkey**                        | A public key and its subkeys.                                                                        |
| **Secret Key**, **Secret Subkey**                        | A private key and its subkeys.                                                                       |
| **User ID**                                              | A name and email address on a key.                                                                   |
| **Armor Type**                                           | The kind of text block, taken from its `-----BEGIN PGP ...` line.                                    |
| **CRC24**                                                | A checksum of a text block. `ok` means it matches. `mismatch` means the text was changed or damaged. |
| **Problem**                                              | Something is wrong with this part. The value says what.                                              |

A block whose checksum does not match is shown in a danger colour. A block or
packet with a problem is shown in a warning colour.

Encrypted parts stay encrypted. The inspector shows that they are there and how
big they are, but not what they say.

### The Summary Line

The line at the bottom gives the format, the size, and the number of packets. If
something could not be read, the reason follows.

If the window says "The current tab holds no OpenPGP data.", the tab has nothing
the inspector can read.

### Search

Type in the search box (**Search packets, fields and values**) to show only the
lines that contain your words, in either column. When a packet matches, all its
fields stay visible. Clear the box to see everything again.

## If the Menu Item Is Missing

The inspector comes from a module that ships with GpgFrontend. If you cannot
find **Open OpenPGP Structure Inspector**, the module may be turned off. See
[Module Controller](/advanced/module-controller/).
