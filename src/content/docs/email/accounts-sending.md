---
title: Mail Accounts and Sending
description: "Add your email account to GpgFrontend, test the connection, and send a signed or encrypted message through your own mail server."
sidebar:
  label: Accounts and Sending
  order: 4
---

To send email, or to read it from your mail server, GpgFrontend needs to know
your mail account. This page shows how to add one and how to send a message.

You only need an account to send and fetch mail. Everything else in GpgFrontend
works without one.

:::note[New in v2.2.3]

Mail accounts and sending are new. Before, you had to send messages with a
separate email app.

:::

## Two Words You Will See

Your mail provider runs two kinds of servers:

- **IMAP** is the server that keeps your mailbox. GpgFrontend uses it to
  **read** your mail.
- **SMTP** is the server that sends mail out. GpgFrontend uses it to **send**.

Your mail provider's help pages list the address of each server. They often
look like `imap.example.com` and `smtp.example.com`.

## Open the Mail Accounts Page

1. Click **Edit** > **Settings**.
2. In the **Features** group, click **Mail Accounts**.

![The Mail Accounts page in Settings][img-1]

## Add an Account

If you have no account yet, the page says **No mail accounts yet**. Click
**Add an Account**. If you already have one, click **Add Account...** under
the list. The **Add Mail Account** window opens. It has four steps:
**Account**, **Servers**, **Check** and **Review**.

1. **Your Account**: type **Your name** (as people will see it), your **Email
   address**, and your **Password**. Click **Continue**.
2. **Servers**: GpgFrontend fills in the servers for you, from your address.
   Choose what the account is for: **Send and receive**, **Receive only** or
   **Send only**. Check the servers under **Server settings**. If they are
   wrong, click **Edit**, change them, and click **Done**. If your provider
   wants a login name that is not your email address, open **Login
   usernames** while editing and fill in **Incoming (IMAP)** and **Outgoing
   (SMTP)**. Click **Continue**.
3. **Connection Check**: GpgFrontend signs in to each server, without sending
   or changing anything. It runs by itself. When everything works, click
   **Continue**.
4. **Review**: check the details. Turn on **Use as the default account** if you
   want this account to be offered first when you send. Your first account
   always becomes the default.
5. Click **Add Account**.
6. Click **OK** at the bottom of the Settings window to save.

Nothing is saved until you click **OK**. If you click **Cancel**, your changes
are thrown away.

:::note[Changed in v2.2.4]

Adding an account is now a guided window that finds your servers for you.
Before, you clicked **Add** and filled in the **Identity**, **Receiving
(IMAP)** and **Sending (SMTP)** sections yourself.

:::

### How GpgFrontend Finds Your Servers

- For well-known providers, such as Gmail, Outlook.com, iCloud, Yahoo, GMX or
  Posteo, GpgFrontend already knows the servers.
- For other addresses, it asks your DNS server (the internet's address book)
  where the mail servers for your domain are. Before it does, the first step
  tells you so. Nothing is looked up while you type.
- If nothing is found, it guesses addresses such as `imap.example.com` and
  `smtp.example.com`.

The **Source** line under **Server settings** says where the servers came
from: built-in settings for your provider, found in DNS, guessed, or
**Entered by you**. If it says the servers were guessed, check them with your
provider's help pages.

### If the Check Fails

Each server shows **Connected** or **Failed**, with the reason. You can:

- Click **Back**, fix the servers, and click **Continue**. The check runs
  again by itself. To run it again without changing anything, click
  **Retry**.
- Tick **Add this account anyway and fix the connection later**, if you want
  to set it up later in Settings.

Click **Stop** to stop the check. Nothing is then verified.

## Change an Account

Click an account in the list to see its details. They are in three parts:

- **Account**: **Display name**, **Email address** and **Password**.
- **Servers**: for receiving and for sending, a **Use this account to
  receive** or **Use this account to send** box, the **Server**, and the
  **Connection** type.
- **Advanced** (click to open):
  - **Reply-To**: where replies should go, if not to your email address. Leave
    it empty if you are not sure.
  - **Incoming user name** and **Outgoing user name**: usually your full email
    address. Leave the outgoing one empty to send without signing in.
  - **Sent folder**: leave it empty. It shows **Discovered automatically**.
    Type a folder name only if your copies of sent mail end up in the wrong
    place.

You can turn on receiving, sending, or both. An account that does neither
cannot be used.

### Connection Choices

The **Connection** list (called **Security** in the **Add Mail Account**
window) decides how your password and mail are protected on
the way to the server. Both choices use **TLS**, which is the standard way to
encrypt the connection between your computer and the server.

| Choice                       | When to use it                                                   | Port it uses       |
| ---------------------------- | ---------------------------------------------------------------- | ------------------ |
| **TLS (recommended)**        | The best choice. Use it unless your provider says otherwise.     | IMAP 993, SMTP 465 |
| **STARTTLS**                 | When your provider asks for it. It also encrypts the connection. | IMAP 143, SMTP 587 |
| **None (this machine only)** | Only for a mail server on your own computer. Not encrypted.      | IMAP 143, SMTP 25  |

You do not type a port number. The port follows your choice, and GpgFrontend
shows it next to the list, for example **Port 993**.

**None (this machine only)** only shows up when the server is your own
computer, such as `localhost`. For any other server, the connection is always
encrypted.

### Password

Type the password for your mail account in the **Password** box.

When you come back later, the box is empty and shows **Leave blank to keep the
stored one**. Leave it empty to keep your saved password. Type a new one only
to change it.

### No Sign-In Through a Web Page

Some providers let other apps sign in through their own web page. This is
called **OAuth2**. GpgFrontend does not support it yet.

If your provider needs it, use an **app password** instead. An app password is
a separate password that your provider makes for one app. You create it in
your provider's account or security settings, then paste it into the
**Password** box. It works only for mail, and you can cancel it at any time
without changing your main password.

## Test the Connection

1. Click **Test Connection** in the **Servers** part. It tests every server the
   account uses, one after the other.
2. Wait. It shows **Testing...**. Click **Stop** if it takes too long.
3. Read the result under each server. Until you test, it says **Not tested**.
   - **Connected successfully.** means it works.
   - Otherwise, you see what went wrong and a hint. For example, **Check the
     user name and password.** or **Check the server address for a typo.**

The test uses what is on screen right now, even before you click **OK**.

## Trust a Server You Run Yourself

If you run your own mail server, its certificate may not be signed by a known
authority. This is called a **self-signed certificate**. A certificate is how a
server proves who it is.

When the test meets such a server, GpgFrontend asks **Trust This
Certificate?** The window shows the certificate details and its SHA-256
fingerprint.

- Click **Yes** only if this is your own server and the fingerprint matches.
- Click **Cancel** if you are not sure. An unknown certificate can also mean
  that someone is trying to listen in.

If you click **Yes**, GpgFrontend trusts **only this exact certificate** for this
account. Any other certificate, even a new one from the same server, is still
refused. Click **Test Connection** again to confirm it works.

Under **Advanced**, the account then says **Receiving server** or **Sending
server**, followed by **Trusting one certificate** and the fingerprint. Click
**Stop trusting it** to undo this.

## Manage Your Accounts

Right-click an account in the list:

- **Set as Default**: make the account the first choice when you send. Its
  details then say **Default account**.
- **Disable**: keep the account, but stop using it. A disabled account is not
  offered for sending or fetching mail, and it is never the default. Its
  settings and password are kept. Choose **Enable** to use it again.
- **Remove**: delete the account. GpgFrontend asks first. Its saved password is
  deleted too.

As always on this page, the change takes effect when you click **OK**.

:::note[New in v2.2.4]

You can now disable an account without removing it.

:::

GpgFrontend checks your accounts before it saves them. It tells you if, for
example, an email address is missing, a server is not filled in, or two
accounts use the same address.

## Where Your Password Is Kept

Your mail password is never saved as plain text in the settings file. It is
kept in GpgFrontend's protected storage, which is encrypted with the
[Application Secure Key](/advanced/app-secure-key/).

Your password is only as safe as that key. For the best protection, guard that
key with your system's keychain or a PIN.

## Send a Message

1. Write your message. See [Write and Protect a Message](/email/compose-protect/).
2. Sign or encrypt it if you like.
3. Click **Send...** (or press Ctrl+Enter; Cmd+Enter on a Mac).

If **Send...** is grayed out, hover over it to see what is missing.

### The Send Message Window

The **Send message** window lets you check everything before the message
leaves. At the top it says: "Ready to send. Nothing has left this computer
yet."

- **Send using**: pick the account to send from. Below it you see the server,
  the port and the connection type.
- **Message**: a summary of what you are sending:
  - **From** and **To**.
  - **Blind copies**: your Bcc people, if any. These addresses go to the mail
    server only. They are not written in the message, so no other reader can
    see them.
  - **Contains**: the size, and how many attachments.

When you are ready, click **Send**. To stop, click **Cancel**.

### Read the Result

While sending, the window says "Sending. This window will say what happened."
The **Result** section then shows two lines:

- **Submission**: did the mail server take the message?
  - **Yes, accepted by the outgoing mail server** means it is on its way.
  - If it failed, this line shows the reason, and the top of the window says
    **Not sent.**
- **Copy in Sent**: was a copy put in your Sent folder?
  - **Yes, saved to ...** names the folder.
  - Many mail servers do not keep a copy of what you send. So GpgFrontend puts
    one in your Sent folder itself, using the account's incoming (IMAP) server.
  - If the account only sends, there is no mailbox, so no copy is kept. The
    message was still sent.

Click **Details** to see more, or **Copy details** to copy them.

When all went well, the window closes by itself after a few seconds. The
**Close** button counts down. Click anywhere in the window to stop the
countdown.

### When the Result Is Unknown

Sometimes the connection drops just after the message went out. Then the
window says: "It is not known whether this was sent."

This means the server may or may not have the message. Before you send it
again:

1. Look in your Sent folder.
2. Or ask the person if they got it.

If you send it again without checking, they may get it twice.

### Closing While Sending

If you close the window while a message is still being sent, GpgFrontend asks
**Still sending**. The server may already have the message. If you close now,
you will not find out if it was delivered.

- Click **Keep Waiting** to stay and see the result. This is the safe choice.
- Click **Close Anyway** to close the window.

To stop a send on purpose, click **Stop** next to **Submission** instead.

## If Something Goes Wrong

- **"No outgoing account is configured."** Add an account that can send, or
  check **Use this account to send** on an existing one. Make sure the account
  is not disabled.
- **"No password is stored for this account..."** Open **Mail Accounts**, select
  the account, type the password in the **Password** box, and click **OK**.
- **The test says the password is wrong.** Check the username. If your provider
  uses web sign-in, make an app password. See
  [No Sign-In Through a Web Page](#no-sign-in-through-a-web-page).
- **The test says the certificate is expired or not yet valid.** Check that the
  clock on your computer is right.

[img-1]: TODO
