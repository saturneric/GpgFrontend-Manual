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

## Find Your Way Around

The source code is well commented. Comments explain why things are done the
way they are, so reading the code around your change is the best way to learn
the project. An AI coding assistant pointed at the repository can also help
you explore it and find the right place to start.

If you want to write a module rather than change the application, start with
[Write Modules](/advanced/write-modules/).

## Technical Requirements

All contributions should follow these rules:

- **C++ Standard:** C++ code must follow the C++17 standard.
- **C Standard:** C code must follow the C11 standard.
- **Rust Standard:** Since v2.2, GpgFrontend includes a Rust component (the
  rPGP engine), located under the `rust/` directory and built into the project
  via [Corrosion][github-corrosion]. Rust code must
  build with the Rust 2024 edition and Rust 1.88 or newer (the `pgp` 0.21 crate
  needs 1.88). It should be formatted with `rustfmt` and pass `clippy` using
  their default configurations.
- **Compilers:** Your C/C++ code should compile with both GCC (8.0 or newer)
  and Clang (9.0 or newer). MSVC is not supported; on Windows the project is
  built with MinGW inside MSYS2.
- **Build System:** CMake 3.24 or newer is required.
- **Third-Party Libraries:** Be careful about adding new libraries. Any new
  library must be compatible with the GPL 3.0 license, and you must discuss it
  with the maintainer first.
- **Code Formatting:** Use the `.clang-format` and `.clang-tidy` configurations
  in the repository to format and check your code.
- **Copyright Headers:** New source files need the project's copyright header.
  `scripts/copyright_checking.py` checks for it, and `--fix` adds it to files
  that have none (see [Python Helper Scripts](#python-helper-scripts)).
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
- **Rust toolchain:** Rust 1.88 or newer. Install it through
  [rustup][rustup] on Linux and macOS. On Windows with MSYS2, the
  `mingw-w64-x86_64-rust` package from the list below is used instead. The
  build expects `cargo` on your `PATH`.

### Clone the Repository

GitHub:

```bash
git clone https://github.com/saturneric/GpgFrontend.git
cd GpgFrontend
```

[BKTUS][bktus]:

```bash
git clone https://git.bktus.com/GpgFrontend/GpgFrontend.git
cd GpgFrontend
```

> Note: BKTUS is the main development repository. Changes usually land there
> first for testing, then get merged into the GitHub repository.

After entering the project directory, initialize and update the submodules.
This step is required: the submodules provide gpgme, libassuan, libgpg-error,
Corrosion, Lua (`third_party/lua`, used by the module UI scripts), the Qt
translations, and the modules sub-project. If you skip it, the build will
fail.

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

Besides Qt, the build needs libarchive, libsodium, OpenSSL, and GoogleTest,
plus the autotools packages used to build gpgme from the bundled submodule.
OpenSSL is used by the email module for TLS connections.

- **On Ubuntu 22.04 or later:**

```bash
sudo apt-get update
sudo apt-get install -y build-essential git cmake ninja-build \
  autoconf automake gettext texinfo \
  libarchive-dev libssl-dev libsodium-dev libgtest-dev
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
brew install cmake ninja automake texinfo libarchive googletest libsodium openssl@3
```

Homebrew's `openssl@3` is not on the default search path, and the LibreSSL
headers that come with macOS do not work. Point CMake at it when you
configure:

```bash
-DOPENSSL_ROOT_DIR="$(brew --prefix openssl@3)"
```

- **For Windows (via MSYS2):** Set up MSYS2 according to [its
  documentation][msys2], open the MINGW64 shell, and install
  the necessary packages:

```bash
pacman -Syu
pacman -S git msys2-devel base-devel msys2-runtime-devel \
  mingw-w64-x86_64-gcc mingw-w64-x86_64-make mingw-w64-x86_64-cmake \
  mingw-w64-x86_64-ninja mingw-w64-x86_64-qt6-base mingw-w64-x86_64-qt6-tools \
  mingw-w64-x86_64-libarchive mingw-w64-x86_64-libsodium \
  mingw-w64-x86_64-gtest mingw-w64-x86_64-libassuan \
  mingw-w64-x86_64-autotools mingw-w64-x86_64-texinfo \
  mingw-w64-x86_64-rust mingw-w64-x86_64-ccache mingw-w64-x86_64-openssl
```

:::caution[Windows build environment]

On Windows, GpgFrontend can only be built within a Unix-like build environment,
namely MSYS2, MinGW, or Cygwin. A native MSVC/Visual Studio toolchain is not
supported and is rejected at configure time. **MSYS2 is the only environment
that is regularly tested, and it is the recommended choice;** MinGW and Cygwin
may work but are not officially verified.

:::

### Install Qt 6

Qt 6.5 or later is required; CI currently builds against Qt 6.11.3 (set in
`.github/actions/install-qt6/action.yml`). The required
modules are Core, Widgets, PrintSupport, Network, LinguistTools, Xml, and Sql,
plus Concurrent for the modules sub-project.

- On Linux, use the [Qt online installer][qt-installer]
  or your package manager (on Ubuntu: `qt6-base-dev qt6-tools-dev` and related
  packages). The packaged Qt of Ubuntu 22.04 (6.2) and 24.04 (6.4) is too
  old; use the online installer there, or a newer distribution such as
  Debian 13.
- On macOS, use the Qt online installer or `brew install qt`.
- On Windows with MSYS2, Qt is already covered by the `mingw-w64-x86_64-qt6-*`
  packages above.

:::note[Qt5]

The `main` branch builds with Qt 6 only. Qt5 builds are made only from the
`release/2.1` branch, for the v2.1.x line.

:::

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
  job uses this option, because GpgFrontend is meant to run on gpgme 2.0 or
  newer and most package managers do not ship it yet. This is why the autotools
  packages (autoconf, automake, gettext, texinfo) are in the dependency lists
  above.
- Adjust the build type (`Release`, `RelWithDebInfo`, etc.) as needed; it
  defaults to `Release` when not set.
- On macOS, CI configures with the Xcode generator (`-G Xcode`) to produce the
  official application bundles. For everyday development builds, Ninja works
  there too. Code signing and notarization are only needed for distribution.
  Remember `-DOPENSSL_ROOT_DIR` (see above).
- The unit tests are off by default. Add `-DGPGFRONTEND_BUILD_TESTS=ON` to
  build them (this needs GoogleTest), and `-DGPGFRONTEND_MODULES_BUILD_TESTS=ON`
  to also build the modules' own unit tests.
- `GPGFRONTEND_BUILD_APP_IMAGE` is gone. The AppImage is now made from the
  tree that `cmake --install` produces.

### Module Binding Options

Two cache options decide how integrated modules are tied to their native
libraries. You only need them when you package a release:

- `GPGFRONTEND_INTEGRATED_MODULE_NATIVE_BINDING`: `OFF` (the default, right
  for a development tree and a normal local install) or `REQUIRED`. Official
  Windows and AppImage releases set `REQUIRED`.
- `GPGFRONTEND_INTEGRATED_MODULE_BINDING_ALGORITHM`: `AUTO` (the default),
  `FILE_SHA256` or `PE_AUTHENTICODE_SHA256`. Naming one is a check: configure
  fails if it does not match what the platform needs.

Modules you build outside the tree always need a binding. See
[Write Modules](/advanced/write-modules/).

## Run the Tests

The test suite is compiled into the main binary, but only when you configured
with `-DGPGFRONTEND_BUILD_TESTS=ON`. Without it, the script stops and tells
you to reconfigure. Run the tests through the helper script, which builds the
project if needed and parses the test results:

```bash
QT_QPA_PLATFORM=offscreen ./scripts/run_tests.sh
```

Setting `QT_QPA_PLATFORM=offscreen` lets the tests run headless, without a
display server. By default the script runs these phases, one after another:
the Rust tests (`cargo test`), the modules' tests, the C++ unit tests, the
stress tests, the key generation coverage sweep, and the slow Rust tests. Run
`./scripts/run_tests.sh --help` for the full list. The most useful options:

| Option                 | What it does                                                                    |
| ---------------------- | ------------------------------------------------------------------------------- |
| `--unit-only`          | Run only the unit tests.                                                        |
| `--stress-only`        | Run only the stress tests.                                                      |
| `--coverage-only`      | Run only the sweep that makes a key with every algorithm on offer.              |
| `--rust-only`          | Run only the Rust tests.                                                        |
| `--no-rust`            | Skip the Rust tests.                                                            |
| `-b`, `--build`        | Build the app before running the tests.                                         |
| `-l LEVEL`             | Set the app's log level: `debug`, `info`, `warn` (default) or `error`.          |
| `-f PATTERN`           | Run a single GoogleTest filter and nothing else.                                |
| `--modules-only`       | Run only the modules' own test binaries.                                        |
| `--require-modules`    | Fail, instead of skip, when module test binaries are missing. Use it in CI.     |
| `--large-file-only`    | Run the large-file tests. They need `gpg`, `sq` and about 15 GiB of free space. |
| `-p N`, `--parallel N` | Split the unit tests across N processes (`auto` picks a number for you).        |
| `--fresh-homes`        | With `-p`, wipe the per-process home folders first.                             |
| `--shard-timeout S`    | With `-p`, stop a process after S seconds (default 900).                        |
| `--asan`               | Run against a separate AddressSanitizer and UBSan build in `build-asan/`.       |
| `--asan-gui`           | Build that sanitizer tree if needed and start the real app from it.             |
| `--reconfigure`        | With `--asan` or `--asan-gui`, configure the sanitizer build from scratch.      |

The module tests only exist if you configured with
`-DGPGFRONTEND_MODULES_BUILD_TESTS=ON`.

The old separate ASan scripts are gone. Use `--asan` and `--asan-gui` instead.

:::caution[`--asan-gui` uses your real data]

`--asan-gui` starts the app with your real GpgFrontend settings and keys, so
you can repeat your own steps. Keep that in mind before you try anything risky.

:::

## Python Helper Scripts

The Python scripts in `scripts/` need Python 3.14 or newer. Their dependencies
are listed in `scripts/pyproject.toml` and locked in `scripts/uv.lock`, and
they are managed with [uv][uv]. There is no `requirements.txt` any more.

```bash
uv sync --project scripts
uv run --project scripts python scripts/copyright_checking.py
```

`copyright_checking.py` only checks by default and never writes. Add `--fix`
to add the header to files that have none.

The old `.devcontainer/` setup was removed. Set up your environment with the
steps above instead.

## Manual Screenshots

The screenshots in this manual are made automatically, not by hand.
GpgFrontend has a hidden screenshot mode that opens each window in a fixed
state, with demo keys, a fixed clock and the same fonts every time. The
scripts in the Manual repository's `scripts/screenshots/` folder start that
mode, take each picture, upload it and put the new link into the page. Its
`README.md` explains how to run them.

- **Windows only:** every screenshot is taken on Windows 11, in English, with
  the light theme. The manual shows only these, so there is one set to keep up
  to date. macOS and Linux look a little different, but the windows and
  buttons are the same.
- **Build option:** the scripts need a binary configured with
  `-DGPGFRONTEND_BUILD_SCREENSHOT_MODE=ON` and
  `-DGPGFRONTEND_BUILD_TESTS=ON`. It cannot be combined with
  `GPGFRONTEND_BUILD_MODE=release`.
- **Where the scenes live:** each window state is a scenario in
  `src/screenshot/`, and the demo data is in `resource/screenshot/`.
- **Changes are noticed:** each screenshot lists the source files it depends
  on. When you change one of them, the next run marks that screenshot as out
  of date and takes it again.

## Make Your Changes

Development happens on `main`, and releases are tagged from it. The
`release/2.1` branch keeps the older v2.1.x line (including its Qt5 builds)
alive. Create a new branch from `main` for your work,
implement your changes while following the technical requirements above, and
run the tests before submitting.

Commit messages follow the [Conventional
Commits][conventionalcommits] style used throughout the
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

[github-corrosion]: https://github.com/corrosion-rs/corrosion
[rustup]: https://rustup.rs/
[bktus]: https://bktus.com
[msys2]: https://www.msys2.org/
[qt-installer]: https://www.qt.io/download-qt-installer
[conventionalcommits]: https://www.conventionalcommits.org/
[uv]: https://docs.astral.sh/uv/
