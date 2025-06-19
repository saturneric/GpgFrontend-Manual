---
title: Frequently Asked Questions (FAQ)
sidebar:
  label: FAQ
  order: 4
---

## Understanding GpgFrontend

**What is GpgFrontend?** GpgFrontend is a user-friendly, cross-platform tool
designed to facilitate the use of OpenPGP encryption, making it easier for
individuals to protect their privacy and secure their communications.

**What can I do with GpgFrontend?** Beyond basic encryption and decryption,
GpgFrontend supports digital signatures to verify the integrity and origin of
messages. Users can manage and generate key pairs, encrypt files and emails, and
sign their communications for added security.

**How can I obtain and start using GpgFrontend?** You can download the latest
version of GpgFrontend from [GpgFrontend's Downloads Page](/overview/downloads) and
choose the installation method for your platform.

**How do I update GpgFrontend to the latest version?** You can always get the
latest stable or nightly release from the Downloads Page. On Windows, simply run
the new installer. On macOS and Linux, replace the old app or AppImage with the
new version. Your settings and keys will be preserved unless noted otherwise in
the release notes.

## OpenPGP and GnuPG Explained

**How do OpenPGP and GnuPG relate?** OpenPGP serves as a standardized protocol
for encrypting and decrypting data, which GpgFrontend supports. GnuPG, or GPG,
implements the OpenPGP standard, providing the necessary cryptographic
functions. GpgFrontend leverages GnuPG for operations like encryption,
decryption, and key management.

**Which operating systems does GpgFrontend support?** GpgFrontend is a
cross-platform application that supports Windows, macOS, and Linux, making it
accessible to nearly all users for their privacy and data protection needs.

## Troubleshooting GnuPG Installation Issues

**Encountering 'GnuPG not installed correctly'?** This issue typically arises
when GpgFrontend cannot locate GnuPG on your system. Here are steps to address
this based on your operating system:

### For macOS Users

- **Install GnuPG for OSX** from
  [here](https://sourceforge.net/p/gpgosx/docu/Download/), or install
  GpgFrontend using Homebrew with `brew install --cask gpgfrontend`.
- If GnuPG is installed in a custom location, please tell GpgFrontend where the
  gpgconf binary it is at GnuPG Controller.

### For Linux Users

- Install GnuPG via your package manager (apt, yum, etc.).
- If GnuPG is installed in a custom location, please tell GpgFrontend where the
  gpgconf binary it is at GnuPG Controller.

### For Windows Users

- The latest GpgFrontend versions include GnuPG. It's recommended to download
  the most recent GpgFrontend version.
- Alternatively, download GnuPG from
  [here](https://www.gnupg.org/ftp/gcrypt/binary/gnupg-w32-2.4.0_20221216.exe)
  and reinstall if necessary.

### Additional Assistance

- For more detailed guidance, refer to the quick start manual available at
  [Getting Started Guide](/overview/getting-started).

## Reporting Bugs and Contributing

**Found a bug?** If you encounter any issues with GpgFrontend, please report
them via the GitHub repository. You can also contact me directly if you're not
on GitHub; see the [Contact](/overview/contact) section for details.

**Interested in contributing?** Feel free to modify GpgFrontend's code and
submit a Pull Request with your enhancements. You can also send patches via
email if you prefer to contribute anonymously.

## Why the Need for GnuPG?

**Importance of Installing GnuPG** GpgFrontend itself does not handle direct
encryption or decryption; it requires GnuPG for these operations. This design
choice ensures higher security, allowing users to rely on their own verified
version of GnuPG.

## Understanding Nightly Versions

A Nightly version is an automatically generated, experimental build of
GpgFrontend that may include the latest features, urgent fixes, and changes that
are still being tested. Nightly builds are less stable than official releases,
may introduce breaking changes without notice, and are not GPG-signed. They are
ideal for users who want early access and are willing to help test, but not
recommended for production use. For integrity, please verify the provided SHA256
checksums. Your feedback is invaluable—please report any issues or suggestions
on GitHub to help improve future stable releases.

## Security and Privacy

**How does GpgFrontend ensure my communications are secure?** GpgFrontend uses
GnuPG to implement the OpenPGP standard, securing your data with robust
encryption algorithms to prevent unauthorized access. It supports public and
private key encryption methods, ensuring only intended recipients can decrypt
and read your messages.

## Importing and Exporting Keys

**How do I import or export keys in GpgFrontend?** Use the Key Management
section to import or export public/private keys. You can also drag-and-drop key
files directly into the application's Key ToolBox.

## File Encryption and Decryption

**Can I encrypt and decrypt files as well as text?** Yes, GpgFrontend supports both
text and file encryption/decryption. Use the dedicated file options in the main
interface to protect or unlock files.

## Compatibility With Other OpenPGP Software

**Can I use keys and encrypted data created in other OpenPGP software?** Yes—as
long as your keys and encrypted data are in a format accepted by GnuPG (GPG),
they can be used with GpgFrontend. GpgFrontend relies on GnuPG for all OpenPGP
operations, so compatibility is determined by what GnuPG supports. Most keys and
data produced by standard-compliant GPG or PGP programs will work seamlessly.

## Supported Languages

**Is GpgFrontend available in my language?** GpgFrontend supports multiple
languages. You can change the display language from the `Settings > General`
tab. Want to help translate? See the [contribution
guide](/appendix/translate-interface) on GitHub!

## Password & PIN Handling

**How does GpgFrontend handle passphrases or PINs?** 

GpgFrontend does not process or store your GPG key passphrases or smart card
PINs. All password and PIN entry for GPG keys is securely handled by the GnuPG
pinentry component, which operates independently of GpgFrontend. GpgFrontend
never sees, intercepts, or retains your passphrases or PINs. 

For application-specific encryption features (such as KeyPackage protection),
passphrases or PINs are used only in memory for cryptographic operations and
immediately cleared afterward. Advanced users can enable PIN caching for these
features, and adjust security levels for maximum protection.

**Can lost passwords or keys be recovered?** No, for your security, neither
GpgFrontend nor the developer can recover lost passwords or private keys. Make
sure to back up your private key and remember your passphrase!

## Using GpgFrontend With Smart Cards

**Does GpgFrontend support OpenPGP smart cards or tokens?** Yes, GpgFrontend
supports smart card operations (such as viewing, key generation, and signing) if
your GnuPG installation is configured for smart card support. Users can manage
their OpenPGP smart cards directly using the SmartCard Controller within
GpgFrontend.

## Privacy Policy

**What data does GpgFrontend collect?** GpgFrontend does not collect or transmit
any personal or usage data. All cryptographic operations are performed locally.
Update checks can be disabled, and no tracking or analytics are built in.

## Feature Requests

**How can I request a new feature?** You can suggest new features by opening an
issue on GitHub or contacting the maintainer directly.
