"""Image reference parsing, inventory counts and definition URL rewriting.

Recognised image forms:
  reference style  ![alt][label], ![alt][] and ![label] (when defined)
  inline           ![alt](url "title")
  html             <img src="url">
Definitions are `[label]: url`, including the wrapped form where the URL sits
on the following line. Fenced code blocks and inline code spans are skipped.
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Iterator
from urllib.parse import urlparse

from common import DOCS_SUBDIR, PipelineError, read_text_exact

DOC_SUFFIXES = (".md", ".mdx")

_FENCE_RE = re.compile(r"^[ \t]*(`{3,}|~{3,})")
_CODE_SPAN_RE = re.compile(r"(`+)(?:(?!\1).)+?\1")
_IMG_START_RE = re.compile(r"!\[")
_DEF_RE = re.compile(r"^[ \t]*\[([^\]\^][^\]]*)\]:[ \t]*(.*)$")
_HTML_IMG_RE = re.compile(r"<img\b[^>]*?\bsrc\s*=\s*(?:\"([^\"]*)\"|'([^']*)'|(\{[^}]*\}))", re.IGNORECASE)
_URL_TOKEN_RE = re.compile(r"<([^>\n]*)>|(\S+)")


def normalize_label(label: str) -> str:
    return " ".join(label.split()).casefold()


@dataclass(frozen=True)
class ImageRef:
    doc: str
    line: int
    kind: str  # reference | inline | html
    label: str | None  # normalized, reference style only
    raw_label: str | None
    url: str | None  # inline and html only


@dataclass(frozen=True)
class Definition:
    label: str
    raw_label: str
    url: str
    line_start: int  # 1-based, inclusive
    line_end: int
    url_start: int  # character offsets into the page text
    url_end: int
    text: str  # the original definition lines, line endings included


@dataclass
class PageScan:
    doc: str
    refs: list[ImageRef] = field(default_factory=list)
    definitions: dict[str, list[Definition]] = field(default_factory=dict)

    def definition_for(self, label: str) -> Definition | None:
        found = self.definitions.get(normalize_label(label))
        return found[0] if found else None

    def ref_url(self, ref: ImageRef) -> str | None:
        if ref.kind != "reference":
            return ref.url
        definition = self.definition_for(ref.label or "")
        return definition.url if definition else None

    def image_labels(self) -> list[str]:
        out: list[str] = []
        for ref in self.refs:
            if ref.kind == "reference" and ref.label not in out:
                out.append(ref.label or "")
        return out

    def has_reference(self, label: str) -> bool:
        wanted = normalize_label(label)
        return any(r.kind == "reference" and r.label == wanted for r in self.refs)


@dataclass(frozen=True)
class _Line:
    number: int
    start: int  # offset of first character
    body: str  # without line ending
    in_code: bool


def _lines(text: str) -> list[_Line]:
    out: list[_Line] = []
    offset = 0
    fence: str | None = None
    for number, raw in enumerate(text.splitlines(keepends=True), start=1):
        body = raw.rstrip("\r\n")
        match = _FENCE_RE.match(body)
        in_code = fence is not None
        if match:
            marker = match.group(1)
            if fence is None:
                fence = marker
                in_code = True
            elif marker[0] == fence[0] and len(marker) >= len(fence) and not body.strip()[len(marker):].strip():
                fence = None
                in_code = True
        out.append(_Line(number, offset, body, in_code))
        offset += len(raw)
    return out


def _mask_code_spans(body: str) -> str:
    return _CODE_SPAN_RE.sub(lambda m: " " * len(m.group(0)), body)


def _bracket_end(text: str, open_index: int) -> int:
    """Index of the `]` closing the `[` at open_index, allowing nesting."""
    depth = 0
    i = open_index
    while i < len(text):
        ch = text[i]
        if ch == "\\":
            i += 2
            continue
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def _parse_definitions(doc: str, text: str, lines: list[_Line]) -> dict[str, list[Definition]]:
    defs: dict[str, list[Definition]] = {}
    for idx, line in enumerate(lines):
        if line.in_code:
            continue
        match = _DEF_RE.match(line.body)
        if not match:
            continue
        raw_label = match.group(1)
        rest_start = line.start + match.start(2)
        rest = match.group(2)
        line_end = line.number
        token = _URL_TOKEN_RE.match(rest) if rest.strip() else None
        if token:
            group = 1 if token.group(1) is not None else 2
            url = token.group(group)
            url_start = rest_start + token.start(group)
            url_end = rest_start + token.end(group)
        else:
            url, url_start, url_end = "", line.start + len(line.body), line.start + len(line.body)
            nxt = lines[idx + 1] if idx + 1 < len(lines) else None
            if nxt and not nxt.in_code and nxt.body.strip() and not _DEF_RE.match(nxt.body):
                lead = len(nxt.body) - len(nxt.body.lstrip())
                wrapped = _URL_TOKEN_RE.match(nxt.body[lead:])
                if wrapped:
                    group = 1 if wrapped.group(1) is not None else 2
                    url = wrapped.group(group)
                    url_start = nxt.start + lead + wrapped.start(group)
                    url_end = nxt.start + lead + wrapped.end(group)
                    line_end = nxt.number
        block_end = lines[line_end].start if line_end < len(lines) else len(text)
        definition = Definition(
            label=normalize_label(raw_label),
            raw_label=raw_label,
            url=url,
            line_start=line.number,
            line_end=line_end,
            url_start=url_start,
            url_end=url_end,
            text=text[line.start:block_end],
        )
        defs.setdefault(definition.label, []).append(definition)
    return defs


def _parse_images(doc: str, lines: list[_Line], defs: dict[str, list[Definition]]) -> list[ImageRef]:
    refs: list[ImageRef] = []
    for line in lines:
        if line.in_code:
            continue
        body = _mask_code_spans(line.body)
        if _DEF_RE.match(body):
            continue
        for match in _IMG_START_RE.finditer(body):
            open_index = match.start() + 1
            close = _bracket_end(body, open_index)
            if close < 0:
                continue
            alt = body[open_index + 1:close]
            after = body[close + 1:]
            if after.startswith("["):
                end = after.find("]")
                if end < 0:
                    continue
                label = after[1:end] or alt
                refs.append(ImageRef(doc, line.number, "reference", normalize_label(label), label, None))
            elif after.startswith("("):
                token = _URL_TOKEN_RE.match(after[1:].lstrip())
                url = None
                if token:
                    url = token.group(1) if token.group(1) is not None else token.group(2).rstrip(")")
                refs.append(ImageRef(doc, line.number, "inline", None, None, url))
            elif normalize_label(alt) in defs:
                refs.append(ImageRef(doc, line.number, "reference", normalize_label(alt), alt, None))
        for match in _HTML_IMG_RE.finditer(body):
            url = next((g for g in match.groups() if g is not None), None)
            if url is not None and url.startswith("{"):
                url = None  # a JSX expression; not a literal URL
            refs.append(ImageRef(doc, line.number, "html", None, None, url))
    return refs


def scan_text(doc: str, text: str) -> PageScan:
    lines = _lines(text)
    defs = _parse_definitions(doc, text, lines)
    return PageScan(doc=doc, refs=_parse_images(doc, lines, defs), definitions=defs)


def doc_files(manual_root: Path) -> list[Path]:
    docs_dir = Path(manual_root) / DOCS_SUBDIR
    if not docs_dir.is_dir():
        raise PipelineError(f"docs directory not found: {docs_dir}")
    return sorted(p for p in docs_dir.rglob("*") if p.is_file() and p.suffix in DOC_SUFFIXES)


def rel_doc(manual_root: Path, path: Path) -> str:
    return Path(path).resolve().relative_to(Path(manual_root).resolve()).as_posix()


def scan_docs(manual_root: Path) -> list[PageScan]:
    return [scan_text(rel_doc(manual_root, p), read_text_exact(p)) for p in doc_files(manual_root)]


def url_format(url: str | None) -> str:
    if not url:
        return "(none)"
    suffix = PurePosixPath(urlparse(url).path).suffix.lower().lstrip(".")
    return suffix or "(none)"


def is_missing_url(url: str | None) -> bool:
    return url is None or not url.strip() or url.strip().upper() == "TODO"


def _iter_ref_urls(page: PageScan) -> Iterator[tuple[ImageRef, str | None]]:
    for ref in page.refs:
        yield ref, page.ref_url(ref)


def inventory(pages: list[PageScan], managed: dict[tuple[str, str], str]) -> dict:
    """Observed counts. `managed` maps (doc, normalized label) to an entry id.

    Formats are by URL extension only; the content is never fetched.
    """
    page_rows = []
    all_refs = []
    total_refs = 0
    total_defs = 0
    total_urls: set[str] = set()
    total_by_ref: Counter[str] = Counter()
    for page in pages:
        if not page.refs:
            continue
        urls: list[str] = []
        by_ref: Counter[str] = Counter()
        labels = page.image_labels()
        defs = sum(len(page.definitions.get(label, [])) for label in labels)
        for ref, url in _iter_ref_urls(page):
            fmt = url_format(url)
            by_ref[fmt] += 1
            if url and not is_missing_url(url):
                urls.append(url)
            all_refs.append({
                "doc": page.doc,
                "line": ref.line,
                "kind": ref.kind,
                "ref": ref.raw_label if ref.kind == "reference" else None,
                "url": url,
                "format": fmt,
                "managed_id": managed.get((page.doc, ref.label or "")) if ref.kind == "reference" else None,
            })
        unique = sorted(set(urls))
        page_rows.append({
            "doc": page.doc,
            "references": len(page.refs),
            "definitions": defs,
            "unique_urls": len(unique),
            "formats_by_reference": dict(sorted(by_ref.items())),
            "formats_by_unique_url": dict(sorted(Counter(url_format(u) for u in unique).items())),
        })
        total_refs += len(page.refs)
        total_defs += defs
        total_urls.update(unique)
        total_by_ref.update(by_ref)
    return {
        "pages": page_rows,
        "total": {
            "pages_with_images": len(page_rows),
            "references": total_refs,
            "definitions": total_defs,
            "unique_urls": len(total_urls),
            "formats_by_reference": dict(sorted(total_by_ref.items())),
            "formats_by_unique_url": dict(sorted(Counter(url_format(u) for u in total_urls).items())),
        },
        "refs": all_refs,
    }


def find_definitions(text: str, label: str) -> list[Definition]:
    return scan_text("", text).definitions.get(normalize_label(label), [])


def replace_url(text: str, definition: Definition, new_url: str) -> str:
    """Swaps only the URL token; every other byte stays as it was."""
    if not new_url or any(c.isspace() for c in new_url):
        raise PipelineError(f"refusing to write an invalid URL {new_url!r}")
    if definition.url_start == definition.url_end and not definition.url:
        return text[:definition.url_start] + " " + new_url + text[definition.url_end:]
    return text[:definition.url_start] + new_url + text[definition.url_end:]


def replace_definition_url(text: str, label: str, new_url: str, expect_url: str) -> str:
    """Rewrites the single definition of `label`, which must carry expect_url."""
    defs = find_definitions(text, label)
    if len(defs) != 1:
        raise PipelineError(f"ref [{label}] has {len(defs)} definitions, expected exactly one")
    if defs[0].url != expect_url:
        raise PipelineError(f"ref [{label}] carries {defs[0].url!r}, expected {expect_url!r}")
    return replace_url(text, defs[0], new_url)
