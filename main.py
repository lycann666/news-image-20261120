#!/usr/bin/env python3
"""THE WORLD TODAY - Friday 20 November 2026.

A one-page newspaper front page summing up the day's world news,
drawn entirely procedurally: every pixel is produced by this file.
Standard library only, no network, no fonts, no images read from disk.
The output is byte-identical on every run.
"""

import math
import os
import struct
import zlib

W, H = 1024, 1024

# ---------------------------------------------------------------- palette
PAPER = (247, 242, 231)
INK = (18, 18, 18)
RED = (178, 28, 28)
BLUE = (28, 64, 128)
SKY = (178, 214, 235)
SEA = (120, 178, 214)
LAND = (96, 148, 84)
LAND2 = (128, 172, 96)
GREY = (110, 108, 100)
LIGHT = (232, 226, 212)
GOLD = (212, 168, 44)
WHITE = (255, 255, 255)
CREAM = (252, 248, 238)

# ---------------------------------------------------------------- 5x7 font
# Each glyph is 7 rows of 5 bits, written here by hand for this entry.
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    "*": ("00000", "10101", "01110", "11111", "01110", "10101", "00000"),
    "#": ("01010", "01010", "11111", "01010", "11111", "01010", "01010"),
    "@": ("01110", "10001", "10111", "10101", "10110", "10000", "01110"),
    "<": ("00010", "00100", "01000", "10000", "01000", "00100", "00010"),
    ">": ("01000", "00100", "00010", "00001", "00010", "00100", "01000"),
    "_": ("00000", "00000", "00000", "00000", "00000", "00000", "11111"),
}


def text_width(text, scale):
    return len(text) * 6 * scale - scale


def wrap(text, max_width, scale):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    words = text.split(" ")
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if text_width(trial, scale) <= max_width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg * (w * h))

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = c

    def rect(self, x, y, w, h, c):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, c)

    def hline(self, x, y, w, c, t=1):
        self.rect(x, y, w, t, c)

    def vline(self, x, y, h, c, t=1):
        self.rect(x, y, t, h, c)

    def line(self, x0, y0, x1, y1, c):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            self.set(x0, y0, c)
            if x0 == x1 and y0 == y1:
                return
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def disc(self, cx, cy, r, c):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    self.set(xx, yy, c)

    def ring(self, cx, cy, r, c, t=2):
        for a in range(360):
            rad = math.radians(a)
            for k in range(t):
                self.set(int(cx + (r - k) * math.cos(rad)),
                         int(cy + (r - k) * math.sin(rad)), c)

    def ellipse_ring(self, cx, cy, rx, ry, c):
        for a in range(720):
            rad = math.radians(a / 2.0)
            self.set(int(cx + rx * math.cos(rad)),
                     int(cy + ry * math.sin(rad)), c)

    def ellipse(self, cx, cy, rx, ry, c):
        for yy in range(cy - ry, cy + ry + 1):
            for xx in range(cx - rx, cx + rx + 1):
                if ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2 <= 1.0:
                    self.set(xx, yy, c)

    def char(self, x, y, ch, scale, c):
        glyph = FONT.get(ch, FONT[" "])
        for row in range(7):
            bits = glyph[row]
            for col in range(5):
                if bits[col] == "1":
                    self.rect(x + col * scale, y + row * scale,
                              scale, scale, c)

    def text(self, x, y, s, scale, c):
        for ch in s.upper():
            self.char(x, y, ch, scale, c)
            x += 6 * scale
        return x

    def text_center(self, cx, y, s, scale, c):
        x = cx - text_width(s.upper(), scale) // 2
        return self.text(x, y, s, scale, c)

    def para(self, x, y, width, s, scale, c, leading=4):
        """Wrapped paragraph; returns y just below the last line."""
        lh = 7 * scale + leading
        for line in wrap(s, width, scale):
            self.text(x, y, line, scale, c)
            y += lh
        return y


# ---------------------------------------------------------------- png
def write_png(cv, path):
    raw = bytearray()
    stride = cv.w * 3
    for y in range(cv.h):
        raw.append(0)
        raw += cv.px[y * stride:(y + 1) * stride]
    comp = zlib.compress(bytes(raw), 9)

    def chunk(kind, data):
        out = struct.pack(">I", len(data)) + kind + data
        return out + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", comp)
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)
    return len(png)


# ---------------------------------------------------------------- artwork
def draw_flag_us(cv, x, y, w, h):
    stripe = max(1, h // 13)
    for i in range(13):
        cv.rect(x, y + i * stripe, w, stripe,
                (178, 34, 52) if i % 2 == 0 else WHITE)
    cw, ch = int(w * 0.4), stripe * 7
    cv.rect(x, y, cw, ch, (28, 48, 96))
    for r in range(5):
        for c in range(6):
            sx = x + 6 + c * (cw - 12) // 5
            sy = y + 5 + r * (ch - 10) // 4
            cv.disc(sx, sy, 2, WHITE)


def draw_flag_cn(cv, x, y, w, h):
    cv.rect(x, y, w, h, (222, 41, 16))
    # one large star + four small stars, drawn as five-point dots
    def star(cx, cy, r, c):
        cv.disc(cx, cy, r, c)
        for a in range(5):
            rad = math.radians(a * 72 - 90)
            cv.set(int(cx + r * 1.6 * math.cos(rad)),
                   int(cy + r * 1.6 * math.sin(rad)), c)
    star(x + w // 5, y + h // 4, 7, GOLD)
    for dx, dy in ((w // 2, 8), (w * 3 // 5, h // 4),
                   (w // 2, h // 2), (w * 3 // 5, h * 3 // 5)):
        star(x + dx, y + dy, 3, GOLD)


def draw_flag_ru(cv, x, y, w, h):
    third = h // 3
    cv.rect(x, y, w, third, WHITE)
    cv.rect(x, y + third, w, third, (0, 57, 166))
    cv.rect(x, y + 2 * third, w, h - 2 * third, (213, 0, 50))


def draw_globe(cv, cx, cy, r):
    cv.disc(cx, cy, r, SEA)
    # stylised landmasses
    cv.ellipse(cx - r // 2, cy - r // 3, r // 3, r // 5, LAND)
    cv.ellipse(cx + r // 3, cy - r // 4, r // 4, r // 6, LAND2)
    cv.ellipse(cx - r // 5, cy + r // 3, r // 4, r // 5, LAND)
    cv.ellipse(cx + r // 2, cy + r // 4, r // 5, r // 7, LAND2)
    cv.ellipse(cx, cy - r // 2, r // 6, r // 8, LAND)
    # meridians and parallels
    for k in range(1, 4):
        cv.ring(cx, cy, r * k // 4, (255, 255, 255), 1)
    cv.ellipse_ring(cx, cy, r // 3, r, (255, 255, 255))
    cv.ellipse_ring(cx, cy, r * 2 // 3, r, (255, 255, 255))
    cv.hline(cx - r, cy, 2 * r, (255, 255, 255), 1)
    cv.ring(cx, cy, r, INK, 3)
    # polar caps
    cv.ellipse(cx, cy - r + 4, r // 3, 5, WHITE)
    cv.ellipse(cx, cy + r - 4, r // 3, 5, WHITE)


def draw_cyclone(cv, cx, cy, r):
    # spiral storm: arms curving into the eye
    for arm in range(3):
        base = arm * 2.094
        prev = None
        for t in range(0, 121):
            a = base + t * 0.055
            rr = 6 + (r - 6) * t / 120.0
            px = int(cx + rr * math.cos(a))
            py = int(cy + rr * math.sin(a) * 0.85)
            if prev is not None:
                cv.line(prev[0], prev[1], px, py, BLUE)
                cv.line(prev[0], prev[1] + 1, px, py + 1, BLUE)
            prev = (px, py)
    cv.disc(cx, cy, 7, PAPER)
    cv.ring(cx, cy, 7, BLUE, 2)
    cv.ring(cx, cy, r, BLUE, 2)


def draw_star(cv, cx, cy, r, c):
    for a in range(5):
        rad = math.radians(a * 72 - 90)
        ex = int(cx + r * math.cos(rad))
        ey = int(cy + r * math.sin(rad))
        cv.line(cx, cy, ex, ey, c)
        rad2 = math.radians(a * 72 - 90 + 36)
        ix = int(cx + r * 0.45 * math.cos(rad2))
        iy = int(cy + r * 0.45 * math.sin(rad2))
        cv.line(cx, cy, ix, iy, c)
    cv.disc(cx, cy, max(1, r // 3), c)


# ---------------------------------------------------------------- layout
def build():
    cv = Canvas(W, H, PAPER)
    M = 36                      # page margin
    CW = W - 2 * M              # content width
    x0, x1 = M, W - M

    # ---- top dateline bar
    cv.text(x0, 26, "FRIDAY 20 NOVEMBER 2026", 2, INK)
    r = "WORLD EDITION - NO. 324"
    cv.text(x1 - text_width(r, 2), 26, r, 2, INK)
    cv.hline(x0, 48, CW, INK, 2)

    # ---- masthead
    cv.text_center(W // 2, 62, "THE WORLD TODAY", 9, INK)
    cv.text_center(W // 2, 132, "THE DAY'S WORLD NEWS IN ONE PAGE",
                   2, GREY)
    cv.hline(x0, 156, CW, RED, 4)
    cv.hline(x0, 164, CW, INK, 1)

    # ---- kicker + main headline
    y = 180
    cv.text_center(W // 2, y, "HISTORIC THREE-WAY SUMMIT IN CHINA", 2, RED)
    y += 28
    for line in ("TRUMP, XI AND PUTIN",
                 "SIGN HISTORIC PEACE",
                 "DECLARATION"):
        cv.text_center(W // 2, y, line, 5, INK)
        y += 40
    y += 6
    y = cv.para(x0 + 120, y, CW - 240,
                "THE THREE LEADERS RELEASE A JOINT STATEMENT AFTER THE "
                "FIRST-EVER TRILATERAL MEETING.",
                2, INK)
    y += 8
    cv.hline(x0, y, CW, INK, 1)
    y += 12

    # ---- hero: the three flags over a globe
    hero_y = y
    hero_h = 140
    fw, fh = 250, 92
    gap = (CW - 3 * fw) // 2
    for fx in (x0, x0 + fw + gap, x0 + 2 * (fw + gap)):
        cv.rect(fx - 2, hero_y + 6, fw + 4, fh + 4, INK)
    draw_flag_us(cv, x0, hero_y + 8, fw, fh)
    draw_flag_cn(cv, x0 + fw + gap, hero_y + 8, fw, fh)
    draw_flag_ru(cv, x0 + 2 * (fw + gap), hero_y + 8, fw, fh)
    cv.text_center(W // 2, hero_y + 104,
                   "THE FLAGS OF THE UNITED STATES, CHINA AND RUSSIA", 2, INK)
    cv.text_center(W // 2, hero_y + 124,
                   "FLY OVER THE JOINT PEACE DECLARATION IN BEIJING", 2, INK)
    y = hero_y + hero_h + 4
    cv.hline(x0, y, CW, INK, 2)
    y += 12

    # ---- three columns of stories
    col_w = (CW - 2 * 24) // 3
    cxs = [x0, x0 + col_w + 24, x0 + 2 * (col_w + 24)]
    col_top = y

    def story(cx, y, kicker, head, body, scale_h=3):
        cv.text(cx, y, kicker, 2, RED)
        y += 24
        y = cv.para(cx, y, col_w, head, scale_h, INK, leading=3)
        y += 8
        y = cv.para(cx, y, col_w, body, 2, INK, leading=3)
        return y + 10

    # column 1: justice + Iran
    yy = story(cxs[0], col_top, "JUSTICE",
               "MYANMAR GUILTY OF GENOCIDE",
               "THE UN'S TOP COURT RULES MYANMAR'S MILITARY LIKELY "
               "INTENDED TO DESTROY A SUBSTANTIAL PART OF THE ROHINGYA "
               "MINORITY.")
    cv.hline(cxs[0], yy, col_w, GREY, 1)
    yy += 12
    yy = story(cxs[0], yy, "WASHINGTON",
               "TRUMP: NO RUSH ON IRAN",
               "THE US PRESIDENT SAYS HE WILL 'SEE WHAT HAPPENS' AFTER "
               "JANUARY 1.")

    # column 2: cyclone, with spiral graphic
    yy = story(cxs[1], col_top, "WEATHER",
               "CYCLONE AKVAN HITS INDIA",
               "300,000 EVACUATED IN ODISHA AS THE SEVERE STORM MAKES "
               "LANDFALL.")
    draw_cyclone(cv, cxs[1] + col_w // 2, yy + 44, 38)
    yy += 96
    cv.text_center(cxs[1] + col_w // 2, yy, "CYCLONE AKVAN", 2, BLUE)
    yy += 20
    cv.hline(cxs[1], yy, col_w, GREY, 1)
    yy += 12
    yy = story(cxs[1], yy, "SPACE",
               "VOYAGER 1 HITS ONE LIGHT-DAY",
               "NASA CONFIRMS THE PROBE IS NOW A FULL DAY'S LIGHT-TRAVEL "
               "FROM HOME.")

    # column 3: markets + Europe talks + globe
    yy = story(cxs[2], col_top, "BUSINESS",
               "ANTHROPIC UP 17% ON DEBUT",
               "SHARES CLOSE SHARPLY HIGHER ON THE FIRST DAY OF TRADING.")
    cv.hline(cxs[2], yy, col_w, GREY, 1)
    yy += 12
    yy = story(cxs[2], yy, "EUROPE",
               "EUROPE READY FOR RUSSIA TALKS",
               "EUROPEAN LEADERS SAY THEY ARE READY TO TALK WITH MOSCOW "
               "ON ENDING THE WAR.")
    yy += 4
    draw_globe(cv, cxs[2] + col_w // 2, yy + 42, 40)

    # column rules
    for vx in (x0 + col_w + 12, x0 + 2 * col_w + 36):
        cv.vline(vx, col_top, 416, GREY, 1)

    # ---- footer strip
    fy = 962
    cv.hline(x0, fy, CW, INK, 2)
    cv.hline(x0, fy + 5, CW, RED, 2)
    cv.text_center(
        W // 2, fy + 16,
        "ALSO TODAY: WORLD CHILDREN'S DAY - VAN GOGH SELLS FOR A RECORD "
        "$190.4M", 2, INK)
    cv.text_center(
        W // 2, fy + 36,
        "GTA 6 SALES PASS $1.8 BILLION - NICHOLLS 113* LEADS NEW ZEALAND",
        2, INK)
    draw_star(cv, x0 + 8, fy + 26, 6, RED)
    draw_star(cv, x1 - 8, fy + 26, 6, RED)
    return cv


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    cv = build()
    path = os.path.join(out_dir, "entry.png")
    size = write_png(cv, path)
    print(f"wrote {path} ({size} bytes, {W}x{H})")


if __name__ == "__main__":
    main()
