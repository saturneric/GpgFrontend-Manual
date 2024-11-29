---
title: Multi-Key Database Support
sidebar:
  label: Multi-Key Database
---

GpgFrontend introduces **Multi-Key Database Support**, providing users with a
flexible and organized way to manage multiple key databases. This feature is
ideal for users who require separate cryptographic environments for different
projects, organizations, or levels of security.

## Features and Benefits

### Key Features

1. **Multiple Key Databases**: Manage distinct key databases for specific
   purposes or contexts.
2. **Flexible Switching**: Easily switch between databases for different
   operations without affecting other configurations.
3. **Customizable Management**: Add, edit, reorder, or remove databases as
   needed.

### Benefits

- **Improved Security**: Isolate sensitive keys in dedicated databases to
  minimize exposure.
- **Enhanced Organization**: Maintain separate databases for better operational
  clarity.
- **Streamlined Workflows**: Quickly switch between databases for various
  projects or encryption tasks.

## Accessing the Multi-Key Database Feature

### Opening the GnuPG Controller

To manage multiple key databases, follow these steps:

1. **Access the Advanced Menu**

   - Click on the **Advanced** menu in the top navigation bar.
   - Select **Open GnuPG Controller** from the dropdown options.

   ![Open GnuPG Controller](https://image.cdn.bktus.com/i/2024/11/29/abfaa919-2945-1acc-eb35-5c86828a97ca.webp)

2. **Navigate to the Key Database Tab**

   - In the **GnuPG Controller** window, switch to the **Key Database** tab.
   - Here, you will find a list of all configured key databases.

   ![Key Database Tab](https://image.cdn.bktus.com/i/2024/11/29/7a66848e-bc23-fd13-08a4-1923de39369e.webp)

## Managing Key Databases

The **Key Database** tab allows you to perform the following operations:

### 1. Adding a New Key Database

- Click the **Add New Key Database** button.
- Specify a name and path for the new database. This will create an isolated
  environment for new keys.

### 2. Editing and Reordering Key Databases

- Right-click on a database entry to view options like:
  - **Move Up/Move Down**: Reorder the database list.
  - **Move to Top**: Prioritize a database by moving it to the top.
  - **Edit**: Rename or modify the path of an existing database.
  - **Remove**: Delete a database from the configuration.

![Edit and Reorder Options](https://image.cdn.bktus.com/i/2024/11/29/0fd0d56b-532c-f0a8-c263-40d288cd74ba.webp)

> **Note**: Any changes to the key database settings will require an application
> restart to take effect.

### 3. Switching Between Databases

- Use the **Key Toolbox** dropdown in the main interface to switch between
  configured databases.
- Select the desired database, and the corresponding keys will be displayed.

![Switch Databases](https://image.cdn.bktus.com/i/2024/11/29/dd783ee0-df5e-2b6f-428f-784c68246186.webp)

## Use Cases for Multi-Key Databases

1. **Project Isolation**

   - Maintain separate databases for different projects to avoid accidental
     cross-use of keys.

2. **Organizational Separation**

   - Keep departmental or team-specific keys isolated to ensure they are only
     accessible to authorized personnel.

3. **Enhanced Security for Sensitive Keys**
   - Store high-security keys in a dedicated database, minimizing the risk of
     exposure during routine operations.

## Tips for Effective Multi-Key Database Usage

1. **Name Databases Clearly**

   - Use descriptive names for each database to make it easier to identify their
     purpose.

2. **Regular Backups**

   - Backup each database regularly to prevent loss of critical keys. Store
     backups in secure, encrypted locations.

3. **Audit Database Usage**

   - Periodically review the contents and usage of each database to ensure
     proper organization and security.

4. **Isolate Sensitive Operations**

   - For highly sensitive keys, consider using a dedicated device or environment
     to manage their database.

5. **Avoid Overloading Databases**

   - Distribute keys evenly across multiple databases instead of overloading a
     single one. This enhances performance and organization.
