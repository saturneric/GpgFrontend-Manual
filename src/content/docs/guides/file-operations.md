---
title: File Operations
description: "Encrypt, decrypt, sign, and verify files and folders in GpgFrontend using the File Panel and quick direct-selection workflows."
sidebar:
  order: 5
---

Working on files is much like [working on text](/guides/text-operations/): you can
**encrypt**, **decrypt**, **sign**, and **verify** them. The difference is that
files are handled as binary input and output. You do all of this in the **File
Panel**.

## Open Files in the File Panel

The File Panel is where you work on files. There are two ways to open it.

**Using the Open button:**

1. In the main window toolbar, click **Open**. Or open the **File** menu and
   choose **Open**.
2. Choose **File...** to pick one file, or **Directory...** to pick a folder.
3. Pick the file or folder you want.
4. The File Panel opens. If you picked a file, it is highlighted and ready. If
   you picked a folder, you see its contents and can choose files inside.

![][img-1]

**Using the Workspace button:**

1. In the main window toolbar, click **Workspace**. Or open the **File** menu
   and choose **Workspace**.
2. Choose **New File Panel**. The shortcut is **Ctrl+B**.
3. A new **File Panel** tab opens. Click the file you want.

The new panel opens at the folder set in **Settings**, **General**, **File
Panel Opens At:**. You can pick **Profile Workspace**, **Home Folder** or
**Working Directory** there.

The Flatpak and Mac App Store builds hide that setting. There, a window called
**Select Default Path** asks you to pick a folder each time you open a new
File Panel.

![][img-2]

## Getting Around the File Panel

The **path bar** across the top shows the folder you are in, one step at a
time. Click any step to jump straight to it. There is a **Home** step at the
start.

To type a path instead, click the edit button at the end of the path bar, or
press **Ctrl+L**. You can use `~` for your home folder.

The small buttons next to the path bar have icons only. Point at one to see
its tooltip:

- **Go to the parent folder (Backspace)**: go to the folder above. The
  **Backspace** key does the same.
- **Read this folder from disk again**: refresh the list.
- **Go to a mounted volume or removable drive**: jump to a USB drive, another
  disk, or your **Profile Workspace**.
- **Create items and choose what the list shows**: opens the options menu.
  It holds:
  - **New Folder** and **New Empty File**, to make something in the folder
    you are in.
  - **Show**, a submenu where you choose what the list shows: **Hidden
    Files**, **System Files** and **Type Column**.
  - **Use ASCII Armor**. See
    [Choose ASCII or Binary Output](#choose-ascii-or-binary-output).
- **Enable batch mode to select multiple files.**: see
  [Batch Mode](#work-on-many-files-at-once-batch-mode).

The **Filter** box lists only the files and folders whose name contains the
text you type.

Along the bottom you can see how many items are in the folder, how many you
have selected, and how much space is left on the disk.

To delete something, right-click it and choose **Move to Trash**, or press
**Del**. GpgFrontend asks first.

## Right-Click a File or Folder

Right-click an item in the File Panel to see what you can do with it:

- **Open**: open the file in a GpgFrontend tab. **Enter** does the same.
- **Open with Default Application**: open the item in the app your system uses
  for it.
- **New**: make an **Empty File** or a **Folder**. See
  [Make or Rename Files and Folders](#make-or-rename-files-and-folders).
- **Rename**: give the item a new name. **F2** does the same.
- **Move to Trash**: move the item to your system's Trash, where you can still
  get it back.
- **Copy Path**: copy the full path of the item to the clipboard.
- **Refresh**: read the folder from disk again.
- **Calculate Hash**: work out checksums of the file and show them in the
  **Status Panel**. Use them to check that a download is complete and
  unchanged.

## Make or Rename Files and Folders

### Make a new folder or file

1. Click the options button (**Create items and choose what the list
   shows**), then **New Folder** or **New Empty File**. Or right-click in the
   list and choose **New**, then **Folder** or **Empty File**.
2. A window called **New Folder** or **New File** opens. It shows the
   **Location:** where the item will be made.
3. Type the name in **Name:**.
4. Click **Create**.

### Rename a file or folder

1. Click the item, then press **F2**. Or right-click it and choose **Rename**.
2. A window called **Rename File** or **Rename Folder** opens.
3. Type the new name in **Name:**.
4. Click **Rename**.

### If the name is not accepted

The window checks the name as you type. The **Create** or **Rename** button
stays greyed out, and a short message says why:

- **Enter a folder name.** or **Enter a file name.**: the box is empty.
- **The name must not contain path separators.**: remove any `/` or `\`.
- **This name is reserved.** or **This name is reserved by the operating
  system.**: pick another name.
- **Enter a name different from the current one.**: when renaming, the name
  is still the same.
- **A file or folder with this name already exists.**: pick another name.

If the name is fine but the item still cannot be made or renamed, for example
because you are not allowed to write to that folder, a message says so. Its
title is **Unable to Create Folder**, **Unable to Create File** or **Unable to
Rename**.

:::note[Changed in v2.2.3]

Making and renaming files and folders now uses one clear window that checks
the name before you click.

:::

## Encrypt, Decrypt, Sign, or Verify a File

The buttons are the same as for text: **Encrypt**, **Decrypt**, **Sign** and
**Verify** on the toolbar, or the same items in the **Operations** menu. They
act on the file you selected in the File Panel. See
[Find the Buttons](/guides/text-operations/#find-the-buttons) for the full list
and shortcuts.

GpgFrontend never changes your original file. It always writes a **new file**
next to it, in the same folder. The new file's name tells you what it is:

| Task    | You select       | New file made          | Example          |
| ------- | ---------------- | ---------------------- | ---------------- |
| Encrypt | `report.pdf`     | name + `.gpg`          | `report.pdf.gpg` |
| Sign    | `report.pdf`     | name + `.sig`          | `report.pdf.sig` |
| Decrypt | `report.pdf.gpg` | name without `.gpg`    | `report.pdf`     |
| Verify  | `report.pdf.sig` | nothing, only a result |                  |

If you turned on ASCII output, encrypting and signing make `.asc` files
instead. See [Choose ASCII or Binary Output](#choose-ascii-or-binary-output).

If a file with the new name is already there, GpgFrontend asks first. It only
replaces the old file after the task has worked. If the task fails, no new file
is left behind.

### Encrypt a File

You need the **recipient's public key**.

1. **Select the file.** In the File Panel, click the file once so it is
   highlighted.
2. **Pick the recipient.** In the **Key ToolBox** on the right, tick the box in
   front of the recipient's public key. Tick your own key too if you want to
   open the file later yourself.
3. **Click Encrypt.**
4. **Answer any questions.** GpgFrontend may stop to check your recipients. See
   [Encryption Safety](/guides/encryption-safety/).
5. **Find the new file.** It appears in the same folder, for example
   `report.pdf.gpg`. The **Status Panel** shows whether it worked.
6. **Send the new file**, not the original.

![][img-3]

:::caution

If you tick **no key**, **Encrypt** is greyed out. To encrypt the file with a
password instead, use **Operations** > **Sym. Encrypt**
([symmetric encryption](/guides/symmetric-encrypt-decrypt/)).

:::

### Decrypt a File

You need **your private key**.

1. **Select the encrypted file** in the File Panel, for example
   `report.pdf.gpg`.
2. **Click Decrypt.** You do not need to tick a key. GpgFrontend finds the
   right one.
3. **Enter your passphrase** when asked.
4. **Find the new file.** It appears in the same folder, with `.gpg`, `.pgp`
   or `.asc` taken off the end: `report.pdf`. If the name has no such ending,
   GpgFrontend adds `.out` instead.

If the file was also signed, use **Decrypt & Verify** from the **Operations**
menu to check the signature at the same time. If you added it to the toolbar,
it is also in the **Decrypt** button's list.

![][img-4]

### Sign a File

Signing makes a small, separate signature file. The original file stays as it
is. You send both files together. You need **your private key**.

1. **Select the file** in the File Panel.
2. **Pick your key.** In the **Key ToolBox**, tick the box in front of **your
   own** key. If you tick no key, or a key that can't sign, **Sign** is greyed
   out.
3. **Click Sign.**
4. **Choose a key, if asked.** If your key has more than one signing subkey
   that still works (not revoked or expired), a window called **Select Signing
   Key(s)** opens. Tick the key or subkey to use and click **Confirm**.
5. **Enter your passphrase** when asked.
6. **Find the signature file.** It appears next to the original, for example
   `report.pdf.sig`.
7. **Send both files**: `report.pdf` and `report.pdf.sig`. Keep their names as
   they are.

:::caution

After signing, do not change the original file, not even by saving it again
without edits. If it changes, the signature no longer matches.

:::

### Verify a File

You need **the sender's public key**, and both files: the original and its
signature.

1. **Put both files in the same folder**, with their names unchanged, for
   example `report.pdf` and `report.pdf.sig`.
2. **Select the signature file** (`report.pdf.sig` or `report.pdf.asc`) in the
   File Panel. Select the signature, not the original.
3. **Click Verify.** You do not need to tick a key.
4. **Read the result** in the **Status Panel**: green means the file is
   unchanged and signed by the key shown; red means it was changed or the
   signature does not match.

GpgFrontend finds the original by taking `.sig` or `.asc` off the signature's
name. If it cannot find that file, a window called **File to be Verified**
asks for the full path of the original:

- Type or paste the full path to the original file and click **OK**.
- Leave the box **empty** and click **OK** if the file you selected holds the
  data and the signature together in one file.

If you select a `.gpg` or `.pgp` file, GpgFrontend treats it as one file that
holds both the data and the signature.

If the sender's public key is missing, the **Missing Keys** window opens. See
[If the Sender's Key Is Missing](/guides/text-operations/#if-the-senders-key-is-missing).

## Drag and Drop Files

The File Panel supports drag-and-drop, an easy way to bring files into your
working folder or move them around without using the system file dialog.

### Where Items Are Dropped

Where an item lands depends on what is under the cursor when you let go:

- Drop onto a folder to place the items inside that folder.
- Drop onto a file to place the items in that file's parent folder.
- Drop onto empty space to place the items in the folder shown in the panel.

The target folder must be one you can write to. If it is not, a **Copy
Failed** or **Move Failed** message says **The target folder is not
writable.**

### Copy Files Into the Panel

Drag one or more files or folders from your system's file manager (Finder, Windows
Explorer, or your Linux file manager) and drop them onto the File Panel. The items
are **copied** in, leaving the originals in place. This is a quick way to gather
the files you want to work on.

### Move Files Within the Panel

Drag files or folders from one spot in the File Panel and drop them onto a
different folder in the same panel. The items are **moved** to that folder.

### Confirmation and Safeguards

Before it moves or copies anything, GpgFrontend asks you to confirm, showing the
item name (or count) and the destination folder. A few safeguards prevent common
mistakes:

- Dropping items back into their own folder does nothing. The status bar says
  **The source and target folder are the same.**
- A folder can't be moved or copied into itself or one of its own subfolders.
  The status bar says so.
- If an item with the same name already exists in the target folder, a **Copy
  Failed** or **Move Failed** message tells you, and nothing is replaced.

After a successful drop, the panel refreshes, selects the new or moved items, and
shows how many items were handled.

## Work on Many Files at Once (Batch Mode)

By default the File Panel works on one file at a time. Turn on **Batch Mode** to
handle several at once.

1. Click the batch mode button, the segmented icon at the top-right of the
   File Panel toolbar. Its tooltip says **Enable batch mode to select multiple
   files.** Once it is on, the tooltip says **Batch mode is enabled. Multiple
   files can be selected.**
2. Select several files with **Ctrl+Click** or **Shift+Click**.
3. Click **Encrypt**, **Decrypt**, **Sign**, or **Verify**. The action applies to
   every selected file.

Batch Mode is handy when you have many files to process at once.

![][img-5]

![][img-6]

## Encrypt or Decrypt a Whole Folder

GpgFrontend can encrypt and decrypt an entire folder, keeping its structure
intact.

### Encrypt a Folder

When you encrypt a folder, GpgFrontend:

1. Packs it into a single `.tar` archive, combining all files and subfolders.
   GpgFrontend does this itself; you don't need a separate tar program.
2. Encrypts that archive, giving you a `.tar.gpg` (binary) or `.tar.asc` (ASCII)
   file, depending on your output mode.

This works like the `gpg-zip` tool: packing and encrypting in one step. The result
is one file that holds the whole folder, ready to store or send.

### Decrypt a Folder Archive

When you decrypt a `.tar.gpg` or `.tar.asc` file, GpgFrontend:

1. Decrypts it back into the `.tar` archive.
2. Unpacks that archive into a folder in the current directory, restoring the
   original structure.

You don't need to unpack anything by hand.

## File Types and Output Format

### File Extensions

Knowing the file extensions helps you keep track of encrypted and signed files:

- **.asc**: ASCII-armored. A text-friendly format that can hold encrypted data or
  signatures.
- **.gpg**: Binary. Encrypted files, or combined encrypted and signed files.
  Smaller than ASCII.
- **.sig**: Binary signature file, used for signatures only.

### Choose ASCII or Binary Output

GpgFrontend saves files in **binary** by default (since version 2.0.4; older
versions used ASCII). Binary files are smaller. Choose **ASCII** when you need
text-friendly output, for example to paste into an email.

**Change it in Settings:**

1. Open **Settings** and go to the **General** section.
2. Find the option **Use Binary Mode for File Operations**.
3. Check it for binary (`.gpg` / `.sig`), or uncheck it for ASCII (`.asc`).

![][img-7]

**Or toggle it from the File Panel:**

1. In the File Panel toolbar, click the options button. Its tooltip says
   **Create items and choose what the list shows**.
2. Tick **Use ASCII Armor**. You then get `.asc` files instead of `.gpg` or
   `.sig`.

This is a faster way to switch output modes without opening the main settings.

![][img-8]

## Large Files

You can encrypt and decrypt large files with either engine. The rPGP engine
works through a file piece by piece, so the whole file never has to fit in
memory at once.

## If an Operation Is Interrupted

Since v2.2.2, GpgFrontend writes its result to a temporary file first and
only puts it in place once it is complete.

If an operation fails or is interrupted, you get no output file at all, rather
than a half-written one sitting next to your original. Your input file is never
touched either way.

If a file with the output name already exists, GpgFrontend asks before it
continues. The old file is only replaced after the operation succeeds. See
[Encryption Safety](/guides/encryption-safety/).

[img-1]: https://image.cdn.bktus.com/i/2026/10/29/ccec4b1351ea81bf66c53658a0c6a22b921ad271.webp
[img-2]: https://image.cdn.bktus.com/i/2026/10/29/49aedaa898733c25e3c65ed5920093cf0ca55ea9.webp
[img-3]: https://image.cdn.bktus.com/i/2026/10/29/16074973fa6f0f4de56f81a8a6e47b4bc8e33307.webp
[img-4]: https://image.cdn.bktus.com/i/2026/10/29/4f25fbcd3ead4b2441915d222880df2fd54692f3.webp
[img-5]: https://image.cdn.bktus.com/i/2026/10/25/6baa1c0859e26072af0a57125c3731d54e1305e4-0.webp
[img-6]: https://image.cdn.bktus.com/i/2026/10/29/b5c17550ea622d15e2b4e8f8e6e81006e4c1b972.webp
[img-7]: https://image.cdn.bktus.com/i/2026/10/29/6f70391c3516fb17fb789cc81c60095719f87b47.webp
[img-8]: https://image.cdn.bktus.com/i/2026/10/25/313b19d12f97356c3f5471c544dafa0f0588ce17-0.webp
