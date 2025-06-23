---
title: Key Groups
---

A Key Group is a powerful feature in GpgFrontend that allows you to manage and
utilize a collection of public keys as if they were a single public key. This
greatly simplifies encryption and access control when you want to address
multiple recipients or roles at once.

## What is a Key Group?

A Key Group is essentially a named set of public keys. Instead of encrypting
data separately for each individual recipient, you can create a group, add the
relevant public keys, and use the group for encryption. All members of the group
will be able to decrypt messages or files encrypted to that group.

## Key Group Characteristics

- Collection of Public Keys: A key group consists of one or more public keys.
- Treated as a Single Key: In GpgFrontend, you can use a key group anywhere a
  single public key would be used, such as for encryption, sharing, or defining
  access.
- Nested Key Groups: Key groups can contain other key groups. This allows you to
  create complex, hierarchical access structures or role-based groups.
- Flexible Management: You can easily add, remove, or reorganize members (public
  keys or other key groups) within a group at any time.
- Naming and Organization: Each key group can be given a unique name for easy
  identification and usage.

## How to Create and Use Key Groups

1. Select Keys to Group: At the Key ToolBox panel, select the public keys you
   want to add to your group by checking the boxes in the “Select” column.
2. Click the “Create Key Group” Button: Once you have selected the desired keys,
   click the Key Group button (key icon) in the toolbar above the key list.
3. Fill in Group Information: A dialog titled New Key Group will appear. Fill in
   the group’s name, email(optional), and an optional comment. Click
   Create to make the group.
4. Key Group Appears in List: After creation, your new key group will appear in
   the key list with Type shown as group. You can now use this group for
   encryption and other operations—just like a single public key.

![](https://image.cdn.bktus.com/i/2025/06/24/0c8840486daaa95b7824b6a9ac34b957c94b175e.webp)

![](https://image.cdn.bktus.com/i/2025/06/24/bf35548136bc176635dc0fd1175795597701e1dc.webp)

## Manage Members and Nested Groups

You can edit a key group at any time. Double-click the group entry (or use the
group management menu) to open the Key Group Management window. Here you can add
or remove keys, or even nest groups within groups.

![](https://image.cdn.bktus.com/i/2025/06/24/4c4c9e18c0c850b4d1bbbf8e0861e7f24fa72269.webp)

## Typical Use Cases

- Team Encryption: Encrypt a document once for an entire project team or
  department. All team members (whose keys are in the group) can decrypt it.
- Role-Based Access: Define groups such as “Developers”, “Managers”, or
  “Auditors” and grant or revoke access by modifying group membership.
- Nested Structures: Organize key groups hierarchically, e.g., a “Project A”
  group containing “Frontend Team” and “Backend Team” key groups.

## Special Notes & Behaviors for Key Groups

Key Groups in GpgFrontend offer flexibility and powerful management for
encryption workflows, but they also come with specific behaviors and rules that
ensure proper usage and system integrity. The following notes highlight
important details about how Key Groups work, their operational constraints, and
how they interact with the broader GpgFrontend environment. Understanding these
points will help you make the most of Key Groups while avoiding common pitfalls.

### Owner Trust Propagation

You can right-click on a Key Group entry to set the Owner Trust level for the
group. When you do this, the Owner Trust value is applied to all public keys
contained within the group (including recursively for nested groups). This is a
convenient way to manage trust settings for many users at once.

### Membership & Encryption Capability

Only keys marked with the E (Encrypt) usage flag can be added to a Key Group. If
a key does not support encryption, you will not be able to include it.

### Automatic Disabling of Invalid Groups

Auto-Disabling on Startup: If, upon startup, any key in a Key Group no longer
meets requirements (e.g., is deleted or loses encryption capability), the Key
Group will be automatically disabled.

- Disabled Key Groups are not shown in the Key ToolBox.
- You can still view and manage them in the Key Management interface, where they
  are highlighted in red to indicate their invalid status.
- The disabled status will propagate: if a nested group becomes unavailable, any
  parent group containing it is also disabled.

### Key Group Usage and Limitations

Key Groups as Encryption Targets Only: In GpgFrontend, a Key Group is treated as
a single encryptable entity—you can use it as a recipient for encryption just
like a public key. Key Groups cannot be used for signing, decryption, or
certification. They are only valid for encryption operations.

### Independence from GnuPG keygroups

Key Groups Are Local to GpgFrontend: GpgFrontend Key Groups are internal objects
managed only by GpgFrontend. They are not connected to GnuPG’s "keygroup"
feature or to the `gpg.conf` file. This means Key Groups are only visible and
usable within GpgFrontend, and will not appear in other OpenPGP tools.
