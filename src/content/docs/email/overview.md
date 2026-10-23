---
title: Email Overview
description: "What the Email feature in GpgFrontend can do, where to find it, and which page to read for each task."
sidebar:
  label: Overview
  order: 1
---

GpgFrontend has its own email tools. With them you can write a message, sign
it, encrypt it, and send it. You can also read messages from your mail server
and check them.

:::note[New in v2.2.3]

GpgFrontend can now send email and read it from your mail server. Before, it
could only work with email files, and your normal email app had to do the
sending and receiving.

:::

## What You Can Do

- **Write** a message, with From, To, Cc, Bcc, Subject and attachments.
- **Sign** it, so the reader can tell it came from you and was not changed.
- **Encrypt** it, so only the people you choose can read it.
- **Send** it through your own mail account.
- **Read** messages from your mail server.
- **Check** a message you received: is the signature good, and can you open it?

Every email is kept as an `.eml` file. This is a common email file format. Most
email apps can open it and save it. So you can still move messages between
GpgFrontend and your usual email app if you like.

All signing, encrypting, checking and decrypting happens on your own computer.
Your private keys never leave it.

## Where to Find It

There are two ways in:

- **To write a new message:** click **File** > **Workspace** > **Mail Editor**.
  A new tab opens with an empty message.
- **To read messages from your mail server:** click **Advanced** > **Open IMAP
  Controller**. A window opens where you can browse your folders.

You can also open an `.eml` file you already have, for example from the
[File Panel](/guides/understand-interface/#file-panel). It opens in a mail tab,
the same kind of tab as a new message.

Before you can send or read mail from a server, you need to add your mail
account. See [Mail Accounts and Sending](/email/accounts-sending/).

:::note[Don't see Open IMAP Controller?]

The **Advanced** menu is hidden in sandboxed builds, such as Flatpak or the Mac
App Store edition. In those builds, **Open IMAP Controller** is not available.

If no account has receiving turned on, the app tells you to set one up in
Settings first.

:::

## The Status Panel in Mail Tabs

In a mail tab, the **Status Panel** at the bottom starts small, as a thin bar.
This leaves more room for the message, its headers and its attachments. The
panel opens by itself when there is a new result to show, for example after
you sign or verify a message.

## Which Page Do I Need?

- **I want to write, sign or encrypt a message.** Read
  [Write and Protect a Message](/email/compose-protect/).
- **I got a message and want to know if I can trust it.** Read
  [Verify and Inspect a Message](/email/verify-inspect/).
- **I want to set up my mail account, or send a message.** Read
  [Mail Accounts and Sending](/email/accounts-sending/).
- **I want to read messages from my mail server, or work with attachments.**
  Read [Read Mail from Your Server](/email/reading-imap/).
