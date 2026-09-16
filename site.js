// Autosleutel Hengelo — geen frameworks. Meten alleen met toestemming van de bezoeker.
(function () {
  // Formulier uit zolang de Web3Forms-key een placeholder is.
  document.querySelectorAll('form[data-key]').forEach(function (f) {
    if (f.getAttribute('data-key').indexOf('VUL-HIER') !== 0) return;
    var knop = f.querySelector('button[type=submit]');
    var melding = f.querySelector('.form-uit');
    if (knop) { knop.disabled = true; knop.style.opacity = '.5'; knop.style.cursor = 'not-allowed'; }
    if (melding) melding.hidden = false;
    f.addEventListener('submit', function (e) { e.preventDefault(); });
  });

  // Mobiel menu (hamburger in de header).
  var menuKnop = document.querySelector('.top__menu'), menu = document.getElementById('mobielmenu');
  if (menuKnop && menu) menuKnop.addEventListener('click', function () {
    var open = menu.hidden; menu.hidden = !open; menuKnop.setAttribute('aria-expanded', String(open));
  });

  // Kenteken netjes in hoofdletters.
  document.querySelectorAll('#kenteken-veld, #kenteken, #f-kenteken').forEach(function (i) {
    i.addEventListener('input', function () { i.value = i.value.toUpperCase(); });
  });

  // Belbalk (mobiel) pas tonen voorbij de hero, zodat hij niet botst met de knoppen bovenaan.
  var balk = document.querySelector('.belbalk');
  if (balk) {
    var regel = function () { balk.classList.toggle('is-verborgen', window.pageYOffset < 420); };
    regel();
    window.addEventListener('scroll', regel, { passive: true });
  }

  // Kentekencheck bij de RDW (open data, geen key): de klant ziet meteen of het kenteken klopt.
  // Niet gevonden of geen kenteken bij de hand: velden merk, model en bouwjaar verschijnen.
  (function () {
    var kt = document.getElementById('kenteken-veld');
    var check = document.getElementById('f-kenteken-check');
    var voertuig = document.getElementById('f-voertuig');
    var autovelden = document.getElementById('f-autovelden');
    var geenKt = document.getElementById('f-geen-kenteken');
    if (!kt || !check) return;
    var ICO_OK = '<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="m8.5 12.5 2.5 2.5 4.5-5"/></svg>';
    var ICO_NEE = '<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="m9 9 6 6M15 9l-6 6"/></svg>';
    var ICO_AUTO = '<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 13l2-5.5A2 2 0 0 1 6.9 6h10.2a2 2 0 0 1 1.9 1.5L21 13v5a1 1 0 0 1-1 1h-1a1 1 0 0 1-1-1v-1H6v1a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1z"/><circle cx="7.5" cy="14.5" r="1"/><circle cx="16.5" cy="14.5" r="1"/></svg>';
    var laatste = '', timer = null;
    function toonAutovelden(aan) {
      if (!autovelden) return;
      autovelden.hidden = !aan;
      kt.required = !aan;
      ['f-merk', 'f-model', 'f-bouwjaar'].forEach(function (id) { var el = document.getElementById(id); if (el) el.required = aan; });
    }
    function jaar(d) { return d && d.length >= 4 ? d.slice(0, 4) : ''; }
    function mooi(s) { s = s || ''; if (/\d/.test(s)) return s; s = s.toLowerCase(); return s.replace(/(^|[\s-])([a-zà-ÿ])/g, function (m, p, c) { return p + c.toUpperCase(); }); }
    function zoek(kenteken) {
      check.hidden = false; check.className = 'kentekencheck is-bezig'; check.innerHTML = ICO_AUTO + '<span>Kenteken opzoeken bij de RDW…</span>';
      fetch('https://opendata.rdw.nl/resource/m9d7-ebf2.json?kenteken=' + encodeURIComponent(kenteken))
        .then(function (r) { return r.ok ? r.json() : []; })
        .then(function (d) {
          if (kenteken !== laatste) return;
          var v = d && d[0];
          if (v && v.merk) {
            var naam = (mooi(v.merk) + ' ' + mooi(v.handelsbenaming || '')).trim(), bj = jaar(v.datum_eerste_toelating);
            var kleur = v.eerste_kleur && v.eerste_kleur !== 'Niet geregistreerd' ? mooi(v.eerste_kleur) : '';
            var extra = [bj ? 'bouwjaar ' + bj : '', kleur].filter(Boolean).join(' · ');
            check.className = 'kentekencheck is-ok';
            check.innerHTML = ICO_OK + '<span><b>' + naam + '</b>' + (extra ? extra + ' · ' : '') + 'klopt dit? Dan zien wij precies welke sleutel u nodig heeft.</span>';
            if (voertuig) voertuig.value = naam + (bj ? ' (' + bj + ')' : '');
            toonAutovelden(false);
          } else {
            check.className = 'kentekencheck is-fout';
            check.innerHTML = ICO_NEE + '<span><b>Kenteken niet gevonden</b>Controleer de letters en cijfers, of vul hieronder merk, model en bouwjaar in.</span>';
            if (voertuig) voertuig.value = '';
            toonAutovelden(true);
          }
        })
        .catch(function () { check.hidden = true; });
    }
    kt.addEventListener('input', function () {
      var schoon = kt.value.toUpperCase().replace(/[^A-Z0-9]/g, '');
      clearTimeout(timer);
      if (schoon.length === 6) { laatste = schoon; timer = setTimeout(function () { zoek(schoon); }, 350); }
      else { laatste = ''; check.hidden = true; if (voertuig) voertuig.value = ''; }
    });
    if (geenKt) geenKt.addEventListener('click', function () { toonAutovelden(autovelden && autovelden.hidden); if (autovelden && !autovelden.hidden) { var m = document.getElementById('f-merk'); m && m.focus(); } });
  })();

  // Vragen per onderwerp: bijmaken (start, afstandsbediening, situatie) of repareren (wat is er kapot).
  (function () {
    var ond = document.getElementById('f-onderwerp');
    if (!ond) return;
    function toon() {
      document.querySelectorAll('.veldgroep').forEach(function (g) {
        var aan = g.getAttribute('data-voor') === ond.value;
        g.hidden = !aan;
        g.querySelectorAll('select').forEach(function (s) { s.required = aan; });
      });
    }
    ond.addEventListener('change', toon); toon();
  })();

  // Bedankt-pagina op het adres waar de site nu draait (vercel.app of eigen domein) en dubbel verzenden voorkomen.
  document.querySelectorAll('form').forEach(function (f) {
    var r = f.querySelector('input[name="redirect"]');
    if (r) r.value = location.origin + (r.value.indexOf('/bedankt/') > -1 ? '/bedankt/' : '/bedankt');
    f.addEventListener('submit', function () {
      var b = f.querySelector('button[type=submit]');
      if (f.dataset.bezig) return;
      f.dataset.bezig = '1';
      if (b) { b.disabled = true; b.textContent = 'Versturen…'; }
    });
  });

  // Lege velden niet meesturen: de aanvraagmail toont dan alleen wat is ingevuld.
  document.querySelectorAll('form').forEach(function (f) {
    f.addEventListener('submit', function () {
      f.querySelectorAll('input, select, textarea').forEach(function (el) {
        if (el.type === 'submit' || el.type === 'checkbox' || el.name === 'access_key' || el.name === 'redirect' || el.name === 'subject' || el.name === 'from_name') return;
        var leeg = !String(el.value || '').trim();
        var verborgen = el.closest('[hidden]');
        if (leeg || verborgen) el.disabled = true;
      });
    });
  });

  // Onderwerpregel van de aanvraagmail: wat, welk kenteken en welke auto, zodat de mailbox in één oogopslag leesbaar is.
  document.querySelectorAll('form').forEach(function (f) {
    var sub = f.querySelector('input[name="subject"]');
    if (!sub) return;
    var basis = sub.value;
    f.addEventListener('submit', function () {
      var v = function (sel) { var el = f.querySelector(sel); return el && el.value ? String(el.value).trim() : ''; };
      var kt = v('input[name="Kenteken"]').toUpperCase().replace(/[^A-Z0-9]/g, '');
      var auto = v('input[name="Auto volgens RDW"]') || [v('input[name="Merk"]'), v('input[name="Model"]'), v('input[name="Bouwjaar"]')].filter(Boolean).join(' ');
      var wat = v('select[name="Onderwerp"]') || 'Aanvraag';
      var sit = v('select[name="Situatie"]'); if (sit) wat += sit.indexOf('kwijt') > -1 ? ' (alle sleutels kwijt)' : ' (reserve)';
      var naam = v('input[name="Naam"]');
      sub.value = [wat, kt, auto, naam].filter(Boolean).join(' · ') + ' · ' + basis;
    });
  });

  // ---------- Toestemming (Consent Mode v2) en gebeurtenissen ----------
  // Zonder toestemming meet Google niets. De keuze onthouden wij in de browser van de bezoeker.
  var heeftTag = typeof window.gtag === 'function';
  var cb = document.getElementById('cookiebalk');
  if (heeftTag && cb) {
    var keuze = null; try { keuze = localStorage.getItem('consent'); } catch (e) {}
    var adsVink = document.getElementById('cookie-ads');
    var aanpassen = cb.querySelector('[data-cookie="aanpassen"]');
    var huidigTab = 'toestemming';
    var consent = function (c) {
      var v = c === 'granted' ? 'granted' : 'denied';
      gtag('consent', 'update', { ad_storage: v, ad_user_data: v, ad_personalization: v, analytics_storage: v });
    };
    var tab = function (naam) {
      huidigTab = naam;
      cb.querySelectorAll('[data-tab]').forEach(function (t) { t.setAttribute('aria-selected', t.getAttribute('data-tab') === naam ? 'true' : 'false'); });
      cb.querySelectorAll('[data-paneel]').forEach(function (p) { p.hidden = p.getAttribute('data-paneel') !== naam; });
      aanpassen.textContent = naam === 'details' ? 'Keuze opslaan' : 'Aanpassen';
      cb.querySelector('[data-consent="denied"]').hidden = naam !== 'details';
      document.getElementById('cookie-knoppen').classList.toggle('met-weigeren', naam === 'details');
    };
    var openen = function () {
      adsVink.checked = keuze === 'granted';
      tab('toestemming');
      cb.hidden = false;
      document.documentElement.classList.add('cookie-open');
    };
    var kies = function (c) {
      keuze = c;
      try { localStorage.setItem('consent', c); } catch (e) {}
      consent(c);
      cb.hidden = true;
      document.documentElement.classList.remove('cookie-open');
    };
    if (keuze === 'granted') consent('granted');
    if (!keuze) openen();
    cb.querySelectorAll('[data-tab]').forEach(function (t) { t.addEventListener('click', function () { tab(t.getAttribute('data-tab')); }); });
    cb.querySelectorAll('button[data-consent]').forEach(function (b) { b.addEventListener('click', function () { kies(b.getAttribute('data-consent')); }); });
    aanpassen.addEventListener('click', function () {
      if (huidigTab === 'details') kies(adsVink.checked ? 'granted' : 'denied'); else tab('details');
    });
    document.querySelectorAll('[data-cookie="open"]').forEach(function (b) { b.addEventListener('click', openen); });
  }

  // Aanvraag: telt op de bedanktpagina, één keer per bezoek.
  if (heeftTag && /^\/bedankt(\.html)?\/?$/.test(location.pathname)) {
    var alGeteld = false;
    try { alGeteld = sessionStorage.getItem('conv_formulier') === '1'; sessionStorage.setItem('conv_formulier', '1'); } catch (e) {}
    if (!alGeteld) gtag('event', 'formulier_verzonden');
  }

  // Klikken op bellen, WhatsApp, route en kenteken.
  document.addEventListener('click', function (e) {
    var el = e.target.closest('[data-conv]');
    if (!el || !window.gtag) return;
    var soort = el.getAttribute('data-conv');
    gtag('event', soort === 'bellen' ? 'tel_klik' : soort === 'whatsapp' ? 'whatsapp_klik'
      : soort === 'route' ? 'route_klik' : soort === 'kenteken' ? 'kenteken_klik' : 'klik_' + soort);
  });
})();
