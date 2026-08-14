---
title: "Module Controller"
description: "See which GpgFrontend modules you have, switch them on or off, and add your own."
sidebar:
  label: Module Controller
  order: 11
---

A **module** is an optional piece of GpgFrontend that adds a feature. Some come
with the program, such as the one that handles email and the one that talks to
key servers. You can also add your own.

The **Module Controller** is where you see what you have and switch things on
or off. Open it with **Advanced**, then **Open Module Controller**.

Most people never need this page. Modules that come with GpgFrontend are on
already.

## The Module List

The first tab, **Registered Modules**, lists everything you have. Click a
module to see its details on the right.

Each module is labelled:

- **Integrated**: comes with GpgFrontend.
- **External**: something you added yourself.
- **Auto**: starts on its own when GpgFrontend opens.

If the list is long, use the search box at the top, or the drop-down beside it
to show only the active, inactive, integrated, or external ones.

## Switch a Module On or Off

Select the module and click **Activate** or **Deactivate**. That takes effect
straight away.

To decide whether it comes back next time, tick or untick **Activate on
Start**.

:::caution[Some features disappear with their module]

Turning off a module removes the features it provides. Switch off the key
server module,
for example, and the **Key Servers** page vanishes from Settings, along with
key server search and publishing.

:::

### If nothing can be switched on

GpgFrontend can be told to load fewer modules, or none at all. If that is the
case, the Module Controller says so and points you at the setting.

You can change it in **Settings**, **General**, under **Module Loading
Policy**:

- **All Modules**: everything, including ones you added.
- **Only Integrated Modules**: just the ones that came with the program.
- **Disable**: none at all.

## Modules Can Add Settings Pages

Since v2.2.2, a module can add its own page to the settings window.

The one you already have is **Key Servers**, under **Keys & Engines**. It only
appears while the key server module is active, which is why it is not always
there. See [Finding Your Settings](/guides/settings/).

## Adding Your Own Module

Click **Show Mods Directory**. That opens the folder GpgFrontend reads
external modules from. Put the module file there and click **Refresh**.

Module files end in `.dll` on Windows, `.dylib` on macOS, and `.so` on Linux.

:::tip[Back up the folder first]

Make a copy of the modules folder before you change anything in it. It is much
quicker than working out afterwards what you removed.

:::

To remove a module that came with GpgFrontend, delete its file from the
`modules` folder. On Linux this may not be possible with AppImage or Flatpak
packages, because their contents are read-only.

## For Developers

The last two tabs are for development work. You can ignore them unless you
are building a module.

**Global Register Table** shows the values modules and the core share with each
other, such as detected GnuPG paths and version check results. Use the search
box, or **Expand All**, to look around.

**Debugger** lets you fire an event or set a value by hand, to see how a module
reacts.

Modules are plain shared libraries with a C interface, linked against
`libgpgfrontend_sdk`. The SDK is still growing, so if something you need is
missing, please get in touch.

For the source and examples, see the
[GpgFrontend Modules repository][modules-readme].

[modules-readme]: https://github.com/saturneric/GpgFrontend-Modules/blob/main/README.md
