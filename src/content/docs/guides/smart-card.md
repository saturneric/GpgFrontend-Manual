---
title: Comprehensive OpenPGP Smart Card Management
sidebar:
  label: Smart Card
---

The Smart Card Controller in GpgFrontend provides a comprehensive interface for
managing your OpenPGP smart cards (such as YubiKey, Nitrokey, or other
compatible devices). It allows you to view detailed card information, perform
essential operations, and manage keys directly on your smart card.

![](https://image.cdn.bktus.com/i/2025/06/24/c5d2b202ae1003d31fe708df2989935ce30bf78d.webp)

## Core Concepts and Frequently Asked Questions

### What is an OpenPGP Smart Card?

An OpenPGP smart card (such as YubiKey, Nitrokey, or similar devices) is a
dedicated hardware token designed to generate, store, and use cryptographic keys
in accordance with the OpenPGP standard (RFC 4880). The key advantages are:

- Private keys never leave the device: All cryptographic operations (signing,
  decryption, authentication) are performed on the card.
- Hardware protection: Even if your computer is compromised, the private key
  cannot be extracted from the card.
- Additional security features: Such as PIN protection, touch-to-sign, and
  multi-factor authentication.

OpenPGP smart cards are widely used for secure email (PGP/GPG), SSH
authentication, and other security-critical applications.

### What is the difference between PIN and Admin PIN?

OpenPGP smart cards support at least two types of PIN codes:

#### User PIN (CHV1)

This is the regular PIN you enter to unlock the card for daily operations, such
as signing or decrypting.

- Usually 6 digits by default.
- Entering it incorrectly too many times will lock the card, requiring admin
  intervention.

#### Admin PIN (CHV2)

This is the administrator PIN, used to perform high-privilege management
operations.

- Usually 8 digits by default.
- Required for actions such as resetting the user PIN, generating or importing
  keys, or changing cardholder information.
- Loss or compromise of the Admin PIN may result in loss of administrative
  control over the card.

In short: The User PIN is for everyday use; the Admin PIN is for advanced or
recovery operations.

### What is a Key Stub?

A key stub in the GnuPG keyring is a placeholder record that indicates the
actual private key is stored externally (e.g., on a smart card). It does not
contain the private key itself.

- GnuPG uses the stub to know that, when a cryptographic operation is needed, it
  should forward the request to the smart card.
- The stub includes information such as the key ID and associated smart card
  serial number.
- If you remove the smart card, the stub remains but cannot be used to perform
  cryptographic operations.

If you lose the smart card, even though the stub remains in your GnuPG keyring,
you will not be able to sign or decrypt using that key.

### Does the Smart Card store the private key and the public key?

The smart card only stores the private key(s). The private key cannot be
exported or extracted from the card. And the public key is not stored on the
card by default. Instead, you are expected to distribute your public key
separately (e.g., via key servers, files, or URLs).

### Why set a Public Key URL?

Setting a public key URL allows others (and your own software) to retrieve your
public key automatically when needed. This helps with secure communication and
verification without manual key distribution.

### What does the “Fetch” operation do? When should I use it?

The Fetch operation reads and synchronizes information from the smart card to
the application interface:

- Use it after inserting a new card, generating or changing keys, or if you
  suspect the card’s status is not up-to-date.
- Fetch ensures that all data (such as card info and key stubs) are current and
  correctly reflected in the application.
- In cases where the card is not detected, or after making changes to the card,
  use Fetch to refresh the state.

## Key Sections and Features

Smart Card(s) Selection: At the top, you can select from multiple detected
smart cards (if more than one is connected) using the dropdown menu.

## OpenPGP Card Information

- Basic Information: Displays card reader type,
  serial number, card type, firmware and app versions, manufacturer, cardholder
  name, language, and gender.
- Status: Displays the status of important card features, such as Signature
  Counter, PIN cache status (CHV1 Cached), PIN length limits, remaining PIN
  attempts (CHV Retry Left), KDF (key derivation function) status, UIF
  (touch-to-sign) status, and whether signing, encryption, and authentication
  are enabled.
- Key Information: Lists all cryptographic keys stored on the card, showing
  their type (sign, encrypt, authenticate), user identity (email), and Key ID.

## Operations Panel

On the right, the Operations panel allows you to perform key management and card
administration tasks:

- Change Name / Language / Gender: Personalize cardholder info stored on the
  card.
- Change Login Data / Public Key URL: Update login data or set a public key
  publication URL.
- Change PIN / Admin PIN / Reset Code: Change user or admin PIN, or reset the
  card if needed.
- Generate Card Keys: Directly generate new keys on the smart card, ensuring
  keys never leave the hardware.
- Fetch: Retrieve updated information from the card.
- Restart All Gpg-Agents: Restarts the background GnuPG agents. This is
  especially helpful if the card is not being recognized or after making major
  changes.
- Refresh: Reloads the interface and card information.

## Key Stub(s) in Key Database(s)

- Shows the corresponding key stubs in your GnuPG keyring that are associated
  with the card.
- You can select keys, view their type, associated identity, and key ID.

## Typical Usage Scenarios

- View and audit your card’s current status and configuration
- Change PINs or reset the card if you forget your credentials
- Generate new signing/encryption keys directly on the smart card for maximum
  security
- Update user information stored on the card
- Sync card keys with your GnuPG keyring

## Other Common Questions

### What if I enter the wrong PIN too many times?

If you exceed the maximum number of attempts for the User PIN, the card will
lock and require the Admin PIN to reset or unlock. If you also lose or forget
the Admin PIN, you may need the reset code or, in some cases, perform a factory
reset (which will erase all keys).

### How many keys can be stored on the card?

Most OpenPGP cards support up to three key slots: one each for signature,
encryption, and authentication. Actual capacity may vary by manufacturer and
card model. Refer to the documentation for your device.

### How do I synchronize card keys with my GnuPG keyring?

After using “Fetch,” GnuPG will automatically create the necessary key stubs,
enabling the software to reference the keys stored on the card. If you replace
or upgrade your card, remember to update your keyring to avoid mismatches or
missing keys.

### Can My Smart Card (e.g., YubiKey) Store Multiple Types of Credentials?

Yes, many modern security tokens and smart cards—such as YubiKey—support
multiple independent modules or “applications” on the same device. Typical
examples include:

- OpenPGP: Used for cryptographic operations (signing, encryption,
  authentication) with GPG/PGP.
- FIDO2 / Passkey: Used for passwordless logins, web authentication (WebAuthn),
  and as a hardware security key for websites or services.
- PIV (Personal Identity Verification): Used in enterprise and government
  settings for smart card logins, certificates, and secure authentication.

#### Independence of Modules

- Each module is logically and cryptographically independent. For example,
  generating or importing a key in the OpenPGP module will not affect keys or
  credentials in the FIDO2 or PIV modules, and vice versa.
- PINs and management codes are typically separate. Each module may have its own
  set of PINs or management credentials.
- Operations and data are isolated: Using one module does not interfere with, or
  grant access to, another module’s secrets.

You can use your YubiKey for OpenPGP-based email encryption, as a passkey for
passwordless login, and as a smart card for Windows logon—all at the same time,
without conflicts.

> While modules are independent, the overall storage of the device is shared.
> Each module has its own storage limit (e.g., number of FIDO2 credentials,
> slots for OpenPGP keys). You may need different software to manage each module
> (e.g., GPG for OpenPGP, YubiKey Manager for FIDO2, PIV tools for smart card
> management).

## Security Note

All sensitive operations (such as PIN change or key generation) are performed
directly on the smart card hardware, ensuring private keys never leave the
device.
