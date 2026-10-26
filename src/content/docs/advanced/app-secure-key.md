---
title: "Application Secure Key"
description: "How GpgFrontend protects the key it uses for its own saved data, and the choices you have: no extra protection, your computer's password store, or a PIN."
sidebar:
  label: Application Secure Key
  order: 8
---

GpgFrontend keeps one key of its own. This key locks the data the program
saves for you: settings, cached details, key server entries, and so on.

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

GpgFrontend stores its key in the place where your computer already keeps
passwords:

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

Point at the greyed-out choice to see why it is not available.

#### If the keychain is locked on Linux

On Linux, your password service may still be locked when GpgFrontend starts,
for example right after you log in. GpgFrontend then asks the system to
unlock it.

1. Your system shows its own unlock window. If you do not see it, look behind
   the GpgFrontend window and other open windows.
2. Type the password for your keyring. This is often your login password.

If the keychain stays locked, GpgFrontend shows **Secure Key Unavailable**.
Click **Show Details...** to see the reason your system gave. Then:

- Click **Quit**, unlock your keychain, and start GpgFrontend again. This
  costs nothing and keeps your data.
- Only click **Reset Secure Key** if you are sure the secret is gone for good.
  Everything the key protected becomes unreadable.

:::note[New in v2.2.3]

On Linux, GpgFrontend now asks the system to unlock a locked keychain, and
shows the system's reason when it cannot read it.

:::

### PIN at startup

You choose a PIN, and GpgFrontend asks for it every time it opens. Nothing it
saved can be read until you type it.

This is the strongest of the three. It is also the only one where you can
lose data.

:::caution[A forgotten PIN cannot be recovered]

There is no reset that keeps your data. If you cannot remember the PIN, the
only way to start the program again is to delete the key. Everything the key
was protecting then becomes unreadable forever.

GpgFrontend offers that as **Forgot PIN? Reset** after three wrong tries, and
warns you twice before doing it.

Your OpenPGP keys are not affected. Only the program's own saved data is.

:::

Use **Change PIN…** on the same settings page to pick a new one later. You
need the current PIN to do it.

### Profiles that have no choice

- A profile **opened from a file** uses the file's passphrase to protect its
  key. To change it, export the profile again with a new passphrase. See
  [Profiles](/advanced/profiles/).
- A [temporary profile](/advanced/temporary-profiles/) has no key protection
  at all. Its key is held in memory only and is destroyed when the window
  closes, so there is nothing to protect. All three choices are greyed out.

## Secure Level

On the same settings page, just above the key protection choices, you will
find **Secure Level**. It has four settings:

- **Standard**: no extra hardening. The default.
- **Enhanced**: wipes memory as soon as it is finished with it.
- **Strong**: also keeps sensitive memory out of the swap file.
- **Maximum**: also changes the program's internal key every week.

The first three are about memory, and are explained on
[Memory Security](/advanced/memory-security/).

**Maximum** is the only one that affects this page. It replaces the key with
a new one every week. So if someone steals an old copy of your saved data, it
soon becomes useless to them.

:::caution[Turning Maximum back off]

While Maximum is on, your data is saved with keys that keep changing. If you
lower the level, the program stops loading those keys, and anything saved
while Maximum was on can no longer be read. It is deleted a short while later.

GpgFrontend asks you to confirm this before it happens. The message is called
**Turn Off Weekly Key Rotation?** and ends with **Lower the level anyway?**.
Click **Yes** to go ahead, or **No** to keep Maximum.

:::

Changes on this page only take effect after GpgFrontend restarts. It offers to
restart for you.

## Where the Key Is Kept

The key lives inside the profile you are using, in a folder called `secure`.
If you use several [profiles](/advanced/profiles/), each has its own key, and
each can have its own protection setting.

:::note[Changed in v2.2.2]

Earlier versions tied the PIN to Secure Level 3 and set the level in an
`ENV.ini` file. Both are gone. Secure Level and key protection are now two
separate settings, and both live in **Settings**, **Advanced**.

The way the key protects your saved data also changed in v2.2.0. Some data
saved by much older versions may not be readable. This never affected your
OpenPGP keys, messages or files.

:::

### If the Key File Is Missing

The key is kept in a file called `app.key` in the `secure` folder. If that file
is gone, but the profile still holds data locked with it, GpgFrontend shows
**Secure Key Missing** when it starts. This usually happens when the data
folder was restored or copied without the key file.

- Click **Quit** to keep your data safe. Put `app.key` back from your backup,
  then start GpgFrontend again. Click **Show Details...** to see where the file
  is expected.
- Click **Create New Key** only if you cannot get the file back. A second
  window, **Reset to Default**, asks you to confirm. GpgFrontend then starts,
  but everything it locked with the old key can never be read again.

## Good Habits

- Back up your OpenPGP private keys and revocation certificates separately.
  This key is not a backup of anything.
- If you pick a PIN, write it down and keep it somewhere safe.
- If you want protection with nothing to remember, pick **System keychain**.
