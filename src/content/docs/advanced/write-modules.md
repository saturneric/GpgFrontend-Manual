---
title: "Write Your Own Module"
description: "For module authors: how a GpgFrontend module is described, signed, published and loaded, and what its Lua UI script can do."
sidebar:
  label: Write Your Own Module
  order: 12
---

This page is for people who want to build a module for GpgFrontend. It gives an
overview of the parts and the rules. The full reference lives in two files in
the source code:

- the [modules README][modules-readme]: how to write, build, sign and publish a
  module;
- the [SDK README][sdk-readme]: the API a module calls, including the Lua UI
  API, the anchor catalog and the widget types.

If you only want to use a module someone else made, see
[Module Controller](/advanced/module-controller/).

:::note[New in v2.2.3]

Modules are now signed `.gfmodule` packages with a `module.json` identity, a
capability list and a Lua UI script. Loose `.so`, `.dll` or `.dylib` modules
built for v2.2.2 no longer load.

:::

## How a Module Is Built

A module is built inside the GpgFrontend source tree, in its own folder under
`modules/src/`. It cannot be built on its own: the toolchain, the SDK headers
and Qt all come from the main project's CMake build. Modules are built when
`GPGFRONTEND_BUILD_MODULES` is `ON` (the default).

Each module folder holds:

- `module.json`: the module's identity (see below);
- `CMakeLists.txt`: one call to `gf_add_module()`;
- the C++ sources;
- `ui/main.lua`: the UI script, if the module has a user interface;
- `ts/`: translation files.

A small `CMakeLists.txt` looks like this:

```cmake
gf_add_module(
  NAME   my_module
  QT     Core Widgets
  LUA_SCRIPTS ui/main.lua
)
```

`gf_add_module()` reads `module.json`, builds the library, generates the
identity header, wires up translations, and builds and signs the `.gfmodule`
package. `LUA_SCRIPTS` needs the `ui` capability. The script is embedded in the
module and covered by its signature.

The module must match the Qt major version of the GpgFrontend build it runs in,
and needs Qt 6.5 or later.

## `module.json`

This file is the one source of truth for the module's identity. The signed
package manifest is made from it.

```json
{
  "schema_version": 1,
  "id": "com.example.my_module",
  "version": "1.0.0",
  "name": "MyModule",
  "description": "What this module does.",
  "author": "Your Name",
  "capabilities": ["ui"],
  "events": ["APPLICATION_LOADED"],
  "commands": ["com.example.my_module.show_about"],
  "translation_context": "ModuleMyModule"
}
```

| Field                 | Meaning                                                                                                                                                                   |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `schema_version`      | Must be `1`.                                                                                                                                                              |
| `id`                  | The module's unique ID. The modules folder name is derived from it.                                                                                                       |
| `version`             | The module's version.                                                                                                                                                     |
| `name`                | The name shown in the Module Controller.                                                                                                                                  |
| `description`         | One line about what the module does.                                                                                                                                      |
| `author`              | Who made it.                                                                                                                                                              |
| `capabilities`        | What the module may use. See below.                                                                                                                                       |
| `events`              | Every event the module handles. Required. The list must match the module's handler table exactly, or the module will not activate.                                        |
| `commands`            | Optional. Every command the module provides. Each ID starts with the module `id` and a dot, is lower case, and appears once. It must match the commands the module binds. |
| `translation_context` | The context for the module's translated strings.                                                                                                                          |
| `min_host_version`    | Optional. The oldest GpgFrontend version the module needs. Defaults to the version it was built against.                                                                  |

The build checks these fields when CMake configures the project. A typo in a
capability name fails the build with a list of the valid names.

## Capabilities

`capabilities` decides what the module can reach. The names below are the full
list in v2.2.3.

**Granted and enforced.** When the module activates, GpgFrontend gives it only
the API groups it declared. A call into a group it did not declare does nothing,
returns its failure value and logs one line that names the missing capability.

| Name        | Gives access to                                                                 |
| ----------- | ------------------------------------------------------------------------------- |
| `gpg`       | Signing, encryption, decryption, verification, keys, key lists, result analysis |
| `pgp`       | OpenPGP packet structure inspection, with no keyring or engine                  |
| `ui`        | A Lua UI script, commands, theme colours by role                                |
| `ui.custom` | The module's own native widgets, mounted by the script. Requires `ui`           |
| `editor`    | Reading the document the user has open                                          |
| `storage`   | Settings, caches, the shared runtime register table                             |
| `process`   | Running an external program                                                     |

**Recorded only.** `network` is signed and shown to the user, but GpgFrontend
cannot enforce it. A module reaches the network through Qt directly. Declare it
honestly when your module goes online.

Buffers, memory, logging, event subscription and translations are always
available and are not declared. Do not declare capabilities you do not use:
users see the list before they decide to trust a module.

## Signed Packages

Every module ships as a signed `.gfmodule` package: a manifest and its Ed25519
signature. An external module's package also carries the publisher public key
that made the signature. Next to the package sits the native library it names:

```text
<key>/module.gfmodule
<key>/native/<library>
```

`<key>` is a folder name derived from the module `id`. GpgFrontend derives it
again from the signed manifest and refuses a package in the wrong folder.

GpgFrontend checks the package before any module code runs. An integrated module
is checked against a key built into that copy of GpgFrontend. An external module
is checked against the key it carries, and loads only after the user trusts that
key and enables the module.

## Publish an External Module

External modules are made from integrated ones, never built directly. You build
your module as part of a GpgFrontend build, then turn its package into one
signed with your own publisher key. The tool for this is
`gf_module_externalize`, built with GpgFrontend.

1. **Create a publisher key, once.** It is your lasting identity. Keep the
   secret file safe. Publish the `.pub` file, or its fingerprint, where your
   users can trust it.

   ```bash
   gf_module_externalize new-key --out publisher.key
   gf_module_externalize fingerprint --key publisher.key.pub
   ```

   `new-key` writes `publisher.key` (secret) and `publisher.key.pub` (public),
   and prints the fingerprint. `fingerprint` prints the fingerprint of either
   file.

2. **Build with native binding required**, so the package binds the exact bytes
   of the native library. Finish every step that rewrites the library (strip,
   `patchelf`, deploy tools) before you externalize.

   ```bash
   cmake -B build -DGPGFRONTEND_INTEGRATED_MODULE_NATIVE_BINDING=REQUIRED
   ```

3. **Externalize the module's folder.**

   ```bash
   gf_module_externalize \
     --input build/artifacts/modules/<key> \
     --publisher-key publisher.key \
     --output-root dist \
     [--publisher-name "Example"] [--publisher-url https://example.com]
   ```

   The input must be an integrated module that this build verifies, with its
   native library bound. The output is `dist/<key>/module.gfmodule` and
   `dist/<key>/native/<library>`. The tool never overwrites an existing output.

4. **Do not change the output.** The package binds the library's bytes, and
   there is no way to reseal it without your secret key. The one exception is
   Authenticode signing of a Windows library, which the binding ignores by
   design.

The publisher name and URL are only claims. GpgFrontend shows them as such. What
users trust is the publisher key.

### How Users Load Your Module

Tell your users to:

1. set **Settings**, **General**, **Module Discovery:** to **Also Look For
   Modules I've Added**;
2. copy your `<key>` folder into the folder that **Show Modules Folder** opens
   in the Module Controller, then restart GpgFrontend;
3. select your module, check the **Publisher key** fingerprint against the one
   you published, and click **Trust This Publisher Key...**;
4. click **Enable This Module**, then restart GpgFrontend.

Trusting your key does not enable anything by itself. Each module signed with it
must be enabled on its own. External modules are always refused on macOS,
because macOS only loads code signed with GpgFrontend's own Team ID.

## The Lua UI Script

A module's user interface has two parts:

- **Commands**, written in C++. They do the work and carry every word the user
  sees: title, description and category.
- **A Lua UI script** (`ui/main.lua`). It says where the commands are offered
  and when they are enabled. It contains no user-visible text.

Here is the script of the bundled OpenPGP Structure Inspector:

```lua
local open = commands.get("com.bktus.gpgfrontend.module.pgp_inspect.open_inspector")

ui.mount {
  id = "inspector",
  anchor = ui.anchor.dialog {},
  widget = native.widget("inspector"),
}

ui.action { id = "menu", anchor = ui.anchor("main.menu.advanced"), command = open }
ui.action { id = "context", anchor = ui.anchor("editor.context"), command = open }
```

### Lua UI API v1

| Function                                      | What it does                                                                                                     |
| --------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `commands.get(id)`                            | Get a command. It must exist, and its capabilities are checked.                                                  |
| `commands.state(cmd)`                         | Read `enabled`, `visible` and `checked`.                                                                         |
| `commands.invoke(cmd, args[, fn])`            | Run a command. Only inside handlers and continuations.                                                           |
| `ui.action{...}`                              | Place a command on an anchor, with `id`, `anchor`, `command` and optional `order`, `icon`, `shortcut`, `update`. |
| `ui.mount{...}`                               | Mount a native widget on a settings, editor or dialog anchor. Needs `ui.custom`.                                 |
| `ui.subscribe{...}`                           | React to a UI event.                                                                                             |
| `native.widget(name)`, `native.factory(name)` | Refer to a native widget the module registered. Needs `ui.custom`.                                               |
| `state.get`, `state.set`                      | Read and write the module's own settings group. Needs `storage`.                                                 |
| `state.host(key)`                             | Read a few shared host keys on an allow list. Needs `storage`.                                                   |
| `theme.color(role)`                           | A theme colour as `0xAARRGGBB`.                                                                                  |

`ui.action`, `ui.mount` and `ui.subscribe` only work while the script loads. The
UI events are `document.activated`, `document.state_changed`, `document.saved`,
`key_database.refreshed` and `app.ui_ready`.

An action's `update(ctx)` function must be pure. It reads the context and
returns `visible`, `enabled`, `checked` and `args`. GpgFrontend runs it again
when the user clicks, so a command never gets stale arguments.

### Anchors

An anchor is a fixed place, owned by GpgFrontend, where a script can add
something.

| Anchor                        | Place                                                          |
| ----------------------------- | -------------------------------------------------------------- |
| `main.menu.file.workspace`    | **File**, **Workspace** menu                                   |
| `main.menu.advanced`          | **Advanced** menu                                              |
| `main.menu.help`              | **Help** menu                                                  |
| `main.menu.import_key`        | **Import Key** menu                                            |
| `main.menu.operations`        | **Operations** menu                                            |
| `editor.context`              | The text editor's right-click menu                             |
| `key.details.actions`         | Buttons in the key details dialog, grouped by command category |
| `key.list.context`            | The key lists' right-click menus                               |
| `key.manager.menu.operations` | The key management window's **Operations** menu                |
| `settings`                    | A settings page                                                |
| `editor`                      | The view of a document type, and the files it opens            |
| `dialog`                      | A dialog                                                       |

Settings pages go in one of four sections: `application`, `keys_engines`,
`features` or `system`. Use them as
`ui.anchor.settings { section = "features" }`.

For `key.list.context` and `key.manager.menu.operations`, `ctx.keys` holds the
checked keys when any are checked, otherwise the selected ones.

**Shortcuts** are allowed only on `main.menu.*` anchors. A key sequence that
GpgFrontend or an earlier module already uses is dropped, with a warning in the
log.

### Sandbox Limits

Each module gets its own Lua state, on the GUI thread, with a reduced standard
library:

- No `io`, `os`, `package`, `debug` or `coroutine`. No `load`, `loadfile`,
  `dofile` or `require`. No files, network, processes, threads or timers.
- `string` has no `dump`, and `math` has no `random`. `print` writes to the
  module log.
- At most 8 MiB of memory per module.
- At most 200,000 instructions for each `update`, handler or continuation, and
  2,000,000 for loading the script.

A script that fails to load leaves nothing behind: every action, mount and
subscription it made is rolled back.

## Learn More

- [Modules README][modules-readme]: writing a module step by step, events,
  storage, GPG operations, translations, packaging and signing.
- [SDK README][sdk-readme]: the full API reference, the complete Lua API and
  anchor catalog, native widget protocols, and the teardown order.
- The bundled modules in `modules/src` are complete examples. `m_pgp_inspect` is
  small. `m_key_server_sync` shows commands with arguments, a dialog, a settings
  page and key details buttons.

[modules-readme]:
  https://github.com/saturneric/GpgFrontend-Modules/blob/main/README.md
[sdk-readme]:
  https://github.com/saturneric/GpgFrontend/blob/main/src/sdk/README.md
