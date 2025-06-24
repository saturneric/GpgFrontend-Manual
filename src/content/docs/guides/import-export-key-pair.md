---
title: Import & Export Key Pair
---

GpgFrontend provides various methods for importing or exporting key pairs, some
of which are outlined below. Please refer to the guide for more information.

## Import Key Pair

To access the import options, navigate to the toolbar and select the desired
method based on your specific requirements. Additionally, you can access
additional options by selecting the action menu in the key management section.

![](https://image.cdn.bktus.com/i/2025/06/24/65a0c1fce233c2fc15afd362b432eb53f684c73d.webp)

In fact, you can find the action menu in the key management section, which
provides access to additional key management options beyond those available in
the toolbar.

![](https://image.cdn.bktus.com/i/2025/06/24/0f9c76d074dd6c364603baea3c565e66c9a8d62d.webp)

### File

This option allows you to select a public or private key file in text format
with any extension to import.

### Editor

You can paste the contents of a key file onto a blank text label page and
GpgFrontend will automatically recognize and import the corresponding key.

### Clipboard

You can copy the contents of a key to your system clipboard and then select this
option to import the corresponding key.

### Key server

This feature enables users to search for and import public keys from a key
server. Users must first enter the email or ID associated with the desired key
and select the appropriate key server. Upon clicking the search button, a list
of public keys that can be imported from the server will be displayed. Users can
choose to import multiple keys together or double-click on a specific table row
to import a corresponding public key. It is important to note that when using
this method, only public keys can be imported.

A detailed description of this part can be found
[Here](/guides/key-server-operations/).

### Dropdown on Key Toolbox

You can drag the key file directly to the key toolbox, and then follow the
prompts of GpgFrontend to import the key.

## Export Key Pair

When deriving the public key of a key pair using the private key, you can derive
either the public key or the private key or both of all the keys present in the
key pair. However, if there are numerous keys in the key pair, the exported data
can be lengthy. Multiple export methods are available, which are similar to the
import process.

In Gpg Frontend, the exported data is encoded in ASCII to ensure compatibility
between computers.

### Export Public Key

You can find this operation in many places. The following will introduce them
one by one.

#### Append Public Key to Editor

To append a public key to the editor in GpgFrontend, right-click on a row in the
key toolbox and select "Append Select Key(s) to Editor" from the pop-up menu.
This will add the public key of the selected key to the end of the text label
page. You can then copy the content to any location as needed.

#### Export on the Key Pair at Operations Tab

To export a public key using the Key Pair at Operations Tab, follow the steps
shown in the screenshot below. This will save the data to a file. Before
proceeding, please make sure to choose a suitable directory to store the file
containing the public key data.

![](https://image.cdn.bktus.com/i/2025/06/24/b9ea951b5c94e8f18cc22e6e415778b97818718f.webp)

### Export multiple public keys at once

To export public key data for multiple key pairs at once, select the desired key
pairs on the key management interface and click on the "Export to Clipboard"
option. This will copy the data to your system clipboard, which you can then
paste into any application or file.

![](https://image.cdn.bktus.com/i/2025/06/24/0ce7919189489923f38e3871e407dad96b788174.webp)

### Export Private Key

Private key options are available in various locations on the detail page that
contains the private key (either the primary key or subkey). From there, you can
select a destination and GpgFrontend will export the corresponding private key
content to that location.

![](https://image.cdn.bktus.com/i/2025/06/24/9dbc57b795542a5f9c2f78875d5be1f9c692ed0d.webp)

Exporting the private key also exports both the public key and private key data,
as the private key data alone is meaningless without the corresponding public
key. Thus, the private key content is typically bundled with the public key
content during export. However, it's essential to note that the private key file
should never be disclosed to others. If leaked, it could compromise the security
of all ciphertexts encrypted by the key.

You can export the private key data in your key pair in two ways.

1. Full export: Include all key data and UID and UID signature in the key pair.
2. Minimal export: Only all key data in the key pair is included.
