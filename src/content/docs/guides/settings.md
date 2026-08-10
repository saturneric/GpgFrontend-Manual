---
title: "Finding Your Settings"
description: "A map of the GpgFrontend settings window: the search box, the four groups in the sidebar, and what lives on each page."
sidebar:
  label: Settings
  order: 19
---

The settings window changed shape in v2.2.2. The row of tabs along the top is
gone. In its place there is a search box and a list of pages down the left
side.

Open it with **Settings** in the menu bar. On macOS it is called
**Preference**, under the GpgFrontend menu.

## Just Search

The fastest way to find anything is the search box at the top. It looks at
page names and at the things on each page, so you do not have to guess which
page a setting is on.

Type `pin` and it takes you to the page with the PIN setting. Type `proxy`,
`theme`, or `keyserver` and the same thing happens.

## The Four Groups

If you would rather browse, the pages are sorted into four groups:

- **Application**: how the program looks and behaves.
- **Keys & Engines**: where your keys live and which engine handles them.
- **Features**: extras you can turn on.
- **System**: the technical settings, plus logging.

## What Is on Each Page

| Page                  | Group          | What you change there                                                     |
| --------------------- | -------------- | ------------------------------------------------------------------------- |
| **General**           | Application    | Language, which engine to use, what the file panel opens at, expiry warnings |
| **Appearance**        | Application    | Theme, icon size, which buttons appear on the toolbar, fonts               |
| **Network**           | Application    | Proxy settings                                                            |
| **Key Databases**     | Keys & Engines | Add, edit and remove key databases                                        |
| **GnuPG**             | Keys & Engines | Point at your own GnuPG, clear the password cache, restart GnuPG          |
| **rPGP**              | Keys & Engines | How long the rPGP engine remembers a passphrase                           |
| **Key Servers**       | Keys & Engines | The list of key servers, and which one is the default                     |
| **Instant Messaging** | Features       | Your shared secret phrase for [instant messaging](/guides/instant-messaging/) |
| **Advanced**          | System         | How the program protects its own key, and how much it writes to the log   |

Some pages only show up when they apply to you. **GnuPG** and **rPGP** appear
only if your copy has that engine. **Key Servers** comes from a module, so it
appears only while the key server module is switched on. You can check that in
[Module Controller](/advanced/module-controller/).

## When a Restart Is Needed

Most settings take effect the moment you click OK. A few cannot.

If you changed one of those, GpgFrontend shows a **Restart Required** message
when you click OK. It tells you which page the change was on and offers to do
the restart for you. That is usually the easiest choice.

The changes that need one are:

- Changing the language or the theme. These only reload the window.
- Changing the default engine, editing key databases, or anything on the
  **Advanced** page. These restart the program.

:::caution[Cancel throws away everything]

Cancel does not just undo the page you are looking at. It undoes every change
you made anywhere in the settings window during that visit.

:::

One exception: the buttons in the **Maintenance** part of the GnuPG page act
straight away. Cancel does not undo those.

## If GnuPG Stops Responding

The **GnuPG** page has a **Maintenance** section with three buttons. They are
the first thing to try when GnuPG hangs, forgets your passphrase at the wrong
moment, or stops seeing your smart card:

- **Clear Password Cache**: make GnuPG forget every passphrase it is holding.
- **Reload Components**: have GnuPG re-read its settings.
- **Restart Components**: stop and restart GnuPG's background programs.

These act the moment you click them, and are not undone by Cancel. Restarting
interrupts anything GnuPG is in the middle of, so do not use it during a large
file operation.

## Checking What Is Actually in Use

When something looks wrong, it helps to see what GpgFrontend thinks it is
running. Open **Help**, then **About**, then the **Status** tab.

It shows which profile you are in, which engine and version, whether this is a
portable copy, and how the application key is protected.
