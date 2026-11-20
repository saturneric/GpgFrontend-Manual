// The privacy policy as the /privacy/ page shows it (pages/privacy.astro).
//
// PrivacyPolicy.md here is a byte-for-byte copy of the file in the main
// repository, and source.json says which revision it is. Both are written
// by scripts/sync-privacy-policy.mjs ("yarn sync:privacy") and never by
// hand. Reading the copy checks it against that record, so a build can't
// publish a policy that is missing, empty or edited here.
//
// The text is a legal one and must reach the page as it is. So it does not
// go through the site's Markdown setup, which would turn its quotes into
// curly ones and number the lines of its address block. micromark renders
// plain CommonMark and changes no character.

import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { micromark } from "micromark";

const DIR = join(process.cwd(), "src/privacy");
const HINT = 'Run "yarn sync:privacy" and commit both files in src/privacy.';

export type Source = {
  repo: string; // "owner/name" on GitHub
  path: string; // the policy's path in that repository
  ref: string; // the branch it is read from
  commit: string; // the last commit that changed it
  committed: string; // that commit's date, UTC
  sha256: string; // what the copy must hash to
  bytes: number;
};

export type Heading = { depth: number; slug: string; text: string };

export type Policy = {
  title: string; // the policy's own first heading
  html: string; // everything below it
  headings: Heading[]; // for the table of contents
  source: Source;
};

function fail(what: string): never {
  throw new Error(`Privacy policy: ${what}. ${HINT}`);
}

function readSource(): Source {
  let s: Partial<Source>;
  try {
    s = JSON.parse(readFileSync(join(DIR, "source.json"), "utf8"));
  } catch {
    fail("src/privacy/source.json is missing or unreadable");
  }
  if (
    typeof s.repo !== "string" ||
    typeof s.path !== "string" ||
    !/^[0-9a-f]{40}$/.test(s.commit ?? "") ||
    !/^\d{4}-\d{2}-\d{2}T/.test(s.committed ?? "") ||
    !/^[0-9a-f]{64}$/.test(s.sha256 ?? "")
  ) {
    fail("src/privacy/source.json is incomplete");
  }
  return s as Source;
}

// micromark writes only these four entities.
function plain(html: string): string {
  return html
    .replace(/<[^>]+>/g, "")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&amp;/g, "&");
}

// "4.1 Update Check" is "41-update-check", as on GitHub.
function slugger(): (text: string) => string {
  const used = new Set<string>();
  return (text) => {
    const base =
      text
        .toLowerCase()
        .trim()
        .replace(/[^\p{L}\p{N}\s-]/gu, "")
        .replace(/\s+/g, "-") || "section";
    let slug = base;
    for (let n = 1; used.has(slug); n++) slug = `${base}-${n}`;
    used.add(slug);
    return slug;
  };
}

export function loadPolicy(): Policy {
  const source = readSource();

  let raw: Buffer;
  try {
    raw = readFileSync(join(DIR, "PrivacyPolicy.md"));
  } catch {
    fail("src/privacy/PrivacyPolicy.md is missing");
  }
  if (createHash("sha256").update(raw).digest("hex") !== source.sha256) {
    fail("src/privacy/PrivacyPolicy.md is not the file source.json records");
  }

  // The first line is the policy's title. The page draws it as its own
  // heading, so it is taken off the text here.
  const text = raw.toString("utf8");
  const first = /^# (\S.*?)\r?\n/.exec(text);
  if (!first) fail("the policy does not start with a title line");
  const body = text.slice(first[0].length);
  if (!body.trim()) fail("the policy has a title but no text");

  // Headings get an id, so the table of contents and links can reach them.
  const headings: Heading[] = [];
  const slug = slugger();
  const html = micromark(body).replace(
    /<h([2-6])>([\s\S]*?)<\/h\1>/g,
    (_all, depth: string, inner: string) => {
      const heading = {
        depth: Number(depth),
        slug: slug(plain(inner)),
        text: plain(inner),
      };
      headings.push(heading);
      return `<h${depth} id="${heading.slug}">${inner}</h${depth}>`;
    },
  );

  return { title: first[1], html, headings, source };
}
