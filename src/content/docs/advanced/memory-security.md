---
title: "Memory Security"
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
residual data in memory. When content is read from Qt—such as user input fields
or temporary buffers—the data is promptly transferred into internal buffers, and
the original source is actively cleared and zeroed out. This process helps
ensure that plaintext information does not remain accessible in memory after it
is no longer needed.

### SecureLevel 1 (Standard)

Enhanced memory management techniques are activated at this level, including
zero-initialization of sensitive buffers and stricter tracking of memory usage.
Sensitive data is less likely to persist in memory after it is no longer needed.

All sensitive data—including file contents, (de)compressed plaintext, and
plaintext from text fields—is placed into dedicated secure buffers prior to any
processing or transfer. These buffers are passed directly to the cryptographic
engine (GpgME) and protected by GnuPG mechanisms. Each secure buffer is fully
initialized to zero upon allocation and is explicitly erased upon release,
minimizing the risk of residual sensitive data in memory.

### SecureLevel 2 (Enhanced):

At this highest security level, GpgFrontend utilizes OpenSSL’s secure memory
feature, allocating sensitive data into locked regions protected from being
swapped to disk or accessed by standard memory inspection tools. All sensitive
data is securely erased from memory after use.

For SecureLevel 2, GpgFrontend pre-allocates a 32 MB secure heap for all
sensitive operations. Regular UI data is not stored in secure memory by default;
however, data from certain UI elements—such as text field contents—is
transferred to secure memory immediately after being read from Qt components.
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

## OpenSSL Secure Memory

At SecureLevel 2, GpgFrontend leverages OpenSSL’s secure heap functionality for
advanced memory protection. The secure heap is a dedicated area of memory
managed by OpenSSL to reduce the risk of sensitive information—such as private
keys, passphrases, and decrypted messages—being exposed via memory overruns,
underruns, or unauthorized access.

Key aspects of OpenSSL’s secure memory in GpgFrontend include:

- Dedicated Secure Heap: Sensitive data such as private keys, passphrases, and
  decrypted messages are stored in a special secure heap, which is isolated from
  the standard dynamic memory used by the rest of the application. This helps
  prevent accidental leaks due to programming errors or memory corruption.
- Locked Memory Regions: Where supported by the operating system, memory in the
  secure heap is “locked,” meaning it cannot be swapped to disk. This reduces
  the risk of sensitive data being written to swap files or hibernation images.
- Strict Allocation and Tracking: Memory is allocated, tracked, and released
  using secure allocation routines (such as OPENSSL_secure_malloc() and
  OPENSSL_secure_free()). If the secure heap is not available, allocation falls
  back to standard memory, but GpgFrontend always tries to maximize security
  when possible.
- Automatic Zeroization: Secure memory is zeroed both when allocated and when
  released (using functions such as OPENSSL_secure_zalloc() and
  OPENSSL_secure_clear_free()). This ensures that no remnants of sensitive data
  remain after it is no longer needed.
- Reduced Attack Surface: By keeping long-term secrets and cryptographic keys in
  protected memory, GpgFrontend reduces the risk of those secrets being
  recovered via memory dumps, pointer overruns, or other memory-related attacks.
- Pre-allocated Secure Heap: GpgFrontend pre-allocates a fixed-size secure heap
  (e.g., 32 MB) at startup, as required by OpenSSL’s secure memory system. This
  secure memory pool is used for all sensitive operations throughout the
  application session.

:::caution

The effectiveness of secure heap protections depends on your operating
system and OpenSSL configuration. While not all intermediate or temporary values
are guaranteed to reside in secure memory, GpgFrontend strives to confine all
critical secrets to the secure heap whenever possible.

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
Community feedback is highly encouraged—users are invited to review the code,
report issues, and contribute suggestions to accelerate improvements in memory
security.

:::

### System Requirements and Recommendations

To enable the highest level of protection (SecureLevel 2), please ensure:

- Your operating system supports OpenSSL 3.0 or later, with secure memory
  features enabled.
- The system is able to allocate at least 32 MB of secure memory for GpgFrontend
  at startup.
- If these conditions are not met, secure memory features may not be fully
  available; GpgFrontend will fall back to the highest supported memory
  protection level.
- For maximum security, it is strongly recommended to use SecureLevel 2 on
  up-to-date systems with a compatible OpenSSL library.
