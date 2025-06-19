---
title: Comprehensive OpenPGP Smart Card Management
sidebar:
  label: Smart Card
---

The Smart Card Controller in GpgFrontend provides a comprehensive interface for
managing your OpenPGP smart cards (such as YubiKey, Nitrokey, or other
compatible devices). It allows you to view detailed card information, perform
essential operations, and manage keys directly on your smart card.

![](https://image.cdn.bktus.com/i/2025/06/19/1a9393f9-2f6a-8df5-d931-239b11dd88fb.webp)

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

## Security Note

All sensitive operations (such as PIN change or key generation) are performed
directly on the smart card hardware, ensuring private keys never leave the
device.
