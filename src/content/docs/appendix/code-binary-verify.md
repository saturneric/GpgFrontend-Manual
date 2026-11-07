---
title: Code & Binary Verify
description: "How to check that your copy of GpgFrontend is genuine and untouched, from signed packages to building it yourself."
sidebar:
  order: 2
---

When you download software, one question matters: is this really the app the
developer made, or did someone change it on the way to you?

For a security tool, that question matters twice. This page shows how
GpgFrontend lets you check, and how deep you can go. To learn how releases
are built, signed and published, see
[How Releases and Updates Work](/appendix/release-updates/#build-and-release-pipeline).

## Which Check Do I Need?

Find the kind of download you have:

| You have                                    | How to check it                                   |
| :------------------------------------------ | :------------------------------------------------ |
| A stable release with a `.sig` file         | [Check a Stable Release](#check-a-stable-release) |
| A test or beta build with a `.minisig` file | [Check a Test Build](#check-a-test-build)         |
| The Windows installer                       | Windows checks it too. See [Windows](#windows).   |
| The macOS app                               | macOS checks it for you. See [macOS](#macos).     |
| Flatpak, an app store or a package manager  | The store or package manager checks it for you.   |

## Check a Stable Release

Since version 1.0.5, every stable release file is signed with the maintainer's
OpenPGP key. Next to each download there is a small `.sig` file. With standard
GPG tools, you can use it to check that the file is genuine and was not
changed by anyone.

### Step 1: Get the Maintainer's Key

1. Download the maintainer's public key from
   [bktus.com/openpgp][bktus-openpgp].
2. Import it into GnuPG. You can also do this in GpgFrontend itself.
3. Check that the key's fingerprint is exactly:

   ```
   12F7E8858CF15BEC9975FF3C5CA3DA246843FD03
   ```

The same fingerprint is listed in the [security policy][security-md] of the
repository, so you can compare the two.

### Step 2: Check the Signature

Put your download and its `.sig` file in the same folder. Open a terminal in
that folder and run this command. Replace `FILE` with the name of your
download:

```sh
gpg --verify FILE.sig FILE
```

GnuPG should say `Good signature`, made by the key with the fingerprint above.
Any other result means the file is not the one that was published. Do not use
it.

## Checks Your System Does for You

Each system also adds its own check on top of the signature.

### Windows

The stable installers are signed with a [Certum][certum] code signing
certificate. Windows checks this itself. You can also look at it yourself:
right-click the file, open Properties, and look at Digital Signatures.

![][img-1]

### macOS

The app is signed with an Apple developer certificate and passes Apple's
notarization check. macOS verifies both automatically the first time you open
the app. If the app had been changed, macOS would refuse to start it.

![][img-2]

### Linux

The AppImage comes with a `.sig` file, like the other packages. Check it with
GPG before you run the app, as shown in
[Check a Stable Release](#check-a-stable-release). Flatpak and other formats
bring their own signature and sandbox systems on top.

![][img-3]

## Check a Test Build

Test builds (nightly builds) and beta versions are not signed with the
maintainer's OpenPGP key, so they have no `.sig` files. Instead, every file
comes with a `.minisig` file. This is a signature made with
[minisign][minisign], a small and simple signing tool.

The test build signing key is:

```
RWSxNasy+OIaiWWGzwNYu223e0UNDwrsb+4S/ttGO8knO/URmtMtDpse
```

The same key is listed in the [security policy][security-md] of the
repository, so you can compare the two.

Get the files from the test build list on the
[Downloads page](/overview/downloads/#test-builds).

### Step 1: Check the Signature

1. Install [minisign][minisign].
2. Put your download and its `.minisig` file in the same folder.
3. Open a terminal in that folder and run this command. Replace `FILE` with
   the name of your download:

   ```sh
   minisign -Vm FILE -P RWSxNasy+OIaiWWGzwNYu223e0UNDwrsb+4S/ttGO8knO/URmtMtDpse
   ```

4. You should see `Signature and comment signature verified`. The line below
   it shows the file name and version that were signed. They must match your
   download.

Any other result means the file is not the one that was published. Do not use
it.

### Step 2: Check the Checksum (Optional)

A checksum is a short fingerprint of a file. If the file changes, the checksum
changes. The file `SHA256SUMS.txt` lists the checksum of every file in the
build.

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

Your file should be listed with `OK`.

### Step 3: Check Who Built It (Optional)

This step shows that GitHub Actions built the files for this project. It needs
the [cosign][cosign-install] tool. Put `SHA256SUMS.txt` and
`SHA256SUMS.txt.sigstore.json` (also linked on the Downloads page) in the same
folder and run:

```sh
cosign verify-blob SHA256SUMS.txt --bundle SHA256SUMS.txt.sigstore.json \
  --certificate-identity https://github.com/saturneric/GpgFrontend/.github/workflows/build.yml@refs/heads/main \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com
```

If it prints `Verified OK`, the checksum list was signed by this project's
build on GitHub, from the `main` branch. The signature is also written to
Rekor, a public log that anyone can search. Because Step 2 checked your file
against that list, your file is covered too.

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
costs real time and skill. That is the honest price of not having to trust
anyone else's build.

[certum]: https://www.certum.eu/en/certum-by-asseco/
[img-1]: https://image.cdn.bktus.com/i/2025/06/25/2eb0e5a1ff970b6d97ed38f18b45476c9aad6ee7.webp
[img-2]: https://image.cdn.bktus.com/i/2025/06/24/cbc3a2ec86515bf5882d1249179e5e06053ada5f.webp
[img-3]: https://image.cdn.bktus.com/i/2025/06/24/690c6b534ab54130dfa100f85a8cc299a0223ff5.webp
[bktus-openpgp]: https://bktus.com/openpgp/
[cosign-install]: https://docs.sigstore.dev/cosign/system_config/installation/
[minisign]: https://jedisct1.github.io/minisign/
[security-md]: https://github.com/saturneric/GpgFrontend/blob/main/SECURITY.md
