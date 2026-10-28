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

![][img-1]

![][img-2]

### From a File

Choose a public or private key file to import. The file can be text with any
extension.

### By Pasting Into the Editor

Paste the key into a Text Editor tab. Then open **Keys** > **Import Key** (or
the **Import** toolbar button) and choose **Editor**. GpgFrontend imports the
key from the text in that tab.

### From the Clipboard

Copy a key's contents to your system clipboard, then choose this option to import
it.

### From a Key Server (public keys only)

Open the **Import Key** menu and choose **Key Server**. Enter the email or ID you are
looking for, pick a key server, and click search. GpgFrontend shows the matching
public keys. Double-click a row to import that key. To import more, double-click
each one in turn. This method imports **public keys only**.

**Key Server** comes from the KeyServerSync module. If that module is turned
off, it is not in the menu.

For the full steps, see [Key Server Operations](/guides/key-server-operations/).

### By Drag and Drop

Drag a key file straight onto the Key ToolBox, then follow the prompts to import
it.

## Export a Key

Exporting saves a key so you can back it up or share it. GpgFrontend always exports
in ASCII text, so the file works across different computers.

You can export your **public key** (safe to share) or your **private key** (keep
this secret). The export options work much like the import ones.

### Export a Public Key

Your public key is safe to give to anyone. There are a few ways to export it.

#### The Quick Way

Click **Manage Keys** to open the **KeyPair Management** window. Right-click the
key there, open **Export** and choose **Export Public Key...**. Pick where to
save it, and you are done. New in v2.2.2.

If you only want to paste it somewhere rather than save a file, open **Copy**
in the same menu and choose **Copy Public Key Block**. See
[Manage Your Keys](/guides/key-management/).

#### Append to the Editor

Right-click a key in the Key ToolBox and choose **Append Public Key to Editor**.
This adds the public key to the end of the editor page, where you can copy it
wherever you need.

#### Save to a File

Use the key pair's **Operations** tab to save the public key to a file, as shown
below. Pick a folder for the file first.

![][img-3]

#### Export Several at Once

To export the public keys of several key pairs together, tick them in the
**KeyPair Management** window. Then open **Key** > **Export Key** and choose
**Export To Clipboard**, or use the **Export Key** button on the toolbar. This
copies the data to your clipboard, ready to paste into any app or file.

If you tick nothing, it uses the rows you selected instead.

![][img-4]

#### Export for SSH

**Export As OpenSSH** saves a single key in the format an SSH server expects,
so you can use an OpenPGP key to log in to a machine. You need a key that can
do **Authentication** (the `A` flag).

In the **KeyPair Management** window, right-click the key, open **Export** and
choose **Export As OpenSSH**. It is also under **Key** > **Export Key**. This
needs the GnuPG engine; with rPGP the item is hidden.

### Export a Private Key

The quickest way is to right-click the key in the **KeyPair Management**
window, open **Export** and choose **Export Private Key...**. New in v2.2.2.

You can also find private key options on the detail page of a key that holds a
private part (the primary key or a subkey). Pick a destination, and GpgFrontend
exports the private key there.

![][img-5]

:::caution[Never share your private key]

The private key file must stay secret. If it leaks, anyone can read every message
encrypted to that key. Share only your public key.

:::

Exporting a private key also includes the matching public key, because a private
key is meaningless on its own. So the two are bundled together in the export.

You can export your private key in two ways:

1. **Export Full Secret Key**: includes all key data, plus the user IDs and their
   signatures.
2. **Export Shortest Secret Key**: includes only the key data, without the extra
   user ID signatures.

## Back Up Everything at Once

Exporting keys one at a time is fine for sharing, but a poor way to make a
backup. It is too easy to miss one.

Since v2.2.2 you can save them all in one go. In the **KeyPair Management**
window, open **Operations** > **Bulk** and choose **Back Up All Private
Keys...**. That writes every private key in the keyring into a single protected
[KeyPackage](/advanced/key-package/). The same three-step window opens as for
any KeyPackage, with all private keys already included.

:::tip[Back up your keys]

Make that backup and keep it somewhere safe and offline, such as an encrypted
drive. If you ever lose your keys, it is the only way to get them back.

Back up your revocation certificates in the same place. See
[Key Revocation](/advanced/key-revocation/).

:::

[img-1]: https://image.cdn.bktus.com/i/2026/10/25/89b5efe0a8c06de2117dc72c62ac7df6cada8c7e-0.webp
[img-2]: https://image.cdn.bktus.com/i/2026/10/25/abf57aec551b57ef4d64cca52cb789af1f7427bf-0.webp
[img-3]: https://image.cdn.bktus.com/i/2026/10/25/325f7d43bec3eb3f9e8663eefe54ca975e13cd79-0.webp
[img-4]: https://image.cdn.bktus.com/i/2026/10/25/5e494676304a77f8e488862567fbf1aba6e51782-0.webp
[img-5]: https://image.cdn.bktus.com/i/2026/10/25/ff3e0ec7b761365a2c2b1a1aafd15887abb49ba2-0.webp
