// Autosleutel Hengelo — geen frameworks, geen cookies, geen trackers.
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

  // Kenteken netjes in hoofdletters.
  document.querySelectorAll('input[name=kenteken]').forEach(function (i) {
    i.addEventListener('input', function () { i.value = i.value.toUpperCase(); });
  });

  // Belbalk (mobiel) pas tonen voorbij de hero, zodat hij niet botst met de knoppen bovenaan.
  var balk = document.querySelector('.belbalk');
  if (balk) {
    var regel = function () { balk.classList.toggle('is-verborgen', window.pageYOffset < 420); };
    regel();
    window.addEventListener('scroll', regel, { passive: true });
  }
})();
