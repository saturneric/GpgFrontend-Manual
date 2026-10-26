---
title: "Module Controller"
description: "See which GpgFrontend modules you have, turn them on or off, and add a module from someone you trust."
sidebar:
  label: Module Controller
  order: 11
---

A **module** is an optional part of GpgFrontend that adds a feature. Several
come with the program, such as the one for key servers and the one for email.
You can also add a module that someone else made.

The **Module Controller** is the window where you see your modules and turn them
on or off.

Most people never need this page. The modules that come with GpgFrontend are
already on.

## Open the Module Controller

Click **Advanced** in the menu bar, then **Open Module Controller**.

:::note[Flatpak and Mac App Store Lite]

These versions run in a sandbox (a closed-off space the system gives the app).
The Module Controller is not available there, and the **Module Discovery**
setting is hidden.

The Flatpak version shows the **Advanced** menu, with the items that modules
add to it, but without **Open Module Controller**. The Mac App Store Lite
version hides the whole menu.

:::

## Modules That Come With GpgFrontend

Each module adds menu items, buttons or settings pages. Here is the name you see
in the module list, what the module does, and where its features appear.

- **InstantMessaging**: short encrypted messages for chat apps. Adds **IM
  Encrypt** and **IM Encrypt & Sign** to the **Operations** menu, and the
  **Instant Messaging** settings page under **Features**. See
  [Instant Messaging](/guides/instant-messaging/).
- **PGPInspect**: a window that shows what is inside OpenPGP data. Adds **Open
  OpenPGP Structure Inspector** to the **Advanced** menu and to the editor's
  right-click menu. See [OpenPGP Structure Inspector](/advanced/pgp-inspector/).
- **KeyServerSync**: finds, publishes and refreshes keys on key servers. Adds
  **Key Server** to **Keys**, **Import Key**, the **Key Server Operations**
  button in key details, and the **Key Servers** settings page under **Keys &
  Engines**. See [Key Server Operations](/guides/key-server-operations/).
- **VersionChecking**: checks for a newer GpgFrontend. Adds **Check for
  Updates** to the **Help** menu, and the **Updates** settings page under
  **Application**.
- **GatherGnupgInfo**: shows details about your GnuPG installation. Adds
  **GnuPG** to the **Help** menu.
- **Email**: writes, reads and protects email. Adds **Mail Editor** to **File**,
  **Workspace**, adds **Open IMAP Controller** to the **Advanced** menu, and
  adds the **Mail Accounts** settings page under **Features**.

Some versions leave modules out:

- The Mac App Store Lite version does not include **VersionChecking** or
  **GatherGnupgInfo**.
- The Flatpak version does not include **VersionChecking**, because Flathub
  delivers its updates.

:::caution[Features leave with their module]

When you turn a module off, its menu items, buttons and settings pages
disappear. For example, turn off **KeyServerSync** and the **Key Servers**
settings page is gone, along with key server search and publishing.

:::

## The Module List

The first tab, **Registered Modules**, lists your modules. Above the list, a
line counts them, for example "6 module(s) · 6 active".

Each module has small labels under its name:

- **Integrated**: comes with GpgFrontend.
- **External**: a module you added.
- **Signed**: an external module whose package signature was checked.
- **Unsigned**: an external module with no checked signature.
- **Auto**: starts by itself when GpgFrontend opens.
- **Needs Approval**: an external module that waits for you to allow it.
- **Refused**: GpgFrontend would not load this module.

To find a module, type in the search box (**Search modules...**). To show only
some modules, use the drop-down beside it: **All**, **Active**, **Inactive**,
**Integrated**, **External** or **Not Loaded**. **Not Loaded** shows the modules
that wait for you or were refused.

### Module Details

Click a module to see its details on the right. They come in two parts:

- **Verified by GpgFrontend**: facts the program checked itself, such as the
  **Identifier**, **Version** and **Origin**. For a module that comes with the
  program, **Origin** says **Built into this application**.
- **Described by its package** or **Claimed by the module**: the name, author
  and description. **Claimed by the module** means nobody checked these words,
  so treat them with care.

## Turn a Module On or Off

1. Click the module in the list.
2. Click **Activate** or **Deactivate**. This works straight away.
3. To choose what happens the next time GpgFrontend starts, tick or untick
   **Activate on Start**.

## Choose Which Modules GpgFrontend Looks For

The **Module Discovery** setting decides where GpgFrontend looks for modules.
Open **Settings** (on macOS, **Preferences**), go to **General**, and find
**Module Discovery:**. It has three choices:

- **Only Integrated Modules**: only the modules that come with GpgFrontend. This
  is the normal choice.
- **Also Look For Modules I've Added**: also look in your modules folder for
  modules you added.
- **Disable**: no modules at all. The **Registered Modules** tab is then greyed
  out.

A change takes effect after GpgFrontend restarts.

Finding a module never runs it. A module you added only runs after you allow it,
as the next section shows.

:::note[Changed in v2.2.3]

This setting used to be called **Module Loading Policy**. Its new name is
**Module Discovery**. The old **All Modules** choice is now
**Also Look For Modules I've Added**, and it only looks. It does not run
anything by itself.

:::

## Add a Module From Someone Else

Only add a module from a person or project you trust. A module runs inside
GpgFrontend and can do anything GpgFrontend can do.

The module's author gives you a folder. It holds a file named `module.gfmodule`
and a folder named `native`. The author should also tell you the **publisher key
fingerprint**: a long code that identifies them. Get it from a place you trust,
such as their website.

1. In **Settings**, **General**, set **Module Discovery:** to **Also Look For
   Modules I've Added**. You do not need to restart yet.
2. Open the Module Controller and click **Show Modules Folder**. Your modules
   folder opens.
3. Copy the author's folder into it, as it is. Do not change or rename anything
   inside.
4. Restart GpgFrontend and open the Module Controller again. The new module
   shows the label **Needs Approval**.
5. Click the module. Compare the **Publisher key** shown in its details with the
   fingerprint the author gave you. They must match exactly.
6. Click **Trust This Publisher Key...**. Read the message, then click **Yes**.
   The button changes to **Publisher Key Trusted**.
7. Click **Enable This Module**. A message says "This module will be loaded the
   next time GpgFrontend starts."
8. Restart GpgFrontend. The module now loads.

Trusting a publisher key does not turn anything on by itself. It only lets you
enable modules signed with that key, one at a time. A module signed with a
different key asks you again.

:::note[New in v2.2.3]

Modules you add are now signed packages. You must trust the publisher key and
enable each module before it runs.

:::

### Why a Module Is Not Loaded

When a module does not load, its details show **Status** and a reason. These are
the reasons you are most likely to see:

- "Waiting for you to trust the publisher key that signed it." Do step 6 above.
- "Waiting for you to enable it." Do step 7 above, then restart.
- "External modules are not supported on macOS: the system only loads code
  signed with this application's own Team ID." See below.
- "The module claims the ID ..., which belongs to a module that comes with
  GpgFrontend." The module pretends to be a built-in one. Do not use it.
- "The module declares the ID ... but is in a directory named ... instead of
  ...". The folder was renamed. Copy the author's folder again without changing
  its name.

Other reasons usually mean the package is damaged or was changed. Ask the
module's author for a new copy.

### macOS Cannot Load Added Modules

On macOS, GpgFrontend always refuses modules you added. macOS only lets the app
load code signed by the app's own maker. The modules that come with GpgFrontend
still work.

### Old Modules From v2.2.2

Modules made for v2.2.2 were single files ending in `.so`, `.dll` or `.dylib`.
GpgFrontend v2.2.3 no longer loads them, and they do not appear in the list. Ask
the module's author for a new, signed version.

## Tabs for Developers

You can ignore these tabs unless you build modules.

- **Global Register Table**: values that modules and the program share, such as
  the GnuPG paths found on your computer. Use the search box, **Expand All** and
  **Collapse All** to look around. This tab is in every version.
- **Events**, **Module Status** and **Commands**: tools for testing modules.
  They only appear in nightly and debug builds, not in normal releases.

To get a report about your modules without opening the window, start GpgFrontend
from a terminal with `--module-status FILE`. It loads the modules, writes a JSON
report to `FILE` and exits. The exit code is not zero when a module was refused
or no module loaded.

To make your own module, see [Write Your Own Module](/advanced/write-modules/).
