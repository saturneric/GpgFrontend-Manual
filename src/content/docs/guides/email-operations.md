---
title: Email Functionality
sidebar:
  label: Email Operations
---

GpgFrontend offers a powerful and user-friendly solution for email encryption
and signing, tailored for security-conscious users. By processing emails offline
in a widely supported `.eml` format, it eliminates the need for complex
protocols while maintaining robust OpenPGP compliance. Whether you're signing,
encrypting, verifying, or decrypting emails, GpgFrontend ensures a secure and
streamlined experience.

## Purpose and Key Advantages

GpgFrontend's email processing functionality is designed to empower users to
handle PGP-signed and encrypted emails in situations where their email clients
or web-based email services lack native PGP support. The core advantages
include:

- **Offline Verification and Decryption**: Users can securely process emails
  locally without uploading their private keys to email providers. This
  significantly enhances privacy and security.
- **EML Format Handling**: By leveraging the widely supported `.eml` format,
  GpgFrontend avoids introducing complex protocols like IMAP or SMTP,
  maintaining simplicity while offering full OpenPGP compliance.
- **Security-Focused**: For security-conscious users, GpgFrontend provides an
  offline, local-first solution that minimizes exposure to online threats and
  untrusted environments.

## Features Overview

### OpenPGP Standards Compliance

GpgFrontend adheres to OpenPGP standards (RFC 4880 and 3156) for email
encryption and signing, ensuring compatibility with tools like Thunderbird and
other OpenPGP-enabled clients.

- Emails processed in GpgFrontend can be easily verified and decrypted by
  compliant email clients.
- Supports separate and combined operations, such as:
  - **Sign Only**: Digitally sign the email to ensure authenticity.
  - **Encrypt Only**: Encrypt the email to protect its content.
  - **Sign and Encrypt Together**: Combine both operations for comprehensive
    security.
  - **Decrypt and Verify Together or Separately**: Flexibly handle incoming
    messages.

### Creating and Signing Emails

1. Open GpgFrontend and click **"New E-Mail"** to create a blank email.
2. Type your email content in the editor.
3. Select your private key from the **Key Toolbox**.
4. Click **"Sign"** to digitally sign the email.
5. Fill Sender, Receiver and the Subject of the email.

![](https://image.cdn.bktus.com/i/2025/06/24/84f732220b3a967aa5d3986f79475bdfcf53454e.webp)

![](https://image.cdn.bktus.com/i/2025/06/24/610ba60f2cd8eeddbcfbbc57aa602cff61197065.webp)

![](https://image.cdn.bktus.com/i/2025/06/24/fea933e12bf46516d6a1385698b6afa94e7543a0.webp)

![](https://image.cdn.bktus.com/i/2025/06/24/ee90e5bb25c7accdccf70f17c1986e53e0b4e81f.webp)

### Encrypting Emails

1. Select the recipient's public key in the **Key Toolbox**.
2. Click **"Encrypt"** to secure the email content. The content will be
   transformed into a PGP-encrypted format.

![](https://image.cdn.bktus.com/i/2025/06/24/f8fe32d6e3502a1ba3503189fa40e4348bd4cc81.webp)

### Saving Emails for Sending

1. Processed emails can be saved as `.eml` files using **File > Save As**.
2. Upload the `.eml` file to your email client's drafts folder or webmail
   interface, then send the email.

### Decrypting and Verifying Emails

1. Export the email source as an `.eml` file from your email client or copy the
   raw email source.
2. Open the `.eml` file in GpgFrontend.
3. Use:
   - **"Decrypt Verify"**: Decrypt and verify the email simultaneously.
   - **"Verify"**: Validate the signature without decrypting.
   - **"Decrypt"**: Decrypt without verifying.

![](https://image.cdn.bktus.com/i/2025/06/24/64b84451fd044cfd0c081161dad3057c5fde25a4.webp)

### Offline Validation

- GpgFrontend processes all email verification and decryption offline, ensuring
  that no sensitive data is exposed to external servers.
- Users retain full control of their private keys, which remain stored locally.

### Why Use EML Format?

- `.eml` is a widely supported format across email clients like Thunderbird,
  Outlook, and webmail platforms.
- Unlike proprietary email handling protocols, `.eml` allows for seamless
  export, import, and offline processing.

### Why Not Use IMAP/SMTP?

- Avoids the complexity and potential vulnerabilities introduced by integrating
  full-fledged email protocols.
- Keeps the application lightweight and focused on local cryptographic
  operations.

### Addressing PGP Limitations in Clients

- Many email clients lack robust PGP support or offer inconsistent
  implementations.
- GpgFrontend provides a reliable and flexible solution for users needing
  advanced PGP functionality.

## Key Use Cases

### Sending Emails

1. Process the email in GpgFrontend (e.g., sign, encrypt, or both).
2. Save the processed email as an `.eml` file.
3. Import the `.eml` file into your email client or webmail interface, then send
   it.

### Receiving Emails

1. Export the email source as `.eml` from your email client.
2. Open it in GpgFrontend to decrypt or verify.
3. For example:
   - A signed email will display a **"Good Digital Signature"** message.
   - An encrypted email will be decrypted and displayed in plaintext.

## Advanced Features

### Combined Operations

- GpgFrontend supports simultaneous encryption and signing of outgoing emails.
- Incoming emails can also be decrypted and verified in a single operation for
  convenience.

### Flexible Processing

- Choose separate or combined workflows for signing, encrypting, verifying, or
  decrypting based on your needs.
- This flexibility makes GpgFrontend a versatile tool for various email
  scenarios.

### Offline-First Design

- All cryptographic operations are performed locally, ensuring that private keys
  and sensitive data are never exposed to external servers.

## Best Practices for Secure Email Handling

- Use Trusted Keys: Regularly validate public keys to prevent misuse and import
  keys only from trusted sources.
- Keep Private Keys Offline: Avoid uploading private keys to email providers and
  store private keys securely, preferably on encrypted storage.
- Leverage GpgFrontend's Local Processing: Ensure all encryption, signing, and
  verification tasks are performed offline for maximum security.
- Save Emails in EML Format: Use `.eml` files for cross-platform compatibility
  and simple integration with various email clients.
- Check Email Compatibility: Ensure recipients can handle PGP-encrypted emails
  or provide instructions for using tools like GpgFrontend or Thunderbird.
