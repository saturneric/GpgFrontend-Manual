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

To delete something, right-click it and choose **Move to Trash**. GpgFrontend
asks first.

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

Once a file is selected in the File Panel, pick the right key in the **Key
Toolbox** and click the matching toolbar button:

- **Encrypt**: choose the recipient's **public key**, then click **Encrypt**.
- **Decrypt**: make sure your **private key** is in your keyring, then click
  **Decrypt**. You don't need to pick a key; GpgFrontend finds the right one.
- **Sign**: choose your **private key**, then click **Sign**.
- **Verify**: make sure the sender's **public key** is in your keyring, then click
  **Verify**.

GpgFrontend checks your choice of keys before it starts. For example, it tells
you why a key cannot be used to encrypt. See
[Encryption Safety](/guides/encryption-safety/).

![][img-3]

![][img-4]

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

1. Packs it into a single `.tar` archive (using the tar tool), combining all files
   and subfolders.
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

[img-1]: https://image.cdn.bktus.com/i/2025/06/24/2365c709356b1339898043390a1ff7ac232e05f4.webp
[img-2]: https://image.cdn.bktus.com/i/2025/06/24/acb0e681d8f383589727d0012c3842c487033fa1.webp
[img-3]: https://image.cdn.bktus.com/i/2025/06/24/5ed085a7ac16c34a1e6ba46707597e91a93b6ecc.gif
[img-4]: https://image.cdn.bktus.com/i/2025/06/24/3dceea13ad31f488a347f3b0d4b1fb998487f223.gif
[img-5]: https://image.cdn.bktus.com/i/2025/04/09/24a8b950-ff08-2133-0ee2-5003095f1ff7.webp
[img-6]: https://image.cdn.bktus.com/i/2025/06/24/41efb25fd3a691a57c04a0a2ec4b0e651ceb556c.gif
[img-7]: https://image.cdn.bktus.com/i/2025/06/24/40365f1a7b1ac8d24ac8c11c45e77476a465eab7.webp
[img-8]: https://image.cdn.bktus.com/i/2025/04/09/ea2c8b52-2a49-ee18-5897-5cf3d72115a5.webp
