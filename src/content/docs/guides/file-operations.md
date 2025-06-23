---
title: File Operations
sidebar:
  order: 6
---

GpgFrontend offers a fast and convenient method for working with files. The
processes of encryption, decryption, signing, and verifying files are similar to
text-based operations but involve binary input and output.

## Using File Panel for Encryption, Decryption, Signing, and Verifying

After clicking the **File Panel** button, a system directory selection dialog
will appear. Follow these steps to perform various cryptographic operations:

1. Open File Panel: Click the **File Panel** button in the toolbar at the top of
   the interface. This will open a system dialog allowing you to choose a
   directory.
2. Select Directory: In the system dialog, navigate to the desired directory and
   select it. Once selected, a new tab named "File Panel" will open in
   GpgFrontend, displaying the contents of the chosen directory.
3. Select a File: In the File Panel tab, click on the file you want to encrypt,
   decrypt, sign, or verify.

### 4. File Operations (Encrypt, Decrypt, Sign, Verify)

Perform various file operations by selecting the desired file in the File Panel
and using the appropriate key from the Key Toolbox:

- Encrypt: Select the desired file in the File Panel. Choose a recipient's
  public key from the Key Toolbox and click the Encrypt button in the toolbar.
- Decrypt: Select the encrypted file in the File Panel. Ensure your private key
  is available in your keyring and click the Decrypt button in the toolbar.
- Sign: Select the desired file in the File Panel. Choose your private key from
  the Key Toolbox and click the Sign button in the toolbar.
- Verify: Select the signed file in the File Panel. Ensure the corresponding
  public key is available in your keyring and click the Verify button in the
  toolbar.

## File Extension Requirements

Understanding the appropriate file extensions helps in managing encrypted and
signed files properly. Here’s a breakdown of the file extensions used:

### ASCII Format

- **.asc**: ASCII-armored files. Can contain encrypted data or signatures in a
  text-compatible format.

### Binary Format

- **.gpg**: Binary encrypted files or combined encrypted and signed files. More
  efficient for storage and transmission.
- **.sig**: Binary signature files used exclusively for signature operations.

## Output Mode

Before version 2.0.4, GpgFrontend generated ciphertext and signature files
exclusively in ASCII format. From version 2.0.4 onwards, it generates files in
binary format by default. This setting can be adjusted in the program's
settings.

### Changing Output Mode

To change the output mode between ASCII and binary formats:

1. Open Settings: Navigate to the GnuPG Controller settings within GpgFrontend by accessing
   the settings menu.
2. Locate Binary Mode Option: In the settings interface, under the "General"
   section, find the option labeled "Use Binary Mode for File Operations".
3. Toggle Binary Mode: Check or uncheck this option to switch between binary
   (gpg/sig) and ASCII (asc) output formats.

This streamlined process allows you to manage file encryption, decryption,
signing, and verification efficiently with GpgFrontend.

### Quick Toggle via File Panel Menu

In addition to the settings menu, GpgFrontend also provides a quick toggle
option for switching between ASCII and binary output modes directly from the
File Panel:

1. Access the File Panel Toolbar: In the File Panel, locate the toolbar at the
   top right.
2. Open the Drop-down Menu: Click the button with the gear icon or three-line
   icon (as shown in the screenshot) to open a drop-down menu.
3. Select ASCII Mode: From the menu, choose “ASCII Mode” to enable ASCII-armored
   output for operations like encryption or signing. When checked, output files
   such as .asc will be generated instead of binary formats like .gpg or .sig.

This feature offers a convenient way to switch output modes without navigating
through the main settings, making file operations faster and more adaptable
based on user needs.

![](https://image.cdn.bktus.com/i/2025/04/09/ea2c8b52-2a49-ee18-5897-5cf3d72115a5.webp)

## Enabling Batch Mode for Multi-file Operations

By default, the File Panel supports only single-file selection for cryptographic
operations. However, GpgFrontend includes a Batch Mode feature that allows users
to select and process multiple files simultaneously:

1. Activate Batch Mode: Click the “Switch Batch Mode” button, represented by a
   segmented icon located at the top-right corner of the File Panel toolbar. A
   tooltip labeled “Switch Batch Mode” will appear when hovering over the
   button.
2. Select Multiple Files: Once Batch Mode is activated, the file panel will
   allow multi-selection using standard keyboard shortcuts (e.g., Ctrl or
   Shift+Click).
3. Perform Bulk Operations: After selecting the desired files, perform
   encryption, decryption, signing, or verification actions using the toolbar
   controls. The operation will be applied to all selected files.

Batch Mode is especially useful for advanced users handling multiple files,
significantly improving operational efficiency in workflows involving large
volumes of data.

![](https://image.cdn.bktus.com/i/2025/04/09/24a8b950-ff08-2133-0ee2-5003095f1ff7.webp)

## Folder Encryption and Decryption

GpgFrontend supports seamless encryption and decryption of entire folders
through the File Panel interface. This feature enables users to securely package
directory contents while preserving their original structure.

### Encrypting Folders

When a folder is selected for encryption, GpgFrontend automatically performs the
following operations:

1. Archiving: The folder is first archived using the tar utility, combining all
   files and subdirectories into a single .tar archive.
2. Encryption: The `.tar` archive is then encrypted using GnuPG, resulting in a
   `.tar.gpg` (binary) or `.tar.asc` (ASCII-armored) file, depending on the
   selected output mode.

This behavior mirrors the functionality of the gpg-zip tool, which combines
archiving and encryption into a single streamlined operation.

Note: The resulting encrypted file represents the entire folder in a secure,
transferable format.

### Decrypting Encrypted Archives

GpgFrontend also offers automatic extraction when decrypting `.tar.gpg` or
`.tar.asc` files:

1. Decryption: The selected encrypted archive is decrypted using GnuPG,
   producing the original `.tar` archive.
2. Extraction: If the decrypted content is a `.tar` archive, GpgFrontend
   automatically extracts its contents into a folder within the current
   directory, restoring the full folder structure.

This automatic process eliminates the need for manual unpacking and ensures that
encrypted folders are fully restored to their original state.
