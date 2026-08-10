---
title: "Application Secure Key"
description: "How GpgFrontend protects the key it uses for its own saved data, and the choices you have: no extra protection, your computer's password store, or a PIN."
sidebar:
  label: Application Secure Key
  order: 8
---

GpgFrontend keeps one key of its own. It uses it to lock the things the
program saves for you: settings, cached details, key server entries, and
similar.

This is **not** one of your OpenPGP keys. It never touches your messages,
your files, or your keyring. GpgFrontend makes it for you the first time it
runs, and you never have to think about it.

Most people can stop reading here. The rest of this page is for people who
want more protection than the default.

## Your Three Choices

Open **Settings**, go to **Advanced**, and look at **Application Key
Protection**.

### No extra protection

The default. The key sits in a file that only your user account can read.

This is fine for a computer only you use. Anyone who can read your files
could also read the key, but someone with that much access could read most
of your other things anyway.

### System keychain

GpgFrontend hides its key in the place your computer already keeps passwords:

- **Windows**: Credential Manager
- **macOS**: your login keychain
- **Linux**: your password service, such as GNOME Keyring or KWallet

Nothing changes for you day to day. The program never asks you for anything.
It just means the key file on its own is useless to someone who copies it.

This choice is greyed out when it cannot work:

- On a **portable** copy, because the store belongs to one computer and a
  portable copy has to run on any of them.
- On a profile you **opened from a file**, for the same reason. That file is
  already protected by its own passphrase.
- On Linux, when **no password service is set up**. Install one and switch it
  on, then try again.

### PIN at startup

You choose a PIN, and GpgFrontend asks for it every time it opens. Nothing it
saved can be read until you type it.

This is the strongest of the three. It is also the only one where you can
lose data.

:::caution[A forgotten PIN cannot be recovered]

There is no reset that keeps your data. If you cannot remember the PIN, the
only way to start the program again is to throw the key away, and everything
it was protecting becomes unreadable for good.

GpgFrontend offers that as **Forgot PIN? Reset** after three wrong tries, and
warns you twice before doing it.

Your OpenPGP keys are not affected. Only the program's own saved data is.

:::

Use **Change PIN** on the same settings page to pick a new one later. You need
the current PIN to do it.

## Secure Level

On the same settings page, just above the key protection choices, you will
find **Secure Level**. It has four settings:

- **Standard**: no extra hardening. The default.
- **Enhanced**: wipes memory as soon as it is finished with it.
- **Strong**: also keeps sensitive memory out of the swap file.
- **Maximum**: also changes the program's internal key every week.

The first three are about memory, and are explained on
[Memory Security](/advanced/memory-security/).

**Maximum** is the only one that affects this page. It swaps the key for a
fresh one every week, so an old copy of your saved data stops being useful
quickly.

:::caution[Turning Maximum back off]

While Maximum is on, your data is saved with keys that keep changing. If you
lower the level, the program stops loading those keys, and anything saved
while Maximum was on can no longer be read. It is deleted a short while later.

GpgFrontend asks you to confirm this before it happens.

:::

Changes on this page only take effect after GpgFrontend restarts. It offers to
restart for you.

## Where the Key Is Kept

Inside the profile you are using, in a folder called `secure`. If you use
several [profiles](/advanced/profiles/), each has its own key, and each can
have its own protection setting.

:::note[Changed in v2.2.2]

Earlier versions tied the PIN to Secure Level 3 and set the level in an
`ENV.ini` file. Both are gone. Secure Level and key protection are now two
separate settings, and both live in **Settings**, **Advanced**.

The way the key protects your saved data also changed in v2.2.0. Some data
saved by much older versions may not be readable. This never affected your
OpenPGP keys, messages or files.

:::

## Good Habits

- Back up your OpenPGP private keys and revocation certificates separately.
  This key is not a backup of anything.
- If you pick a PIN, write it down and keep it somewhere safe.
- If you want protection with nothing to remember, pick **System keychain**.
