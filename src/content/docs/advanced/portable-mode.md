---
title: "Portable Mode"
sidebar:
  label: Portable Mode
  order: 1
---

GpgFrontend offers a Portable Mode to provide users with maximum flexibility and
convenience, particularly for running the application from removable storage
devices (such as USB drives) or non-standard locations, without leaving traces
on the host system.

When Portable Mode is enabled, GpgFrontend stores all user data, configuration
files, secure keys, logs, and other runtime files directly within the
application’s directory structure, rather than using the system’s default user
data folders. This design allows users to move or back up the entire application
and its environment easily.

> Note: Starting from version 2.1.9, Portable Mode is enabled by adding
> PortableMode=true to the ENV.ini file in the working directory. In earlier
> versions (prior to v2.1.9), Portable Mode was activated by creating an empty
> file named PORTABLE.txt in the working directory.

## Key Features

- **Self-Contained Environment:** All configuration, logs, application data
  (data_objs/), secure keys, and modules are stored within the portable
  directory. Nothing is written to system user directories.

- **No System Traces:** Running in Portable Mode avoids leaving personal or
  sensitive data on the host system, making it ideal for shared or temporary
  environments.

- **Cross-Platform Consistency:** Portable Mode works consistently across
  supported operating systems, including Windows, Linux, and macOS (AppImage,
  Flatpak, etc.).

## **How to Enable Portable Mode**

Portable Mode can be enabled via the application’s configuration:

1. In the application’s working directory, create or edit the file ENV.ini.
2. Add the following line to the file:

   ```ini
   PortableMode=true
   ```

3. Save the file and restart GpgFrontend.

Once enabled, the application will operate entirely in Portable Mode, with all
files stored relative to the application’s own directory.

## Notes

- **First Launch:** You can enable Portable Mode at any time, but it is
  recommended to do so before initial setup to ensure all data is stored
  portably from the beginning.
- **AppImage/Flatpak Support:** On Linux, GpgFrontend can detect and adapt to
  being run as an AppImage or within a Flatpak container, and will place user
  data within the application directory accordingly.
- **Disabling Portable Mode:** To revert to standard mode, simply set
  PortableMode=false in the ENV.ini file or remove the line, then restart the
  application. Data previously stored in portable locations will remain, but new
  data will be saved to the default system directories.
