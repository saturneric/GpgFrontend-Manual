---
title: "Application Self-Check"
sidebar:
  label: Application Self-Check
---

When Self-Check is enabled, GpgFrontend validates the digital signatures of its
core dynamic libraries and components at startup. This ensures that the
application’s essential code has not been altered, replaced, or
corrupted—whether accidentally or through malicious interference.

:::tip[Note]

The Application Self-Check feature is available starting from version
2.1.9. In earlier versions, this integrity verification mechanism is not
present.

:::

## How It Works

- During the build process, a cryptographic key pair is generated automatically
  for each build.
- The application libraries (DLLs) are signed using the private key, and only
  the corresponding public key is embedded within the application resources.
- After signing, the private key is discarded, making it impossible to forge new
  signatures for tampered binaries.
- At runtime, GpgFrontend verifies each critical library against its signature
  using the embedded public key. If any library fails validation, a warning is
  displayed and the issue is logged.

## Enabling Self-Check

Self-Check can be enabled by adding the following line to your ENV.ini
configuration file in the application’s working directory:

```ini
SelfCheck=true
```

With this setting active, GpgFrontend will automatically perform a binary
integrity check at startup.

## Build Requirements

- The self-check signing process requires the `GPGFRONTEND_SIGN_BUILT_BINARY`
  parameter to be set during the build. This triggers the generation of the
  signing key pair and the signing of all relevant binaries.
- The signing key pair is unique to each build. The private key is securely
  deleted after signing, ensuring that no one—including the developers—can
  generate valid signatures for modified or malicious binaries.

## Platform Compatibility

- Windows: The self-check feature is currently effective only on Windows
  platforms. On Windows, dynamic library files are stable after build and
  signing, allowing signature verification to work reliably.
- macOS and Linux: Due to common post-build modifications such as codesign,
  rpath adjustment, or packaging processes (e.g., AppImage, Flatpak), dynamic
  library files on macOS and Linux often change after build. As a result,
  digital signatures become invalid, and self-check is not currently effective
  on these platforms.

## Security Note

The Application Self-Check adds an important layer of security by helping to
ensure that GpgFrontend’s executable code remains authentic and untampered. It
is particularly recommended for security-sensitive deployments or when running
GpgFrontend on shared or potentially untrusted systems.
