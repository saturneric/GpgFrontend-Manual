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

Since version 1.0.5, every stable release package is signed with the maintainer's
OpenPGP key. Next to each download there is a small `.sig` file. With standard
GPG tools, you can use it to check that the package is genuine and was not
changed by anyone.

Each system also adds its own check on top:

### Windows

All programs and installers are signed with a
[Certum][certum] code signing certificate.
Windows checks this itself. You can also look at it yourself: right-click the
file, open Properties, and look at Digital Signatures.

![][img-1]

### macOS

The app is signed with an Apple developer certificate and passes Apple's
notarization check. macOS verifies both automatically the first time you open
the app. If the app had been changed, macOS would refuse to start it.

![][img-2]

### Linux

The AppImage comes with a `.sig` file, like the other packages. Check it with
GPG before you run the app. Flatpak and other formats bring their own
signature and sandbox systems on top.

![][img-3]

## Checking a Nightly Build

Nightly builds are not signed with the maintainer's key, so they have no
`.sig` files. Each nightly comes with two other files instead:

- `SHA256SUMS.txt` lists every file of the build with its checksum. A checksum
  is a short fingerprint of a file. If the file changes, the checksum changes.
- `SHA256SUMS.txt.sigstore.json` proves that GitHub Actions made
  `SHA256SUMS.txt` for this project.

There is also a `build-records.json` file. It records which build job made
each file.

### Step 1: Check the Checksum

Put your download in the same folder as `SHA256SUMS.txt`. Open a terminal in
that folder and run the command for your system.

On Linux:

```sh
sha256sum -c --ignore-missing SHA256SUMS.txt
```

On macOS:

```sh
shasum -a 256 -c --ignore-missing SHA256SUMS.txt
```

On Windows, run the Linux command in Git Bash or WSL.

Your file should be listed with `OK`. Any other result means the file is not
the one that was built. Do not use it.

### Step 2: Check Who Built It (Optional)

This step needs the [cosign][cosign-install] tool. Put
`SHA256SUMS.txt.sigstore.json` in the same folder and run:

```sh
cosign verify-blob SHA256SUMS.txt --bundle SHA256SUMS.txt.sigstore.json \
  --certificate-identity https://github.com/saturneric/GpgFrontend/.github/workflows/build.yml@refs/heads/main \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com
```

If it prints `Verified OK`, the checksum list was signed by this project's
build on GitHub, from the `main` branch. The signature is also written to
Rekor, a public log that anyone can search. Because Step 1 checked your file
against that list, your file is covered too.

## Check Inside the App

Open **Help** > **About**, then the **Build Information** tab. It shows the
version, the libraries GpgFrontend was built with, and the exact **Git
Branch:** and **Git Commit:** of the source code. That lets you match your
running app to a specific point in the public code history.

To copy these details, for example into a bug report, click **Copy Build
Information**.

![][img-4]

## The Signing Key

All commits and release packages are signed with the maintainer's OpenPGP key.
The key and its fingerprint are published at
[bktus.com/openpgp][bktus-openpgp]. Get the key there, check the
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
   key from [bktus.com/openpgp][bktus-openpgp].
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
[contributing guide](/appendix/contribute/#set-up-your-environment). This path
costs
real time and skill. That is the honest price of not having to trust anyone
else's build.

[certum]: https://www.certum.eu/en/certum-by-asseco/
[img-1]: https://image.cdn.bktus.com/i/2025/06/25/2eb0e5a1ff970b6d97ed38f18b45476c9aad6ee7.webp
[img-2]: https://image.cdn.bktus.com/i/2025/06/24/cbc3a2ec86515bf5882d1249179e5e06053ada5f.webp
[img-3]: https://image.cdn.bktus.com/i/2025/06/24/690c6b534ab54130dfa100f85a8cc299a0223ff5.webp
[img-4]: https://image.cdn.bktus.com/i/2026/10/29/633ad6c3f31555b317e20d990090bb27d3aef7fb.webp
[bktus-openpgp]: https://bktus.com/openpgp/
[cosign-install]: https://docs.sigstore.dev/cosign/system_config/installation/
