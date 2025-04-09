---
title: A Comprehensive Guide of GpgController
sidebar:
  label: Gpg Controller
---

The **GpgController** in **GpgFrontend** is a powerful tool for configuring and
managing GPG-related settings. It provides advanced options for file operations,
password input methods, and custom GPG configurations, catering to both general
and advanced users.

## Accessing the GpgController

To access the **GpgController**:

1. Navigate to the **Advanced** menu in the top toolbar.
2. Select **Open GnuPG Controller** from the dropdown menu.

![Open GnuPG Controller](https://image.cdn.bktus.com/i/2024/11/29/abfaa919-2945-1acc-eb35-5c86828a97ca.webp)

The **GpgController** interface includes three tabs: **General**, **Key
Database**, and **Advanced**. Below is a detailed explanation of each tab's
features.

## General Tab: Core Settings

The **General** tab provides essential configuration options for GpgFrontend's interaction with GPG.

![General Tab](https://image.cdn.bktus.com/i/2024/11/29/0ee752ca-ecd1-2a86-91b5-f6129184c7a4.webp)

### Available Options

#### Use Binary Mode for File Operations

This option determines the format used for encrypted or signed files:
- **Binary Mode**: Produces compact and efficient files, ideal for storage and
 processing.
- **ASCII Mode**: Generates human-readable files encoded in ASCII format. This
 is useful for sharing files over email or systems that might corrupt binary
 files.

Recommendation: Use binary mode for local file operations and ASCII
mode for file sharing or email attachments.

#### Use Pinentry as Password Input Dialog

GpgFrontend includes a built-in password input dialog designed as a
temporary fallback when no external **Pinentry** program is available.
However, the built-in dialog has limitations and may not work for all
password input scenarios.

Recommendation: Users are strongly encouraged to install a
full-featured **Pinentry** program to ensure a seamless and secure password
input experience. **Pinentry** is optimized for GnuPG's requirements and
provides additional features such as better passphrase caching and hardware
token support.

#### Enable GpgME Debug Log

Enables verbose logging for troubleshooting GPG operations via the
**GpgME** library. This is useful for advanced users diagnosing issues in
encryption or signing workflows.

#### Restart Gpg Agent on Start

Ensures that the GPG agent is restarted whenever GpgFrontend launches. This
helps avoid issues caused by stale GPG agent processes.

#### Kill All GPG Daemons at Close

Terminates all GPG-related background processes when the application exits.
This ensures that no sensitive information is cached in memory or
accessible after the session ends.

Recommendation: Always enable this option for improved security.

> **Note**: Changes to any settings in the General tab will require
> restarting GpgFrontend to take effect.

## Key Database Tab: Overview

The **Key Database** tab allows users to manage multiple key databases. While
detailed documentation is available elsewhere, note the following key points:

- **Add New Key Database**: Easily create and manage isolated key databases for
  different projects or security requirements.
- **Switch Between Databases**: Use the **Key Toolbox** dropdown in the main
  interface to select the active database.

![](https://image.cdn.bktus.com/i/2024/11/29/7a66848e-bc23-fd13-08a4-1923de39369e.webp)

:::tip[Tipps]
> For more information on key database management, refer to the dedicated
> documentation.
:::

## Advanced Tab: Custom GnuPG Configuration

The **Advanced** tab is designed for users who need to configure custom GPG installations.

![](https://image.cdn.bktus.com/i/2024/11/29/ba283263-c9f5-9a6b-44a7-b0adf79684e8.webp)

### Configuring Custom GnuPG

1. **Enable Custom GnuPG**: Check the **Use Custom GnuPG** box to enable this
   feature.
2. **Specify GPG Configuration Path**: Use the **Select GnuPG Path** button to
   locate and set the directory where `gpgconf` resides. This is critical
   because GpgFrontend relies on the paths provided by `gpgconf` to locate
   essential components like `gpg`, `gpgsm`, and `gpg-agent`.
3. **Verifying Custom Configuration**: After setting the path, you can test the
   configuration by running `gpgconf --list-components` in a terminal. This
   command lists all available GPG components and their paths, ensuring that
   GpgFrontend can access themcorrectly.

![](https://image.cdn.bktus.com/i/2024/11/29/a9b9eb46-f064-610f-892e-dfc71f1a45d4.webp)

:::caution
If `gpgconf` is not configured correctly, GpgFrontend may fail to
locate and execute necessary GPG binaries.
:::

## Tips for Using GpgController Effectively

- Choose File Formats Wisely: Use **Binary Mode** for efficiency in local
  operations and **ASCII Mode** for readability and compatibility in file
  sharing.
- Install a Full-Featured Pinentry: Avoid relying on GpgFrontend's built-in
  password dialog for critical operations. Installing **Pinentry** ensures better
  compatibility and security.
