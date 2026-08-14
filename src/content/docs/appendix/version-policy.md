---
title: Version Numbering Policy
description: "What GpgFrontend version numbers mean, why they do not follow Semantic Versioning, and what each release series set out to do."
sidebar:
  label: Version Policy
  order: 5
---

Every copy of GpgFrontend has a version number, like `v2.2.2`. That number does
not tell you how big a release was or how much work went into it.

It tells you which chapter of the project you are holding.

## What the Numbers Mean

A version number has three parts. Here is `v2.2.2`:

| Part      | Name       | What it means                                                   |
| :-------- | :--------- | :-------------------------------------------------------------- |
| **2**.2.2 | Generation | The app was rebuilt from the ground up. This has happened once. |
| 2.**2**.2 | Series     | The app took a new direction.                                   |
| 2.2.**2** | Release    | A new version came out inside that direction.                   |

The first two numbers together are called the **series**. In `v2.2.2`, the series
is **2.2**. This is the part that matters most, and it is how the project talks
about its own versions.

The last number just counts releases inside the series. `v2.2.1` came first, then
`v2.2.2`.

## A Big Release Can Still Be a Small Number

This surprises people, so it is worth saying clearly.

The last number going up does **not** mean the release was small. It only means
the app kept going in the same direction.

For example, `v2.2.1` to `v2.2.2` looks like a tiny step. That release added
[Profiles](/advanced/profiles/), portable profile files you can carry around,
Instant Messaging tokens, a new key list, and a rebuilt settings window.

:::note[How to tell how big a release is]
Do not judge it by the number. Read the release notes on the
[releases page](https://github.com/saturneric/GpgFrontend/releases). They say what
actually changed.
:::

## Why Not Semantic Versioning

You may have heard of **Semantic Versioning**. It is a common set of rules for
numbering software.

Those rules were written for code libraries: software that other programmers
build their own programs on top of. The numbers answer one question: _did
something break for the programmers using this?_

GpgFrontend is an app you use, not a library programmers build on. No other
program is built on top of it, so that question does not apply.

So the numbers here answer a different question: _what is this app trying to be
right now?_

## What Starts a New Series

A new series starts when the project decides to take the app somewhere new. The
decision comes first, and it is usually written down before the code exists.

Two real examples:

- **2.1** moved the app onto a modern toolkit and let you choose which copy of
  GnuPG to use.
- **2.2** added a second engine, rPGP, so GnuPG was no longer the only way to do
  the work. This is why the app is now described as having a "dual-engine core".

Plenty of things do **not** start a new series, even when they are large. A pile
of new features, a redesigned screen, or a lot of fixes all ship as a normal
release. The direction did not change, so the series did not either.

## The Story So Far

| Series  | What it was about                                                                             |
| :------ | :-------------------------------------------------------------------------------------------- |
| **1.0** | Being real software. Getting the app packaged and signed so people could actually install it. |
| **1.1** | Working with files, through a built-in file browser.                                          |
| **1.2** | Getting your encrypted text out to other people, and starting translations.                   |
| **2.0** | A rebuilt core. Everything inside was rewritten.                                              |
| **2.1** | A modern toolkit, more control over GnuPG, and a long run of steady, careful releases.        |
| **2.2** | Two engines instead of one, plus support for newer OpenPGP standards.                         |

The 2.0 release notes show that the number was picked on purpose:

> "Since the core part of the code and the organizational structure are different
> from the previous version, **the version number of this version of GpgFrontend
> starts from v2**."

## Why the Numbers Stay Small

GpgFrontend has been going since 2021, and the first number has changed once.

Many projects raise their version numbers often, because a bigger number looks
like progress. This project does not. The number moves when the app really
changes, and stays put when it does not.

That is a deliberate choice, described in the maintainer's article
["The Past and Present of GpgFrontend"](https://blog.bktus.com/en/archives/u8hywl/):

> "I firmly believe that **steady progress is more valuable than blind
> innovation**."

## Stable, Beta, and Nightly

Not every build is meant for everyday use:

- **Stable** is a normal release, like `v2.2.2`. This is the one you want.
- **Beta** has extra text on the end, like `v2.2.0-beta.1`. It is an early look at
  a new series, for people who want to help test it.
- **Nightly** is an automatic test build, made from the newest code. It can be
  broken.

Nightly builds run under the name **GpgFrontend Testing** and keep their own
separate data, so they leave your everyday keys and settings alone.

:::caution[A beta is a normal install]
A beta is not kept separate. It uses the same keys and settings as your usual
copy. Back up your keys before you try one.
:::

See [Downloads](/overview/downloads/) for where to get each one, and the
[FAQ](/overview/faq/) for more about nightly builds.

## Older Versions

When a new series begins, the previous one does not stop right away. It keeps
getting bug fixes and security updates for a while, but no new features. The
`2.1.x` series is in that state now.

The app's built-in update check only offers you newer versions **from your own
series**. It will not move you to a different one on its own. Moving to a new
series is something you choose to do yourself, by downloading it from the
[Downloads](/overview/downloads/) page.
