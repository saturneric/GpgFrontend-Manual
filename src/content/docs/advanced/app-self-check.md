---
title: "Application Self-Check"
sidebar:
  label: Application Self-Check
---

When Self-Check is enabled, GpgFrontend will verify the digital signatures
(Authenticode signatures) of its core dynamic libraries and components at
startup. This helps ensure that the application’s essential code has not been
altered, replaced, or corrupted—whether accidentally or through malicious
interference.

This mechanism is particularly useful when running a copy of GpgFrontend from a
USB drive or any other removable media that may be more susceptible to
tampering. By validating the digital signatures of critical libraries at
startup, Self-Check helps ensure that all essential dependencies of GpgFrontend
remain intact and trustworthy, even in less secure or portable environments.

:::tip[Note]

The Application Self-Check feature is available starting from version 2.1.9. In
earlier versions, this integrity verification mechanism is not present. This
feature is currently only effective on Windows platforms. On other operating
systems, such as macOS and Linux, runtime self-check is not implemented.

:::

## How It Works

- During the distribution process, application binaries (such as EXE and DLL
  files) are digitally signed using a code signing certificate trusted by the
  Windows operating system, utilizing the Windows Authenticode mechanism.
- At startup, GpgFrontend checks the Windows digital signature of each critical
  dynamic library and main executable, using the operating system’s native
  signature validation (WinVerifyTrust).
- If any library fails validation, a warning is displayed and the issue is
  logged. This can alert users or administrators to possible tampering or
  corruption.

## Enabling Self-Check

Self-Check can be enabled by adding the following line to your ENV.ini
configuration file in the application’s working directory:

```ini
SelfCheck=true
```

With this setting active, GpgFrontend will automatically perform a binary
integrity check at startup.

## Build Requirements

- You must ensure that all Windows binaries (EXE, DLL) are properly code-signed
  using a valid Authenticode certificate during your build or packaging process.
- The self-check feature does not generate or embed any additional cryptographic
  keys; it simply validates the standard Authenticode signatures at runtime.

## Platform Compatibility

### Windows

Self-Check uses Windows Authenticode signatures and WinVerifyTrust, providing
reliable digital signature verification for EXE/DLL files.

### macOS

On macOS, all application binaries are signed using Apple-recognized developer
certificates and go through Apple Notarization. The Gatekeeper security feature
verifies both the signature and the notarization status of your application
bundle upon installation and launch, ensuring integrity and authenticity.

Thus, the application’s authenticity and integrity are protected at the system
level, although the internal self-check feature does not perform additional
runtime verification.

### Linux

For AppImage packages, there is currently no standard built-in self-check or
signature verification mechanism similar to Authenticode or Apple Notarization.
Integrity relies primarily on GPG signature checks during download and
installation, but runtime self-validation is not possible.

Flatpak packages use their own signature and sandboxing mechanisms, which offer
a certain degree of integrity protection within the Flatpak ecosystem.

## Security Note

Application Self-Check adds an important layer of security by helping ensure
that GpgFrontend’s executable code remains authentic and untampered on Windows.
This is particularly valuable for security-sensitive deployments or when running
GpgFrontend on shared or potentially untrusted systems.

The self-check mechanism specifically verifies the integrity of core dynamic
libraries, including GpgFrontend’s own libraries, OpenSSL libraries, and key Qt
modules. It does not verify the main application executable (.exe) itself, as
runtime tampering of the running process is not a practical attack vector for
this component.

For highly sensitive environments, users are strongly advised to use the
operating system’s built-in tools to check the digital signature of the main
executable file before launching the application.

Where possible, administrators should consider configuring Windows security
policies (e.g., AppLocker, WDAC) to only allow the loading of code-signed .exe
and .dll files, ensuring that only trusted binaries can be executed or loaded
into memory.
