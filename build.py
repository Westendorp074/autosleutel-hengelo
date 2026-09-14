#!/usr/bin/env python3
# Bouwt de statische site voor autosleutel-hengelo.nl.
# Aanpassen doe je in het CONFIG-blok. Daarna: python build.py
# Foto's: leg originelen in foto-origineel/ en draai python fotos.py; build.py gebruikt img/.
import json, pathlib, html, hashlib

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
TEL_TONEN, TEL_LINK = "053 - 478 42 45", "+31534784245"
WA_LINK = "https://wa.me/31534784245"
MAIL = "autosleutel@westendorpgroep.nl"
KVK, BTW = "91885124", "097701993B01"
LAT, LON = 52.1929, 6.8886
SINDS = 1985
PER_JAAR = "1.500"
AAN_HUIS_VANAF = "45"
REISTIJD = "15 minuten"
GBP_LINK = "https://share.google/j46orGZulGyU4amTy"   # Google-bedrijfsprofiel Autosleutel Hengelo (deellink)
REVIEW_LINK = "https://g.page/r/CakJOOdkl5gzEAE/review"   # "Vraag om reviews"-link uit het Hengelo-profiel
ROUTE_LINK = "https://maps.app.goo.gl/1DX8q4eZJTdBvAbd8"   # Maps-vermelding werkplaats Enschede (Westendorp Sleutel- en Slotenspecialist)
GBP_SCORE, GBP_AANTAL = "", 0   # invullen zodra er reviews zijn; leeg = niets tonen
WEB3FORMS_KEY = "a64f80df-574c-43c9-b15c-f67332fd1a3f"   # eigen key voor deze site (web3forms.com, 13-9-2026)
PRIVACY_DATUM = "13 september 2026"

OPENING = [("Maandag", "gesloten"), ("Dinsdag", "09:00 – 17:30"), ("Woensdag", "09:00 – 17:30"),
           ("Donderdag", "09:00 – 17:30"), ("Vrijdag", "09:00 – 17:30"),
           ("Zaterdag", "09:00 – 17:00"), ("Zondag", "gesloten")]

# Werkgebied: bewust de Hengelo-kant van Twente. Almelo e.o. is autosleutel-almelo.nl,
# Enschede zelf is autosleutel-enschede.nl.
PLAATSEN = ["Hengelo", "Borne", "Delden", "Goor", "Haaksbergen", "Oldenzaal", "Losser",
            "Denekamp", "Weerselo", "Hengevelde", "Beckum", "Deurningen"]

# Richtprijzen (zelfde werkplaats en tarieven als de andere vestigingen, anders verwoord)
# Alle sleutels kwijt (geen werkend exemplaar): GEEN prijs noemen, verschilt te sterk per merk/bouwjaar (eigenaar 13-9-2026).
P_KOPIE, P_NIEUW, P_SMART, P_REP = "€ 60 – € 120", "Prijs op aanvraag", "€ 150 – € 300", "€ 30 – € 80"
# Schatting wat de dealer meestal rekent (opgave eigenaar 14-09-2026). Altijd als schatting tonen.
DEALER = {"transpondersleutel-bijmaken": "€ 150 of meer", "klapsleutel-bijmaken": "€ 400 – € 700", "smartkey-bijmaken": "€ 400 – € 1.500",
          "sleutelkaart-bijmaken": "€ 400 – € 700", "autosleutel-reparatie": "nieuwe sleutel vanaf € 400"}
P_KLAP, P_KAART = "€ 130 – € 200", "€ 130 – € 250"   # klapsleutel en sleutelkaart: vanaf € 130 (eigenaar 13-9-2026)

# ============================================================
# Sleuteltypen — de ruggengraat van deze site
# ============================================================
SLEUTELTYPEN = [
    dict(slug="klapsleutel-bijmaken", naam="Klapsleutel", kop="Klapsleutel bijmaken",
         icoon="klap", prijs_kopie=P_KLAP, prijs_nieuw=P_NIEUW,
         kort="De sleutel met de uitklapbare baard en knopjes op de behuizing.",
         herken="De metalen baard klapt met een knop uit de behuizing. Op de behuizing zitten twee of drie knopjes.",
         merken="Volkswagen, Audi, Seat, Skoda, Opel, Ford, Fiat, Hyundai, Kia, Peugeot, Citroën",
         foto="opel-astra-klapsleutel-bijmaken.jpg", alt="Twee bijgemaakte Opel-klapsleutels voor een grijze Opel Astra",
         antwoord=f"Een klapsleutel bijmaken kost {P_KLAP} als u nog een werkende sleutel heeft. Daar zit alles in: de "
                  "behuizing, het frezen van de baard, de chip en het inleren van de afstandsbediening. In de meeste "
                  "gevallen is de sleutel klaar terwijl u wacht. Bent u alle sleutels kwijt, dan verschilt de prijs sterk "
                  "per merk en bouwjaar; u krijgt vooraf een vaste prijs op basis van uw kenteken.",
         tekst=[
             ("Wat er in een klapsleutel zit",
              "Drie dingen tegelijk: een gefreesde baard die het slot opent, een transponderchip die de "
              "startonderbreker vrijgeeft, en een zender voor het openen op afstand. Alle drie moeten kloppen, "
              "anders start de auto niet of gaan de deuren niet open. Wij doen ze alle drie in één bezoek."),
             ("Kapotte klapsleutel: repareren is vaak genoeg",
              "Klapt de baard niet meer uit, is de behuizing gebroken of doen de knopjes niets meer? Dan hoeft er "
              "meestal geen nieuwe sleutel te komen. Uw chip en zender gaan over in een nieuwe behuizing en de baard "
              "wordt opnieuw gefreesd. Dat kost " + P_REP + " en u hoeft niets te programmeren."),
             ("Wat u meeneemt",
              "Uw kenteken volstaat voor de prijs. Komt u langs, neem dan het kentekenbewijs en een geldig "
              "identiteitsbewijs mee. Heeft u nog een werkende sleutel, breng die dan mee: dan kopiëren wij de chip "
              "en is het goedkoper en sneller."),
         ],
         faq=[("Waarom kost een klapsleutel meer dan een gewone sleutel?",
               "Omdat er een zender in zit voor het openen op afstand. Die moet apart worden ingeleerd op de auto. "
               "Een sleutel met alleen een chip is daardoor goedkoper."),
              ("Mijn klapsleutel klapt niet meer uit. Moet ik een nieuwe?",
               "Nee. Meestal is de veer of het scharnier versleten. Een nieuwe behuizing met uw eigen chip en "
               "zender erin lost dat op, voor " + P_REP + ".")]),
    dict(slug="smartkey-bijmaken", naam="Smartkey", kop="Smartkey / keyless sleutel bijmaken",
         icoon="smart", prijs_kopie=P_SMART, prijs_nieuw=P_NIEUW,
         kort="U start met een knop; de sleutel blijft in uw zak of tas.",
         herken="Uw auto heeft een startknop. De sleutel heeft vaak geen zichtbare baard, of een noodsleutel die uit de behuizing schuift.",
         merken="BMW, Mini, Mercedes-Benz, Volvo, Jaguar, Land Rover, Jeep, Nissan, Toyota, Hyundai, Kia, Ford",
         foto="bmw-x1-smartkey-bijmaken.jpg", alt="Twee BMW-smartkeys bijgemaakt voor een BMW X1",
         antwoord=f"Een smartkey bijmaken kost {P_SMART}, inclusief het inleren op de auto. Keyless systemen zijn "
                  "zwaarder beveiligd dan een klapsleutel, dus het programmeren duurt langer en vraagt apparatuur per "
                  "merk. Voor de meeste merken en bouwjaren doen wij het in eigen huis; voor een enkel zeer recent "
                  "model is de dealer nodig, en dat hoort u vooraf.",
         tekst=[
             ("Hoe een smartkey werkt",
              "De auto en de sleutel praten draadloos met elkaar. Komt u bij de auto, dan herkent hij de sleutel in "
              "uw zak en gaan de deuren open. Drukt u op de startknop, dan controleert de auto opnieuw of de juiste "
              "sleutel aanwezig is. Daarom moet een nieuwe smartkey exact op uw auto worden ingeleerd."),
             ("Eén sleutel is te weinig",
              "Veel auto's met keyless worden met één sleutel verkocht. Raakt die kwijt, dan is de auto niet te "
              "starten en niet te openen. Een tweede smartkey laten maken terwijl de eerste nog werkt, is goedkoper en "
              "een stuk minder stress dan een nieuwe sleutel zonder werkend exemplaar."),
             ("Smartkey kapot of nat geweest",
              "Doet de smartkey niets meer na een wasbeurt of een val? Vaak is de elektronica te redden of is alleen "
              "de batterij of de behuizing aan vervanging toe. Wij kijken eerst of repareren kan; dat scheelt u een "
              "nieuwe sleutel."),
         ],
         faq=[("Kan ik met een lege smartkey-batterij nog starten?",
               "Meestal wel: houd de sleutel tegen de startknop of op de plek die in het instructieboekje staat. "
               "Lukt dat niet, bel ons dan even."),
              ("Waarom is een smartkey duurder?",
               "De sleutel zelf is duurder in inkoop en het inleren vraagt merkspecifieke apparatuur en meer tijd.")]),
    dict(slug="sleutelkaart-bijmaken", naam="Sleutelkaart", kop="Sleutelkaart bijmaken",
         icoon="kaart", prijs_kopie=P_KAART, prijs_nieuw=P_NIEUW,
         kort="De platte kaart die u in het dashboard schuift of gewoon bij u houdt.",
         herken="Een platte kaart van ongeveer creditcardformaat, met knopjes. Bekend van Renault, Dacia en Mercedes.",
         merken="Renault, Dacia, Mercedes-Benz",
         foto="renault-kadjar-sleutelkaart-bijmaken.jpg", alt="Twee Renault-sleutelkaarten bijgemaakt voor een Renault Kadjar",
         antwoord=f"Een sleutelkaart bijmaken kost {P_KAART}. Renault-kaarten (Mégane, Scénic, Clio, Captur, Kadjar) "
                  "maken wij inclusief het inleren op de auto. Een kaart waarvan de knopjes het niet meer doen, "
                  "repareren wij vaak voor " + P_REP + ".",
         tekst=[
             ("Waarom sleutelkaarten vaak kapotgaan",
              "Een kaart zit in een broekzak, buigt mee en krijgt klappen. De knopjes slijten, de behuizing scheurt bij "
              "de noodsleutel, of de kaart wordt niet meer herkend in de lezer. In veel gevallen is de elektronica nog "
              "goed en is een nieuwe behuizing voldoende."),
             ("Handsfree of insteekkaart",
              "Er zijn kaarten die u in het dashboard schuift en handsfree kaarten waarmee de auto vanzelf opent. "
              "Beide maken wij bij. Zeg bij uw aanvraag welke u heeft, dan ligt de juiste kaart klaar."),
             ("Alle kaarten kwijt",
              "Ook zonder werkende kaart kunnen wij bij de meeste Renault-modellen een nieuwe inleren. Neem het "
              "kentekenbewijs en een identiteitsbewijs mee; wij wissen de oude kaarten uit het geheugen van de auto."),
         ],
         faq=[("Mijn Renault zegt 'kaart niet herkend'. Is de kaart stuk?",
               "Vaak is de batterij leeg of zijn de contacten in de kaart versleten. Wij testen dat in een paar minuten."),
              ("Kunnen jullie de kaart van een Mercedes ook maken?",
               "Voor de meeste Mercedes-modellen wel. Bij een enkel recent model is een bestelling via de dealer nodig; "
               "dat zeggen wij vooraf.")]),
    dict(slug="transpondersleutel-bijmaken", naam="Transpondersleutel", kop="Transpondersleutel bijmaken",
         icoon="chip", prijs_kopie=P_KOPIE, prijs_nieuw=P_NIEUW,
         kort="De 'gewone' sleutel met een chip in de kop, met of zonder knopjes.",
         herken="Een vaste metalen baard met een kunststof kop. Er zit een chip in die u niet ziet. Vanaf ongeveer 1998 heeft bijna elke auto er een.",
         merken="Toyota, Suzuki, Nissan, Dacia, oudere Volkswagen, Opel, Ford, Peugeot, Citroën, bestelwagens",
         foto="werkplaats-voorraad-autosleutel-behuizingen.jpg", alt="Voorraadkasten met sleutels, chips en behuizingen per merk in de werkplaats",
         antwoord=f"Een transpondersleutel kopiëren kost {P_KOPIE}. Heeft u geen werkende sleutel meer, dan maken wij "
                  "een nieuwe en leren die in op de auto; de prijs daarvan hangt sterk af van merk en bouwjaar en hoort u "
                  "vooraf via uw kenteken. Een sleutel zonder chip past wel in het slot, "
                  "maar de auto start er niet mee. Daarom is een autosleutel bijmaken programmeerwerk, geen slijpwerk.",
         tekst=[
             ("Wat de chip doet",
              "Steekt u de sleutel in het contact, dan stelt de auto de chip een versleutelde vraag. Alleen bij het "
              "juiste antwoord geeft de startonderbreker de motor vrij. Wij kopiëren die chip, of leren een nieuwe chip "
              "in op uw auto."),
             ("Ook voor bestelwagens",
              "Transit, Vivaro, Transporter, Ducato, Berlingo: bestelwagens rijden vaak jaren rond op één sleutel. Een "
              "reservesleutel is bij een bedrijfswagen geen luxe. Die maken wij op dezelfde manier als bij een "
              "personenauto."),
             ("Versleten baard",
              "Gaat het slot steeds stroever, dan is de baard vaak versleten. Wij frezen een nieuwe sleutel op code, "
              "niet als kopie van de versleten baard, zodat hij weer soepel draait."),
         ],
         faq=[("Mijn sleutel heeft geen knopjes. Zit er dan wel een chip in?",
               "Bij auto's vanaf ongeveer 1998 vrijwel altijd. Wij lezen het in een paar seconden uit."),
              ("Kan de sleutelmaker in het winkelcentrum dit ook?",
               "Een baard slijpen wel, maar zonder het programmeren van de chip start de auto niet.")]),
    dict(slug="autosleutel-reparatie", naam="Reparatie", kop="Autosleutel repareren",
         icoon="rep", prijs_kopie=P_REP, prijs_nieuw=P_REP,
         kort="Knopjes, behuizing, veer of losse chip: repareren is bijna altijd goedkoper.",
         herken="De sleutel werkt half: knopjes reageren slecht, de behuizing is gebroken, de baard zit los of de auto herkent de sleutel af en toe niet.",
         merken="alle merken",
         foto="werkplaats-autosleutel-reparatie-werkbank.jpg", alt="Sleutelspecialist repareert een autosleutel aan de werkbank in de werkplaats in Enschede",
         antwoord=f"Een autosleutel repareren kost {P_REP}. Uw eigen chip en zender blijven zitten, dus er hoeft niets "
                  "opnieuw geprogrammeerd te worden. Dat is de goedkoopste route en meestal binnen een half uur klaar.",
         tekst=[
             ("Wat wij repareren",
              "Versleten of afgebroken knopjes, gescheurde behuizingen, klapveren die niet meer uitklappen, losgeraakte "
              "chips, batterijcontacten met corrosie en waterschade. Wij solderen op componentniveau en vervangen "
              "alleen wat kapot is."),
             ("Nieuwe behuizing, zelfde sleutel",
              "Is de behuizing op, dan zetten wij uw elektronica over in een nieuwe behuizing en frezen wij de baard "
              "opnieuw. Voor de auto is het dezelfde sleutel; voor u voelt hij als nieuw."),
             ("Wanneer repareren niet meer kan",
              "Is de printplaat gebroken of de chip beschadigd, dan is een nieuwe sleutel nodig. Dat zien wij snel, en "
              "dan zeggen wij het ook. U betaalt geen reparatie die niet gaat werken."),
         ],
         faq=[("Ik heb een nieuwe batterij geplaatst en nu doet de sleutel niets. Wat nu?",
               "Vaak ligt de batterij verkeerd om, of is een contactlipje verbogen. Soms moet de sleutel opnieuw "
               "worden gesynchroniseerd. Kom even langs, dat is zo gedaan."),
              ("Kunnen jullie een sleutelbehuizing van internet monteren?",
               "Meestal wel, maar wij zien vaak behuizingen die net niet passen. Onze behuizingen passen op de "
               "originele elektronica.")]),
]
# Volgorde op de site (wens eigenaar): transpondersleutel, klapsleutel, smartkey, sleutelkaart, reparatie.
_VOLGORDE = ["transpondersleutel-bijmaken", "klapsleutel-bijmaken", "smartkey-bijmaken", "sleutelkaart-bijmaken", "autosleutel-reparatie"]
SLEUTELTYPEN.sort(key=lambda t: _VOLGORDE.index(t["slug"]))

# ============================================================
# Merken — alleen inhoud die per merk echt anders is
# ============================================================
MERKEN = [
    ("Volkswagen", "volkswagen", ["klap", "smart"],
     "Golf, Polo, Passat, Tiguan, Transporter en Caddy: bij Volkswagen is de klapsleutel de standaard. Nieuwere "
     "modellen (globaal vanaf 2014) hebben een zwaarder beveiligde generatie sleutels, waarvoor wij aparte apparatuur "
     "gebruiken. Keyless Volkswagens hebben een smartkey met noodsleutel in de behuizing.",
     "Voor een reservesleutel hebben wij uw werkende sleutel en het kenteken nodig. Bent u alle sleutels kwijt, dan "
     "kan het bij de meeste modellen ook, maar duurt het langer. Enkele zeer recente modellen kunnen alleen via de "
     "dealer.", "volkswagen"),
    ("Audi", "audi", ["klap", "smart"],
     "Audi deelt de techniek met Volkswagen: klapsleutels bij A1 tot A6 van oudere bouwjaren, smartkeys bij de "
     "nieuwere generaties met startknop. De behuizingen slijten bij Audi vaak bij de klapveer en de knopjes.",
     "Reparatie van de behuizing is bij Audi vrijwel altijd mogelijk met behoud van uw eigen elektronica.", "audi"),
    ("Seat", "seat", ["klap", "smart"],
     "Ibiza, Leon, Arona en Ateca hebben dezelfde sleutelgeneraties als Volkswagen. Klapsleutels kopiëren wij "
     "meestal terwijl u wacht.", "", "seat"),
    ("Skoda", "skoda", ["klap", "smart"],
     "Fabia, Octavia, Kodiaq en Karoq: klapsleutel of smartkey, afhankelijk van uitvoering. Zelfde techniek als "
     "Volkswagen, zelfde werkwijze.", "", "skoda"),
    ("BMW", "bmw", ["smart", "chip"],
     "Bij BMW ziet u het bouwjaar aan de sleutel: de oudere ruitvormige sleutel, de smartkey met sleufsysteem, en "
     "de nieuwe generatie smartkeys met display of zonder baard. Wij maken ze alle drie bij, inclusief het "
     "inleren op de auto.",
     "Op de foto: twee smartkeys voor een BMW X1, gemaakt in onze werkplaats. Bij modellen met de nieuwste "
     "beveiliging kan een bestelling via BMW nodig zijn; dat hoort u bij de prijsopgave.", "bmw",
     "bmw-x1-smartkey-bijmaken.jpg", "Twee BMW-smartkeys bijgemaakt voor een BMW X1"),
    ("Mini", "mini", ["smart", "chip"],
     "Mini gebruikt de techniek van BMW. De ronde smartkey van de Cooper, Countryman en Clubman maken wij bij en "
     "leren wij in. Ook de oudere sleutels met ronde kop zijn geen probleem.", "", "mini",
     "mini-clubman-smartkey-bijmaken.jpg", "Twee Mini-smartkeys bijgemaakt voor een Mini Clubman"),
    ("Mercedes-Benz", "mercedes-benz", ["smart", "kaart"],
     "Mercedes werkt met infraroodsleutels (de chromen sleutel met knopjes) en met keyless-go smartkeys. Het "
     "programmeren gaat via de auto zelf en vraagt merkspecifieke apparatuur. Voor de meeste modellen tot en met de "
     "huidige generatie kunnen wij dat.",
     "Bij een enkel zeer recent model is een bestelling via Mercedes de enige weg. Wij checken dat vooraf op "
     "kenteken, zodat u niet voor niets komt.", "mercedes"),
    ("Opel", "opel", ["klap", "smart"],
     "Corsa, Astra, Insignia, Zafira, Mokka: klapsleutels met twee of drie knopjes. De nieuwere Opels (vanaf de "
     "samenwerking met Peugeot en Citroën) hebben dezelfde sleutels als die merken.",
     "Op de foto: twee klapsleutels voor een Opel Astra. Een versleten Opel-klapsleutel is vaak te repareren met een "
     "nieuwe behuizing.", "opel",
     "opel-astra-klapsleutel-bijmaken.jpg", "Twee bijgemaakte Opel-klapsleutels voor een grijze Opel Astra"),
    ("Ford", "ford", ["klap", "smart", "chip"],
     "Fiesta, Focus, Kuga, Transit en Mustang: van de klassieke sleutel met chip tot de smartkey. Bij Ford zit het "
     "programmeren ingebouwd in de auto; wij lezen het uit en leren de nieuwe sleutel in.",
     "Ook bij Ford-bestelwagens is een reservesleutel de moeite waard: een Transit zonder sleutel staat stil.", "ford",
     "ford-mustang-autosleutel-bijmaken.jpg", "Twee bijgemaakte klapsleutels voor een Ford Mustang"),
    ("Peugeot", "peugeot", ["klap", "smart"],
     "208, 308, 2008, 3008, Partner en Expert: klapsleutels en smartkeys. Bij oudere Peugeots (tot ongeveer 2005) is "
     "een pincode uit de autopapieren nodig; heeft u die niet, dan vragen wij hem op.", "", "peugeot"),
    ("Citroën", "citroen", ["klap", "smart"],
     "C1, C3, C4, Berlingo en de Picasso-modellen delen hun techniek met Peugeot. Klapsleutel of smartkey, "
     "afhankelijk van bouwjaar en uitvoering.",
     "Op de foto: twee smartkeys voor een Citroën C4 Picasso.", "citroen",
     "citroen-c4-picasso-smartkey-bijmaken.jpg", "Twee smartkeys bijgemaakt voor een Citroën C4 Picasso"),
    ("Renault", "renault", ["kaart", "klap"],
     "Renault is het merk van de sleutelkaart: Mégane, Scénic, Laguna, Clio, Captur en Kadjar. Wij maken kaarten bij, "
     "leren ze in en repareren kaarten met versleten knopjes. Oudere Renaults en bestelwagens hebben een gewone "
     "sleutel met chip of een klapsleutel.",
     "Op de foto: twee handsfree sleutelkaarten voor een Renault Kadjar.", "renault",
     "renault-kadjar-sleutelkaart-bijmaken.jpg", "Twee Renault-sleutelkaarten bijgemaakt voor een Renault Kadjar"),
    ("Dacia", "dacia", ["chip", "klap", "kaart"],
     "Sandero, Duster, Logan en Dokker: eenvoudige sleutels met chip, klapsleutels en bij nieuwere modellen de "
     "Renault-kaart. Snel en betaalbaar bij te maken.", "", "dacia"),
    ("Toyota", "toyota", ["chip", "smart"],
     "Yaris, Aygo, Auris, Corolla, C-HR en RAV4: bij oudere Toyota's een sleutel met chip, bij de hybrides vrijwel "
     "altijd een smartkey. Toyota's zijn goed te programmeren; ook zonder werkende sleutel.", "", "toyota"),
    ("Hyundai", "hyundai", ["klap", "smart"],
     "i10, i20, i30, Kona en Tucson: klapsleutel of smartkey. Hyundai-sleutels leren wij via de OBD-aansluiting in, "
     "meestal binnen een half uur.",
     "Op de foto: twee Hyundai-sleutels worden ingeleerd via de diagnoseaansluiting.", "hyundai",
     "autosleutel-programmeren-hyundai.jpg", "Twee Hyundai-sleutels worden ingeleerd via de OBD-aansluiting"),
    ("Kia", "kia", ["klap", "smart"],
     "Picanto, Rio, Ceed, Sportage en Niro gebruiken dezelfde techniek als Hyundai. Klapsleutels en smartkeys "
     "maken wij bij en leren wij in.", "", "kia"),
    ("Fiat", "fiat", ["klap", "chip"],
     "500, Panda, Punto, Tipo en Ducato: de klapsleutel met het ronde Fiat-logo is de bekendste. De behuizing en de "
     "knopjes slijten hard; repareren kan bijna altijd.",
     "Op de foto: een Fiat 500 met originele en bijgemaakte klapsleutel.", "fiat",
     "fiat-500-klapsleutel-bijmaken.jpg", "Fiat 500 met originele en bijgemaakte klapsleutel"),
    ("Volvo", "volvo", ["smart", "klap"],
     "V40, V60, XC40, XC60 en XC90: bij de nieuwere Volvo's een smartkey, bij oudere een sleutel met chip of "
     "klapsleutel. Voor sommige recente Volvo's moet de sleutel via Volvo worden besteld; dat checken wij op "
     "kenteken.", "", "volvo"),
    ("Nissan", "nissan", ["smart", "chip"],
     "Qashqai, Juke, Micra en X-Trail: de 'Intelligent Key' smartkey bij de meeste modellen, een sleutel met chip bij "
     "de oudere. Beide maken wij bij.", "", "nissan"),
    ("Jeep", "jeep", ["smart", "klap"],
     "Renegade, Compass en Cherokee: smartkeys en klapsleutels. Jeep deelt de techniek met Fiat en Alfa Romeo.",
     "Op de foto: twee smartkeys voor een Jeep Compass.", "jeep",
     "jeep-compass-smartkey-bijmaken.jpg", "Sleutelspecialist met handschoen toont twee smartkeys voor een witte Jeep Compass"),
    ("Jaguar", "jaguar", ["smart"],
     "XE, XF, F-Pace en E-Pace: smartkeys met keyless entry. Jaguar deelt de sleuteltechniek met Land Rover.",
     "Op de foto: een Jaguar XF met originele en bijgemaakte smartkey.", "jaguar",
     "jaguar-xf-smartkey-bijmaken.jpg", "Jaguar XF met originele en bijgemaakte smartkey"),
    ("Land Rover", "land-rover", ["smart"],
     "Evoque, Discovery Sport, Defender en Range Rover: smartkeys. Voor een reservesleutel hebben wij uw werkende "
     "sleutel en het kenteken nodig; zonder sleutel kan het bij de meeste modellen ook.", "", "landrover"),
]
TYPE_NAAM = {"klap": "Klapsleutel", "smart": "Smartkey", "kaart": "Sleutelkaart", "chip": "Transpondersleutel", "rep": "Reparatie"}
TYPE_SLUG = {"klap": "klapsleutel-bijmaken", "smart": "smartkey-bijmaken", "kaart": "sleutelkaart-bijmaken",
             "chip": "transpondersleutel-bijmaken", "rep": "autosleutel-reparatie"}

# ============================================================
# Kennis — onderwerpen die op autosleutel-almelo.nl NIET staan
# ============================================================
KENNIS = [
    dict(slug="autosleutel-nat-geworden", titel="Autosleutel nat geworden of in de wasmachine: wat nu?",
         omschr="Sleutel in het water of door de was? Zo vergroot u de kans dat hij het overleeft, en dit kunnen wij nog redden.",
         intro="Haal de batterij eruit, druk op geen enkele knop en laat de sleutel minstens een dag drogen. Werkt hij daarna "
               "nog niet, dan is de elektronica vaak nog te repareren. Wacht niet weken: corrosie wordt elke dag erger.",
         body=[
             ("Meteen doen", "Batterij eruit, behuizing open als dat kan, en drogen op een warme, droge plek. Niet op de "
              "verwarming, niet met een föhn. Rijst helpt niet meer dan gewone lucht. Druk niet op de knopjes: met water "
              "op de printplaat kan dat kortsluiting geven."),
             ("Zoet water of iets anders", "Regen en kraanwater zijn het minst erg. Zeepwater uit de wasmachine, zeewater of "
              "frisdrank laten resten achter die de contacten aantasten. Dan is schoonmaken in de werkplaats nodig, ook "
              "als de sleutel het nog lijkt te doen."),
             ("Wat wij kunnen redden", "Wij openen de sleutel, reinigen de printplaat en solderen contacten en knopjes "
              "opnieuw. Vaak werkt de sleutel daarna weer, voor " + P_REP + ". Is de chip beschadigd, dan is een nieuwe "
              "sleutel nodig. Dat zien wij snel."),
             ("Een reservesleutel voorkomt dit", "Met een tweede sleutel is een natte sleutel een ongemak, geen "
              "noodgeval. Heeft u er maar één, laat dan nu een kopie maken."),
         ],
         faq=[("Mijn sleutel doet het na het drogen weer. Ben ik klaar?",
               "Vaak wel, maar laat hem nakijken als u in zeepwater of zeewater bent geweest. Resten blijven vreten."),
              ("Helpt rijst?", "Nee. Droge lucht werkt net zo goed; rijst laat stof en zetmeel achter in de sleutel.")]),
    dict(slug="klapsleutel-veer-kapot", titel="Klapsleutel klapt niet meer uit: veer of behuizing kapot",
         omschr="Een klapsleutel die niet meer uitklapt, is bijna altijd te repareren. Wat er kapot is en wat het kost.",
         intro="Klapt de baard niet meer uit, of blijft hij hangen? Meestal is de veer gebroken of het scharnier "
               "versleten. Een nieuwe behuizing met uw eigen chip en zender erin kost " + P_REP + ", zonder programmeren.",
         body=[
             ("Wat er stuk is", "In het scharnier zit een kleine veer die de baard uitklapt. Die breekt na jaren dagelijks "
              "gebruik. Soms is het kunststof rond het scharnier uitgesleten, waardoor de baard los in de behuizing "
              "zit."),
             ("Waarom u niet zelf een behuizing bestelt", "Behuizingen van internet passen vaak net niet op de originele "
              "printplaat, of de knopjes zitten anders. Wij zetten uw elektronica over in een behuizing die past, en "
              "frezen de nieuwe baard op code."),
             ("Hoe lang het duurt", "Een nieuwe behuizing is meestal binnen een half uur klaar. Uw sleutel blijft dezelfde "
              "sleutel voor de auto: niets hoeft opnieuw ingeleerd."),
         ],
         faq=[("De baard klapt uit, maar draait moeilijk in het slot.",
               "Dan is de baard versleten. Wij frezen een nieuwe op code, zodat hij weer soepel draait."),
              ("Kan ik met een losse baard rijden?", "Even wel, maar hij kan afbreken in het slot. Laat het snel maken.")]),
    dict(slug="tweedehands-auto-een-sleutel", titel="Tweedehands auto gekocht met maar één sleutel?",
         omschr="Een occasion met één sleutel is een risico. Wat u meteen regelt en waarom dat nu goedkoper is dan later.",
         intro="Laat direct een tweede sleutel maken. Nu kost dat een kopie (" + P_KOPIE + "); raakt die ene sleutel "
               "later kwijt, dan wordt het een nieuwe sleutel zonder werkend exemplaar: fors duurder, afhankelijk van merk "
               "en bouwjaar, en de auto staat stil tot het geregeld is.",
         body=[
             ("Waarom occasions vaak met één sleutel komen", "Sleutels raken kwijt bij inruil, blijven achter bij de vorige "
              "eigenaar of gaan verloren bij de handel. De verkoper geeft wat hij heeft. Voor u betekent het dat alles "
              "afhangt van één sleutel."),
             ("Wissen wat u niet kent", "Weet u niet waar de andere sleutels zijn? Bij veel modellen kunnen wij alle "
              "onbekende sleutels uit het geheugen van de auto wissen en alleen uw sleutels inleren. Dan kan niemand "
              "met een oude sleutel uw auto openen of starten."),
             ("Wat u nodig heeft", "Kentekenbewijs op uw naam, een identiteitsbewijs en de sleutel die u heeft. Uw kenteken "
              "is genoeg voor de prijs vooraf."),
         ],
         faq=[("De verkoper zegt dat een tweede sleutel bij de dealer € 400 kost. Klopt dat?",
               "Bij de dealer vaak wel. Bij ons kost een kopie " + P_KOPIE + " en is hij meestal dezelfde dag klaar."),
              ("Ik heb een sleutel zonder afstandsbediening gekregen. Kan dat ook?",
               "Ja, wij kunnen een reservesleutel met afstandsbediening maken als uw auto dat ondersteunt.")]),
    dict(slug="autosleutel-gestolen", titel="Autosleutel gestolen: zo voorkomt u dat iemand met uw auto wegrijdt",
         omschr="Gestolen sleutel, of gestolen samen met uw adres? Dit doet u vandaag nog, en wat wij kunnen wissen.",
         intro="Doe aangifte, bel uw verzekeraar en laat de gestolen sleutel uit het geheugen van de auto wissen. Bij "
               "veel modellen kunnen wij dat, samen met het inleren van een nieuwe sleutel. Daarna is de gestolen "
               "sleutel waardeloos.",
         body=[
             ("Sleutel gestolen mét adres", "Is uw tas met sleutel en papieren gestolen, dan weet de dief waar de auto "
              "staat. Zet de auto zo mogelijk ergens anders neer en laat de sleutel dezelfde of de volgende dag "
              "wissen."),
             ("Wissen in plaats van slot vervangen", "Vroeger moest het hele slot vervangen worden. Nu wissen wij bij de "
              "meeste auto's de oude sleutel uit het geheugen: hij start de auto niet meer. Het slot zelf hoeft "
              "zelden vervangen te worden."),
             ("Keyless en relay-diefstal", "Bij een smartkey kunnen dieven het signaal versterken terwijl de sleutel binnen "
              "ligt. Bewaar een smartkey in een afgeschermd hoesje of ver van de voordeur. Sommige smartkeys kunt u "
              "in slaapstand zetten; wij laten u zien hoe."),
         ],
         faq=[("Vergoedt de verzekering een nieuwe sleutel na diefstal?",
               "Vaak wel bij een WA+ of allrisk-dekking. Vraag het na en bewaar de aangifte."),
              ("Moet ik wachten op de verzekeraar voordat ik de sleutel laat wissen?",
               "Nee. Wissen voorkomt diefstal van de auto; dat wil de verzekeraar ook.")]),
    dict(slug="afstandsbediening-werkt-niet", titel="Afstandsbediening van de autosleutel werkt niet meer",
         omschr="Deuren gaan niet meer open met de knopjes? Loop dit stappenplan door voordat u een nieuwe sleutel koopt.",
         intro="In de meeste gevallen is het de batterij, versleten knopjes of een sleutel die opnieuw gesynchroniseerd "
               "moet worden. Een nieuwe sleutel is zelden nodig; een reparatie kost " + P_REP + ".",
         body=[
             ("Stap 1: batterij", "Vervang de batterij (meestal CR2032 of CR2025). Let op de plus-kant en op de "
              "contactlipjes. Werkt de sleutel dichtbij de auto wel maar op afstand niet, dan is de batterij bijna "
              "leeg."),
             ("Stap 2: knopjes", "Werkt één knopje niet en de andere wel? Dan is de drukknop op de printplaat versleten. "
              "Die solderen wij opnieuw."),
             ("Stap 3: synchroniseren", "Sommige merken 'vergeten' de sleutel na een lege batterij. Dan moet de sleutel "
              "opnieuw met de auto worden gesynchroniseerd. Bij het ene merk kan dat met een knopvolgorde, bij het "
              "andere alleen met apparatuur."),
             ("Stap 4: de auto zelf", "Werkt geen enkele sleutel meer op afstand, dan zit het probleem in de ontvanger of "
              "de zekering van de auto. Dan is de sleutel niet de schuldige."),
         ],
         faq=[("Start de auto nog wel als de afstandsbediening niet werkt?",
               "Ja, de chip voor het starten werkt zonder batterij. U opent de deur met de baard of noodsleutel."),
              ("Wat kost een nieuwe afstandsbediening?",
               "Repareren kost " + P_REP + ". Alleen als de zender echt stuk is, is een nieuwe sleutel nodig.")]),
    dict(slug="zelf-autosleutel-programmeren", titel="Kunt u zelf een autosleutel programmeren?",
         omschr="Met een goedkoop OBD-apparaat en een sleutel van internet? Wanneer dat werkt, en wanneer u de auto ermee blokkeert.",
         intro="Bij een handvol oudere modellen kan het, met de juiste procedure. Bij de meeste auto's van na 2010 niet: "
               "de beveiliging vraagt apparatuur en toegangscodes die u als particulier niet krijgt. Een mislukte "
               "poging kan de startonderbreker blokkeren.",
         body=[
             ("Waar het wel kan", "Sommige oudere Fords, Toyota's en Nissans hebben een inleerprocedure met de sleutels en "
              "het contact, zonder apparatuur. Dat staat dan in het instructieboekje en vraagt twee werkende sleutels."),
             ("Waar het misgaat", "Goedkope OBD-apparaten van internet werken met verouderde gegevens. Zij kunnen een "
              "auto in een beveiligingsstand zetten waaruit alleen de dealer of een specialist hem haalt. De sleutel "
              "zelf moet bovendien de juiste chip en frequentie hebben; 'universeel' bestaat niet."),
             ("Wat wij anders doen", "Wij werken met apparatuur per merk, actuele software en originele of gelijkwaardige "
              "sleutels uit voorraad. En als een sleutel niet kan, zeggen wij dat vooraf."),
         ],
         faq=[("Ik heb online een sleutel gekocht. Kunnen jullie die inleren?",
               "Soms. Breng hem mee; wij checken chip en frequentie. Past hij niet, dan hebben wij de juiste op voorraad."),
              ("Wat als mijn auto na een mislukte poging niet meer start?",
               "Bel ons. Vaak kunnen wij de startonderbreker resetten en alsnog een sleutel inleren.")]),
]
# Foto per kennisartikel (bestand, alt, onderschrift)
KENNIS_FOTO = {
    "autosleutel-nat-geworden": ("werkplaats-autosleutel-reparatie-werkbank.jpg", "Sleutelspecialist repareert de elektronica van een autosleutel aan de werkbank", "Natte elektronica repareren wij op componentniveau"),
    "klapsleutel-veer-kapot": ("fiat-500-klapsleutel-bijmaken.jpg", "Fiat 500 met originele en bijgemaakte klapsleutel", "Nieuwe behuizing, eigen chip en zender: Fiat 500"),
    "tweedehands-auto-een-sleutel": ("jaguar-xf-smartkey-bijmaken.jpg", "Twee smartkeys bijgemaakt voor een Jaguar XF", "Tweede sleutel bijgemaakt voor een Jaguar XF"),
    "autosleutel-gestolen": ("jeep-compass-smartkey-bijmaken.jpg", "Sleutelspecialist toont twee nieuwe smartkeys voor een Jeep Compass", "Oude sleutels gewist, twee nieuwe ingeleerd: Jeep Compass"),
    "afstandsbediening-werkt-niet": ("ford-mustang-autosleutel-bijmaken.jpg", "Bijgemaakte autosleutel met afstandsbediening voor een Ford Mustang", "Afstandsbediening opnieuw ingeleerd: Ford Mustang"),
    "zelf-autosleutel-programmeren": ("autosleutel-programmeren-hyundai.jpg", "Twee Hyundai-sleutels worden ingeleerd via de OBD-aansluiting", "Inleren via de diagnoseaansluiting met professionele apparatuur"),
}

# ============================================================
# Veelgestelde vragen homepage (anders dan Almelo)
# ============================================================
FAQ = [
    ("Hoe ver is de werkplaats vanaf Hengelo?",
     f"Ongeveer {REISTIJD} rijden: via de A35 naar Enschede-Zuid, afslag Wesseler-Nering. U parkeert gratis bij het "
     "overdekte winkelcentrum en loopt droog naar de winkel."),
    ("Wat kost de aan-huisservice in Hengelo?",
     f"Vanaf € {AAN_HUIS_VANAF} bovenop de sleutelprijs. Voor de omgeving van Hengelo vragen wij een kleine "
     "kilometervergoeding; die hoort u bij de prijsopgave."),
    ("Hoe weet ik welk sleuteltype ik heb?",
     "Klapt de baard uit: klapsleutel. Startknop in de auto: smartkey. Platte kaart: sleutelkaart. Vaste baard met "
     "kunststof kop: transpondersleutel. Twijfelt u, stuur een foto via WhatsApp."),
    ("Kan ik mijn sleutel dezelfde dag meenemen?",
     "In vrijwel alle gevallen wel: reken op 20 tot 30 minuten. Alleen een enkel zeer recent model moet besteld "
     "worden, en dat zeggen wij vooraf."),
    ("Mijn auto start niet meer en ik kan niet naar Enschede komen. Wat nu?",
     "Dan komen wij naar u toe. Wij leren de nieuwe sleutel ter plekke in via de diagnoseaansluiting van de auto."),
    ("Maakt u ook sleutels voor bestelwagens en motoren?",
     "Bestelwagens ja, van Caddy tot Sprinter. Voor motorsleutels: bel even, dat hangt van het merk af."),
    ("Gebruikt u originele sleutels?",
     "Wij gebruiken originele sleutels of gelijkwaardige sleutels uit voorraad, afhankelijk van merk en prijs. U "
     "hoort vooraf wat u krijgt. Op de chip geven wij levenslange garantie."),
    ("Wat moet ik meenemen?",
     "Kentekenbewijs en een geldig identiteitsbewijs, en als u die heeft uw werkende sleutel. Wij kijken alleen naar "
     "uw documenten; wij maken er geen kopie van."),
]

# ============================================================
# Hieronder hoef je normaal niets te wijzigen
# ============================================================
OUT = pathlib.Path(__file__).parent
IMG = OUT / "img"

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
}
def icoon(naam, klas="ic"):
    return (f'<svg class="{klas}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{_ICONEN[naam]}</svg>')

def foto(bestand, alt, klas="", breed=1200, hoog=900, lazy=True):
    """Toont de foto als hij in img/ staat; anders een nette plekhouder, zodat de build nooit breekt."""
    if (IMG / bestand).exists():
        lz = ' loading="lazy"' if lazy else ' fetchpriority="high"'
        # Staande foto's (sleutel onderin, auto erboven) krijgen een klasse zodat de uitsnede iets lager ligt.
        try:
            from PIL import Image
            with Image.open(IMG / bestand) as im:
                if im.height > im.width:
                    klas = (klas + " is-staand").strip()
        except Exception:
            pass
        return f'<img class="{klas}" src="/img/{bestand}" alt="{html.escape(alt)}" width="{breed}" height="{hoog}"{lz}>'
    return f'<div class="foto-plek {klas}" role="img" aria-label="{html.escape(alt)}"><span>foto volgt</span></div>'

def bedrijf_jsonld():
    d = {
        "@context": "https://schema.org", "@type": "AutomotiveBusiness", "@id": SITE + "/#bedrijf",
        "name": HANDELSNAAM, "url": SITE, "telephone": TEL_LINK, "email": MAIL, "priceRange": "€€",
        "logo": SITE + "/img/logo-autosleutel-hengelo.png", "image": SITE + "/img/og-autosleutel-hengelo.jpg",
        "foundingDate": str(SINDS),
        "parentOrganization": {"@type": "Organization", "name": RECHTSPERSOON},
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
                        "description": f"Autosleutel bijmaken op locatie, vanaf € {AAN_HUIS_VANAF} extra."}],
    }
    if GBP_SCORE and GBP_AANTAL:
        d["aggregateRating"] = {"@type": "AggregateRating", "ratingValue": GBP_SCORE.replace(",", "."),
                                "reviewCount": GBP_AANTAL}
    return d

def faq_jsonld(items):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": v, "acceptedAnswer": {"@type": "Answer", "text": a}} for v, a in items]}

def kruimels_jsonld(paden):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p}
                                for i, (n, p) in enumerate(paden)]}

def artikel_jsonld(titel, pad, omschr):
    return {"@context": "https://schema.org", "@type": "Article", "headline": titel, "description": omschr,
            "url": SITE + pad, "datePublished": "2026-09-13", "inLanguage": "nl-NL",
            "author": {"@type": "Organization", "name": HANDELSNAAM},
            "publisher": {"@type": "Organization", "name": RECHTSPERSOON}}

def kruimels(items):
    delen = [f'<a href="{p}">{n}</a>' if p else n for n, p in items]
    return '<nav class="kruimels wrap" aria-label="Kruimelpad">' + ' <span>›</span> '.join(delen) + '</nav>'

def kop_html(titel, omschrijving, pad, jsonld, beeld=None, noindex=False):
    canon = SITE + pad
    robots = "noindex,nofollow" if noindex else "index,follow,max-image-preview:large"
    blokken = [bedrijf_jsonld()] + list(jsonld)
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(b, ensure_ascii=False, separators=(",", ":"))}</script>' for b in blokken)
    og = f"{SITE}/img/{beeld}" if beeld and (IMG / beeld).exists() else f"{SITE}/img/og-autosleutel-hengelo.jpg"
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
</head>
<body>
<header class="top">
  <div class="wrap top__in">
    <a class="top__merk" href="/" aria-label="Autosleutel Hengelo – naar de homepage"><img src="/img/logo-autosleutel-hengelo.png" alt="Autosleutel Hengelo" width="720" height="184" decoding="async"></a>
    <nav class="top__nav" aria-label="Hoofdmenu">
      <a href="/autosleutel-bijmaken">Sleutel bijmaken</a>
      <a href="/autosleutel-kwijt">Sleutel kwijt</a>
      <a href="/prijzen">Prijzen</a>
      <a href="/aan-huis">Aan huis</a>
      <a href="/kennis">Kennis</a>
      <a href="/merken">Merken</a>
      <a href="/contact">Contact</a>
    </nav>
    <div class="top__acties">
      <a class="top__wa" href="{WA_LINK}" rel="noopener" data-conv="whatsapp" aria-label="WhatsApp">{icoon("wa")}</a>
      <a class="top__tel" href="tel:{TEL_LINK}" data-conv="bellen">{icoon("tel")}<span>{TEL_HTML}</span></a>
    </div>
  </div>
</header>
"""

VOET = f"""
<footer class="voet">
  <div class="wrap voet__grid">
    <div>
      <div class="voet__kop">{HANDELSNAAM}</div>
      <p>Autosleutels bijmaken, programmeren en repareren voor Hengelo en omgeving. Onderdeel van {MOEDER} ({RECHTSPERSOON}).</p>
      <p>KvK {KVK} · btw {BTW}</p>
    </div>
    <div>
      <div class="voet__kop">Werkplaats</div>
      <p>{STRAAT}<br>{POSTCODE} {PLAATS}<br>Overdekt winkelcentrum, gratis parkeren</p>
      <p><a href="{ROUTE_LINK}" rel="noopener" data-conv="route">{icoon("route")}Routebeschrijving</a></p>
      <p><a href="{REVIEW_LINK}" rel="noopener" data-conv="review">{icoon("ster")}Geef ons een Google-review</a></p>
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
      </ul>
      <ul class="voet__lijst voet__lijst--klein">
        <li><a href="/prijzen">Prijzen</a></li><li><a href="/aan-huis">Aan huis</a></li>
        <li><a href="/kennis">Kennis</a></li><li><a href="/merken">Merken</a></li>
        <li><a href="/contact">Contact</a></li><li><a href="/privacy">Privacy</a></li>
      </ul>
    </div>
  </div>
  <p class="wrap voet__onder">© 2026 {RECHTSPERSOON}. Merknamen zijn eigendom van de fabrikanten en worden alleen gebruikt om aan te geven voor welke auto's wij sleutels maken.
  {HANDELSNAAM} is onderdeel van <a href="{MOEDER_URL}" rel="noopener">{MOEDER}</a> in Enschede.</p>
</footer>
<div class="belbalk is-verborgen">
  <a class="belbalk__bel" href="tel:{TEL_LINK}" data-conv="bellen">{icoon("tel")}Bel {TEL_HTML}</a>
  <a class="belbalk__wa" href="{WA_LINK}" rel="noopener" data-conv="whatsapp">{icoon("wa")}WhatsApp</a>
</div>
<script src="/site.js?v={JS_V}" defer></script>
</body>
</html>
"""

def pagina(bestand, titel, omschrijving, pad, body, jsonld=(), beeld=None, noindex=False):
    (OUT / bestand).write_text(kop_html(titel, omschrijving, pad, jsonld, beeld, noindex) + body + VOET, encoding="utf-8")

# ---------- herbruikbare blokken ----------
def knoppen(primair="Bel " + TEL_HTML):
    return (f'<div class="knoppen"><a class="knop knop--vol" href="tel:{TEL_LINK}" data-conv="bellen">{icoon("tel")}{primair}</a>'
            f'<a class="knop knop--rand" href="/contact#kenteken">{icoon("kenteken")}Prijs via kenteken</a></div>')

def kiezer(titel="Welke sleutel heeft u?", intro='Kies uw sleuteltype. U ziet meteen de richtprijs en leest wat wij ermee kunnen. Alles over <a href="/autosleutel-bijmaken">autosleutel bijmaken</a> op één pagina, of lees wat u doet als u <a href="/autosleutel-kwijt">alle sleutels kwijt</a> bent.'):
    kaarten = "".join(
        f'<a class="kies" href="/{t["slug"]}">{icoon(t["icoon"], "ic ic--groot")}<h3>{t["naam"]}</h3>'
        f'<p>{t["kort"]}</p><span class="kies__prijs">{t["prijs_kopie"]}<small>schatting</small></span></a>'
        for t in SLEUTELTYPEN)
    return f"""
<section class="sectie" id="sleuteltypen">
  <div class="wrap">
    <div class="sectie__kop"><h2>{titel}</h2><p>{intro}</p></div>
    <div class="kiezer">{kaarten}</div>
  </div>
</section>"""

def vertrouwen():
    return f"""
<div class="wrap vertrouwen">
  <div>{icoon("kenteken")}<b>Tot 50%</b><span>goedkoper dan de dealer</span></div>
  <div>{icoon("klok")}<b>20–30 min</b><span>klaar terwijl u wacht</span></div>
  <div>{icoon("kalender")}<b>Sinds 1995</b><span>autosleutels bij Westendorp, bedrijf sinds {SINDS}</span></div>
  <div>{icoon("sleutels")}<b>{PER_JAAR}+</b><span>autosleutels per jaar</span></div>
</div>"""

def contactblok():
    """Wit blok met contactgegevens, werkplaats en het Westendorp-logo (zelfde opzet als autosleutel-almelo)."""
    return f"""
    <div class="blok blok--contact">
      <div class="blok__kop">
        <h2>Werkplaats en winkel</h2>
        <p class="moeder"><a href="{MOEDER_URL}" rel="noopener"><img src="/img/logo-westendorp.png" alt="{MOEDER}" width="360" height="108" loading="lazy"></a>
          <span>{HANDELSNAAM} is onderdeel van {MOEDER} in Enschede; daar staat onze werkplaats. Ook voor huis- en fietssleutels, sloten en inbraakbeveiliging.</span></p>
      </div>
      <ul class="contactlijst contactlijst--rij">
        <li><a href="tel:{TEL_LINK}" data-conv="bellen">{icoon("tel")}<span><b>Bellen</b>{TEL_HTML}</span></a></li>
        <li><a href="{WA_LINK}" rel="noopener" data-conv="whatsapp">{icoon("wa")}<span><b>WhatsApp</b>Stuur een foto van uw sleutel</span></a></li>
        <li><a href="mailto:{MAIL}">{icoon("mail")}<span><b>E-mail</b>{MAIL.replace("@", "@<wbr>")}</span></a></li>
      </ul>
      <ul class="feiten">
        <li>{icoon("pin")}<span><b>Adres</b>{STRAAT}<br>{POSTCODE} {PLAATS}<br><a href="{ROUTE_LINK}" rel="noopener" data-conv="route">Routebeschrijving in Google Maps</a></span></li>
        <li>{icoon("klok")}<span><b>Openingstijden</b>{"<br>".join(f"{d}: {t}" for d, t in OPENING)}</span></li>
        <li>{icoon("parkeren")}<span><b>Parkeren</b>Gratis, overdekt winkelcentrum Enschede-Zuid</span></li>
      </ul>
    </div>"""

def formulier(bron, met_contact=True):
    # Zelfde velden en volgorde als het formulier van autosleutel-almelo (wens eigenaar 13-9-2026).
    return f"""
<section class="sectie sectie--zand" id="kenteken">
  <div class="wrap">
    <div class="blok blok--form">
    <div class="sectie__kop">
      <h2>Vraag uw prijs aan</h2>
      <p>Vul uw kenteken in en u hoort dezelfde werkdag wat uw sleutel kost en wanneer u terecht kunt, of wanneer wij bij u kunnen zijn. Liever direct antwoord? <a href="tel:{TEL_LINK}" data-conv="bellen">Bel {TEL_HTML}</a>.</p>
    </div>
    <form action="https://api.web3forms.com/submit" method="POST" class="form" data-key="{WEB3FORMS_KEY}">
      <input type="hidden" name="access_key" value="{WEB3FORMS_KEY}">
      <input type="hidden" name="subject" value="Prijsaanvraag via autosleutel-hengelo.nl">
      <input type="hidden" name="from_name" value="{HANDELSNAAM}">
      <input type="hidden" name="redirect" value="{SITE}/bedankt">
      <input type="hidden" name="bron" value="{bron}">
      <input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off">
      <div class="veld"><label for="naam">Naam</label><input id="naam" name="naam" required autocomplete="name"></div>
      <div class="veld"><label for="tel">Telefoon</label><input id="tel" name="telefoon" type="tel" required autocomplete="tel"></div>
      <div class="veld"><label for="mail">E-mail</label><input id="mail" name="email" type="email" required autocomplete="email"></div>
      <div class="veld veld--kenteken"><label for="kenteken-veld">Kenteken</label>
        <input id="kenteken-veld" name="kenteken" required placeholder="XX-123-X" autocomplete="off">
        <small>Hiermee zien wij direct welke sleutel u nodig heeft.</small></div>
      <div class="veld"><label for="type">Met of zonder afstandsbediening</label>
        <select id="type" name="sleuteltype" required><option value="">Maak een keuze</option>
          <option>Met afstandsbediening</option><option>Zonder afstandsbediening</option><option>Weet ik niet</option></select></div>
      <div class="veld"><label for="start">Hoe start uw auto</label>
        <select id="start" name="starten" required><option value="">Maak een keuze</option>
          <option>Sleutel in contact / dashboard</option><option>Keyless — startknop</option><option>Weet ik niet</option></select></div>
      <div class="veld veld--vol"><label for="opm">Opmerkingen</label>
        <textarea id="opm" name="opmerkingen" placeholder="Bijvoorbeeld: ik ben alle sleutels kwijt, de knopjes werken niet meer, of ik wil graag aan huis geholpen worden."></textarea></div>
      <div class="veld veld--vol">
        <p class="form-uit" hidden>Het aanvraagformulier is nog niet actief. Bel <a href="tel:{TEL_LINK}" data-conv="bellen">{TEL_HTML}</a> of stuur een <a href="{WA_LINK}" rel="noopener" data-conv="whatsapp">WhatsApp-bericht</a> — dan heeft u meteen antwoord.</p>
        <button class="knop knop--geel" type="submit" data-conv="formulier">Vraag mijn prijs aan</button>
        <small>Wij gebruiken uw gegevens alleen om uw aanvraag te beantwoorden. <a href="/privacy">Privacyverklaring</a>.</small>
      </div>
    </form>
    </div>
    {contactblok() if met_contact else ""}
  </div>
</section>"""

def faqblok(items, kop="Veelgestelde vragen"):
    d = "".join(f"<details><summary>{v}</summary><p>{a}</p></details>" for v, a in items)
    return f'<section class="sectie"><div class="wrap wrap--tekst"><div class="sectie__kop"><h2>{kop}</h2></div><div class="faq">{d}</div></div></section>'

def antwoord(tekst):
    return f'<div class="antwoord"><p>{tekst}</p></div>'

def merkenstrip():
    links = "".join(f'<a href="/{s}">{n}</a>' for n, s, *_ in MERKEN)
    return f"""
<section class="sectie sectie--zand">
  <div class="wrap">
    <div class="sectie__kop"><h2>Voor welk merk?</h2><p>Per merk leest u welke sleuteltypen er zijn, wat wij kunnen en wat het kost.</p></div>
    <div class="merken">{links}</div>
    <p class="noot">Staat uw merk er niet bij? De kans is groot dat het toch kan. <a href="tel:{TEL_LINK}" data-conv="bellen">Bel even</a>.</p>
  </div>
</section>"""

# ============================================================
# HOMEPAGE
# ============================================================
galerij = "".join(
    f'<figure>{foto(f, a)}<figcaption>{c}</figcaption></figure>' for f, a, c in [
        ("mini-clubman-smartkey-bijmaken.jpg", "Twee Mini-smartkeys bijgemaakt voor een Mini Clubman", "Mini Clubman · smartkey"),
        ("citroen-c4-picasso-smartkey-bijmaken.jpg", "Twee smartkeys bijgemaakt voor een Citroën C4 Picasso", "Citroën C4 Picasso · smartkey"),
        ("fiat-500-klapsleutel-bijmaken.jpg", "Fiat 500 met originele en bijgemaakte klapsleutel", "Fiat 500 · klapsleutel"),
        ("jeep-compass-smartkey-bijmaken.jpg", "Twee smartkeys bijgemaakt voor een Jeep Compass", "Jeep Compass · smartkey"),
        ("jaguar-xf-smartkey-bijmaken.jpg", "Twee smartkeys bijgemaakt voor een Jaguar XF", "Jaguar XF · smartkey"),
        ("ford-mustang-autosleutel-bijmaken.jpg", "Bijgemaakte autosleutel voor een Ford Mustang", "Ford Mustang · smartkey"),
        ("renault-kadjar-sleutelkaart-bijmaken.jpg", "Twee Renault-sleutelkaarten bijgemaakt voor een Renault Kadjar", "Renault Kadjar · sleutelkaart"),
        ("opel-astra-klapsleutel-bijmaken.jpg", "Twee bijgemaakte Opel-klapsleutels voor een Opel Astra", "Opel Astra · klapsleutel"),
    ])
pagina("index.html",
       f"Autosleutel bijmaken Hengelo | vanmiddag klaar, vanaf € 60",
       f"Autosleutel kwijt, kapot of een reservesleutel nodig in Hengelo? Klapsleutel, smartkey of sleutelkaart voor vrijwel elk merk. "
       f"Vaste prijs via uw kenteken, {REISTIJD} vanaf Hengelo, of aan huis vanaf € {AAN_HUIS_VANAF}. Bel {TEL_TONEN}.",
       "/", jsonld=[faq_jsonld(FAQ)], beeld="bmw-x1-smartkey-bijmaken.jpg",
       body=f"""
<section class="hero">
  <div class="wrap hero__grid">
    <div>
      <span class="label">{icoon("pin")}Werkplaats in Enschede · {REISTIJD} vanaf Hengelo</span>
      <h1>Autosleutel bijmaken in Hengelo, <em>vanmiddag klaar.</em></h1>
      <p class="hero__lead">Reservesleutel laten maken, autosleutel kwijt of sleutel kapot? Klapsleutel, smartkey, sleutelkaart of transpondersleutel: wij maken, programmeren en repareren autosleutels voor vrijwel elk merk. Tot 50% goedkoper dan de dealer, prijs vooraf op basis van uw kenteken, meestal klaar terwijl u wacht.</p>
      {knoppen()}
      <p class="hero__noot">Liever niet rijden? <strong>Aan huis in Hengelo vanaf € {AAN_HUIS_VANAF}.</strong></p>
    </div>
    <figure class="hero__foto">{foto("bmw-x1-smartkey-bijmaken-hero.jpg", "Twee BMW-smartkeys bijgemaakt voor een BMW X1", lazy=False)}
      <figcaption>BMW X1, twee smartkeys, klaar in één bezoek</figcaption></figure>
  </div>
  {vertrouwen()}
</section>
{kiezer()}
<section class="sectie sectie--zand">
  <div class="wrap">
    <div class="sectie__kop"><h2>Zo gaat het, in drie stappen</h2></div>
    <ol class="stappen">
      <li>{icoon("kenteken")}<h3>Kenteken sturen</h3><p>Via het formulier, WhatsApp of telefoon. Uit het kenteken zien wij precies welke sleutel uw auto heeft.</p></li>
      <li>{icoon("vink")}<h3>Vaste prijs, dezelfde werkdag</h3><p>Inclusief of het terwijl u wacht kan, of een sleutel besteld moet worden, en wat aan huis kost.</p></li>
      <li>{icoon("winkel")}<h3>Werkplaats of aan huis</h3><p>U komt op afspraak naar Enschede ({REISTIJD}), of wij komen naar u toe in Hengelo.</p></li>
    </ol>
    <div class="knoppen knoppen--midden">{knoppen()[len('<div class="knoppen">'):]}
  </div>
</section>
<section class="sectie">
  <div class="wrap media">
    <div>
      <h2>Waarom mensen uit Hengelo naar onze werkplaats rijden</h2>
      <p>Geen busje met een universeel apparaatje: een vaste werkplaats met voorraad behuizingen, chips en afstandsbedieningen voor vrijwel elk merk, sleutelmachines om op code te frezen en apparatuur om op componentniveau te solderen. Daardoor kunnen wij meer, sneller en goedkoper dan onderweg.</p>
      <ul class="vinkjes">
        <li>{icoon("vink")}Meestal klaar terwijl u wacht, in 20 tot 30 minuten</li>
        <li>{icoon("vink")}Repareren waar anderen vervangen: {P_REP} in plaats van een nieuwe sleutel</li>
        <li>{icoon("vink")}Levenslange garantie op de chip, twee jaar op een nieuwe afstandsbediening</li>
        <li>{icoon("vink")}Gratis en overdekt parkeren bij de winkel</li>
      </ul>
      <p><a class="knop knop--rand" href="/contact">{icoon("route")}Route vanuit Hengelo</a></p>
    </div>
    <div class="media__fotos">
      <figure>{foto("werkplaats-voorraad-autosleutel-behuizingen.jpg", "Voorraadkasten met autosleutelbehuizingen en chips in de werkplaats", breed=900, hoog=1200)}<figcaption>De voorraad: behuizingen en chips per merk</figcaption></figure>
      <figure>{foto("werkplaats-autosleutel-reparatie-werkbank.jpg", "Sleutelspecialist repareert een autosleutel aan de werkbank in de werkplaats in Enschede", breed=900, hoog=1200)}<figcaption>Reparatie op componentniveau</figcaption></figure>
    </div>
  </div>
</section>
<section class="sectie sectie--groen-licht">
  <div class="wrap media media--omgekeerd">
    <div>
      <span class="label">{icoon("huis")}Aan-huisservice</span>
      <h2>Auto start niet? Wij komen naar Hengelo.</h2>
      <p>Alle sleutels kwijt, of de auto is niet te verplaatsen? Dan komen wij naar u toe en leren wij de nieuwe sleutel ter plekke in via de diagnoseaansluiting. In Hengelo vanaf € {AAN_HUIS_VANAF} bovenop de sleutelprijs; voor de omgeving hoort u de prijs vooraf.</p>
      <p><a class="knop knop--vol" href="/aan-huis">{icoon("pijl")}Zo werkt aan huis</a></p>
    </div>
    <figure class="media__foto">{foto("autosleutel-programmeren-hyundai.jpg", "Twee Hyundai-sleutels worden ingeleerd via de OBD-aansluiting")}<figcaption>Inleren via de OBD-aansluiting, ook bij u voor de deur</figcaption></figure>
  </div>
</section>
<section class="sectie">
  <div class="wrap">
    <div class="sectie__kop"><h2>Onlangs gemaakt</h2><p>Een greep uit de sleutels die wij de afgelopen tijd maakten of repareerden.</p></div>
    <div class="galerij">{galerij}</div>
  </div>
</section>
{merkenstrip()}
{faqblok(FAQ)}
{formulier("home")}
""")

# ============================================================
# PRIJZEN
# ============================================================
rijen = "".join(
    f'<tr><td><a href="/{t["slug"]}">{t["naam"]}</a><br><small>{t["kort"]}</small></td><td>{t["prijs_kopie"]}</td><td class="dealer">{DEALER.get(t["slug"], "")}</td><td>{t["prijs_nieuw"]}</td></tr>'
    for t in SLEUTELTYPEN[:-1])
pagina("prijzen.html", f"Prijzen autosleutel bijmaken Hengelo | {HANDELSNAAM}",
       f"Wat kost een autosleutel bijmaken in Hengelo? Richtprijzen per sleuteltype: transpondersleutel {P_KOPIE}, klapsleutel {P_KLAP}, "
       f"sleutelkaart {P_KAART}, smartkey {P_SMART}, reparatie {P_REP}. Aan huis vanaf € {AAN_HUIS_VANAF}.",
       "/prijzen", jsonld=[kruimels_jsonld([("Home", "/"), ("Prijzen", "/prijzen")])],
       body=f"""
{kruimels([("Home", "/"), ("Prijzen", "")])}
<section class="sectie sectie--kort">
  <div class="wrap wrap--tekst">
    <h1>Wat kost een autosleutel bijmaken?</h1>
    {antwoord(f"Een gewone transpondersleutel kopiëren kost {P_KOPIE}, een klapsleutel {P_KLAP}, een sleutelkaart {P_KAART} en een smartkey {P_SMART}. "
              f"Een reparatie kost {P_REP}. Alles inclusief programmeren en btw. Bent u alle sleutels kwijt, dan verschilt de prijs "
              f"sterk per merk en bouwjaar; die krijgt u vooraf op basis van uw kenteken. "
              f"Aan huis in Hengelo betaalt u vanaf € {AAN_HUIS_VANAF} extra.")}
    <p>De prijs hangt niet af van hoe duur uw auto was, maar van het sleuteltype en van de vraag of u nog een werkende sleutel heeft. Uw kenteken maakt er één prijs vooraf van.</p>
    <table class="prijstabel">
      <caption><b>Schatting</b>, geen offerte: de bedragen zijn wat het bij ons en bij de dealer meestal kost. Uw werkelijke prijs hangt af van merk, model en bouwjaar en krijgt u vooraf op uw kenteken.</caption>
      <thead><tr><th>Sleuteltype</th><th>Bij ons (schatting)<br><small>kopie, u heeft nog een werkende sleutel</small></th><th>Bij de dealer (schatting)</th><th>Alle sleutels kwijt</th></tr></thead>
      <tbody>{rijen}
      <tr><td><a href="/autosleutel-reparatie">Reparatie</a><br><small>behuizing, knopjes, veer, chip terugsolderen</small></td><td>{P_REP}</td><td class="dealer">{DEALER["autosleutel-reparatie"]}</td><td>—</td></tr>
      <tr><td><a href="/aan-huis">Aan huis in Hengelo</a><br><small>bovenop de sleutelprijs</small></td><td colspan="3">vanaf € {AAN_HUIS_VANAF}</td></tr>
      </tbody>
    </table>
    <h2>Waarom de dealer duurder is</h2>
    <p>Een dealer bestelt de sleutel bij de fabriek, wacht twee tot zes weken en rekent daar werkplaatstarief overheen. Wij hebben de sleutel op voorraad of halen hem uit onze eigen leveranciersketen, en programmeren zelf. Daardoor betaalt u doorgaans de helft tot een derde, en heeft u de sleutel dezelfde dag.</p>
    <h2>Wat er wél extra kan kosten</h2>
    <ul>
      <li><strong>Pincode bij oudere Peugeot of Citroën</strong> (tot ongeveer 2005): € 35 als u de code niet meer heeft.</li>
      <li><strong>Bestelling via de dealer</strong> bij een enkel zeer recent model: dat hoort u vooraf, nooit achteraf.</li>
      <li><strong>Aan huis buiten Hengelo</strong>: een kilometervergoeding, in de prijsopgave inbegrepen.</li>
    </ul>
    {knoppen()}
  </div>
</section>
{kiezer("Zoek uw sleuteltype", "Per type leest u wat het precies kost en wat wij ermee kunnen.")}
{formulier("prijzen")}
""")

# ============================================================
# SLEUTELTYPE-PAGINA'S
# ============================================================
for t in SLEUTELTYPEN:
    secties = "".join(f"<h2>{k}</h2><p>{p}</p>" for k, p in t["tekst"])
    anderen = "".join(f'<a class="kies kies--klein" href="/{o["slug"]}">{icoon(o["icoon"])}<span>{o["naam"]}</span></a>'
                      for o in SLEUTELTYPEN if o is not t)
    pagina(t["slug"] + ".html", f"{t['kop']} Hengelo | {t['prijs_kopie'].split(' – ')[0].replace('€ ', 'vanaf € ')}",
           f"{t['kort']} {t['kop']} in Hengelo: richtprijs {t['prijs_kopie']}, meestal klaar terwijl u wacht. Ook aan huis.",
           "/" + t["slug"],
           jsonld=[faq_jsonld(t["faq"]), kruimels_jsonld([("Home", "/"), ("Sleuteltypen", "/prijzen"), (t["naam"], "/" + t["slug"])])],
           beeld=t["foto"],
           body=f"""
{kruimels([("Home", "/"), ("Prijzen", "/prijzen"), (t["naam"], "")])}
<section class="sectie sectie--kort">
  <div class="wrap media">
    <div>
      <span class="label">{icoon(t["icoon"])}{t["naam"]}</span>
      <h1>{t["kop"]} in Hengelo</h1>
      {antwoord(t["antwoord"])}
      <p><strong>Zo herkent u 'm:</strong> {t["herken"]}</p>
      <p><strong>Vaak bij:</strong> {t["merken"]}.</p>
      {knoppen()}
    </div>
    <figure class="media__foto">{foto(t["foto"], t["alt"], lazy=False)}<figcaption>{t["alt"]}</figcaption></figure>
  </div>
</section>
<section class="sectie sectie--zand"><div class="wrap wrap--tekst">
  <div class="prijs-kaart"><div><small>Kopie, u heeft nog een sleutel</small><b>{t["prijs_kopie"]}</b></div>
  <div><small>Alle sleutels kwijt</small><b>{t["prijs_nieuw"]}</b></div>
  <div><small>Aan huis in Hengelo</small><b>+ vanaf € {AAN_HUIS_VANAF}</b></div></div>
  {secties}
</div></section>
{faqblok(t["faq"], f"Vragen over {t['naam'].lower()}s")}
<section class="sectie sectie--kort"><div class="wrap"><div class="sectie__kop"><h2>Ander sleuteltype?</h2><p>Of lees alles over <a href="/autosleutel-bijmaken">autosleutel bijmaken in Hengelo</a>: werkwijze, prijzen en wat u meeneemt.</p></div><div class="kiezer kiezer--klein">{anderen}</div></div></section>
{formulier(t["slug"])}
""")

# ============================================================
# AUTOSLEUTEL BIJMAKEN (hoofdpagina voor de belangrijkste zoekterm)
# ============================================================
BIJMAKEN_FAQ = [
    ("Wat kost een autosleutel bijmaken in Hengelo?",
     f"Een kopie van een sleutel die u nog heeft: transpondersleutel {P_KOPIE}, klapsleutel {P_KLAP}, sleutelkaart {P_KAART}, "
     f"smartkey {P_SMART}, inclusief programmeren en btw. Bent u alle sleutels kwijt, dan verschilt de prijs sterk per merk en "
     "bouwjaar; u krijgt vooraf een vaste prijs op basis van uw kenteken."),
    ("Hoe lang duurt een autosleutel bijmaken?",
     "Meestal 20 tot 30 minuten, klaar terwijl u wacht. Alleen bij een enkel zeer recent model moet een sleutel besteld worden; dat hoort u vooraf."),
    ("Kan ik een autosleutel laten bijmaken zonder originele sleutel?",
     "Ja, bij de meeste merken en bouwjaren. Wij maken dan een nieuwe sleutel en leren die in op de auto. Neem kentekenbewijs en identiteitsbewijs mee."),
    ("Moet ik naar de dealer voor een nieuwe autosleutel?",
     "Nee. Wij maken en programmeren autosleutels voor vrijwel elk merk in onze eigen werkplaats, tot 50% goedkoper dan de dealer en zonder wachttijd van weken."),
    ("Kan een autosleutel ook aan huis bijgemaakt worden?",
     f"Ja. In Hengelo komen wij aan huis vanaf € {AAN_HUIS_VANAF} bovenop de sleutelprijs; voor de omgeving hoort u de prijs vooraf."),
    ("Wat moet ik meenemen?",
     "Uw kenteken volstaat voor de prijs. Bij het maken: kentekenbewijs, een geldig identiteitsbewijs en, als u die nog heeft, een werkende sleutel."),
]
pagina("autosleutel-bijmaken.html",
       f"Autosleutel bijmaken Hengelo | vanaf € 60, klaar terwijl u wacht",
       f"Autosleutel bijmaken in Hengelo: reservesleutel, nieuwe sleutel of kopie voor vrijwel elk merk, inclusief programmeren. "
       f"Vaste prijs via uw kenteken, meestal klaar in 20–30 minuten, {REISTIJD} vanaf Hengelo of aan huis vanaf € {AAN_HUIS_VANAF}.",
       "/autosleutel-bijmaken",
       jsonld=[faq_jsonld(BIJMAKEN_FAQ), kruimels_jsonld([("Home", "/"), ("Autosleutel bijmaken", "/autosleutel-bijmaken")])],
       beeld="opel-astra-klapsleutel-bijmaken.jpg",
       body=f"""
{kruimels([("Home", "/"), ("Autosleutel bijmaken", "")])}
<section class="sectie sectie--kort">
  <div class="wrap media">
    <div>
      <span class="label">{icoon("sleutels")}Reservesleutel · nieuwe sleutel · kopie</span>
      <h1>Autosleutel bijmaken in Hengelo</h1>
      {antwoord(f"Wij maken, programmeren en repareren autosleutels voor vrijwel elk merk en bouwjaar: als reservesleutel, als kopie van "
                f"uw huidige sleutel of als volledig nieuwe sleutel wanneer u alles kwijt bent. Vanaf {P_KOPIE.split(' – ')[0]}, inclusief "
                f"programmeren en btw, meestal klaar terwijl u wacht. De werkplaats staat op {REISTIJD} van Hengelo; aan huis kan ook.")}
      <p>Een autosleutel bijmaken is bij moderne auto's programmeerwerk: de transponderchip en de afstandsbediening moeten op uw auto worden ingeleerd, anders start hij niet. Dat doen wij in eigen huis met apparatuur per merk, zonder dealer en zonder wachttijd van weken.</p>
      {knoppen()}
    </div>
    <figure class="media__foto">{foto("opel-astra-klapsleutel-bijmaken.jpg", "Twee bijgemaakte Opel-klapsleutels voor een Opel Astra", lazy=False)}<figcaption>Opel Astra: klapsleutel bijgemaakt en geprogrammeerd, klaar in één bezoek</figcaption></figure>
  </div>
</section>
<section class="sectie sectie--zand"><div class="wrap wrap--tekst">
  <h2>Welke autosleutel wilt u laten bijmaken?</h2>
  <p>De prijs en de werkwijze hangen af van het sleuteltype, niet van het merk of hoe duur uw auto was. Kies het type dat op uw sleutel lijkt:</p>
  <div class="kiezer kiezer--klein">{"".join(f'<a class="kies kies--klein" href="/{t["slug"]}">{icoon(t["icoon"])}<span>{t["naam"]}</span></a>' for t in SLEUTELTYPEN)}</div>
  <h2>Reservesleutel laten maken: goedkoper nu dan later</h2>
  <p>Heeft u nog een werkende sleutel? Dan kopiëren wij de chip en de afstandsbediening naar een nieuwe sleutel: dat is de goedkoopste en snelste route. Raakt u die ene sleutel later kwijt, dan moet er een nieuwe sleutel zonder werkend exemplaar komen. Dat kan bij de meeste auto's, maar het kost meer en de auto staat stil tot het geregeld is. Een tweede sleutel is daarom een kleine investering die veel gedoe voorkomt.</p>
  <h2>Autosleutel kwijt of kapot?</h2>
  <p>Bent u <a href="/autosleutel-kwijt">alle sleutels kwijt</a>, dan maken wij een nieuwe sleutel en wissen wij de oude uit de auto, zodat een gevonden of gestolen sleutel niet meer werkt. Is de sleutel kapot (gebroken behuizing, knopjes doen niets, klapt niet meer uit), dan is <a href="/autosleutel-reparatie">repareren</a> meestal genoeg: uw eigen chip en zender gaan over in een nieuwe behuizing, zonder programmeren.</p>
  <h2>Zo werkt autosleutel bijmaken bij ons</h2>
  <ol class="stappen stappen--lijst">
    <li>{icoon("kenteken")}<h3>Kenteken doorgeven</h3><p>Via het formulier, WhatsApp of telefoon. Uit het kenteken zien wij welk sleuteltype, welke chip en welke procedure uw auto heeft.</p></li>
    <li>{icoon("vink")}<h3>Vaste prijs vooraf</h3><p>U hoort dezelfde werkdag wat het kost, of het terwijl u wacht kan en of wij bij u langs kunnen komen.</p></li>
    <li>{icoon("winkel")}<h3>Maken en programmeren</h3><p>In de werkplaats in Enschede ({REISTIJD} vanaf Hengelo) of <a href="/aan-huis">aan huis in Hengelo</a>. De baard wordt gefreesd, de chip en afstandsbediening ingeleerd, en u test de sleutel voordat u betaalt.</p></li>
  </ol>
  <h2>Wat u meeneemt</h2>
  <ul class="vinkjes">
    <li>{icoon("vink")}Kentekenbewijs (of het kenteken vooraf via het formulier)</li>
    <li>{icoon("vink")}Geldig identiteitsbewijs, zodat wij weten dat de auto van u is</li>
    <li>{icoon("vink")}Uw huidige sleutel, als u die nog heeft: dan is het goedkoper en sneller</li>
  </ul>
  <h2>Waarom niet naar de dealer?</h2>
  <p>Een dealer bestelt de sleutel bij de fabriek, wacht twee tot zes weken en rekent daar werkplaatstarief overheen. Wij hebben behuizingen, chips en afstandsbedieningen voor vrijwel elk merk op voorraad en programmeren zelf. Daardoor betaalt u doorgaans de helft tot een derde en heeft u de sleutel dezelfde dag. U krijgt levenslange garantie op de chip en twee jaar op een nieuwe afstandsbediening.</p>
  <h2>Voor Hengelo en heel Twente</h2>
  <p>Klanten komen naar onze werkplaats vanuit Hengelo, {", ".join(PLAATSEN[1:-1])} en {PLAATSEN[-1]}. Kunt u niet komen, bijvoorbeeld omdat de auto niet start, dan komen wij naar u toe.</p>
  {knoppen()}
</div></section>
{merkenstrip()}
{faqblok(BIJMAKEN_FAQ, "Vragen over autosleutel bijmaken")}
{formulier("autosleutel-bijmaken")}
""")

# ============================================================
# AUTOSLEUTEL KWIJT (situatiepagina, geen prijs: verschilt te sterk)
# ============================================================
KWIJT_FAQ = [
    ("Ik ben al mijn autosleutels kwijt. Kan er nog een nieuwe gemaakt worden?",
     "Bij de meeste merken en bouwjaren wel. Wij maken een nieuwe sleutel op basis van uw kenteken en leren die in op de auto, ook zonder werkend exemplaar."),
    ("Wat kost een nieuwe autosleutel als ik alles kwijt ben?",
     "Dat verschilt sterk per merk, model en bouwjaar, daarom noemen wij daar geen vast bedrag voor. Geef uw kenteken door en u krijgt vooraf een vaste prijs."),
    ("Kan iemand met mijn verloren sleutel mijn auto stelen?",
     "Zolang de oude sleutel nog geprogrammeerd staat wel. Bij het maken van de nieuwe sleutel wissen wij de verloren sleutel uit de auto, zodat die niet meer start."),
    ("Wat als de auto niet naar Enschede kan?",
     f"Dan komen wij naar u toe: in Hengelo vanaf € {AAN_HUIS_VANAF} bovenop de sleutelprijs. Wij leren de sleutel ter plekke in via de diagnoseaansluiting."),
    ("Wat heb ik nodig?",
     "Kentekenbewijs en een geldig identiteitsbewijs. Zonder die papieren maken wij geen sleutel voor een auto zonder werkend exemplaar."),
]
pagina("autosleutel-kwijt.html",
       f"Autosleutel kwijt in Hengelo? Nieuwe sleutel, ook zonder reserve",
       f"Autosleutel kwijt of gestolen in Hengelo? Wij maken een nieuwe sleutel op basis van uw kenteken en wissen de oude uit de auto. "
       f"Werkplaats op {REISTIJD} van Hengelo, of aan huis vanaf € {AAN_HUIS_VANAF}. Bel {TEL_TONEN}.",
       "/autosleutel-kwijt",
       jsonld=[faq_jsonld(KWIJT_FAQ), kruimels_jsonld([("Home", "/"), ("Autosleutel kwijt", "/autosleutel-kwijt")])],
       beeld="jeep-compass-smartkey-bijmaken.jpg",
       body=f"""
{kruimels([("Home", "/"), ("Autosleutel kwijt", "")])}
<section class="sectie sectie--kort">
  <div class="wrap media">
    <div>
      <span class="label">{icoon("sleutels")}Alle sleutels kwijt of gestolen</span>
      <h1>Autosleutel kwijt in Hengelo</h1>
      {antwoord("Geen enkele werkende sleutel meer? Voor de meeste merken en bouwjaren maken wij een volledig nieuwe autosleutel op basis van uw "
                "kenteken en leren die in op de auto. De verloren sleutel wissen wij, zodat niemand er nog mee kan rijden. De prijs hangt sterk af "
                "van merk en bouwjaar; u krijgt hem vooraf, vast, via uw kenteken.")}
      <p>Heeft u nog wél een reservesleutel? Dan is het eenvoudiger en goedkoper: wij <a href="/autosleutel-bijmaken">kopiëren die sleutel</a> (vanaf {P_KOPIE.split(' – ')[0]}) en u heeft er weer twee.</p>
      {knoppen("Bel direct " + TEL_HTML)}
    </div>
    <figure class="media__foto">{foto("jeep-compass-smartkey-bijmaken.jpg", "Sleutelspecialist met twee nieuwe smartkeys voor een Jeep Compass waarvan alle sleutels kwijt waren", lazy=False)}<figcaption>Jeep Compass: oude sleutels gewist, twee nieuwe ingeleerd</figcaption></figure>
  </div>
</section>
<section class="sectie sectie--zand"><div class="wrap wrap--tekst">
  <h2>Eerst dit, voordat u iets laat maken</h2>
  <ol class="stappen stappen--lijst">
    <li>{icoon("vink")}<h3>Zoek nog één keer goed</h3><p>Jaszakken, de wasmachine, de auto zelf, de vorige parkeerplaats. Duikt de sleutel binnen een dag op, dan bespaart u het hele bedrag.</p></li>
    <li>{icoon("schild")}<h3>Gestolen? Doe aangifte en bel uw verzekeraar</h3><p>Bij diefstal vergoeden veel beperkt-casco- en allriskpolissen de nieuwe sleutel. Bij gewoon verlies meestal niet, maar vragen kost niets.</p></li>
    <li>{icoon("kenteken")}<h3>Geef uw kenteken door</h3><p>U hoort dezelfde werkdag wat een nieuwe sleutel kost, of het bij uw bouwjaar zonder werkende sleutel kan, en of wij naar Hengelo kunnen komen.</p></li>
  </ol>
  <h2>Zo maken wij een sleutel zonder werkend exemplaar</h2>
  <p>Uit het kenteken halen wij het sleutelprofiel en de chipgeneratie van uw auto. De baard wordt op code gefreesd, zodat hij in het slot past. Daarna koppelen wij de nieuwe transponderchip en de afstandsbediening aan de startonderbreker via de diagnoseaansluiting van de auto. Bij dezelfde handeling wissen wij alle sleutels die niet aanwezig zijn: de verloren sleutel start de auto daarna niet meer.</p>
  <p>Bij oudere Peugeot- en Citroën-modellen is soms een pincode nodig; bij een enkel zeer recent model moet een sleutel via de fabriek besteld worden. Dat hoort u vooraf, nooit achteraf.</p>
  <h2>Auto start niet en staat vast?</h2>
  <p>Dan hoeft u niet te slepen. Wij komen naar u toe in Hengelo (vanaf € {AAN_HUIS_VANAF} bovenop de sleutelprijs) of in de omgeving, en leren de sleutel ter plekke in. <a href="/aan-huis">Zo werkt de aan-huisservice</a>.</p>
  {knoppen()}
</div></section>
{faqblok(KWIJT_FAQ, "Vragen over een verloren autosleutel")}
{formulier("autosleutel-kwijt")}
""")

# ============================================================
# AAN HUIS
# ============================================================
AANHUIS_FAQ = [
    ("Wat kost aan huis precies?", f"In Hengelo vanaf € {AAN_HUIS_VANAF} bovenop de sleutelprijs. Buiten Hengelo rekenen wij een kilometervergoeding; het totaalbedrag staat in uw prijsopgave."),
    ("Kunnen jullie alles aan huis?", "Het meeste: programmeren, inleren, een reservesleutel maken. Wat er bij uw auto ter plekke kan, hoort u vooraf. Soms is het slimmer dat wij de sleutel in de werkplaats voorbereiden en bij u alleen nog inleren."),
    ("Hoe snel kunnen jullie komen?", "Meestal dezelfde of de volgende werkdag, op afspraak. Bel voor de snelste optie."),
    ("Moet ik erbij zijn?", "Ja: wij controleren uw kentekenbewijs en identiteitsbewijs voordat wij een sleutel inleren."),
]
pagina("aan-huis.html", f"Autosleutel aan huis Hengelo | vanaf € {AAN_HUIS_VANAF} extra",
       f"Auto start niet of alle sleutels kwijt? Wij komen naar u toe in Hengelo en leren de sleutel ter plekke in. Vanaf € {AAN_HUIS_VANAF} bovenop de sleutelprijs.",
       "/aan-huis", jsonld=[faq_jsonld(AANHUIS_FAQ), kruimels_jsonld([("Home", "/"), ("Aan huis", "/aan-huis")])],
       beeld="autosleutel-programmeren-hyundai.jpg",
       body=f"""
{kruimels([("Home", "/"), ("Aan huis", "")])}
<section class="sectie sectie--kort">
  <div class="wrap media">
    <div>
      <span class="label">{icoon("huis")}Aan-huisservice</span>
      <h1>Autosleutel aan huis in Hengelo</h1>
      {antwoord(f"Kunt u niet naar Enschede komen, dan komen wij naar u. In Hengelo kost dat vanaf € {AAN_HUIS_VANAF} bovenop de sleutelprijs. "
                "Wij nemen de juiste sleutel mee, leren hem ter plekke in via de diagnoseaansluiting van de auto, en u rijdt weer.")}
      {knoppen("Bel voor een afspraak")}
    </div>
    <figure class="media__foto">{foto("autosleutel-programmeren-hyundai.jpg", "Twee Hyundai-sleutels worden ingeleerd via de OBD-aansluiting van de auto", lazy=False)}<figcaption>Inleren via de diagnoseaansluiting, ook bij u voor de deur</figcaption></figure>
  </div>
</section>
<section class="sectie sectie--zand"><div class="wrap wrap--tekst">
  <h2>Wanneer aan huis de beste keuze is</h2>
  <ul class="vinkjes">
    <li>{icoon("vink")}U bent alle sleutels kwijt en de auto staat vast</li>
    <li>{icoon("vink")}De auto start niet meer door een kapotte sleutel</li>
    <li>{icoon("vink")}U heeft geen tijd of vervoer om naar Enschede te komen</li>
    <li>{icoon("vink")}Een bedrijfswagen die niet stil mag staan</li>
  </ul>
  <h2>Zo gaat het</h2>
  <ol class="stappen stappen--lijst">
    <li>{icoon("kenteken")}<h3>Kenteken en adres</h3><p>U stuurt uw kenteken en waar de auto staat. Wij zien welke sleutel het wordt en of het ter plekke kan.</p></li>
    <li>{icoon("vink")}<h3>Eén prijs, inclusief voorrijden</h3><p>U krijgt het totaalbedrag vooraf: sleutel, programmeren en de aan-huisservice.</p></li>
    <li>{icoon("auto")}<h3>Wij komen langs</h3><p>Op afspraak, meestal dezelfde of de volgende werkdag. Wij controleren uw papieren en leren de sleutel in.</p></li>
  </ol>
  <h2>Werkgebied</h2>
  <p>Hengelo en directe omgeving: {", ".join(PLAATSEN[1:])}. Buiten Hengelo rekenen wij een kilometervergoeding, die in de prijsopgave zit.</p>
  <p class="noot">Wilt u liever naar de werkplaats komen? Dat is {REISTIJD} rijden en bespaart u de voorrijkosten. <a href="/contact">Route en openingstijden</a>.</p>
</div></section>
{faqblok(AANHUIS_FAQ, "Vragen over aan huis")}
{formulier("aan-huis")}
""")

# ============================================================
# CONTACT
# ============================================================
pagina("contact.html", f"Contact en route vanuit Hengelo | {HANDELSNAAM}",
       f"Bel {TEL_TONEN}, stuur een WhatsApp of vraag een prijs aan via uw kenteken. Werkplaats: {STRAAT}, {PLAATS}, {REISTIJD} vanaf Hengelo via de A35.",
       "/contact", jsonld=[kruimels_jsonld([("Home", "/"), ("Contact", "/contact")])],
       body=f"""
{kruimels([("Home", "/"), ("Contact", "")])}
<section class="sectie sectie--kort">
  <div class="wrap">
    <div class="wrap--tekst" style="margin:0 0 36px">
      <h1>Contact</h1>
      <p class="intro">Het snelst gaat het per telefoon: dan weet u binnen een paar minuten wat uw sleutel kost en wanneer u terecht kunt. Buiten openingstijden stuurt u een WhatsApp of het formulier hieronder; u hoort dezelfde werkdag van ons.</p>
    </div>
    {contactblok()}
  </div>
</section>
<section class="sectie sectie--kort sectie--groen-licht">
  <div class="wrap media">
    <div>
      <h2>Route vanuit Hengelo</h2>
      <p>Vanuit Hengelo neemt u de A35 richting Enschede en volgt u de borden Enschede-Zuid. De werkplaats zit in het winkelcentrum aan de Wesseler-Nering; u rijdt er in ongeveer {REISTIJD}. Vanuit Borne, Delden en Oldenzaal is het vergelijkbaar. Kom op afspraak, dan ligt de juiste sleutel klaar en bent u meestal binnen een half uur weer buiten.</p>
      <p>Auto die niet start? Dan hoeft u niet te komen: <a href="/aan-huis">wij komen naar Hengelo</a>.</p>
      <p><a class="knop knop--vol" href="{ROUTE_LINK}" rel="noopener" data-conv="route">{icoon("route")}Routebeschrijving</a></p>
    </div>
    <figure class="media__foto">{foto("werkplaats-autosleutel-reparatie-werkbank.jpg", "De werkplaats van Westendorp in Enschede: sleutelspecialist aan de werkbank")}<figcaption>De werkplaats aan de Wesseler-Nering in Enschede</figcaption></figure>
  </div>
</section>
{formulier("contact", met_contact=False)}
""")

# ============================================================
# KENNIS
# ============================================================
kaarten = "".join(f'<a class="kb" href="/{k["slug"]}"><h2>{k["titel"]}</h2><p>{k["omschr"]}</p><span>Lees verder {icoon("pijl")}</span></a>' for k in KENNIS)
pagina("kennis.html", f"Kennis over autosleutels | {HANDELSNAAM}",
       "Praktische uitleg zonder jargon: natte sleutel, kapotte klapsleutel, occasion met één sleutel, gestolen sleutel, afstandsbediening die niet werkt en zelf programmeren.",
       "/kennis", jsonld=[kruimels_jsonld([("Home", "/"), ("Kennis", "/kennis")])],
       body=f"""
{kruimels([("Home", "/"), ("Kennis", "")])}
<section class="sectie sectie--kort"><div class="wrap">
  <h1>Kennis over autosleutels</h1>
  <p class="intro">Wat u zelf kunt doen, wanneer u beter even belt, en wat het kost. Geschreven vanuit de werkplaats, in gewone taal.</p>
  <div class="kb-lijst">{kaarten}</div>
</div></section>
""")
for k in KENNIS:
    secties = "".join(f"<h2>{h}</h2><p>{p}</p>" for h, p in k["body"])
    kf = KENNIS_FOTO.get(k["slug"])
    kfoto = f'<figure class="artikel__foto">{foto(kf[0], kf[1], breed=1200, hoog=800)}<figcaption>{kf[2]}</figcaption></figure>' if kf else ""
    pagina(k["slug"] + ".html", f"{k['titel']} | Kennis {HANDELSNAAM}", k["omschr"], "/" + k["slug"],
           jsonld=[artikel_jsonld(k["titel"], "/" + k["slug"], k["omschr"]), faq_jsonld(k["faq"]),
                   kruimels_jsonld([("Home", "/"), ("Kennis", "/kennis"), (k["titel"], "/" + k["slug"])])],
           beeld=kf[0] if kf else None,
           body=f"""
{kruimels([("Home", "/"), ("Kennis", "/kennis"), (k["titel"], "")])}
<article class="sectie sectie--kort"><div class="wrap wrap--tekst artikel">
  <h1>{k["titel"]}</h1>
  {antwoord(k["intro"])}
  {kfoto}
  {secties}
  <div class="artikel__cta"><p><strong>Hulp nodig?</strong> Bel {TEL_HTML} of stuur een WhatsApp met een foto van uw sleutel. U hoort direct wat het kost.</p>{knoppen()}</div>
</div></article>
{faqblok(k["faq"], "Vragen hierover")}
{formulier("kennis-" + k["slug"])}
""")

# ============================================================
# MERKEN
# ============================================================
merk_kaarten = "".join(f'<a class="merk" href="/{s}"><b>{n}</b><span>Alle sleuteltypen · vanaf {P_KOPIE.split(" – ")[0]}</span></a>' for n, s, typen, *_ in MERKEN)
pagina("merken.html", f"Autosleutel bijmaken per merk | {HANDELSNAAM}",
       "Per automerk: welke sleuteltypen er zijn, wat wij bijmaken en repareren, en wat het kost. Van Volkswagen tot Jaguar.",
       "/merken", jsonld=[kruimels_jsonld([("Home", "/"), ("Merken", "/merken")])],
       body=f"""
{kruimels([("Home", "/"), ("Merken", "")])}
<section class="sectie sectie--kort"><div class="wrap">
  <h1>Autosleutel per merk</h1>
  <p class="intro">Ieder merk heeft zijn eigen sleutelgeneraties en eigenaardigheden. Kies uw merk en lees wat wij kunnen en wat het kost.</p>
  <div class="merk-lijst">{merk_kaarten}</div>
  <p class="noot">Staat uw merk er niet bij? Bel {TEL_HTML}: de kans is groot dat het toch kan.</p>
</div></section>
{formulier("merken")}
""")
for m in MERKEN:
    naam, slug, typen, tekst1, tekst2, _key, *fotoinfo = m
    fotohtml = ""
    if fotoinfo:
        fotohtml = f'<figure class="media__foto">{foto(fotoinfo[0], fotoinfo[1], lazy=False)}<figcaption>{fotoinfo[1]}</figcaption></figure>'
    # Bewust ALLE sleuteltypen tonen: welk type een auto heeft verschilt per model en bouwjaar, dus wij gaan er niet vanuit maar vragen het de klant.
    typelinks = "".join(f'<a class="kies kies--klein" href="/{t["slug"]}">{icoon(t["icoon"])}<span>{t["naam"]}</span></a>' for t in SLEUTELTYPEN)
    prijs = P_KOPIE
    mfaq = [(f"Wat kost een {naam}-sleutel bijmaken?",
             f"Dat hangt af van het sleuteltype: een transpondersleutel {P_KOPIE}, een klapsleutel {P_KLAP}, een sleutelkaart {P_KAART}, een smartkey {P_SMART}. Bent u alle sleutels kwijt, dan verschilt de prijs sterk per model en bouwjaar. Uw kenteken geeft de exacte prijs."),
            (f"Welk sleuteltype heeft mijn {naam}?",
             "Dat verschilt per model en bouwjaar, dus daar gaan wij niet vanuit. Kijk naar uw sleutel: klapt de baard uit (klapsleutel), start u met een knop (smartkey), is het een platte kaart (sleutelkaart) of een vaste sleutel zonder knopjes (transpondersleutel)? Twijfelt u, stuur dan een foto via WhatsApp."),
            (f"Kan het ook als ik alle {naam}-sleutels kwijt ben?",
             "Bij de meeste modellen wel. Neem kentekenbewijs en identiteitsbewijs mee; wij wissen de oude sleutels uit de auto.")]
    pagina(slug + ".html", f"{naam} autosleutel bijmaken Hengelo | {prijs.split(' – ')[0].replace('€ ', 'vanaf € ')}",
           f"{naam}-sleutel kwijt, kapot of een reserve nodig? {tekst1[:120].rsplit(' ', 1)[0]}… Vaste prijs via kenteken, {REISTIJD} vanaf Hengelo of aan huis.",
           "/" + slug,
           jsonld=[faq_jsonld(mfaq), kruimels_jsonld([("Home", "/"), ("Merken", "/merken"), (naam, "/" + slug)])],
           beeld=fotoinfo[0] if fotoinfo else None,
           body=f"""
{kruimels([("Home", "/"), ("Merken", "/merken"), (naam, "")])}
<section class="sectie sectie--kort">
  <div class="wrap {'media' if fotohtml else 'wrap--tekst'}">
    <div>
      <h1>{naam} autosleutel bijmaken in Hengelo</h1>
      {antwoord(f"Voor {naam} maken wij transpondersleutels, klapsleutels, smartkeys en sleutelkaarten bij, inclusief het programmeren op uw auto. "
                f"Welk type uw {naam} heeft, hangt af van model en bouwjaar; wij vragen het u, of zien het aan uw kenteken. "
                f"Richtprijs vanaf {prijs.split(' – ')[0]}, meestal klaar terwijl u wacht in onze werkplaats, {REISTIJD} vanaf Hengelo. Ook aan huis.")}
      <p>{tekst1}</p>
      {f"<p>{tekst2}</p>" if tekst2 else ""}
      {knoppen()}
    </div>
    {fotohtml}
  </div>
</section>
<section class="sectie sectie--zand"><div class="wrap"><div class="sectie__kop"><h2>Welk sleuteltype heeft uw {naam}?</h2><p>Dat verschilt per model en bouwjaar. Kies het type dat op uw sleutel lijkt; u ziet dan meteen de richtprijs. Twijfelt u? Stuur een foto via <a href="{WA_LINK}" rel="noopener" data-conv="whatsapp">WhatsApp</a>.</p></div><div class="kiezer kiezer--klein">{typelinks}</div></div></section>
{faqblok(mfaq, f"Vragen over {naam}")}
{formulier("merk-" + slug)}
""")

# ============================================================
# BEDANKT + PRIVACY
# ============================================================
pagina("bedankt.html", f"Bedankt | {HANDELSNAAM}", "Uw aanvraag is verstuurd.", "/bedankt", noindex=True, body=f"""
<section class="sectie"><div class="wrap wrap--tekst">
  <h1>Uw aanvraag is verstuurd</h1>
  <p>Wij bekijken uw kenteken en sturen u dezelfde werkdag een vaste prijs, met daarbij wanneer u terecht kunt of wanneer wij bij u kunnen zijn. Heeft u haast? Bel gerust.</p>
  {knoppen()}
  <p class="review-tip">{icoon("ster")}Al eerder bij ons geweest? Een korte <a href="{REVIEW_LINK}" rel="noopener" data-conv="review">Google-review voor Autosleutel Hengelo</a> helpt andere automobilisten uit Hengelo ons te vinden.</p>
</div></section>
""")

pagina("privacy.html", f"Privacyverklaring | {HANDELSNAAM}",
       f"Hoe {HANDELSNAAM} ({RECHTSPERSOON}) omgaat met uw persoonsgegevens.", "/privacy",
       jsonld=[kruimels_jsonld([("Home", "/"), ("Privacyverklaring", "/privacy")])],
       body=f"""
{kruimels([("Home", "/"), ("Privacyverklaring", "")])}
<section class="sectie sectie--kort"><div class="wrap wrap--tekst artikel">
  <h1>Privacyverklaring</h1>
  <p><em>Laatst bijgewerkt: {PRIVACY_DATUM}</em></p>
  <h2>Wie zijn wij</h2>
  <p>{HANDELSNAAM} is een onderdeel van <strong>{RECHTSPERSOON}</strong>, gevestigd aan de {VESTIGING} (KvK {KVK}). Onze werkplaats en winkel zijn te vinden aan de {STRAAT}, {POSTCODE} {PLAATS}. Vragen over privacy: <a href="mailto:{MAIL}">{MAIL}</a> of {TEL_HTML}.</p>
  <h2>Welke gegevens wij verwerken</h2>
  <ul>
    <li><strong>Prijsaanvraag:</strong> kenteken, sleuteltype, naam, telefoonnummer, gewenste locatie en uw toelichting.</li>
    <li><strong>Telefoon, e-mail en WhatsApp:</strong> wat u ons zelf stuurt, inclusief eventuele foto's van uw sleutel.</li>
    <li><strong>Aan huis:</strong> het adres waar de auto staat, alleen voor die afspraak.</li>
    <li><strong>In de werkplaats en aan huis:</strong> wij controleren uw kentekenbewijs en identiteitsbewijs voordat wij een sleutel maken. Wij kijken alleen; wij maken geen kopie of foto en slaan de gegevens daaruit niet op.</li>
    <li><strong>Websitebezoek:</strong> technische gegevens die nodig zijn om de site te tonen. Wij houden geen bezoekersstatistieken bij en gebruiken geen advertentiecookies.</li>
  </ul>
  <h2>Waarvoor</h2>
  <ul>
    <li>Uw aanvraag beantwoorden en een prijs en afspraak geven.</li>
    <li>De opdracht uitvoeren en factureren (wettelijke bewaarplicht).</li>
    <li>Controleren dat u eigenaar of gebruiker van de auto bent (gerechtvaardigd belang: misbruik voorkomen).</li>
  </ul>
  <p>Wij verkopen uw gegevens niet en gebruiken ze niet voor andere doelen.</p>
  <h2>Cookies</h2>
  <p>Deze website gebruikt <strong>geen tracking-, analyse- of advertentiecookies</strong>. Daarom ziet u geen cookiemelding. Verandert dat, dan vragen wij eerst uw toestemming en passen wij deze verklaring aan.</p>
  <h2>Met wie wij gegevens delen</h2>
  <ul>
    <li><strong>Vercel</strong> — hosting van deze website.</li>
    <li><strong>Web3Forms</strong> — verzendt uw formulieraanvraag per e-mail naar ons.</li>
    <li><strong>Google</strong> — lettertypen van deze website (Google Fonts).</li>
    <li><strong>WhatsApp (Meta)</strong> — alleen als u ons zelf via WhatsApp benadert.</li>
  </ul>
  <p>Sommige van deze partijen zijn gevestigd buiten de EU. Doorgifte gebeurt op basis van de waarborgen die de AVG voorschrijft. Daarnaast verstrekken wij gegevens als de wet ons daartoe verplicht.</p>
  <h2>Bewaartermijnen</h2>
  <ul>
    <li>Aanvragen die niet tot een opdracht leiden: uiterlijk 12 maanden.</li>
    <li>Gegevens van opdrachten en facturen: 7 jaar (fiscale bewaarplicht).</li>
  </ul>
  <h2>Uw rechten</h2>
  <p>U kunt uw gegevens inzien, laten corrigeren of verwijderen, bezwaar maken, de verwerking laten beperken en uw gegevens opvragen. Stuur uw verzoek naar <a href="mailto:{MAIL}">{MAIL}</a>; wij reageren binnen een maand. Klachten kunt u indienen bij de <a href="https://autoriteitpersoonsgegevens.nl" rel="noopener">Autoriteit Persoonsgegevens</a>.</p>
</div></section>
""")

# ============================================================
# sitemap, robots, llms.txt
# ============================================================
paden = ["/", "/autosleutel-bijmaken", "/autosleutel-kwijt", "/prijzen", "/aan-huis", "/contact", "/kennis", "/merken", "/privacy"] + \
        ["/" + t["slug"] for t in SLEUTELTYPEN] + ["/" + k["slug"] for k in KENNIS] + ["/" + m[1] for m in MERKEN]
urls = "".join(f"<url><loc>{SITE}{p}</loc><changefreq>monthly</changefreq><priority>{'1.0' if p == '/' else '0.7'}</priority></url>" for p in paden)
(OUT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>', encoding="utf-8")
(OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /bedankt\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
(OUT / "llms.txt").write_text(f"""# {HANDELSNAAM}

Autosleutelspecialist voor Hengelo en omgeving ({", ".join(PLAATSEN)}). Onderdeel van {RECHTSPERSOON};
zusterbedrijf van {MOEDER} ({MOEDER_URL}). Werkplaats: {STRAAT}, {POSTCODE} {PLAATS} — {REISTIJD} vanaf Hengelo.

## Feiten
- Telefoon {TEL_TONEN}, WhatsApp, e-mail {MAIL}. Open di–vr 09:00–17:30, za 09:00–17:00.
- Maakt, programmeert en repareert klapsleutels, smartkeys, sleutelkaarten en transpondersleutels voor vrijwel elk merk.
- Richtprijzen incl. programmeren en btw: transpondersleutel {P_KOPIE}; klapsleutel {P_KLAP}; sleutelkaart {P_KAART}; smartkey {P_SMART}; reparatie {P_REP}. Alle sleutels kwijt (geen werkend exemplaar): prijs op aanvraag, verschilt sterk per merk en bouwjaar.
- Aan-huisservice in Hengelo vanaf € {AAN_HUIS_VANAF} bovenop de sleutelprijs; omgeving op aanvraag.
- Meestal klaar terwijl u wacht (20–30 minuten). Levenslange garantie op de chip, 2 jaar op een nieuwe afstandsbediening.
- Westendorp bestaat sinds {SINDS}; maakt jaarlijks meer dan {PER_JAAR} autosleutels bij.
- Benodigd: kenteken (voor de prijs), kentekenbewijs en identiteitsbewijs (bij het maken).

## Pagina's
{chr(10).join(f"- {SITE}{p}" for p in paden)}
""", encoding="utf-8")

print(f"Gebouwd: {len(paden) + 1} pagina's")
