---
title: Best Practices for OpenPGP Trust Chain Management
description: "Manage the OpenPGP web of trust in GpgFrontend by setting Owner Trust levels and signing other keys' UIDs to build a reliable, decentralized trust model."
sidebar:
  label: Trust Chain Management
---

## What trust means here

When you get someone's public key, how do you know it really belongs to them? In
OpenPGP, there is no central office that checks this for you. Instead, you decide
who to trust. This is called the Web of Trust.

This page shows how GpgFrontend helps you build that trust, and what it can and
cannot do today.

:::note[Needs the GnuPG engine]

The trust features on this page (setting Owner Trust and signing the UIDs of
other keys) come from GnuPG. They only work when GnuPG is the active engine. The
rPGP engine does not support them, so the related menus and dialogs are hidden
when rPGP is on. Switch to GnuPG to manage your trust.

:::

## Owner Trust

Owner Trust is your answer to one question: **how much do I trust this person to
vouch for other people's keys?**

First you check that a key really belongs to the right person, usually by
comparing its fingerprint. Then you give the key an Owner Trust level. That level
says how much you trust the owner to correctly sign other people's keys.

Owner Trust is **not** about whether the key itself is real. It is about how much
you trust the owner to vouch for others. This is what lets you build your own Web
of Trust without depending on a central authority.

![](https://image.cdn.bktus.com/i/2025/06/24/38399d86fb330ca20eab85c33c03331797d32679.webp)

The trust levels are:

- **Unknown:** You have not decided yet.
- **None:** You do not trust this owner to vouch for other keys.
- **Marginal:** You trust this owner a little.
- **Full:** You trust this owner completely.
- **Ultimate:** This is your own key. GpgFrontend sets this for you.

With Owner Trust, you stay in control of your trust network and you do not need
constant updates from key servers.

### How to set Owner Trust

1. **Find the key.** Locate the public key (or key group) in the Key Toolbox
   table.
2. **Right-click it.** This opens the context menu.
3. **Choose "Set Owner Trust Level".**

A window opens where you pick the level (Unknown, None, Marginal, Full, or
Ultimate).

![](https://image.cdn.bktus.com/i/2025/06/24/4b7624b599a5f310d059843c872cf81e6b089ba4.webp)

## How Owner Trust and signing work together

Owner Trust and signing a UID answer two different questions:

- **Signing a UID** says: "Is this key really this person?" This is about the
  key's **validity**.
- **Owner Trust** says: "How much do I trust this person to vouch for other
  people's keys?" This is about trusting the owner as a **referee**.

The two connect like this. GnuPG treats a key as valid for you when either:

- You signed its UID yourself (your own key has Ultimate trust, so your signature
  counts fully), or
- It was signed by people you gave Owner Trust to. By default, one **Full**-trust
  signer is enough, or three **Marginal**-trust signers.

So Owner Trust is the dial that decides **how much other people's signatures
count** toward making a key valid in your eyes. Signing is the act of vouching;
Owner Trust is how much you let other people's vouching influence you.

This is also why we suggest Owner Trust over signing for everyday use. It gives
you the same result without pushing signatures onto public key servers.

## Signing UIDs (not recommended)

You can sign the UID (the name and email) on someone else's public key to say "I
checked this, and it is really them."

:::caution[We no longer recommend this]

A normal UID signature is meant to be shared on key servers, and that causes the
problems below (server rules and key bloat). For your own trust decisions, you
usually do not need that. Set **Owner Trust** to control how much you rely on
someone, and only sign a UID when you truly need to certify that a key belongs to
a person.

:::

When GpgFrontend was first designed, sending these signatures to key servers was
not fully planned for.

![](https://image.cdn.bktus.com/i/2025/06/24/d974152f4b2b850d228408b99d37ea487a3cf914.webp)

### What happens now

- GpgFrontend does not upload your signed UIDs to key servers on its own.
- If you do upload one, whether it is accepted depends on each key server's
  rules.

### Why uploads are not automatic

**Key servers behave differently.**

- Servers like keys.openpgp.org and SKS servers treat third-party signatures
  differently.
- Some accept them, some need the UID checked first, and some reject them.

**Keys would get bigger.**

- Every extra signature makes the public key larger.
- Uploading lots of third-party signatures would bloat keys and slow down syncing.

**Most people do not need it.**

- Most users check fingerprints by hand and rely on Owner Trust.
- Uploading every third-party signature to public servers is usually not needed.

## For organizations

In a big company, plain Owner Trust is often not enough. Larger groups usually
use a Certificate Authority (CA) instead:

- A trusted internal CA signs each member's key.
- Members only need to trust the CA, not check every coworker's key one by one.
- This works like the X.509 certificate system and is usually done with gpgsm
  (an S/MIME setup).

GpgFrontend does not support gpgsm or CA management yet. It may be added later if
users want it.

## What might come later

- An optional prompt after you sign a UID, asking if you want to upload the
  updated key.
- A clear warning about key bloat when uploading third-party signatures.
- Support for organization trust models, such as CA-based signing and
  certificates.
