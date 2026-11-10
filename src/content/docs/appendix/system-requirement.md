---
title: System Requirement
description: "Recommended hardware and operating system requirements for running GpgFrontend on Windows, macOS, and Linux."
sidebar:
  order: 1
---

This page lists what you need to run GpgFrontend. For the libraries the app is
built with, see [Dependencies](/extra/dependencies/).

## Hardware

These values are recommendations, not strict limits. The app may run fine on
weaker machines too.

- RAM: 2 GB or more
- Disk: 200 MB free for the app itself, plus space for GnuPG and your data
- CPU: a dual-core processor or better

## OS

These are the oldest systems the official builds run on:

- Windows 10 (version 1809) or later. Windows 7 can only run the older v2.1.x
  line, which still has Qt5 builds. It is not recommended.
- macOS 15 or later, on both Intel and Apple Silicon
- Linux on x86_64: Ubuntu 22.04 or later, or a comparable distribution (glibc
  2.35 or newer)
- Linux on arm64: Ubuntu 24.04 or later, or a comparable distribution

> Note: Only 64-bit machines are supported.

:::note[Changed in v2.2.3]

There are no Qt5 builds of v2.2.x. If your system needs Qt5, use a v2.1.x
release. See [Downloads](/overview/downloads/).

:::

## GnuPG

- Minimum: 2.2.0. Some features need a newer version.
- Recommended: 2.4.0 or later.
- On Windows, the official packages already include a recent GnuPG, so there
  is nothing extra to install.

Since v2.2, the app also has a second, built-in engine (rPGP). If GnuPG is
missing, or older than 2.1.0, GpgFrontend does not use it. The app still
starts and works through rPGP. But the features that depend on GnuPG, such as
smart cards, stay unavailable until a working GnuPG is found.

## Optional on Linux

To let GpgFrontend keep its own key in your system password store, you need a
password service running, such as GNOME Keyring or KWallet, plus the libsecret
library:

- Debian and Ubuntu: `libsecret-1-0`
- Fedora: `libsecret`

Without them, that option is greyed out in the settings. Everything else
works as normal. See [Application Secure Key](/advanced/app-secure-key/).

## Network

GpgFrontend works without the Internet. You only need a connection for
optional things, such as update checks, key servers, or sending and reading
email.
