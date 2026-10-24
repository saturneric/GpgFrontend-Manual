---
title: Key Groups
description: "Create and use key groups in GpgFrontend to encrypt to multiple recipients at once, treating a collection of public keys as a single key."
sidebar:
  label: Key Group
  order: 13
---

A Key Group lets you bundle many public keys together and use them as one key.
This makes it easy to send an encrypted message or file to several people at the
same time.

:::note[Not the same as a key category]

A key group is something you can **encrypt to**. It behaves like a key.

A [key category](/guides/key-categories/) only tidies up your key list. You
cannot encrypt to one.

:::

## What is a Key Group?

Think of a Key Group as a mailing list for encryption. You give the group a name
and put public keys inside it. When you encrypt to the group, every person whose
key is in the group can open the message.

Without a group, you would have to pick each person's key one by one. With a
group, you pick the group once and you are done.

## What you should know

- A group holds one or more public keys.
- You can use a group anywhere you would use a single public key, such as when
  you encrypt a file.
- A group can hold other groups inside it. This helps you build bigger groups
  out of smaller ones.
- You can add or remove keys from a group at any time.
- Each group has a name so you can find it easily.

## Create a Key Group

1. **Pick the keys.** In the Key ToolBox panel, check the box in the "Select"
   column next to each public key you want in the group.
2. **Click the New Key Group button.** It is in the toolbar above the key list.
3. **Fill in the details.** A window called **New Key Group** opens. Type a
   **Name**. The **Email** and **Comment** are optional. Click **Create**.
4. **Done.** Your new group shows up in the key list with the Type set to
   "group". You can now use it just like a single public key.

![][img-1]

![][img-2]

![A key group in the Key ToolBox][img-4]

## Edit a group

You can change a group whenever you want. Double-click the group in the list to
open the **Key Group Management** window.

![][img-3]

:::note[Changed in v2.2.3]

The **Key Group Management** window has a new layout. It also shows groups
inside groups as a tree.

:::

The window has three parts:

- **At the top**: the group's name, with two buttons:
  - **Edit…** changes the group's name, email, and comment.
  - **Delete Group…** deletes the group. The keys in it are not deleted.
- **On the left, Members**: the keys and groups that are in this group now. A
  group inside this group shows its own members below it. Type in the **Filter
  members** box to find a member.
- **On the right, Available Keys**: keys and groups you can still add.

### Add keys to the group

1. In **Available Keys**, check the box next to each key or group you want.
2. Click **Add**, or press **Alt+Left**.

Press **Ctrl+F** to jump to the search box above **Available Keys**.

### Remove keys from the group

1. In **Members**, check the box next to each key you want to take out.
2. Click **Remove**, or press **Alt+Right**. You can also press **Delete**.

### Right-click a member

Right-click a key or group in **Members** for these choices:

- **Remove from Group**: take this member out of the group. This shows only for
  direct members, not for keys inside a nested group.
- **Manage Group…**: open a nested group in its own **Key Group Management**
  window.
- **Key Details…**: show the details of a key.

### Change the name, email, or comment

1. Click **Edit…** at the top of the window.
2. The **Edit Key Group** window opens. Change the **Name**, **Email**, or
   **Comment**.
3. Click **Save**.

These details only name the group. Changing them does not change which keys are
in it.

## When to use Key Groups

- **A whole team.** Encrypt a file once for your whole team. Everyone whose key
  is in the group can open it.
- **Roles.** Make groups like "Developers", "Managers", or "Auditors". To give
  or take away access, just change who is in the group.
- **Groups inside groups.** Build a big group from smaller ones. For example, a
  "Project A" group can hold a "Frontend Team" group and a "Backend Team" group.

## Things to keep in mind

Key Groups are easy to use, but they follow a few rules. Read these so you know
what to expect.

### Setting trust for the whole group

Right-click a group and set the Owner Trust level. That trust level is then
applied to every key in the group, including keys in any groups nested inside it.
This is a fast way to set trust for many people at once.

### Only encryption keys can join

You can only add a key that can encrypt (it has the E flag). If a key cannot
encrypt, you cannot add it to a group.

### Broken groups turn off by themselves

When you start GpgFrontend, it checks each group. If a key in a group is gone or
can no longer encrypt, the group is turned off.

- A turned-off group does not show in the Key ToolBox.
- You can still see and fix it in the Key Management screen, where it is shown in
  red so you know something is wrong.
- If a group inside another group breaks, the outer group is turned off too.

### What groups can and cannot do

A Key Group is only for encryption. You cannot use a group to sign, to decrypt,
or to certify.

### Groups stay inside GpgFrontend

Key Groups live only inside GpgFrontend. They are not the same as GnuPG's
"keygroup" feature and they are not saved in the `gpg.conf` file. Other OpenPGP
tools will not see your groups.

[img-1]: https://image.cdn.bktus.com/i/2026/10/25/57e048acae5d42e3a10525cdb04063ca86e1d313-0.webp
[img-2]: https://image.cdn.bktus.com/i/2026/10/25/1dbb1a9a7c3b0485afb742541f7ca84ade0df728-0.webp
[img-3]: https://image.cdn.bktus.com/i/2026/10/25/b3aac622bf1127f32ad3ab69979bc75ba70e2f04-0.webp
[img-4]: https://image.cdn.bktus.com/i/2026/10/25/1df29ddb6cbc7e0c069083a26b9b8e8fe9067da3-0.webp
