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

- Windows 10 or later (Windows 7 can work with the separate Qt5 build, but it
  is not recommended)
- macOS 15 or later, on both Intel and Apple Silicon
- Ubuntu 22.04 or later, or a comparable Linux distribution, on both x86_64
  and arm64

> Note: Only 64-bit machines are supported.

## GnuPG

- Minimum 2.2.0. Versions below 2.1.0 are refused at startup, and some
  features need newer versions than 2.2.0.
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
optional things, such as update checks or sending public keys to key servers.
