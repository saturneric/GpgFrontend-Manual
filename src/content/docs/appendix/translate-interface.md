---
title: Translate Interface
description: "Help translate GpgFrontend into more languages with Qt Linguist; no cryptography expertise needed, just fluency in English and another language."
sidebar:
  order: 3
  label: Translate
---

GpgFrontend speaks many languages, and the translations come from the
community.

You do not need to know anything about cryptography or the code to help. If
you know English and one other language well, you can translate.

## What You Need to Know

GpgFrontend uses Qt's translation system (since v2.1.2). Translations are
edited with [Qt Linguist][qt-linguist], a graphical tool. The basics:

- `.ts` files store the English source strings and their translations.
- Qt Linguist opens these files and lets you translate string by string.
- You do not have to finish everything at once; partial work is fine.
- Keep placeholders such as `%1`, `%2`, `%n`, and HTML-like tags as they are.

## About Translation Files

1. Download or clone the source code from
   [GitHub][github-gpgfrontend].
2. The application's translation files are located in
   [`resource/lfs/locale/ts`][locale-ts-dir],
   named `GpgFrontend.<locale>.ts` (for example `GpgFrontend.de_DE.ts`).
   Integrated modules keep their own translations under
   `modules/src/<module>/ts/`, so the application and every module always share
   the same set of languages.
3. To update an existing language, edit the corresponding `.ts` file. This is
   the most common contribution.

### How the `.ts` Files Are Generated

The `.ts` files are no longer hand-created. The set of supported languages is
defined in one place, `GPGFRONTEND_SUPPORTED_LOCALES` in
[`cmake/Translations.cmake`][github-translations-cmake],
and both the application and the modules derive their `.ts` file set from it.

A helper script,
[`scripts/update_translations.sh`][github-update-translations-sh],
keeps them in sync. It creates any missing `.ts` files and pulls new or
changed interface strings into every language file, marking them as
`type="unfinished"`. It covers the application and all modules at once, works
offline, and does not translate anything itself.

To **add a brand-new language**, add its locale code to
`GPGFRONTEND_SUPPORTED_LOCALES` and run `scripts/update_translations.sh`,
which generates the matching `.ts` files everywhere. See this
[locale code list][locale-codes] for reference. If you would rather not touch
the build files, ask the maintainer to register the new locale for you, then
translate the generated `.ts` file.

## Translation Lifecycle

Once a language is added, it stays supported in later releases unless it is
removed on purpose.

But the interface keeps changing. New features and renamed options bring new
strings that are not translated yet. Before a release, the maintainer may fill
those gaps with AI translation tools, in languages the maintainer cannot check
personally, so every language stays reasonably complete.

Those AI translations are only a stopgap. They can be clumsy, too literal, or
inconsistent with the usual terms. A human translation is always better,
especially for security terms, OpenPGP concepts, and interface wording.

So if you see an awkward or wrong translation in your language, that is your
invitation: edit the `.ts` file and send in the improved version.

## Submitting Your Work

There are two ways to send in your work:

1. Open a pull request with the changed `.ts` file or files.
2. Send the updated `.ts` file by email to
   [eric@bktus.com][eric].

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

[qt-linguist]: https://doc.qt.io/qt-6/qtlinguist-index.html
[github-gpgfrontend]: https://github.com/saturneric/GpgFrontend
[locale-ts-dir]: https://github.com/saturneric/GpgFrontend/tree/main/resource/lfs/locale/ts
[github-translations-cmake]: https://github.com/saturneric/GpgFrontend/blob/main/cmake/Translations.cmake
[github-update-translations-sh]: https://github.com/saturneric/GpgFrontend/blob/main/scripts/update_translations.sh
[locale-codes]: https://saimana.com/list-of-country-locale-code/
[eric]: mailto:eric@bktus.com
