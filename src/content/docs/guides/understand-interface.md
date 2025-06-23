---
title: Interface Understanding
sidebar:
  order: 2
---

This documentation explains the layout and features of the latest GpgFrontend
interface, helping users to efficiently utilize all cryptographic operations in
different workspaces.

![Interface](https://image.cdn.bktus.com/i/2025/06/24/f0121645a9c0d8f0e67b2b9f4d1788bd42c7674a.webp)

## Workspace Overview

GpgFrontend organizes your cryptographic workflow into multiple workspaces
(tabs), making it easy to work with files, plain text, and email data
simultaneously.

There are three main workspace types, each represented by a tab:

- File Panel: For batch file and folder operations.
- Text Editor: For editing and encrypting/decrypting plain text.
- Mail Editor: For handling email messages in a dedicated editor.

You can open multiple tabs of each type and switch between them as needed.

### File Panel

The File Panel is dedicated to cryptographic operations on files and folders. It
allows you to:

- Browse and select files or folders from your system.
- Encrypt, decrypt, sign, or verify one or multiple files.
- Switch between ASCII and binary output modes.
- Activate Batch Mode for multi-file operations.
- Automatically handle folder archiving/encryption (see the File Operations
  section for details).

Files and folders selected via Open are always opened in a File Panel tab.

### Text Editor

The Text Editor allows users to input any desired text or work on existing
files.

#### Key Features

- **Operations Bar**: Located at the top, it provides options to encrypt,
  decrypt, sign, and verify text directly.
- **Standard Shortcuts**: Supports basic shortcuts like **Ctrl+C**, **Ctrl+V**,
  and **Ctrl+S** for copying, pasting, and saving text.
- **Plain Text Format**: Text is encoded in UTF-8 without formatting to ensure
  clarity and compatibility. Future plans may include rich text editing.
- Files up to **1MB** are supported. Larger files may cause performance issues
  and are not recommended.
- While loading large files, editing will be temporarily disabled until the
  entire file is processed.

### Mail Editor

The Mail Editor is specifically designed for working with EML-format email
messages.

- Open and Edit EML Files: Load .eml files (standard email format) directly for
  viewing and editing their content.
- Compose, Encrypt, Sign, and Verify Emails: Easily write or modify email
  content and apply encryption, digital signatures, or verify received
  signatures—all in one place.

:::caution[Note]

The Mail Editor is optimized for .eml files, ensuring compatibility with standard email clients and maintaining proper formatting and metadata during cryptographic operations.

:::

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

Located on the right side, the Key Toolbox lists all your available keys,
including public, private, and key groups.

Key features:

- Selection: Tick boxes to choose keys for current operations.
- Type/Usage/Email: Quickly review each key’s function.
- Tab Filtering: Tabs let you quickly filter keys by type or status.

Keys that are expired, revoked, or unavailable are hidden by default, but can be
managed in the Manage Keys interface.

### Understanding the Key Toolbox Table

The Key Toolbox contains detailed information about each key. Some of the
columns and codes—especially in the Type and Usage columns—may not be
immediately obvious. The section below explains the meaning of these less
obvious—but essential—fields and codes, so you can confidently interpret key
types, usage, and status in your daily cryptographic operations.

- **Type**:
  - `pub`: Public key (for encryption or verification).
  - `pub/sec`: Key pair with both public and private keys.
  - `pub/sec#`: Key pair with missing primary key.
  - `pub/sec^`: Key pair with components stored on a smart card.
  - `group`: Key Group (a collection of public keys used as one recipient for
    encryption).
- **Usage**: Indicates key functionality with codes:
  - `C`: Certification – can certify (sign) other keys (typically primary keys only)
  - `E`: Encryption – can encrypt data to this key
  - `S`: Signing – can create digital signatures
  - `A`: Authentication – can be used for authentication (e.g. SSH)

### Categories

The toolbox categorizes keys by type (e.g., public or private) using tabs.
Expired or revoked keys are not displayed by default and can be viewed in
**Manage Keys**.

## Operations Bar

The Operations Bar at the top provides one-click access to all core
cryptographic and workspace features. Here are the main buttons, from left to
right:

1. **Open**: Open a file or directory, launching the File Panel for file-based
   operations.
2. **Workspace**: Manage and switch between different workspaces or tabs, such
   as File Panel, Text Editor, and Mail Editor.
3. **Encrypt**: Encrypt the currently selected file(s) or text using the
   selected recipient keys.
4. **Decrypt**: Decrypt the currently selected encrypted file(s) or text. No key
   selection is required—gpg automatically detects and uses the
   appropriate private key(s) from your keyring.
5. **Sign**: Digitally sign the selected file(s) or text with your private key.
6. **Verify**: Verify the signature of the selected file(s) or text.
7. **New Keypair**: Generate a new key pair.
8. **Import Key...**: Import existing public or private keys into your keyring.
9. **Manage Keys**: Access the key management interface.

### Customization

You can hide unused functions or add frequently used ones via the view settings
menu in the application.
