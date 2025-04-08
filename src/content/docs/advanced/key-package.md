---
title: KeyPackage Functionality
sidebar:
  label: KeyPackage
---

## Overview

The KeyPackage is a feature designed to securely package and transfer key data
between different devices. It encapsulates both the public and private keys of
multiple key pairs, ensuring that users can maintain cryptographic functionality
across various platforms. This document outlines the process of creating,
exporting, and safely transferring a KeyPackage.

## Creating a KeyPackage

To create a KeyPackage, follow these steps:

1. **Open the Key Management Interface**: Navigate to the main interface where
   you manage your keys.

2. **Export Keys**: Click on the "Export Key" button to initiate the export
   process.

3. **Choose KeyPackage Export**: Select the option to export keys as a
   KeyPackage. This will open a new dialog box for configuring the KeyPackage.

4. **Configure KeyPackage**:

   - **KeyPackage Name**: In the first field, you will see a generated name for
     the KeyPackage, such as `KeyPackage_41132`. You can click the button
     labeled "Generate Key Package Name" to generate a new name if desired.
   - **Output Path**: In the second field, click the button labeled "Select
     Output Path" to choose where to save the KeyPackage file.
   - **Passphrase**: In the third field, click the button labeled "Generate and
     Save Passphrase" to generate and save a passphrase for the KeyPackage.
     Ensure the security of this passphrase.

5. **Optional Settings**:

   - **Include Secret Keys**: Check the box labeled "Include secret key (Think
     twice before acting)" if you want to include private keys in the
     KeyPackage. This is generally not recommended unless necessary.
   - **Exclude Keys without Private Parts**: Check the box labeled "Exclude keys
     that do not have a private key" to exclude keys that do not have associated
     private keys.

6. **Export**: Once all settings are configured and reviewed, click the "OK"
   button to create and export the KeyPackage.

By following these steps, you can create a secure KeyPackage to transfer your
cryptographic keys between devices. Ensure that the generated passphrase and the
KeyPackage file are stored securely to prevent unauthorized access.

## Security Notice

When the KeyPackage is successfully created, a message will inform you that the
package is protected with encryption algorithms (e.g., AES-256-ECB) and is safe
to transfer. However, it emphasizes that the key file must not be disclosed
under any circumstances. Users are advised to delete the KeyPackage file and the
key file as soon as possible after the transfer is complete.

## Transferring the KeyPackage

To transfer the KeyPackage:

1. Use a secure transfer method to move the `.gpgpack` file to the target
   device. This could be through a secured network connection, encrypted email,
   or a physical device like a USB drive, which should be encrypted as well.
2. Once transferred, import the KeyPackage into the key management tool on the
   target device using the passphrase set during the creation process.

## After Transfer: Importing

To import the KeyPackage after transferring it to the target device, follow
these steps:

![Importing KeyPackage](https://image.cdn.bktus.com/i/2024/06/15/a086df66-bdac-74fb-9a2c-35cddd224564.webp)

1. **Initiate Import**:

   - Open the key management tool on the target device and click on the "Import
     Key" button.

2. **Select KeyPackage Option:**

   - As shown in the image, from the dropdown menu, select the "Key Package"
     option. This indicates that you will be importing a KeyPackage.

3. **Select KeyPackage File**:

   - A file selection dialog will appear. First, choose the `.gpgpack` file that
     you transferred. This file contains the packaged keys.

4. **Select Key File**:

   - After selecting the `.gpgpack` file, another file selection dialog will
     prompt you to choose the corresponding key file. This key file is used to
     decrypt the KeyPackage.

5. **Import Keys**:
   - Once both files are selected, the key management tool will automatically
     import the keys contained within the KeyPackage. You will be prompted to
     enter the passphrase that was set during the creation of the KeyPackage to
     complete the import process.

By following these steps, you can securely import your cryptographic keys from
the KeyPackage into the key management tool on the target device.

## Best Practices

- Always ensure that you are transferring key data over a secure channel.
- Keep the passphrase strong and confidential.
- Delete the KeyPackage files from all devices and any intermediaries (like
  email servers or cloud storage) after the transfer is complete to prevent
  unauthorized access.
