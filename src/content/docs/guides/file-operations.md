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

1. In the main window, click **Open** and choose **Open File** or **Open
   Directory**.
2. Pick the file or folder you want.
3. The File Panel opens. If you picked a file, it is highlighted and ready. If you
   picked a folder, you see its contents and can choose files inside.

![][img-1]

**Using the File Panel button:**

1. Click the **File Panel** button in the top toolbar.
2. Choose a folder in the dialog.
3. A new **File Panel** tab opens showing that folder. Click the file you want.

![][img-2]

## Getting Around the File Panel

The **path bar** across the top shows the folder you are in, one step at a
time. Click any step to jump straight to it. There is a **Home** step at the
start.

To type a path instead, click the edit button at the end of the path bar, or
press **Ctrl+L**. You can use `~` for your home folder.

The rest of the toolbar gives you:

- **Up**: go to the folder above. **Backspace** does the same.
- **Refresh**: read the folder from disk again.
- **Volumes**: jump to a USB drive or another mounted disk.
- **Show**: choose what the list shows, and make a new folder or file.
- **Filter**: type here to show only files whose name contains that text.

Along the bottom you can see how many items are in the folder, how many you
have selected, and how much space is left on the disk.

To delete something, right-click it and choose **Move to Trash**. GpgFrontend
asks first.

## Encrypt, Decrypt, Sign, or Verify a File

Once a file is selected in the File Panel, pick the right key in the **Key
Toolbox** and click the matching toolbar button:

- **Encrypt**: choose the recipient's **public key**, then click **Encrypt**.
- **Decrypt**: make sure your **private key** is in your keyring, then click
  **Decrypt**. You don't need to pick a key; GpgFrontend finds the right one.
- **Sign**: choose your **private key**, then click **Sign**.
- **Verify**: make sure the sender's **public key** is in your keyring, then click
  **Verify**.

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

The target folder must be writable. If it is not, the drop is rejected and a
message explains why.

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

- Dropping items back into their own folder does nothing.
- A folder can't be moved or copied into itself or one of its own subfolders.
- If an item with the same name already exists in the target folder, that item is
  skipped and you are told.

After a successful drop, the panel refreshes, selects the new or moved items, and
shows how many items were handled.

## Work on Many Files at Once (Batch Mode)

By default the File Panel works on one file at a time. Turn on **Batch Mode** to
handle several at once.

1. Click **Switch Batch Mode**, the segmented icon at the top-right of the File
   Panel toolbar. (Hover over it to see the "Switch Batch Mode" tooltip.)
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

1. In the File Panel toolbar, open the **Show** menu.
2. Tick **Use ASCII Armor**. You then get `.asc` files instead of `.gpg` or
   `.sig`.

This is a faster way to switch output modes without opening the main settings.

![][img-8]

## If an Operation Is Interrupted

Since v2.2.2, GpgFrontend writes its result to a temporary file first and
only puts it in place once it is complete.

If an operation fails or is interrupted, you get no output file at all, rather
than a half-written one sitting next to your original. Your input file is never
touched either way.

[img-1]: https://image.cdn.bktus.com/i/2025/06/24/2365c709356b1339898043390a1ff7ac232e05f4.webp
[img-2]: https://image.cdn.bktus.com/i/2025/06/24/acb0e681d8f383589727d0012c3842c487033fa1.webp
[img-3]: https://image.cdn.bktus.com/i/2025/06/24/5ed085a7ac16c34a1e6ba46707597e91a93b6ecc.gif
[img-4]: https://image.cdn.bktus.com/i/2025/06/24/3dceea13ad31f488a347f3b0d4b1fb998487f223.gif
[img-5]: https://image.cdn.bktus.com/i/2025/04/09/24a8b950-ff08-2133-0ee2-5003095f1ff7.webp
[img-6]: https://image.cdn.bktus.com/i/2025/06/24/41efb25fd3a691a57c04a0a2ec4b0e651ceb556c.gif
[img-7]: https://image.cdn.bktus.com/i/2025/06/24/40365f1a7b1ac8d24ac8c11c45e77476a465eab7.webp
[img-8]: https://image.cdn.bktus.com/i/2025/04/09/ea2c8b52-2a49-ee18-5897-5cf3d72115a5.webp
