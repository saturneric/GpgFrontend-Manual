---
title: Generate and Use Subkey(s)
sidebar:
  order: 4
---

GpgFrontend allows users to extend their primary key pairs by generating one or
more subkeys. Subkeys can be used for specific cryptographic purposes, such as
encryption, signing, or authentication, while keeping the primary key more
secure and reserved for certification.

## Generating a Subkey

There are **two entry points** to generate a subkey:

### Method 1: From Key Management

1. Open Key Management
2. Navigate to the main **KeyPair Management** interface.
3. Right-click on the key pair to which you want to add a subkey.
4. Select **“New Subkey”** from the context menu.

![](https://image.cdn.bktus.com/i/2025/04/09/194529c8-4745-a2f1-5b9a-70cb66344243.webp)

### Method 2: From Key Details View

1. Open Key Details
2. Double-click on the desired key pair in the **Key Management** list.
3. Switch to the **Keychain** tab.
4. Click the **“Generate A New Subkey”** button.

![](https://image.cdn.bktus.com/i/2025/06/24/629f4685256b3facbb8c3d6e4e14d9e31bd6f83a.webp)

### Configuring the Subkey

Once the subkey generation dialog appears, configure the following settings:

- **Algorithm**: Choose the algorithm for the subkey. Options include:

  - RSA, DSA
  - ECC (e.g., ED25519, ED448, CV25519, SECP256K1, Brainpool, NIST curves, etc.)
  - ECDH for encryption, EdDSA for signing, etc.

- **Key Size**: Select the desired key size. This setting is available for most
  algorithms, including RSA, DSA, and ECC variants (such as Curve25519,
  Brainpool, or NIST curves). For curve-based algorithms, the key size typically
  corresponds to the selected curve (e.g., ED25519 = 256 bits), while RSA/DSA
  allows configurable sizes like 2048, 3072, or 4096 bits.

- **Expiration Date**: Set how long the subkey remains valid:

  - Predefined periods (e.g., 1 year, 2 years)
  - Exact date/time
  - Or enable **“Non Expired”** for permanent validity.

- **Key Usage**: Choose what the subkey can be used for:
  - `Encrypt`
  - `Sign`
  - `Authenticate`  
    _(Certification usage is reserved for primary keys.)_

### Final Step: Generate

Once all configurations are completed:

- Review your choices in the summary area (if available).
- Click **“Generate”** to create the subkey.
- The new subkey will be listed under the **Keychain** tab of the selected key
  pair.

![](https://image.cdn.bktus.com/i/2025/06/24/a52b9445c4aef48b880ae1fb7d031b6d445b700e.webp)

## Understanding Primary Keys and Subkeys

In the realm of cryptography, key management plays a crucial role in ensuring
data security. A key pair consists of a primary key and one or more subkeys,
each serving distinct functions yet working together to secure and manage
digital identities and communications. This structure not only enhances security
but also provides flexibility in key usage and management.

### The Role of Primary Key and Subkeys

- **Primary Key**: The primary key is the cornerstone of your cryptographic
  identity. It is used for identity verification, which includes signing other
  keys to establish trust. The primary key's signature on a subkey validates the
  subkey's association with the identity of the primary key holder.

- **Subkeys**: Subkeys are associated with the primary key and are used for
  encryption and signing documents or messages. Subkeys can be thought of as
  extensions of the primary key, each designated for specific tasks. This
  separation of duties allows for greater security and operational flexibility.
  For example, you can have separate subkeys for signing and encryption.

### Advantages of Using Subkeys

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

## Best Practices for Using Subkeys

After understanding the concepts discussed above, you might be wondering how
exactly you can effectively use subkeys to maximize their advantages. In
principle, the main goal is to separate the subkey from the primary key to
leverage better security. If your subkeys are always kept together with the
primary key, you will always need to use the complete set of keys, increasing
the risk of compromising the primary key. GpgFrontend supports the export of
individual subkeys, as well as the configuration of multiple key databases.
Using these features together, you can easily isolate a particular subkey,
export it, and import it into another key database. This allows you to secure
the primary key separately, even removing it from the original key database to
reduce exposure. For high-security environments, it is recommended that:

> "The primary key should be stored in a highly secure location, preferably
> offline or in a hardware security module (HSM), to prevent unauthorized
> access. The loss or compromise of the primary key jeopardizes the entire
> cryptographic framework."

### Step-by-Step Guide to Exporting Subkeys

To demonstrate how to export an individual subkey, let's refer to the screenshot
provided. Below is a step-by-step guide to navigate the GpgFrontend interface
and successfully export a subkey:

1. **Open Key Details View**: Open the GpgFrontend application and navigate to
   the key database section. Select the desired key from the list to open the
   **Key Details** view.

2. **Access the Keychain Tab**: Click on the **Keychain** tab within the Key
   Details window. Here, you will be able to see a list of all keys associated
   with your selected primary key. The list includes the primary key itself,
   which is displayed in the first row, as well as any subkeys.

3. **Select a Subkey**: Locate and click on the subkey you wish to export. Once
   selected, details about the subkey will appear in the lower half of the
   window, providing information such as **Key ID**, **Algorithm**, **Key
   Size**, and **Usage**.

4. **Export the Subkey**: On the right side of the key details section, there is
   an **Export Subkey** button, highlighted in the screenshot. Click this button
   to start the export process.

5. **Save the Subkey File**: A file dialog will appear, prompting you to specify
   a location to save the exported subkey. Choose a secure directory and save
   the subkey as a separate file.

![](https://image.cdn.bktus.com/i/2025/06/24/b4f1dc5e6eb6f683300564a4ba998e48d22b75b4.webp)

### Step-by-Step Guide to Importing Subkeys

To demonstrate how to import an individual subkey that has been previously
exported, let's refer to the screenshots provided. Below is a step-by-step guide
to navigate the GpgFrontend interface and successfully import a subkey:

1.  **Select the Key Database**: Choose the appropriate key database from the
    **Key Toolbox**.

![Switch Key Database](https://image.cdn.bktus.com/i/2024/11/29/0e8ff19e-4189-65db-5732-1a2e79d9b8a6.webp)

1. **Import the Subkey**: Click on the **Import Key** button in the top toolbar,
   and select **File** from the dropdown menu. This action will open a dialog
   where you can browse your system to locate the previously exported subkey
   file.

   ![Import the Subkey](https://image.cdn.bktus.com/i/2024/11/29/8f3456ba-6275-4ef9-8e41-49b9b6bc0dfa.webp)

2. **Select Subkey File**: Browse to the location where the subkey file is
   saved, select it, and click **Open**. This will import the subkey into the
   selected key database.

3. **Verify Imported Subkey**: After importing the subkey, locate it in the
   **Key Toolbox** list. Click on the subkey to open its **Key Details** view.
   You should see all relevant information about the subkey, including **Key
   ID**, **Algorithm**, **Key Size**, and **Usage**.

4. **Handling Primary Key**:You can now move your master key to a safe place.
   Then delete it at GpgFrontend.

   ![Verify Imported Subkey](https://image.cdn.bktus.com/i/2024/11/29/ac01142d-1ffa-ba32-daac-36ddf0729ff1.webp)

### Confirming Primary Key Absence

In the **Key Toolbox**, you may notice that some keys have a `#` symbol next to
their **Type** (e.g., **pub/sec#**). This symbol indicates that the primary key
for this subkey does not exist in the current key database. This is expected if
you have securely removed the primary key to minimize exposure, while retaining
the subkeys for ongoing operations.

![Meaning of'#' Symbol](https://image.cdn.bktus.com/i/2024/11/29/78d9bc07-8b96-302b-25d1-cbb88815f16a.webp)

You can confirm the absence of the primary key by opening the **Key Details**
view of the imported subkey. In the **Primary Key Existence** section, it should
indicate **Not Exists**. This ensures that the primary key is not present, which
enhances the overall security of your cryptographic setup.

## Key Functionality Without a Primary Key

When a primary key is absent from the key database, certain limitations apply.
You can confirm the absence of the primary key by checking the **Primary Key
Existence** section in the Key Details view, which will display **Not Exists**.
This setup is intentional in many cases to improve security by isolating the
primary key.

![Primary Key Not Exists](https://image.cdn.bktus.com/i/2024/11/29/05594a4b-cdad-7ad4-070b-58e24701cce3.webp)

### Actions Limited by the Absence of a Primary Key:

1. **Creating New Subkeys**: The absence of the primary key prevents the
   generation of additional subkeys.
2. **Adding UID**: You cannot attach new User IDs (UIDs) to the keyset without
   the primary key.
3. **Key Certification**: Signing other keys to certify them as trusted is only
   possible with a primary key.
4. **Key Revocation**: Generating a revocation certificate for the subkey or
   primary key is impossible without the primary key.

### Practical Example: Subkey-Only Use Case

In scenarios where only the subkey remains, as depicted in the screenshot:

- The subkey can be actively used for encryption purposes (e.g., encrypting
  emails or files).
- Since no subkey capable of signing exists, you cannot digitally sign data. To
  address this, it is advisable to generate a signing-capable subkey during the
  initial key creation process.

This setup is particularly beneficial for environments where the exposure of the
primary key poses a security risk. By isolating the primary key and relying
solely on subkeys, you can maintain a balance between functionality and
security.

![Use Subkey to Encrypt](https://image.cdn.bktus.com/i/2024/11/29/20047766-48ab-f4a3-175c-241c7d5c0dbf.webp)

## Common Misconceptions about Subkey

When you export only a subkey and then import it into a different key database
(or application), you may notice that:

- The key listing still shows the primary key’s ID as the main identifier.
- The keyring still displays the original key structure—including the primary
  key and potentially other subkeys—though only the exported subkey is available
  for actual use (decryption, signing, etc.).
- The usage flags (such as CESA: Certify, Encrypt, Sign, Authenticate) may
  change—only capabilities for which the private part is present remain active.

### Why is this the case?

This is not a bug, but a fundamental part of how OpenPGP and GnuPG represent keys.

### Key Structure: Public Context is Required

Even if you export and import only a subkey’s secret part, you are actually
exporting and importing a full public key structure (a certificate) with only a
partial set of private components.

- The public key block still contains the primary key’s information, all user
  IDs, and all subkey definitions.
- The secret part of the primary key is absent, so you cannot certify, revoke,
  or generate further subkeys.
- The exported file needs to include the primary key’s public information,
  because the subkey’s trust depends on its certification by the primary key.

:::tip[Analogy]

Exporting a subkey is like sending only the content of a letter but still
including the envelope, address, and signature. You need all of these for the
recipient (the application) to know who sent it and to verify its authenticity.

:::

The primary key is the identity anchor for the whole key structure. Subkeys
derive their trust from the fact that the primary key certified them. If the
primary key’s public info and signatures are missing, the subkey would not be
recognized as legitimate or trustworthy by other OpenPGP tools.

### Multiple Subkeys Included

If the key structure contains other subkeys, their definitions will also be
present in the exported key material—even if their secret parts are missing.
This design ensures the integrity and context of the key structure for any
OpenPGP-compliant tool.

### Why is the Key ID Still the Primary Key’s?

OpenPGP keyrings and applications (including GpgFrontend, Thunderbird, etc.)
identify the whole key structure by the primary key ID. This ensures consistency
and interoperability across tools and platforms. It’s not possible to create a
"standalone" subkey that appears as its own identity—the subkey’s value is only
recognized as part of the primary key’s web-of-trust.

### Can I use only a subkey for all operations?

Yes, as long as you have generated the necessary subkeys for signing,
encryption, and authentication. But certain actions, like certifying other keys
or adding User IDs, require the primary key.

## Tips for Secure Usage

- **Inspect Subkey Capabilities**: Always verify what operations a subkey can
  perform by reviewing its **Usage** field.
- **Plan Subkey Generation**: At the time of key creation, consider creating
  multiple subkeys with distinct purposes (e.g., signing, encryption,
  authentication).
- **Backup Primary Key Securely**: Store the primary key in an offline, highly
  secure location to allow recovery or advanced operations if needed.

## Additional Note on Subkey Algorithm Types

Subkeys in GpgFrontend offer more algorithm types than primary keys due to their
specialized roles. While primary keys focus on establishing identity and trust,
subkeys are often dedicated to specific tasks like encryption or authentication.
This task-specific design allows subkeys to utilize a broader range of
algorithms, enhancing their flexibility and functionality. For instance, while
primary keys may be restricted to certain secure algorithms for signing, subkeys
can employ diverse algorithms optimized for encryption, like ECDH, ensuring
efficient and secure operations tailored to the user's needs.

For more Details: [Comparison of Cryptographic
Algorithms](/extra/algorithms-comparison)

**Subkey Supported Algorithms:**

- RSA
- DSA
- ELG-E
- ECDSA ED25519
- ECDSA ED448 (GnuPG >2.3.0)
- ECDH CV25519
- ECDH SECP256K1 (GnuPG >2.3.0)
- ECDH X448 (GnuPG >2.3.0)
- ECDH NIST P-256
- ECDH NIST P-384
- ECDH NIST P-521
- ECDH BrainPool P-256 (GnuPG >2.3.0)
- ECDH BrainPool P-384 (GnuPG >2.3.0)
- ECDH BrainPool P-512 (GnuPG >2.3.0)
