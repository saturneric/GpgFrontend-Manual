---
title: Key Server Operations
description: "Find public keys on key servers, publish your own key, refresh keys you already have, and choose which key servers GpgFrontend uses."
sidebar:
  order: 15
---

A **key server** is a place on the internet that stores public keys. Think of it
as a public phone book for keys. You can use it to **find, share and update**
public keys.

Key servers are handy when:

- You want to encrypt a message but you do not have the other person's public
  key.
- You want other people to be able to find your public key.
- You want the newest copy of a key, for example to see if its owner has revoked
  (cancelled) it.

GpgFrontend gives you simple buttons and windows for all of this. You do not
need to type any commands.

:::note[Changed in v2.2.3]

Publishing and refreshing now work on many keys at once, and you can check
whether a key is published. The old **Sync Public Key** button in the Key
ToolBox was removed. So was the **Network Ability** option in **Settings**,
**Network** that checked publish status by itself. Use
**Refresh Public Key From Key Server** and **Check Publication Status** instead.

:::

## Find and Import a Key

1. In the main window, click **Keys** in the menu bar, then **Import Key**, then
   **Key Server**. You can also click the **Import** button in the toolbar and
   choose **Key Server**.

   ![][img-1]

2. A search window opens. Under **Key Server**, choose a server from the list.
3. Under **Search Type**, choose **By Key ID**, **By Email** or **By
   Fingerprint**.
4. Type what you are looking for in the **Search Value** box.
5. Click **Search**, or press Enter.
6. Double-click a result to import that key.

![][img-2]

Type the full value. A key ID has 8 or 16 characters. A fingerprint has 16, 40
or 64 characters. Some servers, such as `keys.openpgp.org`, only find a key when
you type the exact email address or the full fingerprint.

### After You Import

When a key comes in, GpgFrontend shows a message to confirm it. If you already
have that key, anything new is added to your copy.

You can then check the key in the key list:

- when the key was made;
- its user ID and key ID;
- whether it is expired or revoked.

![][img-3]

## Work With One Key

Each key has its own key server buttons.

1. Open the key's details, for example by double-clicking the key in the key
   list.
2. Go to the **Operations** tab.
3. Click **Key Server Operations**. A small menu opens with three items:
   - **Publish Public Key to Key Server**: upload this public key to your
     default key server.
   - **Refresh Public Key From Key Server**: download the newest copy of this
     key from your default key server.
   - **Check Publication Status**: ask your default key server whether it has
     this key.

![][img-4]

The **Operations** tab is not shown for a revoked key.

### Publish Your Key

Publishing lets other people find your public key.

- **Only your public key is uploaded.** Your private key is never sent.
- Once a key is on a key server, it can spread to other servers. It may be
  impossible to remove it.

What happens next depends on your default key server:

- If the server supports **VKS** (a kind of key server that checks email
  addresses, such as `keys.openpgp.org`), GpgFrontend uploads the key and shows
  each email address with its status. The server then sends you an email. Click
  the link in it, or other people cannot find your key by its email address.
- If the server only supports **HKP** (the older kind), GpgFrontend first asks
  **Publish Without Verification?**. The server does not confirm your email
  address, and the upload cannot be undone. Click **OK** only if you are sure.

### Refresh a Key

Refreshing downloads the newest copy of a key and adds it to your keys. Use it
to see if someone has changed or revoked their key. It works for any key,
including your own.

If the server does not have the key, the message says "The key server does not
have this key."

### Check Whether a Key Is Published

Click **Check Publication Status**. A **Publication Status** message tells you
one of these:

- the key is published on the server;
- the key is not published on the server;
- GpgFrontend could not ask the server, with the reason.

GpgFrontend never checks this by itself. Asking tells the server which key you
are interested in, so it only asks when you click.

:::note[New in v2.2.3]

**Check Publication Status** is new in v2.2.3.

:::

## Work With Many Keys at Once

You can publish or refresh many keys in one go.

1. In a key list, tick the keys you want. If you tick nothing, GpgFrontend uses
   the keys you selected (clicked) instead.
2. Choose one of these:
   - Right-click the keys, then choose **Publish Public Key to Key Server** or
     **Refresh Public Key From Key Server**.
   - In the **KeyPair Management** window, open the **Operations** menu and
     choose one of the same two items.

These items are greyed out when your choice includes a key group. A key group is
not a key, so a key server cannot hold it.

When the work is done, a message such as **Key Publishing Finished** or **Key
Refresh Finished** sums it up, for example "3 of 4 keys were published to the
key server keys.openpgp.org." A **Failed:** list follows, with one line per key
that did not work.

Good to know:

- Only one batch runs at a time. If you start another, GpgFrontend says "A key
  server operation is already running. Try again when it has finished."
- If your key databases change while a batch runs, the batch stops, and a **Key
  Refresh Stopped** or **Key Publishing Stopped** message says how far it got.
  Nothing fetched is imported. Start it again.
- GpgFrontend waits up to 15 seconds for each answer from the server.

:::note[New in v2.2.3]

Publishing and refreshing many keys at once is new in v2.2.3.

:::

## Choose Your Key Servers

You decide which key servers GpgFrontend uses.

1. Open **Settings** (on macOS, **Preferences**).
2. Under **Keys & Engines**, choose **Key Servers**.

The **Key Server List** shows each server with these columns: **Default**,
**Address**, **HKP**, **VKS**, **Status** and **Last Tested**.

GpgFrontend starts with two servers:

- `https://keys.openpgp.org`, the default. It supports HKP and VKS.
- `https://keyserver.ubuntu.com`. It supports HKP.

### Add a Server

1. Type the address in the box under **Add a Key Server**, for example
   `https://keys.example.org`.
2. Click **Add**.

GpgFrontend tests the new server right away. If the server does not answer like
a key server, GpgFrontend still adds it, marks it **Unverified**, and tells you.
If the address starts with `http://` instead of `https://`, GpgFrontend warns
you first, because anyone on the network could see and change what you send.

### Change the Default Server

Select a server, then click **Set As Default**.

The default server matters. Publishing, refreshing and **Check Publication
Status** always use it. They use VKS when the server offers it, and HKP
otherwise. If a tested server has no VKS, GpgFrontend warns you with **No
Verified Publishing** before it makes the change.

Searching uses HKP, and you can pick any server from the list in the search
window.

### Test or Delete a Server

- **Test Selected**: test the selected server again and update its **Status**.
- **Delete Selected**: remove the selected server from the list.

:::note[Changed in v2.2.3]

Before v2.2.3, publishing always used `keys.openpgp.org`. Now it uses the
default server you choose here.

:::

## If the Key Server Items Are Missing

All of these features come from the **KeyServerSync** module, which ships with
GpgFrontend. If you cannot find **Key Server** in the **Import Key** menu, or
the **Key Servers** settings page, the module is turned off. See
[Module Controller](/advanced/module-controller/).

## Final Reminders

- Public keys you upload can spread around the world and may never be deleted.
- Always check a key before you trust it. Compare its fingerprint with its
  owner.
- Revoke your key and publish the change if your private key is stolen.
- Never upload a private key to any server.

[img-1]:
  https://image.cdn.bktus.com/i/2025/06/24/3660f65893c4e79954486f1b3cfb5cb6b09a13d0.webp
[img-2]:
  https://image.cdn.bktus.com/i/2025/06/24/0dc8821cc3c83c7bb3266f3a1059ce59fabc4a8f.webp
[img-3]:
  https://image.cdn.bktus.com/i/2025/06/24/4efe7862bc47b95387a8ee247d4b767dbbfa36b6.webp
[img-4]:
  https://image.cdn.bktus.com/i/2025/06/24/34505c6435d485dc2f8ce680a8c8f630fbb18b2a.webp
