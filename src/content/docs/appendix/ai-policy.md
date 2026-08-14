---
title: AI Policy
description: "How AI coding tools are used to develop GpgFrontend, what they are not allowed to do, and how every change is checked before it reaches you."
sidebar:
  label: AI Policy
  order: 6
---

AI coding tools help build GpgFrontend. They never touch your keys, and they do
not write the encryption. Every change is planned and checked by a person before
it reaches you.

This page explains how that works, so you can judge it for yourself.

## The Short Answer

If you only read one thing, read this table.

| Your question                         | Answer                                                                |
| :------------------------------------ | :-------------------------------------------------------------------- |
| Is there AI inside the app?           | **No.** There is no AI feature of any kind.                           |
| Does anything I do get sent to an AI? | **No.** There is no AI service in the app to send it to.              |
| Did AI write the encryption?          | **No.** GnuPG and rPGP do that, and the app has no crypto of its own. |
| Was this app designed by AI?          | **No.** It has been built by hand since 2021.                         |
| Is AI used at all, then?              | **Yes.** It helps write ordinary code, tests and documentation.       |

## The Project Came First

GpgFrontend was not made by asking a machine for an app.

Work started in **May 2021**. About two thirds of all changes were written
before any AI tool touched the project, and so was the whole design. The parts
that keep the app safe were designed and written by hand:

| When     | What                                                                                                |
| :------- | :-------------------------------------------------------------------------------------------------- |
| **2021** | The core was thrown away and rewritten from scratch. This is why the version number jumped to 2.    |
| **2023** | The module system, which lets parts of the app be built and loaded separately.                      |
| **2025** | A full security overhaul in v2.1.9, covering how keys are stored, protected in memory, and rotated. |

That work came from years of reading and studying, as described in the
maintainer's article ["The Past and Present of
GpgFrontend"](https://blog.bktus.com/en/archives/u8hywl/).

GpgFrontend is also not the biggest system its
[maintainer](https://blog.bktus.com/en/about-me/) has worked on. Behind it are
years of backend engineering on far larger systems, and graduate study in
cryptography, security and computer systems.

That background includes knowing how these AI models work and where they fail.
They are treated as what they are: fast, tireless, and confident even when they
are wrong.

## What the Tools Actually Do

They are an assistant. They write ordinary code, tests, interface work and
documentation, and they help review changes for mistakes.

The first reason for using them is speed. The maintainer estimates that work now
goes more than five times faster than before.

The more important change is what gets done at all. Two kinds of work used to be
put off:

- **Tests.** Writing them is slow and dull, and it was easy to keep postponing.
  The app now ships with well over a thousand automated tests, around 20,000
  lines of them.
- **Interface code.** The repetitive part of building windows, dialogs and
  settings pages. There are 66 of those, and about 53,000 lines of interface
  code, most of it the same patterns over and over.

That is the trade. The tools do the slow, repetitive work. The maintainer keeps
the work that needs judgment: designing how the app fits together, and trying
out new ideas.

## What They Are Not Allowed to Do

These limits do not move, and they are the ones that matter for your safety.

**They do not write the cryptography.** The real work of encrypting, signing and
handling keys is done by **GnuPG** and **rPGP**. Those are long-standing,
independent projects with their own developers, their own review and their own
audits. GpgFrontend asks them to do the job rather than inventing its own.

You can check this yourself, without trusting anybody. The source code contains
no encryption algorithms of its own. It calls the GnuPG library from more than
four hundred places, and the rPGP library from the Rust side. There is no
home-made cryptography in it to get wrong, no matter who or what wrote the
surrounding code.

**They are not in the app.** Neither GpgFrontend nor any of its modules contains
an AI feature or contacts an AI service. Nothing you type, encrypt, sign or open
is sent anywhere.

**They never see your data.** Development happens on test keys and sample files.
Your keys stay on your computer, so no AI tool has any route to them.

## How Every Change Is Checked

Using an assistant does not lower the bar. Every change clears the same checks:

| Check                      | What it means                                                                                                            |
| :------------------------- | :----------------------------------------------------------------------------------------------------------------------- |
| **A person directed it**   | What the change should do is decided first. The result is then checked against that, and rewritten if it does not match. |
| **It builds**              | It compiles on Windows, macOS and Linux.                                                                                 |
| **It passes the tests**    | More than a thousand automated tests, around 20,000 lines of them, run against the code.                                 |
| **It still interoperates** | Separate tests check that keys and messages still work with GnuPG and follow the OpenPGP standard.                       |

Nothing is accepted just because a tool produced it. A change that cannot be
explained does not go in.

:::note[You do not have to take our word for any of this]
Every line of source is public, and every official release is built in the open
by GitHub Actions and then signed. You can check that the copy you downloaded
matches the code it claims to come from. See [Code & Binary
Verify](/appendix/code-binary-verify/).
:::

## If You Contribute

You are welcome to use AI tools. Two rules apply:

1. **You own what you send.** You must understand every line of your patch and
   be able to explain it. If you cannot, it is not ready.
2. **You must have run it.** Build it and run the tests first. Do not send
   output you have not read and tried.

The same goes for bug reports. Check the problem against the real code and
include the steps to reproduce it. A report based only on an AI guess wastes
time the project does not have.

For everything else, see [Contributing to
GpgFrontend](/appendix/contribute/).

## The Wiki and This Manual

The project links to an [AI-assisted
Wiki](https://deepwiki.com/saturneric/GpgFrontend), generated automatically from
the source code by an outside service. It is useful for finding your way around,
but it is not written by the maintainer and it can be wrong about details. Use
it to get oriented, and check anything important against the source code.

This manual is a different case. The maintainer's first language is Chinese, and
the manual is written in English, so AI tools help turn rough notes into clear
English. Every page is read and checked by a person before it goes out. These
tools are better at wording than at facts, so the facts here are checked against
the source code and the release notes.

Mistakes still get through. If you find one, please report it. Every page has an
"Edit page" link, or you can write to the address on the
[Contact](/overview/contact/) page.

## Why This Page Exists

Plenty of projects use these tools quietly. For an ordinary app, that might not
matter much.

A security tool is different. If you cannot see how something is made, you are
being asked to trust it on faith. This page says plainly what the tools are used
for, what they are kept away from, and how every change is checked. That is a
better basis for trust than silence.

Being open about using these tools is not the same as being built by them. The
design, the security decisions, and the responsibility for this app stay with the
person who has been maintaining it since 2021.
