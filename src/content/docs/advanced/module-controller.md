---
title: "Module Controller: Extending GpgFrontend Functionality"
sidebar:
  label: Module Controller
---

The **Module Controller** in **GpgFrontend** allows users to manage modular
extensions that enhance the core functionality of the application. These modules
provide features such as email integration, version checking, and key
synchronization, offering flexibility for different workflows.

This guide provides an overview of the **Module Controller** interface,
instructions for managing modules, and guidance for advanced users interested in
developing custom modules.

---

## Accessing the Module Controller

To access the **Module Controller**:

1. Open the **Advanced** menu in the top toolbar.
2. Select **Open Module Controller**.

   ![Open Module Controller](https://image.cdn.bktus.com/i/2024/11/29/fa515b3c-d9b1-70f5-c355-832b6bf07a38.webp)

The **Module Controller** interface consists of the following tabs:

- **Registered Modules**
- **Global Register Table**

---

## Registered Modules Tab

The **Registered Modules** tab displays all available modules and provides tools
for managing their activation, metadata, and storage.

### Key Features

1. **Module List**

   - The left panel lists all currently available modules.
   - Modules prefixed with `*` are **Integrated Modules**, meaning they are
     bundled with the GpgFrontend application.

2. **Module Information**

   - When a module is selected, detailed metadata is displayed in the right
     panel, including:

     - **ID**: The unique identifier of the module.
     - **Version**: The current module version.
     - **SDK Version**: The version of the SDK required by the module.
     - **Path**: The physical location of the module file.
     - **Activation Status**: Indicates whether the module is active or set to
       auto-activate.

     Example:

     ```
     - ID: com.bktus.gpgfrontend.module.email
     - Version: 1.0.0
     - SDK Version: 2.1.5
     - Path: /path/to/module/file
     - Auto Activate: True
     - Active: True
     ```

   ![Registered Modules](https://image.cdn.bktus.com/i/2024/11/29/b35d35f9-4ae2-0d3b-917d-a6fb815711f9.webp)

3. **Module Actions**

   - **Deactivate**: Temporarily disables the selected module.
   - **Disable Auto Activate**: Prevents the module from loading automatically
     when GpgFrontend starts.

4. **Show Mods Directory**

   - Opens the directory where external modules are stored. Users can manually
     add or remove custom modules by placing or deleting files in this
     directory.

   > **Tip for Integrated Modules**:

   - **Windows/Mac Users**: Integrated Modules (prefixed with `*`) can be
     removed by deleting the corresponding `.dll` (Windows) or `.dylib` (Mac)
     file from the `modules` directory.
   - **Linux Users**: Due to the nature of **AppImage** and **Flatpak**
     packages, removing Integrated Modules may require recompiling and
     repackaging the application.

## Global Register Table Tab

The **Global Register Table** provides a detailed view of the internal data
structure used by GpgFrontend and its modules. This table is primarily useful
for developers and advanced users who want to debug or inspect module
interactions with the core application.

### Key Features

1. **Key-Value Data**

   - Displays the hierarchical structure of global variables, including:
     - Module-specific settings (e.g., version checking, state tracking).
     - GnuPG paths and environment configurations.
   - Example:
     ```
     gpgme:
       ctx:
         app_path: /opt/homebrew/Cellar/gnupg/2.4.5_1/bin/gpg
         gnupg_version: 2.4.5
         gpgconf_path: /opt/homebrew/bin/gpgconf
     ```

2. **Navigation**

   - Expand nodes to explore detailed properties for modules or core components.

   ![Global Register Table](https://image.cdn.bktus.com/i/2024/11/29/e4a74c1d-c81a-166f-abd8-4f3f4f92f4d0.webp)

## Developing Custom Modules

The **Module Controller** supports custom modules, allowing developers to extend
GpgFrontend's functionality for specialized use cases. All modules adhere to a
strict **C ABI (Application Binary Interface)** and are dynamically linked to
the `libgpgfrontend_sdk` library.

### Key Points for Developers

1. **C ABI Compliance**

   - Modules must be implemented using the C ABI to ensure compatibility across
     all supported platforms (Windows, macOS, Linux).

2. **Dynamic SDK Linking**

   - Modules interact with GpgFrontend by linking dynamically to the
     **libgpgfrontend_sdk** library. This library provides the necessary
     interfaces for module initialization, data exchange, and runtime
     interaction.

3. **SDK Limitations**

   - The current SDK API is still under development and may not cover all
     potential use cases. Developers are encouraged to contact the project
     maintainer for guidance or feature requests.

4. **Getting Started**
   - Place the compiled module file (`.dll`, `.dylib`, or `.so`) in the
     `modules` directory. Use the **Show Mods Directory** button to locate this
     directory.

---

## Tips for Managing Modules

1. **Backup Before Changes**

   - Always create a backup of the `modules` directory before making changes,
     especially when adding or removing modules.

2. **Regular Updates**

   - Check for updates to both GpgFrontend and its modules to ensure
     compatibility and access to the latest features.

3. **Safe Removal**

   - Follow the guidelines for deleting Integrated Modules based on your
     platform to avoid accidental issues.

4. **Use Global Register Table for Debugging**
   - Advanced users can verify module configurations and GPG environment paths
     through the **Global Register Table**.

---

## Example Module: Version Checking

The **VersionChecking** module is a bundled example of how GpgFrontend uses
modules to provide additional functionality.

### Features:

- Checks the current application version.
- Displays release notes for new updates.
- Notifies users when an upgrade is available.

### Example Metadata:

```
- ID: com.bktus.gpgfrontend.module.version_checking
- Version: 1.0.0
- Auto Activate: True
```

### Global Register Table:

```
com.bktus.gpgfrontend.module.version_checking:
  current_version: v2.1.5
  need_upgrade: false
  latest_version: v2.1.5
```

---

By leveraging the **Module Controller**, users can customize and extend
GpgFrontend to suit their needs. Developers interested in creating new modules
are encouraged to experiment with the SDK and collaborate with the maintainer
for additional API support. For more details, visit the [GpgFrontend Modules
GitHub
Repository](https://github.com/saturneric/GpgFrontend-Modules/blob/main/README.md).