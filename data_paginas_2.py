# Overige pagina's: bijmaken, kwijt, prijzen, aan huis, over ons, contact, kennis, bedankt, privacy.

def bouw(g):
    globals().update(g)

    # ---------- Autosleutel bijmaken ----------
    BIJ_FAQ = [
        ("Wat kost een reservesleutel?", f"Een transpondersleutel vanaf € {P_TRANS}, een klapsleutel vanaf € {P_KLAP}, een sleutelkaart vanaf € {P_KAART} en een smartkey vanaf € {P_SMART}. Inclusief programmeren en btw; uw kenteken bepaalt de precieze prijs."),
        ("Kan het ook zonder mijn huidige sleutel?", "Ja, maar dan maken wij geen kopie meer: het wordt een nieuwe sleutel die op de auto wordt aangemeld. De prijs daarvan krijgt u op aanvraag. Lees meer bij autosleutel kwijt."),
        ("Hoe lang duurt het?", f"Meestal {DOORLOOPTIJD}, terwijl u wacht."),
        ("Werkt een bijgemaakte sleutel even goed als het origineel?", f"Chip en zender werken hetzelfde en worden op dezelfde manier ingeleerd. U krijgt levenslange garantie op de transponderchip en {GARANTIE_AB} op een nieuwe afstandsbediening."),
        ("Is twee sleutels tegelijk goedkoper?", "Ja. Op de tweede sleutel in hetzelfde bezoek krijgt u korting, in overleg. Zet bij uw aanvraag dat u er twee wilt."),
        ("Kan een sleutel ook aan huis bijgemaakt worden?", f"Ja. In Hengelo vanaf € {AAN_HUIS_VANAF} bovenop de sleutelprijs; daarbuiten met een kilometervergoeding in de prijsopgave."),
    ]
    pagina("/autosleutel-bijmaken", f"Autosleutel bijmaken Hengelo | reservesleutel vanaf € {P_TRANS}",
           f"Reservesleutel of nieuwe autosleutel voor Hengelo: vanaf € {P_TRANS} inclusief programmeren, meestal in {DOORLOOPTIJD} klaar. Prijs vooraf via uw kenteken.",
           jsonld=[faq_jsonld(BIJ_FAQ), kruimels_jsonld([("Home", "/"), ("Autosleutel bijmaken", "/autosleutel-bijmaken")])],
           beeld="renault-kadjar-sleutelkaart-hengelo.jpg", body=f"""
{kruimels([("Home", "/"), ("Autosleutel bijmaken", "")])}
<section class="sectie sectie--kort"><div class="wrap twee">
  <div>
    <span class="label">{icoon("sleutels")}Reservesleutel · kopie · nieuwe sleutel</span>
    <h1>Autosleutel bijmaken in Hengelo</h1>
    {antwoord(f"Heeft u nog een werkende sleutel, dan zetten wij de chip en de afstandsbediening over op een nieuwe sleutel. Dat kost vanaf € {P_TRANS}, inclusief frezen, programmeren en btw; per sleuteltype ziet u hieronder de vanaf-prijs. Meestal bent u in {DOORLOOPTIJD} klaar, in de werkplaats op {REISTIJD} van Hengelo of aan huis. Met uw kenteken krijgt u de prijs vooraf.")}
    {knoppen()}
  </div>
  <figure class="figuur">{foto("renault-kadjar-sleutelkaart-hengelo.jpg", "Twee Renault-sleutelkaarten in de hand, met de zwarte Renault Kadjar op de achtergrond", lazy=False)}<figcaption>Renault Kadjar: twee sleutelkaarten bijgemaakt en ingeleerd</figcaption></figure>
</div></section>
{kiezer("Welke sleutel heeft u?", "Het sleuteltype bepaalt de prijs, niet hoe duur uw auto was. Kies het type dat op uw sleutel lijkt. Wij gaan bij geen enkel merk uit van één type; twijfelt u, stuur dan een foto of uw kenteken.", zand=True)}
{cta("Twee sleutels tegelijk? Op de tweede krijgt u korting. Stuur uw kenteken en vraag naar de prijs voor twee.")}
<section class="sectie"><div class="wrap wrap--tekst">
  <h2>Waarom een tweede sleutel nu slim is</h2>
  <p>Zolang één sleutel het doet, is bijmaken een kopie: wij lezen de chip uit, zetten die in een nieuwe sleutel en melden de afstandsbediening aan. Raakt die laatste sleutel kwijt, dan moet er een sleutel zonder origineel komen. Dat lukt bij bijna elke auto, maar het is meer werk en de auto staat stil tot het geregeld is. Een reservesleutel voorkomt dat gedoe.</p>
  <h2>Wat u meeneemt</h2>
  <ul class="vinkjes">
    <li>{icoon("vink")}Uw huidige, werkende sleutel</li>
    <li>{icoon("vink")}De auto, zodat wij de nieuwe sleutel meteen testen</li>
  </ul>
  <h2>Bij ons of bij de dealer</h2>
  <p>De dealer bestelt uw sleutel bij de fabriek en doet er doorgaans twee tot zes weken over. Wij hebben behuizingen, chips en afstandsbedieningen op voorraad en programmeren in de software van uw auto, net als de dealer. Zo bent u tot 50% goedkoper dan de dealer en rijdt u dezelfde dag met twee sleutels.</p>
  <p>Is uw sleutel niet kwijt maar kapot? Dan is <a href="/autosleutel-reparatie">repareren</a> vaak genoeg. Alle bedragen op een rij staan bij <a href="/prijzen">prijzen</a>, en per merk leest u meer via <a href="/merken">merken</a>.</p>
</div></section>
{stappen()}
{faqblok(BIJ_FAQ, "Vragen over autosleutel bijmaken")}
{formulier("autosleutel-bijmaken")}
""")

    # ---------- Autosleutel kwijt ----------
    KWIJT_FAQ = [
        ("Kan er nog een sleutel gemaakt worden als alles kwijt is?", f"Bijna altijd wel. Wij maken een nieuwe sleutel op basis van uw kenteken en melden die aan op de auto. Een uitzondering: {MERCEDES_REGEL}"),
        ("Wat betaal ik als er geen sleutel meer is?", "Dat verschilt per merk, model en bouwjaar te veel om een bedrag te noemen. Stuur uw kenteken, dan krijgt u de prijs vooraf."),
        ("Moet de auto mee?", f"De nieuwe sleutel wordt op de auto zelf aangemeld, dus de auto moet erbij zijn. Start hij niet, dan komen wij naar u toe: in Hengelo vanaf € {AAN_HUIS_VANAF} bovenop de sleutelprijs."),
        ("Werkt de verloren sleutel daarna nog?", "Nee. Bij het aanmelden wissen wij alle sleutels die er niet bij zijn."),
        ("Wat heb ik nodig?", "Het kentekenbewijs en een geldig identiteitsbewijs van de eigenaar. Zo weten wij zeker dat de auto van u is. Bij Peugeot en Citroën tot ongeveer 2005 ook de pincode uit de autopapieren; zonder code vragen wij hem op, vanaf € 35."),
    ]
    pagina("/autosleutel-kwijt", "Autosleutel kwijt Hengelo | nieuwe sleutel zonder reserve",
           "Alle autosleutels kwijt? Wij maken een nieuwe sleutel op uw kenteken, melden hem aan en wissen de oude. In de werkplaats of bij u aan huis in Hengelo.",
           jsonld=[faq_jsonld(KWIJT_FAQ), kruimels_jsonld([("Home", "/"), ("Autosleutel kwijt", "/autosleutel-kwijt")])],
           beeld="jeep-compass-smartkey-hengelo.jpg", body=f"""
{kruimels([("Home", "/"), ("Autosleutel kwijt", "")])}
<section class="sectie sectie--kort"><div class="wrap twee">
  <div>
    <span class="label">{icoon("kwijt")}Alle sleutels kwijt of gestolen</span>
    <h1>Autosleutel kwijt? Zo krijgt u in Hengelo een nieuwe</h1>
    {antwoord("Geen werkende sleutel meer? Wij maken een nieuwe sleutel op basis van uw kenteken en melden die aan op de auto. De verloren sleutels wissen wij, zodat niemand er nog mee wegrijdt. Dat kan in de werkplaats of bij u aan huis. De prijs hangt af van merk en bouwjaar; u krijgt hem vooraf op aanvraag.")}
    <p>Heeft u nog wel een reservesleutel? Dan is het eenvoudiger: een <a href="/autosleutel-bijmaken">kopie van die sleutel</a> kost vanaf € {P_TRANS}.</p>
    {knoppen('Bel direct <span class="tel-nr">' + TEL_HTML + '</span>')}
  </div>
  <figure class="figuur">{foto("jeep-compass-smartkey-hengelo.jpg", "Twee nieuwe smartkeys in een gehandschoende hand, met de Jeep Compass waarvan alle sleutels kwijt waren op de achtergrond", lazy=False)}<figcaption>Jeep Compass: oude sleutels gewist, twee nieuwe ingeleerd</figcaption></figure>
</div></section>
<section class="sectie sectie--zand"><div class="wrap wrap--tekst">
  <h2>Eerst dit</h2>
  <ol class="stappen stappen--lijst">
    <li>{icoon("kwijt")}<h3>Zoek nog één keer</h3><p>Jaszakken, de wasmand, de auto zelf, de laatste parkeerplek. Duikt de sleutel binnen een dag op, dan bespaart u het hele bedrag.</p></li>
    <li>{icoon("schild")}<h3>Gestolen? Doe aangifte</h3><p>En vraag uw verzekeraar of uw polis een nieuwe sleutel na diefstal vergoedt. Lees ook <a href="/autosleutel-gestolen">wat u doet bij een gestolen sleutel</a>.</p></li>
    <li>{icoon("kenteken")}<h3>Stuur uw kenteken</h3><p>U hoort dezelfde werkdag wat een nieuwe sleutel kost, of het bij uw bouwjaar kan en of wij naar u toe kunnen komen.</p></li>
  </ol>
  <h2>Zo maken wij een sleutel zonder origineel</h2>
  <p>Uit uw kenteken halen wij het sleutelprofiel en de chipgeneratie. De baard frezen wij op code, zodat hij in het slot past. Daarna koppelen wij de nieuwe chip en de afstandsbediening via de diagnoseaansluiting aan de startonderbreker. In dezelfde handeling verdwijnen alle sleutels die er niet bij zijn uit het geheugen. Daarom moet de auto erbij zijn: het aanmelden gebeurt op de auto, niet op de sleutel.</p>
  <p>Bij Peugeot en Citroën tot ongeveer 2005 is een <a href="/peugeot">pincode uit de autopapieren</a> nodig. {MERCEDES_REGEL} Moet een sleutel voor een enkel zeer recent model via de fabriek, dan hoort u dat vooraf.</p>
  <h2>Auto start niet en staat vast?</h2>
  <p>Slepen is niet nodig. Wij komen naar u toe in Hengelo, vanaf € {AAN_HUIS_VANAF} bovenop de sleutelprijs, of in de omgeving met een kilometervergoeding. <a href="/aan-huis">Zo werkt de aan-huisservice</a>.</p>
  <h2>Wat u klaarlegt</h2>
  <ul class="vinkjes">
    <li>{icoon("vink")}De auto, in de werkplaats of bij u voor de deur</li>
    <li>{icoon("vink")}Kentekenbewijs</li>
    <li>{icoon("vink")}Geldig identiteitsbewijs van de eigenaar</li>
    <li>{icoon("vink")}Bij Peugeot of Citroën tot ongeveer 2005: de pincode uit de autopapieren</li>
  </ul>
</div></section>
{cta("Alle sleutels kwijt? Stuur uw kenteken; u hoort dezelfde werkdag wat wij kunnen doen.")}
{faqblok(KWIJT_FAQ, "Vragen over een verloren autosleutel")}
{formulier("autosleutel-kwijt")}
""")

    # ---------- Prijzen ----------
    PRIJS_FAQ = [
        ("Waarom zijn het vanaf-prijzen?", "Merk, model en bouwjaar maken het verschil. Met uw kenteken zien wij welke sleutel uw auto heeft, en krijgt u de prijs voordat u komt."),
        ("Zit programmeren bij de prijs in?", "Ja. In elk bedrag zitten het programmeren, het frezen en de btw."),
        ("Waarom is een nieuwere auto duurder?", "Jongere auto's hebben zwaarder beveiligde chips. De sleutel kost meer en het programmeren vraagt meer werk."),
        ("Wat kost het als alle sleutels kwijt zijn?", "Dan noemen wij op de site geen bedrag, omdat merk en bouwjaar het te sterk laten wisselen. Stuur uw kenteken, dan krijgt u de prijs vooraf."),
        ("Wat kost aan huis?", f"In Hengelo vanaf € {AAN_HUIS_VANAF} bovenop de sleutelprijs; daarbuiten een kilometervergoeding, die in de prijsopgave staat."),
    ]
    pagina("/prijzen", f"Autosleutel prijzen Hengelo | vanaf € {P_TRANS}, incl. btw",
           f"Wat kost een autosleutel? Transponder vanaf € {P_TRANS}, klapsleutel en sleutelkaart vanaf € {P_KLAP}, smartkey vanaf € {P_SMART}, reparatie vanaf € {P_REP}. Incl. btw.",
           jsonld=[faq_jsonld(PRIJS_FAQ), kruimels_jsonld([("Home", "/"), ("Prijzen", "/prijzen")])], body=f"""
{kruimels([("Home", "/"), ("Prijzen", "")])}
<section class="sectie sectie--kort"><div class="wrap wrap--tekst">
  <h1>Wat kost een autosleutel bijmaken?</h1>
  {antwoord(f"Een transpondersleutel kost vanaf € {P_TRANS}, een klapsleutel vanaf € {P_KLAP}, een sleutelkaart vanaf € {P_KAART} en een smartkey vanaf € {P_SMART}. Een reparatie kost vanaf € {P_REP}. Programmeren, frezen en btw zitten erbij. Met uw kenteken maken wij er vooraf één prijs van. Zijn alle sleutels kwijt, dan is de prijs op aanvraag. Aan huis in Hengelo komt er vanaf € {AAN_HUIS_VANAF} bij.")}
  <p>Wat u betaalt, wordt bepaald door het sleuteltype en het bouwjaar, niet door de nieuwprijs van uw auto. Het bouwjaar bepaalt welke chip erin zit, en daarmee de sleutel en het programmeerwerk.</p>
  {prijstabel()}
  {uitzonderingen()}
  <h2>Twee sleutels tegelijk</h2>
  <p>Laat u twee sleutels in één bezoek maken, dan krijgt u korting op de tweede, in overleg. Zet het bij uw aanvraag, dan staan beide in de prijsopgave.</p>
  <h2>Garantie</h2>
  <p>U krijgt levenslange garantie op de transponderchip, {GARANTIE_AB} op een nieuwe afstandsbediening.</p>
  {knoppen()}
</div></section>
{kiezer("Welke sleutel heeft u?", "Per sleuteltype leest u wat wij doen, wat u meeneemt en waar u op uitkomt.")}
{cta("Van schatting naar echte prijs? Stuur uw kenteken; u krijgt de prijs vooraf.")}
{dealerblok()}
{faqblok(PRIJS_FAQ, "Vragen over prijzen")}
{formulier("prijzen")}
""")

    # ---------- Aan huis ----------
    AANHUIS_FAQ = [
        ("Wat kost aan huis?", f"In Hengelo vanaf € {AAN_HUIS_VANAF} bovenop de sleutelprijs. Buiten Hengelo rekenen wij een kilometervergoeding; het totaal staat in uw prijsopgave."),
        ("Kan alles aan huis?", "Het meeste wel: programmeren, aanmelden, een reservesleutel maken. Wat bij uw auto ter plekke kan, hoort u vooraf. Soms bereiden wij de sleutel in de werkplaats voor en melden wij hem bij u alleen nog aan."),
        ("Hoe snel kunnen jullie komen?", "Op afspraak, meestal dezelfde of de volgende werkdag. Bellen is de snelste weg."),
        ("Moet ik erbij zijn?", "Ja. Wij willen weten dat de auto van u is voordat wij een sleutel aanmelden."),
    ]
    pagina("/aan-huis", f"Autosleutel aan huis Hengelo | vanaf € {AAN_HUIS_VANAF} extra",
           f"Auto start niet of alle sleutels kwijt? Wij komen naar u toe in Hengelo en melden de sleutel ter plekke aan. Vanaf € {AAN_HUIS_VANAF} bovenop de sleutelprijs.",
           jsonld=[faq_jsonld(AANHUIS_FAQ), kruimels_jsonld([("Home", "/"), ("Aan huis", "/aan-huis")])],
           beeld="hyundai-autosleutel-programmeren-hengelo.jpg", body=f"""
{kruimels([("Home", "/"), ("Aan huis", "")])}
<section class="sectie sectie--kort"><div class="wrap twee">
  <div>
    <span class="label">{icoon("huis")}Aan-huisservice · {prijs(AAN_HUIS_VANAF)}</span>
    <h1>Autosleutel aan huis in Hengelo</h1>
    {antwoord(f"Kunt u niet naar de werkplaats komen, dan komen wij naar u. In Hengelo kost dat vanaf € {AAN_HUIS_VANAF} bovenop de sleutelprijs; daarbuiten komt er een kilometervergoeding bij, die in de prijsopgave staat. Wij nemen de juiste sleutel mee, melden hem ter plekke aan via de diagnoseaansluiting, en u rijdt weer.")}
    {knoppen("Bel voor een afspraak")}
  </div>
  <figure class="figuur">{foto("hyundai-autosleutel-programmeren-hengelo.jpg", "Hyundai-sleutels in de hand terwijl ze met een programmeertablet via de diagnoseaansluiting worden ingeleerd", lazy=False)}<figcaption>Inleren via de diagnoseaansluiting, ook bij u voor de deur</figcaption></figure>
</div></section>
<section class="sectie sectie--zand"><div class="wrap wrap--tekst">
  <h2>Wanneer aan huis handig is</h2>
  <ul class="vinkjes">
    <li>{icoon("vink")}Alle sleutels zijn kwijt en de auto staat vast</li>
    <li>{icoon("vink")}De auto start niet meer door een kapotte sleutel</li>
    <li>{icoon("vink")}U heeft geen tijd of vervoer om naar Enschede Zuid te komen</li>
    <li>{icoon("vink")}Een bedrijfswagen die niet stil mag staan</li>
  </ul>
  <h2>Zo gaat het</h2>
  <ol class="stappen stappen--lijst">
    <li>{icoon("kenteken")}<h3>Kenteken en adres</h3><p>U stuurt uw kenteken en waar de auto staat. Wij zien welke sleutel het wordt en of het ter plekke kan.</p></li>
    <li>{icoon("vink")}<h3>Eén prijs vooraf</h3><p>U krijgt het totaal: sleutel, programmeren en de aan-huisservice, en buiten Hengelo de kilometervergoeding.</p></li>
    <li>{icoon("auto")}<h3>Wij komen langs</h3><p>Op afspraak, meestal dezelfde of de volgende werkdag. De sleutel wordt op uw auto aangemeld en u test hem meteen.</p></li>
  </ol>
  <h2>Werkgebied</h2>
  <p>Hengelo en omgeving: {", ".join(PLAATSEN[1:])}. Buiten Hengelo rekenen wij een kilometervergoeding.</p>
  <p class="noot">Liever zelf komen? De werkplaats ligt op {REISTIJD} rijden en dan betaalt u geen aan-huistoeslag. <a href="/contact">Route en openingstijden</a>.</p>
</div></section>
{cta()}
{faqblok(AANHUIS_FAQ, "Vragen over aan huis")}
{formulier("aan-huis")}
""")

    # ---------- Over ons ----------
    pagina("/over-ons", "Over ons | Autosleutel Hengelo, onderdeel van Westendorp",
           f"Autosleutel Hengelo is de autosleuteldienst van Westendorp Sleutel- en Slotenspecialist: bedrijf sinds {SINDS_BEDRIJF}, autosleutels sinds {SINDS_AUTOSLEUTELS}.",
           jsonld=[kruimels_jsonld([("Home", "/"), ("Over ons", "/over-ons")])], beeld="werkplaats-reparatie-werkbank-hengelo.jpg", body=f"""
{kruimels([("Home", "/"), ("Over ons", "")])}
<section class="sectie sectie--kort"><div class="wrap twee">
  <div>
    <h1>Autosleutel Hengelo is Westendorp</h1>
    {antwoord(f"{HANDELSNAAM} is geen los bedrijf, maar de autosleuteldienst van {MOEDER}. Dat familiebedrijf bestaat sinds {SINDS_BEDRIJF} en maakt sinds {SINDS_AUTOSLEUTELS} autosleutels, inmiddels meer dan {PER_JAAR} per jaar. De werkplaats zit aan de {STRAAT} in {WINKELCENTRUM}, {REISTIJD} vanaf Hengelo. Kunt u niet komen, dan komen wij aan huis.")}
    {knoppen(tweede="Naar de hoofdsite", tweede_href=MOEDER_URL, tweede_icoon="pijl")}
  </div>
  <figure class="figuur">{foto("werkplaats-reparatie-werkbank-hengelo.jpg", "Sleutelspecialist aan de werkbank in de werkplaats van Westendorp in Enschede", lazy=False)}<figcaption>De werkbank in {WINKELCENTRUM}</figcaption></figure>
</div></section>
<section class="sectie sectie--zand"><div class="wrap wrap--tekst">
  <h2>Wat u bij ons vindt</h2>
  <p>Een werkplaats met voorraad: behuizingen, chips en afstandsbedieningen voor vrijwel elk merk, sleutelmachines die op code frezen en programmeerapparatuur per merk. Wij programmeren in de software van uw auto, net als de dealer, en werken ook met dealers samen. Daardoor is uw sleutel meestal in {DOORLOOPTIJD} klaar en bent u tot 50% goedkoper dan de dealer.</p>
  <p>Westendorp doet ook huis- en fietssleutels, sloten en beveiliging. Daarvoor kijkt u op <a href="{MOEDER_URL}" rel="noopener">westendorpslotenspecialist.nl</a>; deze site gaat alleen over autosleutels.</p>
  <h2>Eerlijk over wat kan en wat niet</h2>
  <p>Wat bij uw auto mogelijk is, hoort u vooraf. {MERCEDES_REGEL} Een enkel zeer recent keyless-systeem is soms alleen via de dealer te krijgen. Een duidelijk nee vooraf is beter dan een sleutel die niet werkt.</p>
  <h2>Garantie</h2>
  <p>U krijgt levenslange garantie op de transponderchip, {GARANTIE_AB} op een nieuwe afstandsbediening.</p>
</div></section>
<section class="sectie"><div class="wrap">
  <div class="sectie__kop"><h2>Uit de werkplaats</h2></div>
  <div class="galerij">
    <figure>{foto("werkplaats-voorraad-behuizingen-hengelo.jpg", "Sleutelspecialist bij de voorraadkasten met sleutelbehuizingen per merk")}<figcaption>Behuizingen en chips op voorraad</figcaption></figure>
    <figure>{foto("hyundai-autosleutel-programmeren-hengelo.jpg", "Hyundai-sleutels worden met een programmeertablet via de diagnoseaansluiting ingeleerd")}<figcaption>Inleren via de diagnoseaansluiting</figcaption></figure>
    <figure>{foto("ford-mustang-autosleutel-hengelo.jpg", "Twee Ford-sleutels in de hand, met de Ford Mustang op de achtergrond")}<figcaption>Ford Mustang</figcaption></figure>
    <figure>{foto("mini-clubman-smartkey-hengelo.jpg", "Twee Mini-smartkeys in de hand, met de Mini Clubman op de achtergrond")}<figcaption>Mini Clubman</figcaption></figure>
  </div>
</div></section>
{cta()}
<section class="sectie sectie--zand"><div class="wrap wrap--tekst">
  <h2>Bedrijfsgegevens</h2>
  <ul class="feiten">
    <li>{icoon("winkel")}<span><b>Onderdeel van</b>{MOEDER}<br>{RECHTSPERSOON} · KvK {KVK} · btw {BTW}</span></li>
    <li>{icoon("pin")}<span><b>Werkplaats</b>{STRAAT}, {POSTCODE} {PLAATS}<br>{WINKELCENTRUM}</span></li>
    <li>{icoon("klok")}<span><b>Open</b>di – vr 09:00 – 17:30, za 09:00 – 17:00<br>maandag en zondag gesloten</span></li>
    <li>{icoon("tel")}<span><b>Contact</b>{TEL_HTML}<br>{MAIL.replace("@", "@<wbr>")}</span></li>
  </ul>
</div></section>
{werkgebiedblok(wit=True)}
{formulier("over-ons")}
""")

    # ---------- Contact ----------
    uren = "".join(f'<div class="uren__rij{" is-dicht" if t == "gesloten" else ""}"><span>{d}</span><span>{t}</span></div>' for d, t in OPENING)
    pagina("/contact", f"Contact en route vanuit Hengelo | {HANDELSNAAM}",
           f"Bel {TEL_TONEN}, stuur een WhatsApp of uw kenteken. Werkplaats: {STRAAT}, Enschede Zuid, {REISTIJD} vanaf Hengelo via de A35. Gratis parkeren.",
           jsonld=[kruimels_jsonld([("Home", "/"), ("Contact", "/contact")])], body=f"""
{kruimels([("Home", "/"), ("Contact", "")])}
<section class="sectie sectie--kort"><div class="wrap">
  <div class="sectie__kop">
    <h1>Contact</h1>
    <p class="intro">Bellen gaat het snelst: binnen een paar minuten weet u wat uw sleutel kost en wanneer u terecht kunt. Zijn wij dicht, app ons dan of vul het formulier in; op de eerstvolgende werkdag reageren wij.</p>
  </div>
  <ul class="contactlijst contactlijst--groot">
    <li><a href="tel:{TEL_LINK}" data-conv="bellen">{icoon("tel")}<span><b>Bellen</b>{TEL_HTML}<small>di – vr 09:00 – 17:30, za tot 17:00</small></span></a></li>
    <li><a href="{WA_LINK}" rel="noopener" data-conv="whatsapp">{icoon("wa")}<span><b>WhatsApp</b>Stuur een foto van uw sleutel<small>met uw kenteken, dan hoort u de prijs</small></span></a></li>
    <li><a href="#kenteken">{icoon("kenteken")}<span><b>Formulier</b>Prijs via kenteken<small>antwoord dezelfde werkdag</small></span></a></li>
  </ul>
</div></section>
<section class="sectie sectie--zand"><div class="wrap twee twee--boven">
  <div>
    <h2>Route vanuit Hengelo</h2>
    <p>Neem vanuit Hengelo de A35 richting Enschede en volg de borden naar Enschede Zuid. De werkplaats zit in het overdekte winkelcentrum aan de Wesseler-Nering; reken op ongeveer {REISTIJD}. Vanuit Borne, Delden en Oldenzaal is het vergelijkbaar. U parkeert gratis.</p>
    <p>Kom op afspraak, dan ligt de juiste sleutel klaar. Start de auto niet? Dan hoeft u niet te komen: <a href="/aan-huis">wij komen naar Hengelo</a>.</p>
    <div class="winkelgegevens">
      <div>
        <h3>{icoon("pin")}Adres</h3>
        <p>{MOEDER}<br>{STRAAT}<br>{POSTCODE} {PLAATS}<br><span class="inspring">{WINKELCENTRUM}</span></p>
        <p><a href="mailto:{MAIL}">{MAIL.replace("@", "@<wbr>")}</a></p>
        <p><a class="knop knop--vol" href="{ROUTE_LINK}" rel="noopener" data-conv="route">{icoon("route")}Routebeschrijving</a></p>
      </div>
      <div>
        <h3>{icoon("klok")}Openingstijden</h3>
        <div class="uren">{uren}</div>
      </div>
    </div>
  </div>
  <figure class="figuur">{foto("werkplaats-voorraad-behuizingen-hengelo.jpg", "Sleutelspecialist bij de voorraadkasten in de werkplaats van Westendorp in Enschede Zuid", lazy=False)}<figcaption>De werkplaats: hier wordt uw sleutel gemaakt</figcaption></figure>
</div></section>
{werkgebiedblok(wit=True)}
{formulier("contact")}
""")

    # ---------- Kennis ----------
    kaarten = "".join(f'<a class="kb" href="/{k["slug"]}"><h2>{k["titel"]}</h2><p>{k["omschr"]}</p><span>Lees verder {icoon("pijl")}</span></a>' for k in KENNIS)
    pagina("/kennis", f"Kennis over autosleutels | {HANDELSNAAM}",
           "Uitleg zonder jargon: natte sleutel, kapotte klapsleutel, occasion met één sleutel, gestolen sleutel, afstandsbediening die niet werkt en zelf programmeren.",
           jsonld=[kruimels_jsonld([("Home", "/"), ("Kennis", "/kennis")])], body=f"""
{kruimels([("Home", "/"), ("Kennis", "")])}
<section class="sectie sectie--kort"><div class="wrap">
  <h1>Kennis over autosleutels</h1>
  <p class="intro">Wat u zelf kunt doen, wanneer u beter even belt, en wat het kost. Geschreven vanuit de werkplaats, in gewone taal.</p>
  <div class="kb-lijst">{kaarten}</div>
</div></section>
{cta()}
{formulier("kennis")}
""")
    for k in KENNIS:
        pad = "/" + k["slug"]
        secties = "".join(f"<h2>{h}</h2><p>{p}</p>" for h, p in k["body"])
        kf = KENNIS_FOTO.get(k["slug"])
        fig = f'<figure class="figuur">{foto(kf[0], kf[1])}<figcaption>{kf[2]}</figcaption></figure>' if kf else ""
        titel = k.get("seotitel") or (k["titel"] + " | " + HANDELSNAAM if len(k["titel"]) <= 40 else k["titel"])
        pagina(pad, titel, k["omschr"],
               jsonld=[artikel_jsonld(k["titel"], pad, k["omschr"], k["datum"], kf[0] if kf else None), faq_jsonld(k["faq"]),
                       kruimels_jsonld([("Home", "/"), ("Kennis", "/kennis"), (k["titel"], pad)])],
               beeld=kf[0] if kf else None, body=f"""
{kruimels([("Home", "/"), ("Kennis", "/kennis"), (k["titel"], "")])}
<article class="sectie sectie--kort"><div class="wrap wrap--tekst artikel">
  <h1>{k["titel"]}</h1>
  <p class="artikel__meta">Geschreven door {HANDELSNAAM}, onderdeel van {MOEDER} · {int(k["datum"][8:10])} {MAANDEN[int(k["datum"][5:7]) - 1]} {k["datum"][:4]}</p>
  {antwoord(k["intro"])}
  {fig}
  {secties}
  <div class="artikel__cta"><p><strong>Hulp nodig?</strong> Bel {TEL_HTML} of stuur een WhatsApp met een foto van uw sleutel en uw kenteken. Nog dezelfde werkdag weet u de prijs. Kunt u niet komen, dan komen wij <a href="/aan-huis">aan huis</a>.</p></div>
</div></article>
{cta()}
{faqblok(k["faq"], "Vragen hierover")}
{formulier("kennis-" + k["slug"])}
""")

    # ---------- Bedankt + privacy ----------
    pagina("/bedankt", f"Bedankt | {HANDELSNAAM}", "Uw aanvraag is verstuurd.", noindex=True, body=f"""
<section class="sectie"><div class="wrap wrap--tekst">
  <h1>Uw aanvraag is verstuurd</h1>
  <p>Wij bekijken uw kenteken en sturen u dezelfde werkdag de prijs, met daarbij wanneer u terecht kunt of wanneer wij bij u kunnen zijn. Heeft u haast? Bel gerust.</p>
  {knoppen(tweede="Naar de homepage", tweede_href="/", tweede_icoon="pijl")}
  <p class="review-tip">{icoon("ster")}Al eerder bij ons geweest? Een korte <a href="{REVIEW_LINK}" rel="noopener" data-conv="review">Google-review voor Autosleutel Hengelo</a> helpt andere automobilisten uit Hengelo ons te vinden.</p>
</div></section>
""")

    pagina("/privacy", f"Privacyverklaring | {HANDELSNAAM}",
           f"Hoe {HANDELSNAAM} ({RECHTSPERSOON}) omgaat met uw persoonsgegevens. Deze site meet geen bezoekers en plaatst geen tracking- of advertentiecookies.",
           jsonld=[kruimels_jsonld([("Home", "/"), ("Privacyverklaring", "/privacy")])], body=f"""
{kruimels([("Home", "/"), ("Privacyverklaring", "")])}
<section class="sectie sectie--kort"><div class="wrap wrap--tekst artikel">
  <h1>Privacyverklaring</h1>
  <p><em>Laatst bijgewerkt: {PRIVACY_DATUM}</em></p>
  <h2>Wie zijn wij</h2>
  <p>{HANDELSNAAM} is een onderdeel van <strong>{RECHTSPERSOON}</strong>, gevestigd aan de {VESTIGING} (KvK {KVK}). Onze werkplaats en winkel zijn te vinden aan de {STRAAT}, {POSTCODE} {PLAATS}. Vragen over privacy: <a href="mailto:{MAIL}">{MAIL}</a> of {TEL_HTML}.</p>
  <h2>Welke gegevens wij verwerken</h2>
  <ul>
    <li><strong>Prijsaanvraag:</strong> kenteken, merk, model en bouwjaar als u die invult, uw keuzes in het formulier, naam, e-mailadres, telefoonnummer als u dat opgeeft, en uw toelichting.</li>
    <li><strong>Kentekencheck:</strong> zodra u een kenteken intypt, vraagt uw browser bij de open data van de RDW merk, model en bouwjaar op, zodat u ziet dat het kenteken klopt. Daarbij worden geen andere gegevens meegestuurd.</li>
    <li><strong>Telefoon, e-mail en WhatsApp:</strong> wat u ons zelf stuurt, inclusief eventuele foto's van uw sleutel.</li>
    <li><strong>Aan huis:</strong> het adres waar de auto staat, alleen voor die afspraak.</li>
    <li><strong>Websitebezoek:</strong> de technische gegevens die nodig zijn om de site te tonen. Bezoekstatistieken houden wij alleen bij als u daar toestemming voor geeft (zie Cookies).</li>
  </ul>
  <h2>Waarvoor</h2>
  <ul>
    <li>Uw aanvraag beantwoorden en een prijs en afspraak geven.</li>
    <li>De opdracht uitvoeren en factureren (wettelijke bewaarplicht).</li>
    <li>Controleren dat u eigenaar of gebruiker van de auto bent (gerechtvaardigd belang: misbruik voorkomen).</li>
  </ul>
  <p>Wij verkopen uw gegevens niet en gebruiken ze niet voor andere doelen.</p>
  <h2>Cookies</h2>
  <p>Deze website plaatst geen statistiekcookies zonder uw toestemming. Bij uw eerste bezoek vragen wij toestemming via de cookiemelding. Geeft u toestemming, dan gebruiken wij Google Analytics en Google Ads om te zien hoe bezoekers op onze website komen en hoe zij onze website gebruiken: welke pagina&#39;s worden bekeken en of iemand contact opneemt (bijvoorbeeld een klik op het telefoonnummer, WhatsApp of het versturen van het formulier). Uw keuze onthouden wij in uw eigen browser en u kunt die altijd wijzigen via &quot;Cookie-instellingen&quot; onderaan elke pagina.</p>
  <h2>Met wie wij gegevens delen</h2>
  <ul>
    <li><strong>Vercel</strong>: hosting van deze website.</li>
    <li><strong>Web3Forms</strong>: verzendt uw formulieraanvraag per e-mail naar ons.</li>
    <li><strong>Google</strong>: lettertypen van deze website (Google Fonts), en met uw toestemming Google Analytics en Google Ads.</li>
    <li><strong>WhatsApp (Meta)</strong>: alleen als u ons zelf via WhatsApp benadert.</li>
  </ul>
  <p>Sommige van deze partijen zijn gevestigd buiten de EU. Doorgifte gebeurt op basis van de waarborgen die de AVG voorschrijft. Daarnaast verstrekken wij gegevens als de wet ons daartoe verplicht.</p>
  <h2>Bewaartermijnen</h2>
  <ul>
    <li>Aanvragen die niet tot een opdracht leiden: uiterlijk 12 maanden.</li>
    <li>Gegevens van opdrachten en facturen: 7 jaar (fiscale bewaarplicht).</li>
    <li>Bezoekstatistieken: maximaal 14 maanden in Google Analytics; meetgegevens van advertenties volgens de bewaartermijnen van Google Ads.</li>
  </ul>
  <h2>Uw rechten</h2>
  <p>U kunt uw gegevens inzien, laten corrigeren of verwijderen, bezwaar maken, de verwerking laten beperken en uw gegevens opvragen. Stuur uw verzoek naar <a href="mailto:{MAIL}">{MAIL}</a>; wij reageren binnen een maand. Klachten kunt u indienen bij de <a href="https://autoriteitpersoonsgegevens.nl" rel="noopener">Autoriteit Persoonsgegevens</a>.</p>
</div></section>
""")
