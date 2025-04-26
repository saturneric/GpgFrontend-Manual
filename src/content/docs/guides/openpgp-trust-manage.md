---
title: Best Practices for OpenPGP Trust Chain Management
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

## Signing UIDs and Current Limitations

In GpgFrontend, users can sign the UID (User ID) of another user’s OpenPGP
public key to confirm its authenticity. However, during the initial design
phase, the potential need to synchronize these signatures with key servers was
not fully considered.

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

3.	Practical User Behavior
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

