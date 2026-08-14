---
title: Contributing to GpgFrontend
description: "How to contribute to GpgFrontend: set up a development environment, build and test the project, and submit changes through GitHub pull requests or email patches."
sidebar:
  order: 4
---

Thank you for wanting to contribute! GpgFrontend is maintained by one person,
so every contribution counts, no matter how small. This guide walks the whole
path: set up a development environment, build and test the project, and send
in your changes, either as a GitHub pull request or as a git patch by email.

You are welcome to use AI tools in your work. Before you do, read the two rules
in the [AI Policy](/appendix/ai-policy/#if-you-contribute): you must understand
every line you send, and you must have built and run it yourself.

## Wiki

An [AI-generated Wiki](https://deepwiki.com/saturneric/GpgFrontend) is built
automatically from the source code. It gives a good overview of the
architecture, the design ideas, and the main components.

Read it before you dive into the code. Knowing the layout of the project first
saves a lot of time. It is mostly accurate, but it is machine-written, so
check anything important against the source itself.

## Technical Requirements

All contributions should follow these rules:

- **C++ Standard:** C++ code must follow the C++17 standard.
- **C Standard:** C code must follow the C99 standard.
- **Rust Standard:** Since v2.2, GpgFrontend includes a Rust component (the
  rPGP engine), located under the `rust/` directory and built into the project
  via [Corrosion](https://github.com/corrosion-rs/corrosion). Rust code must
  build with the Rust 2024 edition (Rust 1.85 or newer) and should be formatted
  with `rustfmt` and pass `clippy` using their default configurations.
- **Compilers:** Your C/C++ code should compile with both GCC (8.0 or newer)
  and Clang (9.0 or newer). MSVC is not supported; on Windows the project is
  built with MinGW inside MSYS2.
- **Build System:** CMake 3.24 or newer is required.
- **Third-Party Libraries:** Be careful about adding new libraries. Any new
  library must be compatible with the GPL 3.0 license, and you must discuss it
  with the maintainer first.
- **Code Formatting:** Use the `.clang-format` and `.clang-tidy` configurations
  in the repository to format and check your code.
- **Unit Testing:** If you add a feature or change behavior, please add unit
  tests to cover it.
- **Documentation:** Update the documentation to match your changes.
- **Code Maintenance and Attribution:** The maintainer may edit your code to
  fit the project better. If you wish, add your name and contact details in a
  code comment on your contribution.

## Set Up Your Environment

The steps below mirror what the continuous integration (CI) pipeline does, so a
local build behaves the same way as the official builds.

### Prerequisites

- **Git:** installed and configured. For GitHub contributions, fork the
  repository first.
- **Compilers:** GCC 8+ or Clang 9+ (on Windows, the MinGW toolchain from
  MSYS2).
- **Rust toolchain:** Rust 1.85 or newer. Install it through
  [rustup](https://rustup.rs/) on Linux and macOS. On Windows with MSYS2, the
  `mingw-w64-x86_64-rust` package from the list below is used instead. The
  build expects `cargo` on your `PATH`.

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

> Note: BKTUS is the main development repository. Changes usually land there
> first for testing, then get merged into the GitHub repository.

After entering the project directory, initialize and update the submodules.
This step is required: the submodules provide gpgme, libassuan, libgpg-error,
Corrosion, the Qt translations, and the modules sub-project. If you skip it,
the build will fail.

```bash
git submodule update --init --recursive
```

### Configure Git Line Endings

This keeps line endings the same on every operating system.

```bash
git config --global core.autocrlf false
git config --global core.eol lf
```

### Install Dependencies

Besides Qt, the build needs libarchive, libsodium, and GoogleTest, plus the
autotools packages used to build gpgme from the bundled submodule.

- **On Ubuntu 22.04 or later:**

```bash
sudo apt-get update
sudo apt-get install -y build-essential git cmake ninja-build \
  autoconf automake gettext texinfo \
  libarchive-dev libsodium-dev libgtest-dev
```

If the `libgtest-dev` package on your distribution is too old, build GoogleTest
from source instead (CI uses v1.15.2):

```bash
git clone --branch v1.15.2 --depth 1 https://github.com/google/googletest.git
cmake -S googletest -B googletest/build -DBUILD_SHARED_LIBS=ON
cmake --build googletest/build && sudo cmake --install googletest/build
```

- **On macOS 15 or later:**

```bash
brew install cmake ninja automake texinfo libarchive googletest libsodium
```

- **For Windows (via MSYS2):** Set up MSYS2 according to [its
  documentation](https://www.msys2.org/), open the MINGW64 shell, and install
  the necessary packages:

```bash
pacman -Syu
pacman -S git msys2-devel base-devel msys2-runtime-devel \
  mingw-w64-x86_64-gcc mingw-w64-x86_64-make mingw-w64-x86_64-cmake \
  mingw-w64-x86_64-ninja mingw-w64-x86_64-qt6-base mingw-w64-x86_64-qt6-tools \
  mingw-w64-x86_64-libarchive mingw-w64-x86_64-libsodium \
  mingw-w64-x86_64-gtest mingw-w64-x86_64-libassuan \
  mingw-w64-x86_64-autotools mingw-w64-x86_64-texinfo \
  mingw-w64-x86_64-rust mingw-w64-x86_64-ccache
```

:::caution[Windows build environment]

On Windows, GpgFrontend can only be built within a Unix-like build environment,
namely MSYS2, MinGW, or Cygwin. A native MSVC/Visual Studio toolchain is not
supported and is rejected at configure time. **MSYS2 is the only environment
that is regularly tested, and it is the recommended choice;** MinGW and Cygwin
may work but are not officially verified.

:::

### Install Qt 6

Any Qt 6.x release works; CI currently builds against Qt 6.10.3. The required
modules are Core, Widgets, PrintSupport, Network, LinguistTools, Xml, and Sql,
plus Concurrent for the modules sub-project.

- On Linux, use the [Qt online installer](https://www.qt.io/download-qt-installer)
  or your package manager (on Ubuntu: `qt6-base-dev qt6-tools-dev` and related
  packages).
- On macOS, use the Qt online installer or `brew install qt`.
- On Windows with MSYS2, Qt is already covered by the `mingw-w64-x86_64-qt6-*`
  packages above.

## Build the Project

Configure and build from the project root:

```bash
cmake -B build -G Ninja -DCMAKE_BUILD_TYPE=Debug \
  -DGPGFRONTEND_LINK_GPGME_INTO_CORE=ON
cmake --build build
```

Notes:

- `GPGFRONTEND_LINK_GPGME_INTO_CORE=ON` builds gpgme, libassuan, and
  libgpg-error from the bundled submodules and links them statically. Every CI
  job uses this option, because GpgFrontend needs gpgme 2.0 or newer and most
  package managers do not ship it yet. This is why the autotools packages
  (autoconf, automake, gettext, texinfo) are in the dependency lists above.
- Adjust the build type (`Release`, `RelWithDebInfo`, etc.) as needed; it
  defaults to `Release` when not set.
- On macOS, CI configures with the Xcode generator (`-G Xcode`) to produce the
  official application bundles. For everyday development builds, Ninja works
  there too. Code signing and notarization are only needed for distribution.

## Run the Tests

The test suite is compiled into the main binary. Run it through the helper
script, which builds the project if needed and parses the test results:

```bash
QT_QPA_PLATFORM=offscreen ./scripts/run_tests.sh
```

Setting `QT_QPA_PLATFORM=offscreen` lets the tests run headless, without a
display server. The script also accepts flags such as `--unit-only`,
`--stress-only`, and `-f FILTER`; see its header comments for details.

## Make Your Changes

The repository uses a single-branch model: development happens on `main`, and
releases are tagged from it. Create a new branch from `main` for your work,
implement your changes while following the technical requirements above, and
run the tests before submitting.

Commit messages follow the [Conventional
Commits](https://www.conventionalcommits.org/) style used throughout the
project history: `type(scope): subject`, for example `fix(ui): correct key
list refresh`.

## Submit Your Contribution

### Via GitHub Pull Request

Push your changes to your fork and open a pull request against the `main`
branch of the original repository. Describe what you changed and why.

### Via Email with Git Patch

Generate a git patch for your commits with `git format-patch` and send it to
the project's contribution email address. Include a description of your
changes and the reasons for them in your email.

## Contact

Stuck, or unsure how to start? Ask. The maintainer's email address is on the
[Contact](/overview/contact/) page, and a question early is better than a lot
of work in the wrong direction.
