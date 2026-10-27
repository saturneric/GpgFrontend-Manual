---
title: Read Mail from Your Server
description: "Browse the folders on your mail server with the IMAP Controller, open a message in GpgFrontend, and save or open its attachments safely."
sidebar:
  label: Read Mail
  order: 5
---

GpgFrontend can fetch messages from your mail server, so you can check and
decrypt them right away. It does this with the **IMAP Controller**.

**IMAP** is the way email apps talk to the server that keeps your mailbox.

:::note[New in v2.2.3]

The IMAP Controller is new. Before, you had to save each message as a file in
another email app first.

:::

## Before You Start

You need a mail account with receiving turned on. See
[Mail Accounts and Sending](/email/accounts-sending/). In short: add the
account with **Send and receive** or **Receive only**, or check **Use this
account to receive** on an existing one. Disabled accounts are not listed.

## Open the IMAP Controller

1. Click **Advanced** > **Open IMAP Controller**.
2. The **IMAP Controller** window opens and connects to your account.

If you have no account with receiving turned on, GpgFrontend says **No mail
account** and asks you to set one up in Settings first.

The **Advanced** menu is hidden in the Mac App Store edition. There, the IMAP
Controller is not available.

## It Only Reads

The IMAP Controller is for looking, not for changing. It does not delete, move
or send anything. Opening a message here does not mark it as read on the
server.

To answer, sort or delete mail, use your usual email app.

## Find a Message

At the top of the window:

- **Account**: pick the mail account to look in.
- **Folder**: pick a folder, such as your inbox.
- **Search subject or sender**: type a word to find matching messages.
- The refresh button (**Reload this folder from the server**) fetches the
  folder again.

The message list shows the subject, the sender and the date. Click a message
to see its details on the right: subject, sender, date, size, **Message-ID**
and **Folder**.

Messages come in pages of 50. Use **Previous** and **Next** to move between
pages. The bottom of the window shows where you are, for example **Page 1 of
4**.

If a search finds very many messages, only the first ones are shown. Type more
words to narrow it down.

### Remembered Folder Lists

When you open an account again, GpgFrontend first shows the list from your
last visit, so you do not stare at an empty window. It says **Shown from the
previous visit to this account; refreshing.** while it gets the newest list
from the server.

## Open a Message

1. Select a message in the list.
2. Click **Open**.

The message is downloaded and opens in a **new tab**. The window says **Opened
in a new tab.**

From there you can check and decrypt it like any other message. See
[Verify and Inspect a Message](/email/verify-inspect/). You can also save it as
an `.eml` file.

Right-click a message for more: **Open**, **Copy Subject**, **Copy Sender** and
**Copy Message-ID**.

While something is loading, the **Close** button turns into **Stop**. Click it
to stop.

### Very Large Messages

A message larger than 64 MiB cannot be opened. If you select one, the details
say: "This message is too large for this application to open, so it cannot be
imported." Use your usual email app for such a message.

## Work With Attachments

Attachments are listed under the message, with their **Name**, **Type**,
**Size**, and whether they are **Signed**. Click **Expand** to see every file,
or **Collapse** to show only a summary.

The **Signed** column tells you if a file is covered by the message's
signature:

- **signed**: covered, and the signature is good.
- **signed, not checked**: covered, but the signature has not been checked yet.
- **signed, could not be checked**: covered, but the check gave no answer.
- **signature not good**: covered by a signature that failed. Do not trust it.
- **unsigned**: not covered. Anyone could have added this file.

### Attachment Actions

Click **Attachments** on the action row, or right-click a file in the list:

- **Open**: open the file with the app your computer uses for it.
- **Save...**: save the selected files to a folder.
- **Save All...**: save every attachment to a folder.
- **Import Key**: import the file into your key database. This shows only when
  the file is an OpenPGP key.
- **Remove**: take the selected files out of the message. This only works on a
  message you can edit.
- **Copy Name**: copy the file name.

With **Save All...**, a file never replaces one that is already in the folder.
If a name is taken, GpgFrontend saves the file under a new name and tells you.

Removing an attachment from a message you received cannot be undone. Save it
first if you might need it.

### Which Files It Will Open

GpgFrontend opens only files that are safe to look at:

- **Documents**: such as PDF, text, Word, Excel, PowerPoint, OpenDocument,
  CSV, RTF and EPUB.
- **Pictures**: such as PNG, JPEG, GIF, WebP and HEIC.
- **Sound and video**: such as MP3, WAV, MP4 and MKV.
- **Plain data files**: such as JSON, XML, YAML, calendar (`.ics`) and contact
  (`.vcf`) files, and other emails (`.eml`).

Everything else is refused, for example programs, scripts, shortcuts,
installers, archives such as ZIP, and SVG images. A file from a stranger that
"opens" might really **run**, and that could harm your computer. An archive is
refused because you cannot tell what is inside until it is unpacked.

When a file is refused, GpgFrontend explains why. You can still click
**Save...**, then open the file yourself if you are sure where it came from.

### Size Limit When Attaching

When you add a file to your own message with **Attach File...**, each file can
be up to 48 MiB. Bigger files are refused with a message that names them.
