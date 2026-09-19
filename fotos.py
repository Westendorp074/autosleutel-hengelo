#!/usr/bin/env python3
# Verkleint de originele foto's uit foto-origineel/ naar img/ (max 1600 px breed, jpg ~82%).
# Bestandsnamen: zet ze in NAMEN (originele naam -> web-naam); onbekende originelen worden gemeld.
import pathlib, sys
from PIL import Image, ImageOps

BRON, DOEL = pathlib.Path("foto-origineel"), pathlib.Path("img")
DOEL.mkdir(exist_ok=True)
MAX_BREED = 1600

# Vul aan zodra de originelen er zijn: "IMG_1234.jpg": "opel-astra-klapsleutel-hengelo.jpg"
NAMEN = {
    "IMG_3024-1024x683.jpg": "hyundai-autosleutel-programmeren-hengelo.jpg",
    "IMG_3319.JPEG": "opel-astra-klapsleutel-hengelo.jpg",
    "IMG_3477.JPEG": "citroen-c4-picasso-smartkey-hengelo.jpg",
    "IMG_3757.JPEG": "renault-kadjar-sleutelkaart-hengelo.jpg",
    "IMG_3762.JPEG": "fiat-500-klapsleutel-hengelo.jpg",
    "IMG_3861.JPEG": "ford-mustang-autosleutel-hengelo.jpg",
    "IMG_4050.JPEG": "bmw-x1-smartkey-hengelo.jpg",
    "IMG_4502.JPEG": "mini-clubman-smartkey-hengelo.jpg",
    "IMG_4562.JPEG": "jaguar-xf-smartkey-hengelo.jpg",
    "IMG_4611.JPEG": "jeep-compass-smartkey-hengelo.jpg",
    "IMG_6150.JPEG": "werkplaats-reparatie-werkbank-hengelo.jpg",
    "IMG_6169.JPEG": "werkplaats-voorraad-behuizingen-hengelo.jpg",
}

def verwerk(pad, naam):
    im = ImageOps.exif_transpose(Image.open(pad)).convert("RGB")
    if im.width > MAX_BREED:
        im = im.resize((MAX_BREED, round(im.height * MAX_BREED / im.width)), Image.LANCZOS)
    im.save(DOEL / naam, "JPEG", quality=82, optimize=True, progressive=True)
    print(f"{pad.name} -> img/{naam} ({im.width}x{im.height})")

if not BRON.exists():
    sys.exit("Map foto-origineel/ ontbreekt.")
for pad in sorted(BRON.iterdir()):
    if pad.suffix.lower() not in (".jpg", ".jpeg", ".png", ".webp", ".heic"):
        continue
    naam = NAMEN.get(pad.name) or (pad.stem.lower().replace(" ", "-") + ".jpg")
    verwerk(pad, naam)
