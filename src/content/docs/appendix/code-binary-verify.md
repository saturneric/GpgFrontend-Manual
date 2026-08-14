---
title: Code & Binary Verify
description: "How to check that your copy of GpgFrontend is genuine and untouched, from signed packages to building it yourself."
sidebar:
  order: 2
---

When you download software, one question matters: is this really the app the
developer made, or did someone change it on the way to you?

For a security tool, that question matters twice. This page shows how
GpgFrontend lets you check, and how deep you can go.

## Nobody Builds the App by Hand

Every official release is built by **GitHub Actions**, an automatic build
service. It takes the source code straight from the public repository,
compiles it, and publishes the result. No person builds release files on their
own computer and uploads them.

The build recipe is public too, in the repository file
`.github/workflows/build.yml`. So anyone can see exactly how each release
was made, and anyone can repeat it.

## Every Package Is Signed

Since version 1.0.5, every release package is signed with the maintainer's
OpenPGP key. Next to each download there is a small `.sig` file. With standard
GPG tools, you can use it to check that the package is genuine and was not
changed by anyone.

Each system also adds its own check on top:

### Windows

All programs and installers are signed with a
[Certum](https://www.certum.eu/en/certum-by-asseco/) code signing certificate.
Windows checks this itself. You can also look at it yourself: right-click the
file, open Properties, and look at Digital Signatures.

![](https://image.cdn.bktus.com/i/2025/06/25/2eb0e5a1ff970b6d97ed38f18b45476c9aad6ee7.webp)

### macOS

The app is signed with an Apple developer certificate and passes Apple's
notarization check. macOS verifies both automatically the first time you open
the app. If the app had been changed, macOS would refuse to start it.

![](https://image.cdn.bktus.com/i/2025/06/24/cbc3a2ec86515bf5882d1249179e5e06053ada5f.webp)

### Linux

The AppImage comes with a `.sig` file, like the other packages. Check it with
GPG before you run the app. Flatpak and other formats bring their own
signature and sandbox systems on top.

![](https://image.cdn.bktus.com/i/2025/06/24/690c6b534ab54130dfa100f85a8cc299a0223ff5.webp)

## Check Inside the App

Open the About window from the Help menu. It shows the version, the platform,
and the exact branch and commit hash of the source code this copy was built
from. That lets you match your running app to a specific point in the public
code history.

![](https://image.cdn.bktus.com/i/2025/06/24/fe75a2c041c9e5a7823d0c4d8820bf35501117cd.webp)

## The Signing Key

All commits and release packages are signed with the maintainer's OpenPGP key.
The key and its fingerprint are published at
[bktus.com/openpgp](https://bktus.com/openpgp/). Get the key there, check the
fingerprint, and use it to verify the `.sig` file that comes with each release.

## When the Stakes Are Very High

The checks above are enough for everyday use. But if your safety, your freedom
or your work depends on this software, hold it to a higher standard: do not
use any prebuilt binary at all, not even ours.

Every prebuilt binary asks you to trust the machines and services that built
it. For most people that trust is reasonable. In a truly critical situation,
you can remove it: build the app yourself, from source code you have checked.

If you are in that situation, this is the path:

1. **Get the source, not a binary.** Clone the repository and check out an
   official release tag. Verify the tag's GPG signature with the maintainer's
   key from [bktus.com/openpgp](https://bktus.com/openpgp/).
2. **Read before you build.** Review the code yourself, or have someone you
   trust review it. Pay attention to the build scripts too, not only the app
   code.
3. **Build on a machine you trust.** Use a clean, freshly installed system
   used only for this build. Install the compiler and libraries from your
   operating system's official repositories. Keep the machine offline once
   everything is downloaded, if you can.
4. **Keep your own record.** Note the commit hash you built and the checksums
   of what you produced, so you can tell later whether anything changed.

Build instructions are in the
[development environment guide](/appendix/setup-dev-env/). This path costs
real time and skill. That is the honest price of not having to trust anyone
else's build.
