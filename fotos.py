#!/usr/bin/env python3
# Verkleint de originele foto's uit foto-origineel/ naar img/ (max 1600 px breed, jpg ~82%).
# Bestandsnamen: zet ze in NAMEN (originele naam -> web-naam); onbekende originelen worden gemeld.
import pathlib, sys
from PIL import Image, ImageOps

BRON, DOEL = pathlib.Path("foto-origineel"), pathlib.Path("img")
DOEL.mkdir(exist_ok=True)
MAX_BREED = 1600

# Vul aan zodra de originelen er zijn: "IMG_1234.jpg": "opel-astra-klapsleutel-bijmaken.jpg"
NAMEN = {}

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
