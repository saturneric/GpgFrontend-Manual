---
title: "Application Secure Key"
sidebar:
  label: Application Secure Key
---

To enhance the protection of application data, GpgFrontend automatically
generates and manages a dedicated Application Secure Key. This key is used to
encrypt sensitive internal data—such as certain configuration files, key server
settings, and key generation profiles—distinct from user PGP keys. Key
management adapts according to the configured security level and user
preferences.

## Key Features

### Automatic Key Generation

- Upon first use or initialization, GpgFrontend generates a high-entropy random
  key. Since v2.1.9, this is done using OpenSSL’s secure random generator for
  maximum security. Prior to v2.1.9, QRandom’s generator was used.
- If OpenSSL secure random is unavailable, a fallback random generator is used,
  with a warning provided for lower security levels.
- Application secure keys are stored with operating system file permissions set
  to restrict access to the current user only, even if stored in plaintext.

:::tip[HOW TO]

SecureLevel is configured in the same way as described in the memory security
documentation: simply add or edit a line such as `SecureLevel=1` in your
`ENV.ini` file located in the working directory. This allows flexible adjustment
of both memory and key security to fit your needs.

:::

### Data Encryption Algorithms

- Default Encryption: Application data (such as dynamic configuration, key
  server settings, and key generation profiles) is encrypted using AES-GCM 128
  for confidentiality and integrity.
- PIN-based Key Encryption (SecureLevel ≥ 3): Starting from SecureLevel 3, the
  application secure key itself is encrypted on disk using a key derived from
  the user’s PIN via Argon2ID and then AES-GCM 256. This means that upon
  startup, the user must enter their PIN to decrypt the secure key and access
  protected application data.
- General Configuration: Most standard, non-sensitive configuration data is not
  encrypted by default.

## Key Storage and File Protection

Application secure keys are stored in the application’s secure key directory,
identified by a partial HMAC of their encrypted content. Even when stored in
plaintext (SecureLevel < 3), file system permissions ensure that only the
current user can access the key files.

### PIN Protection & Key Structure (SecureLevel ≥ 3)

At SecureLevel 3 or higher:

- The user is prompted to enter a PIN at application startup.
- The master key (application secure key) is encrypted with a PIN-derived key
  and stored using AES-GCM 256.
- After PIN entry, only the encryption key (derived and rotated weekly) is used
  for encrypting/decrypting application data. The master key itself is not used
  directly for data encryption.
- The encrypted master key must be successfully decrypted with the PIN-derived
  key for the application to function.

### Key Rotation and Data Migration

- **Key Rotation**: For maximum security, GpgFrontend automatically rotates the
  encryption key on a weekly basis. Each new key is derived using Argon2ID and a
  time-based salt.
- **Automatic Data Migration:** When the encryption key is rotated, existing
  application data is automatically re-encrypted with the new key. This ensures
  ongoing data protection with minimal user intervention.

### Historical Changes

- Before v2.1.9:
  - Application data was encrypted with AES-ECB 256 (a less secure mode).
  - Random keys were generated using QRandom.
  - The master key was used directly for data encryption.
- Since v2.1.9:
  - Encryption uses AES-GCM 128 for data, and AES-GCM 256 for PIN-based key
    wrapping.
  - Key generation relies on OpenSSL’s random number generator.
  - The introduction of key hierarchy and rotation enhances security, with
    legacy data seamlessly migrated to new standards.

## Security Levels and Functionality

| SecureLevel | Key Generation               | PIN Protection | Key Rotation | Key Storage                     | User Prompt at Startup |
| ----------- | ---------------------------- | -------------- | ------------ | ------------------------------- | ---------------------- |
| 0, 1, 2     | Automatic, plaintext storage | No             | No           | File permissions                | No                     |
| 3 or higher | Automatic, encrypted storage | Yes            | Yes          | PIN-encrypted, file permissions | Yes                    |

- At SecureLevel < 3, the key is generated and stored in plaintext (with OS
  permissions).
- At SecureLevel ≥ 3, PIN protection and regular key rotation are enforced; application startup requires PIN entry.

## **Downgrade Support and Data Separation**

GpgFrontend supports **downgrade** operations for SecureLevel. If you initially
start GpgFrontend with SecureLevel set to 3 or higher (enabling PIN protection
and advanced encryption), you can later change the SecureLevel to a lower value
(such as 0, 1, or 2). In this case:

- GpgFrontend will start normally and will restore all application data
  associated with the lower SecureLevel. Any data previously created or modified
  under this SecureLevel will be accessible as before, while the data protected
  under SecureLevel 3 remains securely stored and inaccessible in this mode.
- You can switch the SecureLevel back to 3 (or higher) at any time. After you
  enter the correct PIN, all your previous application data—including
  configuration, key server settings, and other protected content—will be fully
  restored and available.
- You can freely alternate between SecureLevel 3 and any lower level. Each time
  you return to SecureLevel 3 and successfully authenticate with your PIN, your
  original encrypted application data will be available. When you downgrade
  again, the application data from the lower SecureLevel (as it was before
  upgrading) will be restored.

:::caution

You must initially set SecureLevel to 3 or higher on the first launch
to enable this feature. It is not possible to enable SecureLevel 3 for the first
time if the application was previously initialized with a lower SecureLevel.

:::

## Technical Notes

- **Encryption Algorithms:**
  - Application data: AES-GCM 128
  - Key encryption (PIN-derived): AES-GCM 256
- **Key Derivation:** Argon2ID with robust parameters for resistance to
  brute-force attacks.
- **Key IDs:** Calculated using HMAC-SHA256 for uniqueness and integrity.
- **Secure Memory:** All key material is managed in secure memory (if enabled),
  and sensitive values are securely erased after use.

## Best Practices & Recommendations

- For the best protection of application data, set SecureLevel to 3 or higher
  and use a strong, memorable PIN.
- Keep a backup of your PIN in a safe place, as losing the PIN may render
  encrypted data inaccessible.
- Watch for application warnings about key generation, encryption, or system
  cryptography support.

## Troubleshooting

- Key File Cannot Be Saved: Ensure the application has permission to write to
  its secure key directory.
- PIN Incorrect: If you forget your PIN or cannot unlock your key, you may need
  to reinitialize the secure key. This will create a new key, making old
  encrypted data inaccessible.
- Cryptographic Support Warning: If OpenSSL or secure random functions are
  unavailable, less secure fallback methods are used and the application will
  notify you.

## Feedback and Development

All secure key management and related enhancements have been introduced in
v2.1.9. GpgFrontend’s secure key management continues to evolve. Users are
encouraged to review the implementation, report issues, and suggest
improvements. The development team is committed to maintaining robust security
standards and welcomes community participation.
