---
title: Key Groups
description: "Create and use key groups in GpgFrontend to encrypt to multiple recipients at once, treating a collection of public keys as a single key."
---

A Key Group lets you bundle many public keys together and use them as one key.
This makes it easy to send an encrypted message or file to several people at the
same time.

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
2. **Click the Key Group button.** It is the key icon in the toolbar above the
   key list.
3. **Fill in the details.** A window called New Key Group opens. Type a name. The
   email and comment are optional. Click Create.
4. **Done.** Your new group shows up in the key list with the Type set to
   "group". You can now use it just like a single public key.

![](https://image.cdn.bktus.com/i/2025/06/24/c70891d9ad74b21074be03c7a1d0aabf77d9ea3a.webp)

![](https://image.cdn.bktus.com/i/2025/06/24/bf35548136bc176635dc0fd1175795597701e1dc.webp)

## Edit a group

You can change a group whenever you want. Double-click the group in the list (or
use the group management menu) to open the Key Group Management window. From
there you can add keys, remove keys, or put other groups inside the group.

![](https://image.cdn.bktus.com/i/2025/06/24/4c4c9e18c0c850b4d1bbbf8e0861e7f24fa72269.webp)

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
