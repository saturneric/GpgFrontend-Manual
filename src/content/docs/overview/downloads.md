---
title: Downloads
sidebar:
  order: 3
---

GpgFrontend is available for download through multiple channels. For more
detailed instructions on installation and getting started, please refer to the
[Getting Started Guide](/overview/getting-started/).

[![Packaging status](https://repology.org/badge/vertical-allrepos/gpgfrontend.svg)](https://repology.org/project/gpgfrontend/versions)

## Direct Downloads

Choose from the options below to download GpgFrontend directly for your platform.

### GitHub Releases

Click the badges below to access the latest stable and nightly builds.

[![GitHub Release](https://img.shields.io/github/downloads/saturneric/GpgFrontend/latest/total?style=for-the-badge)](https://github.com/saturneric/GpgFrontend/releases/latest)

[![GitHub Release Nightly](https://img.shields.io/github/downloads/saturneric/GpgFrontend/nightly/total?style=for-the-badge)](https://github.com/saturneric/GpgFrontend/releases/nightly)

### Static Mirror

For privacy-conscious users, a fast and secure direct-download mirror is
available at [ftp.bktus.com](https://ftp.bktus.com/GpgFrontend/). This mirror is
served over HTTPS with no authentication, tracking, rate limits, or
redirections.

### Asset Naming Patterns and Descriptions

Below is a summary table explaining the naming patterns and purposes of each
downloadable asset. You can use the filename patterns to quickly identify and
select the appropriate package for your platform or use case.

| Filename Pattern                  | Description                                                                                 |
| --------------------------------- | ------------------------------------------------------------------------------------------- |
| `***-universal.zip`               | The universal package: contains both Windows Portable and Linux AppImage in one archive.    |
| `***-windows-x86_64-portable.zip` | Fully portable Windows version. No installation needed; just extract and run.               |
| `***-windows-x86_64.msix`         | MSIX installer for Windows (recommended for most Windows users).                            |
| `***-windows-x86_64.msi`          | Classic MSI installer for Windows; suitable for legacy/enterprise environments.             |
| `***-macos-**.dmg`                | macOS disk image; number = minimum required macOS version. Drag to install.                 |
| `***-linux-******.AppImage`       | AppImage for Linux; make it executable and run directly.                                    |
| `*.sig`                           | GPG signature file for verifying the integrity and authenticity of the corresponding asset. |

## Homebrew Cask

Mac users can check the version information through the
badge below or install using the command line.

[![Homebrew Cask](https://img.shields.io/homebrew/cask/v/gpgfrontend?style=for-the-badge)](https://formulae.brew.sh/cask/gpgfrontend)

Install command:

```
brew install --cask gpgfrontend
```

## Flatpak

Linux users can click the image below to navigate to the Flathub page for
installation.

[![Download on Flathub](https://flathub.org/api/badge?locale=en)](https://flathub.org/apps/com.bktus.gpgfrontend)

## Windows

There are several convenient ways to install GpgFrontend on Windows. Choose the
method that best fits your workflow.

### WinGet

Windows users can install GpgFrontend through the Windows Package Manager
(WinGet). Check the version information through the badge below or install
using the command line.

[![WinGet Package Version](https://img.shields.io/winget/v/Saturneric.GpgFrontend?style=for-the-badge)](https://repology.org/project/gpgfrontend/versions)

Install command:

```
winget install Saturneric.GpgFrontend
```

### Microsoft Store

Windows users can also visit the application store page through the Microsoft
Store badge below.

<a href="https://apps.microsoft.com/detail/9nh716mqk2b5">
  <img src="https://get.microsoft.com/images/en-us%20dark.svg" width="200"/>
</a>
