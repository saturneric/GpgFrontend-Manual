---
title: Frequently Asked Questions (FAQ)
sidebar:
  label: FAQ
  order: 4
---

## Understanding GpgFrontend

### What is GpgFrontend?

A user-friendly, cross-platform tool for OpenPGP encryption, making it easy to
protect your privacy and secure your communications.

### What can I do with GpgFrontend?

Beyond basic encryption and decryption, you can generate/manage key pairs,
encrypt files and emails, and use digital signatures to verify integrity and
origin.

## Getting and Updating GpgFrontend

### How can I obtain and start using GpgFrontend?

You can download the latest version of GpgFrontend from [GpgFrontend's Downloads
Page](/overview/downloads) and choose the installation method for your platform.

### How do I update GpgFrontend to the latest version?

You can always get the latest stable or nightly release from the Downloads Page.
On Windows, simply run the new installer. On macOS and Linux, replace the old
app or AppImage with the new version. Your settings and keys will be preserved
unless noted otherwise in the release notes.

## OpenPGP and GnuPG Explained

### How do OpenPGP and GnuPG relate?

OpenPGP serves as a standardized protocol for encrypting and decrypting data,
which GpgFrontend supports. GnuPG, or GPG, implements the OpenPGP standard,
providing the necessary cryptographic functions. GpgFrontend leverages GnuPG for
operations like encryption, decryption, and key management.

### Which operating systems does GpgFrontend support?

GpgFrontend is a cross-platform application that supports Windows, macOS, and
Linux, making it accessible to nearly all users for their privacy and data
protection needs.

### Why the Need for GnuPG?

GpgFrontend itself does not handle direct encryption or decryption; it requires
GnuPG for these operations. This design choice ensures higher security, allowing
users to rely on their own verified version of GnuPG.

### Can I use keys/data from other OpenPGP software??

Yes—as long as your keys and encrypted data are in a format accepted by GnuPG
(GPG), they can be used with GpgFrontend. GpgFrontend relies on GnuPG for all
OpenPGP operations, so compatibility is determined by what GnuPG supports. Most
keys and data produced by standard-compliant GPG or PGP programs will work
seamlessly.

## Troubleshooting GnuPG Installation Issues

### What if I see "GnuPG not installed correctly"?

This issue typically arises when GpgFrontend cannot locate GnuPG on your system.
Here are steps to address this based on your operating system:

- For macOS Users: Install GpgFrontend using Homebrew with `brew install --cask gpgfrontend`.
- For Linux Users: Install GnuPG via your package manager (apt, yum, etc.).
- For Windows Users: New versions include GnuPG; or get it
  [here](https://www.gnupg.org/ftp/gcrypt/binary/).

### Where can I find more help?

For more detailed guidance, refer to the quick start manual available at
[Getting Started Guide](/overview/getting-started).

## Key and File Management

### How do I import or export keys in GpgFrontend?

Use the Key Management section to import or export public/private keys. You can
also drag-and-drop key files directly into the application's Key ToolBox.

### Can I encrypt and decrypt files as well as text?

Yes, GpgFrontend supports both text and file encryption/decryption. Use the
dedicated file options in the main interface to protect or unlock files.

## Nightly & Experimental Versions

### What are Nightly versions?

Automatically generated experimental builds with new features/fixes under
testing. Less stable than official releases, may have breaking changes, and are
not GPG-signed. Not recommended for production. Always verify the SHA256
checksum. Please report feedback/issues on GitHub.

## Password, PIN, and Security

### How does GpgFrontend handle passphrases or PINs?

GpgFrontend never processes or stores your GPG key passphrases or smart card
PINs. All PIN entry is securely handled by GnuPG’s pinentry, independent from
GpgFrontend.

For app-specific encryption (e.g., KeyPackage), passphrases/PINs are used only
in memory and immediately cleared. Advanced users can enable PIN caching and
adjust security levels.

### Can lost passwords or keys be recovered?

No, for your security, neither GpgFrontend nor the developer can recover lost
passwords or private keys. Make sure to back up your private key and remember
your passphrase!

### How does GpgFrontend ensure secure communications?

It uses GnuPG to implement OpenPGP with robust encryption algorithms. Only
intended recipients can decrypt your messages.

## Smart Card Support

### Does GpgFrontend support OpenPGP smart cards or tokens?

Yes, if your GnuPG supports smart cards. Manage your smart cards directly via
the SmartCard Controller.

## Language Support

### Is GpgFrontend available in my language?

GpgFrontend supports multiple languages. You can change the display language
from the `Settings > General` tab. Want to help translate? See the [contribution
guide](/appendix/translate-interface) on GitHub!

## Privacy Policy

### What data does GpgFrontend collect?

GpgFrontend does not collect or transmit any personal or usage data. All
cryptographic operations are performed locally. Update checks can be disabled,
and no tracking or analytics are built in.

## Bugs, Feedback, and Feature Requests

### How can I request a new feature?

You can suggest new features by opening an issue on GitHub or contacting the
maintainer directly.

### Found a bug?

If you encounter any issues with GpgFrontend, please report them via the GitHub
repository. You can also contact me directly if you're not on GitHub; see the
[Contact](/overview/contact) section for details.

### Interested in contributing?

Feel free to modify GpgFrontend's code and submit a Pull Request with your
enhancements. You can also send patches via email if you prefer to contribute
anonymously.
