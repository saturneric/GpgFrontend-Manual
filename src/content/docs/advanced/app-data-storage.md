---
title: "Application Data Storage"
description: "How GpgFrontend protects the data it saves for you, such as key server entries and key generation profiles."
sidebar:
  label: Application Data Storage
  order: 9
---

Besides your keys, GpgFrontend saves a few things of its own: key server
entries, key generation profiles, window positions, and similar. The sensitive
parts are encrypted with the program's own key.

This all happens on its own. There is nothing to set up and nothing to
maintain. This page is here for people who want to know what is going on.

For the key that does the protecting, and the choices you have about it, see
[Application Secure Key](/advanced/app-secure-key/).

## How It Works

Each saved item is encrypted on its own, with its own key worked out from the
program's key and that item's name. Nothing is encrypted with one shared key,
so getting at one item tells an attacker nothing about the others.

The encryption is authenticated. If a file is altered, GpgFrontend notices and
refuses it rather than using bad data.

Files are written in a way that cannot leave a half-finished result behind. If
the program or the computer stops in the middle of a write, the old version
survives intact.

## Where the Files Are

Inside your profile, in a folder called `data_objs`. Each file is named after a
scrambled version of what it holds, so the file names give nothing away.

Each [Secure Level](/advanced/memory-security/) keeps its data apart from the
others. That is why lowering the level makes data saved at a higher one
unavailable.

## Key Changes

At the **Maximum** Secure Level, the program's key is replaced every week. Old
files stay readable because each one records which key it was written with, so
GpgFrontend can still open them and re-encrypt them with the new key.

You never see this happen.

:::note[Changed in v2.2.0]

The way this data is protected changed in v2.2.0. Some data saved by v2.1.x or
earlier may not be readable any more.

This has never affected your OpenPGP keys, your messages, or your files. Only
GpgFrontend's own saved settings.

:::
