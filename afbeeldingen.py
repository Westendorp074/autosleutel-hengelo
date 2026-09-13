#!/usr/bin/env python3
# Maakt uit foto-origineel/autosleutel-hengelo-logo.png:
#   img/logo-autosleutel-hengelo.png (transparant, 720 px breed)
#   img/favicon.png (512) + img/apple-touch-icon.png (180) — de groene cirkel met sleutel
#   img/og-autosleutel-hengelo.jpg (1200x630) — logo + tekst + foto
from PIL import Image, ImageDraw, ImageFont
import pathlib

IMG = pathlib.Path("img")
BRON = pathlib.Path("foto-origineel/autosleutel-hengelo-logo.png")
GEEL, BG, INKT, GROEN = "#F2C94C", "#FBF8F3", "#1B2A24", "#1F6B4A"

def font(maat, vet=True):
    for naam in (["segoeuib.ttf", "arialbd.ttf"] if vet else ["segoeui.ttf", "arial.ttf"]):
        try:
            return ImageFont.truetype("C:/Windows/Fonts/" + naam, maat)
        except OSError:
            pass
    return ImageFont.load_default(maat)

# 1. Logo: wit -> transparant, bijsnijden
im = Image.open(BRON).convert("RGBA")
px = im.load()
for y in range(im.height):
    for x in range(im.width):
        r, g, b, a = px[x, y]
        m = min(r, g, b)
        if m > 235:
            px[x, y] = (r, g, b, 0)
        elif m > 200:
            px[x, y] = (r, g, b, int(255 * (235 - m) / 35))
im = im.crop(im.getbbox())
logo = im.resize((720, round(im.height * 720 / im.width)), Image.LANCZOS)
logo.save(IMG / "logo-autosleutel-hengelo.png", optimize=True)

# 2. Favicon: de groene cirkel (positie in het origineel)
c = Image.open(BRON).convert("RGBA").crop((490, 285, 815, 600)).resize((512, 512), Image.LANCZOS)
mask = Image.new("L", (512, 512), 0)
ImageDraw.Draw(mask).ellipse((2, 2, 509, 509), fill=255)
c.putalpha(mask)
c.save(IMG / "favicon.png", optimize=True)
c.resize((180, 180), Image.LANCZOS).save(IMG / "apple-touch-icon.png", optimize=True)

# 3. OG-afbeelding
og = Image.new("RGB", (1200, 630), BG)
foto = Image.open(IMG / "bmw-x1-smartkey-bijmaken.jpg").convert("RGB")
r = max(520 / foto.width, 630 / foto.height)
foto = foto.resize((round(foto.width * r), round(foto.height * r)), Image.LANCZOS)
l, t = (foto.width - 520) // 2, (foto.height - 630) // 2
og.paste(foto.crop((l, t, l + 520, t + 630)), (680, 0))
d = ImageDraw.Draw(og)
d.rectangle((0, 0, 14, 630), fill=GEEL)
lg = logo.resize((440, round(logo.height * 440 / logo.width)), Image.LANCZOS)
og.paste(lg, (64, 56), lg)
d.text((64, 230), "Autosleutel\nbijmaken", font=font(84), fill=INKT, spacing=6)
d.text((64, 440), "Vanaf € 60  ·  klaar terwijl u wacht\nAan huis in Hengelo vanaf € 45", font=font(30, False), fill=INKT, spacing=12)
d.text((64, 570), "Westendorp · sinds 1985", font=font(24, False), fill=GROEN)
og.save(IMG / "og-autosleutel-hengelo.jpg", "JPEG", quality=88, optimize=True)
print("logo, favicon, apple-touch-icon en og-afbeelding gemaakt")
