---
title: "Application Data Storage"
description: "How GpgFrontend protects the data it saves for you, such as key server entries and key generation profiles."
sidebar:
  label: Application Data Storage
  order: 9
---

Besides your keys, GpgFrontend saves a few things of its own: key server
entries, key generation profiles, window positions, and so on. The sensitive
parts are encrypted with the program's own key.

This also holds the copy of your unsaved text editor tabs, when **Cache text
editor contents.** is on. It is on by default. See
[Unsaved Editor Tabs](/advanced/memory-security/#unsaved-editor-tabs).

All of this happens automatically. There is nothing to set up and nothing to
maintain. This page is here for people who want to know what is going on.

To clear this saved data (window positions, the key server list and similar),
open **Settings** > **General** and click **Clear All Data Objects** in the
**Data** box. Your keys are not touched. Sandboxed builds hide this button.

For the key that does the protecting, and the choices you have about it, see
[Application Secure Key](/advanced/app-secure-key/).

## How It Works

Each saved item is encrypted on its own, with its own key made from the
program's key and the item's name. Nothing is encrypted with one shared key,
so breaking into one item tells an attacker nothing about the others.

The encryption also detects tampering. If someone changes a file, GpgFrontend
notices and refuses to use it.

Files are written in a way that cannot leave a half-finished result behind. If
the program or the computer stops in the middle of a write, the old version
survives intact.

## Where the Files Are

The files live inside your profile, in a folder called `data_objs`. Each file
is named after a scrambled version of what it holds, so the file names give
nothing away.

Below **Maximum**, every [Secure Level](/advanced/memory-security/) uses the
same key, so you can move between them freely. **Maximum** uses keys that
change every week (see below). If you lower the level from **Maximum**, data
saved with those weekly keys can no longer be opened.

GpgFrontend clears out files whose key is gone. It waits a few days first
(3 days at **Strong** or **Maximum**, 7 days below that), then moves them
aside, and deletes them later.

## Key Changes

At the **Maximum** Secure Level, the program's key is replaced every week. Old
files stay readable because each one records which key it was written with, so
GpgFrontend can still open them. A file moves to the new key the next time
GpgFrontend saves it.

You never see this happen.

:::note[Changed in v2.2.0]

The way this data is protected changed in v2.2.0. Some data saved by v2.1.x or
earlier may not be readable any more.

This has never affected your OpenPGP keys, your messages, or your files. Only
GpgFrontend's own saved settings.

:::
