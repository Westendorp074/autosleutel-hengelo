#!/usr/bin/env python3
"""autosleutel-hengelo.nl — statische site-generator.

Opbouw gelijk aan autosleutel-enschede.nl (CONFIG hier, teksten in data-modules), met eigen teksten,
eigen huisstijl en platte URL's (/prijzen, /bmw) met cleanUrls.
Wijzigen = CONFIG of een data-module aanpassen → `python build.py` → commit. HTML nooit met de hand bewerken.
Foto's: leg originelen in foto-origineel/ en draai python fotos.py; build.py gebruikt alleen img/.
"""
import hashlib, html, json, pathlib, re

# ============================================================
# CONFIG
# ============================================================
SITE = "https://autosleutel-hengelo.nl"          # hoofdadres zónder www (www stuurt door)
HANDELSNAAM = "Autosleutel Hengelo"
RECHTSPERSOON = "Westendorp Groep VOF"
VESTIGING = "Oldenzaalsestraat 553, 7558 PW Hengelo"   # KvK-adres VOF (geen winkel)
MOEDER = "Westendorp Sleutel- en Slotenspecialist"
MOEDER_URL = "https://westendorpslotenspecialist.nl/"
STRAAT, POSTCODE, PLAATS = "Wesseler-Nering 32", "7544 JC", "Enschede"
WINKELCENTRUM = "Winkelcentrum Enschede Zuid"
TEL_TONEN, TEL_LINK = "053 478 42 45", "+31534784245"
WA_LINK = "https://wa.me/31534784245"
MAIL = "autosleutel@westendorpgroep.nl"
KVK, BTW = "91885124", "097701993B01"
LAT, LON = 52.1929, 6.8886
SINDS_BEDRIJF, SINDS_AUTOSLEUTELS = 1985, 1995
SINDS = SINDS_BEDRIJF
PER_JAAR = "1.500"
DOORLOOPTIJD = "20 tot 30 minuten"
AAN_HUIS_VANAF = "45"
REISTIJD = "15 minuten"
GBP_LINK = "https://share.google/j46orGZulGyU4amTy"   # Google-bedrijfsprofiel Autosleutel Hengelo (deellink)
REVIEW_LINK = "https://g.page/r/CakJOOdkl5gzEAE/review"   # "Vraag om reviews"-link uit het Hengelo-profiel
ROUTE_LINK = "https://maps.app.goo.gl/1DX8q4eZJTdBvAbd8"   # Maps-vermelding werkplaats Enschede
GBP_SCORE, GBP_AANTAL = "", 0   # invullen zodra er reviews zijn; leeg = nergens een score of reviewblok
WEB3FORMS_KEY = "a64f80df-574c-43c9-b15c-f67332fd1a3f"   # eigen key voor deze site (web3forms.com, 13-9-2026)
PRIVACY_DATUM = "15 september 2026"
MAANDEN = ["januari", "februari", "maart", "april", "mei", "juni", "juli", "augustus", "september", "oktober", "november", "december"]

# ---------- Meten: Google Analytics 4 ----------
# Leeg of "G-XXXX" = geen tag, geen cookiemelding en de privacytekst zegt dat er niet gemeten wordt.
GA_ID = "G-60VCGF9LL1"                        # property "Autosleutel Hengelo" (aangemaakt 16-09-2026)
MEET_ACTIEF = GA_ID.startswith("G-") and "XXXX" not in GA_ID
TAG_HEAD = (f"""<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('consent','default',{{'ad_storage':'denied','ad_user_data':'denied','ad_personalization':'denied','analytics_storage':'denied','wait_for_update':500}});</script>
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script><script>gtag('js',new Date());gtag('config','{GA_ID}');</script>""") if MEET_ACTIEF else ""
COOKIE_HTML = """<div class="cookie" id="cookiebalk" hidden>
  <div class="cookie__venster" role="dialog" aria-modal="true" aria-labelledby="cookie-titel">
    <div class="cookie__kop"><img src="/img/logo-autosleutel-hengelo.png" alt="Autosleutel Hengelo" width="720" height="240"></div>
    <div class="cookie__tabs" role="tablist">
      <button type="button" role="tab" aria-selected="true" data-tab="toestemming">Toestemming</button>
      <button type="button" role="tab" aria-selected="false" data-tab="details">Details</button>
      <button type="button" role="tab" aria-selected="false" data-tab="over">Over</button>
    </div>
    <div class="cookie__inhoud">
      <div data-paneel="toestemming">
        <p class="cookie__titel" id="cookie-titel">Autosleutel Hengelo maakt gebruik van cookies</p>
        <p>Onze website gebruikt cookies en vergelijkbare technieken. Zo werkt de website goed en kunnen wij hem blijven verbeteren. Via Aanpassen kiest u zelf welke cookies u toestaat. Meer informatie leest u in onze <a href="/privacy">privacyverklaring</a>.</p>
      </div>
      <div data-paneel="details" hidden>
        <div class="cookie__rij">
          <div><strong>Noodzakelijk</strong><p>Nodig om de website goed te laten werken en uw keuze te onthouden.</p></div>
          <span class="cookie__altijd">Altijd aan</span>
        </div>
        <div class="cookie__rij">
          <div><strong>Statistieken</strong><p>Cookies van Google waarmee wij kunnen zien hoe bezoekers onze website gebruiken.</p></div>
          <label class="schakel"><input type="checkbox" id="cookie-ads" aria-label="Statistieken"><span></span></label>
        </div>
      </div>
      <div data-paneel="over" hidden>
        <p>Cookies zijn kleine tekstbestanden die een website op uw computer of telefoon opslaat. Wij verkopen geen gegevens aan anderen. Uw keuze kunt u altijd wijzigen via &quot;Cookie-instellingen&quot; onderaan de pagina.</p>
        <p>Autosleutel Hengelo is onderdeel van Westendorp Sleutel- en Slotenspecialist. Meer over cookies en persoonsgegevens leest u in onze <a href="/privacy">privacyverklaring</a>.</p>
      </div>
    </div>
    <div class="cookie__knoppen" id="cookie-knoppen">
      <button type="button" class="cookie__knop cookie__knop--licht" data-consent="denied" hidden>Weigeren</button>
      <button type="button" class="cookie__knop cookie__knop--licht" data-cookie="aanpassen">Aanpassen</button>
      <button type="button" class="cookie__knop" data-consent="granted">Alle cookies toestaan</button>
    </div>
  </div>
</div>""" if MEET_ACTIEF else ""

OPENING = [("Maandag", "gesloten"), ("Dinsdag", "09:00 – 17:30"), ("Woensdag", "09:00 – 17:30"),
           ("Donderdag", "09:00 – 17:30"), ("Vrijdag", "09:00 – 17:30"),
           ("Zaterdag", "09:00 – 17:00"), ("Zondag", "gesloten")]

# Werkgebied: de Hengelo-kant van Twente. Almelo e.o. is autosleutel-almelo.nl, Enschede zelf autosleutel-enschede.nl.
PLAATSEN = ["Hengelo", "Borne", "Delden", "Goor", "Haaksbergen", "Oldenzaal", "Losser",
            "Denekamp", "Weerselo", "Hengevelde", "Beckum", "Deurningen"]

# Prijzen: altijd "vanaf". Exacte prijs volgt op kenteken. Alle sleutels kwijt: nooit een prijs noemen.
P_TRANS, P_KLAP, P_KAART, P_SMART, P_REP = "60", "130", "130", "150", "30"
P_BEHUIZING_VAST, P_BEHUIZING_KLAP = "35", "49,95"
P_PINCODE = "35"          # Peugeot/Citroën tot ongeveer 2005
P_UP = "129"              # VW Up, Škoda Citigo, Seat Mii
P_BMW_NIEUW = "249"       # kopie originele BMW-sleutel 2019 en nieuwer
GARANTIE_CHIP, GARANTIE_AB = "levenslange garantie", "2 jaar"
MERCEDES_REGEL = "Mercedes-Benz personenwagens vanaf 2015 maken wij niet; de Sprinter W906 tot en met 2017 wel."

# Schattingen (opgave eigenaar 14-09-2026): alleen tonen in blokken die als "schatting" gelabeld zijn.
SCHATTING = {
    "transpondersleutel-bijmaken": ("€ 60 – € 120",  "€ 150 of meer"),
    "klapsleutel-bijmaken":        ("€ 130 – € 200", "€ 400 – € 700"),
    "smartkey-bijmaken":           ("€ 150 – € 300", "€ 400 – € 1.500"),
    "sleutelkaart-bijmaken":       ("€ 130 – € 250", "€ 400 – € 700"),
    "autosleutel-reparatie":       ("€ 30 – € 80",   "nieuwe sleutel vanaf € 400"),
}

OUT = pathlib.Path(__file__).parent
IMG = OUT / "img"

from data_typen import SLEUTELTYPEN
from data_merken import MERKEN, OVERIGE_MERKEN
from data_kennis import KENNIS, KENNIS_FOTO

# ============================================================
# Hulpfuncties
# ============================================================
def versie(bestand):
    p = OUT / bestand
    return hashlib.md5(p.read_bytes()).hexdigest()[:8] if p.exists() else "0"

CSS_V, JS_V = versie("styles.css"), versie("site.js")
TEL_HTML = html.escape(TEL_TONEN)

_ICONEN = {
    "ster": '<path d="M12 3.5l2.6 5.4 5.9.8-4.3 4.1 1.1 5.9L12 16.9l-5.3 2.8 1.1-5.9-4.3-4.1 5.9-.8z"/>',
    "klap": '<rect x="8" y="11" width="8" height="10" rx="3"/><path d="M10.5 15h3M10.5 18h3"/><circle cx="12" cy="11" r="1.1" fill="currentColor" stroke="none"/><path d="M12 11l7-7"/><path d="M15.5 7.5l1.4 1.4M17.5 5.5l1.4 1.4"/>',
    "smart": '<rect x="7" y="3" width="10" height="18" rx="4"/><circle cx="12" cy="9" r="1.5"/><path d="M10 14h4M10 17h4"/>',
    "kaart": '<rect x="3" y="6" width="18" height="12" rx="2.5"/><path d="M7 10h4M7 14h6"/><circle cx="17" cy="12" r="1.5"/>',
    "chip": '<circle cx="7.5" cy="12" r="3.8"/><circle cx="7.5" cy="12" r="1" fill="currentColor" stroke="none"/><path d="M11.3 12H21M17.5 12v3.2M20 12v2.4"/>',
    "winkel": '<path d="M4 10.5 5.2 6h13.6L20 10.5"/><path d="M4 10.5a2.7 2.7 0 0 0 5.3 0 2.7 2.7 0 0 0 5.4 0 2.7 2.7 0 0 0 5.3 0"/><path d="M5.5 12.8V20h13v-7.2"/><path d="M10 20v-4.5h4V20"/>',
    "rep": '<path d="M14.5 5.5a3.5 3.5 0 0 0-4.7 4.3L4 15.6 8.4 20l5.8-5.8a3.5 3.5 0 0 0 4.3-4.7l-2.3 2.3-2.2-.6-.6-2.2 2.1-2.3z"/>',
    "tel": '<path d="M5 4h4l1.5 4-2 1.5a11 11 0 0 0 5 5l1.5-2 4 1.5v4a1.5 1.5 0 0 1-1.6 1.5C10.9 20 4 13.1 4 5.6A1.5 1.5 0 0 1 5 4z"/>',
    "wa": '<path d="M4 20l1.3-4A7.5 7.5 0 1 1 8 18.7L4 20z"/><path d="M9 9.5c0 3 2.5 5.5 5.5 5.5.6 0 1-.5 1-1l-.2-1.2-1.6-.6-.8.9c-1-.4-1.8-1.2-2.2-2.2l.9-.8-.6-1.6L9.8 8c-.5 0-1 .4-1 1z"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3.5 6.5 12 13l8.5-6.5"/>',
    "pin": '<path d="M12 21s7-6.3 7-11a7 7 0 1 0-14 0c0 4.7 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>',
    "klok": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    "huis": '<path d="M3 11 12 4l9 7"/><path d="M5 10v10h14V10"/><path d="M9 20v-6h6v6"/>',
    "auto": '<path d="M3 13l2-5h14l2 5v5H3z"/><circle cx="7.5" cy="16" r="1.5"/><circle cx="16.5" cy="16" r="1.5"/><path d="M5 13h14"/>',
    "kenteken": '<rect x="3" y="6" width="18" height="12" rx="2"/><path d="M7 10h2M11 10h6M7 14h4M13 14h4"/>',
    "vink": '<circle cx="12" cy="12" r="8.5"/><path d="M8.5 12.2l2.4 2.4 4.6-4.8"/>',
    "route": '<path d="M7.5 3.5 3 5.2v15l4.5-1.7 9 3.3 4.5-1.7v-15l-4.5 1.7-9-3.3z"/><path d="M7.5 3.5v15M16.5 6.8v15"/>',
    "schild": '<path d="M12 3l7 3v5c0 4.5-3 7.8-7 9-4-1.2-7-4.5-7-9V6z"/><path d="M9 12l2 2 4-4"/>',
    "kalender": '<rect x="4" y="5" width="16" height="15" rx="2"/><path d="M4 9h16M8 3v4M16 3v4"/>',
    "sleutels": '<circle cx="8" cy="8" r="3"/><path d="M10.5 10.5 20 20M16 16l2-2M18 18l2-2"/>',
    "parkeren": '<rect x="3.5" y="3.5" width="17" height="17" rx="3"/><path d="M9.5 16.5V8h3.2a2.6 2.6 0 0 1 0 5.2H9.5"/>',
    "pijl": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "kwijt": '<circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/><path d="M9 11h4"/>',
}
def icoon(naam, klas="ic"):
    return (f'<svg class="{klas}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{_ICONEN[naam]}</svg>')

def foto(bestand, alt, klas="", breed=None, hoog=None, lazy=True):
    """Toont de foto als hij in img/ staat; anders een nette plekhouder, zodat de build nooit breekt."""
    if (IMG / bestand).exists():
        lz = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
        b, h = breed or 1200, hoog or 900
        try:
            from PIL import Image
            with Image.open(IMG / bestand) as im:
                if not breed: b, h = im.size
                # Staande foto's (sleutel onderin, auto erboven): uitsnede lager, sleutel volledig in beeld.
                if im.height > im.width:
                    klas = (klas + " is-staand").strip()
        except Exception:
            pass
        return f'<img class="{klas}" src="/img/{bestand}" alt="{html.escape(alt)}" width="{b}" height="{h}"{lz}>'
    return f'<div class="foto-plek {klas}" role="img" aria-label="{html.escape(alt)}"><span>foto volgt</span></div>'

def prijs(v): return f"vanaf € {v}"
def typeprijs(t): return globals()[t["prijs"]]

# ---------- JSON-LD ----------
def bedrijf_jsonld():
    d = {
        "@context": "https://schema.org", "@type": "AutomotiveBusiness", "@id": SITE + "/#bedrijf",
        "name": HANDELSNAAM, "url": SITE, "telephone": TEL_LINK, "email": MAIL, "priceRange": "€€",
        "logo": SITE + "/img/logo-autosleutel-hengelo.png", "image": SITE + "/img/og-autosleutel-hengelo.jpg",
        "foundingDate": str(SINDS_BEDRIJF),
        "parentOrganization": {"@type": "Organization", "name": RECHTSPERSOON, "url": MOEDER_URL},
        "sameAs": [MOEDER_URL] + ([GBP_LINK] if GBP_LINK else []),
        "address": {"@type": "PostalAddress", "streetAddress": STRAAT, "postalCode": POSTCODE,
                    "addressLocality": PLAATS, "addressRegion": "Overijssel", "addressCountry": "NL"},
        "geo": {"@type": "GeoCoordinates", "latitude": LAT, "longitude": LON},
        "areaServed": [{"@type": "City", "name": p} for p in PLAATSEN],
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": d, "opens": "09:00", "closes": c}
            for d, c in [("Tuesday", "17:30"), ("Wednesday", "17:30"), ("Thursday", "17:30"),
                         ("Friday", "17:30"), ("Saturday", "17:00")]],
        "makesOffer": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": t["kop"]},
                        "description": t["kort"]} for t in SLEUTELTYPEN] +
                      [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Aan-huisservice Hengelo"},
                        "description": f"Autosleutel bijmaken op locatie, vanaf € {AAN_HUIS_VANAF} bovenop de sleutelprijs."}],
    }
    if GBP_SCORE and GBP_AANTAL:
        d["aggregateRating"] = {"@type": "AggregateRating", "ratingValue": GBP_SCORE.replace(",", "."), "reviewCount": GBP_AANTAL}
    return d

def _schoon(t): return re.sub(r"<[^>]+>", "", t)
def faq_jsonld(items):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": _schoon(v), "acceptedAnswer": {"@type": "Answer", "text": _schoon(a)}} for v, a in items]}

def kruimels_jsonld(paden):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p}
                                for i, (n, p) in enumerate(paden)]}

def artikel_jsonld(titel, pad, omschr, datum, beeld=None):
    d = {"@context": "https://schema.org", "@type": "Article", "headline": titel, "description": omschr,
         "url": SITE + pad, "datePublished": datum, "dateModified": datum, "inLanguage": "nl-NL",
         "author": {"@type": "Organization", "name": HANDELSNAAM},
         "publisher": {"@type": "Organization", "name": RECHTSPERSOON}}
    if beeld: d["image"] = SITE + "/img/" + beeld
    return d

# ============================================================
# Componenten
# ============================================================
def kruimels(items):
    li = "".join(f'<a href="{p}">{n}</a><span>›</span>' if p else f"<b>{n}</b>" for n, p in items)
    return f'<nav class="wrap kruimels" aria-label="Kruimelpad">{li}</nav>'

def antwoord(tekst):
    return f'<div class="antwoord"><p>{tekst}</p></div>'

def knoppen(primair=None, tweede="Prijs via kenteken", tweede_href="#kenteken", tweede_icoon="kenteken", midden=False):
    primair = primair or f'Bel <span class="tel-nr">{TEL_HTML}</span>'
    return (f'<div class="knoppen{" knoppen--midden" if midden else ""}"><a class="knop knop--vol" href="tel:{TEL_LINK}" data-conv="bellen">{icoon("tel")}{primair}</a>'
            f'<a class="knop knop--rand" href="{tweede_href}">{icoon(tweede_icoon)}{tweede}</a></div>')

def faqblok(items, kop="Veelgestelde vragen"):
    d = "".join(f"<details><summary>{v}</summary><p>{a}</p></details>" for v, a in items)
    return f'<section class="sectie sectie--kort"><div class="wrap wrap--tekst"><h2>{kop}</h2><div class="faq">{d}</div></div></section>'

def cta(tekst="Wilt u weten wat uw sleutel kost? Stuur uw kenteken; u hoort het dezelfde werkdag."):
    return f"""
<section class="cta"><div class="wrap cta__in">
  <p>{icoon("kenteken")}<span>{tekst}</span></p>
  <div class="knoppen"><a class="knop knop--vol" href="#kenteken">{icoon("kenteken")}Stuur uw kenteken</a><a class="knop knop--rand" href="{WA_LINK}" rel="noopener" data-conv="whatsapp">{icoon("wa")}WhatsApp</a></div>
</div></section>"""

def situaties():
    items = [
        ("sleutels", "Reserve autosleutel", "Eén werkende sleutel over? Wij maken er een tweede naast, geprogrammeerd op uw auto.", "/autosleutel-bijmaken", "vanaf € 60<small>afhankelijk van uw sleuteltype</small>"),
        ("rep", "Sleutel kapot", "Behuizing gebroken, knopjes dood of de baard klapt niet meer uit: de chip gaat mee, de rest wordt nieuw.", "/autosleutel-reparatie", "vanaf € 30<small>afhankelijk van de reparatie</small>"),
        ("kwijt", "Alle sleutels kwijt", "Een nieuwe sleutel op basis van uw kenteken; de verloren sleutels werken daarna niet meer.", "/autosleutel-kwijt", "prijs op aanvraag<small>vooraf via uw kenteken</small>"),
    ]
    k = "".join(f'<a class="situatie" href="{h}">{icoon(i, "ic ic--groot")}<h3>{t}</h3><p>{o}</p><span class="situatie__prijs">{p}</span></a>' for i, t, o, h, p in items)
    return f"""
<section class="sectie" id="situaties">
  <div class="wrap">
    <div class="sectie__kop"><h2>Wat is er met uw sleutel?</h2><p>Kies wat bij u past. U leest wat wij doen, wat u meeneemt en waar u ongeveer op uitkomt. Met meer dan {PER_JAAR} autosleutels per jaar is de kans klein dat wij de uwe nog niet eerder hebben gezien.</p></div>
    <div class="situaties">{k}</div>
  </div>
</section>"""

def kiezer(titel="Welke sleutel heeft u?", intro=None, zand=False):
    intro = intro or "Kies het type dat op uw sleutel lijkt. U ziet de vanaf-prijs en leest wat wij ermee kunnen. Geen idee welk type het is? Uw kenteken zegt het ons."
    kaarten = "".join(
        f'<a class="kies" href="/{t["slug"]}">{icoon(t["icoon"], "ic ic--groot")}<h3>{t["naam"]}</h3>'
        f'<p>{t["kort"]}</p><span class="kies__prijs">{"vanaf € " + {"transpondersleutel-bijmaken": "60", "klapsleutel-bijmaken": "130", "smartkey-bijmaken": "150", "sleutelkaart-bijmaken": "130", "autosleutel-reparatie": "30"}[t["slug"]]}<small>{"afhankelijk van de reparatie" if t["slug"] == "autosleutel-reparatie" else "afhankelijk van merk en bouwjaar"}</small></span></a>'
        for t in SLEUTELTYPEN)
    return f"""
<section class="sectie{" sectie--zand" if zand else ""}" id="sleuteltypen">
  <div class="wrap">
    <div class="sectie__kop"><h2>{titel}</h2><p>{intro}</p></div>
    <div class="kiezer">{kaarten}</div>
  </div>
</section>"""

def vertrouwen():
    return f"""
<div class="wrap vertrouwen">
  <div>{icoon("kenteken")}<b>Tot 50%</b><span>goedkoper dan de dealer, prijs vooraf op uw kenteken</span></div>
  <div>{icoon("klok")}<b>20 tot 30 minuten</b><span>klaar terwijl u wacht</span></div>
  <div>{icoon("kalender")}<b>Sinds {SINDS_AUTOSLEUTELS}</b><span>autosleutels bij Westendorp, bedrijf sinds {SINDS_BEDRIJF}</span></div>
  <div>{icoon("sleutels")}<b>{PER_JAAR}+</b><span>autosleutels per jaar</span></div>
</div>"""

def prijstabel():
    rijen = "".join(
        f'<tr><th scope="row"><a href="/{t["slug"]}">{t["naam"]}</a><small>{t["kort"]}</small></th>'
        f'<td>{SCHATTING[t["slug"]][0]}</td><td class="dealer">{SCHATTING[t["slug"]][1]}</td>'
        f'<td>{"prijs op aanvraag" if t["slug"] != "autosleutel-reparatie" else "—"}</td></tr>' for t in SLEUTELTYPEN)
    rijen += (f'<tr><th scope="row"><a href="/aan-huis">Aan huis in Hengelo</a><small>bovenop de sleutelprijs</small></th>'
              f'<td colspan="3">vanaf € {AAN_HUIS_VANAF}</td></tr>')
    return f"""
<div class="tabel-scroll"><table class="prijstabel">
  <caption><b>Schatting</b>, geen offerte. Zo ongeveer valt het bij ons en bij de dealer uit. Wat u werkelijk betaalt, hangt af van merk, model en bouwjaar; die prijs krijgt u vooraf op uw kenteken.</caption>
  <thead><tr><th scope="col">Sleuteltype</th><th scope="col">Bij ons (schatting)</th><th scope="col">Bij de dealer (schatting)</th><th scope="col">Alle sleutels kwijt</th></tr></thead>
  <tbody>{rijen}</tbody>
</table></div>
<p class="noot">Onze bedragen zijn inclusief programmeren, frezen en btw; de dealerbedragen horen wij doorgaans van klanten. Wij programmeren in de software van uw auto, net als de dealer, en werken ook met dealers samen. Zijn alle sleutels kwijt, dan loopt de prijs per auto te ver uiteen om hier te noemen.</p>"""

def uitzonderingen():
    return f"""
<h2>Uitzonderingen per merk</h2>
<ul class="lijst">
  <li><b>Jongere bouwjaren</b>: nieuwere auto's hebben een zwaarder beveiligde chip, en dat ziet u terug in de prijs. Het bouwjaar lezen wij uit uw kenteken, dus u weet het vooraf.</li>
  <li><b>Volkswagen, Audi, Seat en Škoda</b>: de prijs kan per model afwijken van de vanaf-prijs. VW Up, Škoda Citigo en Seat Mii: {prijs(P_UP)}.</li>
  <li><b>BMW en Mini</b>: prijs op aanvraag per model. Kopie van een originele BMW-sleutel van 2019 of nieuwer: {prijs(P_BMW_NIEUW)}.</li>
  <li><b>Mercedes-Benz</b> personenwagens vanaf 2015 maken wij niet; de Sprinter W906 tot en met 2017 wel.</li>
  <li><b>Peugeot en Citroën tot ongeveer 2005</b>: de auto vraagt om de pincode uit de autopapieren. Kwijt? Wij vragen hem op, {prijs(P_PINCODE)}.</li>
  <li><b>Twee sleutels in één keer</b>: korting op de tweede sleutel, in overleg.</li>
  <li><b>Alle sleutels kwijt</b>: prijs op aanvraag, vooraf via uw kenteken.</li>
  <li><b>Reparatie</b>: nieuwe behuizing voor een vaste sleutel {prijs(P_BEHUIZING_VAST)}, voor een klapsleutel {prijs(P_BEHUIZING_KLAP)}. Printplaat- of soldeerwerk: prijs na een foto via WhatsApp.</li>
  <li><b>Aan huis</b>: in Hengelo {prijs(AAN_HUIS_VANAF)} bovenop de sleutelprijs; daarbuiten een kilometervergoeding, die in de prijsopgave staat.</li>
</ul>"""

def dealerblok():
    return f"""
<section class="sectie sectie--zand">
  <div class="wrap media">
    <div>
      <h2>Wij of de dealer</h2>
      <p>De dealer bestelt uw sleutel bij de fabriek. Daar zit doorgaans twee tot zes weken tussen, en daarna betaalt u ook nog werkplaatsuren. Wij hebben behuizingen, chips en afstandsbedieningen op voorraad en programmeren zelf. Zo bent u tot 50% goedkoper dan de dealer, en u rijdt dezelfde dag met de nieuwe sleutel.</p>
      <ul class="vinkjes">
        <li>{icoon("vink")}Meestal klaar terwijl u wacht, in {DOORLOOPTIJD}</li>
        <li>{icoon("vink")}Prijs vooraf, op basis van uw kenteken</li>
        <li>{icoon("vink")}Levenslange garantie op de transponderchip, {GARANTIE_AB} op een nieuwe afstandsbediening</li>
        <li>{icoon("vink")}Wat niet kan, zeggen wij vooraf: {MERCEDES_REGEL}</li>
      </ul>
    </div>
    <figure class="media__foto">{foto("werkplaats-voorraad-autosleutel-behuizingen.jpg", "Voorraadkasten met autosleutelbehuizingen en chips per merk in de werkplaats")}<figcaption>Voorraad per merk in de werkplaats</figcaption></figure>
  </div>
</section>"""

def moederblok():
    return f"""
<section class="sectie">
  <div class="wrap moederkaart">
    <div class="moederkaart__logo"><a href="{MOEDER_URL}" rel="noopener"><img src="/img/logo-westendorp.png" alt="{MOEDER}" width="360" height="108" loading="lazy"></a></div>
    <div>
      <h2>Onderdeel van {MOEDER}</h2>
      <p>{HANDELSNAAM} is de autosleuteldienst van Westendorp. Het familiebedrijf bestaat sinds {SINDS_BEDRIJF} en maakt sinds {SINDS_AUTOSLEUTELS} autosleutels, tegenwoordig meer dan {PER_JAAR} per jaar. De werkplaats zit in {WINKELCENTRUM}, op {REISTIJD} rijden van Hengelo. Daar maakt de specialist die u spreekt ook zelf uw sleutel.</p>
      <p class="tekstlink"><a href="/over-ons">{icoon("pijl")}Over ons</a> <a href="{MOEDER_URL}" rel="noopener">{icoon("pijl")}Naar westendorpslotenspecialist.nl</a></p>
    </div>
  </div>
</section>"""

def werkgebiedblok(wit=False):
    return f"""
<section class="sectie{"" if wit else " sectie--zand"}">
  <div class="wrap werkgebied">
    <div>
      <h2>Voor Hengelo en omgeving</h2>
      <p>U komt naar de werkplaats in Enschede Zuid, via de A35 zo'n {REISTIJD} vanaf Hengelo. Kan dat niet, dan komen wij aan huis: in Hengelo {prijs(AAN_HUIS_VANAF)} bovenop de sleutelprijs, in de plaatsen hieronder met een kilometervergoeding die u vooraf hoort.</p>
      <ul class="plaatsen">{"".join(f"<li>{p}</li>" for p in PLAATSEN)}</ul>
      <p class="noot">Uw plaats staat er niet bij? Bel even; in de werkplaats bent u altijd welkom.</p>
    </div>
    <div class="adreskaart">
      {foto("werkplaats-autosleutel-reparatie-werkbank.jpg", "Sleutelspecialist aan de werkbank in de werkplaats van Westendorp in Enschede", klas="adreskaart__foto")}
      <div class="adreskaart__in">
        <h3>Werkplaats {MOEDER}</h3>
        <ul class="feiten feiten--kolom">
          <li>{icoon("pin")}<span><b>Adres</b>{STRAAT}, {POSTCODE} {PLAATS}<br>{WINKELCENTRUM}</span></li>
          <li>{icoon("parkeren")}<span><b>Parkeren</b>Gratis, bij het overdekte winkelcentrum</span></li>
          <li>{icoon("klok")}<span><b>Openingstijden</b>di – vr 09:00 – 17:30 · za 09:00 – 17:00<br>maandag en zondag gesloten</span></li>
        </ul>
        <div class="knoppen"><a class="knop knop--vol" href="{ROUTE_LINK}" rel="noopener" data-conv="route">{icoon("route")}Routebeschrijving</a><a class="knop knop--rand" href="{WA_LINK}" rel="noopener" data-conv="whatsapp">{icoon("wa")}WhatsApp</a></div>
      </div>
    </div>
  </div>
</section>"""

def formulier(bron):
    # Velden, volgorde, key en redirect gelijk aan het bestaande Hengelo-formulier (13-9-2026).
    return f"""
<section class="sectie sectie--zand" id="kenteken">
  <div class="wrap">
    <div class="blok blok--form">
    <div class="sectie__kop">
      <h2>Vraag uw prijs aan</h2>
      <p>Vul uw kenteken in en u hoort dezelfde werkdag wat uw sleutel kost en wanneer u terecht kunt, of wanneer wij bij u kunnen zijn. Liever direct antwoord? <a href="tel:{TEL_LINK}" data-conv="bellen">Bel {TEL_HTML}</a> of stuur een <a href="{WA_LINK}" rel="noopener" data-conv="whatsapp">WhatsApp</a>.</p>
    </div>
    <form action="https://api.web3forms.com/submit" method="POST" class="form" data-key="{WEB3FORMS_KEY}">
      <input type="hidden" name="access_key" value="{WEB3FORMS_KEY}">
      <input type="hidden" name="subject" value="via autosleutel-hengelo.nl">
      <input type="hidden" name="from_name" value="{HANDELSNAAM}">
      <input type="hidden" name="redirect" value="{SITE}/bedankt">
      <input type="hidden" name="Pagina" value="{bron}">
      <input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off">
      <div class="veld veld--kenteken"><label for="kenteken-veld">Kenteken</label>
        <div class="kentekenveld"><span class="kenteken__nl">NL</span><input id="kenteken-veld" name="Kenteken" required placeholder="XX-123-X" autocomplete="off" maxlength="9" aria-describedby="f-kenteken-check"></div>
        <div class="kentekencheck" id="f-kenteken-check" aria-live="polite" hidden></div>
        <small>Hiermee zien wij direct welke sleutel u nodig heeft. <button type="button" class="linkknop" id="f-geen-kenteken">Kenteken niet bij de hand?</button></small>
        <input type="hidden" name="Auto volgens RDW" id="f-voertuig" value=""></div>
      <div class="veld autovelden" id="f-autovelden" hidden>
        <p class="autovelden__kop">Vul dan merk, model en bouwjaar in</p>
        <div class="autovelden__grid">
          <div class="veld"><label for="f-merk">Merk</label><input id="f-merk" name="Merk" placeholder="Bijv. Volkswagen"></div>
          <div class="veld"><label for="f-model">Model</label><input id="f-model" name="Model" placeholder="Bijv. Polo"></div>
          <div class="veld"><label for="f-bouwjaar">Bouwjaar</label><input id="f-bouwjaar" name="Bouwjaar" inputmode="numeric" placeholder="Bijv. 2016" maxlength="4"></div>
        </div>
      </div>
      <div class="veld veld--vol"><label for="f-onderwerp">Waarvoor komt u?</label>
        <select id="f-onderwerp" name="Onderwerp" required><option>Autosleutel bijmaken</option><option>Autosleutel repareren</option></select></div>
      <div class="veldgroep" data-voor="Autosleutel bijmaken">
        <div class="veld"><label for="f-start">Hoe start uw auto?</label>
          <select id="f-start" name="Hoe start de auto" required><option value="">Maak een keuze</option><option>Sleutel in het contact of dashboard</option><option>Keyless (start-stopknop)</option><option>Weet ik niet</option></select></div>
          <div class="veld"><label for="f-situatie">Wat is de situatie?</label>
          <select id="f-situatie" name="Situatie" required><option value="">Maak een keuze</option><option>Reserve autosleutel, ik heb nog een werkende sleutel</option><option>Alle sleutels kwijt</option></select></div>
      </div>
      <div class="veldgroep" data-voor="Autosleutel repareren" hidden>
        <div class="veld veld--vol"><label for="f-reparatie">Wat is er kapot?</label>
          <select id="f-reparatie" name="Wat is er kapot"><option value="">Maak een keuze</option><option>Autosleutel behuizing (gebroken, versleten, klapt niet meer uit)</option><option>Printplaat reparatie (knopjes doen niets, elektronica, waterschade)</option><option>Allebei</option><option>Weet ik niet</option></select>
          <small>Twijfelt u? Kies "Weet ik niet" en stuur een foto van de sleutel via WhatsApp.</small></div>
      </div>
      <div class="veld"><label for="naam">Naam</label><input id="naam" name="Naam" required autocomplete="name"></div>
      <div class="veld"><label for="tel">Telefoon <small>(niet verplicht)</small></label><input id="tel" name="Telefoon" type="tel" autocomplete="tel"></div>
      <div class="veld"><label for="mail">E-mail</label><input id="mail" name="email" type="email" required autocomplete="email"></div>
      <div class="veld veld--vol"><label for="opm">Opmerkingen</label>
        <textarea id="opm" name="Opmerkingen" placeholder="Bijvoorbeeld: ik ben alle sleutels kwijt, de knopjes werken niet meer, of ik wil graag aan huis geholpen worden."></textarea></div>
      <div class="veld veld--vol">
        <p class="form-uit" hidden>Het aanvraagformulier is nog niet actief. Bel <a href="tel:{TEL_LINK}" data-conv="bellen">{TEL_HTML}</a> of stuur een <a href="{WA_LINK}" rel="noopener" data-conv="whatsapp">WhatsApp-bericht</a>, dan heeft u meteen antwoord.</p>
        <button class="knop knop--geel" type="submit" data-conv="formulier">Vraag mijn prijs aan</button>
        <small>Wij gebruiken uw gegevens alleen om uw aanvraag te beantwoorden. <a href="/privacy">Privacyverklaring</a>.</small>
      </div>
    </form>
    </div>
  </div>
</section>"""

# ============================================================
# Pagina-omhulsel
# ============================================================
NAV = [("/autosleutel-bijmaken", "Sleutel bijmaken"), ("/autosleutel-kwijt", "Sleutel kwijt"), ("/prijzen", "Prijzen"),
       ("/aan-huis", "Aan huis"), ("/merken", "Merken"), ("/kennis", "Kennis"), ("/over-ons", "Over ons"), ("/contact", "Contact")]
LENGTE_FOUTEN = []
PAGINAS = []   # (pad, noindex)

def kop_html(titel, omschrijving, pad, jsonld, beeld=None, noindex=False):
    if len(titel) > 62: LENGTE_FOUTEN.append(f"titel {len(titel)} > 62: {pad} | {titel}")
    if len(omschrijving) > 160: LENGTE_FOUTEN.append(f"description {len(omschrijving)} > 160: {pad}")
    canon = SITE + pad
    robots = "noindex,follow" if noindex else "index,follow,max-image-preview:large"
    blokken = [bedrijf_jsonld()] + list(jsonld)
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(b, ensure_ascii=False, separators=(",", ":"))}</script>' for b in blokken)
    og = f"{SITE}/img/{beeld}" if beeld and (IMG / beeld).exists() else f"{SITE}/img/og-autosleutel-hengelo.jpg"
    nav = "".join(f'<a href="{h}">{n}</a>' for h, n in NAV)
    return f"""<!DOCTYPE html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(titel)}</title>
<meta name="description" content="{html.escape(omschrijving)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:locale" content="nl_NL">
<meta property="og:title" content="{html.escape(titel)}">
<meta property="og:description" content="{html.escape(omschrijving)}">
<meta property="og:url" content="{canon}">
<meta property="og:site_name" content="{HANDELSNAAM}">
<meta property="og:image" content="{og}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;700;800&family=Nunito+Sans:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/styles.css?v={CSS_V}">
<link rel="icon" href="/img/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
{ld}
{TAG_HEAD}
</head>
<body>
<a class="skip" href="#inhoud">Naar de inhoud</a>
<header class="top">
  <div class="wrap top__in">
    <a class="top__merk" href="/" aria-label="{HANDELSNAAM}, naar de homepage"><img src="/img/logo-autosleutel-hengelo.png" alt="{HANDELSNAAM}" width="720" height="184" decoding="async"></a>
    <nav class="top__nav" aria-label="Hoofdmenu">{nav}</nav>
    <div class="top__acties">
      <a class="top__wa" href="{WA_LINK}" rel="noopener" data-conv="whatsapp" aria-label="WhatsApp">{icoon("wa")}</a>
      <a class="top__tel" href="tel:{TEL_LINK}" data-conv="bellen" aria-label="Bel {TEL_TONEN}">{icoon("tel")}<span>{TEL_HTML}</span></a>
      <button class="top__menu" type="button" aria-expanded="false" aria-controls="mobielmenu" aria-label="Menu"><span></span><span></span><span></span></button>
    </div>
  </div>
  <nav class="mobielmenu" id="mobielmenu" hidden aria-label="Menu">{nav}</nav>
</header>
<main id="inhoud">
"""

VOET = f"""
</main>
<footer class="voet">
  <div class="wrap voet__grid">
    <div>
      <div class="voet__kop">{HANDELSNAAM}</div>
      <p>Autosleutels bijmaken, programmeren en repareren voor Hengelo en omgeving, in de werkplaats of aan huis. Onderdeel van <a href="{MOEDER_URL}" rel="noopener">{MOEDER}</a> ({RECHTSPERSOON}), sinds {SINDS_BEDRIJF}.</p>
      <p>KvK {KVK} · btw {BTW}</p>
    </div>
    <div>
      <div class="voet__kop">Werkplaats</div>
      <p>{STRAAT}<br>{POSTCODE} {PLAATS}<br>{WINKELCENTRUM}, gratis parkeren</p>
      <p><a href="{ROUTE_LINK}" rel="noopener" data-conv="route">{icoon("route")}Routebeschrijving</a></p>
    </div>
    <div>
      <div class="voet__kop">Open</div>
      <p>{'<br>'.join(f"{d}: {t}" for d, t in OPENING)}</p>
    </div>
    <div>
      <div class="voet__kop">Contact</div>
      <ul class="voet__lijst">
        <li><a href="tel:{TEL_LINK}" data-conv="bellen">{icoon("tel")}{TEL_HTML}</a></li>
        <li><a href="{WA_LINK}" rel="noopener" data-conv="whatsapp">{icoon("wa")}WhatsApp</a></li>
        <li><a href="mailto:{MAIL}">{icoon("mail")}{MAIL}</a></li>
        <li><a href="{REVIEW_LINK}" rel="noopener" data-conv="review">{icoon("ster")}Geef ons een Google-review</a></li>
      </ul>
      <ul class="voet__lijst voet__lijst--klein">
        <li><a href="/prijzen">Prijzen</a></li><li><a href="/aan-huis">Aan huis</a></li><li><a href="/merken">Merken</a></li>
        <li><a href="/kennis">Kennis</a></li><li><a href="/over-ons">Over ons</a></li><li><a href="/contact">Contact</a></li><li><a href="/privacy">Privacy</a></li>{'<li><button type="button" class="voet__cookie" data-cookie="open">Cookie-instellingen</button></li>' if MEET_ACTIEF else ''}
      </ul>
    </div>
  </div>
  <p class="wrap voet__onder">© 2026 {RECHTSPERSOON}. Merknamen zijn eigendom van de fabrikanten en staan hier alleen om aan te geven voor welke auto's wij sleutels maken.</p>
</footer>
<div class="belbalk is-verborgen">
  <a class="belbalk__bel" href="tel:{TEL_LINK}" data-conv="bellen" aria-label="Bel {TEL_TONEN}">{icoon("tel")}Bel</a>
  <a class="belbalk__wa" href="{WA_LINK}" rel="noopener" data-conv="whatsapp">{icoon("wa")}WhatsApp</a>
</div>
{COOKIE_HTML}
<script src="/site.js?v={JS_V}" defer></script>
</body>
</html>
"""


# Lange samenstellingen in koppen: zachte afbreking (&shy;), zodat een smalle kaart of telefoon
# nooit midden in een woord afbreekt. Alleen binnen <h1>-<h3>; zichtbaar pas als het nodig is.
import re as _re_afbreek
_AFBREEK = {"Transpondersleutels": "Transponder&shy;sleutels", "Transpondersleutel": "Transponder&shy;sleutel",
            "transpondersleutels": "transponder&shy;sleutels", "transpondersleutel": "transponder&shy;sleutel",
            "Afstandsbediening": "Afstands&shy;bediening", "afstandsbediening": "afstands&shy;bediening",
            "Privacyverklaring": "Privacy&shy;verklaring", "Reserveautosleutel": "Reserve&shy;autosleutel",
            "Sleutelkaarten": "Sleutel&shy;kaarten", "Sleutelkaart": "Sleutel&shy;kaart",
            "autosleutelprijzen": "autosleutel&shy;prijzen", "Autosleutelprijzen": "Autosleutel&shy;prijzen",
            "startonderbreker": "start&shy;onderbreker", "Winkelcentrum": "Winkel&shy;centrum"}
def afbreken(doc):
    def kop(m):
        s = m.group(0)
        for a, b in _AFBREEK.items():
            s = _re_afbreek.sub(r"(?<![\w/-])" + a + r"(?![\w-])", b, s)
        return s
    doc = _re_afbreek.sub(r"(?s)<h([1-3])\b[^>]*>.*?</h\1>", kop, doc)
    return _re_afbreek.sub(r'(?s)<a class="kies kies--klein"[^>]*>.*?</a>', kop, doc)

def pagina(pad, titel, omschrijving, body, jsonld=(), beeld=None, noindex=False):
    bestand = "index.html" if pad == "/" else pad.strip("/") + ".html"
    (OUT / bestand).write_text(afbreken(kop_html(titel, omschrijving, pad, jsonld, beeld, noindex) + body + VOET), encoding="utf-8")
    PAGINAS.append((pad, noindex))

# ============================================================
# PAGINA'S
# ============================================================
from data_paginas import bouw_paginas
bouw_paginas(globals())

# ============================================================
# 404, sitemap, robots, llms.txt
# ============================================================
(OUT / "404.html").write_text(kop_html(f"Pagina niet gevonden | {HANDELSNAAM}", "Deze pagina bestaat niet (meer). Kies uw situatie of bel ons.", "/404", [], noindex=True) + f"""
<section class="sectie sectie--kort"><div class="wrap wrap--tekst">
  <p class="kentekenbord"><span class="kenteken__nl">NL</span><span>404</span></p>
  <h1>Deze pagina bestaat niet</h1>
  <p>De link is verouderd of er zit een tikfout in. Kies hieronder wat er met uw sleutel is, of bel ons; dan bent u het snelst geholpen.</p>
  {knoppen(tweede="Naar de homepage", tweede_href="/", tweede_icoon="pijl")}
</div></section>
{situaties()}
""" + VOET, encoding="utf-8")

indexeerbaar = [p for p, ni in PAGINAS if not ni]
urls = "".join(f"<url><loc>{SITE}{p}</loc><changefreq>monthly</changefreq><priority>{'1.0' if p == '/' else '0.7'}</priority></url>" for p in indexeerbaar)
(OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>', encoding="utf-8")
(OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /bedankt\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
(OUT / "llms.txt").write_text(f"""# {HANDELSNAAM}

Autosleutelservice voor Hengelo en omgeving ({", ".join(PLAATSEN)}). Onderdeel van {MOEDER} ({RECHTSPERSOON}, KvK {KVK}), {MOEDER_URL}
Werkplaats: {STRAAT}, {POSTCODE} {PLAATS} ({WINKELCENTRUM}), {REISTIJD} vanaf Hengelo via de A35, gratis parkeren.

## Feiten
- Telefoon {TEL_TONEN}, WhatsApp wa.me/31534784245, e-mail {MAIL}. Open di–vr 09:00–17:30, za 09:00–17:00, ma en zo gesloten.
- Bedrijf sinds {SINDS_BEDRIJF}, autosleutels sinds {SINDS_AUTOSLEUTELS}, meer dan {PER_JAAR} autosleutels per jaar.
- Maakt, programmeert en repareert transpondersleutels, klapsleutels, smartkeys (keyless), sleutelkaarten voor vrijwel elk merk.
- Vanaf-prijzen incl. programmeren en btw: transpondersleutel vanaf € {P_TRANS}; klapsleutel vanaf € {P_KLAP}; sleutelkaart vanaf € {P_KAART}; smartkey vanaf € {P_SMART}; reparatie vanaf € {P_REP}. Exacte prijs vooraf op kenteken.
- Reparatie: nieuwe behuizing vaste sleutel vanaf € {P_BEHUIZING_VAST}, klapsleutel vanaf € {P_BEHUIZING_KLAP}.
- Uitzonderingen: VW Up/Škoda Citigo/Seat Mii vanaf € {P_UP}; BMW/Mini prijs op aanvraag (kopie originele BMW-sleutel 2019 en nieuwer vanaf € {P_BMW_NIEUW}); {MERCEDES_REGEL} Peugeot/Citroën tot ongeveer 2005 pincode nodig (opvragen vanaf € {P_PINCODE}); twee sleutels tegelijk: korting op de tweede, in overleg.
- Alle sleutels kwijt: nieuwe sleutel op kenteken, oude sleutels worden gewist; prijs op aanvraag.
- Aan-huisservice in Hengelo vanaf € {AAN_HUIS_VANAF} bovenop de sleutelprijs; buiten Hengelo kilometervergoeding in de prijsopgave.
- Meestal klaar terwijl u wacht in {DOORLOOPTIJD}. Tot 50% goedkoper dan de dealer; de dealer doet er doorgaans twee tot zes weken over.
- Programmeren in de software van de auto, net als de dealer; Westendorp werkt ook met dealers samen.
- Garantie: {GARANTIE_CHIP} op de transponderchip, {GARANTIE_AB} op een nieuwe afstandsbediening.
- Schatting bij ons / bij de dealer (geen offerte): transpondersleutel € 60 – € 120 / € 150 of meer; klapsleutel € 130 – € 200 / € 400 – € 700; smartkey € 150 – € 300 / € 400 – € 1.500; sleutelkaart € 130 – € 250 / € 400 – € 700; reparatie € 30 – € 80 / nieuwe sleutel vanaf € 400.
- Benodigd: kenteken (voor de prijs), kentekenbewijs en identiteitsbewijs (bij het maken).

## Pagina's
{chr(10).join(f"- {SITE}{p}" for p in indexeerbaar)}
""", encoding="utf-8")

for f in LENGTE_FOUTEN: print("LENGTE:", f)
print(f"Gebouwd: {len(PAGINAS) + 1} pagina's ({len(indexeerbaar)} indexeerbaar)")
