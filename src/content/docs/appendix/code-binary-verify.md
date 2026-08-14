---
title: Code & Binary Verify
description: "Verify the authenticity and integrity of GpgFrontend binaries using digital signatures and reproducible, automated GitHub Actions builds."
sidebar:
  order: 2
---

To enhance the security and integrity of software distribution, it’s crucial for
developers and users alike to employ methods for verifying the authenticity and
integrity of code and executable files. The process outlined below aims to
fortify trust in software distribution by leveraging digital signatures and
secure, automated build processes.

## Automated Build Process

GpgFrontend leverages **GitHub Actions** for automated compilations, ensuring
that every binary file version released is directly compiled from the source
code stored in the GitHub repository's main branch. This approach guarantees
that the compilation process is transparent, replicable, and free from manual
interference. The exact commands and environment configurations used during the
compilation are documented within the project's `.github/workflow/release.yml`
file, allowing for full accountability and reproducibility.

## Platform-Specific Binary Signing

From version 1.0.5 onwards, I sign our packages containing the binary
executable files with a GPG key to further ensure security. Each package is
accompanied by a signature file in the release section (with a `.sig` suffix),
allowing users to verify the package before use using standard GPG tools.

All official binary releases are signed with a GPG key, providing a baseline
level of cross-platform integrity and authenticity verification. In addition to
GPG signatures, each platform incorporates its own native code signing and
verification mechanisms, as outlined below:

### Windows

All executable files (.exe, .dll) and installer packages (.msi, .msix) are
signed using a [Certum](https://www.certum.eu/en/certum-by-asseco/) code signing
certificate. The signature is trusted by Windows and can be verified through
standard Windows mechanisms (e.g., file properties or signtool).

![](https://image.cdn.bktus.com/i/2025/06/25/2eb0e5a1ff970b6d97ed38f18b45476c9aad6ee7.webp)

### macOS

All application bundles and binaries are signed with an Apple-approved developer
certificate (codesign). Each official release also passes Apple Notarization,
ensuring the package’s integrity and compliance with Apple’s security standards.
Gatekeeper will automatically verify these protections on first launch.

![](https://image.cdn.bktus.com/i/2025/06/24/cbc3a2ec86515bf5882d1249179e5e06053ada5f.webp)

### Linux

AppImage packages are provided with a GPG signature file (with a .sig suffix) in
the release section. Users are encouraged to verify the authenticity and
integrity of the package using the provided GPG public key before installation
or execution. For Flatpak and other formats, the platform’s own signature and
sandboxing mechanisms offer additional security.

![](https://image.cdn.bktus.com/i/2025/06/24/690c6b534ab54130dfa100f85a8cc299a0223ff5.webp)

## Build Info Verification

Our software includes an "About" interface accessible from the help menu,
providing users with information about the software version, platform, and the
specific GitHub repository branch and commit hash used for compiling the binary.
This feature adds an extra layer of transparency and verification for users.

![](https://image.cdn.bktus.com/i/2025/06/24/fe75a2c041c9e5a7823d0c4d8820bf35501117cd.webp)

## Public Key for Verification

All commits and binary packages are signed with the maintainer's OpenPGP key.
The key and its fingerprint are published at
[bktus.com/openpgp](https://bktus.com/openpgp/). Get the key there, check the
fingerprint, and use it to verify the `.sig` file that comes with each release.

## When the Stakes Are Very High

The checks above are enough for everyday use. But if your safety, your freedom
or your work depends on this software, hold it to a higher standard: do not use
any prebuilt binary at all, not even ours.

Every prebuilt binary asks you to trust the machines and services that built
it. For most people that trust is reasonable. In a truly critical situation, it
is a risk you do not need to take, because you can remove it: build the app
yourself, from source code you have checked.

If you are in that situation, this is the path:

1. **Get the source, not a binary.** Clone the repository and check out an
   official release tag. Verify the tag's GPG signature with the maintainer's
   key from [bktus.com/openpgp](https://bktus.com/openpgp/).
2. **Read before you build.** Review the code yourself, or have someone you
   trust review it. Pay attention to the build scripts too, not only the app
   code.
3. **Build on a machine you trust.** Use a clean, freshly installed system used
   only for this build. Install the compiler and libraries from your operating
   system's official repositories. Keep the machine offline once everything is
   downloaded, if you can.
4. **Keep your own record.** Note the commit hash you built and the checksums
   of what you produced, so you can tell later whether anything changed.

Build instructions are in the
[development environment guide](/appendix/setup-dev-env/). This path costs real
time and skill. That is the honest price of not having to trust anyone else's
build.
