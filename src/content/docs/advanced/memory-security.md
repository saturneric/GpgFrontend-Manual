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

Everything sensitive goes into memory buffers that are wiped clean before use
and wiped again after use.

This costs almost nothing and is a sensible step up.

### Strong (2)

Everything from Enhanced, plus the memory holding your secrets is **locked**.
Locked memory cannot be written to the swap file or into a hibernation image,
so it does not end up on your disk by accident.

This is the strongest memory protection. Pick it if you are handling
something sensitive.

### Maximum (3)

Everything from Strong. It adds no further memory protection.

Instead, it makes GpgFrontend replace its own internal key every week. That
is about the data the program saves, not about memory, and it has a catch
worth reading before you turn it on. See
[Application Secure Key](/advanced/app-secure-key/).

## Undo After an Operation

When you encrypt or decrypt text, the result replaces what was in the editor
tab. If undo were allowed there, pressing Ctrl+Z after encrypting would bring
your plain text back. To allow that, the program would have to keep the plain
text in memory.

So by default, you **cannot** undo an encrypt, decrypt or other operation in
the text editor. The old text is gone once the result appears.

If you want undo back:

1. Open **Settings** and go to **General**.
2. Under **Operation**, tick **Allow undoing encrypt, decrypt and other
   operations in the text editor.**
3. Click **OK**. On macOS, close the window instead.

Leave it off if you handle sensitive text. As the setting's tip says, undo
keeps the previous text in memory, and after encrypting that is the
plaintext.

:::note[Changed in v2.2.3]

Undo after an operation is now off by default, and has its own setting.

:::

## Unsaved Editor Tabs

The setting **Cache text editor contents.** is on by default. It keeps the
text in your editor tabs, so nothing is lost when you close the program.

What it does:

- While you type, GpgFrontend keeps a copy of every unsaved editor tab. This
  includes tabs that hold plain text, such as a message you just decrypted.
- The copy is kept in the program's own saved data, which is locked with the
  program's key. See [Application Data Storage](/advanced/app-data-storage/).
- When you quit, the program does not ask you to save your tabs. It just
  closes.
- The next time you start GpgFrontend, your tabs come back.

The trade-off is simple. With the cache on, you never lose a draft. But your
unsaved text, plain text included, stays on the disk in locked form until you
close those tabs or turn the cache off.

If you would rather nothing is kept:

1. Open **Settings** and go to **General**.
2. Under **Operation**, untick **Cache text editor contents.**
3. Click **OK**. On macOS, close the window instead.

With the cache off, quitting asks whether to save your unsaved tabs, and
any cached tabs are cleared the next time the program starts.

When you quit and the program is sure it will close, it also wipes the text
out of every open tab. This happens after the cache is saved and after any
question about saving has been answered.

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
malware is running under your account, or someone is sitting at your unlocked
computer, no memory setting can save you.
