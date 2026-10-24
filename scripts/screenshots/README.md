# Manual screenshots

These scripts make the manual's screenshots from the GpgFrontend screenshot
mode. They render each image, post-process it, compare it with the last one,
upload it to the image CDN and rewrite the `[img-N]: url` definition in the
page. Everything runs locally. Nothing is uploaded unless you pass `--upload`.

The scripts never run git in this repository. They only read the GpgFrontend
repository, with `rev-parse`, `cat-file`, `merge-base`, `diff` and `status`.

## Setup

Windows (PowerShell):

```powershell
cd scripts\screenshots
py -3 -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```

Linux:

```bash
cd scripts/screenshots
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

You also need `git` on PATH. On Linux you need `xvfb-run` and `fc-match`.
`oxipng` is optional. When it is on PATH it is used and its version is part of
`inputs_hash`; otherwise `none` is recorded.

You need a GpgFrontend binary built with `GPGFRONTEND_BUILD_SCREENSHOT_MODE=ON`.
Pass it with `--binary`, or set `GF_SCREENSHOT_BINARY`.

## Files

| File                                                                             | Purpose                                                       |
| -------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| `screenshots.yaml`                                                               | the manifest: defaults, global sources, entries               |
| `screenshots.lock.json`                                                          | committed record per entry: url, hashes, commit, env          |
| `.screenshots-cache/`                                                            | ignored: previews, baselines, transactions, `last-run.json`   |
| `check.py`                                                                       | status report and inventory                                   |
| `run.py`                                                                         | select, render, post-process, diff, upload, apply, recover    |
| `render.py`                                                                      | runs the binary in a throwaway environment (also a debug CLI) |
| `postprocess.py`                                                                 | frame, shadow, padding, highlights, PNG and lossless WebP     |
| `diff.py`                                                                        | compares with the local baseline                              |
| `upload.py`                                                                      | EasyImages upload                                             |
| `txn.py`                                                                         | the durable upload/apply transaction                          |
| `apply.py`                                                                       | doc definition and lock writes                                |
| `manifest.py`, `docrefs.py`, `envhash.py`, `fonts.py`, `gitutil.py`, `common.py` | shared pieces                                                 |

## Manifest

```yaml
defaults:
  platform: windows11 # the only reference platform
  locale: en_US
  theme: light # light | dark
  size: 1280x960 # logical size, or "auto" for a dialog's natural size
  fonts: ["Noto Sans", "Noto Sans CJK SC"]
  clock: "2026-01-15T10:00:00Z"
  timeout_ms: 30000
  frame: { radius: 8, shadow: 12, padding: 24 } # logical px, scaled by DPR 2
  diff: { tolerance: 16, threshold: 0.001 }
  preview_platforms: [linux-xvfb]
global_sources: [src/screenshot/, resource/screenshot/, scripts/screenshot/]
entries:
  - id: main-window
    doc: src/content/docs/guides/understand-interface.mdx
    ref: img-1
    scenario: main-window
    sources: [src/ui/main_window/]
    highlight: InfoBoardWidget # or {name: X, style: box|arrow}, or a list
    crop: ownerBox # optional: cut the image down to this named widget
  - id: drag-to-applications
    doc: src/content/docs/overview/getting-started.mdx
    ref: img-1
    status: manual-only # or animated; never rendered
```

`sources` and `global_sources` are paths in the GpgFrontend repository. Any
entry key can override a default.

## check.py

```
python check.py --gpgfrontend ../../../GpgFrontend [--binary <exe>] [--inventory] [--json]
```

| Status              | Meaning                                                                            |
| ------------------- | ---------------------------------------------------------------------------------- |
| `missing`           | the ref has no definition, an empty or `TODO` URL, or the entry has no lock record |
| `unmanaged`         | an image ref (reference, inline or `<img>`) that is not in the manifest            |
| `orphan`            | a manifest entry whose ref is no longer on the page                                |
| `unknown-baseline`  | the lock commit is not in the repository, or not an ancestor of HEAD               |
| `outdated`          | the entry's sources or the global sources changed since the lock commit            |
| `inputs-changed`    | settings, pipeline scripts, requirements or the optimizer changed                  |
| `env-changed`       | the probed environment hash differs from the lock                                  |
| `env-unchecked`     | no binary, so the environment was not probed (or the probe failed; see details)    |
| `dirty-sources`     | uncommitted changes in the relevant sources                                        |
| `platform-mismatch` | the probed platform is not the entry's platform                                    |
| `ok`                | none of the above                                                                  |

Without a binary, every entry is `env-unchecked` and never `ok`. Each distinct
(locale, theme, fonts, clock, size) is probed once per run.

`--inventory` adds the observed counts: references, definitions, unique URLs
and formats by URL extension, per page and in total, plus every ref. The format
comes from the URL only; nothing is downloaded. With `--json --inventory` the
output is `{"entries": [...], "inventory": {...}}`; with `--json` alone it is the
entries array.

## run.py

```
python run.py --gpgfrontend <repo> --binary <exe> [--only id,...] [--force]
              [--accept-baseline id,...] [--force-replace id,...]
              [--allow-dirty] [--apply | --upload] [--repeat N]
              [--work-root DIR] [--keep-work]
python run.py --recover [--resolve TXN_ID (--url URL | --retry-upload)]
```

Selection:

1. Candidates are every renderable entry, or exactly `--only`. An unknown id,
   or a `manual-only`/`animated` id, is a usage error.
2. Candidates that are `missing`, `unknown-baseline`, `outdated`,
   `inputs-changed` or `env-changed` are selected. `--force` selects them all.
3. `--accept-baseline` only applies to a selected id whose baseline is
   unavailable. `--force-replace` replaces a selected id whatever the diff says.
   Naming an unselected id, or one id in both lists, is a usage error.

Writes: the default is a dry run (previews, cache, `last-run.json`). `--apply`
writes the lock, docs and cache without network. `--upload` implies `--apply`
and allows the upload. A `replace` is only carried out with `--upload`;
otherwise it is reported as `would-replace`.

Dirty sources: without `--allow-dirty` a dirty entry is `refused-dirty` and not
rendered. With it, the entry is a preview only. An entry rendered on a
non-reference platform is always `preview-only-platform`. Preview-only entries
are never uploaded, applied or advanced in the lock.

Binary freshness is a warning, never a block: the binary is older than a
relevant source file, or `BUILD-INFO.json` next to the binary names a commit
other than HEAD.

Summary statuses: `updated`, `unchanged`, `lock-advanced`,
`unchanged-lock-not-advanced`, `doc-restored`, `would-restore-doc`,
`would-replace`, `baseline-unavailable`,
`refused-dirty`, `preview-only-dirty`, `preview-only-platform`,
`failed:<reason>`, `conflict`, `upload-unknown`, `artifact-corrupt`.

An entry whose link was emptied or set to `TODO` while its image is unchanged
gets the URL from the lock written back under `--apply` (`doc-restored`); no
upload is needed. A dry run reports `would-restore-doc`.

Exit codes: 0 when every entry is `updated`, `unchanged`, `lock-advanced`,
`unchanged-lock-not-advanced`, `doc-restored`, `would-restore-doc` or
`would-replace` (and preview-only entries in a dry run). 1 when any entry is refused, failed or `baseline-unavailable`, or is
preview-only under `--apply`/`--upload`. 2 for usage errors. 3 when a
`conflict`, `upload-unknown` or `artifact-corrupt` is pending.

Previews are in `.screenshots-cache/preview/<id>.{png,webp,json}`.

### CDN credentials

`--upload` reads `GF_MANUAL_CDN_API` (an https URL) and `GF_MANUAL_CDN_TOKEN`.
The token is never written anywhere. The response's `del` link is kept only in
the ignored transaction cache, never in the lock, the docs or `last-run.json`.
Nothing on the CDN is deleted automatically. When a run replaces an image that
an earlier run uploaded, or hits a conflict, the summary prints the `del` link
so you can remove the old upload in the admin panel.

## Transactions and the failure window

Each replacement is one transaction in `.screenshots-cache/txn/<txn_id>/`. Its
state moves `prepared`, `uploading`, `uploaded`, `doc-applied`,
`lock-applied`, `committed`, and is saved to disk before each step.

`run.py --recover` finishes interrupted transactions without rendering:

- `prepared` becomes `abandoned`. Nothing left the machine.
- `uploaded`, `doc-applied` and `lock-applied` continue from where they stopped.
- `uploading` becomes `upload-unknown` and waits for you.
- Changed artifacts become `artifact-corrupt`. Nothing is applied from them.
- A doc or lock changed by someone else becomes `conflict`. Newer data is never
  overwritten.

**The failure window.** If the process dies, or the connection drops, after
the server stored the upload but before `uploaded` was saved, the local side
cannot know whether the upload happened. EasyImages has no idempotency key and
no lookup by hash, so this cannot be made duplicate-free. Such a transaction is
`upload-unknown` and is never retried on its own. Decide with:

- `run.py --recover --resolve <txn_id> --url <url>` if you found the image in the
  EasyImages admin. The `del` link stays unknown.
- `run.py --recover --resolve <txn_id> --retry-upload` to upload the same file
  again. This may leave a duplicate on the CDN, which is harmless and can be
  deleted in the admin panel.

While an entry has an unfinished transaction, a normal `--upload` run does not
upload it again.

## Render environment

Each render runs `<exe> --temp-profile --screenshot <scenario> ...` in a
throwaway directory, `<work root>/run`, emptied before every render:

- Windows: `LOCALAPPDATA`, `APPDATA`, `TEMP`/`TMP` and `USERPROFILE` point into
  it. It runs in your interactive desktop session. The default work root is
  `%SystemDrive%\gf-shot`, not your `%TEMP%`: the temporary profile lives under
  `TEMP`, the Key Databases settings page shows that path, and a per-user temp
  folder would put your account name into the manual.
- Linux: `HOME`, `XDG_*` and `TMPDIR` point into it, under
  `xvfb-run -s "-screen 0 3200x2000x24"`. The default work root is
  `/tmp/gf-shot-<uid>`. Keep `--work-root` short: gpg-agent's socket lives
  deep inside it and Unix sockets are limited to 108 bytes.

The directory name and the temporary profile's own name are fixed, so the
paths the application shows are the same on every run. On Linux the
temporary profile itself is made in `/dev/shm/gf-shot-<uid>`
(`GF_PROFILE_PACKAGE_STORAGE_DIR`), which is emptied before every render too;
the application refuses to start on a session a crash left behind
(`stale-session`) rather than render from its old settings. That also means one
pipeline at a time per work root: two runs sharing one would collide.

`GNUPGHOME`, `QT_QPA_PLATFORM` and the Qt scaling variables are removed from
the inherited environment. After each run, the per-user app data
(`BKTUS/GpgFrontend*`) is checked for new files; any new file fails the entry.
A real GpgFrontend running at the same time could cause a false alarm.

The final `env_hash` combines the binary's `env_hash_core`, which Python
recomputes and must match, with the platform tag and the sha256 of each font
file.

### Font detection limit

Fonts are found through the `...\Windows NT\CurrentVersion\Fonts` registry keys
(HKLM and HKCU) on Windows, and `fc-match` on Linux. The hashed files are those
of every listed family plus the system UI font. Qt does not say which file it
used for each glyph, so a fallback to a font outside that list cannot be seen.
The binary's gate requires every listed family to resolve, which keeps that
risk small.

## Windows 11 checklist (reference renders)

1. Dispatch `build.yml` with `screenshot: true`, then download the
   `screenshot-windows-2022-portable` artifact. Extract the portable zip in
   the same folder as its `BUILD-INFO.json`, so the freshness check finds the
   commit. CI only builds this binary and checks nothing: the steps below,
   on this machine, are the first time it runs.
2. Install Noto Sans and Noto Sans CJK SC if they are not installed.
3. Run a dry run, in light and dark (set `theme` in the manifest, or add
   entries):

   ```powershell
   .venv\Scripts\python run.py --gpgfrontend <GpgFrontend repo> --binary <path>\GpgFrontend.exe `
       --only main-window,key-generate-dialog,text-decrypt-verify-result,main-window-menu-popup --repeat 2
   ```

   Any gate failure is reported by name.

4. Review the previews in `.screenshots-cache\preview\`.
5. If anything fails, send `.screenshots-cache\last-run.json` and the env
   records in `.screenshots-cache\preview\*.json`. They contain no `del` links.

## Tests

```
.venv/bin/python -m unittest discover -s tests -v
```

The tests use temporary git repositories, temporary doc trees, a fake binary
(`tests/fakegf.py`) and a mock EasyImages server on 127.0.0.1. They never
contact the network. The environment hash cross-check reads
`resource/screenshot/env-hash-fixture.json` from the GpgFrontend checkout next
to this repository; set `GF_SHOTS_GPGFRONTEND` to point elsewhere.

Variables used only by the tests: `GF_SHOTS_NO_XVFB=1` (run without
xvfb-run; the platform tag is then not a reference one),
`GF_SHOTS_APPDATA_ROOTS` (where the footprint check looks) and
`GF_SHOTS_TEST_CRASH_AFTER=<state>` (simulate a crash right after a
transaction state is saved).
