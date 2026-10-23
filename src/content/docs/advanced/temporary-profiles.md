---
title: "Temporary Profiles"
description: "Open a throwaway GpgFrontend setup in its own window. Use it for a quick test or on a borrowed computer, and everything in it is destroyed when you close it."
sidebar:
  label: Temporary Profiles
  order: 2
---

A **temporary profile** is a [profile](/advanced/profiles/) that only lasts as
long as its window. It starts empty: no keys, no saved state. When you close
its window, everything in it is destroyed: its keys, its settings and its
files.

:::note[New in v2.2.3]

Temporary profiles were added in GpgFrontend v2.2.3.

:::

## When to Use One

- **A quick test.** You want to try a setting, a key, or a feature without
  touching your real setup.
- **A borrowed computer.** You need to decrypt or sign something on a computer
  that is not yours, and you do not want to leave anything behind.
- **A clean start.** You want to see how GpgFrontend behaves with no keys at
  all, for example to follow a guide step by step.

Your normal profile is not touched. It stays exactly as it was in its own
window.

## Start a Temporary Profile

There are three ways. Each one opens a **new window** for the temporary
profile.

### From the menu

1. Open **Profiles** in the menu bar.
2. Choose **New Temporary Profile**.

### From Manage Profiles

1. Open **Profiles**, then **Manage Profiles...**.
2. Click **New Temporary**.

### From a terminal

```bash
gpgfrontend --temp-profile
```

:::note[Not in the Mac App Store Lite edition]

The Lite edition from the Mac App Store has no **Profiles** menu, so it cannot
open temporary profiles.

:::

## What It Starts With

- **Keys**: none. The temporary profile has its own empty keyring. Import or
  make the keys you need inside it.
- **Settings**: when you start it from the menu or from **Manage Profiles**,
  it copies the settings of the window you started it from. These are the same
  groups the [New Profile](/advanced/profiles/#pick-which-settings-to-copy)
  window offers: engine and GnuPG, rPGP passphrase handling, everyday
  behaviour, language and appearance, and diagnostics. When you start it from a
  terminal, it starts with the normal default settings.

Keys, key databases, the workspace folder, key protection and proxy
credentials are never copied.

To check that you are in a temporary profile, point at the profile name in the
status bar at the bottom right of the window. It says the profile is not kept
on this computer, and that everything in it is destroyed when the window
closes.

## Close a Temporary Profile

When you close the window, GpgFrontend asks **Destroy Temporary Profile?**. It
warns that everything in the profile will be destroyed: its keys, settings and
files.

- Click **Destroy and Close** to throw it all away and close the window.
- Click **Cancel** to go back to the window.

There is no way to get a temporary profile back once it is destroyed.

### Keep It Instead

If you decide you want to keep what you made, save it first:

1. In the **Destroy Temporary Profile?** message, click **Cancel**.
2. Open **Profiles**, then **Export This Profile...**.
3. Save it to a file, as described in
   [Save a Profile to a File](/advanced/profiles/#save-a-profile-to-a-file).
4. Close the window again and click **Destroy and Close**.

Later you can open or import that file like any other profile file.

## Limits

### Settings that need a restart

Some settings only take effect after GpgFrontend restarts. A restart starts a
new copy of the program, and that would destroy the temporary profile. So the
program refuses: it shows **Restart Not Possible**, and lists the settings
pages with changes that need a restart.

- On Windows and Linux, the settings window stays open. Undo those changes, or
  click **Cancel** to throw away everything you changed in the settings window.
- On macOS, the settings window closes and all the changes you made in it are
  thrown away.

### No key protection

A temporary profile's own key is made fresh, held in memory only, and
destroyed with the window. There is nothing on disk to protect, so the
[Application Key Protection](/advanced/app-secure-key/) choices are greyed out.

### Where it is kept

While it is open, the temporary profile is kept in the safest place this
computer offers: memory, an encrypted folder, or an ordinary folder. See
[Where the Open File Is Kept](/advanced/profiles/#where-the-open-file-is-kept).
