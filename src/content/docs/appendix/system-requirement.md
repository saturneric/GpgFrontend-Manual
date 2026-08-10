---
title: System Requirement
description: "Recommended hardware and operating system requirements for running GpgFrontend on Windows, macOS, and Linux."
sidebar:
  order: 1
---

The following are mainly the recommended system requirements for running
GpgFrontend. However, these are not strict requirements, and the application may
run smoothly on lower-spec machines.

## Hardware

For smooth operation, we recommend:

- RAM: 2 GB for basic desktop environments;
- Disk: 200 MB free for the Application itself, plus additional space for GnuPG and user data; 
- CPU: Dual-core processor or better for general use;

## OS

- Windows 10 or later (Windows 7 possible with the Qt5 version, but not recommended)
- macOS 13 or later
- Ubuntu 22.04 or later

> Note: Only 64-bit machines are supported.

## GnuPG

- Minimum 2.2.0 (but some features may not work properly)
- Recommended 2.4.0+

## Optional on Linux

To let GpgFrontend keep its own key in your system password store, you need a
password service running, such as GNOME Keyring or KWallet, plus the libsecret
library:

- Debian and Ubuntu: `libsecret-1-0`
- Fedora: `libsecret`

Without these, that option is greyed out in the settings. Everything else works
as normal. See [Application Secure Key](/advanced/app-secure-key/).

## Network

Although not necessary for basic operation, an active Internet connection may be
required for software updates or uploading public keys to key servers.
