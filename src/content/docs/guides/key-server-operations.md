---
title: Key Server Operations
description: "Search, import, export, and synchronize OpenPGP public keys with key servers using GpgFrontend's graphical interface."
---

A key server is a place on the internet that stores public keys. Think of it as a
public phone book for keys. You can use it to **share, find, and update** public
keys.

Key servers are handy when:

- You want to encrypt a message but you don't have the other person's public key.
- You want other people to be able to find your public key.
- You need to **update or cancel (revoke)** your public key, for example if it
  was stolen.

GpgFrontend gives you simple buttons and windows to search, import, export, and
sync keys. You do not need to type any commands.

## Import a public key from a key server

1. **Open the import menu.** In the Operations Bar at the top of the main window,
   click the Import Key button (the one with a downward arrow).
2. **Pick "Keyserver".** In the drop-down menu, choose Keyserver as the source.

![](https://image.cdn.bktus.com/i/2025/06/24/3660f65893c4e79954486f1b3cfb5cb6b09a13d0.webp)

### Steps to import

1. Choose a key server from the drop-down list.
2. Type a **Key ID**, **Fingerprint**, or **Email Address** in the search box.
3. Click **Search**.
4. When you see a result, double-click it to import the key.

![](https://image.cdn.bktus.com/i/2025/06/24/0dc8821cc3c83c7bb3266f3a1059ce59fabc4a8f.webp)

> GpgFrontend already lists a few key servers for you, such as:
>
> - `https://keys.openpgp.org`
> - `https://keyserver.ubuntu.com`
>
> These are just suggestions to start with. You can change the list in
> **Settings → Key Servers**.

### After you import

When a key comes in:

- GpgFrontend shows a message to confirm it worked.
- If you already have a newer copy of that key, the import is skipped.

You can then check:

- When the key was made
- The UID and key ID
- Whether the key is expired or revoked (use the Key Manager filters)

![](https://image.cdn.bktus.com/i/2025/06/24/4efe7862bc47b95387a8ee247d4b767dbbfa36b6.webp)

## Send your public key to a key server

You can upload your public key so other people can find it and send you encrypted
messages.

Since v2.1.6, GpgFrontend uploads keys to
[https://keys.openpgp.org](https://keys.openpgp.org) by default. This server uses
the **Verifying Keyserver (VKS) Interface**, which gives extra protection against
spam and fake keys.

### Things to know

- **Only your public key is uploaded.** Your private key is never sent.
- You need your **master key** to upload.
- `keys.openpgp.org` asks you to confirm your email before other people can find
  your key. Once a key is uploaded, it spreads to other servers and **cannot be
  deleted**.

To upload:

1. Open the **Key Details** window.
2. Go to the **Operations** tab.
3. Click **"Upload key pair to key server"**.

![](https://image.cdn.bktus.com/i/2025/06/24/34505c6435d485dc2f8ce680a8c8f630fbb18b2a.webp)

## Sync a public key

If you want your local copy of a key to match the copy on the key server, use the
**"Synchronize key pair with key server"** feature.

Like uploading, since v2.1.6 this uses **https://keys.openpgp.org** and its
**VKS API**.

GpgFrontend will:

- Look up the key on the server using its fingerprint.
- Compare the server copy with your copy.
- Tell you if anything was updated.

:::caution[Sync or publish]

You cannot sync a key if you have its private key on your computer. In that case
you are the owner, so you should **publish** your updates instead of pulling them.

:::

## Things to know about key servers

| Key server             | Fuzzy search | VKS interface | Notes                                     |
| ---------------------- | ------------ | ------------- | ----------------------------------------- |
| `keys.openpgp.org`     | ❌ No        | ✅ Yes        | Needs an exact match (email, fingerprint) |
| `keyserver.ubuntu.com` | ✅ Yes       | ❌ No         | Older HKP server, less strict             |

> `keys.openpgp.org` does **not** do fuzzy search. You must use the **exact
> email**, **full fingerprint**, or **full key ID**.

## Check if your key is published

GpgFrontend v2.1.6 can check on its own whether your public key is published on
[keys.openpgp.org](https://keys.openpgp.org). This helps you know if people can
find your key.

### What it does

- When turned on, GpgFrontend asks the server whether your key is published.
- If your key is found on `keys.openpgp.org`, you see a message in the **Key
  Details** tab, like this:

![](https://image.cdn.bktus.com/i/2025/06/24/e52d18a85267987f8202ba6ede39068b3c6e140b.webp)

### How to turn it on

1. Go to the `Settings -> Network` tab.
2. Under **Network Ability**, check the box: `Automatically fetch key publish
status from key server`.
3. Restart GpgFrontend to apply the change.

![](https://image.cdn.bktus.com/i/2025/06/24/b2daf0876b29278e703f4721f7f68c22ffa1752b.webp)

### Notes

- This works **only with `keys.openpgp.org`** (the one with the VKS API).
- If the `KeyServerSync` module is **off**, the status is **not checked** and no
  message appears.
- It only **reads** the status. It does not change or upload anything.

## Final reminders

- Public keys you upload spread around the world and **cannot be deleted**.
- Always check a key before you trust it.
- Keep your keys clean: revoke and update them if they are stolen.
- Never upload a private key to any server.
