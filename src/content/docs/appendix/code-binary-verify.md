---
title: Code & Binary Verify
---

To enhance the security and integrity of software distribution, it's crucial for
developers and users alike to employ methods for verifying the authenticity and
integrity of code and executable files. The process outlined below aims to
fortify trust in software distribution by leveraging digital signatures and
secure, automated build processes.

### Automated Build Process

Our software leverages **GitHub Actions** for automated compilations, ensuring
that every binary file version released is directly compiled from the source
code stored in the GitHub repository's main branch. This approach guarantees
that the compilation process is transparent, replicable, and free from manual
interference. The exact commands and environment configurations used during the
compilation are documented within the project's `.github/workflow/release.yml`
file, allowing for full accountability and reproducibility.

### Third-Party Library Assurance

To uphold our commitment to security, we do not include GnuPG in our major
releases and strictly avoid insecure or proprietary third-party libraries.
Instead, we only utilize third-party libraries that are open-source and have
been compiled from publicly accessible code repositories. This practice ensures
that our software remains secure and trustworthy.

### Code Verification

We encourage users to review our code to ensure its integrity and security. The
code for all releases is available on our GitHub repository. For any inquiries
or concerns, please feel free to contact us directly. Most new git commits are
signed with a designated key, which is also used for Git operations: `Saturneric
<eric@bktus.com>`. This commitment to transparency allows users to verify the
authenticity of our code easily.

#### Key Fingerprint

```
E3379489C39B7270E70E2E303AAF1C64137CEE57
```

### Binary File Verification

From version 1.0.5 onwards, we sign our packages containing the binary
executable files with a GPG key to further ensure security. Each package is
accompanied by a signature file in the release section (with a `.sig` suffix),
allowing users to verify the package before use using standard GPG tools.

#### About Interface Verification

Our software includes an "About" interface accessible from the help menu,
providing users with information about the software version, platform, and the
specific GitHub repository branch and commit hash used for compiling the binary.
This feature adds an extra layer of transparency and verification for users.

### Public Key for Verification

Below is the public key used for signing the commits and binary files, which can
be used to verify the authenticity of our releases:

#### Key Fingerprint

```
12F7E8858CF15BEC9975FF3C5CA3DA246843FD03
```

#### Public Key (OpenPGP)

```
-----BEGIN PGP PUBLIC KEY BLOCK-----

mDMEZsEF1xYJKwYBBAHaRw8BAQdAPZ3dA2od9HFaiaJRr1TEEeRMfAcrBp8oqQPa
R16Icva0OHNhdHVybmVyaWMoZm9yIGNvZGUgb3IgYmluYXJ5IHNpZ24gb25seSk8
ZXJpY0Bia3R1cy5jb20+iJkEExYKAEEWIQQS9+iFjPFb7Jl1/zxco9okaEP9AwUC
ZsEF1wIbIwUJA8JmbgULCQgHAgIiAgYVCgkICwIEFgIDAQIeBwIXgAAKCRBco9ok
aEP9A3TTAQC/H61IVj6LiSQ0dvodo5VFb2jTJa8XVfb2NT3yc/+JDwD+KTm+nV73
dbaEG0FOTKu+n4rVhBpTes93Bn2GcRSbQwA=
=fWZe
-----END PGP PUBLIC KEY BLOCK-----
```

This comprehensive approach to security, including automated builds, careful
selection of third-party libraries, and transparent verification methods,
ensures that users can trust the software they are using while also providing
the tools needed to verify that trust independently.
