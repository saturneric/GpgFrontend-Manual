---
title: Synchronizing Public Keys with Key Server
description: "Keep your local OpenPGP keyring current by synchronizing public keys with key servers in GpgFrontend to catch revocations and subkey updates."
sidebar:
  label: Sync Public Keys
  order: 4
---

The public keys you have saved locally can go stale. The key's owner may
revoke it, extend it, or add a new subkey, and your local copy knows nothing
about that. **Syncing** asks a key server for the latest version of each key
and updates your local copy.

Why this matters:

- **Revoked keys**: If a key was revoked (for example, because its private key
  was stolen), you must stop using it right away. Without a sync, you cannot
  see the revocation.
- **New subkeys**: If someone added a new signing subkey, signatures made with
  it look invalid to you until your local copy learns about the new subkey.

A good habit: sync before you start an important encrypted conversation, and
every now and then in between.

## Sync Your Public Keys

1. In the main window, click **Manage Keys** to open the Key Management
   interface.

2. Choose what to sync:

   - To sync **specific keys**, check the boxes next to them.
   - To sync **all** public keys, leave all boxes unchecked.

3. Click the **Sync Public Key** button in the toolbar. It is the cloud icon
   with a refresh symbol.

   - If you selected keys, only those are synced.
   - If you selected nothing, GpgFrontend asks you to confirm syncing all
     public keys.

4. GpgFrontend checks each key against the key server. If the server has a
   newer version, the updates are imported into your local keyring.

![](https://image.cdn.bktus.com/i/2025/06/28/38eefac3220f864b5e4a1fe98681f8cef817ef21.webp)

## Which Key Server Is Used

Since GpgFrontend v2.1.6, **Sync** and **Export** always use
`https://keys.openpgp.org`. This server uses the Verifying Keyserver (VKS)
API, which gives better security and consistent results worldwide. You cannot
change the server for these two operations.

The **default key server** you set in Settings applies only to key
**searches and imports**:

1. Open the **Settings** and go to the key server section. The current default
   server is listed there.

2. To use a different one for searches and imports, add your preferred key
   server and set it as the default.

![](https://image.cdn.bktus.com/i/2025/06/28/86bc996c90eb449dee681a86be15797015128f5c.webp)

## Tips

- **Sync regularly**: Especially before you encrypt something important or
  verify a signature that fails unexpectedly.
- **Check what changed**: After a sync, look at any updated keys and make sure
  the changes make sense.
- **Use a trusted network**: Sync over a network you trust, not open public
  Wi-Fi you know nothing about.
