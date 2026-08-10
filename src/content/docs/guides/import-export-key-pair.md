---
title: Import & Export Key Pair
description: "Import and export OpenPGP key pairs in GpgFrontend via file, editor, clipboard, or key server for easy backup and key sharing."
sidebar:
  order: 9
---

GpgFrontend gives you several ways to **import** keys (bring them in) and
**export** keys (save or share them). You'll usually do this for two reasons: to
**share your public key** with someone, or to **back up** your own keys. This
page covers each method.

## Import a Key

You can import a public or private key in a few ways. Find them on the toolbar, or
open the action menu in the key management section for more options.

![](https://image.cdn.bktus.com/i/2025/06/24/65a0c1fce233c2fc15afd362b432eb53f684c73d.webp)

![](https://image.cdn.bktus.com/i/2025/06/24/0f9c76d074dd6c364603baea3c565e66c9a8d62d.webp)

### From a File

Choose a public or private key file to import. The file can be text with any
extension.

### By Pasting Into the Editor

Paste the contents of a key into a blank editor page. GpgFrontend recognizes the
key and imports it for you.

### From the Clipboard

Copy a key's contents to your system clipboard, then choose this option to import
it.

### From a Key Server (public keys only)

Search a key server and import public keys from it. Enter the email or ID you are
looking for, pick a key server, and click search. GpgFrontend shows the matching
public keys. You can import several at once, or double-click one row to import just
that key. This method imports **public keys only**.

For the full steps, see [Key Server Operations](/guides/key-server-operations/).

### By Drag and Drop

Drag a key file straight onto the Key Toolbox, then follow the prompts to import
it.

## Export a Key

Exporting saves a key so you can back it up or share it. GpgFrontend always exports
in ASCII text, so the file works across different computers.

You can export your **public key** (safe to share) or your **private key** (keep
this secret). The export options work much like the import ones.

### Export a Public Key

Your public key is safe to give to anyone. There are a few ways to export it.

#### The Quick Way

Right-click the key in the **Manage Keys** window and choose **Export Public
Key...**. Pick where to save it, and you are done. New in v2.2.2.

If you only want to paste it somewhere rather than save a file, use **Copy
Public Key Block** in the same menu. See
[Manage Your Keys](/guides/key-management/).

#### Append to the Editor

Right-click a key in the Key Toolbox and choose **Append Select Key(s) to Editor**.
This adds the public key to the end of the editor page, where you can copy it
wherever you need.

#### Save to a File

Use the key pair's **Operations** tab to save the public key to a file, as shown
below. Pick a folder for the file first.

![](https://image.cdn.bktus.com/i/2025/06/24/b9ea951b5c94e8f18cc22e6e415778b97818718f.webp)

#### Export Several at Once

To export the public keys of several key pairs together, select them in the key
management view and click **Export to Clipboard**. This copies the data to your
clipboard, ready to paste into any app or file.

![](https://image.cdn.bktus.com/i/2025/06/24/0ce7919189489923f38e3871e407dad96b788174.webp)

#### Export for SSH

**Export As OpenSSH** saves a single key in the format an SSH server expects,
so you can use an OpenPGP key to log in to a machine. You need a key that can
do **Authentication** (the `A` flag).

### Export a Private Key

The quickest way is to right-click the key in the **Manage Keys** window and
choose **Export Private Key...**. New in v2.2.2.

You can also find private key options on the detail page of a key that holds a
private part (the primary key or a subkey). Pick a destination, and GpgFrontend
exports the private key there.

![](https://image.cdn.bktus.com/i/2025/06/24/9dbc57b795542a5f9c2f78875d5be1f9c692ed0d.webp)

:::caution[Never share your private key]

The private key file must stay secret. If it leaks, anyone can read every message
encrypted to that key. Share only your public key.

:::

Exporting a private key also includes the matching public key, because a private
key is meaningless on its own. So the two are bundled together in the export.

You can export your private key in two ways:

1. **Full export**: includes all key data, plus the user IDs and their signatures.
2. **Minimal export**: includes only the key data, without the extra user ID
   signatures.

## Back Up Everything at Once

Exporting keys one at a time is fine for sharing, but a poor way to make a
backup. It is too easy to miss one.

Since v2.2.2 you can save the lot in one go. In the **Manage Keys** window,
open the **Bulk** menu and choose **Back Up All Private Keys...**. That writes
every private key in the keyring into a single protected file.

:::tip[Back up your keys]

Make that backup and keep it somewhere safe and offline, such as an encrypted
drive. If you ever lose your keys, it is the only way to get them back.

Back up your revocation certificates in the same place. See
[Key Revocation](/advanced/key-revocation/).

:::
