// The release notes there are, read from the signed update index. No DOM
// work here: the Release Notes page (ReleaseNotes.astro) draws from this.
//
// Each release in the index may name its notes: a Markdown file in the
// build storage (notes/<version>/<sha256>.md), signed by the maintainer, and
// the file's hash. Releases without notes are left out.

import { isObj, seriesOf, storeUrl } from "../downloads/offers";

export type Entry = {
  version: string;
  series: string;
  notes: string; // path in the build storage
  sha256: string; // what the notes must hash to
  latest: boolean; // the release the stable channel names
};

export type Group = {
  series: string;
  status: string | null; // the series' policy status
  eol: string | null; // last day of fixes, for a legacy series
  current: boolean; // the series of the latest release
  entries: Entry[];
};

// "2.1.14" as [2, 1, 14]; null for anything but a plain release number.
function numbers(version: string): number[] | null {
  const m = /^(\d+)\.(\d+)\.(\d+)$/.exec(version);
  return m ? m.slice(1).map(Number) : null;
}

// Newest first, comparing the numbers as numbers (2.1.10 after 2.1.9).
function newestFirst(x: number[], y: number[]): number {
  for (let i = 0; i < 3; i++) {
    if (x[i] !== y[i]) return y[i] - x[i];
  }
  return 0;
}

// Every release with notes, newest version first.
export function entries(index: unknown): Entry[] {
  const ix = isObj(index) ? index : {};
  const releases = isObj(ix.releases) ? ix.releases : {};
  const stable = ix.channels?.stable;
  const out: [number[], Entry][] = [];
  for (const [version, r] of Object.entries(releases)) {
    const n = numbers(version);
    if (!n || !isObj(r)) continue;
    if (typeof r.notes !== "string" || typeof r.notes_sha256 !== "string") {
      continue;
    }
    out.push([
      n,
      {
        version,
        series: seriesOf(version),
        notes: r.notes,
        sha256: r.notes_sha256,
        latest: version === stable,
      },
    ]);
  }
  return out.sort((x, y) => newestFirst(x[0], y[0])).map(([, e]) => e);
}

// The same entries by series, in the same order, with what the index says
// about each series.
export function groups(index: unknown, list: Entry[]): Group[] {
  const ix = isObj(index) ? index : {};
  const series = isObj(ix.series) ? ix.series : {};
  const latest = list.find((e) => e.latest);
  const out: Group[] = [];
  for (const e of list) {
    let g = out[out.length - 1];
    if (!g || g.series !== e.series) {
      const s = isObj(series[e.series]) ? series[e.series] : {};
      g = {
        series: e.series,
        status: typeof s.status === "string" ? s.status : null,
        eol: typeof s.eol === "string" ? s.eol : null,
        current: latest?.series === e.series,
        entries: [],
      };
      out.push(g);
    }
    g.entries.push(e);
  }
  return out;
}

// Notes begin with their own heading, "## 2.2.5 (2026-11-16)". The page
// draws its own, so that line is taken off, and its date kept.
export function splitHeading(
  md: string,
  version: string,
): { date: string | null; body: string } {
  const text = md.replace(/^﻿/, "").replace(/\r\n/g, "\n");
  const m = /^\s*#{1,6}[ \t]+v?(\S+)[ \t]*(?:\((\d{4}-\d{2}-\d{2})\))?[ \t]*\n/.exec(
    text,
  );
  if (!m || m[1] !== version) return { date: null, body: text };
  return { date: m[2] ?? null, body: text.slice(m[0].length) };
}

// The notes' address, only inside notes/ of the build storage.
export function notesUrl(path: unknown): string | null {
  return storeUrl(path, "notes/");
}

// The anchor of a version on the page: "2.2.5" is "v2-2-5".
export function anchor(version: string): string {
  return `v${version.replace(/\./g, "-")}`;
}
