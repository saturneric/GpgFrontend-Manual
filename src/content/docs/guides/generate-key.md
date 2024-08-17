---
title: Generate Key Pair & Subkey
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

## Steps to Generate a Subkey

![Generate A Subkey](https://image.cdn.bktus.com/i/2024/06/15/a56c83bc-72ad-6232-1764-6fef5aeceddd.webp)

1. **Open Key Management**:

   - In the Key Management interface, right-click on the key pair you wish to
     add a subkey to. Select the "New Subkey" option from the context menu.

2. **Fill in Basic Information**:

   - **Key Type**: Select the type of subkey you want to generate. Available
     options include RSA, DSA, ECDSA, ECDH, ECDH NIST P-256, ECDH NIST P-384,
     ECDH NIST P-521, ECDH BrainPool P-256, ECDH BrainPool P-384, and ECDH
     BrainPool P-512.
   - **Key Size**: Choose the key size. This option is only applicable when the
     key type is RSA or DSA.
   - **Expiration Date**: Set an expiration date for the subkey. You can also
     choose to check the "Never expire" checkbox to make the subkey permanent.

3. **Set a Passphrase**:

   - If the primary key has a passphrase, the subkey's passphrase must be equal
     to it. Ensure that the "Non Pass Phrase" checkbox is unchecked if you want
     to set a passphrase.

4. **Select Key Usage**:

   - Specify the usage for the subkey. Options include:
     - **Encryption**: For encrypting data.
     - **Signing**: For creating digital signatures.
     - **Authentication**: For authentication purposes, such as SSH keys.
   - Note that the certification usage is not available for subkeys.

5. **Generate the Subkey**:
   - After filling in all the necessary information and selecting the desired
     options, click the "OK" button to generate your subkey.

By following these steps, you can generate a subkey using GpgFrontend, which
enhances the functionality of your primary key pair for various cryptographic
operations.

## Extra Note

Below are some guidelines that may prove useful in comprehending the
aforementioned concepts and utilizing this tool accurately.

#### Understanding Primary Keys and Subkeys

In the realm of cryptography, key management plays a crucial role in ensuring
data security. A key pair consists of a primary key and one or more subkeys,
each serving distinct functions yet working together to secure and manage
digital identities and communications. This structure not only enhances security
but also provides flexibility in key usage and management.

#### The Role of Primary Key and Subkeys

- **Primary Key**: The primary key is the cornerstone of your cryptographic
  identity. It is used for identity verification, which includes signing other
  keys to establish trust. The primary key's signature on a subkey validates the
  subkey's association with the identity of the primary key holder.

- **Subkeys**: Subkeys are associated with the primary key and are used for
  encryption and signing documents or messages. Subkeys can be thought of as
  extensions of the primary key, each designated for specific tasks. This
  separation of duties allows for greater security and operational flexibility.
  For example, you can have separate subkeys for signing and encryption.

#### Advantages of Using Subkeys

1. **Enhanced Security**: By using subkeys for day-to-day operations, you
   minimize the risk associated with key exposure. If a subkey is compromised,
   it can be revoked without affecting the primary key or other subkeys, thereby
   limiting the potential damage.

2. **Operational Flexibility**: Subkeys allow for specific roles (e.g., signing,
   encryption) to be isolated. This means you can renew or revoke subkeys as
   needed without disrupting the overall cryptographic setup.

3. **Convenient Key Rotation**: Regularly updating keys is a best practice in
   cryptography. Subkeys make it easier to rotate keys for signing and
   encryption without needing to re-establish the primary key's trust
   relationships.

#### Managing Primary Keys and Subkeys

- **Secure Storage**: The primary key should be stored in a highly secure
  location, preferably offline or in a hardware security module (HSM), to
  prevent unauthorized access. The loss or compromise of the primary key
  jeopardizes the entire cryptographic framework.

- **Key Generation and Maintenance**: While tools like GpgFrontend provide
  user-friendly interfaces for managing keys, they may lack support for advanced
  operations like generating multiple subkeys. Therefore, using the command-line
  `gpg` tool for such tasks is advisable. Despite this limitation, GpgFrontend
  can play a critical role in monitoring the presence of the primary key, which
  is essential for certain operations like adding subkeys or signing other keys.

- **Revocation and Renewal**: Prepare revocation certificates for your primary
  key and subkeys in advance. In case of key compromise or expiration, these
  certificates allow you to invalidate the keys, informing others in your trust
  network not to use them anymore.

#### Practical Tips for Effective Key Management

- **Purpose-Specific Subkeys**: If your primary key was not generated with
  certain capabilities (e.g., encryption), you can create a subkey with the
  required functionality. This allows the key pair to be used for the intended
  cryptographic operations without regenerating the primary key.

- **Multiple Subkeys for Different Devices**: For users operating across
  multiple devices, generating separate subkeys for each device can enhance
  security. If one device is compromised, only the subkey on that device needs
  to be revoked, leaving the others unaffected.

- **Backup and Recovery**: Regularly back up your key pair, including the
  primary key and all subkeys. Secure backups ensure that you can recover your
  cryptographic capabilities even in the event of hardware failure or data loss.

In summary, understanding and implementing a robust key management strategy,
with a clear distinction between primary keys and subkeys, is essential for
maintaining the integrity and security of cryptographic operations. By adhering
to best practices for key usage, storage, and renewal, users can safeguard their
digital identities and ensure the confidentiality and authenticity of their
communications.

#### Additional Note on Subkey Algorithm Types

Subkeys in GpgFrontend offer more algorithm types than primary keys due to their
specialized roles. While primary keys focus on establishing identity and trust,
subkeys are often dedicated to specific tasks like encryption or authentication.
This task-specific design allows subkeys to utilize a broader range of
algorithms, enhancing their flexibility and functionality. For instance, while
primary keys may be restricted to certain secure algorithms for signing, subkeys
can employ diverse algorithms optimized for encryption, like ECDH, ensuring
efficient and secure operations tailored to the user's needs.

**Primary Key Supported Algorithms:**

- RSA
- DSA
- ECDSA ED25519
- ECDSA NIST P-256
- ECDSA NIST P-384
- ECDSA NIST P-521
- ECDSA BrainPool P-256 (GnuPG >2.3.0)
- ECDSA BrainPool P-384 (GnuPG >2.3.0)
- ECDSA BrainPool P-512 (GnuPG >2.3.0)

**Subkey Supported Algorithms:**

- RSA
- DSA
- ELG-E
- ECDSA ED25519
- ECDSA ED448 (GnuPG >2.3.0)
- ECDH CV25519
- ECDH X448 (GnuPG >2.3.0)
- ECDH NIST P-256
- ECDH NIST P-384
- ECDH NIST P-521
- ECDH BrainPool P-256 (GnuPG >2.3.0)
- ECDH BrainPool P-384 (GnuPG >2.3.0)
- ECDH BrainPool P-512 (GnuPG >2.3.0)

**Explanation:**

The broader range of algorithms available for subkeys arises because subkeys are
designed for specific functions and can therefore leverage specialized
algorithms optimized for those functions. For example, ECDH (Elliptic Curve
Diffie-Hellman) is highly efficient for encryption tasks and is commonly used
for subkeys dedicated to encryption. This flexibility in algorithm choice
ensures that cryptographic operations can be optimized for both performance and
security based on the specific use case.

Primary keys, however, are central to the user's cryptographic identity and are
primarily used for signing and certifying subkeys. This critical role
necessitates the use of well-established and highly secure algorithms to ensure
the integrity and trustworthiness of the entire cryptographic system.

By differentiating the algorithms and roles of primary keys and subkeys,
GpgFrontend enhances both security and operational efficiency, allowing users to
maintain a robust and flexible cryptographic setup​.
