import os
import textwrap
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SIZE = (1080, 1080)
FONT_PATH = os.getenv("FONT_PATH", "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc")

CATEGORY_COLORS = {
    "it": {"primary": "#6c63ff", "dark": "#4b44cc", "gradient_start": "#0f0c29", "gradient_end": "#302b63"},
    "economy": {"primary": "#00b894", "dark": "#007a62", "gradient_start": "#0f2027", "gradient_end": "#203a43"},
}

LABEL = {
    "it": "IT·과학",
    "economy": "경제",
}


def _load_font(size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except Exception:
        return ImageFont.load_default()


def _draw_text_wrapped(draw, text, xy, font, fill, max_width, line_spacing=8):
    x, y = xy
    avg_char_w = font.getlength("가") if hasattr(font, "getlength") else 20
    chars_per_line = max(1, int(max_width / avg_char_w))
    lines = textwrap.wrap(text, width=chars_per_line)
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        bbox = draw.textbbox((x, y), line, font=font)
        y += (bbox[3] - bbox[1]) + line_spacing
    return y


def _draw_gradient_bg(img, color_start: str, color_end: str):
    draw = ImageDraw.Draw(img)
    r1, g1, b1 = int(color_start[1:3], 16), int(color_start[3:5], 16), int(color_start[5:7], 16)
    r2, g2, b2 = int(color_end[1:3], 16), int(color_end[3:5], 16), int(color_end[5:7], 16)
    for y in range(SIZE[1]):
        t = y / SIZE[1]
        r = int(r1 + (r2 - r1) * t)
        g = int(g1 + (g2 - g1) * t)
        b = int(b1 + (b2 - b1) * t)
        draw.line([(0, y), (SIZE[0], y)], fill=(r, g, b))


def _make_cover(article: dict, content: dict, colors: dict, category: str) -> Image.Image:
    img = Image.new("RGB", SIZE)
    _draw_gradient_bg(img, colors["gradient_start"], colors["gradient_end"])
    draw = ImageDraw.Draw(img)

    # Category badge
    badge_font = _load_font(28)
    badge_label = LABEL.get(category, category.upper())
    badge_w = int(badge_font.getlength(badge_label)) + 40
    draw.rounded_rectangle([(60, 80), (60 + badge_w, 80 + 48)], radius=24, fill=colors["primary"])
    draw.text((60 + 20, 88), badge_label, font=badge_font, fill="#ffffff")

    # Decorative accent line
    draw.rectangle([(60, 170), (160, 178)], fill=colors["primary"])

    # Headline
    headline_font = _load_font(68)
    _draw_text_wrapped(draw, content["cover"]["headline"], (60, 200), headline_font, "#ffffff", 960, line_spacing=12)

    # Subtitle
    subtitle_font = _load_font(38)
    _draw_text_wrapped(draw, content["cover"]["subtitle"], (60, 480), subtitle_font, "#ccccee", 960, line_spacing=10)

    # Card indicator
    indicator_font = _load_font(26)
    draw.text((60, 980), "1 / 5", font=indicator_font, fill="#888899")

    # Decorative dots
    for i, x in enumerate(range(900, 1020, 24)):
        alpha = 180 if i == 0 else 80
        draw.ellipse([(x, 980), (x + 12, 992)], fill=(*[int(colors["primary"][j:j+2], 16) for j in (1, 3, 5)], alpha))

    return img


def _make_content_card(card_data: dict, card_num: int, total: int, colors: dict) -> Image.Image:
    img = Image.new("RGB", SIZE, "#f8f9fa")
    draw = ImageDraw.Draw(img)

    # Top accent bar
    draw.rectangle([(0, 0), (SIZE[0], 10)], fill=colors["primary"])

    # Left accent line
    draw.rectangle([(60, 100), (68, 200)], fill=colors["primary"])

    # Card title
    title_font = _load_font(52)
    _draw_text_wrapped(draw, card_data["title"], (90, 110), title_font, "#1a1a2e", 900, line_spacing=10)

    # Bullet points
    bullet_font = _load_font(36)
    y = 300
    for bullet in card_data.get("bullets", []):
        # Bullet dot
        draw.ellipse([(60, y + 14), (76, y + 30)], fill=colors["primary"])
        y = _draw_text_wrapped(draw, bullet, (100, y), bullet_font, "#333344", 900, line_spacing=8)
        y += 30

    # Card indicator
    indicator_font = _load_font(26)
    draw.text((60, 980), f"{card_num} / {total}", font=indicator_font, fill="#aaaaaa")

    # Bottom accent
    draw.rectangle([(0, SIZE[1] - 8), (SIZE[0], SIZE[1])], fill=colors["primary"])

    return img


def _make_closing_card(article: dict, content: dict, colors: dict) -> Image.Image:
    img = Image.new("RGB", SIZE)
    _draw_gradient_bg(img, colors["primary"], colors["dark"])
    draw = ImageDraw.Draw(img)

    # Label
    label_font = _load_font(30)
    draw.text((60, 80), "핵심 요약", font=label_font, fill="#ffffff99")
    draw.rectangle([(60, 128), (200, 134)], fill="#ffffff44")

    # Summary
    summary_font = _load_font(54)
    _draw_text_wrapped(draw, content["closing"]["summary"], (60, 180), summary_font, "#ffffff", 960, line_spacing=12)

    # Takeaway box
    draw.rounded_rectangle([(60, 600), (1020, 760)], radius=16, fill="#ffffff22")
    take_font = _load_font(38)
    _draw_text_wrapped(draw, content["closing"]["takeaway"], (90, 640), take_font, "#ffffff", 880, line_spacing=10)

    # Source
    source_font = _load_font(24)
    draw.text((60, 860), f"출처: {article['link'][:60]}...", font=source_font, fill="#ffffff66")

    # Card indicator
    indicator_font = _load_font(26)
    draw.text((60, 980), "5 / 5", font=indicator_font, fill="#ffffff88")

    return img


class CardMaker:
    def __init__(self, category: str = "it"):
        self.category = category
        self.colors = CATEGORY_COLORS.get(category, CATEGORY_COLORS["it"])

    def create_cards(self, article: dict, content: dict) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = article["title"][:20].replace("/", "_").replace(" ", "_")
        out_dir = Path("output") / f"{timestamp}_{safe_title}"
        out_dir.mkdir(parents=True, exist_ok=True)

        cards = [
            ("01_cover", _make_cover(article, content, self.colors, self.category)),
            ("02_content", _make_content_card(content["cards"][0], 2, 5, self.colors)),
            ("03_content", _make_content_card(content["cards"][1], 3, 5, self.colors)),
            ("04_content", _make_content_card(content["cards"][2], 4, 5, self.colors)),
            ("05_closing", _make_closing_card(article, content, self.colors)),
        ]

        for name, img in cards:
            path = out_dir / f"{name}.png"
            img.save(path, "PNG")
            print(f"  저장: {path}")

        return str(out_dir)
