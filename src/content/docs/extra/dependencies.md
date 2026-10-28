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
derivation. OpenSSL is still used by the email module, for its secure (TLS)
connections to mail servers. Qt may also use it for other secure connections.

### Common

- **Qt (Open Source)**: [https://www.qt.io][qt]
- **GnuPG**: [https://gnupg.org][gnupg]
- **GpgME**: [https://gnupg.org/software/gpgme/index.html][gnupg-gpgme]
- **libgpg-error** and **libassuan**: [https://gnupg.org][gnupg]. Helper
  libraries of GnuPG that GpgME needs.
- **rPGP** (the `pgp` crate, Rust): [https://github.com/rpgp/rpgp][rpgp]. The
  second OpenPGP engine.
- **Corrosion**: [https://github.com/corrosion-rs/corrosion][corrosion]. Builds
  the Rust part of GpgFrontend.
- **OpenSSL**: [https://openssl-library.org][openssl-library]
- **libarchive**: [https://www.libarchive.org][libarchive]
- **libsodium**: [https://libsodium.gitbook.io/doc][libsodium]
- **Lua** 5.4.7 (MIT License): [https://www.lua.org][lua]. Built into
  GpgFrontend to run the scripts that place module menus, buttons and
  settings pages.
- **VMime** (GPL-3.0): [https://www.vmime.org][vmime]. Used by the email
  module to read, build and send email messages.

### Windows

- **MSYS2**: [https://www.msys2.org][msys2]
- **mingw-w64**: [https://www.mingw-w64.org][mingw-w64]
- **Microsoft Edge WebView2**: [https://developer.microsoft.com/microsoft-edge/webview2/][webview2].
  Shows HTML email formatted.

### Linux

- **AppImage**: [https://appimage.org][appimage]
- **libsecret**: [https://gitlab.gnome.org/GNOME/libsecret][gnome-gitlab-libsecret]

### macOS

- **macOS Application Bundles**: [Link][apple-aboutbundles]
- **Xcode Command Line Tools**: [https://developer.apple.com/xcode/][apple-xcode]
- **WebKit**: part of macOS. Shows HTML email formatted.

### Optional

- **Qt WebEngine**: [https://doc.qt.io/qt-6/qtwebengine-index.html][qt-webengine].
  Used only by the optional WebEngine module, which shows HTML email formatted
  on Linux. The official downloads leave it out.

## Fonts

GpgFrontend includes the **JetBrains Mono NL** 2.304 font, from the
[JetBrains Mono][jetbrains-mono] project. It is the default font of the text editor
and the Status Panel. The font is licensed under the SIL Open Font License 1.1
(OFL-1.1), and the font files are included unchanged.

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
[lua]: https://www.lua.org
[vmime]: https://www.vmime.org
[jetbrains-mono]: https://github.com/JetBrains/JetBrainsMono
[rpgp]: https://github.com/rpgp/rpgp
[corrosion]: https://github.com/corrosion-rs/corrosion
[webview2]: https://developer.microsoft.com/microsoft-edge/webview2/
[qt-webengine]: https://doc.qt.io/qt-6/qtwebengine-index.html
