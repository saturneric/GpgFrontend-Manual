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

:::note[Mac App Store Lite]

This version hides the **Advanced** menu. Use the right-click menu in the Text
Editor instead.

:::

## Read the Window

The window has a search box at the top, a list of parts on the left, details
on the right, and a summary line at the bottom.

:::note[Changed in v2.2.4]

The window was redesigned. It used to show everything in one tree with a
**Structure** and a **Value** column. Now the left side lists the parts, and
the details of the part you click appear in tabs on the right.

:::

### The List on the Left

The list has two levels:

1. **Blocks.** One for each piece of OpenPGP data in the tab. A block line says
   what kind it is, for example "Block 1: Cleartext Signed Message", and then
   how many packets it holds.
2. **Packets.** The parts inside a block. Each line shows the packet's number
   and kind (for example `#1  Signature`), a short summary, and its size.
   Packets inside other packets get numbers like `#2.3`.

Click a line to see its details on the right.

### The Tabs on the Right

Each tab is a table with a **Field** and a **Value** column. Tabs with nothing
to show are hidden.

- **Overview**: the main details of the packet. A **Problem** line comes
  first, if there is one. A **Framing** group at the end says where the packet
  starts (**Offset**), how it is wrapped (**Header**, **Body**) and its
  **Size**.
- **Subpackets**: the extra details inside a signature, such as who made it
  and when.
- **Key Material**, **Signature Material** or **Session Key Material**: the
  numbers that make up the key, signature or locked message key. Each value
  says how many bytes it has. Private key material is never shown, only that it
  is there.
- **Hex**: the raw bytes of the packet, with labels.

For keys, **Overview** also shows the **Public Key Algorithm**, the **Key
Size** and, for keys based on elliptic curves, the **Curve**.

When you click from one packet to the next, the tab you picked stays open.

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

A line is coloured only when something is wrong with it. A block whose
checksum does not match is shown in red. Other problems are shown in a warning
colour. Hold the mouse over the line to see the reason.

Encrypted parts stay encrypted. The inspector shows that they are there and how
big they are, but not what they say.

### The Summary Line

The line at the bottom gives the format, the size, and the number of packets. If
something could not be read, the reason follows.

If the window says "The current tab holds no OpenPGP data.", the tab has nothing
the inspector can read.

### Search

Type in the search box (**Search packets, fields and values**) to show only the
packets whose details contain your words. Matching lines in the tabs are shown
in bold. Clear the box to see everything again.

## If the Menu Item Is Missing

The inspector comes from a module that ships with GpgFrontend. If you cannot
find **Open OpenPGP Structure Inspector**, the module may be turned off. See
[Module Controller](/advanced/module-controller/).
