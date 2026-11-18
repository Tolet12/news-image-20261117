"""Draw the 17 November 2026 world-news front page as entry.png.

Original flat-shape newspaper collage, drawn entirely with Pillow
primitives (rectangles, polygons, ellipses, lines and text).
No randomness: every run produces byte-identical output.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024

PAPER = (247, 242, 231)
INK = (20, 16, 12)
WHITE = (255, 255, 255)
SKY = (176, 216, 235)
SKY2 = (203, 232, 245)
SEA = (38, 110, 168)
SEA_DARK = (24, 84, 136)
GREY = (110, 110, 110)
SMOKE = (138, 138, 138)
SMOKE_DARK = (95, 95, 95)
FIRE = (242, 110, 20)
FIRE_Y = (250, 190, 30)
RED = (198, 32, 40)
SHIP_HULL = (35, 35, 40)
DECK = (90, 90, 98)
TABLE = (110, 72, 40)
WALL = (222, 208, 178)

SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(draw, text, path, start, max_width, min_size=14):
    size = start
    while size > min_size:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_width:
            return f
        size -= 1
    return font(path, min_size)


def centered(draw, cx, y, text, f, fill=INK):
    w = draw.textlength(text, font=f)
    draw.text((cx - w / 2, y), text, font=f, fill=fill)
    return f.size


def wrap_text(draw, text, f, max_width):
    words = text.split()
    lines = []
    cur = ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=f) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def smoke(draw, cx, cy, r):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SMOKE)
    draw.ellipse([cx - r - 14, cy - r // 2, cx + r // 2, cy + r // 2], fill=SMOKE_DARK)
    draw.ellipse([cx, cy - r - 10, cx + r + 16, cy + r // 3], fill=SMOKE)


def flame(draw, cx, base_y, w, h):
    draw.polygon(
        [(cx - w // 2, base_y), (cx, base_y - h), (cx + w // 2, base_y)],
        fill=FIRE,
    )
    inner_w = max(8, w // 2)
    inner_h = max(10, int(h * 0.6))
    draw.polygon(
        [(cx - inner_w // 2, base_y), (cx, base_y - inner_h), (cx + inner_w // 2, base_y)],
        fill=FIRE_Y,
    )


def figure(draw, cx, top_y, suit):
    # Head.
    draw.ellipse([cx - 17, top_y, cx + 17, top_y + 34], fill=(232, 190, 150), outline=INK, width=2)
    # Body: bold trapezoid suit with a white shirt triangle and tie.
    draw.polygon(
        [(cx - 34, top_y + 92), (cx - 22, top_y + 36), (cx + 22, top_y + 36), (cx + 34, top_y + 92)],
        fill=suit, outline=INK, width=2,
    )
    draw.polygon(
        [(cx - 9, top_y + 36), (cx + 9, top_y + 36), (cx, top_y + 62)],
        fill=WHITE,
    )


def flag_us(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=WHITE, outline=INK, width=2)
    stripe = h / 7
    for i in range(7):
        if i % 2 == 0:
            draw.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe], fill=RED)
    draw.rectangle([x, y, x + w * 0.45, y + stripe * 4], fill=(40, 60, 140))
    for r in range(3):
        for c in range(4):
            sx = x + 6 + c * 11
            sy = y + 5 + r * 10
            draw.ellipse([sx, sy, sx + 4, sy + 4], fill=WHITE)


def flag_china(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 30, 40), outline=INK, width=2)
    for (dx, dy, r) in [(12, 10, 7), (30, 6, 3), (36, 16, 3), (30, 26, 3), (24, 34, 3)]:
        draw.ellipse([x + dx - r, y + dy - r, x + dx + r, y + dy + r], fill=FIRE_Y)


def flag_russia(draw, x, y, w, h):
    third = h / 3
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    draw.rectangle([x, y, x + w, y + third], fill=WHITE)
    draw.rectangle([x, y + third, x + w, y + 2 * third], fill=(30, 70, 170))
    draw.rectangle([x, y + 2 * third, x + w, y + h], fill=RED)


def scene_bridge(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=SKY2)
    water_y = y0 + 150
    draw.rectangle([x0, water_y, x1, y1], fill=SEA)
    for wy in (water_y + 26, water_y + 58, water_y + 88):
        for wx in range(x0 + 18, x1 - 50, 92):
            draw.line([wx, wy, wx + 44, wy], fill=SEA_DARK, width=4)
    deck_y = y0 + 96
    # Towers.
    for tx in (x0 + 92, x1 - 122):
        draw.rectangle([tx, y0 + 34, tx + 30, water_y + 8], fill=DECK, outline=INK, width=3)
    # Standing spans.
    draw.rectangle([x0 + 6, deck_y, x0 + 200, deck_y + 16], fill=DECK, outline=INK, width=3)
    draw.rectangle([x1 - 206, deck_y, x1 - 6, deck_y + 16], fill=DECK, outline=INK, width=3)
    # Cables.
    draw.line([x0 + 107, y0 + 36, x0 + 30, deck_y], fill=INK, width=3)
    draw.line([x1 - 107, y0 + 36, x1 - 30, deck_y], fill=INK, width=3)
    # Collapsed middle span, tilted steeply down into the water.
    draw.polygon(
        [(x0 + 196, deck_y + 2), (x1 - 202, deck_y + 78),
         (x1 - 202, deck_y + 102), (x0 + 196, deck_y + 26)],
        fill=(70, 70, 78), outline=INK, width=3,
    )
    draw.line([x0 + 240, deck_y + 16, x0 + 252, water_y + 34], fill=INK, width=4)
    draw.line([x1 - 250, deck_y + 84, x1 - 238, water_y + 30], fill=INK, width=4)
    # Strike flash where the span broke.
    flame(draw, x0 + 208, deck_y + 6, 40, 44)
    # Splash where the span meets the water.
    draw.polygon(
        [(x0 + 222, water_y + 4), (x0 + 250, water_y - 16), (x0 + 278, water_y + 4)],
        fill=WHITE,
    )
    # Smoke plumes.
    smoke(draw, x0 + 150, y0 + 40, 26)
    smoke(draw, x1 - 160, y0 + 34, 22)


def scene_hormuz(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=SKY)
    sea_y = y0 + 138
    draw.rectangle([x0, sea_y, x1, y1], fill=SEA)
    for wy in (sea_y + 30, sea_y + 66, sea_y + 96):
        for wx in range(x0 + 24, x1 - 50, 104):
            draw.line([wx, wy, wx + 48, wy], fill=SEA_DARK, width=4)
    # Aircraft carrier silhouette behind the tanker, island on its left.
    cx0, cy = x0 + 84, y0 + 100
    draw.polygon(
        [(cx0, cy + 22), (cx0 + 26, cy), (cx0 + 290, cy), (cx0 + 316, cy + 22),
         (cx0 + 298, cy + 34), (cx0 + 18, cy + 34)],
        fill=(88, 94, 104), outline=INK, width=2,
    )
    draw.rectangle([cx0 + 52, cy - 34, cx0 + 82, cy], fill=(88, 94, 104), outline=INK, width=2)
    draw.line([cx0 + 67, cy - 34, cx0 + 67, cy - 56], fill=INK, width=3)
    # Tanker in front, on fire.
    tx, ty = x0 + 52, y0 + 168
    draw.polygon(
        [(tx, ty), (tx + 330, ty), (tx + 306, ty + 34), (tx + 26, ty + 34)],
        fill=SHIP_HULL, outline=INK, width=3,
    )
    draw.rectangle([tx, ty - 8, tx + 330, ty], fill=RED)
    draw.rectangle([tx + 36, ty - 34, tx + 92, ty - 8], fill=DECK, outline=INK, width=2)
    for px in (150, 205, 260):
        draw.rectangle([tx + px, ty - 22, tx + px + 30, ty - 8], fill=(150, 150, 158), outline=INK, width=2)
    flame(draw, tx + 200, ty - 20, 64, 74)
    flame(draw, tx + 262, ty - 20, 44, 52)
    smoke(draw, tx + 208, y0 + 62, 26)
    smoke(draw, tx + 282, y0 + 84, 18)
    # Mine markers in the water.
    for (mx, my) in [(x0 + 66, y1 - 34), (x1 - 76, y1 - 52)]:
        draw.ellipse([mx - 13, my - 13, mx + 13, my + 13], fill=INK)
        draw.line([mx - 20, my, mx + 20, my], fill=INK, width=4)
        draw.line([mx, my - 20, mx, my + 20], fill=INK, width=4)


def scene_summit(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=WALL)
    draw.rectangle([x0, y1 - 46, x1, y1], fill=(150, 110, 70))
    # Flags on poles behind the table.
    pole_top = y0 + 22
    flag_specs = [(x0 + 66, flag_us), (x0 + 196, flag_china), (x0 + 326, flag_russia)]
    for fx, painter in flag_specs:
        draw.line([fx, pole_top + 58, fx, y0 + 168], fill=INK, width=4)
        painter(draw, fx + 4, pole_top, 96, 58)
    # Long summit table.
    table_y = y0 + 196
    draw.polygon(
        [(x0 + 52, table_y), (x1 - 52, table_y), (x1 - 26, table_y + 44), (x0 + 26, table_y + 44)],
        fill=TABLE, outline=INK, width=3,
    )
    draw.rectangle([x0 + 120, table_y + 44, x0 + 138, table_y + 56], fill=(80, 52, 26))
    draw.rectangle([x1 - 138, table_y + 44, x1 - 120, table_y + 56], fill=(80, 52, 26))
    # Papers and glasses on the table.
    for px in (x0 + 120, x0 + 226, x0 + 332):
        draw.rectangle([px, table_y + 12, px + 44, table_y + 30], fill=WHITE, outline=INK, width=2)
    # Three seated leaders.
    figure(draw, x0 + 118, y0 + 108, (30, 40, 90))
    figure(draw, x0 + 240, y0 + 108, (150, 28, 34))
    figure(draw, x1 - 118, y0 + 108, (52, 52, 58))


def scene_rocket(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(28, 44, 92))
    # Stars.
    for (sx, sy) in [(40, 30), (120, 70), (210, 24), (330, 56), (420, 30),
                     (70, 130), (400, 130), (180, 96), (300, 110), (440, 90)]:
        px, py = x0 + sx, y0 + sy
        draw.line([px - 5, py, px + 5, py], fill=WHITE, width=2)
        draw.line([px, py - 5, px, py + 5], fill=WHITE, width=2)
    cx, cy = x0 + 238, y0 + 118
    # Explosion starburst behind the break-up point.
    spikes = [
        (cx, cy - 84), (cx + 22, cy - 30), (cx + 80, cy - 52), (cx + 34, cy - 8),
        (cx + 88, cy + 26), (cx + 28, cy + 30), (cx + 52, cy + 78), (cx + 6, cy + 38),
        (cx - 30, cy + 72), (cx - 24, cy + 26), (cx - 84, cy + 40), (cx - 36, cy - 2),
        (cx - 80, cy - 46), (cx - 22, cy - 28),
    ]
    draw.polygon(spikes, fill=FIRE)
    draw.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], fill=FIRE_Y, outline=INK, width=2)
    # Nose cone flying up-left, trailing smoke.
    smoke(draw, cx - 52, cy - 52, 13)
    draw.polygon(
        [(cx - 138, cy - 104), (cx - 58, cy - 132), (cx - 82, cy - 52)],
        fill=WHITE, outline=INK, width=3,
    )
    draw.rectangle([cx - 116, cy - 76, cx - 88, cy - 60], fill=RED)
    # Broken mid-body fragment tumbling left of the burst.
    draw.polygon(
        [(cx - 128, cy + 34), (cx - 76, cy + 18), (cx - 64, cy + 52), (cx - 116, cy + 68)],
        fill=(205, 205, 212), outline=INK, width=3,
    )
    draw.rectangle([cx - 104, cy + 30, cx - 92, cy + 58], fill=RED)
    # Lower booster tumbling down-right.
    draw.polygon(
        [(cx + 58, cy + 52), (cx + 108, cy + 76), (cx + 88, cy + 118), (cx + 40, cy + 94)],
        fill=(205, 205, 212), outline=INK, width=3,
    )
    flame(draw, cx + 96, cy + 128, 30, 30)
    # Tumbling satellite rectangles with solar panels.
    for (sx, sy, ang) in [(x0 + 92, y0 + 196, 0), (x0 + 330, y0 + 186, 1), (x0 + 216, y0 + 222, 0)]:
        draw.rectangle([sx - 44, sy - 9, sx - 14, sy + 9], fill=(50, 90, 180), outline=INK, width=2)
        draw.rectangle([sx - 14, sy - 13, sx + 14, sy + 13], fill=(170, 170, 178), outline=INK, width=2)
        draw.rectangle([sx + 14, sy - 9, sx + 44, sy + 9], fill=(50, 90, 180), outline=INK, width=2)
        if ang:
            draw.line([sx - 30, sy + 22, sx + 30, sy + 34], fill=FIRE_Y, width=3)
    # Debris dots.
    for (dx, dy) in [(-70, 40), (60, -50), (110, 10), (-40, 90), (30, 110)]:
        draw.ellipse([cx + dx - 5, cy + dy - 5, cx + dx + 5, cy + dy + 5], fill=(200, 200, 205))


def panel(draw, box, scene_fn, headline, subline):
    x0, y0, x1, y1 = box
    cap_h = 96
    scene_box = (x0, y0, x1, y1 - cap_h)
    # Clip scene drawing to the scene box by drawing, then restoring borders.
    scene_fn(draw, scene_box)
    draw.rectangle(scene_box, outline=INK, width=4)
    # Caption bar.
    cap_y = y1 - cap_h
    draw.rectangle([x0, cap_y, x1, y1], fill=PAPER, outline=INK, width=4)
    cx = (x0 + x1) // 2
    hf = fit_font(draw, headline, SANS_BOLD, 31, (x1 - x0) - 20)
    centered(draw, cx, cap_y + 10, headline, hf)
    sf = fit_font(draw, subline, SANS_BOLD, 20, (x1 - x0) - 20)
    centered(draw, cx, cap_y + 52, subline, sf, fill=(70, 60, 48))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    draw.line([24, 18, W - 24, 18], fill=INK, width=5)
    draw.line([24, 28, W - 24, 28], fill=INK, width=2)
    title = "THE WORLD IN ONE DAY"
    tf = fit_font(draw, title, SERIF_BOLD, 66, W - 48)
    centered(draw, W // 2, 36, title, tf)
    sub = "TUESDAY \u00b7 17 NOVEMBER 2026 \u00b7 THE DAY IN ONE PICTURE"
    sf = fit_font(draw, sub, SANS_BOLD, 24, W - 80)
    centered(draw, W // 2, 112, sub, sf)
    draw.line([24, 146, W - 24, 146], fill=INK, width=2)
    draw.line([24, 152, W - 24, 152], fill=INK, width=5)

    # ---- 2x2 panel grid --------------------------------------------------
    gx, gy, gap = 24, 168, 16
    pw = (W - 2 * gx - gap) // 2
    ph = 352
    panels = [
        ((gx, gy, gx + pw, gy + ph), scene_bridge,
         "CRIMEAN BRIDGE DOWN", "UKRAINE STRIKE \u2014 KYIV HIT IN RETURN"),
        ((gx + pw + gap, gy, gx + 2 * pw + gap, gy + ph), scene_hormuz,
         "HORMUZ: TANKERS HIT MINES", "THIRD US CARRIER ARRIVES"),
        ((gx, gy + ph + gap, gx + pw, gy + 2 * ph + gap), scene_summit,
         "TRUMP IN MANILA", "XI & PUTIN SUMMIT NEXT \u2014 SHENZHEN"),
        ((gx + pw + gap, gy + ph + gap, gx + 2 * pw + gap, gy + 2 * ph + gap), scene_rocket,
         "VULCAN ROCKET LOST", "40 AMAZON LEO SATELLITES GONE"),
    ]
    for box, scene_fn, headline, subline in panels:
        panel(draw, box, scene_fn, headline, subline)

    # ---- Bottom ticker ---------------------------------------------------
    tick_y = gy + 2 * ph + gap + 16
    draw.rectangle([0, tick_y, W, H], fill=INK)
    ticker = (
        "JPMORGAN: SOFTWARE BUG CAUSED BANK OUTAGE \u2022 NVIDIA POSTS FIRST "
        "EARNINGS SINCE HUANG EXIT \u2022 ESTONIA TO CLOSE RUSSIA BORDER DEC 1"
    )
    tf2 = font(SANS_BOLD, 25)
    lines = wrap_text(draw, ticker, tf2, W - 56)
    while len(lines) > 2 and tf2.size > 16:
        tf2 = font(SANS_BOLD, tf2.size - 1)
        lines = wrap_text(draw, ticker, tf2, W - 56)
    line_h = tf2.size + 12
    total_h = len(lines) * line_h
    ly = tick_y + ((H - tick_y) - total_h) // 2
    for line in lines:
        centered(draw, W // 2, ly, line, tf2, fill=PAPER)
        ly += line_h

    out = Path(__file__).resolve().parent / "entry.png"
    img.save(out, format="PNG", optimize=False)
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
