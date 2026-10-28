---
title: "Finding Your Settings"
description: "A map of the GpgFrontend settings window: the search box, the four groups in the sidebar, what lives on each page, and which changes need a restart."
sidebar:
  label: Settings
  order: 19
---

The settings window has a search box at the top and a list of pages down the
left side.

To open it, click **Edit** > **Settings**. On macOS the window is called
**Preferences**, and you find it under the GpgFrontend menu.

:::note[Changed in v2.2.3]

On macOS the window is now called **Preferences**, as macOS apps usually do.

:::

## Just Search

The fastest way to find anything is the search box at the top. It looks at
page names and at the things on each page, so you do not have to guess which
page a setting is on.

Type `pin` and it takes you to the page with the PIN setting. Type `proxy`,
`theme`, or `update` and the same thing happens.

## The Four Groups

If you would rather browse, the pages are sorted into four groups:

- **Application**: how the program looks and behaves.
- **Keys & Engines**: where your keys live and which engine handles them.
- **Features**: extras that come from modules.
- **System**: the technical settings, plus logging.

## What Is on Each Page

| Page                  | Group          | What you change there                                                                  |
| --------------------- | -------------- | -------------------------------------------------------------------------------------- |
| **General**           | Application    | Language, how operations behave, where the File Panel opens, which modules to look for |
| **Appearance**        | Application    | Theme, icon size, which actions appear on the toolbar and what a click runs, fonts    |
| **Network**           | Application    | Proxy settings                                                                         |
| **Updates**           | Application    | Whether GpgFrontend checks for a new version when it starts                            |
| **Key Databases**     | Keys & Engines | Your key databases, which one is the default, and the built-in database's engine       |
| **Key Generation**    | Keys & Engines | The default key type, the made-up identity for Quick Generate, and your key profiles   |
| **GnuPG**             | Keys & Engines | Point at your own GnuPG, and fix GnuPG when it stops responding                        |
| **rPGP**              | Keys & Engines | How long the rPGP engine remembers a passphrase, and passphrase encryption strength    |
| **Key Servers**       | Keys & Engines | The list of key servers, and which one is the default                                  |
| **Instant Messaging** | Features       | Your phrase for [instant messaging](/guides/instant-messaging/)                        |
| **Mail Accounts**     | Features       | Your email accounts for [sending and reading email](/email/accounts-sending/)          |
| **Advanced**          | System         | How the program protects its own key, and how much it writes to the log                |

Some pages only show up when they apply to you:

- **GnuPG** and **rPGP** appear only if your copy has that engine.
- **Network** does not appear in sandboxed builds, such as Flatpak or the Mac
  App Store edition.
- **Updates** is not in the Flatpak or Mac App Store builds, which get their
  updates from Flathub or the App Store.
- **Updates**, **Key Servers**, **Instant Messaging** and **Mail Accounts**
  come from built-in modules. Each one appears only while its module is
  switched on. You can check that in
  [Module Controller](/advanced/module-controller/).

:::note[New in v2.2.3]

The **Updates** and **Mail Accounts** pages are new. The **Network** page now
holds only the proxy settings.

:::

## The General Page

The **General** page has these parts.

### Base

**Module Discovery:** decides which modules GpgFrontend looks for when it
starts. The choices are **Only Integrated Modules**, **Also Look For Modules
I've Added** and **Disable**. Looking for a module never runs it. See
[Module Controller](/advanced/module-controller/) for the rest. A change here
takes effect the next time you start GpgFrontend.

Sandboxed builds hide the whole **Base** box.

### Operation

- **Default Workspace As:** choose whether GpgFrontend starts with the
  **File Panel** or the **Text Editor**. The default is **File Panel**.
- **File Panel Opens At:** the folder the File Panel shows first. Sandboxed
  builds hide this and **Default Workspace As:**. They always start with the
  **Text Editor**, and ask for a folder each time you open a File Panel.
- **Cache text editor contents.** keeps your open text tabs, including ones you
  have not saved, so they come back the next time you start GpgFrontend. They
  are stored encrypted. This is **on** by default.
- **Allow only one checked key in the key list.** When you check a key, the
  others are unchecked. This stops a key from an earlier message from being
  added to the next one by mistake.
- **Ask before encrypting to more than one recipient.** GpgFrontend shows you
  the list of recipients and asks you to confirm.
- **Allow undoing encrypt, decrypt and other operations in the text editor.**
  This is **off** by default. When it is on, the old text stays in memory so
  you can undo. After you encrypt, that old text is your plaintext.

For more about these choices, see
[Encrypting Safely](/guides/encryption-safety/).

The same box also has options to import dropped files without asking, to
remember checked keys, to use binary mode for files, and to warn about keys
that expire soon.

:::note[Changed in v2.2.3]

Undo after an operation is now off by default. **Module Discovery** replaces the
old module loading setting. The default engine moved from this page to the **Key
Databases** page.

:::

### Language

Pick the language GpgFrontend uses. **System Default** follows your operating
system. Changing it reloads the window.

### Data

- **Reveal in File Explorer**: open the folder where GpgFrontend keeps its
  data, in your system's file manager.
- **Clear All Data Objects (Total Size: ...)**: delete the data GpgFrontend has
  saved for you, such as window positions, states and your key server list.
  GpgFrontend asks first. See [App Data Storage](/advanced/app-data-storage/).

Sandboxed builds hide the **Data** box.

## The Key Databases Page

A key database is a folder where your keys are kept.

The **Key Databases** page lists your key databases and lets you add, edit and
remove them. You can also pick which one is the default with **Use as
Default**.

The **Built-in Key Database** box has a **Key engine:** choice. It applies only
to the built-in database. Other databases always open with their own engine.

This page is still changing. For the details, see
[Key Database](/advanced/key-database/).

## The Key Generation Page

This page decides what [making a new key](/guides/generate-key/) starts with.
It has two tabs.

:::note[New in v2.2.4]

This page is new.

:::

### The Quick Generate Tab

- **Default key profile**: the key type that is picked first in the
  **Generate Key** window, and that **Quick Generate** uses. A **profile** is
  a saved set of key choices. The default is **Ed25519 / X25519 (Modern &
  Fast)**.
- **Quick Generate identity**: how the made-up name, email and comment look.
  **Quick Generate** and the **Fill In Anonymously** button use these. Change
  them in **Name pattern:**, **Email pattern:** and **Comment pattern:**.
  **Preview:** shows an example. Click the refresh button next to it for
  another one.

A pattern is normal text with placeholders in curly braces. For example, the
default name pattern `anon-{token}` gives `anon-` followed by 8 random letters
and digits.
Click **Placeholders** to see them all. Some useful ones:

- `{token}`: 8 random letters and digits, the same in every field.
- `{domain}` and `{tld}`: a made-up domain. `{tld}` gives `test`, `example` or
  `invalid`, so no mail can ever reach the address.
- `{date}`: today's date.

**Restore Default Patterns** puts the three patterns back as they were.

### The Profiles Tab

The list shows every profile and its **Status**: **Default**, **Hidden**,
**Unavailable** (your engine cannot make it) or **Offered**. Click a profile to
see what it makes and where it appears in the **Generate Key** window.

- **New…** makes a profile. Choose its **Name**, the **Primary key**, and
  whether to add a **Subkey**.
- **Edit…** changes the selected profile.
- **More** has **Duplicate**, **Set as Default**, **Hide** and **Delete**.
- Drag a profile, or use the arrow buttons, to change the order.

You cannot delete or hide the default profile. Choose another default first.
Deleting a profile never changes keys you already made with it.

**Restore Built-in Profiles…** adds back the profiles GpgFrontend comes with,
if you deleted any. Your own profiles and your changes are kept.

## The rPGP Page

The **rPGP** page sets how long the rPGP engine remembers a passphrase and how
long its passphrase prompt waits.

Under **Passphrase Encryption** there is **Argon2 Parameters:**. It decides how
much memory it takes to turn a passphrase into a key when you encrypt with a
passphrase only:

- **High memory, 2 GiB**: the default. It makes a stolen message much harder
  to crack.
- **Low memory, 64 MiB**: choose this if your computer, or the computer of the
  person who opens the message, cannot spare 2 GiB.

The choice applies only to messages you encrypt from now on. See
[Symmetric Encryption](/guides/symmetric-encrypt-decrypt/).

## The Updates Page

The **Updates** page has one checkbox: **Checking for version updates when the
application starts.**

When it is on, GpgFrontend checks quietly in the background, at most once a
day. It never opens a window for this. If a newer version exists, a badge
appears on **Help** > **Check for Updates**.

GpgFrontend only checks after the first-run setup has asked you whether you
want this.

To check yourself, click **Help** > **Check for Updates**. If you have not
turned the check on, the window does not check by itself. Click **Check now**
to check once. The window then tells you one of these things:

- **You're up to date**.
- A new version is available. The window names it, offers a button to
  download it, and has **Release notes** you can open.
- **This version isn't listed on GitHub Releases**. This can happen with a
  pre-release or a withdrawn version.
- **This build isn't from the official repository**. This is expected if you
  built GpgFrontend yourself.
- **Couldn't check for updates**, with **Try again**.

The check only asks GitHub Releases.

:::note[New in v2.2.3]

The **Updates** page and the background check are new, and the **Check for
Updates** window was redesigned.

:::

## The Advanced Page

The **Advanced** page has two parts:

- **Security**: **Secure Level:** and **Application Key Protection:**. See
  [App Secure Key](/advanced/app-secure-key/).
- **Diagnostics**: **Log Level:** and **Log Ring Buffer:**.

**Log Level:** decides how much GpgFrontend writes to its log. The choices are
**Trace**, **Debug**, **Info**, **Warning**, **Error** and **Fatal**. **Trace**
writes the most. It adds detail from modules that **Debug** leaves out.

You can also set the level for one run when you start GpgFrontend from a
terminal:

```bash
gpgfrontend --log-level trace
```

The short form is `-l`. The values are `trace`, `debug`, `info`, `warn` and
`error`.

:::caution[Trace logs can hold private details]

Logs at **Trace** or **Debug** level can contain details about your keys,
files and messages. Read a log before you share it, and switch back to a lower
level when you are done.

:::

:::note[Changed in v2.2.3]

**Trace** is a new log level.

:::

## When a Restart Is Needed

Most settings take effect the moment you click OK. That now includes all
changes on the **Key Databases** page, the built-in database's engine, and
**Forbid all GnuPG network connection.** on the **GnuPG** page. GpgFrontend
opens your key databases again, without a restart.

On macOS there are no OK and Cancel buttons. Your changes are saved when you
close the window.

A few settings still need a restart. If you changed one of them, GpgFrontend
shows a **Restart Required** message when you click OK. It names the pages
with these changes. Click **Save and Restart** or **Save and Reload** to apply
them, or **Cancel** to throw away every change you made in the window.

These changes reload the window:

- the language, on the **General** page;
- the theme, on the **Appearance** page.

These changes restart the program:

- **Use Custom GnuPG**, the GnuPG path, and **Enable GpgME Debug Log**, on the
  **GnuPG** page;
- anything on the **Advanced** page.

A module's settings page may also ask for a restart.

:::note[Changed in v2.2.3]

Key database changes and the engine choice no longer need a restart.

:::

:::caution[Cancel throws away everything]

Cancel does not just undo the page you are looking at. It undoes every change
you made anywhere in the settings window during that visit.

On macOS, choosing **Cancel** in the **Restart Required** message also throws
away every change you made, and the window closes.

:::

One exception: the buttons in the **Maintenance** part of the GnuPG page act
straight away. Cancel does not undo those.

## If GnuPG Stops Responding

The **GnuPG** page has a **Maintenance** section with three buttons. They are
the first thing to try when GnuPG hangs, forgets your passphrase at the wrong
moment, or stops seeing your smart card. Sandboxed builds, such as Flatpak,
hide this section and the **Clear password cache on exit** option.

- **Clear Password Cache**: make GnuPG forget every passphrase it is holding.
- **Reload Components**: have GnuPG re-read its settings.
- **Restart Components**: stop and restart GnuPG's background programs.

These act the moment you click them, and are not undone by Cancel. Restarting
interrupts anything GnuPG is in the middle of, so do not use it during a large
file operation.

## Checking What Is Actually in Use

When something looks wrong, it helps to see what GpgFrontend thinks it is
running. Click **Help** > **About**, then open the **Status** tab.

The tab shows:

1. **Needs Attention**: only appears when something is not as it should be,
   for example when the system credential store cannot be used.
2. **At a Glance**: your profile, how the application key is protected, and
   the secure level.
3. **More details**: click it to open the **Details** card. It has rows for
   **Application**, **Profile**, **Folders** and **OpenPGP Engines**.

Hold the mouse over a row to read more about it, or to see a long value in
full.

To share this with someone who helps you, click **Copy Status Information**.
It copies every row, including the hidden ones.

Your key databases are not listed here. Look on the **Key Databases** settings
page instead.

The other tabs of the About window are also useful:

- **About** has a **Resources** card with links to the website, the
  documentation, the source code and the release notes.
- **Build Information** lists the versions GpgFrontend was built with. Click
  **Copy Build Information** to copy them.

:::note[Changed in v2.2.3]

The **Status** tab was rebuilt, and the **About** and **Build Information**
tabs were redesigned.

:::
