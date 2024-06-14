---
title: Encrypt & Sign File
---

GpgFrontend offers a fast and convenient method for working with files. The
encryption and decryption process for files is nearly identical to that of text,
with the exception that file operations involve binary input and output.

## Using File Browser for Encryption and Decryption

After clicking the **File Browser** button, a system directory selection dialog
will appear. Follow these steps to perform encryption, decryption, and signing
operations:

1. **Open File Browser**:

   - Click the **File Browser** button in the toolbar at the top of the
     interface. This will open a system dialog allowing you to choose a
     directory.

2. **Select Directory**:

   - In the system dialog, navigate to the desired directory and select it. Once
     selected, a new tab named "File Browser" will open in GpgFrontend,
     displaying the contents of the chosen directory.

3. **Select a File**:

   - In the File Browser tab, you will see a list of files and folders within
     the selected directory. Click on the file you want to encrypt, decrypt, or
     sign.

4. **Encrypt the File**:

   - To encrypt a file, first select the file in the File Browser. Then, in the
     **Key Toolbox** on the right, select the public key of the recipient by
     checking the box next to the desired key. Finally, click the **Encrypt**
     button in the toolbar at the top.

5. **Decrypt the File**:

   - To decrypt a file, select the encrypted file in the File Browser. Ensure
     you have the corresponding private key in your keyring. Click the
     **Decrypt** button in the toolbar. If the correct key is available, the
     file will be decrypted.

![File Operations](https://image.cdn.bktus.com/i/2024/06/15/a8d7bf2f-54f6-ccc6-7bdd-8bb0d2ba44af.webp)

By following these steps, you can easily manage file encryption, decryption, and
signing using the GpgFrontend's File Browser feature. This streamlined process
allows you to handle your cryptographic needs directly from the file system
interface.

## File Extension Requirements

GpgFrontend supports different file extensions for various cryptographic
operations. Understanding these extensions helps in properly managing encrypted
and signed files. Here’s a breakdown of the file extensions used:

#### ASCII Format

- **.asc**: Files with the ".asc" extension are in ASCII format. These files
  contain ASCII-armored ciphertext, which is a text representation of the
  encrypted data. ASCII format is typically used for easy sharing via email or
  text editors, as it ensures compatibility with text-based applications.

#### Binary Format

- **.gpg**: Files with the ".gpg" extension are in binary format. Binary
  ciphertext files are more compact than their ASCII counterparts and are
  generally used for more efficient storage and transmission. They cannot be
  viewed directly in text editors, as the content is in a binary format.

#### Combined Content

- **.gpg**: When you use the encryption and signing functions together,
  GpgFrontend generates a file with the ".gpg" extension. This file contains
  both the encrypted content and the signature, ensuring that the recipient can
  verify that the ciphertext originates from you.

To perform decryption and verification operations, you need to use files with
either the ".gpg" or ".asc" extension. These files contain the necessary
ciphertext and signature content required for these operations.

By adhering to these file extension requirements, you can ensure that your
encrypted and signed files are correctly recognized and processed by
GpgFrontend.

### Default Output Mode

Before version 2.0.4, GpgFrontend generated ciphertext files exclusively in
ASCII format. However, beginning with version 2.0.4, GpgFrontend now generates
ciphertext files in binary format by default. This setting can be adjusted in
the program's settings.

### Changing Output Mode

To change the output mode between ASCII and binary formats, follow these steps:

1. **Open Settings**:

   - Navigate to the GnuPG Controller settings within GpgFrontend. This can be
     done by accessing the settings menu from the main interface.

2. **Locate Binary Mode Option**:

   - In the settings interface, under the "General" section, locate the option
     labeled "Use Binary Mode for File Operations".

3. **Toggle Binary Mode**:
   - Check or uncheck this option to switch between binary (gpg) and ASCII (asc)
     output formats. Checking the box will enable binary mode, while unchecking
     it will revert to ASCII format.

By following these steps, you can customize how GpgFrontend handles the format
of ciphertext files according to your preference or needs.

![Locate Binary Mode Option](https://image.cdn.bktus.com/i/2024/06/15/1a82922d-4a68-d315-f388-5571a4d93e8f.webp)
