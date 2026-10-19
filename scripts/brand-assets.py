"""Draw the pack's visual identity into PNGs: the title wordmark, the pack and
instance icons, the window icons and the menu buttons.

Stdlib only, on purpose. There is no PIL on the machines this runs on, and a PNG
is a few dozen lines of zlib and struct. The images it writes carry no metadata
at all (no tEXt, no time, no path), which is what the privacy rules want of
every image in a repo that may go public.

The palette and the heart are COPIES. The source of truth is weloveyou.mc:
scripts/brand.py for the colours and icons.toml for the heart grid. Same
arrangement as pack-site.py: one duplicated block across a repo boundary,
deliberately, with this comment naming where it comes from.

    python scripts/brand-assets.py            # rewrite every asset
    python scripts/brand-assets.py --check    # fail if any committed asset differs
"""

import pathlib
import struct
import sys
import zlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PACK = ROOT / "pack" / "stable"
RP = PACK / "global_packs" / "required_resources" / "wly"


def rgb(h, a=255):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


# From weloveyou.mc scripts/brand.py. Minecraft's chat palette, desaturated.
BG = rgb("#211F1B")
PANEL = rgb("#282621")
RULE = rgb("#3B372F")
RULE_HI = rgb("#564E42")
FG_HI = rgb("#EFE9DC")
DIM = rgb("#8E8677")
HEART = rgb("#E39AAE")
HEART_SHADE = rgb("#8F5A69")  # the heart, in its own shadow
CLEAR = (0, 0, 0, 0)

# From weloveyou.mc icons.toml [icons.heart].
HEART_ROWS = [
    ".HH..HH.",
    "HHHHHHHH",
    "HHHHHHHH",
    "HHHHHHHH",
    ".HHHHHH.",
    "..HHHH..",
    "...HH...",
    "........",
]

# The wordmark's letters, on an 8-row grid: rows 0-1 ascender, 2-6 x-height,
# 7 descender. Lowercase, because the name is lowercase everywhere else.
GLYPHS = {
    "w": [
        ".....",
        ".....",
        "#...#",
        "#...#",
        "#.#.#",
        "#.#.#",
        ".#.#.",
        ".....",
    ],
    "l": [
        "##.",
        ".#.",
        ".#.",
        ".#.",
        ".#.",
        ".#.",
        ".##",
        "...",
    ],
    "y": [
        ".....",
        ".....",
        "#...#",
        "#...#",
        "#...#",
        ".####",
        "....#",
        "####.",
    ],
}


class Canvas:
    def __init__(self, w, h, fill=CLEAR):
        self.w, self.h = w, h
        self.px = [[fill] * w for _ in range(h)]

    def rect(self, x, y, w, h, c):
        for yy in range(max(0, y), min(self.h, y + h)):
            for xx in range(max(0, x), min(self.w, x + w)):
                self.px[yy][xx] = c

    def grid(self, rows, x, y, scale, colour, mark="#"):
        for r, line in enumerate(rows):
            for col, ch in enumerate(line):
                if ch in mark:
                    self.rect(x + col * scale, y + r * scale, scale, scale, colour)

    def header(self):
        return struct.pack(">IIBBBBB", self.w, self.h, 8, 6, 0, 0, 0)

    def raw(self):
        """Scanlines as a PNG stores them before compression: filter 0, RGBA."""
        return b"".join(b"\x00" + bytes(v for p in row for v in p) for row in self.px)

    def png(self):
        raw = self.raw()

        def chunk(kind, data):
            body = kind + data
            return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body))

        return (b"\x89PNG\r\n\x1a\n"
                + chunk(b"IHDR", self.header())
                + chunk(b"IDAT", zlib.compress(raw, 9))
                + chunk(b"IEND", b""))


def heart(c, x, y, scale, shadow=None, offset=0):
    if shadow:
        c.grid(HEART_ROWS, x + offset, y + offset, scale, shadow, "H")
    c.grid(HEART_ROWS, x, y, scale, HEART, "H")


def wordmark():
    """The title logo. Minecraft draws the top 256x44 of a 256x64 texture, so the
    mark is centred in that band and the rest stays clear."""
    c = Canvas(256, 64)
    scale, gap = 5, 1
    letters = "wly"
    width = sum(len(GLYPHS[ch][0]) for ch in letters) + gap * (len(letters) - 1)
    total = (width + 2 + 8) * scale  # two columns of air, then the heart
    x = (256 - total) // 2
    y = 0
    shadow = 4
    for ch in letters:
        g = GLYPHS[ch]
        c.grid(g, x + shadow, y + shadow, scale, BG)
        c.grid(g, x, y, scale, FG_HI)
        x += (len(g[0]) + gap) * scale
    x += (2 - gap) * scale
    heart(c, x, y + scale, scale, HEART_SHADE, shadow)
    return c


def icon(size, bg=None):
    """The heart, alone, centred. On the dark background where a launcher or a
    pack list puts it against anything; clear where the OS frames it."""
    c = Canvas(size, size, bg or CLEAR)
    scale = max(1, size // 8 if bg is None else (size * 3 // 4) // 8)
    side = 8 * scale
    o = (size - side) // 2
    heart(c, o, o + scale // 2, scale)
    return c


def button(fill, border, top):
    """A 200x20 widget sprite: a fill, a one-pixel border, and a lit top edge.
    Nine-sliced by its .mcmeta, so the borders stay one pixel at every width."""
    c = Canvas(200, 20, fill)
    c.rect(0, 0, 200, 1, border)
    c.rect(0, 19, 200, 1, border)
    c.rect(0, 0, 1, 20, border)
    c.rect(199, 0, 1, 20, border)
    c.rect(1, 1, 198, 1, top)
    return c


NINE_SLICE = ('{\n  "gui": {\n    "scaling": {\n      "type": "nine_slice",\n'
              '      "width": 200,\n      "height": 20,\n      "border": 2\n    }\n  }\n}\n')

SPRITES = RP / "assets" / "minecraft" / "textures" / "gui" / "sprites" / "widget"

ASSETS = {
    RP / "pack.png": lambda: icon(64, BG),
    RP / "assets" / "wly" / "textures" / "gui" / "title" / "wly.png": wordmark,
    SPRITES / "button.png": lambda: button(PANEL, RULE_HI, RULE),
    SPRITES / "button_highlighted.png": lambda: button(RULE, HEART, RULE_HI),
    SPRITES / "button_disabled.png": lambda: button(BG, RULE, BG),
    # The window icon, for FancyMenu's Global Customizations to point at.
    PACK / "config" / "fancymenu" / "assets" / "wly" / "icon_16.png": lambda: icon(16),
    PACK / "config" / "fancymenu" / "assets" / "wly" / "icon_32.png": lambda: icon(32),
    # Prism imports <iconKey>.png from the zip root as the instance icon.
    ROOT / "instance" / "stable" / "wly.png": lambda: icon(128, BG),
}

TEXT = {SPRITES / f"{n}.png.mcmeta": NINE_SLICE
        for n in ("button", "button_highlighted", "button_disabled")}


def decoded(data):
    """(header, scanlines) of a PNG this script wrote, or None.

    --check compares these rather than file bytes: the same pixels compress to
    different bytes under a different zlib, and CI's Python bundles another one.
    """
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        return None
    pos, header, idat = 8, None, b""
    while pos + 8 <= len(data):
        (length,) = struct.unpack(">I", data[pos:pos + 4])
        kind, body = data[pos + 4:pos + 8], data[pos + 8:pos + 8 + length]
        if kind == b"IHDR":
            header = body
        elif kind == b"IDAT":
            idat += body
        pos += 12 + length
    try:
        return header, zlib.decompress(idat)
    except zlib.error:
        return None


def main():
    check = "--check" in sys.argv
    stale = []
    for path, draw in ASSETS.items():
        canvas = draw()
        if check:
            if not path.exists() or decoded(path.read_bytes()) != (canvas.header(), canvas.raw()):
                stale.append(path)
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(canvas.png())
    for path, text in TEXT.items():
        if check:
            if not path.exists() or path.read_text(encoding="utf-8") != text:
                stale.append(path)
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")
    if stale:
        for p in stale:
            print(f"::error::{p.relative_to(ROOT)} differs from scripts/brand-assets.py")
        sys.exit(1)
    if not check:
        print(f"wrote {len(ASSETS)} images and {len(TEXT)} sprite metadata files")


if __name__ == "__main__":
    main()
