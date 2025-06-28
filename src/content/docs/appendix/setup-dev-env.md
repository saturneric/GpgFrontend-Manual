---
title: Setting Up Your Local Development Environment
sidebar:
  label: Development Environment
---

Creating a local development environment that mirrors the GitHub Actions
workflow is essential for maintaining consistency between local development and
continuous integration (CI) builds. This guide outlines the steps necessary to
configure your local machine in a way that aligns with the CI pipeline, ensuring
that the compilation, build, and testing processes are consistent across
environments. This approach minimizes integration issues and allows for smoother
development workflows.

## Leveraging GitHub Codespaces

To simplify and expedite the setup of a consistent development environment, we
recommend using GitHub Codespaces. Codespaces offers a cloud-hosted,
containerized development environment that matches the configurations used in
your GitHub Actions workflows. This enables you to quickly create an environment
that mirrors your CI pipeline, reducing the overhead of manual environment
configuration.

### Quick Start

[![Open in GitHub
Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/saturneric/GpgFrontend)

With just one click, you can quickly launch a fully configured development
environment in GitHub Codespaces.

### Manual Setup

1. Navigate to your GitHub repository.
2. Click on the Code button and select Open with Codespaces.
3. If you haven't set up a Codespace for this repository, create a new one by
   following the prompts. GitHub will automatically configure a development
   environment based on the repository’s settings, including any configurations
   specified in the .devcontainer folder.
4. The Codespace environment will include all necessary dependencies and tools,
   ensuring consistency with the CI environment.

## Local Environment Setup (without Codespaces)

### Prerequisites

- **Git:** Installed and configured on your system.
- **Compilers:** GCC and Clang for cross-compatibility.

### Clone the Repository

GitHub:

```bash
git clone https://github.com/saturneric/GpgFrontend.git
cd GpgFrontend
```

[BKTUS](https://bktus.com):

```bash
git clone https://git.bktus.com/GpgFrontend/GpgFrontend.git
cd GpgFrontend
```

> Note: The BKTUS repository serves as the main development repository. Many
> updates and commits are first pushed here for validation and testing before
> being merged into the public GitHub repository.

After entering the project directory, be sure to initialize and update
submodules (required for dependencies and third-party libraries):

```bash
git submodule update --init --recursive
```

This step is necessary to fetch all required submodules used by the project. If
you skip this, the build may fail due to missing dependencies.

### Configure Git Line Endings

This step ensures that line endings are consistent across different operating
systems.

```bash
git config --global core.autocrlf false
git config --global core.eol lf
```

### Install Dependencies

- **On Ubuntu 22.04 or later:**

```bash
sudo apt-get update
sudo apt-get install -y build-essential cmake ninja-build libarchive-dev libssl-dev libgpgme-dev
```

- **On macOS 13 or later:**

```bash
brew install cmake openssl@3 ninja libarchive gpgme
brew link --force openssl@3
```

- **For Windows (via MSYS2):** Set up MSYS2 according to [its
  documentation](https://www.msys2.org/) and install the necessary packages:

```bash
pacman -Syu
pacman -S mingw-w64-x86_64-cmake msys2-runtime-devel mingw-w64-x86_64-ninja mingw-w64-x86_64-gnupg mingw-w64-x86_64-libarchive mingw-w64-x86_64-gpgme
```

### Install Qt6

Use the Qt online installer or your package manager to install Qt6 and the
required modules for your project.

## Configure and Build the Project

```bash
$ mkdir build && cd build
$ cmake -G Ninja -DCMAKE_BUILD_TYPE=Debug ..
$ ninja
```

:::caution[Note for v2.1.9]

Starting from version 2.1.9, GpgFrontend requires gpgme 2.0 or newer. However,
most package managers do not provide a sufficiently recent version of gpgme at
this time. It is strongly recommended to enable in-tree building of gpgme by
setting the CMake option: `GPGFRONTEND_LINK_GPGME_INTO_CORE=ON`

:::

### Notes

- Adjust the build type (`Release`, `Debug`, etc.) as needed.
- Replace project-specific commands and dependency installation commands based
  on your project's requirements.
- For macOS, additional steps for code signing and notarization are required only
  for distribution.
