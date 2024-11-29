---
title: Generate Key Pair
sidebar:
  order: 3
---

GpgFrontend makes it easy to generate a key pair or a subkey for encryption,
signing, and authentication. Follow the steps below to create your own keys.

## Steps to Generate a Key Pair

![Generate A Key Pair](https://image.cdn.bktus.com/i/2024/06/15/5df15149-1890-2645-8452-e7c4798ccd16.webp)

1. **Open Key Management**:

   - Click on the "New Keypair" button in the Key Management interface. This
     will open the Generate Key dialog box.

2. **Fill in Basic Information**:

   - **Name**: Enter your name. The name should be at least 5 characters long.
   - **Email Address**: Enter your email address. It should follow the correct
     email format.
   - **Comment**: Optionally, add a comment to help differentiate this key pair
     from others.

3. **Set Expiration Date**:

   - Choose an expiration date for the key pair. By default, GpgFrontend
     suggests setting the expiration date to two years after generation.
   - Alternatively, you can check the "Never expire" checkbox to make the key
     pair permanent. This option can be changed later, even after the key has
     expired.

4. **Select Key Size and Type**:

   - **Key Size**: Choose the key size. The default size is 2048 bits. Note that
     the size option is only applicable when the key type is RSA or DSA.
   - **Key Type**: Select the type of key you want to generate. Available
     options include RSA, DSA, ECDSA, ECDSA + ECDH, ECDSA + ECDH NIST P-256, and
     ECDSA + ECDH BrainPool P-256. For key types with a plus sign (e.g., ECDSA +
     ECDH), a primary key and a corresponding subkey will be generated.

5. **Set a Passphrase**:

   - It is crucial to set a passphrase to protect your private key. Uncheck the
     "Non Pass Phrase" checkbox and enter a strong, unique passphrase.
   - If you prefer not to set a passphrase (not recommended for security
     reasons), you can leave the "Non Pass Phrase" checkbox checked.

6. **Select Key Usage**:

   - Specify the usage for the key pair. Options include:
     - **Encryption**: For encrypting data.
     - **Signing**: For creating digital signatures.
     - **Certification**: For certifying other keys (only for primary keys).
     - **Authentication**: For authentication purposes, such as SSH keys.
   - Note that some usages may not be available depending on the selected key
     type. For example, the DSA algorithm does not support encryption.

7. **Generate the Key Pair**:
   - After filling in all the necessary information and selecting the desired
     options, click the "OK" button to generate your key pair.

By following these steps, you can generate a secure key pair using GpgFrontend,
tailored to your specific needs for encryption, signing, and authentication.

## Primary Key Supported Algorithms

- RSA
- DSA
- ECDSA ED25519
- EdDSA ED448 (GnuPG >2.3.0)
- ECDSA SECP256K1 (GnuPG >2.3.0)
- ECDSA NIST P-256
- ECDSA NIST P-384
- ECDSA NIST P-521
- ECDSA BrainPool P-256 (GnuPG >2.3.0)
- ECDSA BrainPool P-384 (GnuPG >2.3.0)
- ECDSA BrainPool P-512 (GnuPG >2.3.0)
