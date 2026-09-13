#!/usr/bin/env python3
# Maakt img/favicon.png (512px, ook 32px-versie ingebakken via meerdere maten) en img/og-autosleutel-hengelo.jpg (1200x630).
from PIL import Image, ImageDraw, ImageFont
import pathlib

IMG = pathlib.Path("img")
GROEN, GEEL, BG, INKT = "#1F6B4A", "#F2C94C", "#FBF8F3", "#1B2A24"

def font(maat, vet=True):
    for naam in (["segoeuib.ttf", "arialbd.ttf"] if vet else ["segoeui.ttf", "arial.ttf"]):
        try:
            return ImageFont.truetype("C:/Windows/Fonts/" + naam, maat)
        except OSError:
            pass
    return ImageFont.load_default(maat)

def sleutel(d, x, y, s, kleur):
    # Eenvoudig sleutelicoon: ronde kop + baard, in eenheid s
    d.ellipse((x, y, x + 0.42 * s, y + 0.42 * s), outline=kleur, width=round(0.09 * s))
    d.rounded_rectangle((x + 0.36 * s, y + 0.165 * s, x + s, y + 0.255 * s), radius=round(0.04 * s), fill=kleur)
    d.rectangle((x + 0.78 * s, y + 0.255 * s, x + 0.86 * s, y + 0.40 * s), fill=kleur)
    d.rectangle((x + 0.92 * s, y + 0.255 * s, x + s, y + 0.36 * s), fill=kleur)

# Favicon
fav = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
d = ImageDraw.Draw(fav)
d.rounded_rectangle((0, 0, 511, 511), radius=110, fill=GROEN)
sleutel(d, 70, 165, 372, GEEL)
fav.save(IMG / "favicon.png")
fav.resize((180, 180), Image.LANCZOS).save(IMG / "apple-touch-icon.png")

# OG-afbeelding
og = Image.new("RGB", (1200, 630), BG)
foto = Image.open(IMG / "bmw-x1-smartkey-bijmaken.jpg").convert("RGB")
# rechterhelft: foto 520x630, gecentreerd bijgesneden
r = max(520 / foto.width, 630 / foto.height)
foto = foto.resize((round(foto.width * r), round(foto.height * r)), Image.LANCZOS)
l, t = (foto.width - 520) // 2, (foto.height - 630) // 2
og.paste(foto.crop((l, t, l + 520, t + 630)), (680, 0))
d = ImageDraw.Draw(og)
d.rectangle((0, 0, 14, 630), fill=GEEL)
sleutel(d, 64, 60, 96, GROEN)
d.text((180, 74), "Autosleutel Hengelo", font=font(40), fill=GROEN)
d.text((64, 210), "Autosleutel\nbijmaken", font=font(84), fill=INKT, spacing=6)
d.text((64, 420), "Vanaf € 60  ·  klaar terwijl u wacht\nAan huis in Hengelo vanaf € 45", font=font(32, False), fill=INKT, spacing=12)
d.text((64, 560), "Westendorp · sinds 1985", font=font(26, False), fill=GROEN)
og.save(IMG / "og-autosleutel-hengelo.jpg", "JPEG", quality=88, optimize=True)
print("favicon.png, apple-touch-icon.png en og-autosleutel-hengelo.jpg gemaakt")
