---
title: Synchronizing Public Keys with Key Server
sidebar:
  label: Sync Public Keys
  order: 4
---

Keeping your public keys in sync with those stored on a key server is crucial
for secure communications. This synchronization ensures that any changes to
public keys, such as revocations or the addition of subkeys, are reflected in
your local keyring. Without this, you may be vulnerable to security risks like
man-in-the-middle attacks or authentication errors.

## Importance of Public Key Synchronization

**Key Revocation:** If a key is revoked by its owner, it's vital to stop using
it immediately. Revocation might occur if the private key is compromised or if
the key is no longer used.

**Subkey Updates:** If a new signing subkey is generated, it's essential for
your local gpg to recognize it. Without the updated information, gpg won't
authenticate signatures made with the new subkey.

## How to Sync Public Keys

GpgFrontend automates the public key synchronization process through a
user-friendly interface. Here’s how to use it:

1. Open the Key Management Interface: Navigate to the Key Management interface
   by clicking on the "Manage Keys" button in the main interface.
2. Select Keys to Sync: In the list of public keys, you can select specific keys
   to sync by checking the boxes next to them. If you want to sync all public keys,
   you do not need to select any specific keys.
3. Click the Sync Public Key Button: Locate and click the **Sync Public Key**
   button. This button is represented by a cloud icon with a refresh symbol,
   located in the toolbar at the top of the Key Management interface.If you have
   selected specific keys, the synchronization process will initiate for those
   keys. If no keys are selected, a confirmation prompt will appear, asking you to
   confirm if you want to synchronize all public keys.
4. Synchronization Process: The feature works by checking all the public keys in
   your possession against the key server. If there is an updated version of a key
   you own, GpgFrontend will import the new details to your local keyring.

![](https://image.cdn.bktus.com/i/2025/06/28/38eefac3220f864b5e4a1fe98681f8cef817ef21.webp)

By following these steps, you can ensure that your public keys are always
up-to-date, enhancing the security and reliability of your cryptographic
communications.

### Choosing the Right Key Server

To know which key server GpgFrontend interacts with, follow these steps:

1. Go to the settings section of GpgFrontend.
2. The default key server configured will be listed here.

![](https://image.cdn.bktus.com/i/2025/06/28/86bc996c90eb449dee681a86be15797015128f5c.webp)

If you need to use a different key server:

1. Navigate to the key server settings within GpgFrontend.
2. Add your preferred key server's details.
3. Set it as the default for future synchronizations.

:::caution[Changes (v2.1.6 and later)]

Setting a default key server **only affects key searches/imports**.

- **Export** and **Sync** operations are no longer affected by this setting.
- These operations **always use `https://keys.openpgp.org`**, which implements
  the Verifying Keyserver (VKS) API.

This behavior ensures improved security and global consistency in public key
management.

Or: [Want to restore previous behavior?](/guides/key-server-operations/#want-to-restore-previous-behavior)

:::

## Best Practices for Key Synchronization

- **Regular Sync:** Regularly sync your keys to ensure you have the latest
  updates, especially before engaging in secure communication.
- **Verify Changes:** After syncing, verify any changes or updates to ensure
  they are legitimate.
- **Secure Network:** Always perform key synchronization over a secure network
  to prevent interception or tampering.
