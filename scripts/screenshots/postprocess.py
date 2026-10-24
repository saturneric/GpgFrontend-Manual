"""Frame, shadow, padding and highlights for a raw capture; PNG and lossless WebP out.

Every size is given in logical pixels and scaled by the capture's DPR. All
drawing uses integer coordinates so the output depends only on the inputs and
the Pillow/libwebp versions (both recorded in inputs_hash).
"""

from __future__ import annotations

import re
import shutil
import subprocess
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import PIL
from PIL import Image, ImageChops, ImageDraw, ImageFilter, features

from common import PipelineError, atomic_write_bytes, sha256_bytes, sha256_file
from manifest import Entry, Highlight

HIGHLIGHT_RGBA = (229, 72, 77, 255)
HIGHLIGHT_WIDTH = 2
HIGHLIGHT_OUTSET = 3
HIGHLIGHT_RADIUS = 4
ARROW_LENGTH = 40
ARROW_HEAD = 10
ARROW_WIDTH = 3
ARROW_GAP = 4
SHADOW_OPACITY = 0.30
SHADOW_OFFSET_Y = 4


class PostprocessError(PipelineError):
    def __init__(self, reason: str, detail: str = "") -> None:
        super().__init__(f"{reason}: {detail}" if detail else reason)
        self.reason = reason


@dataclass
class Processed:
    png: Path
    webp: Path
    png_sha256: str
    webp_sha256: str
    pixels_sha256: str


@lru_cache(maxsize=1)
def optimizer() -> str:
    """`oxipng <version>` when available, else `none`."""
    exe = shutil.which("oxipng")
    if not exe:
        return "none"
    try:
        out = subprocess.run([exe, "--version"], capture_output=True, timeout=30, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return "none"
    match = re.search(r"(\d+\.\d+(?:\.\d+)?)", out.stdout.decode("utf-8", "replace"))
    return f"oxipng {match.group(1)}" if match and out.returncode == 0 else "none"


def processing_descriptor() -> dict[str, str]:
    return {
        "optimizer": optimizer(),
        "pillow": PIL.__version__,
        "libwebp": str(features.version("webp")),
    }


def pixels_sha256(image: Image.Image) -> str:
    return sha256_bytes(image.convert("RGBA").tobytes())


def png_pixels_sha256(path: Path) -> str:
    with Image.open(path) as img:
        return pixels_sha256(img)


def _rect_for(geometry: dict[str, Any], name: str) -> tuple[int, int, int, int]:
    if name in (geometry.get("missing") or []):
        raise PostprocessError("highlight-missing", name)
    widget = (geometry.get("widgets") or {}).get(name)
    if not isinstance(widget, dict) or not isinstance(widget.get("rect"), list) or len(widget["rect"]) != 4:
        raise PostprocessError("highlight-unknown", name)
    x, y, w, h = (int(v) for v in widget["rect"])
    if w <= 0 or h <= 0:
        raise PostprocessError("highlight-missing", f"{name} has an empty rect")
    return x, y, w, h


def _draw_box(draw: ImageDraw.ImageDraw, rect: tuple[int, int, int, int], size: tuple[int, int], dpr: int) -> None:
    x, y, w, h = rect
    out = HIGHLIGHT_OUTSET * dpr
    width = HIGHLIGHT_WIDTH * dpr
    left = max(0, x - out)
    top = max(0, y - out)
    right = min(size[0] - 1, x + w - 1 + out)
    bottom = min(size[1] - 1, y + h - 1 + out)
    if right - left < 2 * width or bottom - top < 2 * width:
        raise PostprocessError("highlight-too-small", str(rect))
    draw.rounded_rectangle((left, top, right, bottom), radius=HIGHLIGHT_RADIUS * dpr,
                           outline=HIGHLIGHT_RGBA, width=width)


def _draw_arrow(draw: ImageDraw.ImageDraw, rect: tuple[int, int, int, int], size: tuple[int, int], dpr: int) -> None:
    """An arrow pointing at the rect, from the left if there is room, else
    from the right, else from below."""
    x, y, w, h = rect
    length = ARROW_LENGTH * dpr
    head = ARROW_HEAD * dpr
    gap = ARROW_GAP * dpr
    cy = y + h // 2
    cx = x + w // 2
    if x - gap - length >= 0:
        tip, tail, axis = (x - gap, cy), (x - gap - length, cy), (-1, 0)
    elif x + w + gap + length <= size[0]:
        tip, tail, axis = (x + w + gap, cy), (x + w + gap + length, cy), (1, 0)
    else:
        tip = (cx, min(size[1] - 1, y + h + gap))
        tail, axis = (cx, min(size[1] - 1, tip[1] + length)), (0, 1)
    draw.line((tail, tip), fill=HIGHLIGHT_RGBA, width=ARROW_WIDTH * dpr)
    # axis points from the tip towards the tail.
    ax, ay = axis
    base = (tip[0] + ax * head, tip[1] + ay * head)
    side = (-ay * (head // 2 + dpr), ax * (head // 2 + dpr))
    draw.polygon([tip, (base[0] + side[0], base[1] + side[1]), (base[0] - side[0], base[1] - side[1])],
                 fill=HIGHLIGHT_RGBA)


def apply_highlights(image: Image.Image, geometry: dict[str, Any], highlights: tuple[Highlight, ...], dpr: int) -> Image.Image:
    if not highlights:
        return image
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for highlight in highlights:
        rect = _rect_for(geometry, highlight.name)
        if highlight.style == "arrow":
            _draw_arrow(draw, rect, image.size, dpr)
        else:
            _draw_box(draw, rect, image.size, dpr)
    return Image.alpha_composite(image, overlay)


def apply_crop(image: Image.Image, geometry: dict[str, Any], crop: str | None) -> Image.Image:
    """Cut the capture down to one named widget, after highlights are drawn."""
    if crop is None:
        return image
    x, y, w, h = _rect_for(geometry, crop)
    return image.crop((x, y, x + w, y + h))


def apply_frame(image: Image.Image, frame: dict[str, Any], dpr: int) -> Image.Image:
    radius = int(frame["radius"]) * dpr
    blur = int(frame["shadow"]) * dpr
    pad = int(frame["padding"]) * dpr
    w, h = image.size
    if radius:
        mask = Image.new("L", image.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, w - 1, h - 1), radius=radius, fill=255)
        image = image.copy()
        image.putalpha(ImageChops.multiply(image.getchannel("A"), mask))
    canvas = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0))
    if blur:
        alpha = image.getchannel("A").point(lambda v: int(v * SHADOW_OPACITY))
        shadow_alpha = Image.new("L", canvas.size, 0)
        shadow_alpha.paste(alpha, (pad, pad + SHADOW_OFFSET_Y * dpr))
        shadow_alpha = shadow_alpha.filter(ImageFilter.GaussianBlur(blur / 2))
        shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        shadow.putalpha(shadow_alpha)
        canvas = Image.alpha_composite(canvas, shadow)
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    layer.paste(image, (pad, pad))
    return Image.alpha_composite(canvas, layer)


def _encode_png(image: Image.Image, path: Path) -> None:
    from io import BytesIO

    buf = BytesIO()
    image.save(buf, format="PNG", compress_level=9)
    atomic_write_bytes(path, buf.getvalue())
    if optimizer() != "none":
        proc = subprocess.run(
            [shutil.which("oxipng") or "oxipng", "--opt", "2", "--strip", "safe", "--quiet", str(path)],
            capture_output=True, timeout=300, check=False,
        )
        if proc.returncode != 0:
            raise PostprocessError("oxipng-failed", proc.stderr.decode("utf-8", "replace").strip())


def _encode_webp(image: Image.Image, path: Path) -> None:
    from io import BytesIO

    buf = BytesIO()
    image.save(buf, format="WEBP", lossless=True, quality=100, method=6, exact=True)
    atomic_write_bytes(path, buf.getvalue())


def process(raw_png: Path, geometry: dict[str, Any], entry: Entry, out_dir: Path, stem: str) -> Processed:
    dpr = int(geometry.get("dpr") or 0)
    if dpr != 2:
        raise PostprocessError("dpr-mismatch", f"expected 2, got {geometry.get('dpr')!r}")
    with Image.open(raw_png) as opened:
        image = opened.convert("RGBA")
    if list(image.size) != list(geometry.get("image_size") or []):
        raise PostprocessError("size-mismatch", f"PNG {image.size} vs geometry {geometry.get('image_size')}")
    image = apply_highlights(image, geometry, entry.highlight, dpr)
    image = apply_crop(image, geometry, entry.crop)
    image = apply_frame(image, entry.frame, dpr)
    png = Path(out_dir) / f"{stem}.png"
    webp = Path(out_dir) / f"{stem}.webp"
    _encode_png(image, png)
    with Image.open(png) as final:
        final_rgba = final.convert("RGBA")
    _encode_webp(final_rgba, webp)
    with Image.open(webp) as check:
        if check.convert("RGBA").tobytes() != final_rgba.tobytes():
            raise PostprocessError("webp-not-lossless", str(webp))
    return Processed(
        png=png,
        webp=webp,
        png_sha256=sha256_file(png),
        webp_sha256=sha256_file(webp),
        pixels_sha256=pixels_sha256(final_rgba),
    )
