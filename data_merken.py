# Merkpagina's: opbouw zoals autosleutel-enschede.nl (antwoord + foto, sleuteltypen per periode, prijsblok, extra,
# modellenlijst, stappen, cta, faq, formulier), teksten en URL's eigen voor Hengelo (/bmw, /merken, /overige-merken).
import html, unicodedata
from data_merken_1 import MERKEN_1
from data_merken_2 import MERKEN_2

def _sorteer(naam):   # alfabetisch zonder hoofdletters of accenten: Dacia vóór DS, Škoda bij de S
    return "".join(c for c in unicodedata.normalize("NFD", naam) if not unicodedata.combining(c)).casefold()

MERKEN = sorted(MERKEN_1 + MERKEN_2, key=lambda m: _sorteer(m["naam"]))

OVERIGE_MERKEN = ['Abarth', 'Bentley', 'BYD', 'Cadillac', 'Chevrolet', 'Chrysler', 'Cupra', 'Daewoo', 'Daihatsu', 'Ferrari', 'Infiniti', 'Isuzu', 'Lamborghini', 'Lancia', 'Lotus', 'Lynk & Co', 'Maserati', 'MG', 'Polestar', 'Rover', 'Saab', 'SsangYong', 'Subaru', 'Tesla']

FALLBACK_FOTO = [("werkplaats-reparatie-werkbank-hengelo.jpg", "Sleutelspecialist programmeert een autosleutel aan de werkbank in de werkplaats in Enschede", "De werkbank in onze werkplaats in Enschede Zuid"),
                 ("werkplaats-voorraad-behuizingen-hengelo.jpg", "Sleutelspecialist bij de voorraadkasten met sleutels en behuizingen per merk", "Sleutels en behuizingen per merk op voorraad")]

def _vanaf(g, m):
    r = m["prijsregel"]
    if r in ("bmw", "aanvraag"): return "prijs op aanvraag"
    if r == "mercedes": return "tot en met 2014"
    return f"vanaf € {g['P_TRANS']}"

def _prijsblok(g, m):
    r, naam = m["prijsregel"], m["naam"]
    aanhuis = f"Aan huis in Hengelo komt daar vanaf € {g['AAN_HUIS_VANAF']} bij; buiten Hengelo een kilometervergoeding, die in de prijsopgave staat."
    if r == "bmw":
        return f"""<div class="prijs-kaart"><div><small>Alle {naam}-sleutels</small><b>prijs op aanvraag</b><span>per model en generatie, vooraf op uw kenteken</span></div>
      {f'<div><small>Kopie originele BMW-sleutel 2019 en nieuwer</small><b>vanaf € {g["P_BMW_NIEUW"]}</b><span>nieuwste generatie</span></div>' if naam == "BMW" else ""}
      <div><small>Reparatie</small><b>vanaf € {g['P_REP']}</b><span>uw chip en zender blijven</span></div></div>
    <p class="noot">{aanhuis}</p>"""
    if r == "aanvraag":
        return f"""<div class="prijs-kaart"><div><small>{naam}-kaart of keyfob</small><b>prijs op aanvraag</b><span>per model, vooraf op uw kenteken</span></div></div>"""
    if r == "mercedes":
        return f"""<div class="prijs-kaart"><div><small>Personenwagens tot en met 2014</small><b>prijs vooraf</b><span>op basis van uw kenteken</span></div>
      <div><small>Sprinter W906</small><b>tot en met 2017</b><span>maken wij ook</span></div>
      <div><small>Personenwagens vanaf 2015</small><b>maken wij niet</b><span>daarvoor verwijzen wij naar de dealer</span></div></div>
    <p class="noot">{aanhuis}</p>"""
    extra = ""
    if r == "vag": extra = f"Bij {naam} kan de prijs per model afwijken van de vanaf-prijs. "
    if r == "psa": extra = f"Tot ongeveer 2005 is de pincode uit de autopapieren nodig; opvragen kost vanaf € {g['P_PINCODE']}. "
    return f"""<div class="prijs-kaart">
      <div><small>Transpondersleutel</small><b>vanaf € {g['P_TRANS']}</b><span>chip in de kop, met of zonder knopjes</span></div>
      <div><small>Klapsleutel of sleutelkaart</small><b>vanaf € {g['P_KLAP']}</b><span>met afstandsbediening</span></div>
      <div><small>Smartkey / keyless</small><b>vanaf € {g['P_SMART']}</b><span>startknop in de auto</span></div>
    </div>
    <p class="noot">Inclusief programmeren, frezen en btw; jongere bouwjaren zijn duurder. {extra}Alle sleutels kwijt: prijs op aanvraag. {aanhuis}</p>"""

def merkpagina(g, m, i):
    pagina, icoon, foto, antwoord, knoppen, faqblok, formulier, kruimels, cta = (g[k] for k in ("pagina", "icoon", "foto", "antwoord", "knoppen", "faqblok", "formulier", "kruimels", "cta"))
    faq_jsonld, kruimels_jsonld, SLEUTELTYPEN = g["faq_jsonld"], g["kruimels_jsonld"], g["SLEUTELTYPEN"]
    naam, slug = m["naam"], m["slug"]
    pad = "/" + slug
    vanaf = _vanaf(g, m)
    titel = f"{naam} autosleutel bijmaken Hengelo | {vanaf}"
    vanaf_zin = "personenwagens tot en met 2014" if m["prijsregel"] == "mercedes" else vanaf
    vraag = f"{naam}-sleutel kwijt of kapot?" if m["prijsregel"] == "mercedes" else f"{naam}-sleutel kwijt, kapot of een reserve nodig?"
    omschr = f"{vraag} Bijmaken en programmeren voor Hengelo, {vanaf_zin}. Werkplaats op {g['REISTIJD']} of aan huis."
    if len(omschr) > 160: omschr = f"{naam}-sleutel kwijt, kapot of reserve nodig? Bijmaken en programmeren voor Hengelo, {vanaf_zin}, of aan huis."
    typen = "".join(f"<li><b>{p}</b>{t}</li>" for p, t in m["typen"])
    extra = "".join(f"<h2>{k}</h2><p>{a}</p>" for k, a in m["extra"])
    modellen = "".join(f"<li>{html.escape(x)}</li>" for x in m["modellen"])
    f = m["foto"] or FALLBACK_FOTO[i % 2]
    fig = f'<figure class="figuur">{foto(f[0], f[1], lazy=False)}<figcaption>{f[2]}</figcaption></figure>'
    typelinks = "".join(f'<a class="kies kies--klein" href="/{t["slug"]}">{icoon(t["icoon"])}<span>{t["naam"]}</span></a>' for t in SLEUTELTYPEN)
    faq = m["faq"] + [("Wat neem ik mee?", f"Voor de prijs is uw kenteken genoeg. Op de afspraak neemt u de auto mee en, als u die heeft, uw huidige {naam}-sleutel.")]
    pagina(pad, titel, omschr,
           jsonld=[faq_jsonld(faq), kruimels_jsonld([("Home", "/"), ("Merken", "/merken"), (naam, pad)])],
           beeld=f[0], body=f"""
{kruimels([("Home", "/"), ("Merken", "/merken"), (naam, "")])}
<section class="sectie sectie--kort"><div class="wrap twee">
  <div>
    <h1>{naam} autosleutel bijmaken in Hengelo</h1>
    {antwoord(m["intro"])}
    {knoppen()}
  </div>
  {fig}
</div></section>
<section class="sectie sectie--zand"><div class="wrap wrap--tekst">
  <h2>Welke sleutel heeft uw {naam}?</h2>
  <p>Dat hangt af van model en bouwjaar, en daar gaan wij niet op gokken: wij lezen het uit uw kenteken. Als richtlijn:</p>
  <ul class="typen">{typen}</ul>
  <p>Twijfelt u welk type u heeft? Kies hieronder het type dat op uw sleutel lijkt, of stuur een foto via <a href="{g['WA_LINK']}" rel="noopener" data-conv="whatsapp">WhatsApp</a>.</p>
  <div class="kiezer kiezer--klein">{typelinks}</div>
  <h2>Wat kost een {naam}-sleutel?</h2>
  {_prijsblok(g, m)}
  {extra}
  <h2>{naam}-modellen die wij vaak zien</h2>
  <p>Een greep uit de modellen. Staat het uwe er niet tussen, stuur dan gewoon uw kenteken.</p>
  <ul class="modellen">{modellen}</ul>
  <h2>Zo gaat het</h2>
  <ol class="stappen">
    <li>{icoon("kenteken")}<h3>Kenteken sturen</h3><p>Bel, app of vul het formulier in. Daaruit lezen wij af welke sleutel en welke inleermethode bij uw {naam} horen.</p></li>
    <li>{icoon("vink")}<h3>Prijs vooraf</h3><p>U hoort dezelfde werkdag wat het kost en of het bij uw bouwjaar kan.</p></li>
    <li>{icoon("winkel")}<h3>Werkplaats of aan huis</h3><p>In Enschede Zuid, {g['REISTIJD']} vanaf Hengelo, meestal in {g['DOORLOOPTIJD']}. Of wij komen naar u toe.</p></li>
  </ol>
  <p>Is uw {naam}-sleutel kapot maar start de auto nog? Kijk bij <a href="/autosleutel-reparatie">reparatie</a>. Alle sleutels kwijt? Lees <a href="/autosleutel-kwijt">wat er dan gebeurt</a>. Alle bedragen op een rij vindt u bij <a href="/prijzen">prijzen</a>.</p>
</div></section>
{cta(f"Wat kost een sleutel voor uw {naam}? Stuur uw kenteken; u hoort het dezelfde werkdag.")}
{faqblok(faq, f"Vragen over {naam}-sleutels")}
{formulier("merk-" + slug)}
""")

def merkenoverzicht(g):
    pagina, kruimels, kruimels_jsonld, formulier = (g[k] for k in ("pagina", "kruimels", "kruimels_jsonld", "formulier"))
    kaarten = "".join(f'<a class="merk" href="/{m["slug"]}"><b>{m["naam"]}</b><span>{_vanaf(g, m)}</span></a>' for m in MERKEN)
    kaarten += f'<a class="merk" href="/overige-merken"><b>Overige merken</b><span>{", ".join(OVERIGE_MERKEN[:4])} en meer</span></a>'
    pagina("/merken", "Autosleutel bijmaken per merk | Autosleutel Hengelo",
           f"Per automerk: welke sleuteltypen er zijn, wat bijmaken kost en wat u meeneemt. Vanaf € {g['P_TRANS']} inclusief programmeren, voor Hengelo en omgeving.",
           jsonld=[kruimels_jsonld([("Home", "/"), ("Merken", "/merken")])], body=f"""
{kruimels([("Home", "/"), ("Merken", "")])}
<section class="sectie sectie--kort"><div class="wrap">
  <h1>Autosleutel bijmaken per merk</h1>
  <p class="intro">Elk merk heeft eigen sleutelgeneraties, uitzonderingen en prijsregels. Kies uw merk: u leest welke sleuteltypen er zijn, wat wij kunnen en wat het kost. Weet u niet welk type u heeft, dan zegt uw kenteken het ons.</p>
  <div class="merk-lijst">{kaarten}</div>
</div></section>
{formulier("merken")}
""")

def overige_pagina(g):
    pagina, kruimels, kruimels_jsonld, formulier, knoppen, antwoord, faqblok, faq_jsonld = (g[k] for k in ("pagina", "kruimels", "kruimels_jsonld", "formulier", "knoppen", "antwoord", "faqblok", "faq_jsonld"))
    faq = [("Maken jullie ook sleutels voor merken die hier niet staan?", "Vaak wel, maar wij zoeken het eerst uit. Stuur uw kenteken, dan hoort u vooraf of het kan en wat het kost."),
           ("Hoe zit het met exotische merken?", "Op aanvraag. Een deel van die sleutels levert alleen de fabriek; in dat geval hoort u het van tevoren."),
           ("Wat kost het?", "Voor deze merken is er geen tabelprijs. Uw kenteken geeft vooraf de prijs.")]
    lijst = "".join(f"<li>{html.escape(x)}</li>" for x in OVERIGE_MERKEN)
    pagina("/overige-merken", "Overige automerken | Autosleutel Hengelo",
           "Sleutel nodig voor een minder gangbaar merk, zoals Saab, Subaru of Maserati? Wij zoeken op uw kenteken uit wat kan en wat het kost.",
           jsonld=[faq_jsonld(faq), kruimels_jsonld([("Home", "/"), ("Merken", "/merken"), ("Overige merken", "/overige-merken")])], body=f"""
{kruimels([("Home", "/"), ("Merken", "/merken"), ("Overige merken", "")])}
<section class="sectie sectie--kort"><div class="wrap wrap--tekst">
  <h1>Overige automerken</h1>
  {antwoord("Staat uw merk niet in ons overzicht, zoals Saab, Subaru, Chevrolet, Lancia of een exotisch merk? Ook dan kunnen wij vaak een sleutel maken, maar op aanvraag. Wij zoeken eerst op uw kenteken uit welke chip en procedure de auto heeft en of de sleutel te krijgen is. Voordat u iets betaalt, weet u of het lukt en wat het kost.")}
  <p>Een tabelprijs is er voor deze merken niet. Soms is een sleutel alleen via de fabriek te krijgen; dan zeggen wij dat eerlijk. Bij een kopie van een werkende sleutel of een reparatie van de behuizing kunnen wij vaker helpen.</p>
  <h2>Merken op aanvraag</h2>
  <ul class="modellen">{lijst}</ul>
  <p>Ook uw merk niet gevonden? App ons een foto van de sleutel met uw kenteken erbij; wij gaan het na.</p>
  {knoppen()}
</div></section>
{faqblok(faq, "Vragen over overige merken")}
{formulier("merk-overige")}
""")
