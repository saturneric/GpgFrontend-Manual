---
title: View Key Pair Details
sidebar:
  label: Key Pair Details
---

You can view the details of a key pair by right-clicking on the key pair in the
key toolbox or key management interface and selecting "Show key details".

This section may include a brief introduction to gpg-related concepts and could
be relatively long.

Here is a randomly generated private key. The most significant difference
between this and the previous key is that the key pair with only the public key
is used for encryption only, but if you possess the private key, you can perform
more actions (it also depends on your algorithm; DSA can only be used for
signatures).

![View Key Pair Details 1](https://image.cdn.bktus.com/i/2024/06/15/9f5b0089-923f-33e1-d2cd-f7690ec2d050.webp)

## General Info

This interface provides some useful information to help you manage your key pair
properly.

### Owner

This section enables you to know the owner of this key pair. This information is
not fixed and can be changed. You can create a new UID in the UID section and
set it as the primary UID to change it.

According to the OpenPGP protocol, this part is divided into Name, Email, and
Comment.

![View Key Pair Details Owner](https://image.cdn.bktus.com/i/2024/06/15/30066ecc-ec79-ee27-a3ed-5faad0e6934f.webp)

### Primary Key

This part is the information of the primary key of the key pair. The primary key
is very crucial because without it, you cannot perform related management
operations like adding and revoking sub-keys (similar to not being able to open
the key ring). Let's introduce the information of the primary key separately
below. If you want to learn more, see the [Basic Concepts](../basic-concepts.md)
section.

The absence of the master key means that the private key of the master key does
not exist, but this doesn't mean that neither the public key nor the private key
exists. Please remember: Each subkey and primary key consist of a pair of public
and private keys.

![View Key Pair Details Primary Key](https://image.cdn.bktus.com/i/2024/06/15/8cd3691e-70dc-1239-5f80-9a89f1d342ba.webp)

#### Key ID

This is the unique identifier of the key, which is fixed and unchanging. Note
that this key ID is the key ID of the primary key. The key ID is uniquely
determined after the key is generated. Compared with the fingerprint, the key ID
is shorter and more user-friendly.

#### Algorithm

This refers to the algorithm used for key generation. This also pertains to the
generation algorithm of the primary key. The generation algorithm determines the
properties and capabilities of the key. Algorithms such as RSA can be used for
both encryption and signatures, whereas DSA can only be used for signatures.
More modern algorithms like ECDH (Elliptic-curve Diffie-Hellman) are used for
secure key exchange, and ECDSA (Elliptic Curve Digital Signature Algorithm) is
employed for digital signatures. These elliptic curve algorithms offer enhanced
security with shorter key lengths compared to traditional algorithms.

### Algorithm Detail

Algorithm Detail displays both the key type and the key length. In some cases,
the key algorithm shown here is more precise. For example, it can specify
particular algorithms such as ED25519 or NISTP256, providing detailed
information about the specific cryptographic methods employed.

![Algorithm Detail](https://image.cdn.bktus.com/i/2024/06/15/1e2fba1d-5d5a-738c-a51f-6a3732f6e296.webp)

#### Key Size

This is the length of the primary key. Generally, the longer the key, the harder
it is to crack the ciphertext. But at the same time, it takes more time for a
single operation. Generally speaking, a length of 2048 bits is safe enough (this
refers to the key generated using the RSA algorithm).

#### Normal Usage

This refers to what the key pair can conceptually be used for, including the
conceptual usage of the primary key and sub-key. When the primary key or subkey
generation can be used to sign, but it has already expired or does not exist,
the signature usage will still be displayed here.

#### Actual Usage

This is the actual usage of the primary key and all subkeys, which is the union
of their usage. If there is only one primary key in the key pair that can be
used for signing, but this primary key does not exist, then the signature usage
will not appear here, only in Normal Usage. In addition, when there is only one
subkey that can be used for signing, if it has expired, the signature purpose
will not be displayed here.

#### Expires on

This is the expiration time of the primary key. When the primary key expires, it
will become invalid and you can't use it for any operation. In addition, the
subkeys in the key pair will also be unavailable. Fortunately, you can change
the expiration time of the primary key at any time, or even set it to never
expire. The prerequisite for this is that the primary key exists in the key
pair.

#### Last Update

This is the time when the content of the key pair was last updated. Operations
such as adding a UID or subkey will modify the content of the key pair.

#### Secret Key Existence

This indicates whether the actual content of the primary key exists. When the
primary key does not exist, if there are still available subkeys in the key
pair, the key pair can still be used for normal operations. However, in the
above case, the content of the key pair cannot be modified (that is, operations
such as adding UID or subkey cannot be performed), and the key pair cannot sign
other key pairs.

### Fingerprint

![View Key Pair Details Fingerprint](https://image.cdn.bktus.com/i/2024/06/15/e3250448-a947-a583-eea9-464847e9da32.webp)

The fingerprint of the key pair is used for humans to quickly compare whether
the key pair is the expected key pair. This field is unique for all keys in the
world. You can certainly do this with the key ID mentioned above.

This also refers to the fingerprint of the primary key.

## UID Info

User ID (UID) is used to identify a key, mainly for human identification. It's
similar to a name tag that accompanies a key ring, indicating who the key ring
belongs to. By looking at the UID, users can get a rough idea of whether a key
pair is what they expected. However, for accurate identification, fingerprints
or key IDs should be compared. A key can have multiple UIDs, but a key pair can
only have one primary UID, which is always listed first in the interface.

![View Key Pair Details UID](https://image.cdn.bktus.com/i/2024/06/15/b502d2b6-db02-7d52-f82f-8e4c2e056276.webp)

UID has three elements: Name, Email, Comment. The name should be at least five
characters long, and the email should conform to the format. The rules for
comments are relatively loose.

### Signature of UID

The lower section of the interface displays the signature of the selected User
ID (UID), not the checked one. This is a key trust system. When someone receives
your public key, they can use their private key to sign your nameplate,
indicating their recognition of your public key. Afterward, they can upload the
keyring with their signature to the keyserver. If many people do the same, the
public key on the keyserver will have numerous signatures, making it
trustworthy.

![Signatures of UID](https://image.cdn.bktus.com/i/2024/06/15/81d4f9bd-5c4e-ad22-25dc-f5a4a0c3d9af.webp)

You can also use the primary key of another key pair to sign a UID. Generally, a
primary UID of a key pair with many valid signatures is considered more
trustworthy.

As shown in the image, some signatures do not have the signer's UID identified.
If you need to identify these signatures, you can try importing the
corresponding key from other sources, such as key servers. The Key ID is already
provided, which can help you locate and import the necessary keys to recognize
the signer's UID.

## Subkey Info

The sub-key mechanism is a crucial feature of GPG that improves both flexibility
and security. However, it also introduces some complexity, which can be
challenging for beginners. For a basic understanding, consider the following
points:

- A key pair can be likened to a key ring, comprising a primary key (a pair of
  public and private keys) and multiple subkeys (or none).
- Each subkey and primary key consists of a pair of public and private keys.
- The subkey can perform related operations (such as signing, encryption) in the
  absence or unavailability of the primary key.
- The functions of subkeys can overlap, and when both subkeys can be used for
  signing, the earlier one is selected.
- Subkeys can use more algorithms than the primary key, but usually have the
  same effect on daily operations.
- The disclosure of a subkey only affects that subkey, while the disclosure of
  the primary key endangers the entire key pair.

![Subkeys Details](https://image.cdn.bktus.com/i/2024/06/15/49283a38-47ec-4ff3-5c84-8167a97ab68e.webp)

The primary key and all subkeys in the key pair are displayed on the interface.
Some information about the key is also listed below.

### Key In smart card

Whether a key is in the smart card refers to whether the key is moved to the
smart card. Moving the key to the smart card changes the structure of the key
and is irreversible.

### Operations

In this column, what you can do differs for a key pair that only has a public
key and a key pair that includes a private key.

### Operations on a Public Key

This interface provides various general operations that can be performed on the
selected public key. Below is an explanation of each button's function:

![View Key Pair Details Operations](https://image.cdn.bktus.com/i/2024/06/15/5748a38d-7804-2cca-ecff-bdbfc186290f.webp)

1. **Export Public Key**:

   - **Function**: This button allows you to export the public key to a file.
     Exporting a public key is useful when you need to share it with others or
     upload it to a keyserver. The exported file can then be distributed or
     backed up as needed.

2. **Key Server Operation (Pubkey)**:

   - **Function**: This dropdown menu provides options for interacting with
     keyservers. A keyserver is a repository where public keys are stored and
     can be retrieved by others. The operations might include uploading your
     public key to a keyserver, refreshing your public key with updates from the
     keyserver, or searching for other public keys on the keyserver.

3. **Set Owner Trust Level**:
   - **Function**: This button allows you to set the trust level for the owner
     of the public key. Trust levels are part of the web of trust model used in
     public key infrastructures. By setting the trust level, you indicate how
     much you trust the key owner to correctly verify and sign other keys. This
     affects how your system evaluates the validity of signatures made by the
     key owner.

These operations facilitate the management and sharing of public keys, helping
to establish and maintain trust within a cryptographic system.

### Operations on a Private Key

This interface provides various general operations that can be performed on the
selected key pair, including both public and private key operations. Below is an
explanation of each button's function:

![View Key Pair Details Operations 1](https://image.cdn.bktus.com/i/2024/06/15/68cb4069-5db5-6057-c122-9b9dc2a862f1.webp)

1. **Export Public Key**:

   - **Function**: This button allows you to export the public key to a file.
     This is useful for sharing your public key with others or for uploading it
     to a keyserver. The exported file can be distributed or backed up as
     needed.

2. **Export Private Key**:

   - **Function**: This button provides options for exporting the private key.
     There are typically two modes for exporting:
     - **Export Complete Private Key**: This exports the entire private key,
       including all associated information. It is used when you need a full
       backup or when transferring the key to another system.
     - **Export Minimal Private Key**: This exports only the essential
       components of the private key, minimizing the amount of data. This can be
       useful for more secure key transfers or for environments with specific
       security requirements.

3. **Modify Expiration Datetime (Primary Key)**:

   - **Function**: This button allows you to modify the expiration date and time
     of the primary key. This is important for managing the key's lifecycle and
     ensuring that it remains valid for the desired period. Adjusting the
     expiration date can help maintain security by ensuring keys are
     periodically reviewed and updated.

4. **Modify Password**:

   - **Function**: This button enables you to change the password that protects
     the private key. Changing the password can enhance security, especially if
     you suspect that the current password may have been compromised or if you
     want to follow best practices for regular password updates.

5. **Key Server Operation (Pubkey)**:

   - **Function**: This dropdown menu provides options for interacting with
     keyservers using the public key. Operations might include uploading the
     public key to a keyserver, or refreshing the key from the keyserver.
     Keyservers facilitate the distribution and retrieval of public keys.

6. **Revoke Certificate Operation**:
   - **Function**: This dropdown menu provides options for revoking a key
     certificate. Revoking a certificate is necessary if the key has been
     compromised or if it is no longer needed. This action invalidates the key,
     ensuring it cannot be used maliciously. The revocation information is
     typically uploaded to a keyserver so that others are aware of the key's
     revoked status.

These operations help manage the lifecycle of key pairs, ensuring their secure
use and proper distribution.
