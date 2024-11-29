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

## **Purpose and Key Advantages**

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

## **Features Overview**

### **1. OpenPGP Standards Compliance**

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

### **2. Creating and Processing Emails**

#### **Creating and Signing Emails**

1. Open GpgFrontend and click **"New E-Mail"** to create a blank email.

![Open Email Tab](https://image.cdn.bktus.com/i/2024/11/29/19674701-548b-db30-3d19-473422618fc3.webp)

2. Type your email content in the editor.
3. Select your private key from the **Key Toolbox**.
4. Click **"Sign"** to digitally sign the email.
   - Signed emails include a PGP signature block, visible in the content.

![Sign Email](https://image.cdn.bktus.com/i/2024/11/29/fc733201-8a5e-b2c9-8043-c17e09b5367b.webp)

#### **Encrypting Emails**

1. Select the recipient's public key in the **Key Toolbox**.
2. Click **"Encrypt"** to secure the email content.
   - The content will be transformed into a PGP-encrypted format.

![Encrypt Email](https://image.cdn.bktus.com/i/2024/11/29/92427d5d-937b-2285-97a5-48d7c6edf9a2.webp)

#### **Saving Emails for Sending**

1. Processed emails can be saved as `.eml` files using **File > Save As**.
2. Upload the `.eml` file to your email client's drafts folder or webmail
   interface, then send the email.

### **3. Receiving and Processing Emails**

#### **Decrypting and Verifying Emails**

1. Export the email source as an `.eml` file from your email client or copy the
   raw email source.
2. Open the `.eml` file in GpgFrontend.
3. Use:
   - **"Decrypt Verify"**: Decrypt and verify the email simultaneously.
   - **"Verify"**: Validate the signature without decrypting.
   - **"Decrypt"**: Decrypt without verifying.
  
![Verify Email](https://image.cdn.bktus.com/i/2024/11/29/1147e7e4-5fc0-26e7-04a3-e1c71e17f550.webp)

#### **Offline Validation**

- GpgFrontend processes all email verification and decryption offline, ensuring
  that no sensitive data is exposed to external servers.
- Users retain full control of their private keys, which remain stored locally.

### **4. Why Use EML Format?**

#### **Benefits of EML**

- `.eml` is a widely supported format across email clients like Thunderbird,
  Outlook, and webmail platforms.
- Unlike proprietary email handling protocols, `.eml` allows for seamless
  export, import, and offline processing.

#### **Why Not Use IMAP/SMTP?**

- Avoids the complexity and potential vulnerabilities introduced by integrating
  full-fledged email protocols.
- Keeps the application lightweight and focused on local cryptographic
  operations.

#### **Addressing PGP Limitations in Clients**

- Many email clients lack robust PGP support or offer inconsistent
  implementations.
- GpgFrontend provides a reliable and flexible solution for users needing
  advanced PGP functionality.

## **Key Use Cases**

### **1. Sending Emails**

1. Process the email in GpgFrontend (e.g., sign, encrypt, or both).
2. Save the processed email as an `.eml` file.
3. Import the `.eml` file into your email client or webmail interface, then send
   it.

### **2. Receiving Emails**

1. Export the email source as `.eml` from your email client.
2. Open it in GpgFrontend to decrypt or verify.
3. For example:
   - A signed email will display a **"Good Digital Signature"** message.
   - An encrypted email will be decrypted and displayed in plaintext.

## **Advanced Features**

### **1. Combined Operations**

- GpgFrontend supports simultaneous encryption and signing of outgoing emails.
- Incoming emails can also be decrypted and verified in a single operation for
  convenience.

### **2. Flexible Processing**

- Choose separate or combined workflows for signing, encrypting, verifying, or
  decrypting based on your needs.
- This flexibility makes GpgFrontend a versatile tool for various email
  scenarios.

### **3. Offline-First Design**

- All cryptographic operations are performed locally, ensuring that private keys
  and sensitive data are never exposed to external servers.

## **Best Practices for Secure Email Handling**

1. **Use Trusted Keys**:

   - Regularly validate public keys to prevent misuse.
   - Import keys only from trusted sources.

2. **Keep Private Keys Offline**:

   - Avoid uploading private keys to email providers.
   - Store private keys securely, preferably on encrypted storage.

3. **Leverage GpgFrontend's Local Processing**:

   - Ensure all encryption, signing, and verification tasks are performed
     offline for maximum security.

4. **Save Emails in EML Format**:

   - Use `.eml` files for cross-platform compatibility and simple integration
     with various email clients.

5. **Check Email Compatibility**:
   - Ensure recipients can handle PGP-encrypted emails or provide instructions
     for using tools like GpgFrontend or Thunderbird.
