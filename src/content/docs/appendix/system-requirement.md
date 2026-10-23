---
title: System Requirement
description: "Recommended hardware and operating system requirements for running GpgFrontend on Windows, macOS, and Linux."
sidebar:
  order: 1
---

These are the recommended requirements for running GpgFrontend. They are not
strict; the app may run fine on weaker machines too.

## Hardware

For smooth operation, we recommend:

- RAM: 2 GB or more
- Disk: 200 MB free for the app itself, plus space for GnuPG and your data
- CPU: a dual-core processor or better

## OS

- Windows 10 or later. Windows 7 can only run the older v2.1.x line, which
  still has Qt5 builds. It is not recommended.
- macOS 15 or later, on both Intel and Apple Silicon
- Ubuntu 22.04 or later, or a comparable Linux distribution, on both x86_64
  and arm64

> Note: Only 64-bit machines are supported.

:::note[Changed in v2.2.3]

There are no Qt5 builds of v2.2.x. If your system needs Qt5, use a v2.1.x
release. See [Downloads](/overview/downloads/).

:::

## GnuPG

- Minimum 2.2.0. Some features need newer versions than 2.2.0.
- GnuPG older than 2.1.0 is not used at all. GpgFrontend still starts, but it
  uses the built-in rPGP engine instead.
- Recommended: 2.4.0 or later.
- On Windows, the official packages already include a recent GnuPG, so there
  is nothing extra to install.

Since v2.2, the app also ships a second, built-in engine (rPGP). If GnuPG is
missing or too old, the app still starts and works through rPGP, but the
features that depend on GnuPG, such as smart cards, stay unavailable until a
working GnuPG is found.

## Optional on Linux

To let GpgFrontend keep its own key in your system password store, you need a
password service running, such as GNOME Keyring or KWallet, plus the libsecret
library:

- Debian and Ubuntu: `libsecret-1-0`
- Fedora: `libsecret`

Without these, that option is greyed out in the settings. Everything else works
as normal. See [Application Secure Key](/advanced/app-secure-key/).

## Network

GpgFrontend works without the Internet. You only need a connection for
optional things, such as update checks, key servers, or sending and reading
email.
