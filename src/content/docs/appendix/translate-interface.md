---
title: Translate Interface
sidebar:
  label: Translate
---

GpgFrontend is designed to support multiple languages, and community
translation is an important part of making the application accessible to more
users.

Translation work does not require deep technical knowledge of cryptography or
GpgFrontend internals. If you are familiar with both English and another
language, you can help improve the interface, documentation, and user
experience.

## What You Need to Know

Since v2.1.2, GpgFrontend has used Qt's translation system through
[Qt Linguist](https://doc.qt.io/qt-6/qtlinguist-index.html).

Before starting, it is helpful to understand the basic Qt Linguist workflow:

- `.ts` files store source strings and translations.
- Qt Linguist can be used to edit translations with a graphical interface.
- Unfinished or outdated translations can be updated gradually.
- Placeholders such as `%1`, `%2`, `%n`, and HTML-like tags should be preserved.

## About Translation Files

1. Download or clone the source code from
   [GitHub](https://github.com/saturneric/GpgFrontend).
2. Translation files are located in
   [`resource/lfs/locale/ts`](https://github.com/saturneric/GpgFrontend/tree/main/resource/lfs/locale/ts).
3. To add a new language, create a new `.ts` file using the appropriate locale
   code. See this [locale code list](https://saimana.com/list-of-country-locale-code/)
   for reference.
4. To update an existing language, edit the corresponding `.ts` file.

## Translation Lifecycle

Once a translation file is created and added to GpgFrontend, the language will
continue to be supported in later releases unless it is intentionally removed.

However, interface strings change over time. New features, renamed options, and
updated dialogs may introduce untranslated or outdated strings. Before a
release, I may use AI-assisted translation tools to fill missing translations
in languages that I cannot confidently review myself, so that supported
languages remain reasonably complete.

AI-assisted translations are only a fallback. They may be inaccurate, unnatural,
too literal, or inconsistent with established terminology. Human review is still
preferred, especially for security-related terms, OpenPGP concepts, and user
interface wording.

Contributors are welcome to improve existing translations at any time. If you
notice awkward, incorrect, or incomplete translations, you can edit the
corresponding `.ts` file and submit the updated version again.

## Submitting Your Work

You can submit translation updates in either of the following ways:

1. Open a pull request with the changed `.ts` file or files.
2. Send the updated `.ts` file by email to
   [eric@bktus.com](mailto:eric@bktus.com).

Both new languages and corrections to existing translations are welcome.
