# autosleutel-hengelo.nl

Statische site voor Autosleutel Hengelo (Westendorp Groep VOF). Geen framework: `build.py` genereert alle HTML.

| Bestand | Wat |
|---|---|
| `build.py` | Alle teksten, prijzen, sleuteltypen, merken en kennisartikelen staan bovenin in CONFIG. Draai `python build.py`. |
| `styles.css`, `site.js` | Opmaak en het beetje script (formulier, belbalk). |
| `fotos.py` | Verkleint originelen uit `foto-origineel/` naar `img/`. Niet-verkleinde originelen horen niet in git. |
| `vercel.json` | Redirects (www → kaal domein, oude one.com-URL's) en cache. |

## Aanpassen
1. Wijzig iets in het CONFIG-blok van `build.py`.
2. `python build.py`
3. Commit en push naar `main`; Vercel zet het live.

## Vóór livegang
- `WEB3FORMS_KEY`: eigen key voor deze site (web3forms.com, gekoppeld aan autosleutel@westendorpgroep.nl). Tot die tijd staat het formulier uit.
- `GBP_LINK`, `GBP_SCORE`, `GBP_AANTAL`: vaste Google Maps-link en de reviewscore van het Hengelo-bedrijfsprofiel.
- Foto's in `img/` (zie `fotos.py`). Ontbreekt een foto, dan toont de site een plekhouder.
- `img/favicon.png` en `img/og-autosleutel-hengelo.jpg` (deelafbeelding 1200×630).

## Afspraken
- Deze site is bewust anders dan autosleutel-almelo.nl: eigen structuur (per sleuteltype), eigen teksten, eigen foto's, eigen ontwerp. Niets kopiëren tussen de sites.
- Werkgebied: Hengelo-kant van Twente (PLAATSEN). Almelo e.o. hoort bij autosleutel-almelo.nl, Enschede bij autosleutel-enschede.nl.
- De werkplaats is en blijft Wesseler-Nering 32, Enschede. Geen nep-adres in Hengelo.
