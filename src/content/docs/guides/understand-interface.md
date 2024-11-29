---
title: Interface Understanding
sidebar:
  order: 2
---

This documentation explains the interface and functionality of GpgFrontend,
based on the latest UI design. It is intended to guide users through its
features effectively.

![Interface](https://image.cdn.bktus.com/i/2024/11/29/0b427894-0706-70fd-cd68-634d57655df4.webp)

## Text Editing Zone

The **Text Editing Zone** allows users to input any desired text or work on
existing files. You can open a new tab using the **"New"** or **"New E-Mail"**
button or load an existing file with **"Open"** from the menu bar.

### Key Features:

- **Operations Bar**: Located at the top, it provides options to encrypt,
  decrypt, sign, and verify text directly.
- **Standard Shortcuts**: Supports basic shortcuts like **Ctrl+C**, **Ctrl+V**,
  and **Ctrl+S** for copying, pasting, and saving text.
- **Plain Text Format**: Text is encoded in UTF-8 without formatting to ensure
  clarity and compatibility. Future plans may include rich text editing.

#### Large Text File Support

- Files up to **1MB** are supported. Larger files may cause performance issues
  and are not recommended.
- While loading large files, editing will be temporarily disabled until the
  entire file is processed.

## Information Panel

The **Information Panel** displays the results of current operations (e.g.,
encryption, decryption, signing) and their status, such as success or failure.
It provides helpful details about the operation, such as timestamps, key IDs,
and algorithms used.

### Color Coding for Status

- **Green**: Indicates a successful operation with no issues.
- **Yellow**: Suggests a successful operation but with potential warnings.
- **Red**: Signifies an unsuccessful operation or critical errors.

### Dashboard Actions Menu

- **Copy**: Copies content from the Information Panel to the clipboard.
- **Save File**: Saves the Information Panel's content as a plain text file
  (UTF-8).
- **Clear**: Clears all content from the Information Panel, resetting it for the
  next operation.

## Key Toolbox

The **Key Toolbox**, located on the right side of the interface, lists all
available keys. It provides details such as key type, name, email address, and
usage. Users can select keys for specific operations by ticking the boxes in the
first column.

### Key Details

- **Type**:
  - `pub`: Public key (for encryption or verification).
  - `pub/sec`: Key pair with both public and private keys.
  - `pub/sec#`: Key pair with missing primary key.
  - `pub/sec^`: Key pair with components stored on a smart card.
- **Email Address**: Shows the email associated with each key.
- **Usage**: Indicates key functionality with codes:
  - `C`: Certification.
  - `E`: Encryption.
  - `S`: Signing.
  - `A`: Authentication.

### Categories

The toolbox categorizes keys by type (e.g., public or private) using tabs.
Expired or revoked keys are not displayed by default and can be viewed in
**Manage Keys**.

## Operations Bar

The **Operations Bar**, at the top of the interface, provides quick access to
all core functionalities:

1. **New E-Mail**: Create a new email or text file.
2. **Open**: Open an existing text file.
3. **File Browser**: Browse and select files from your system.
4. **Encrypt**: Encrypt text or files using selected keys.
5. **Encrypt Sign**: Encrypt and sign text or files simultaneously.
6. **Decrypt**: Decrypt text or files.
7. **Decrypt Verify**: Decrypt and verify signed files.
8. **Sign**: Digitally sign text or files.
9. **Verify**: Verify the signature of text or files.
10. **Manage Keys**: Access the key management interface.
11. **Import Key**: Import keys into your keyring.

### Customization

You can hide unused functions or add frequently used ones via the view settings
menu in the application.
