---
title: Best Practices for OpenPGP Trust Chain Management
sidebar:
  label: Trust Chain Management
---

## Background: Understanding Trust Management

Trust management is a fundamental concept in OpenPGP-based systems. Users must
establish whether they can trust a particular public key to authenticate
communications and verify signatures. Building a secure and efficient trust
model is essential for maintaining communication integrity without relying on
centralized authorities.

In decentralized environments, the responsibility for managing trust rests with
each individual user. This document introduces the key mechanisms behind trust
management in GpgFrontend and outlines current behaviors and design decisions.

## Owner Trust Mechanism

The Owner Trust mechanism in OpenPGP is a way for users to manage the
trustworthiness of public keys in a decentralized manner. After verifying the
fingerprint of a key and ensuring its authenticity, a user can assign an "Owner
Trust" level to the key. This level indicates how much the user trusts the key
owner to sign other people's keys accurately.

Owner Trust is not about whether the key itself is valid; rather, it defines the
user's confidence in the key owner's ability to vouch for others. This
distinction allows users to build personalized and scalable Web of Trust models
without relying heavily on external signatures or centralized authorities.

![](https://image.cdn.bktus.com/i/2025/06/24/38399d86fb330ca20eab85c33c03331797d32679.webp)

Typical trust levels include:

- **Unknown**: No trust decision has been made.
- **None**: The key owner is not trusted to certify other keys.
- **Marginal**: The key owner is partially trusted.
- **Full**: The key owner is completely trusted.
- **Ultimate**: The user owns this key personally (automatically assigned to
  their own keys).

By using Owner Trust, users can securely manage communication without requiring
constant updates from key servers, maintaining both simplicity and control over
their trust network.

### Setting Owner Trust

GpgFrontend makes it easy to manage Owner Trust levels for any key in your
collection directly from the Key Toolbox.

To change the Owner Trust level:

1. Locate the Key: Find the desired public key (or key group) in the Key Toolbox
   table.
2. Open the Context Menu: Right-click on the key entry to display the context
   menu.
3. Set Owner Trust Level: Select the “Set Owner Trust Level” option.

A dialog will appear allowing you to choose the appropriate trust level
(Unknown, None, Marginal, Full, Ultimate).

![](https://image.cdn.bktus.com/i/2025/06/24/4b7624b599a5f310d059843c872cf81e6b089ba4.webp)

## Signing UIDs and Current Limitations

In GpgFrontend, users can sign the UID (User ID) of another user’s OpenPGP
public key to confirm its authenticity. However, during the initial design
phase, the potential need to synchronize these signatures with key servers was
not fully considered.

![](https://image.cdn.bktus.com/i/2025/06/24/d974152f4b2b850d228408b99d37ea487a3cf914.webp)

Currently:

- GpgFrontend does not automatically upload signed UIDs to OpenPGP key servers.
- Whether a signature update is accepted depends entirely on the specific key
  server’s policy.

Reasons for not enforcing automatic synchronization:

Uncontrollable Behavior of Key Servers

- Different servers (e.g., keys.openpgp.org, SKS servers) have varied policies
  regarding third-party signatures.
- Some servers accept them; others require UID validation or reject them
  altogether.

Potential Key Size Inflation

- Each additional signature increases the public key’s size.
- Frequent uploads of third-party signatures would cause key bloat, impacting
  synchronization and performance.

Practical User Behavior

- Most users verify fingerprints manually and rely on Owner Trust.
- Synchronizing all third-party signatures to public servers is often
  unnecessary for typical use cases.

## Special Considerations for Organizational Users

In organizational environments (e.g., large enterprises), simple Owner Trust is
often inadequate. In these cases, a Certificate Authority (CA)-based trust model
is used:

- A trusted internal CA signs the members' keys.
- Members only need to trust the CA's signature rather than validating each
  colleague's key individually.
- This process is similar to the X.509 certificate system and is often
  implemented through gpgsm (S/MIME-based solutions).

Currently, GpgFrontend does not support gpgsm or CA certificate management, but
future development may consider it based on user demand.

## Possible Future Enhancements

- Provide an optional prompt after signing a UID, asking if the user wishes to
  upload the updated key to a key server.
- Clearly warn users about potential issues of key bloat when uploading
  third-party signatures.
- Explore the implementation of organizational trust models such as CA-based
  signature management and certificate presentation.
