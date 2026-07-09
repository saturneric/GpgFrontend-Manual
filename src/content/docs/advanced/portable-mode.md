---
title: "Portable Mode"
description: "Run GpgFrontend in Portable Mode from a USB drive, keeping all data and configuration in the app directory and leaving no trace on the host."
sidebar:
  label: Portable Mode
  order: 1
---

Normally, GpgFrontend saves its settings and data in your system's user
folders. **Portable Mode** changes that: everything is saved next to the
application itself, in one folder.

Use it when you want to:

- Run GpgFrontend **from a USB drive** and carry it between computers.
- Use GpgFrontend on a **shared or temporary computer** without leaving your
  data behind on it.
- **Back up or move** the whole application, with all its settings, by copying
  one folder.

## How It Works

With Portable Mode on:

- All configuration, logs, application data, secure keys, and modules are
  stored inside the application's own folder.
- Nothing is written to the system's user data folders. No personal data is
  left on the host computer.

It works the same way on Windows, Linux, and macOS. On Linux, the AppImage and
Flatpak builds are detected automatically, and data is placed in the
application directory accordingly.

## Turn Portable Mode On

1. Open the folder where the GpgFrontend program is located (its working
   directory).

2. Find the file named `ENV.ini`. If it does not exist, create it.

3. Add this line to the file:

   ```ini
   PortableMode=true
   ```

4. Save the file and restart GpgFrontend.

That's it. From now on, GpgFrontend keeps all of its files inside its own
folder.

:::tip[Turn it on before you start using the app]

You can enable Portable Mode at any time, but it is best to do it **before you
set up GpgFrontend for the first time**. That way, all your data is portable
from the start, and nothing is left in the system folders.

:::

## Turn Portable Mode Off

1. Open `ENV.ini` again.

2. Change the line to `PortableMode=false`, or delete the line.

3. Restart GpgFrontend.

The data already stored in the portable folder stays where it is, but new data
is saved to the default system folders again.

## Tip: Moving Between Computers

If you use several [key databases](/advanced/key-database), turn on the
**Relative Path** option for each one. Then the database paths keep working
even when the drive gets a different letter or mount point on another
computer.

## Older Versions

The `ENV.ini` method works in GpgFrontend v2.1.9 and later. In versions before
v2.1.9, you enabled Portable Mode differently: by creating an empty file named
`PORTABLE.txt` in the working directory.
