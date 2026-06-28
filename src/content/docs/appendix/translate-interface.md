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
2. The application's translation files are located in
   [`resource/lfs/locale/ts`](https://github.com/saturneric/GpgFrontend/tree/main/resource/lfs/locale/ts),
   named `GpgFrontend.<locale>.ts` (for example `GpgFrontend.de_DE.ts`).
   Integrated modules keep their own translations under
   `modules/src/<module>/ts/`, so the application and every module always share
   the same set of languages.
3. To update an existing language, edit the corresponding `.ts` file. This is
   the most common contribution.

### How the `.ts` Files Are Generated

The `.ts` files are no longer hand-created. The set of supported languages is
defined in one place, `GPGFRONTEND_SUPPORTED_LOCALES` in
[`cmake/Translations.cmake`](https://github.com/saturneric/GpgFrontend/blob/main/cmake/Translations.cmake),
and both the application and the modules derive their `.ts` file set from it.

A helper script,
[`scripts/update_translations.sh`](https://github.com/saturneric/GpgFrontend/blob/main/scripts/update_translations.sh),
runs Qt's `lupdate` to create any missing `.ts` files and to sync newly added or
changed `tr()` strings into every locale (marking them as
`type="unfinished"`), for the application and all modules at once. It works
offline and only updates source strings; it does not translate anything.

To **add a brand-new language**, you therefore add its locale code to
`GPGFRONTEND_SUPPORTED_LOCALES` and run `scripts/update_translations.sh`, which
generates the matching `.ts` files everywhere. See this
[locale code list](https://saimana.com/list-of-country-locale-code/) for
reference. If you would rather not touch the build files, you can instead ask
the maintainer to register the new locale for you, then translate the generated
`.ts` file.

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

When opening a pull request, keep the diff focused on your actual translation
changes:

- Edit the text inside the `<translation>` elements (and remove the
  `type="unfinished"` marker once a string is translated). Do not modify source
  string entries or `<location>` line numbers by hand.
- If you ran `scripts/update_translations.sh` locally, only commit the `.ts`
  files for the language(s) you actually worked on. Avoid committing unrelated
  churn from regenerating every locale and module, as that makes the pull
  request harder to review.
- Adding a new language touches `cmake/Translations.cmake` as well; mention this
  in the pull request description so the build change is easy to spot.

Both new languages and corrections to existing translations are welcome.
