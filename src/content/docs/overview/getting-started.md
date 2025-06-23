---
title: Getting Started with GpgFrontend
sidebar:
  label: Getting Started
  order: 2
---

Welcome to GpgFrontend, the cross-platform, OpenPGP encryption tool designed for
simplicity and security. This guide will walk you through the installation
process tailored to your operating system, ensuring you can start securing your
communications as quickly and efficiently as possible.

## Before You Begin: Prerequisites

**Note for Windows users: You may skip this prerequisites section.**

GpgFrontend leverages the robust functionalities of GnuPG for encryption,
decryption, and key management. It is crucial to have GnuPG installed on your
device to make full use of GpgFrontend. Starting from version 2.0, GnuPG
operates on modular components for enhanced functionality, requiring proper
integration with your system.

Be aware, due to GnuPG's inability to function within an App Sandbox,
GpgFrontend is not available through the Apple Store.

For Linux users, most contemporary distributions come with GnuPG 2.0
pre-installed. Check your GnuPG version with `gpg --version` in your terminal.
It is advisable to upgrade to GnuPG version 2.2 or later for optimal performance
and compatibility.

## Brief Installation Guide

GpgFrontend is distributed through multiple official channels, making
installation easy on all major platforms. **For the latest download options and
installation commands for your system, please visit the
[Downloads](/overview/downloads) page.**

> Note: The installation methods below provide general guidance. If you prefer
> installing via package managers such as WinGet, Microsoft Store, or Flatpak,
> please refer to the Downloads page for the most up-to-date and recommended
> options.

### For Windows Users

You can choose from several installation methods based on your preferences.

#### Portable Version (No Installation Required)

1. **Download** the portable version from [GpgFrontend's latest
   releases](https://github.com/saturneric/GpgFrontend/releases/latest), labeled
   `GpgFrontend-*******-windows-x86_64-portable.zip`.
2. **Extract** the contents of the downloaded ZIP file.
3. **Run** `GpgFrontend.exe` from the extracted `bin` directory.

#### Installer Version

1. **Download** the MSIX installer from [GpgFrontend's latest
   releases](https://github.com/saturneric/GpgFrontend/releases/latest), named
   `GpgFrontend-*******-windows-x86_64.msix`.
2. **Install** GpgFrontend by following the on-screen instructions. After
   installation, you can access GpgFrontend directly from your desktop.

The MSIX installer is recommended for most users due to improved security,
simpler updates, and better integration with modern Windows features.

### For macOS Users

GpgFrontend's macOS packages are Apple-verified, allowing straightforward
opening without additional permissions.

#### Using Homebrew Cask

For an effortless install or removal process, use Homebrew Cask:

1. Ensure **Homebrew** is installed.
2. **Install** GpgFrontend with the command `brew install --cask gpgfrontend`.
3. **Launch** GpgFrontend from your Launchpad.

#### Installation from DMG

1. **Install GnuPG** via Homebrew or download it from [GPG for OS
   X](https://sourceforge.net/projects/gpgosx/files).
2. **Download** the `GpgFrontend-*******-macos-**.dmg` file from [GpgFrontend's
   latest releases](https://github.com/saturneric/GpgFrontend/releases/latest).
3. **Mount** the DMG file and **run** GpgFrontend.
4. **Optional:** Drag GpgFrontend into your Applications folder for easy access.

### For Linux Users (AppImage)

AppImage simplifies software distribution by bundling applications and all
necessary libraries into a single, executable file, eliminating dependency
conflicts.

1. **Install GnuPG** if it's not already installed.
   - Debian/Ubuntu: `sudo apt update && sudo apt install gpg`
   - Fedora: `sudo yum install gnupg`
2. **Download** the AppImage from [GpgFrontend's latest
   releases](https://github.com/saturneric/GpgFrontend/releases/latest), labeled
   `GpgFrontend-*******-linux-******.AppImage`.
3. **Make it executable:** `chmod u+x ./GpgFrontend-***-linux-******.AppImage`.
4. **Launch** the AppImage with a double-click or through the terminal.

### BSD Users (FreeBSD/OpenBSD)

Currently, there are no binary releases for BSD systems. However, GpgFrontend
can be compiled and run on BSD. Refer to the GitHub repository for build
instructions.

## Basic Operations Index

Before diving into the specific operations, **we highly recommend that beginners
start with the [Fundamental Concepts](/guides/fundamental-concepts/) guide**. It
provides an essential overview of encryption principles, key management basics,
and the main concepts used throughout GpgFrontend.

Then, you can quickly get started by referring to the following topic-specific
guides. For more details about operations and the user interface, please refer to:
[Interface Understanding](/guides/understand-interface/)

- [Generating a Key Pair](/guides/generate-key/)
- [Importing and Exporting Key Pairs](/guides/import-export-key-pair/)
- [File Encryption and Decryption](/guides/file-operations/)
- [Text Encryption and Decryption](/guides/text-opetations/)
- [Using Key Groups](/guides/key-group/)
- [Key Server Operations](/guides/key-server-operations/)
- [Smart Card Operations](/guides/smart-card/)

:::tip

You can also explore more topic-specific guides in the "Brief Guides" section.
If you encounter any questions, it is recommended to consult the dedicated
documentation for each feature first.

:::
