// What can be downloaded right now, read from the signed update index, and
// the helpers that pick a file for the visitor. No DOM work here: the
// download boxes in BuildDownloads.astro draw from this.
//
// The index is built by GpgFrontend's release tooling
// (scripts/release/gfrelease/index.py). Each series ("2.1", "2.2", ...) has
// a status from the release policy, its newest release (latest), and the
// test builds offered for it (beta, rc). Older indexes have no per-series
// rc and keep the newest beta and release candidate at the top level only;
// both shapes are read.

export const BUILDS_BASE = "https://builds.bktus.com/gpgfrontend/";

// stable: the newest release, the main download.
// line: the newest release of another series that still gets fixes.
// rc, beta, nightly: test builds.
export type OfferKind = "stable" | "line" | "rc" | "beta" | "nightly";

export type Offer = {
  kind: OfferKind;
  series: string;
  version: string;
  descriptor: string;
  sha256: string;
  status?: string; // the series' policy status, for "line"
  eol?: string | null; // last day of fixes, for a legacy series
};

export type Artifact = {
  name: string;
  path: string;
  sig?: string; // only releases sign each file
  os: string;
  arch: string;
  kind: string;
  flavor: string; // "installed", "portable" or "qt5"
  min_os: { macos?: string } | null;
  size?: number;
};

export type Visitor = {
  os: string | null; // "ios" for iPhone and iPad
  arch: string | null; // "arm" or "x86" when known
  macos: number | null; // major macOS version when known
};

// Releases sit in releases/; every other build (nightly, beta, release
// candidate) is a promoted CI build and sits in nightly/.
export function isRelease(kind: OfferKind): boolean {
  return kind === "stable" || kind === "line";
}

function folder(kind: OfferKind): string {
  return isRelease(kind) ? "releases/" : "nightly/";
}

// Only files inside the offer's folder of the build storage.
export function buildUrl(path: unknown, kind: OfferKind): string | null {
  if (typeof path !== "string" || !path.startsWith(folder(kind))) {
    return null;
  }
  if (path.includes("..") || path.includes("//")) return null;
  const url = new URL(path, BUILDS_BASE);
  return url.href.startsWith(BUILDS_BASE) ? url.href : null;
}

export async function sha256Hex(data: ArrayBuffer): Promise<string> {
  const digest = await crypto.subtle.digest("SHA-256", data);
  return Array.from(new Uint8Array(digest))
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
}

// ---------------------------------------------------------------- the index

const RC = /^\d+\.\d+\.0-rc\.\d+$/;

function isObj(x: unknown): x is Record<string, any> {
  return typeof x === "object" && x !== null && !Array.isArray(x);
}

// "2.2.4" and "2.3.0-alpha.5+g1234" are in series "2.2" and "2.3".
export function seriesOf(version: string): string {
  const m = /^(\d+)\.(\d+)/.exec(version);
  return m ? `${m[1]}.${m[2]}` : version;
}

// Newest series first. "1" (a whole generation) sorts before "1.0".
function seriesKey(key: string): [number, number] {
  const [a, b] = key.split(".");
  return [parseInt(a, 10) || 0, b === undefined ? -1 : parseInt(b, 10) || 0];
}
function newestFirst(x: string, y: string): number {
  const [xa, xb] = seriesKey(x);
  const [ya, yb] = seriesKey(y);
  return ya - xa || yb - xb;
}

function make(
  kind: OfferKind,
  entry: unknown,
  version: unknown,
  extra: Partial<Offer> = {},
): Offer | null {
  if (!isObj(entry) || typeof version !== "string") return null;
  const { descriptor, sha256 } = entry;
  if (typeof descriptor !== "string" || typeof sha256 !== "string") {
    return null;
  }
  return {
    kind,
    series: seriesOf(version),
    version,
    descriptor,
    sha256,
    ...extra,
  };
}

// Statuses whose releases are still worth downloading.
const SUPPORTED = ["stable", "legacy"];

export type Offers = {
  current: Offer | null;
  older: Offer[];
  testing: Offer[];
};

export function offers(index: unknown): Offers {
  const ix = isObj(index) ? index : {};
  const releases = isObj(ix.releases) ? ix.releases : {};
  const series = isObj(ix.series) ? ix.series : {};
  const keys = Object.keys(series)
    .filter((k) => isObj(series[k]))
    .sort(newestFirst);

  // The release the stable channel names.
  const stableVersion = ix.channels?.stable;
  const current =
    typeof stableVersion === "string"
      ? make("stable", releases[stableVersion], stableVersion)
      : null;

  // The newest release of every other series that still gets fixes.
  const older: Offer[] = [];
  for (const key of keys) {
    const s = series[key];
    if (!SUPPORTED.includes(s.status) || typeof s.latest !== "string") {
      continue;
    }
    if (current && seriesOf(s.latest) === current.series) continue;
    const o = make("line", releases[s.latest], s.latest, {
      status: s.status,
      eol: typeof s.eol === "string" ? s.eol : null,
    });
    if (o) older.push(o);
  }

  // Test builds: release candidates, then betas, newest series first, then
  // the nightly. Older indexes name only one of each at the top level.
  const rcs = keys
    .map((k) => make("rc", series[k].rc, series[k].rc?.version))
    .filter((o): o is Offer => !!o);
  if (!rcs.length) {
    const top = make("rc", ix.prerelease, ix.prerelease?.version);
    if (top) rcs.push(top);
  }
  const betas = keys
    .map((k) => make("beta", series[k].beta, series[k].beta?.version))
    .filter((o): o is Offer => !!o);
  if (!betas.length) {
    const top = make("beta", ix.beta, ix.beta?.version);
    if (top) betas.push(top);
  }
  const nightly = make("nightly", ix.nightly, ix.nightly?.version);

  const seen = new Set<string>();
  const testing = [
    ...rcs.filter((o) => RC.test(o.version)),
    ...betas,
    ...(nightly ? [nightly] : []),
  ].filter((o) => {
    if (seen.has(o.descriptor)) return false;
    seen.add(o.descriptor);
    return true;
  });

  return { current, older, testing };
}

// ------------------------------------------------------- choosing a file

export const MAC_CHIP: Record<string, string> = {
  arm64: "Mac with Apple chip",
  x86_64: "Mac with Intel chip",
};

export function macMajor(a: Artifact): number {
  return parseInt(a.min_os?.macos ?? "0", 10) || 0;
}

// Who a file is for, in plain words, for the full file list.
export function variant(a: Artifact): string {
  const portable = a.flavor === "portable";
  const qt5 = a.flavor === "qt5";
  let base: string;
  switch (a.os) {
    case "windows":
      if (portable) return "Portable";
      if (qt5) return "Qt5 build, for older Windows (portable)";
      return a.kind === "msix" ? "MSIX installer" : "Installer";
    case "macos": {
      const chip = MAC_CHIP[a.arch] ?? a.arch;
      const major = a.min_os?.macos?.split(".")[0];
      return major ? `${chip}, macOS ${major} or newer` : chip;
    }
    case "linux":
      base = a.arch === "aarch64" ? "ARM computers" : "Intel or AMD computers";
      if (portable) return `${base}, portable`;
      if (qt5) return `${base}, Qt5 build for older Linux`;
      return base;
    case "android":
      return a.arch === "arm64-v8a"
        ? "Most phones and tablets"
        : a.arch === "x86_64"
          ? "Emulators and x86 devices"
          : a.arch;
    default:
      return a.arch;
  }
}

const KIND_LABEL: Record<string, string> = {
  msi: ".msi",
  msix: ".msix",
  zip: ".zip",
  dmg: ".dmg",
  apk: ".apk",
  appimage: "AppImage",
};

export function size(bytes: unknown): string {
  if (typeof bytes !== "number" || bytes <= 0) return "";
  return `${(bytes / 1048576).toFixed(bytes < 10485760 ? 1 : 0)} MB`;
}

export function details(a: Artifact): string {
  const parts = [KIND_LABEL[a.kind] ?? a.kind];
  if (a.os === "linux" || a.os === "android") parts.push(a.arch);
  parts.push(size(a.size));
  return parts.filter(Boolean).join(" · ");
}

// On Windows the MSI installer is the recommended one.
function kindRank(a: Artifact): number {
  return a.kind === "msi" ? 0 : a.kind === "msix" ? 1 : 2;
}

function flavorRank(a: Artifact): number {
  return a.flavor === "portable" ? 1 : a.flavor === "qt5" ? 2 : 0;
}

// Most common choice first: the usual chip before the rare one, installed
// before portable before Qt5, MSI before MSIX, older macOS (wider reach)
// before newer.
const COMMON_ARCH: Record<string, string> = {
  windows: "x86_64",
  macos: "arm64",
  linux: "x86_64",
  android: "arm64-v8a",
};
export function order(x: Artifact, y: Artifact): number {
  const rank = (a: Artifact) => [
    COMMON_ARCH[a.os] === a.arch ? 0 : 1,
    flavorRank(a),
    kindRank(a),
    macMajor(a),
  ];
  const rx = rank(x);
  const ry = rank(y);
  for (let i = 0; i < rx.length; i++) {
    if (rx[i] !== ry[i]) return rx[i] - ry[i];
  }
  return 0;
}

// Best guess of the visitor's system. Chromium browsers report the real
// CPU and macOS version through client hints; others only through the
// user agent, which on macOS hides both. iPads ask for the Mac site, so
// a "Mac" with a touch screen is an iPad.
export async function detect(): Promise<Visitor> {
  const ua = navigator.userAgent;
  const v: Visitor = { os: null, arch: null, macos: null };
  const touchMac = /Macintosh/i.test(ua) && (navigator.maxTouchPoints ?? 0) > 1;
  if (/Android/i.test(ua)) v.os = "android";
  else if (/iPhone|iPad|iPod/i.test(ua) || touchMac) v.os = "ios";
  else if (/Windows/i.test(ua)) v.os = "windows";
  else if (/Macintosh|Mac OS X/i.test(ua)) v.os = "macos";
  else if (/Linux|X11/i.test(ua)) v.os = "linux";
  if (/aarch64|arm64/i.test(ua)) v.arch = "arm";
  else if (/x86_64|x64|amd64|Win64/i.test(ua)) v.arch = "x86";

  const uad = (navigator as any).userAgentData;
  if (uad?.getHighEntropyValues) {
    try {
      const h = await uad.getHighEntropyValues([
        "architecture",
        "platformVersion",
      ]);
      if (h.architecture === "arm") v.arch = "arm";
      else if (h.architecture === "x86") v.arch = "x86";
      if (v.os === "macos" && h.platformVersion) {
        const major = parseInt(h.platformVersion, 10);
        if (major > 10) v.macos = major;
      }
    } catch {
      /* keep what the user agent said */
    }
  }
  return v;
}

// The CPU type the app's updater would pick for this visitor.
function wantedArch(v: Visitor): string {
  if (v.os === "android") return v.arch === "x86" ? "x86_64" : "arm64-v8a";
  if (v.os === "linux") return v.arch === "arm" ? "aarch64" : "x86_64";
  return "x86_64";
}

// The build of one flavor for this system, as the app's own updater picks
// it.
export function pick(
  artifacts: Artifact[],
  v: Visitor,
  flavor = "installed",
): Artifact | null {
  const want = wantedArch(v);
  return (
    artifacts
      .filter((a) => a.os === v.os && a.flavor === flavor && a.arch === want)
      .sort((x, y) => kindRank(x) - kindRank(y))[0] ?? null
  );
}

// The disk image for one Mac chip: built for the newest macOS this Mac
// runs when the browser says which; otherwise the oldest, which also runs
// on newer ones.
export function pickMac(
  artifacts: Artifact[],
  v: Visitor,
  arch: string,
): Artifact | null {
  const fits = artifacts
    .filter(
      (a) => a.os === "macos" && a.flavor === "installed" && a.arch === arch,
    )
    .filter((a) => v.macos === null || macMajor(a) <= v.macos)
    .sort((x, y) => macMajor(x) - macMajor(y));
  if (!fits.length) return null;
  return v.macos === null ? fits[0] : fits[fits.length - 1];
}
