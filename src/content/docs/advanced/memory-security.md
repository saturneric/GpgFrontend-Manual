---
title: "Memory Security"
description: Configure GpgFrontend's SecureLevel memory protection settings to balance security, compatibility, and performance when handling sensitive data.
sidebar:
  label: Memory Security
---

## Security Levels and Configurability

Starting from v2.1.9, users can configure the SecureLevel setting by creating or
editing an `ENV.ini` file in the working directory. To enable a specific
SecureLevel, add a line such as `SecureLevel=1` (or another level as needed)
alongside any other configuration options. This flexible approach lets you
adjust memory protection according to your security requirements and system
capabilities.

### SecureLevel 0 (Default)

Standard memory allocation is used at this level. It is recommended for
environments prioritizing compatibility and performance, where handling of
highly sensitive data is limited.

Even at SecureLevel 0, GpgFrontend implements safeguards to reduce the risk of
residual data in memory. When content is read from Qt(such as user input fields
or temporary buffers) the data is promptly transferred into internal buffers, and
the original source is actively cleared and zeroed out. This process helps
ensure that plaintext information does not remain accessible in memory after it
is no longer needed.

### SecureLevel 1 (Standard)

Enhanced memory management techniques are activated at this level, including
zero-initialization of sensitive buffers and stricter tracking of memory usage.
Sensitive data is less likely to persist in memory after it is no longer needed.

All sensitive data, including file contents, (de)compressed plaintext, and
plaintext from text fields, is placed into dedicated secure buffers prior to any
processing or transfer. These buffers are passed directly to the cryptographic
engine (GpgME) and protected by GnuPG mechanisms. Each secure buffer is fully
initialized to zero upon allocation and is explicitly erased upon release,
minimizing the risk of residual sensitive data in memory.

### SecureLevel 2 (Enhanced)

At this highest security level, GpgFrontend utilizes libsodium’s guarded secure
memory (`sodium_malloc`), allocating sensitive data into locked regions
protected from being swapped to disk or accessed by standard memory inspection
tools. All sensitive data is securely erased from memory after use.

For SecureLevel 2, each sensitive allocation is its own libsodium-guarded region
rather than a single pre-allocated heap. Regular UI data is not stored in secure
memory by default; however, data from certain UI elements, such as text field
contents, is transferred to secure memory immediately after being read from Qt
components.
The original Qt objects are then overwritten and actively cleansed, reducing the
risk of residual plaintext in standard memory and avoiding inadvertent multiple
copies.

Before any cryptographic operation (such as encryption or decryption), once data
has been moved to secure memory, the corresponding Qt text field is cleared and
its Undo/Redo history is reset. This prevents sensitive data from being
recovered through standard UI actions. All cryptographic operations are
performed directly from secure memory, with data passed to GpgME and GnuPG
without additional unsecured copies in memory. The same approach applies to file
operations, maximizing protection of sensitive content.

## libsodium Secure Memory

:::note[Migrated to libsodium in v2.2.0]

Up to the 2.1.x series, SecureLevel 2 used OpenSSL’s secure heap
(`OPENSSL_secure_malloc` and related routines) with a fixed-size pre-allocated
heap. Starting with v2.2.0, secure memory was migrated to libsodium’s guarded
allocations (`sodium_malloc`). Descriptions in older documentation that mention
an OpenSSL secure heap or a 32 MB pre-allocated pool refer to the previous
implementation.

:::

At SecureLevel 2, GpgFrontend leverages libsodium’s guarded heap allocations
(`sodium_malloc`) for advanced memory protection. Each guarded allocation is
placed in its own protected region to reduce the risk of sensitive information
(such as private keys, passphrases, and decrypted messages) being exposed via
memory overruns, underruns, or unauthorized access.

Key aspects of libsodium’s secure memory in GpgFrontend include:

- Guarded Allocations: Sensitive data such as private keys, passphrases, and
  decrypted messages are stored in dedicated guarded regions, isolated from the
  standard dynamic memory used by the rest of the application. libsodium places
  guard pages around each region and a canary to detect overflows, helping
  prevent accidental leaks due to programming errors or memory corruption.
- Locked Memory Regions: Where supported by the operating system, guarded memory
  is “locked” (via `sodium_mlock`), meaning it cannot be swapped to disk. This
  reduces the risk of sensitive data being written to swap files or hibernation
  images.
- Strict Allocation and Tracking: Memory is allocated, tracked, and released
  using secure allocation routines (`sodium_malloc()` and `sodium_free()`). If
  guarded secure memory is not available, allocation falls back to standard
  memory, but GpgFrontend always tries to maximize security when possible.
- Automatic Zeroization: Secure memory is zeroed when allocated and wiped when
  released (`sodium_free` clears the region, and `sodium_memzero` is used
  elsewhere). This ensures that no remnants of sensitive data remain after it is
  no longer needed.
- Reduced Attack Surface: By keeping long-term secrets and cryptographic keys in
  protected memory, GpgFrontend reduces the risk of those secrets being
  recovered via memory dumps, pointer overruns, or other memory-related attacks.
- Per-Allocation Guarded Regions: GpgFrontend does not reserve a fixed-size
  secure heap. Each sensitive object is allocated in its own libsodium-guarded
  region on demand and released when no longer needed.

:::caution

The effectiveness of guarded memory protections depends on your operating system
and its memory-locking limits. While not all intermediate or temporary values
are guaranteed to reside in secure memory, GpgFrontend strives to confine all
critical secrets to guarded memory whenever possible.

:::

## GpgFrontend’s Commitment to Memory Security

GpgFrontend is designed with a strong commitment to in-memory protection of
sensitive data. Regardless of the SecureLevel, the application strives to:

- Minimize Lifetime of Sensitive Data: Sensitive data is kept in memory only as
  long as absolutely necessary.
- Avoid Unnecessary Copies: The design ensures that confidential data is not
  inadvertently copied or exposed elsewhere in memory.
- Secure Deletion: Wherever possible, sensitive information is actively
  overwritten (“zeroized”) before memory is released, even in the event of
  errors.
- User Control: Users can choose the SecureLevel that best matches their needs,
  ensuring both flexibility and strong protection for those who require it.

:::tip[Evolution]

These memory security measures are available from version 2.1.9 onward and
continue to evolve. While GpgFrontend aims to cover as many scenarios as
possible, some edge cases may not be fully addressed in the initial versions.
Community feedback is highly encouraged. For example, users are invited to
review the code, report issues, and contribute suggestions to accelerate
improvements in memory security.

:::

### System Requirements and Recommendations

To enable the highest level of protection (SecureLevel 2), please ensure:

- Your operating system allows locking memory pages (for example, a sufficient
  `RLIMIT_MEMLOCK` limit), so libsodium can keep guarded regions out of swap.
- The system can satisfy libsodium guarded allocations, which reserve guard
  pages around each protected region.
- If these conditions are not met, secure memory features may not be fully
  available; GpgFrontend will fall back to the highest supported memory
  protection level.
- For maximum security, it is strongly recommended to use SecureLevel 2 on
  up-to-date systems.
