---
title: "Application Secure Key"
sidebar:
  label: Application Secure Key
---

To protect application-managed sensitive data, GpgFrontend automatically
generates and manages a dedicated **Application Secure Key**.

This key is used only for GpgFrontend's own internal data, such as selected
configuration records, key server settings, cached metadata, and key generation
profiles. It is separate from your OpenPGP keys and is not used to encrypt or
decrypt normal OpenPGP messages, files, signatures, or GnuPG-managed keyrings.

Key handling depends on the configured **SecureLevel** and user preferences.

## Key Features

### Automatic Key Generation

GpgFrontend automatically generates an application secure key during
initialization when needed.

- Before v2.1.9, random key generation relied on Qt's random generator.
- Since v2.1.9, GpgFrontend used OpenSSL-based cryptographic helpers for
  internal application data protection.
- Starting with v2.2.0, GpgFrontend has migrated these internal
  cryptographic helpers from OpenSSL to **libsodium**.

Application secure keys are stored with operating system file permissions set to
restrict access to the current user whenever possible, even when the key is
stored without PIN-based encryption.

:::tip[HOW TO]

SecureLevel is configured in the same way as described in the memory security
documentation: add or edit a line such as `SecureLevel=1` in your `ENV.ini` file
located in the working directory.

The meaning of each SecureLevel remains unchanged in v2.2.0. The internal
cryptographic implementation and data format have changed, but the user-facing
SecureLevel behavior is the same.

:::

### Internal Cryptographic Backend

Starting with GpgFrontend v2.2.0, internal application-managed
cryptographic helpers use **libsodium**.

This includes application-level helpers such as:

- random generation,
- hashing,
- HMAC,
- password hashing,
- key derivation,
- authenticated encryption for application-managed data.

Standard OpenPGP operations are still handled by the selected OpenPGP engine,
such as **GnuPG** or **rPGP**.

:::note

OpenSSL may still be used indirectly by Qt or the operating system for network
communication, such as HTTPS/TLS connections. The migration to libsodium applies
to GpgFrontend's own internal cryptographic helpers and does not mean OpenSSL is
absent from every runtime environment.

:::

## Data Encryption and SecureLevel Behavior

The Application Secure Key protects internal application data. General
non-sensitive configuration data is not encrypted by default.

### SecureLevel 0, 1, and 2

At SecureLevel lower than 3:

- the application secure key is generated automatically;
- the key may be stored without PIN-based encryption;
- access is restricted using file system permissions where possible;
- no PIN is required at application startup.

### SecureLevel 3 or Higher

At SecureLevel 3 or higher:

- the user is prompted for a PIN at application startup;
- the application secure key is protected using a PIN-derived key;
- protected internal application data is available only after successful PIN
  entry;
- if the PIN is lost, protected application data may become inaccessible.

The SecureLevel model is unchanged from earlier versions. The main change in
v2.2.0 is the migration of the internal cryptographic implementation and storage
format to libsodium-based helpers.

## Key Storage and File Protection

Application secure keys are stored in GpgFrontend's secure key directory. File
permissions are applied to restrict access to the current user whenever possible.

At SecureLevel lower than 3, protection relies mainly on operating system file
permissions.

At SecureLevel 3 or higher, the secure key is additionally protected by the
user's PIN. The application must successfully unlock the secure key before it
can access protected internal data.

## Key Rotation and Data Migration

Depending on SecureLevel and configuration, GpgFrontend may rotate internal
encryption keys and migrate protected application data to the currently active
internal format.

When internal data formats change, GpgFrontend may need to re-encrypt or
recreate some application-managed encrypted data.

:::caution[Compatibility Notice]

Starting with v2.2.0, GpgFrontend's internal application-managed
cryptographic format has changed as part of the migration from OpenSSL-based
helpers to libsodium-based helpers.

Some encrypted application data created by earlier versions may not be readable
by v2.2.0 or later. This may affect selected application-managed data such
as encrypted settings, cached metadata, key server settings, or key generation
profiles.

This does **not** affect standard OpenPGP messages, encrypted files, detached
signatures, inline signatures, or GnuPG-managed keyrings.

:::

## Historical Changes

### Before v2.1.9

- Application data was encrypted using the older internal format.
- Random key generation relied on Qt's random generator.
- Some internal cryptographic designs were simpler and less isolated.

### Since v2.1.9

- GpgFrontend removed the QtAES dependency.
- Internal application-managed encryption was migrated to OpenSSL-based helpers.
- AES-GCM became the internal authenticated encryption mode.
- Secure key hierarchy and stronger internal protection were introduced.

### Starting with v2.2.0

- Internal application-managed cryptographic helpers migrated from OpenSSL to
  **libsodium**.
- Internal encrypted data formats changed.
- SecureLevel behavior remains the same.
- Standard OpenPGP operations remain handled by the selected OpenPGP engine,
  such as GnuPG or rPGP.
- OpenSSL may still be used by Qt or the operating system for HTTPS/TLS network
  communication.

## Security Levels and Functionality

| SecureLevel | Key Generation | PIN Protection | Key Rotation | Key Storage                     | User Prompt at Startup |
| ----------- | -------------- | -------------- | ------------ | ------------------------------- | ---------------------- |
| 0, 1, 2     | Automatic      | No             | No           | File permissions                | No                     |
| 3 or higher | Automatic      | Yes            | Yes          | PIN-protected, file permissions | Yes                    |

- At SecureLevel lower than 3, the secure key is generated automatically and
  stored with file permission protection.
- At SecureLevel 3 or higher, PIN protection is enforced and application startup
  requires PIN entry.

## Downgrade Support and Data Separation

GpgFrontend supports SecureLevel downgrade workflows. If you initially start
GpgFrontend with SecureLevel set to 3 or higher, you can later change the
SecureLevel to a lower value, such as 0, 1, or 2.

In this case:

- GpgFrontend starts normally using the application data associated with the
  lower SecureLevel.
- Data protected under SecureLevel 3 remains stored separately and is not
  accessible while running at a lower SecureLevel.
- You can switch SecureLevel back to 3 or higher later. After entering the
  correct PIN, the protected application data associated with that SecureLevel
  becomes available again.
- You may alternate between SecureLevel 3 and lower SecureLevels. Each level
  uses its own protected data state.

:::caution

You must initially set SecureLevel to 3 or higher on the first launch to enable
this protected-data workflow. It is not possible to enable SecureLevel 3 for the
first time if the application was previously initialized with a lower
SecureLevel.

:::

## Technical Notes

- **Internal cryptographic backend since v2.2.0:** libsodium
- **Previous internal backend since v2.1.9:** OpenSSL
- **OpenPGP operations:** handled by the selected OpenPGP engine, such as GnuPG
  or rPGP
- **Network TLS/HTTPS:** may still use OpenSSL indirectly through Qt or the
  operating system
- **SecureLevel behavior:** unchanged from earlier versions
- **Secure memory:** sensitive values are managed in secure memory when enabled
  and erased after use where supported

## Best Practices & Recommendations

- Set SecureLevel to 3 or higher if you want PIN protection for
  application-managed sensitive data.
- Use a strong, memorable PIN and store a backup in a safe place.
- Back up important GpgFrontend configuration and key database data regularly.
- Do not confuse the Application Secure Key with your OpenPGP private keys.
- Review warning messages after upgrading from older versions, especially when
  internal encrypted application data cannot be migrated.
- Back up OpenPGP private keys and revocation certificates separately. The
  Application Secure Key is not a replacement for OpenPGP key backups.

## Feedback and Development

Application Secure Key management was significantly improved in v2.1.9 and
updated again in v2.2.0 with the migration to libsodium-based internal
cryptographic helpers.

GpgFrontend's secure key management continues to evolve. Users are encouraged to
review the implementation, report issues, and suggest improvements.
