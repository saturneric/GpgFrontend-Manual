---
title: "Portable Mode"
description: "Run GpgFrontend from a USB drive with a portable download, keeping all data and settings next to the application and leaving nothing on the host computer."
sidebar:
  label: Portable Mode
  order: 2
---

A **portable** copy of GpgFrontend keeps everything in its own folder, right
next to the program. Nothing is written to the computer's user folders, so
nothing of yours is left behind.

Use it when you want to:

- Run GpgFrontend **from a USB drive** and carry it between computers.
- Use GpgFrontend on a **shared or borrowed computer**.
- **Move your whole setup** by copying one folder.

## You Choose It When You Download

Portable is not a setting inside the program. It is a separate download.

On the [Downloads](/overview/downloads/) page you will find two kinds of file
for each system:

- **Installed**: the normal choice. Settings and keys go in your user folder.
- **Portable**: everything stays in the program's own folder.

Pick the portable one and unpack it wherever you want it, such as onto a USB
drive. That is all there is to it.

:::note[Changed in v2.2.2]

Older versions had a `PortableMode=true` switch in an `ENV.ini` file, and
before that a `PORTABLE.txt` file. Both are gone. If you were using one, they
no longer do anything, and you should download the portable build instead.

:::

:::caution[The two do not share anything]

An installed copy and a portable copy keep completely separate data. Moving
from one to the other looks like starting from scratch. Your keys are not
carried over on their own.

To bring a setup across, see [Profiles](/advanced/profiles/). You can save your
whole setup to one file and open it in the other copy.

:::

## Where Things Are Kept

A portable copy stores its settings, keys, logs and modules in the folder it
was unpacked into. On Linux, an AppImage uses the folder that holds the
`.AppImage` file.

That means whoever holds the drive holds your keys. Keep it somewhere safe,
and use a strong passphrase on your private keys.

## What a Portable Copy Cannot Do

A portable copy cannot use your computer's password store to protect its own
key. That store belongs to one computer, and a portable copy has to work on
any computer you plug it into.

That option is greyed out for you, so there is nothing to do. See
[Application Secure Key](/advanced/app-secure-key/) if you want the details.

## Tip: Moving Between Computers

If you use several [key databases](/advanced/key-database/), turn on the
**Relative Path** option for each one. The paths then keep working even when
the drive gets a different letter or mount point on the next computer.
