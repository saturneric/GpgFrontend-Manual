#!/usr/bin/env node
// Updates the site's copy of the GpgFrontend privacy policy.
//
// The policy is kept in the main repository, and that file is the only one
// anybody edits. The site shows a byte-for-byte copy of it
// (src/privacy/PrivacyPolicy.md) and records which revision the copy is
// (src/privacy/source.json). Both files are written here and nowhere else,
// and the build refuses a copy that does not match its record
// (src/privacy/policy.ts).
//
//   yarn sync:privacy                     update from GitHub
//   yarn sync:privacy --from <checkout>   update from a local clone
//   yarn sync:privacy --check             only say whether the copy is current
//
// Nothing is written unless the policy was read in full and looks like the
// policy. A revision older than the copy is refused, unless --allow-older
// is given. Exit codes: 0 fine, 1 the copy is not current (--check only),
// 2 the policy could not be read or is not usable.

import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import { readFileSync, renameSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const REPO = "saturneric/GpgFrontend";
const FILE = "PrivacyPolicy.md";
const REF = "main";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const COPY = join(ROOT, "src/privacy/PrivacyPolicy.md");
const RECORD = join(ROOT, "src/privacy/source.json");

const TIMEOUT_MS = 20_000;
// The policy is some 16 KB. Far less is a stub or an error page, far more
// is not the policy.
const MIN_BYTES = 1024;
const MAX_BYTES = 512 * 1024;

const USAGE =
  "usage: sync-privacy-policy.mjs [--check] [--from <checkout>] [--allow-older]";

function parseArgs(argv) {
  const opts = { check: false, allowOlder: false, from: null };
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === "--check") opts.check = true;
    else if (argv[i] === "--allow-older") opts.allowOlder = true;
    else if (argv[i] === "--from" && argv[i + 1]) opts.from = argv[++i];
    else throw new Error(USAGE);
  }
  return opts;
}

// One date format whatever the source, so the same commit always gives the
// same record: "2026-11-20T09:31:38Z".
function utc(date) {
  const d = new Date(date);
  if (Number.isNaN(d.getTime())) throw new Error(`bad commit date: ${date}`);
  return d.toISOString().replace(/\.\d{3}Z$/, "Z");
}

async function get(url, accept) {
  const res = await fetch(url, {
    headers: { "User-Agent": "privacy-policy-sync", Accept: accept },
    signal: AbortSignal.timeout(TIMEOUT_MS),
  });
  if (!res.ok) throw new Error(`${url}: HTTP ${res.status}`);
  return res;
}

// The last commit on the branch that changed the file, and the file as that
// commit has it. Asking for the file by commit, not by branch, makes sure
// the text and the recorded revision belong together.
async function fromGitHub() {
  const api =
    `https://api.github.com/repos/${REPO}/commits` +
    `?path=${encodeURIComponent(FILE)}&sha=${REF}&per_page=1`;
  const list = await (await get(api, "application/vnd.github+json")).json();
  const head = Array.isArray(list) ? list[0] : null;
  if (!head || !/^[0-9a-f]{40}$/.test(head.sha ?? "")) {
    throw new Error(`no commit on ${REF} changes ${FILE}. Has the file moved?`);
  }
  const raw = await get(
    `https://raw.githubusercontent.com/${REPO}/${head.sha}/${FILE}`,
    "text/plain",
  );
  return {
    commit: head.sha,
    committed: utc(head.commit?.committer?.date),
    bytes: Buffer.from(await raw.arrayBuffer()),
  };
}

// The same from a local clone. Only committed content is read, never the
// working tree.
function fromCheckout(dir) {
  const git = (...args) =>
    execFileSync("git", ["-C", dir, ...args], {
      maxBuffer: 2 * MAX_BYTES,
      stdio: ["ignore", "pipe", "pipe"],
    });
  const [commit, date] = git("log", "-1", "--format=%H %cI", REF, "--", FILE)
    .toString()
    .trim()
    .split(" ");
  if (!/^[0-9a-f]{40}$/.test(commit ?? "")) {
    throw new Error(`no commit on ${REF} in ${dir} changes ${FILE}`);
  }
  return {
    commit,
    committed: utc(date),
    bytes: git("show", `${commit}:${FILE}`),
  };
}

// Is this the policy, whole? The page needs a title line and sections; an
// empty file, an error page or a binary must never replace the good copy.
function validate(bytes) {
  if (bytes.length < MIN_BYTES || bytes.length > MAX_BYTES) {
    throw new Error(`unexpected size: ${bytes.length} bytes`);
  }
  if (bytes[0] === 0xef && bytes[1] === 0xbb && bytes[2] === 0xbf) {
    throw new Error("starts with a byte order mark");
  }
  let text;
  try {
    text = new TextDecoder("utf-8", { fatal: true }).decode(bytes);
  } catch {
    throw new Error("not valid UTF-8");
  }
  if (!/^# \S.*\r?\n/.test(text)) {
    throw new Error("does not start with a '# ' title line");
  }
  if (!/^## \S/m.test(text)) {
    throw new Error("has no '## ' sections");
  }
}

function readRecord() {
  try {
    return JSON.parse(readFileSync(RECORD, "utf8"));
  } catch {
    return null;
  }
}

// Write next to the target, then rename, so a file is never half written.
function replaceFile(path, data) {
  const tmp = `${path}.tmp`;
  writeFileSync(tmp, data);
  renameSync(tmp, path);
}

function describe(r) {
  return `${r.commit.slice(0, 7)} (${r.committed.slice(0, 10)})`;
}

async function main() {
  const opts = parseArgs(process.argv.slice(2));

  const found = opts.from ? fromCheckout(opts.from) : await fromGitHub();
  validate(found.bytes);

  const record = {
    repo: REPO,
    path: FILE,
    ref: REF,
    commit: found.commit,
    committed: found.committed,
    sha256: createHash("sha256").update(found.bytes).digest("hex"),
    bytes: found.bytes.length,
  };

  const old = readRecord();
  let copyHash = null;
  try {
    copyHash = createHash("sha256").update(readFileSync(COPY)).digest("hex");
  } catch {
    // No copy yet.
  }
  const current =
    old?.commit === record.commit &&
    old?.sha256 === record.sha256 &&
    copyHash === record.sha256;

  const where = opts.from ? opts.from : `github.com/${REPO}`;
  if (current) {
    console.log(`Privacy policy is current: ${describe(record)}, ${where}.`);
    return 0;
  }
  if (opts.check) {
    console.log(
      `Privacy policy is NOT current. Site copy: ${old ? describe(old) : "none"}. ` +
        `${where}: ${describe(record)}. Run "yarn sync:privacy".`,
    );
    return 1;
  }
  // Going back to an older revision is almost always a mistake, such as a
  // policy that was committed but not pushed yet.
  if (old && record.committed < old.committed && !opts.allowOlder) {
    throw new Error(
      `${where} has ${describe(record)}, which is older than the site's copy, ` +
        `${describe(old)}. Has the newer policy been pushed? ` +
        `To go back anyway, add --allow-older`,
    );
  }

  replaceFile(COPY, found.bytes);
  replaceFile(RECORD, `${JSON.stringify(record, null, 2)}\n`);
  console.log(
    `Privacy policy updated: ${old ? describe(old) : "none"} -> ${describe(record)}, ` +
      `${record.bytes} bytes, from ${where}.\n` +
      `Review "git diff src/privacy", then commit both files.`,
  );
  return 0;
}

main().then(
  (code) => process.exit(code),
  (err) => {
    const why = err.cause?.message ? ` (${err.cause.message})` : "";
    console.error(`Privacy policy not updated: ${err.message}${why}`);
    process.exit(2);
  },
);
