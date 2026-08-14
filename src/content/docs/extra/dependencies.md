---
title: Dependencies and Acknowledgements
description: "Libraries and third-party dependencies used by GpgFrontend, with their licenses and acknowledgements, including OpenSSL and libsodium."
sidebar:
  label: Dependencies
  order: 2
---

## Libraries

GpgFrontend incorporates various libraries and binaries, each with their own
license terms. For more information or to obtain the source code, please visit
the respective project homepages.

Note: As of v2.1.9, GpgFrontend no longer uses the QtAES library. All
cryptographic operations (mainly used for the Application itself) are now
performed using OpenSSL, with AES-GCM as the default and only mode.

Note: Starting with v2.2.0, the internal cryptographic helpers have been
migrated again from OpenSSL to **libsodium**. This includes application-level
helpers such as hashing, HMAC, random generation, password hashing, and key
derivation. OpenSSL may also still be used indirectly by Qt or the operating
system for network communication, such as HTTPS/TLS connections. Therefore, this
change does not mean OpenSSL is completely absent from all runtime environments.

### Common

- **Qt (Open Source)**: [https://www.qt.io][qt]
- **GnuPG**: [https://gnupg.org][gnupg]
- **GpgME**: [https://gnupg.org/software/gpgme/index.html][gnupg-gpgme]
- **OpenSSL**: [https://openssl-library.org][openssl-library]
- **libarchive**: [https://www.libarchive.org][libarchive]
- **libsodium**: [https://libsodium.gitbook.io/doc][libsodium]

### Windows

- **MSYS2**: [https://www.msys2.org][msys2]
- **mingw-w64**: [https://www.mingw-w64.org][mingw-w64]

### Linux

- **AppImage**: [https://appimage.org][appimage]
- **libsecret**: [https://gitlab.gnome.org/GNOME/libsecret][gnome-gitlab-libsecret]

### macOS

- **macOS Application Bundles**: [Link][apple-aboutbundles]
- **Xcode Command Line Tools**: [https://developer.apple.com/xcode/][apple-xcode]

## Icons

The icons utilized in this software are sourced from [Alibaba
Iconfont][iconfont]. This vector icon library is free of use,
isn't registered as a trademark, has no copyright issues, and can be
commercially utilized.

[qt]: https://www.qt.io
[gnupg]: https://gnupg.org
[gnupg-gpgme]: https://gnupg.org/software/gpgme/index.html
[openssl-library]: https://openssl-library.org
[libarchive]: https://www.libarchive.org
[libsodium]: https://libsodium.gitbook.io/doc
[msys2]: https://www.msys2.org
[mingw-w64]: https://www.mingw-w64.org
[appimage]: https://appimage.org
[gnome-gitlab-libsecret]: https://gitlab.gnome.org/GNOME/libsecret
[apple-aboutbundles]: https://developer.apple.com/library/archive/documentation/CoreFoundation/Conceptual/CFBundles/AboutBundles/AboutBundles.html
[apple-xcode]: https://developer.apple.com/xcode/
[iconfont]: https://www.iconfont.cn/
