---
title: "Memory Security"
description: "Choose how hard GpgFrontend works to keep passphrases and decrypted text out of memory once it is finished with them."
sidebar:
  label: Memory Security
  order: 10
---

While GpgFrontend works, your passphrases and your decrypted text have to sit
in the computer's memory. **Secure Level** decides how much effort the program
puts into clearing them out again afterwards.

The default is fine for most people. Raise it if you handle something you
would not want recovered from a memory dump or a swap file.

## Change It

Open **Settings**, go to **Advanced**, and set **Secure Level**.

The change takes effect after GpgFrontend restarts. It offers to restart for
you.

:::note[Changed in v2.2.2]

Older versions set this by putting a line like `SecureLevel=1` in an `ENV.ini`
file next to the program. That file is no longer read. Use the settings page.

:::

## The Levels

The old version numbers are in brackets, in case you are used to them.

### Standard (0)

The default. Normal memory, with no extra work.

Even here, GpgFrontend does not simply leave things lying around. Whenever it
reads text out of a box on screen, it copies it into its own buffer and wipes
the original straight away.

Choose this if you want the best speed and the fewest surprises.

### Enhanced (1)

Everything sensitive goes into buffers that are wiped clean when they are
allocated and wiped again when they are released.

This costs almost nothing and is a sensible step up.

### Strong (2)

Everything from Enhanced, plus the memory holding your secrets is **locked**.
Locked memory cannot be written to the swap file or into a hibernation image,
so it does not end up on your disk by accident.

GpgFrontend also clears the text box and its undo history before encrypting or
decrypting, so your plain text cannot be brought back with Ctrl+Z.

This is the strongest memory protection, and what to pick if you are handling
something sensitive.

### Maximum (3)

Everything from Strong. It adds no further memory protection.

What it adds instead is that GpgFrontend changes its own internal key every
week. That is about the data the program saves, not about memory, and it has a
catch worth reading before you turn it on. See
[Application Secure Key](/advanced/app-secure-key/).

## What Strong and Maximum Need

Locking memory is something the operating system has to allow, and some
systems limit how much any one program may lock.

If your system will not allow it, GpgFrontend does not fail. It falls back to
the best protection it can actually get.

On Linux you may need to raise the memory locking limit for your user if you
want the full effect.

## What This Cannot Do

GpgFrontend keeps your secrets in memory for as short a time as it can, avoids
making extra copies, and wipes what it can before letting memory go.

It cannot protect you from someone who already controls your computer. If
malware is running as you, or someone has your unlocked machine, no memory
setting saves you.
