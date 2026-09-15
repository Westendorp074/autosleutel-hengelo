# Kernpagina's, opbouw zoals autosleutel-enschede.nl: hero met grote foto, situaties, stappen, werkplaats, aan huis,
# sleuteltype-kiezer, galerij, cta, merken, Westendorp, werkgebied, FAQ, formulier. Teksten eigen voor Hengelo.
# Wordt aangeroepen vanuit build.py met diens globals.

def bouw_paginas(g):
    globals().update(g)
    from data_merken import MERKEN, merkpagina, merkenoverzicht, overige_pagina
    import data_paginas_2

    def stappen():
        return f"""
<section class="sectie sectie--zand" id="zo-werkt-het">
  <div class="wrap">
    <div class="sectie__kop"><h2>Zo werkt het</h2><p>Drie stappen, en meestal staat u binnen {DOORLOOPTIJD} weer buiten. Op afspraak staat alles voor uw auto al klaar.</p></div>
    <ol class="stappen">
      <li>{icoon("kenteken")}<h3>Kenteken doorgeven</h3><p>Bel, app of vul het formulier in. Wij zien welk sleuteltype, welke chip en welke procedure uw auto heeft, en u hoort de prijs vooraf.</p></li>
      <li>{icoon("winkel")}<h3>Werkplaats of aan huis</h3><p>U rijdt in {REISTIJD} naar de werkplaats in Enschede Zuid, gratis parkeren. Kan dat niet, dan komen wij naar u toe in Hengelo.</p></li>
      <li>{icoon("vink")}<h3>Klaar terwijl u wacht</h3><p>Wij maken, programmeren of repareren uw sleutel, en u test hem op uw eigen auto voordat u betaalt.</p></li>
    </ol>
    {knoppen(midden=True)}
  </div>
</section>"""

    def werkplaatsblok():
        return f"""
<section class="sectie">
  <div class="wrap media">
    <div>
      <h2>Eigen werkplaats in {WINKELCENTRUM}</h2>
      <p>Geen busje met één universeel apparaat, maar een vaste werkplaats: kasten vol behuizingen, chips en afstandsbedieningen voor vrijwel elk merk, sleutelmachines die op code frezen en programmeerapparatuur per merk. Daardoor is uw sleutel meestal klaar terwijl u wacht.</p>
      <p>Wij programmeren in de software van uw auto, net zoals de dealer dat doet, en werken ook met dealers samen. Het verschil zit in de voorraad en de wachttijd: de dealer bestelt en doet er doorgaans twee tot zes weken over. Zo bent u bij ons tot 50% goedkoper dan de dealer.</p>
      <ul class="vinkjes">
        <li>{icoon("vink")}Prijs vooraf op basis van uw kenteken, inclusief programmeren en btw</li>
        <li>{icoon("vink")}Levenslange garantie op de transponderchip, {GARANTIE_AB} op een nieuwe afstandsbediening</li>
        <li>{icoon("vink")}Gratis parkeren bij het overdekte winkelcentrum</li>
        <li>{icoon("vink")}Eerlijk over wat niet kan: {MERCEDES_REGEL}</li>
      </ul>
      <p class="tekstlink"><a href="{ROUTE_LINK}" rel="noopener" data-conv="route">{icoon("route")}Route vanuit Hengelo</a></p>
    </div>
    <div class="media__fotos">
      <figure>{foto("werkplaats-voorraad-autosleutel-behuizingen.jpg", "Sleutelspecialist bij de voorraadkasten met autosleutelbehuizingen en chips in de werkplaats")}<figcaption>Behuizingen en chips per merk op voorraad</figcaption></figure>
      <figure>{foto("werkplaats-autosleutel-reparatie-werkbank.jpg", "Sleutelspecialist repareert een autosleutel aan de werkbank in de werkplaats in Enschede")}<figcaption>Programmeren en repareren aan de werkbank</figcaption></figure>
    </div>
  </div>
</section>"""

    def aanhuisblok():
        return f"""
<section class="sectie sectie--groen-licht">
  <div class="wrap media media--omgekeerd">
    <div>
      <span class="label">{icoon("huis")}Aan-huisservice</span>
      <h2>Auto start niet? Wij komen naar Hengelo.</h2>
      <p>Alle sleutels kwijt of staat de auto vast? Dan komen wij naar u toe en melden de nieuwe sleutel ter plekke aan via de diagnoseaansluiting. In Hengelo kost dat vanaf € {AAN_HUIS_VANAF} bovenop de sleutelprijs; daarbuiten rekenen wij een kilometervergoeding, die in de prijsopgave staat.</p>
      <p class="tekstlink"><a href="/aan-huis">{icoon("pijl")}Zo werkt aan huis</a></p>
    </div>
    <figure class="media__foto">{foto("autosleutel-programmeren-hyundai.jpg", "Hyundai-sleutels in de hand terwijl ze met een programmeertablet via de diagnoseaansluiting worden ingeleerd")}<figcaption>Inleren via de diagnoseaansluiting, ook bij u voor de deur</figcaption></figure>
  </div>
</section>"""

    GALERIJ = [
        ("bmw-x1-smartkey-bijmaken.jpg", "Twee BMW-smartkeys in de hand, met de BMW X1 op de achtergrond", "BMW X1 · smartkey"),
        ("mini-clubman-smartkey-bijmaken.jpg", "Twee Mini-smartkeys in de hand, met de Mini Clubman op de achtergrond", "Mini Clubman · smartkey"),
        ("renault-kadjar-sleutelkaart-bijmaken.jpg", "Twee Renault-sleutelkaarten in de hand, met de Renault Kadjar op de achtergrond", "Renault Kadjar · sleutelkaart"),
        ("fiat-500-klapsleutel-bijmaken.jpg", "Twee Fiat-klapsleutels in de hand, met de witte Fiat 500 op de achtergrond", "Fiat 500 · klapsleutel"),
        ("jeep-compass-smartkey-bijmaken.jpg", "Twee smartkeys in de hand, met de witte Jeep Compass op de achtergrond", "Jeep Compass · smartkey"),
        ("citroen-c4-picasso-smartkey-bijmaken.jpg", "Twee Citroën-sleutels in de hand, met de Citroën C4 Picasso op de achtergrond", "Citroën C4 Picasso · smartkey"),
        ("jaguar-xf-smartkey-bijmaken.jpg", "Twee Jaguar-smartkeys in de hand, met de Jaguar XF op de achtergrond", "Jaguar XF · smartkey"),
        ("opel-astra-klapsleutel-bijmaken.jpg", "Twee Opel-klapsleutels in de hand, met de Opel Astra op de achtergrond", "Opel Astra · klapsleutel"),
    ]
    def galerijblok():
        figs = "".join(f"<figure>{foto(n, a)}<figcaption>{c}</figcaption></figure>" for n, a, c in GALERIJ)
        return f"""
<section class="sectie sectie--zand">
  <div class="wrap">
    <div class="sectie__kop"><h2>Onlangs gemaakt</h2><p>Echte foto's van sleutels die wij maakten: de nieuwe sleutel voorop, de auto erachter.</p></div>
    <div class="galerij">{figs}</div>
  </div>
</section>"""

    def merkenstrip():
        return f"""
<section class="sectie">
  <div class="wrap">
    <div class="sectie__kop"><h2>Voor welk merk?</h2><p>Per merk leest u welke sleuteltypen er zijn, wat het kost en wat wij kunnen. Wij gaan bij geen enkel merk uit van één type: u ziet ze allemaal en uw kenteken beslist.</p></div>
    <div class="merken">{"".join(f'<a href="/{m["slug"]}">{m["naam"]}</a>' for m in MERKEN)}<a href="/overige-merken">Overige merken</a></div>
  </div>
</section>"""

    g.update(stappen=stappen, werkplaatsblok=werkplaatsblok, aanhuisblok=aanhuisblok, galerijblok=galerijblok, merkenstrip=merkenstrip)

    # ---------- Home ----------
    HOME_FAQ = [
        ("Wat kost een autosleutel bijmaken in Hengelo?", f"Een transpondersleutel vanaf € {P_TRANS}, een klapsleutel vanaf € {P_KLAP}, een sleutelkaart vanaf € {P_KAART} en een smartkey vanaf € {P_SMART}, inclusief programmeren en btw. Tot 50% goedkoper dan de dealer. Met uw kenteken maken wij er vooraf één prijs van."),
        ("Hoe ver is de werkplaats vanaf Hengelo?", f"Ongeveer {REISTIJD} rijden via de A35 naar Enschede Zuid. U parkeert gratis bij het overdekte winkelcentrum."),
        ("Wat kost de aan-huisservice?", f"In Hengelo vanaf € {AAN_HUIS_VANAF} bovenop de sleutelprijs. Buiten Hengelo komt er een kilometervergoeding bij; die staat in de prijsopgave."),
        ("Geen enkele sleutel meer over. Kan dat ook?", "Dan maken wij een nieuwe sleutel op basis van uw kenteken en wissen wij de verloren sleutels uit de auto. De prijs verschilt per merk en bouwjaar te veel om hier te noemen; u krijgt hem vooraf op aanvraag."),
        ("Hoe lang duurt het?", f"Meestal {DOORLOOPTIJD}, terwijl u wacht. Moet een sleutel voor een enkel zeer recent model besteld worden, dan hoort u dat vooraf."),
        ("Hoe weet ik welk sleuteltype ik heb?", "Klapt de baard uit: klapsleutel. Startknop in de auto: smartkey. Platte kaart: sleutelkaart. Vaste baard met kunststof kop: transpondersleutel. Twijfelt u, stuur dan een foto via WhatsApp."),
    ]
    pagina("/", "Autosleutel bijmaken Hengelo | klaar terwijl u wacht",
           f"Autosleutel kwijt, kapot of een reserve nodig? Bijmaken en programmeren vanaf € {P_TRANS}, meestal in {DOORLOOPTIJD}. Werkplaats op {REISTIJD} of aan huis.",
           jsonld=[faq_jsonld(HOME_FAQ)], beeld="bmw-x1-smartkey-bijmaken.jpg", body=f"""
<section class="hero">
  <div class="wrap hero__grid">
    <div>
      <span class="label">{icoon("pin")}Werkplaats in Enschede Zuid · {REISTIJD} vanaf Hengelo</span>
      <h1>Autosleutel bijmaken in Hengelo, <em>klaar terwijl u wacht.</em></h1>
      <p class="hero__lead">Wij maken, programmeren en repareren autosleutels voor vrijwel elk merk. U bent tot 50% goedkoper dan de dealer, weet de prijs voordat u komt en rijdt meestal na {DOORLOOPTIJD} weer weg.</p>
      {knoppen()}
      <p class="hero__noot">Liever niet rijden? <strong>Aan huis in Hengelo vanaf € {AAN_HUIS_VANAF}</strong></p>
    </div>
    <figure class="hero__foto">{foto("bmw-x1-smartkey-bijmaken-hero.jpg", "Twee bijgemaakte BMW-smartkeys in de hand, met de BMW X1 op de achtergrond", lazy=False)}<figcaption>BMW X1: twee smartkeys, klaar in één bezoek</figcaption></figure>
  </div>
  {vertrouwen()}
</section>
{situaties()}
{stappen()}
{werkplaatsblok()}
{aanhuisblok()}
{kiezer()}
{galerijblok()}
{cta()}
{merkenstrip()}
{moederblok()}
{werkgebiedblok()}
{faqblok(HOME_FAQ)}
{formulier("home")}
""")

    # ---------- Sleuteltype-pagina's ----------
    for t in SLEUTELTYPEN:
        p = typeprijs(t)
        pad = "/" + t["slug"]
        rep = t["slug"] == "autosleutel-reparatie"
        andere = "".join(f'<a class="kies kies--klein" href="/{o["slug"]}">{icoon(o["icoon"])}<span>{o["naam"]}</span></a>' for o in SLEUTELTYPEN if o is not t)
        secties = "".join(f"<h2>{h}</h2><p>{x}</p>" for h, x in t["tekst"])
        meenemen = "".join(f"<li>{icoon('vink')}{x}</li>" for x in t["meenemen"])
        titel = f"{t['kop']} Hengelo | vanaf € {p}"
        if len(titel) > 62: titel = f"Smartkey bijmaken Hengelo | keyless vanaf € {p}"
        omschr = (f"{t['kop']} voor Hengelo: vanaf € {p} inclusief programmeren en btw, meestal klaar terwijl u wacht. Prijs vooraf op uw kenteken, ook aan huis."
                  if not rep else f"Autosleutel kapot? Behuizing, knopjes, klapveer of printplaat gerepareerd vanaf € {p}. Uw chip blijft, meestal klaar terwijl u wacht.")
        if len(omschr) > 160: omschr = f"{t['naam']} bijmaken voor Hengelo: vanaf € {p} inclusief programmeren en btw, meestal klaar terwijl u wacht. Ook aan huis."
        kwijt = "" if rep else f"""
  <h2>Alle sleutels kwijt?</h2>
  <p>Dan is het geen kopie meer, maar een nieuwe sleutel die op de auto wordt aangemeld. Dat kan bij vrijwel elk merk. Een prijs noemen wij daarvoor niet, omdat die per auto te ver uiteenloopt; u krijgt hem vooraf op aanvraag. Lees <a href="/autosleutel-kwijt">wat er gebeurt als alle sleutels kwijt zijn</a>.</p>"""
        pagina(pad, titel, omschr,
               jsonld=[faq_jsonld(t["faq"]), kruimels_jsonld([("Home", "/"), ("Prijzen", "/prijzen"), (t["naam"], pad)])],
               beeld=t["foto"][0], body=f"""
{kruimels([("Home", "/"), ("Prijzen", "/prijzen"), (t["naam"], "")])}
<section class="sectie sectie--kort"><div class="wrap twee">
  <div>
    <span class="label">{icoon(t["icoon"])}{t["naam"]} · {prijs(p)}</span>
    <h1>{t["kop"]} in Hengelo</h1>
    {antwoord(t["antwoord"])}
    {knoppen()}
    <ul class="hero__feiten"><li>{icoon("vink")}{prijs(p)}, inclusief {"btw" if rep else "programmeren en btw"}</li><li>{icoon("vink")}Meestal klaar in {DOORLOOPTIJD}</li><li>{icoon("vink")}Aan huis in Hengelo {prijs(AAN_HUIS_VANAF)} extra</li></ul>
  </div>
  <figure class="figuur">{foto(t["foto"][0], t["foto"][1], lazy=False)}<figcaption>{t["foto"][1]}</figcaption></figure>
</div></section>
<section class="sectie sectie--zand"><div class="wrap wrap--tekst">
  <h2>Zo herkent u {"een sleutel die gerepareerd kan worden" if rep else "een " + t["naam"].lower()}</h2>
  <p>{t["herken"]}</p>
  <p><b>Komt voor bij:</b> {t["merken"]}. Niet zeker? Uw kenteken vertelt het ons, of stuur een foto van de sleutel via <a href="{WA_LINK}" rel="noopener" data-conv="whatsapp">WhatsApp</a>.</p>
  {secties}
  {kwijt}
  <h2>Wat u meeneemt</h2>
  <ul class="vinkjes">{meenemen}</ul>
</div></section>
{cta()}
<section class="sectie"><div class="wrap">
  <div class="sectie__kop"><h2>Ander sleuteltype?</h2><p>Of lees alles over <a href="/autosleutel-bijmaken">autosleutel bijmaken in Hengelo</a>.</p></div>
  <div class="kiezer kiezer--klein">{andere}</div>
</div></section>
{stappen()}
{faqblok(t["faq"], f"Vragen over {'reparatie' if rep else t['naam'].lower() + ('en' if t['naam'].endswith('kaart') else 's')}")}
{formulier(t["slug"])}
""")

    data_paginas_2.bouw(g)
    merkenoverzicht(g)
    for i, m in enumerate(MERKEN):
        merkpagina(g, m, i)
    overige_pagina(g)
