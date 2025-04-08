---
title: Key Server Operations
---

Key servers are essential components in the ecosystem of encrypted
communication, serving as centralized repositories for public key information.
They allow users to **share, retrieve, and update** public keys, making secure
communication possible even when direct key exchange is not feasible.

Key servers are especially helpful when:
- You need to encrypt a message but don't have the recipient’s public key.
- You want to make your public key available for others to use.
- You need to **update or revoke** your public key in case of a compromise.

GpgFrontend offers a convenient graphical interface for interacting with key
servers, making key search, import, export, and synchronization operations
straightforward for all users.

## 📥 Import Public Key From Key Server

To import a public key, go to the **Import Key** section in the main page or Key
Manager, and select the **Key Server** option.

![Import Key Server
UI](https://image.cdn.bktus.com/i/2023/11/16/d75cb252-9a65-5b73-01cd-a45b5ff501ef.webp)

### How to Import:
1. Choose a key server from the drop-down list.  
2. Enter a **Key ID**, **Fingerprint**, or **Email Address** into the search
   field.
3. Click **Search**.
4. If results are found, double-click a record to import the public key.

> 💡 By default, the key server list includes recommended options such as:
> - `https://keys.openpgp.org`
> - `https://keyserver.ubuntu.com`
>
> These servers are **preloaded as initial suggestions** in GpgFrontend, but you
> can fully customize this list through the **Settings → Key Servers**
> interface.

### After Importing

Once a key is imported:
- GpgFrontend will display a confirmation message.
- If a newer version of the key already exists locally, the import is skipped.

You can then verify:
- Key creation date
- UID and key ID
- Whether the key is expired or revoked (using Key Manager filters)

## 📤 Export My Public Key to Key Server

To publish your public key:

1. Open the **Key Details** interface for your key pair.
2. Go to the **Operations** tab.
3. Click **“Upload key pair to key server”**.

![Upload
Key](https://image.cdn.bktus.com/i/2023/11/16/87b435b1-3eb2-421d-c8cb-f6d926b6a1c7.webp)

> ⚠️ GpgFrontend only allows uploading if a **master key** is present to prevent
> accidental publishing of incomplete keys.

Note:
- Only **public key** data is uploaded.
- Private keys are **never** uploaded.

## 📤 Export My Public Key to Key Server

GpgFrontend allows you to upload your public key to a key server, making it
discoverable for others who wish to send you encrypted messages.

After v2.1.6, **GpgFrontend uses
[https://keys.openpgp.org](https://keys.openpgp.org)** for exporting public keys
by default. This server uses the **Verifying Keyserver (VKS) Interface**, which
provides extra protection against spam and key poisoning.

### Key Points:
- 🔐 **Only public keys are uploaded**, never private keys.
- ✅ **Master key is required** to export.
- ✉️ `keys.openpgp.org` requires email verification before your key becomes
  publicly searchable.
- 🧱 Uploaded keys are **propagated through the VKS protocol** and cannot be
  deleted.

To export:
1. Open the **Key Details** interface.
2. Go to the **Operations** tab.
3. Click **“Upload key pair to key server”**.

![](https://image.cdn.bktus.com/i/2023/11/16/87b435b1-3eb2-421d-c8cb-f6d926b6a1c7.webp)

## 🔄 Synchronize Public Key Information

If you want to ensure that your local key matches what is available on the key
server, use the **“Synchronize key pair with key server”** feature.

Like exporting, after v2.1.6, this operation also uses
**https://keys.openpgp.org** and its **VKS API**.

GpgFrontend will:
- Query the key server using your key’s fingerprint.
- Compare the server copy with your local one.
- Indicate if any update is applied.

> ⚠️ Synchronization is **not available** if you have the private key locally.
> In this case, you are expected to **publish** updates, not pull them.

## ⚙️ Key Server Related Settings

You can configure your key server preferences in:

> **Settings → Key Servers**

![](https://image.cdn.bktus.com/i/2023/11/16/afe69b9b-0576-d275-91df-79585c245b22.webp)

### Features:
- **Add a Server**: Enter the `https://` or `http://` address and click **Add**.
- **Edit a Server**: Double-click an address to edit it.
- **Delete a Server**: Right-click a row and select **Delete**.
- **Test Connection**: Click **Test** to check if the server is reachable.

> ✅ **Recommended**: Always use HTTPS to prevent man-in-the-middle attacks.

### 🌐 Set Default Key Server

To set a key server as your **default** for public key **search/import**
operations:

1. Right-click the desired server in the list.
2. Select **“Set as Default”**.
3. The default server will be marked in the first column of the table.

> ⚠️ **Important (v2.1.6 and later)**:
>
> Setting a default key server **only affects key searches/imports**.
>
> - **Export** and **Sync** operations are no longer affected by this setting.
> - These operations **always use `https://keys.openpgp.org`**, which implements
>   the Verifying Keyserver (VKS) API.
>
> This behavior ensures improved security and global consistency in public key
> management.

## Tips about Key Servers

| Key Server              | Fuzzy Search | VKS Interface | Notes                                     |
|-------------------------|--------------|---------------|-------------------------------------------|
| `keys.openpgp.org`      | ❌ No         | ✅ Yes        | Requires exact match (email, fingerprint) |
| `keyserver.ubuntu.com`  | ✅ Yes        | ❌ No         | Traditional HKP server, less strict       |

> 🔎 `keys.openpgp.org` does **not** support fuzzy search — you must use the
> **exact email**, **full fingerprint**, or **full key ID**.

> ⚠️ **Don't confuse search servers with export/sync servers** — even if you
> perform key searches using a custom server like `keyserver.ubuntu.com`,  
> **Export** and **Sync** operations will still use `keys.openpgp.org` by
> default in **GpgFrontend v2.1.6 and later**.

> 🛠️ **Want to restore previous behavior?**  
> You can disable the `KeyServerSync` module in the advanced settings.  
> This will prevent GpgFrontend from forcing export/sync operations to use
> `keys.openpgp.org`, allowing custom server logic to take effect again.

## 🔍 Automatically Check Key Publish Status

GpgFrontend v2.1.6 introduces a feature that automatically checks whether your
public key has been published on [keys.openpgp.org](https://keys.openpgp.org),
helping users keep track of their key visibility on the VKS-based keyserver.

### ✅ Feature Overview

- When enabled, GpgFrontend will fetch the **publish status** of a key from the
  key server.
- If the key is found to be published on `keys.openpgp.org`, a message like the
  following will be shown in the **Key Details** tab:

![](https://image.cdn.bktus.com/i/2025/04/09/40653adf-bf71-4038-77d3-3860f4fef106.webp)

### ⚙️ How to Enable

To activate this:

1. Go to `Settings → Network` tab.
2. Under **Network Ability**, check the box:
 - ✅ **Automatically fetch key publish status from key server**
3. Restart GpgFrontend to apply the change.

![](https://image.cdn.bktus.com/i/2025/04/09/6c6d4f27-ff0e-176a-305b-d4bbbaaa7d75.webp)

### ⚠️ Important Notes

- This feature **only works with `keys.openpgp.org`**, which supports the
  **Verifying Keyserver (VKS) API**.
- If the `KeyServerSync` plugin is **disabled**, the publish status will **not
  be fetched**, and no notice will appear in the UI.
- It is purely a **read-only status check**, and does not modify or upload
  anything to the server.

## 🔒 Final Notes

- Public keys uploaded to key servers are **distributed globally** and **cannot
  be deleted**.
- Always verify imported keys before using them.
- Maintain proper key hygiene: revoke and update keys when compromised.
- Never upload private key material to any server.