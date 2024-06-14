---
title: Interface Understanding
sidebar:
  order: 2
---

As a beginner, you're only required to swiftly comprehend a few crucial sections
of the page. The exploration that follows will gradually unveil additional
functionalities. Bear in mind that interfaces may vary across different
versions.

![Interface](https://image.cdn.bktus.com/i/2024/06/15/baf33505-c34f-12c7-d897-a60fc9b5b600.webp)

## Text Editor

The text editing zone allows you the liberty to input any desired text or
establish a new tab through the "New" option in the file menu at the top. Moving
or closing tabs can be done with ease as per your needs.

Numerous operations can be performed on your text using options available in the
Operations Bar at the top of the interface. You can encrypt, decrypt, sign, and
verify text directly from this menu. Additionally, standard shortcuts like
Ctrl+C, Ctrl+V, and Ctrl+S for copy, paste, and save operations, or searching
within the text using Ctrl+F, are supported.

The edited text within the text box is encoded in UTF-8 without any formatting.
This plain text format ensures that no message alteration leads to confusion.
While there are plans to introduce rich text editing in the future, the
specifics are still being deliberated.

### Large Text File Support

GpgFrontend accommodates opening larger files without hindrance, with the
current limit set to 1MB per file. When dealing with relatively large files,
editing of the tab won't be feasible until the entire file is loaded. During
this time, despite not being able to edit the file, you still have the
capability to view it.

It is important to note that opening files larger than 1MB is not supported, as
excessively long text files can cause significant performance issues with the
graphical user interface (GUI). This limitation helps maintain the application's
responsiveness and ensures a smooth user experience.

## Information Board

GpgFrontend presents the outcome of the current tab page operation on the
Information Board, signifying the success or failure of the operation. The
Information Board's text includes supplementary details to assist in
understanding the particulars of your encryption, decryption, signature, and
other operations. Depending on your language settings, the output displayed on
the dashboard may differ.

The Information Board was conceived to provide a comprehensive view of more
information within the same space. However, GpgFrontend plans to incorporate a
graphical interface in the future to augment the user's comprehension of this
information.

### Color Coding

- **Green**: Indicates a successful operation that has been thoroughly verified
  and found devoid of any issues. The appearance of green font color signifies
  an all-clear.
- **Yellow**: Denotes a successful operation with some potential issues detected
  during result testing. The yellow font color serves as a subtle alert for the
  user, necessitating a detailed review of the operation.
- **Red**: Symbolizes an unsuccessful operation or a significant discrepancy in
  the operation's outcome. The red font color acts as a clear warning, demanding
  the user to meticulously inspect the operation's specifics to ensure security.

### Customizable Font Size

Should you find the font size on the information board to be diminutive, you can
easily adjust it under the 'Application' section in the settings. The default
font size is 10, and it can be modified to any value ranging from 9 to 18.

### Dashboard Actions Menu

The dashboard actions menu, located below the Information Board, provides quick
and easy access to essential functions related to the content displayed. It
empowers users to efficiently manage and process large chunks of information for
various purposes.

#### Copy

This function allows users to swiftly capture significant portions of content
from the Information Board for use in other applications. Simply select the
content you need and use this button to copy it to the clipboard.

#### Save File

This operation archives the contents of the Information Board into the file
system in UTF-8 format. Although the resultant output file does not have a
suffix, it is essentially plain text and can be opened with any text editor.

#### Clear

This command promptly purges all content from the Information Board, including
both the displayed contents and statuses. Any new operation, such as encryption
or decryption, will automatically trigger this clearing process, ensuring that
the Information Board always displays the most current and relevant information.

## Key Toolbox

The Key Toolbox on the right side of the interface lists all available keys,
including public and private keys. The columns provide details such as key type,
name, and email address. You can select keys from this list to perform various
operations such as encryption, decryption, signing, and verification.

### Usage

Most Gpg-related operations require specifying a key pair (for tasks like
encryption, decryption, signature, etc.). You can select the checkbox in the
first column of the Key Toolbox's table to designate one or more keys for your
operation. Categories that contain only public keys are frequently utilized in
cryptographic scenarios.

### Classification

The Toolbox showcases categories via tabbed display. None of these categories
include any expired or revoked keys. To view such keys, you should refer to the
Key Manager. The default category comprises all private and public keys. During
any operation, only the keys from the currently selected category will be
considered for input.

### Columns

Understanding this list is crucial. Let's walk through its components step by
step.

- **Select**: Check the box in this column to notify GpgFrontend that you wish
  to use the key from this row for your subsequent operation.

- **Type**: This column informs you about the key type and whether the primary
  key exists in your key pair.

  - `pub` signifies that it is a public key, which can be used for encryption or
    verification operations.
  - `pub/sec` indicates that the key pair contains both public and private keys.
    It can be employed for nearly all operations (consult the 'Usage' column to
    confirm this).
  - `pub/sec#` shows that the key pair has a public key and a private key, but
    the primary key is absent from the key pair. This suggests you won't be able
    to perform certain specific operations (like adding subkeys, signing other
    key pairs, etc.)
  - `pub/sec^` implies that one or more keys (subkeys or master keys) from the
    key pair are in the smart card.
  - `pub/sec#^` denotes a simultaneous occurrence of the previous two
    situations.

- **Name**: Represents the identity information of the key pair.
- **Email Address**: Also denotes the identity information of the key pair.
- **Usage**: Determines which operations the key pair can execute. Composed of
  four uppercase letters, each letter signifies a specific use.

  - `C` stands for Certificate. Key pairs containing the primary key generally
    have this usage.
  - `E` stands for Encrypt. The key pair can be used for encryption operations.
  - `S` stands for Sign. The key pair can be used for signing operations.
  - `A` stands for Authenticate. The key pair can be used to perform operations
    like SSH authentication.

- **Validity**: A Gpg concept that roughly represents the level of trust in this
  key.

## Operations Bar

The Operations Bar at the top includes the following functions:

1. New: Create a new text file tab.
2. Open: Open an existing text file.
3. File Browser: Browse and select files from your system.
4. Encrypt: Encrypt the text or file.
5. Encrypt Sign: Encrypt and sign the text or file.
6. Decrypt: Decrypt the text or file.
7. Decrypt Verify: Decrypt and verify the text or file.
8. Sign: Sign the text or file.
9. Verify: Verify the signature of the text or file.
10. Manage Keys: Open the key management interface.
11. Import Key: Import a new key through some approaches.

This interface provides a comprehensive suite of tools for managing and
utilizing your cryptographic keys and performing various encryption-related
operations with ease.

### Customization

For operations that you may not use for a while, you have the option to uncheck
the associated function group in the top menu view. Conversely, for the
operations you frequently use, you have the ability to add them here.
