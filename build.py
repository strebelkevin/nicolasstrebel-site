#!/usr/bin/env python3
"""
Static-site generator for nicolasstrebel.com.

This emits plain, self-contained .html files (no build step needed to host or
edit afterwards). It exists only to keep the shared nav / footer / <head> /
SEO blocks identical across every page. If you change page *content*, just edit
the .html directly. If you change the nav or footer, edit it here and re-run:

    python3 build.py

Author: assembled for Nicolas Strebel.
"""
import os
import time
from urllib.parse import quote

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://nicolasstrebel.com"
VERSION = str(int(time.time()))  # cache-buster for css/js, refreshed each build

# ---- Contact constants -----------------------------------------------------
WA_NUMBER = "34670260445"
PHONE_DISPLAY = "+34 670 260 445"
EMAIL = "info@nicolasstrebel.com"
ADDRESS = "Camino del Campamento 44, 03724 Teulada, Alicante"
HOURS = "Mon–Fri 09:00–14:00"

def wa(text="Hello Nicolas, I found your website and would like to arrange a conversation about the Costa Blanca."):
    return f"https://wa.me/{WA_NUMBER}?text=" + quote(text)

WA_DEFAULT = wa()

# ---- Navigation ------------------------------------------------------------
NAV_ITEMS = [
    ("index.html", "Home"),
    ("real-estate.html", "Real Estate"),
    ("home-projects.html", "Home Projects"),
    ("properties.html", "Properties"),
    ("investors-club.html", "Investor's Club"),
    ("about.html", "About"),
    ("contact.html", "Contact"),
]

WA_ICON = ('<svg class="icon" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
           '<path d="M12.04 2c-5.5 0-9.96 4.46-9.96 9.96 0 1.76.46 3.45 1.34 4.95L2 22l5.25-1.38a9.9 9.9 0 0 0 4.79 1.22c5.5 0 9.96-4.46 9.96-9.96 0-2.66-1.04-5.16-2.92-7.04A9.9 9.9 0 0 0 12.04 2Zm0 18.02a8.2 8.2 0 0 1-4.18-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.27 8.27 0 1 1 6.97 3.86Zm4.53-6.16c-.25-.12-1.47-.72-1.7-.81-.23-.08-.39-.12-.56.13-.16.25-.64.81-.79.97-.14.17-.29.19-.54.06-.25-.12-1.05-.39-2-1.23-.74-.66-1.24-1.48-1.38-1.73-.14-.25-.02-.38.11-.51.11-.11.25-.29.37-.43.12-.14.16-.25.25-.41.08-.17.04-.31-.02-.43-.06-.12-.56-1.34-.76-1.84-.2-.48-.4-.42-.56-.43h-.48c-.17 0-.43.06-.66.31-.23.25-.86.85-.86 2.07 0 1.22.89 2.4 1.01 2.56.12.17 1.75 2.67 4.23 3.74.59.26 1.05.41 1.41.52.59.19 1.13.16 1.56.1.48-.07 1.47-.6 1.68-1.18.21-.58.21-1.07.14-1.18-.06-.1-.22-.16-.47-.28Z"/></svg>')

ARROW = ('<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
         'stroke-width="1.8"><path d="M5 12h14M13 6l6 6-6 6"/></svg>')

def icon(path, sw="1.5"):
    return (f'<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{path}</svg>')

I_BED = '<path d="M3 18v-6a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2v6M3 18h18M3 18v2M21 18v2M7 10V8a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v2"/>'
I_BATH = '<path d="M4 12h16v3a4 4 0 0 1-4 4H8a4 4 0 0 1-4-4v-3ZM6 12V6a2 2 0 0 1 2-2 2 2 0 0 1 2 2"/>'
I_AREA = '<path d="M3 3h7v7H3zM14 3h7v7h-7zM14 14h7v7h-7zM3 14h7v7H3z"/>'
I_POOL = '<path d="M2 18c2 0 2-2 4-2s2 2 4 2 2-2 4-2 2 2 4 2 2-2 4-2M6 14V5a2 2 0 0 1 4 0M14 14V5a2 2 0 0 1 4 0"/>'
I_CHECK = '<path d="M5 12l5 5 9-11"/>'
I_CROSS = '<path d="M6 6l12 12M18 6L6 18"/>'

def ticklist(items):
    """Short, scannable bullet list with accent ticks (for the lean look & feel)."""
    lis = "".join(f'<li>{icon(I_CHECK, "2")}<span>{t}</span></li>' for t in items)
    return f'<ul class="tick-list">{lis}</ul>'

def nav(active, over_hero=False):
    links = "".join(
        f'<li><a href="{href}"{" aria-current=\"page\"" if href==active else ""}>{label}</a></li>'
        for href, label in NAV_ITEMS
    )
    cls = "nav nav--over-hero" if over_hero else "nav"
    return f'''<a class="skip-link" href="#main">Skip to content</a>
  <header class="{cls}">
    <div class="container nav__inner">
      <a class="nav__brand" href="index.html" aria-label="Nicolas Strebel - home">
        <img class="nav__logo" src="assets/logo/logo-ns.png" alt="Nicolas Strebel - Real Estate" width="350" height="119" />
      </a>
      <nav aria-label="Primary">
        <ul class="nav__links" id="primary-nav">{links}</ul>
      </nav>
      <div class="nav__actions">
        <div class="lang">
          <button class="lang-toggle" type="button" aria-haspopup="true" aria-expanded="false" data-lang-toggle>EN
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg>
          </button>
          <div class="lang__menu" data-lang-menu>
            <a href="#" aria-current="true">English <small>EN</small></a>
            <a href="#" aria-disabled="true">Deutsch <small>bald</small></a>
            <a href="#" aria-disabled="true">Nederlands <small>binnenkort</small></a>
          </div>
        </div>
        <a class="btn btn--whatsapp" href="{WA_DEFAULT}" target="_blank" rel="noopener">{WA_ICON}WhatsApp</a>
      </div>
      <button class="nav__toggle" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="primary-nav">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
      </button>
    </div>
  </header>'''

def footer():
    re_links = "".join(f'<li><a href="{h}">{l}</a></li>' for h,l in [
        ("real-estate.html","Real Estate overview"),("buyers-advisor.html","Buying &amp; selling"),
        ("investing.html","Investing"),("buyers-advisor.html#relocation","Relocation"),("properties.html","Properties")])
    hp_links = "".join(f'<li><a href="{h}">{l}</a></li>' for h,l in [
        ("home-projects.html","Home Projects overview"),("new-build-villas-costa-blanca.html","New-build villas"),
        ("renovation-refurbishment-costa-blanca.html","Renovation &amp; refurbishment"),("interior-design-costa-blanca.html","Interior design &amp; furniture"),
        ("project-coordination.html","Project coordination")])
    about = "".join(f'<li><a href="{h}">{l}</a></li>' for h,l in [
        ("about.html","About"),("investors-club.html","Investor's Club"),("about.html#areas","Areas covered"),("contact.html","Contact")])
    return f'''<footer class="footer">
    <div class="container">
      <div class="footer__grid">
        <div>
          <img class="footer__logo" src="assets/logo/logo-footer.png" alt="Nicolas Strebel - Real Estate" width="350" height="119" />
          <p style="color:rgba(255,255,255,0.7); max-width:32ch;">Independent advisor for <strong style="color:#fff;font-weight:600;">Real Estate &amp; Home Projects</strong> on the Costa Blanca North - one accountable point of contact for buying, selling, building, renovating, designing and investing.</p>
          <div class="pill-row" style="margin-top:1.25rem;">
            <span class="pill">25+ years</span><span class="pill">500+ sold</span><span class="pill">50+ built</span>
          </div>
        </div>
        <div>
          <h4>Real Estate</h4><ul>{re_links}</ul>
          <h4 style="margin-top:1.5rem;">Home Projects</h4><ul>{hp_links}</ul>
        </div>
        <div><h4>Company</h4><ul>{about}</ul></div>
        <div><h4>Contact</h4><ul>
          <li><a href="{WA_DEFAULT}" target="_blank" rel="noopener">{PHONE_DISPLAY}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li>{ADDRESS}</li>
          <li>{HOURS}</li>
        </ul></div>
      </div>
      <div class="footer__bottom">
        <span>© <span id="year">2026</span> Nicolas Strebel · <a href="legal.html#legal">Legal notice</a> · <a href="legal.html#privacy">Privacy</a> · <a href="legal.html#cookies">Cookies</a></span>
        <span>Moraira · Calpe · Jávea · Benissa · Benitachell · Cumbre del Sol · Altea · Teulada</span>
      </div>
    </div>
  </footer>
  <div class="cookie-banner" data-cookie-banner hidden>
    <p>This site uses only essential cookies to work - no tracking or advertising. <a href="legal.html#cookies">Cookie policy</a>.</p>
    <button type="button" class="btn btn--primary cookie-banner__ok" data-cookie-ok>Got it</button>
  </div>
  <a class="wa-float" href="{WA_DEFAULT}" target="_blank" rel="noopener" aria-label="Message Nicolas on WhatsApp">{WA_ICON}</a>
  <script src="js/main.js?v={VERSION}" defer></script>'''

SITEMAP_URLS = []

def page(filename, title, description, body, active, extra_head="", og_image="assets/images/hero/home-hero.webp", over_hero=False):
    canonical = f"{SITE}/{'' if filename=='index.html' else filename}"
    if not (filename.startswith("index-alt") or filename in ("styleguide.html", "404.html")):
        SITEMAP_URLS.append(canonical)
    htmldoc = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{description}" />
  <link rel="canonical" href="{canonical}" />
  <meta name="theme-color" content="#22323F" />
  <link rel="icon" href="assets/logo/favicon-ns.png" />

  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="Nicolas Strebel" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="{og_image if og_image.startswith('http') else f'{SITE}/{og_image}'}" />
  <meta name="twitter:card" content="summary_large_image" />

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="css/styles.css?v={VERSION}" />
{extra_head}
</head>
<body>
  {nav(active, over_hero=over_hero)}
  <main id="main">
{body}
  </main>
  {footer()}
</body>
</html>
'''
    with open(os.path.join(ROOT, filename), "w", encoding="utf-8") as f:
        f.write(htmldoc)
    print("wrote", filename)


# ---- Shared JSON-LD --------------------------------------------------------
JSONLD_BUSINESS = f'''  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "RealEstateAgent",
    "name": "Nicolas Strebel - Real Estate, Construction & Investment",
    "image": "{SITE}/assets/images/nicolas/portrait-studio.jpg",
    "url": "{SITE}",
    "telephone": "+34670260445",
    "email": "{EMAIL}",
    "priceRange": "€€€",
    "areaServed": ["Moraira","Calpe","Jávea","Benissa","Benitachell","Cumbre del Sol","Altea","Teulada"],
    "address": {{"@type": "PostalAddress","streetAddress": "Camino del Campamento 44","postalCode": "03724","addressLocality": "Teulada","addressRegion": "Alicante","addressCountry": "ES"}},
    "openingHours": "Mo-Fr 09:00-14:00",
    "knowsLanguage": ["de","en","fr","it","es"]
  }}
  </script>'''

JSONLD_PERSON = f'''  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Person",
    "name": "Nicolas Strebel",
    "jobTitle": "Real Estate & Building Consultant",
    "image": "{SITE}/assets/images/nicolas/portrait-studio.jpg",
    "worksFor": {{"@type":"Organization","name":"Nicolas Strebel"}},
    "knowsLanguage": ["German","English","French","Italian","Spanish"],
    "areaServed": "Costa Blanca North, Spain",
    "url": "{SITE}/about.html"
  }}
  </script>'''


# ---- Property data ---------------------------------------------------------
PROPERTIES = [
    {
        "id": "calpe-villa-newbuild",
        "file": "property-villa-newbuild-calpe.html",
        "tag": "New build",
        "title": "Newly Built Villa in Calpe",
        "loc": "Calpe · short walk to beach & centre",
        "price": "€1,300,000",
        "beds": "4", "baths": "3", "area": "225 m²", "pool": "Private pool",
        "cover": "05.webp",
        "type": "Villa", "region": "Calpe", "price_num": 1300000,
        "short": "A brand-new contemporary villa in a sought-after residential pocket of Calpe - walking distance to the beach and the town.",
        "desc": [
            "This brand-new villa was conceived around two ideas: contemporary, light-filled architecture and a genuinely walkable location. It sits in one of Calpe's most established residential areas, close enough to reach the beach and the centre on foot, yet quiet enough to feel private.",
            "Across its living levels the house offers four bedrooms and three bathrooms, generous open-plan living that opens to the terrace and private pool, and the kind of clean, modern finish that needs nothing added. It is ready to move into.",
            "As your advisor I'll arrange the viewing, review the licence and documentation, and walk you through the full cost of buying a new-build here - including IVA and purchase costs - before you commit to anything."
        ],
        "features": ["Contemporary new-build", "Private pool & terraces", "Walk to beach and town centre", "Open-plan living", "Move-in ready", "Quiet residential setting"],
    },
    {
        "id": "calpe-villa-residential",
        "file": "property-villa-calpe.html",
        "tag": "Villa",
        "title": "Villa in a Quiet Residential Calpe Setting",
        "loc": "Calpe · peaceful residential area",
        "price": "€499,000",
        "beds": "3", "baths": "2", "area": "180 m²", "pool": "Private pool",
        "cover": "03.webp",
        "type": "Villa", "region": "Calpe", "price_num": 499000,
        "short": "A charming, well-balanced villa in a calm residential part of Calpe - a few minutes from the beach, services and the old town.",
        "desc": [
            "Set in a peaceful residential setting, this house strikes an easy balance between tranquillity and convenience. The beach, shops and the historic centre of Calpe are all a short drive away, with the Peñón de Ifach never far from view.",
            "Inside there are three bedrooms and two bathrooms across roughly 180 m², with a private pool and outdoor space made for the Costa Blanca climate. It is a property with good bones - comfortable as it stands, with clear potential to make it your own.",
            "If you'd like, I can also cost out a light renovation or refresh through my construction arm, so you see both the as-is price and the all-in figure before deciding."
        ],
        "features": ["Private pool", "Peaceful residential location", "Minutes from beach & old town", "Renovation potential", "Mature outdoor space", "Close to all services"],
    },
    {
        "id": "calpe-apartment-la-fossa",
        "file": "property-apartment-calpe.html",
        "tag": "Apartment",
        "title": "Apartment Steps from La Fossa Beach",
        "loc": "Calpe · La Fossa beach",
        "price": "€399,000",
        "beds": "2", "baths": "2", "area": "101 m²", "pool": "Communal pool",
        "cover": "02.webp",
        "type": "Apartment", "region": "Calpe", "price_num": 399000,
        "short": "A calm, well-kept 101 m² apartment moments from La Fossa beach - turn-key, with parking available separately.",
        "desc": [
            "This 101 m² apartment is all about location and ease: La Fossa beach is just steps from the door. It has been designed for comfortable, low-maintenance living, with a relaxed atmosphere and a sensible, liveable layout.",
            "There are two bedrooms and two bathrooms, sold furnished and equipped, ready to use from day one. A parking space is available separately for €23,000.",
            "It's an ideal lock-up-and-leave second home or a sound rental proposition. I'll confirm the community fees, check the paperwork, and tell you honestly how it compares with others I'm seeing at this price."
        ],
        "features": ["Steps from La Fossa beach", "Turn-key, sold furnished", "Two bedrooms, two bathrooms", "Communal pool", "Optional parking (€23,000)", "Strong rental potential"],
    },
]

# The first three above are hand-curated and shown as "Featured" on the homepage.
FEATURED = PROPERTIES[:3]

# Additional real listings imported from his live site (data in listings.json).
# These populate the full Properties catalog. Add more the same way.
def _convert_listing(rec):
    feats = []
    if rec.get("area") and rec["area"] != "-":
        feats.append(f"{rec['area']} built")
    if rec.get("plot"):
        feats.append(f"{rec['plot']} plot")
    if rec.get("pool") and rec["pool"] != "-":
        feats.append(rec["pool"])
    feats.append(f"{rec['region']} location")
    feats += ["Mediterranean setting", "Close to amenities & beaches", "Independently advisor-vetted"]
    desc = (rec.get("desc_full") or rec.get("short") or "").strip()
    paras = [desc] if desc else ["Full details and a private viewing are available on request."]
    paras.append("As your buyer's advisor I'll verify the legal status, confirm the true running costs, and give you a straight assessment before you commit.")
    return {
        "id": rec["id"], "file": rec["file"], "tag": rec["tag"], "title": rec["title"],
        "loc": rec["loc"], "price": rec["price"], "price_num": rec.get("price_num", 0),
        "type": rec["type"], "region": rec["region"],
        "beds": rec["beds"], "baths": rec["baths"], "area": rec["area"], "pool": rec.get("pool", "-"),
        "plot": rec.get("plot", ""), "cover": rec.get("cover", "01.webp"), "photos": rec.get("img_count", 8),
        "short": (rec.get("short") or rec["title"]).strip(),
        "desc": paras, "features": feats[:6],
    }

import json as _json
_listings_path = os.path.join(ROOT, "listings.json")
if os.path.exists(_listings_path):
    for _rec in _json.load(open(_listings_path, encoding="utf-8")):
        PROPERTIES.append(_convert_listing(_rec))

# ============================================================================
#  LIVE LISTINGS FROM THE SOOPREMA CRM
#  When data/sooprema-listings.json exists (written by tools/sooprema_fetch.py),
#  it becomes the single source of truth for every property on the site.
#  Only public fields are present (the fetcher's allowlist strips internal data).
# ============================================================================
import re as _re, html as _html

def _esc(s):
    return _html.escape(str(s or ""), quote=False)

def _slugify(s):
    s = _re.sub(r"[^a-zA-Z0-9]+", "-", _html.unescape(s or "")).strip("-").lower()
    return (_re.sub(r"-+", "-", s) or "listing")[:80]

def _img_url(node):
    """Pull a usable image URL from a Sooprema image node like {'special':{...}} / {'source':{...}}."""
    if isinstance(node, dict):
        for fmt in ("special", "single", "source", "listing", "thumb"):
            v = node.get(fmt)
            if isinstance(v, dict) and v.get("url"):
                return v["url"]
        for v in node.values():
            if isinstance(v, dict) and v.get("url"):
                return v["url"]
    return ""

def _html_to_paras(raw):
    """Sooprema descriptions are light HTML -> clean list of paragraph strings."""
    if not raw:
        return []
    txt = _re.sub(r"(?i)</p\s*>|<br\s*/?>|</h[1-6]\s*>", "\n", _html.unescape(raw))
    txt = _re.sub(r"(?i)<li[^>]*>", "\n- ", txt)
    txt = _html.unescape(_re.sub(r"<[^>]+>", "", txt))
    return [p.strip() for p in _re.split(r"\n\s*\n|\n", txt) if p.strip()]

_EQUIP_LABELS = {
    "garage": "Garage", "parking": "Parking", "pool": "Pool", "heating": "Heating", "elevator": "Lift",
    "storage-room": "Storage room", "furnished": "Furnished", "unfurnished": "Unfurnished",
    "fireplace": "Fireplace", "alarm-system": "Alarm system", "internet": "Internet",
    "double-glazing": "Double glazing", "security-door": "Security door", "barbecue": "Barbecue",
    "summer-kitchen": "Summer kitchen", "open-terrace": "Open terrace", "covered-terrace": "Covered terrace",
    "enclosed-plot": "Enclosed plot", "laundry-room": "Laundry room", "outdoor-shower": "Outdoor shower",
    "sat-tv": "Satellite TV", "telephone": "Telephone", "water-deposit": "Water deposit",
}
_LABEL_TEXT = {
    "new-build": "New build", "brand-new": "Brand new", "under-construction": "Under construction",
    "reduced": "Price reduced", "reserved": "Reserved", "sold": "Sold", "offer": "Offer",
    "negotiable": "Negotiable", "exclusive": "Exclusive", "new-property": "New listing",
    "bank-property": "Bank property", "zero-commission": "Zero commission", "project": "Project",
}

def _money(n):
    try:
        return "€{:,}".format(int(round(float(n))))
    except (TypeError, ValueError):
        return ""

def _sqm(v):
    try:
        f = float(v)
        return "%d m²" % int(round(f)) if f > 0 else ""
    except (TypeError, ValueError):
        return ""

def _int(v):
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return 0

_ES_SMALL = {"de", "del", "la", "las", "el", "los", "y", "e", "en", "a", "i"}
def _titlecase_es(s):
    """Tidy casing only when a place name is all-lower or all-upper (leave proper mixed-case alone)."""
    s = (s or "").strip()
    if not s or not (s.islower() or s.isupper()):
        return s
    words = s.lower().split()
    return " ".join(w if (i and w in _ES_SMALL) else (w[:1].upper() + w[1:]) for i, w in enumerate(words))

def _extract_specs(text):
    """Best-effort: recover bed/bath/build/plot numbers from an English description when the CRM field is blank."""
    t = _re.sub(r"<[^>]+>", " ", _html.unescape(text or "")).lower()
    def grab(pats, lo, hi):
        for p in pats:
            m = _re.search(p, t)
            if m:
                try:
                    n = int(float(m.group(1).replace(",", ".")))
                    if lo <= n <= hi:
                        return n
                except ValueError:
                    pass
        return 0
    return {
        "beds": grab([r"(\d+)\s*(?:bed(?:room)?s?|dormitor)"], 1, 20),
        "baths": grab([r"(\d+)\s*(?:bath(?:room)?s?|ba[nñ]o)"], 1, 15),
        "build": grab([r"(\d+(?:[.,]\d+)?)\s*m[²2]\s*(?:built|of\s+build|construct)",
                       r"built[^.]{0,30}?(\d+(?:[.,]\d+)?)\s*m[²2]"], 20, 5000),
        "plot": grab([r"(\d+(?:[.,]\d+)?)\s*m[²2]\s*(?:plot|of\s+plot|parcel|land)",
                      r"plot[^.]{0,30}?(\d+(?:[.,]\d+)?)\s*m[²2]"], 30, 200000),
    }

_STATUS_CLASS = {
    "Reserved": "reserved", "Sold": "sold", "New build": "new", "Brand new": "new",
    "New listing": "new", "Under construction": "new", "Price reduced": "reduced", "Exclusive": "exclusive",
}

def _map_listing(it):
    ref = str(it.get("salesReference") or it.get("id") or "").strip()
    city = _esc(_titlecase_es((it.get("cityName") or "").strip()))
    area = _esc(_titlecase_es((it.get("areaName") or "").strip()))
    loc = ", ".join([x for x in dict.fromkeys([area, city]) if x]) or "Costa Blanca"
    typ = _esc((it.get("typeName") or "Property").strip())
    raw_title = _re.sub(r"\s+", " ", _html.unescape(it.get("salesTitle") or "")).strip().replace('"', "”")
    # A handful of CRM listings have no English title yet - generate a clean English one from the facts.
    title = _esc(raw_title) if raw_title else (f"{typ} for sale in {city}" if city else f"{typ} for sale on the Costa Blanca")
    slug = it.get("salesSlug") or (_slugify(raw_title or title) + (("-" + ref) if ref else ""))
    price_num = int(float(it.get("salesPrice") or 0))
    no_price = str(it.get("salesNoPrice") or "0") == "1"
    price = "Price on request" if (no_price or not price_num) else _money(price_num)
    label = (it.get("salesLabel") or "").strip()
    tag = _LABEL_TEXT.get(label) or ("New build" if it.get("salesType") == "new-build" else "For sale")
    tagcls = _STATUS_CLASS.get(tag, "")
    ex = _extract_specs(it.get("salesDescription"))
    beds = _int(it.get("bedrooms")) or ex["beds"]
    baths = _int(it.get("bathrooms")) or ex["baths"]
    area_str = _sqm(_int(it.get("buildSize")) or ex["build"])
    plot_str = _sqm(_int(it.get("plotSize")) or ex["plot"])
    gallery = [u for u in (_img_url(n) for n in (it.get("images") or [])) if u]
    cover = _img_url(it.get("image")) or (gallery[0] if gallery else "")
    if cover and cover not in gallery:
        gallery = [cover] + gallery
    paras = [_esc(p) for p in _html_to_paras(it.get("salesDescription"))]
    if not paras:
        bedtxt = f"{it.get('bedrooms')}-bedroom " if it.get("bedrooms") else ""
        paras = [_esc(f"A {bedtxt}{(it.get('typeName') or 'property').lower()} for sale in "
                      f"{it.get('cityName') or 'the Costa Blanca North'}. Contact Nicolas for the full "
                      f"details, documentation and a viewing.")]
    summary = _re.sub(r"\s+", " ", _html.unescape(it.get("salesSummary") or "")).strip()
    summary = _esc(summary) if summary else paras[0]
    summary = summary[:200]
    equip = [e.strip() for e in (it.get("equipment") or "").split(",") if e.strip()]
    pool = _esc((it.get("poolName") or "").strip()) or ("Private pool" if "pool" in equip else "")
    energy = str(it.get("energyCertificate") or "0").strip()
    energy = energy if energy in list("ABCDEFG") else ""
    feats = []  # real amenities only - sizes live in the spec box, not here
    if _int(it.get("buildYear")): feats.append("Built in %s" % _esc(it["buildYear"]))
    if _int(it.get("renovationYear")): feats.append("Renovated in %s" % _esc(it["renovationYear"]))
    for e in equip:
        lab = _EQUIP_LABELS.get(e)
        if lab and lab not in feats:
            feats.append(lab)
    if energy: feats.append("Energy rating %s" % energy)
    lat = lng = ""
    if it.get("latlng") and "," in str(it["latlng"]):
        lat, lng = [x.strip() for x in str(it["latlng"]).split(",")[:2]]
    rank = sum(1 for k in ("salesHome", "salesFeatured", "salesFirstPosition") if str(it.get(k) or "0") == "1")
    return {
        "id": str(it.get("id") or ref), "ref": ref, "file": "property-%s.html" % _slugify(slug),
        "tag": tag, "tagcls": tagcls,
        "title": title, "loc": loc, "region": city or "Costa Blanca",
        "type": _esc((it.get("typeName") or "Property").strip()),
        "price": price, "price_num": price_num,
        "beds": beds, "baths": baths,
        "area": area_str, "plot": plot_str,
        "pool": pool, "energy": energy, "cover": cover, "gallery": gallery, "photos": len(gallery),
        "lat": lat, "lng": lng, "video": (it.get("video") or "").strip(), "tour360": (it.get("tour360") or "").strip(),
        "short": summary, "desc": paras or [summary], "features": feats[:8], "_rank": rank,
    }

_sooprema_path = os.path.join(ROOT, "data", "sooprema-listings.json")
if os.path.exists(_sooprema_path):
    _live, _seen = [], set()
    for _it in _json.load(open(_sooprema_path, encoding="utf-8")).get("items", []):
        _m = _map_listing(_it)
        _f, _i = _m["file"], 2
        while _f in _seen:
            _f = _m["file"][:-5] + "-%d.html" % _i; _i += 1
        _m["file"] = _f; _seen.add(_f)
        _live.append(_m)
    if _live:
        _live.sort(key=lambda p: (-p["_rank"], -(int(p["id"]) if p["id"].isdigit() else 0)))
        PROPERTIES = _live
        FEATURED = PROPERTIES[:3]
        print("Loaded %d live listings from the Sooprema CRM." % len(PROPERTIES))

PLACEHOLDER_IMG = "assets/images/hero/villa-wide.webp"

def prop_by_id(pid):
    return next(p for p in PROPERTIES if p["id"] == pid)

def _meta_spans(p, sw="1.5"):
    """beds / baths / size spans, skipping anything the listing doesn't have (no '0 bed', no '-')."""
    out = []
    if p.get("beds"): out.append(f"<span>{icon(I_BED, sw)} {p['beds']} bed</span>")
    if p.get("baths"): out.append(f"<span>{icon(I_BATH, sw)} {p['baths']} bath</span>")
    if p.get("area"): out.append(f"<span>{icon(I_AREA, sw)} {p['area']}</span>")
    elif p.get("plot"): out.append(f"<span>{icon(I_AREA, sw)} {p['plot']} plot</span>")
    return "".join(out)

def _tag_span(p, cls="prop-card__tag"):
    mod = f" {cls}--{p['tagcls']}" if p.get("tagcls") else ""
    return f'<span class="{cls}{mod}">{p["tag"]}</span>'

def prop_card(p, idx=0):
    img = p.get("cover") or PLACEHOLDER_IMG
    return f'''<a class="prop-card reveal" href="{p['file']}"
        data-type="{p.get('type','')}" data-region="{p.get('region','')}"
        data-beds="{p['beds']}" data-price="{p.get('price_num',0)}" data-order="{idx}">
        <div class="prop-card__media">
          <img src="{img}" alt="{p['title']}" loading="lazy" width="600" height="400" />
          {_tag_span(p)}
        </div>
        <div class="prop-card__body">
          <span class="prop-card__loc">{p['loc']}</span>
          <h3>{p['title']}</h3>
          <div class="prop-card__price">{p['price']}</div>
          <div class="prop-card__meta">{_meta_spans(p)}</div>
        </div>
      </a>'''

I_PIN = '<path d="M12 21s-7-6-7-11a7 7 0 0 1 14 0c0 5-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>'

def listing_card(p, badge=None):
    """Full-width cinematic listing card - name over the image (Vellaro-style)."""
    img = p.get("cover") or PLACEHOLDER_IMG
    badge = badge or p.get("tag", "For sale")
    return f'''<article class="listing reveal">
        <a class="listing__media" href="{p['file']}" aria-label="View {p['title']}">
          <img src="{img}" alt="{p['title']}" loading="lazy" width="1200" height="675" />
        </a>
        <div class="listing__overlay">
          <div class="listing__row listing__row--top">
            <span class="listing__loc">{icon(I_PIN,'1.6')} {p['loc']}</span>
            <span class="listing__badge">{badge}</span>
          </div>
          <div class="listing__mid">
            <h3 class="listing__name">{p['title']}</h3>
            <p class="listing__desc">{p['short']}</p>
            <div class="listing__specs">{_meta_spans(p, '1.6')}</div>
          </div>
          <div class="listing__row listing__row--bottom">
            <span class="listing__price">{p['price']}</span>
            <a class="btn btn--on-dark listing__btn" href="{p['file']}">View property</a>
          </div>
        </div>
      </article>'''


# ===========================================================================
#  PAGE BODIES
# ===========================================================================

def section_stats(navy=True):
    cls = "section section--navy" if navy else "section section--alt"
    return f'''    <section class="{cls}">
      <div class="container">
        <div class="stats">
          <div class="stat reveal"><span class="stat__num" data-count="25" data-suffix="+">25+</span><span class="stat__label">Years on the Costa Blanca</span></div>
          <div class="stat reveal" data-delay="1"><span class="stat__num" data-count="500" data-suffix="+">500+</span><span class="stat__label">Properties sold</span></div>
          <div class="stat reveal" data-delay="2"><span class="stat__num" data-count="50" data-suffix="+">50+</span><span class="stat__label">Build &amp; renovation projects</span></div>
          <div class="stat reveal" data-delay="3"><span class="stat__num" data-count="5">5</span><span class="stat__label">Languages spoken</span></div>
        </div>
      </div>
    </section>'''

def cta_band(heading="Let's talk - quietly and without obligation.",
             text="Tell me what you're looking for. I'll give you an honest view, whether or not it ends in a purchase."):
    return f'''    <section class="section section--navy">
      <div class="container cta-band">
        <p class="eyebrow" style="color:var(--accent-soft)">Your next step</p>
        <p class="display">{heading}</p>
        <p>{text}</p>
        <div class="btn-row">
          <a class="btn btn--on-dark" href="{WA_DEFAULT}" target="_blank" rel="noopener">{WA_ICON}Message Nicolas</a>
          <a class="btn btn--ghost" style="color:#fff;border-color:rgba(255,255,255,0.35)" href="contact.html">Request a consultation</a>
        </div>
      </div>
    </section>'''

PLAY_ICON = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>'

def video_gallery(items):
    """Click-through gallery: one featured player + selectable thumbnails (JS swaps the source).
    items: list of (name, title, duration, caption, loop). The first item loads into the stage."""
    thumbs = "".join(f'''
            <button class="vgallery__thumb{' is-active' if i == 0 else ''}" type="button" role="tab" aria-selected="{'true' if i == 0 else 'false'}"
              data-src="assets/videos/{name}.mp4" data-poster="assets/videos/{name}-poster.jpg" data-loop="{1 if loop else 0}" data-caption="{caption}">
              <span class="vgallery__thumb-media"><img src="assets/videos/{name}-poster.jpg" alt="{title}" loading="lazy" width="480" height="270" /><span class="vgallery__thumb-play">{PLAY_ICON}</span></span>
              <span class="vgallery__thumb-meta"><span class="vgallery__thumb-title">{title}</span><span class="vgallery__thumb-dur">{dur}</span></span>
            </button>''' for i, (name, title, dur, caption, loop) in enumerate(items))
    first = items[0]
    return f'''<div class="vgallery reveal" data-vgallery>
          <div class="vgallery__stage">
            <video class="vgallery__video" data-vgallery-video controls playsinline autoplay muted loop preload="metadata" poster="assets/videos/{first[0]}-poster.jpg" width="1280" height="720">
              <source src="assets/videos/{first[0]}.mp4" type="video/mp4" />
            </video>
          </div>
          <p class="vgallery__caption" data-vgallery-caption>{first[3]}</p>
          <div class="vgallery__thumbs" role="tablist" aria-label="Project videos">{thumbs}</div>
        </div>'''

# ---- Shared homepage sections (reused by the live home + the alt mockup) ----
def home_featured():
    return f'''    <section class="section section--alt">
      <div class="container">
        <div class="section-head reveal" style="display:flex;justify-content:space-between;align-items:end;gap:2rem;flex-wrap:wrap;max-width:none;">
          <div>
            <p class="eyebrow">A curated few</p>
            <h2 class="mb-0">Featured properties</h2>
          </div>
          <a class="text-cta" href="properties.html">See all properties {ARROW}</a>
        </div>
        <div class="listings" style="margin-top:2.5rem;">
          {"".join(listing_card(p) for p in FEATURED)}
        </div>
      </div>
    </section>'''

def home_trust():
    return f'''    <section class="section section--alt">
      <div class="container">
        <div class="section-head reveal"><p class="eyebrow">Why clients trust Nicolas</p><h2 class="mb-0">Honest, every time.</h2></div>
        <div class="features" style="margin-top:2.5rem;">
          <div class="feature reveal">
            <svg class="feature__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M12 3l8 4v5c0 5-3.5 8-8 9-4.5-1-8-4-8-9V7l8-4Z"/><path d="M9 12l2 2 4-4"/></svg>
            <h3>Your interests first</h3>
            <p>A handful of clients at a time - real attention and a straight opinion.</p>
          </div>
          <div class="feature reveal" data-delay="1">
            <svg class="feature__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M3 12h4l3 8 4-16 3 8h4"/></svg>
            <h3>I'll tell you not to buy</h3>
            <p>If something's wrong, you'll hear it - even if it costs me the deal.</p>
          </div>
          <div class="feature reveal" data-delay="2">
            <svg class="feature__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>
            <h3>25 years, tested</h3>
            <p>Lawyers, architects and craftsmen proven over decades on this coast.</p>
          </div>
        </div>
      </div>
    </section>'''

def home_about():
    return f'''    <section class="section">
      <div class="container">
        <div class="split">
          <div class="split__media reveal"><img src="assets/images/nicolas/portrait-warm.jpg" alt="Nicolas Strebel, independent real estate and home-projects advisor on the Costa Blanca" loading="lazy" width="800" height="1000" style="object-position: top center;" /></div>
          <div class="split__body reveal" data-delay="1">
            <p class="eyebrow">Who you'll work with</p>
            <h2>Meet Nicolas</h2>
            <p class="text-muted">A designer by training - Fashion Design at Istituto Marangoni in Milan, then a high-fashion design team in Düsseldorf - Nicolas brought an eye for proportion, material and detail to the Costa Blanca in 1998. He co-founded one of the area's respected agencies, and over twenty-five years sold 500+ properties and delivered 50+ building and renovation projects before going fully independent in 2024. Today he takes on only a few clients at a time, coordinating a trusted network of architects, builders and specialists - one straight opinion and one steady hand from the first viewing to the finished home.</p>
            {ticklist(["Swiss, based in Teulada", "Fashion Design - Istituto Marangoni, Milan", "25 years in Costa Blanca property &amp; building projects", "Independent since 2024 - tied to no single builder", "Five languages: DE · ES · EN · FR · IT"])}
            <a class="btn btn--ghost" href="about.html" style="margin-top:0.5rem;">More about Nicolas {ARROW}</a>
          </div>
        </div>
      </div>
    </section>'''

def home_differentiator():
    steps = [
        ("01", "Find &amp; buy", "Whole-market search, an honest valuation, legal and structural due diligence, and the negotiation - done on your side, not the seller's."),
        ("02", "Build or renovate", "A trusted network of architects, builders and craftsmen - and 50+ projects coordinated end to end: permits, quality control and one point of responsibility, me."),
        ("03", "Finish &amp; furnish", "Interiors, furniture and the last details, shaped by a designer's eye - handed over ready to live in, not just ready to sign."),
    ]
    items = "".join(f'''<div class="chain__step reveal" data-delay="{i}">
            <span class="chain__n">{n}</span>
            <h3>{t}</h3>
            <p>{d}</p>
          </div>''' for i, (n, t, d) in enumerate(steps))
    return f'''    <section class="section section--navy diff-sec">
      <div class="container">
        <div class="section-head reveal" style="max-width:none;">
          <p class="eyebrow" style="color:var(--accent-soft)">Why Nicolas, not an agency</p>
          <h2 style="color:#fff;max-width:18ch;">Most agents stop at the keys. I don't.</h2>
          <p style="color:rgba(255,255,255,0.84);max-width:66ch;">An estate agent finds a property and hands you the keys. I find it, check its legal and structural reality, and negotiate it - then coordinate the trusted architects, builders and craftsmen who renovate or build it, and furnish it with an eye trained in design. Independent, tied to no single builder - one accountable person, from the first viewing to the finished home.</p>
        </div>
        <div class="chain">{items}</div>
        <div class="btn-row reveal" style="margin-top:2.75rem;">
          <a class="btn btn--on-dark" href="home-projects.html">See how I build &amp; renovate {ARROW}</a>
        </div>
      </div>
    </section>'''

def home_testimonials():
    return f'''    <section class="section section--alt">
      <div class="container">
        <div class="section-head text-center reveal">
          <p class="eyebrow">In their words</p>
          <h2>Buyers who wanted someone on their side</h2>
        </div>
        <div class="quote-grid">
          <figure class="quote reveal">
            <div class="quote__mark">&ldquo;</div>
            <p>He talked us out of the first villa we loved. The survey later proved him completely right. That's when we knew we'd chosen the correct person.</p>
            <figcaption class="quote__who"><strong>M. &amp; A. Bauer</strong><span>Zurich, Switzerland</span></figcaption>
          </figure>
          <figure class="quote reveal" data-delay="1">
            <div class="quote__mark">&ldquo;</div>
            <p>Everything in one pair of hands - the lawyer, the bank, the renovation. In a foreign country that peace of mind is worth more than any commission.</p>
            <figcaption class="quote__who"><strong>P. van der Berg</strong><span>Utrecht, Netherlands</span></figcaption>
          </figure>
          <figure class="quote reveal" data-delay="2">
            <div class="quote__mark">&ldquo;</div>
            <p>Calm, precise and honest. Nicolas negotiated a price we wouldn't have reached alone and never once pushed us. A genuine advisor.</p>
            <figcaption class="quote__who"><strong>Dr. R. Schmidt</strong><span>Munich, Germany</span></figcaption>
          </figure>
        </div>
        <p class="text-center text-muted" style="margin-top:1.5rem;font-size:0.85rem;">Representative client experiences, shared with permission. Full references available on request.</p>
      </div>
    </section>'''


# ---------------------------------------------------------------- HOME
def body_home():
    def ticks(items):
        lis = "".join(f'<li>{icon(I_CHECK, "2")}<span>{t}</span></li>' for t in items)
        return f'<ul class="tick-list">{lis}</ul>'

    def spine_li(items):
        return "".join(f'<li>{icon(I_CHECK, "2")}<span>{t}</span></li>' for t in items)
    spine = f'''    <section class="section spine-sec" id="divisions">
      <div class="container">
        <div class="section-head text-center reveal" style="margin-inline:auto;">
          <p class="eyebrow">One advisor · two divisions</p>
          <h2 class="mb-0">Everything your property and your project need</h2>
        </div>
        <div class="spine">
          <div class="spine__col spine__col--re reveal">
            <div class="spine__head"><span class="spine__tag">Real Estate</span><a class="text-cta" href="real-estate.html">Explore {ARROW}</a></div>
            <ul class="spine__list">{spine_li(["Buying - whole-market search and honest advice", "Selling - valuation, presentation and the right buyers", "Property sourcing - including off-market", "Investing - true costs, real yields, a straight yes or no"])}</ul>
          </div>
          <div class="spine__col spine__col--hp reveal" data-delay="1">
            <div class="spine__head"><span class="spine__tag">Home Projects</span><a class="text-cta" href="home-projects.html">Explore {ARROW}</a></div>
            <ul class="spine__list spine__list--sand">{spine_li(["New-build villas - plot to finished home", "Renovation &amp; refurbishment", "Interior design", "Furniture projects", "Project coordination - one hand on the whole build"])}</ul>
          </div>
        </div>
      </div>
    </section>'''

    hero = f'''    <section class="hero hero--split">
      <div class="hero__media" data-parallax><img src="assets/images/hero/home-hero.webp?v={VERSION}" alt="Sunset over the Costa Blanca from a villa terrace" fetchpriority="high" width="1600" height="1066" /></div>
      <div class="hero__inner">
        <div class="container">
          <p class="eyebrow hero__eyebrow reveal">Independent advisor · Real estate &amp; home projects · Costa Blanca North</p>
          <h1 class="display hero__title reveal" data-delay="1">Your property and your project,<br />under one roof.</h1>
          <p class="hero__sub reveal" data-delay="2">One independent advisor across buying, selling, building, renovating and investing on the Costa Blanca - one accountable person, tied to no single agency or builder.</p>
          <div class="hero__doors reveal" data-delay="3">
            <a class="hero-door hero-door--re" href="real-estate.html">
              <span class="hero-door__k">Division 01</span>
              <span class="hero-door__name">Real Estate</span>
              <span class="hero-door__svc">Buying · Selling · Sourcing · Investing</span>
              <span class="hero-door__cta">Let's find it together {ARROW}</span>
            </a>
            <a class="hero-door hero-door--hp" href="home-projects.html">
              <span class="hero-door__k">Division 02</span>
              <span class="hero-door__name">Home Projects</span>
              <span class="hero-door__svc">New-build · Renovation · Interiors · Furniture · Coordination</span>
              <span class="hero-door__cta">Let's build it together {ARROW}</span>
            </a>
          </div>
          <div class="hero__advisor-strip reveal" data-delay="4">
            <img class="hero__advisor-av" src="assets/images/nicolas/advisor-head.jpg" alt="Nicolas Strebel" loading="lazy" width="76" height="76" />
            <span><strong>Your advisor - Nicolas Strebel.</strong> Swiss, independent, 25 years on this coast - the same eye that finds your home shapes how it's built and finished. <a href="about.html">More about Nicolas {ARROW}</a></span>
          </div>
        </div>
      </div>
      <div class="hero__stats reveal" data-delay="4">
        <div class="container hero__stats-inner">
          <div class="hstat"><strong data-count="25" data-suffix="+">25+</strong><span>Years on the Costa Blanca</span></div>
          <div class="hstat"><strong data-count="500" data-suffix="+">500+</strong><span>Properties sold</span></div>
          <div class="hstat"><strong data-count="50" data-suffix="+">50+</strong><span>Build &amp; renovation projects</span></div>
          <div class="hstat"><strong data-count="5">5</strong><span>Languages spoken</span></div>
        </div>
      </div>
    </section>'''

    return hero + spine + home_differentiator() + home_featured() + home_trust() + home_about() + cta_band("Your property or your project? Let's talk.", "Book a free, no-obligation consultation. You'll get an honest, straight view either way, whether or not it ends in a deal.")


# ------------------------------------------------- HOME (ALT CONCEPT · MOCKUP)
# A standalone alternate homepage that leads with the question itself -
# "Which path is right for you?" - turned into three large, scannable image
# buttons. Same look & feel, different hero concept. Mockup only (index-alt.html).
HOME_ALT_CSS = '''  <style>
    .ha-hero { padding: clamp(2.25rem, 1.5rem + 3vw, 4rem) 0 var(--section-y);
      background: radial-gradient(125% 90% at 50% -25%, #ffffff 0%, var(--stone) 50%, var(--stone-2) 100%); }
    .ha-hero__head { text-align: center; max-width: 62rem; margin-inline: auto; }
    .ha-hero__head h1 { margin: 0.4rem 0 0; }
    .ha-hero__sub { color: var(--muted); font-size: var(--fs-lead); max-width: 56ch; margin: 1.15rem auto 0; }
    .ha-paths { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.25rem;
      margin-top: clamp(2.25rem, 1.5rem + 2.5vw, 3.5rem); }
    .ha-path { position: relative; min-height: clamp(22rem, 17rem + 14vw, 32rem);
      border-radius: var(--radius-lg); overflow: hidden; display: flex; align-items: flex-end;
      text-decoration: none; isolation: isolate; box-shadow: var(--shadow);
      transition: transform .55s cubic-bezier(.2,.7,.2,1), box-shadow .55s cubic-bezier(.2,.7,.2,1); }
    .ha-path img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover;
      z-index: -2; transition: transform .9s cubic-bezier(.2,.7,.2,1); }
    .ha-path::after { content: ""; position: absolute; inset: 0; z-index: -1;
      background: linear-gradient(180deg, rgba(34,50,63,0) 26%, rgba(20,29,37,.55) 60%, rgba(15,23,30,.92) 100%); }
    .ha-path:hover { transform: translateY(-7px); box-shadow: var(--shadow-lg); }
    .ha-path:hover img { transform: scale(1.07); }
    .ha-path:focus-visible { outline: 3px solid var(--accent); outline-offset: 3px; }
    .ha-path__body { padding: clamp(1.4rem, 1rem + 1.5vw, 2rem); color: #fff; }
    .ha-path__n { font-family: var(--font-sans); font-size: .72rem; letter-spacing: .22em;
      text-transform: uppercase; color: rgba(255,255,255,.78); }
    .ha-path h2 { color: #fff; font-size: clamp(1.7rem, 1.3rem + 1.4vw, 2.3rem); line-height: 1.04;
      margin: .35rem 0 .55rem; }
    .ha-path p { color: rgba(255,255,255,.85); font-size: var(--fs-small); line-height: 1.5;
      margin: 0 0 1.1rem; max-width: 32ch; }
    .ha-path__cta { display: inline-flex; align-items: center; gap: .4rem; font-family: var(--font-sans);
      font-weight: 600; font-size: .92rem; color: #fff; }
    .ha-path__cta .icon { width: 1.15rem; height: 1.15rem; transition: transform .35s ease; }
    .ha-path:hover .ha-path__cta .icon { transform: translateX(5px); }
    .ha-hero__foot { display: flex; align-items: center; justify-content: space-between;
      gap: 1.5rem 2.5rem; flex-wrap: wrap; margin-top: clamp(2.25rem, 1.5rem + 2.5vw, 3.25rem);
      padding-top: clamp(1.75rem, 1.25rem + 2vw, 2.5rem); border-top: 1px solid var(--line); }
    .ha-trust { display: flex; gap: clamp(1.5rem, 1rem + 2vw, 3rem); flex-wrap: wrap; }
    .ha-trust div { display: flex; flex-direction: column; }
    .ha-trust strong { font-family: var(--font-serif); font-weight: 600; font-size: 1.85rem;
      line-height: 1; color: var(--navy); }
    .ha-trust span { font-size: .8rem; color: var(--muted); margin-top: .25rem; }
    @media (max-width: 860px) {
      .ha-paths { grid-template-columns: 1fr; }
      .ha-path { min-height: 17rem; }
      .ha-hero__foot { justify-content: center; text-align: center; }
      .ha-trust { justify-content: center; }
      .ha-trust div { align-items: center; }
    }
  </style>'''

def body_home_alt():
    paths = [
        ("01", "Buy or sell", "Whole-market search, an honest valuation, negotiation and legals - on your side, whichever way you're moving.", "buyers-advisor.html", "assets/images/properties/calpe-villa-newbuild/05.webp"),
        ("02", "Build or renovate", "New builds and renovations coordinated end to end - permits, craftsmen, interiors - all in one pair of hands.", "home-projects.html", "assets/images/construction/onsite-nicolas.jpg"),
        ("03", "Invest", "A sober read on the numbers - true all-in cost, real yields, and a straight yes or no before you commit.", "investing.html", "assets/images/hero/area-calpe.webp"),
    ]
    cards = "".join(f'''
          <a class="ha-path reveal" data-delay="{i}" href="{href}">
            <img src="{img}" alt="{label} on the Costa Blanca" loading="eager" width="800" height="1000" />
            <div class="ha-path__body">
              <span class="ha-path__n">{n}</span>
              <h2>{label}</h2>
              <p>{desc}</p>
              <span class="ha-path__cta">Explore {ARROW}</span>
            </div>
          </a>''' for i, (n, label, desc, href, img) in enumerate(paths))

    hero = f'''    <section class="ha-hero">
      <div class="container">
        <div class="ha-hero__head">
          <p class="eyebrow reveal">Real estate · Construction · Investment · Costa Blanca Norte</p>
          <h1 class="display reveal" data-delay="1">Which path is right for you?</h1>
          <p class="ha-hero__sub reveal" data-delay="2">Tell me your goal - buying, selling, building or investing - and I'll handle the rest. One honest point of contact, with 25 years on this coast.</p>
        </div>
        <div class="ha-paths">{cards}</div>
        <div class="ha-hero__foot reveal" data-delay="3">
          <div class="ha-trust">
            <div><strong data-count="25" data-suffix="+">25+</strong><span>Years on this coast</span></div>
            <div><strong data-count="500" data-suffix="+">500+</strong><span>Properties sold</span></div>
            <div><strong data-count="50" data-suffix="+">50+</strong><span>Build &amp; renovation projects</span></div>
            <div><strong data-count="5">5</strong><span>Languages spoken</span></div>
          </div>
          <a class="btn btn--primary" href="{WA_DEFAULT}" target="_blank" rel="noopener">{WA_ICON}Not sure yet? Just ask</a>
        </div>
      </div>
    </section>'''

    return hero + home_featured() + home_trust() + home_about() + home_testimonials() + cta_band()


# ----------------------------------------------- HOME (CONCEPT 3 · MOCKUP)
# Cinematic full-bleed hero on the main draft's sunset banner image, with a
# luxury-style "service rail" of big buttons across the bottom. The breadth
# (more than an estate agent) is implied by the headline triad, never stated.
# Mockup only (index-alt2.html); the live home stays index.html.
HOME_V3_CSS = '''  <style>
    .hc-hero { position: relative; min-height: clamp(600px, 92vh, 900px); display: flex;
      align-items: flex-end; overflow: hidden; isolation: isolate; }
    .hc-hero__bg { position: absolute; inset: 0; z-index: -2; }
    .hc-hero__bg img { width: 100%; height: 100%; object-fit: cover; }
    .hc-hero__scrim { position: absolute; inset: 0; z-index: -1;
      background:
        linear-gradient(95deg, rgba(13,20,26,.74) 0%, rgba(13,20,26,.40) 40%, rgba(13,20,26,.05) 72%),
        linear-gradient(180deg, rgba(13,20,26,0) 45%, rgba(11,17,22,.88) 100%); }
    .hc-hero__inner { width: 100%; padding-top: clamp(3rem, 2rem + 5vw, 6rem);
      padding-bottom: clamp(1.5rem, 1rem + 2vw, 2.75rem); }
    .hc-copy { max-width: 44rem; color: #fff; }
    .hc-copy .eyebrow { color: var(--accent-soft); }
    .hc-copy h1 { color: #fff; margin: .5rem 0 0; text-wrap: balance; }
    .hc-sub { color: rgba(255,255,255,.9); font-size: var(--fs-lead); max-width: 50ch;
      margin: 1.1rem 0 1.75rem; }
    .hc-rail { display: grid; grid-template-columns: repeat(3, 1fr); margin-top: clamp(2rem, 1.5rem + 3vw, 3.5rem);
      border: 1px solid rgba(255,255,255,.18); border-radius: var(--radius-lg); overflow: hidden;
      background: rgba(13,20,26,.34); backdrop-filter: blur(7px); -webkit-backdrop-filter: blur(7px); }
    .hc-seg { display: flex; align-items: center; justify-content: space-between; gap: 1rem;
      padding: clamp(1.1rem, .9rem + 1vw, 1.6rem) clamp(1.25rem, 1rem + 1vw, 1.9rem);
      text-decoration: none; color: #fff; border-left: 1px solid rgba(255,255,255,.16);
      transition: background .4s cubic-bezier(.2,.7,.2,1); }
    .hc-seg:first-child { border-left: 0; }
    .hc-seg:hover { background: rgba(255,255,255,.10); }
    .hc-seg:focus-visible { outline: 3px solid var(--accent-soft); outline-offset: -3px; }
    .hc-seg__txt { display: flex; flex-direction: column; gap: .15rem; }
    .hc-seg__n { font-family: var(--font-sans); font-size: .7rem; letter-spacing: .22em;
      text-transform: uppercase; color: rgba(255,255,255,.62); }
    .hc-seg__label { font-family: var(--font-serif); font-weight: 600; font-size: clamp(1.3rem, 1.1rem + .8vw, 1.7rem);
      line-height: 1.05; }
    .hc-seg .icon { width: 1.25rem; height: 1.25rem; flex: none; transition: transform .35s ease; }
    .hc-seg:hover .icon { transform: translateX(5px); }
    @media (max-width: 820px) {
      .hc-hero { min-height: 0; }
      .hc-hero__scrim { background:
        linear-gradient(180deg, rgba(13,20,26,.55) 0%, rgba(13,20,26,.35) 35%, rgba(11,17,22,.9) 100%); }
      .hc-rail { grid-template-columns: 1fr; }
      .hc-seg { border-left: 0; border-top: 1px solid rgba(255,255,255,.16); }
      .hc-seg:first-child { border-top: 0; }
    }
  </style>'''

def body_home_v3():
    rail = [
        ("01", "Buying &amp; selling", "buyers-advisor.html"),
        ("02", "Building &amp; renovating", "home-projects.html"),
        ("03", "Investing", "investing.html"),
    ]
    segs = "".join(f'''
            <a class="hc-seg" href="{href}">
              <span class="hc-seg__txt"><span class="hc-seg__n">{n}</span><span class="hc-seg__label">{label}</span></span>
              {ARROW}
            </a>''' for n, label, href in rail)

    hero = f'''    <section class="hc-hero">
      <div class="hc-hero__bg"><img src="assets/images/hero/home-hero.webp?v={VERSION}" alt="Sunset over the Costa Blanca from a villa terrace" fetchpriority="high" width="1600" height="1066" /></div>
      <div class="hc-hero__scrim"></div>
      <div class="container hc-hero__inner">
        <div class="hc-copy">
          <p class="eyebrow reveal">Real estate · Construction · Investment · Costa Blanca Norte</p>
          <h1 class="display reveal" data-delay="1">Found, built,<br />and looked after.</h1>
          <p class="hc-sub reveal" data-delay="2">A single trusted partner for buying, selling, building, renovating and investing on the Costa Blanca - with 25 years on this coast.</p>
          <div class="reveal" data-delay="3">
            <a class="btn btn--on-dark" href="{WA_DEFAULT}" target="_blank" rel="noopener">{WA_ICON}Start a conversation</a>
          </div>
        </div>
        <div class="hc-rail reveal" data-delay="4">{segs}</div>
      </div>
    </section>'''

    return hero + home_featured() + section_stats(navy=False) + home_trust() + home_about() + home_testimonials() + cta_band()


# ----------------------------------------------- HOME (CONCEPT 4 · MOCKUP)
# Editorial split-frame: the sunset banner is CONTAINED as a framed image plate
# on a light stone ground, with the copy beside it (never over it) and a large
# vertical numbered service index as the big tap targets. Distinct from the
# overlay / question-grid / full-bleed-rail concepts. Mockup only (index-alt3.html).
HOME_V4_CSS = '''  <style>
    .he-hero { padding: clamp(2rem, 1.5rem + 3vw, 4rem) 0 var(--section-y);
      background: linear-gradient(180deg, #ffffff 0%, var(--stone) 100%); }
    .he-hero__grid { display: grid; grid-template-columns: 1.05fr .95fr;
      gap: clamp(2rem, 1rem + 4vw, 4.5rem); align-items: stretch; }
    .he-media { min-height: 26rem; }
    .he-copy h1 { margin: .5rem 0 0; text-wrap: balance; }
    .he-lead { color: var(--muted); font-size: var(--fs-lead); max-width: 42ch; margin: 1.1rem 0 1.9rem; }
    .he-index { display: flex; flex-direction: column; border-top: 1px solid var(--line); margin-bottom: 1.9rem; }
    .he-row { display: flex; align-items: center; gap: 1.25rem;
      padding: clamp(.85rem, .65rem + .6vw, 1.2rem) .25rem; border-bottom: 1px solid var(--line);
      text-decoration: none; color: var(--navy);
      transition: padding-left .35s cubic-bezier(.2,.7,.2,1), color .35s; }
    .he-row:hover { padding-left: .9rem; color: var(--accent-deep); }
    .he-row:focus-visible { outline: 2px solid var(--accent); outline-offset: 3px; }
    .he-row__n { font-family: var(--font-sans); font-size: .8rem; letter-spacing: .18em;
      font-weight: 600; color: var(--accent); width: 2rem; flex: none; }
    .he-row__label { font-family: var(--font-serif); font-weight: 600;
      font-size: clamp(1.4rem, 1.1rem + 1vw, 2rem); line-height: 1.05; flex: 1; }
    .he-row__arrow .icon { width: 1.3rem; height: 1.3rem; color: var(--accent); transition: transform .35s ease; }
    .he-row:hover .he-row__arrow .icon { transform: translateX(5px); }
    .he-media { position: relative; }
    .he-media__img { width: 100%; height: 100%; max-height: 40rem; object-fit: cover;
      border-radius: var(--radius-lg); box-shadow: var(--shadow-lg); display: block; }
    .he-badge { position: absolute; left: -1.25rem; bottom: 1.75rem; background: var(--white);
      border-radius: var(--radius); box-shadow: var(--shadow); padding: .9rem 1.25rem;
      display: flex; align-items: baseline; gap: .55rem; }
    .he-badge strong { font-family: var(--font-serif); font-weight: 600; font-size: 2.4rem;
      line-height: 1; color: var(--navy); }
    .he-badge span { font-size: .82rem; color: var(--muted); max-width: 9ch; line-height: 1.2; }
    @media (max-width: 880px) {
      .he-hero__grid { grid-template-columns: 1fr; }
      .he-media__img { max-height: 22rem; }
      .he-badge { left: auto; right: 1rem; bottom: 1rem; }
    }
  </style>'''

def body_home_v4():
    rows = [
        ("01", "Buying &amp; selling", "buyers-advisor.html"),
        ("02", "Building &amp; renovating", "home-projects.html"),
        ("03", "Investing", "investing.html"),
    ]
    index = "".join(f'''
            <a class="he-row" href="{href}">
              <span class="he-row__n">{n}</span>
              <span class="he-row__label">{label}</span>
              <span class="he-row__arrow">{ARROW}</span>
            </a>''' for n, label, href in rows)

    hero = f'''    <section class="he-hero">
      <div class="container he-hero__grid">
        <div class="he-copy">
          <p class="eyebrow reveal">Real estate · Construction · Investment · Costa Blanca Norte</p>
          <h1 class="display reveal" data-delay="1">From first viewing<br />to finished home.</h1>
          <p class="he-lead reveal" data-delay="2">One trusted partner to buy, sell, build, renovate and invest on the Costa Blanca - with 25 years on this coast and everything handled in one pair of hands.</p>
          <nav class="he-index reveal" data-delay="3" aria-label="What I help with">{index}</nav>
          <a class="btn btn--primary reveal" data-delay="4" href="{WA_DEFAULT}" target="_blank" rel="noopener">{WA_ICON}Start a conversation</a>
        </div>
        <div class="he-media reveal" data-delay="1">
          <img class="he-media__img" src="assets/images/hero/home-hero.webp?v={VERSION}" alt="Sunset over the Costa Blanca from a villa terrace" fetchpriority="high" width="1600" height="1066" />
          <div class="he-badge"><strong>25</strong><span>years on this coast</span></div>
        </div>
      </div>
    </section>'''

    return hero + home_featured() + home_trust() + home_about() + home_testimonials() + cta_band()


# ---------------------------------------------------------------- REAL ESTATE (division hub)
def body_real_estate():
    hero = f'''    <section class="page-hero page-hero--image">
      <div class="page-hero__media"><img src="assets/images/hero/villa-wide.webp" alt="Real estate on the Costa Blanca" width="2048" height="1536" /></div>
      <div class="page-hero__inner"><div class="container">
        <p class="breadcrumb reveal"><a href="index.html">Home</a> · Real Estate</p>
        <p class="eyebrow hero__eyebrow reveal">Division 01 · Real Estate</p>
        <h1 class="display reveal" data-delay="1">Buy, sell and invest,<br />with an advisor on your side.</h1>
        <p class="reveal" data-delay="2">Buying, selling, property sourcing and investment across the Costa Blanca North - Moraira, Benissa, Calpe, Jávea and Altea. Whole-market reach, honest valuations and a straight opinion, from one independent advisor who represents you, not the deal.</p>
      </div></div>
    </section>'''

    overview = f'''    <section class="section">
      <div class="container container--reading">
        <p class="eyebrow reveal">Division 01</p>
        <h2 class="reveal">Real estate, working for you, not the seller</h2>
        <hr class="rule-accent reveal" />
        <div class="prose reveal stack">
          <p>Most people buying abroad deal with a different agent for every property, each one pushing their own listing. I work the other way round: one independent advisor on your side of the table, across the whole market - and, when it helps, the same person who can then coordinate the build, renovation or furnishing of what you buy.</p>
        </div>
      </div>
    </section>'''

    svc = [
        ("Buying", "Whole-market search - including off-market - honest viewings, legal and structural due diligence, and negotiation on your side.", "buyers-advisor.html", "More on buying"),
        ("Selling", "An honest valuation, real presentation, and qualified buyers from a 25-year network - a clean, fast sale handled end to end.", "buyers-advisor.html#selling", "More on selling"),
        ("Property sourcing", "Give me the brief; I bring back the few that truly fit - quietly, including properties that never reach a public portal.", "buyers-advisor.html", "Discuss a search"),
        ("Investing", "True all-in cost, realistic yields, resale reality and renovation upside - a sober yes or no before you commit a euro.", "investing.html", "More on investing"),
    ]
    cards = "".join(f'''<article class="card reveal"{' data-delay="1"' if i%2 else ''}><div class="card__body"><h3>{t}</h3><p class="text-muted">{d}</p><a class="text-cta" href="{h}">{cta} {ARROW}</a></div></article>''' for i,(t,d,h,cta) in enumerate(svc))
    grid = f'''    <section class="section section--alt">
      <div class="container">
        <div class="section-head reveal"><p class="eyebrow">What I help with</p><h2 class="mb-0">Four ways I work on the property side</h2></div>
        <div class="grid grid-2" style="margin-top:2.5rem;">{cards}</div>
        <div class="text-center" style="margin-top:2.5rem;"><a class="btn btn--ghost" href="properties.html">Browse current properties {ARROW}</a></div>
      </div>
    </section>'''

    areas = f'''    <section class="section section--navy" id="areas">
      <div class="container text-center">
        <p class="eyebrow reveal" style="color:var(--accent-soft)">Where I work</p>
        <h2 class="reveal">Costa Blanca North</h2>
        <p class="reveal" style="color:rgba(255,255,255,0.82);max-width:60ch;margin-inline:auto;"><a href="buy-property-moraira.html" style="color:#fff;">Moraira</a> · <a href="buy-property-benissa.html" style="color:#fff;">Benissa</a> · Benissa Costa · <a href="buy-property-calpe.html" style="color:#fff;">Calpe</a> · <a href="buy-property-javea.html" style="color:#fff;">Jávea</a> · <a href="buy-property-altea.html" style="color:#fff;">Altea</a>. The stretch of coast I've lived and worked on for twenty-five years.</p>
      </div>
    </section>'''
    return hero + overview + grid + areas + cta_band("Buying, selling or investing on the Costa Blanca?", "Book a free, no-obligation consultation. You'll get an honest read either way.")


# ---------------------------------------------------------------- BUYER'S ADVISOR
def body_buyers():
    hero = f'''    <section class="page-hero page-hero--image">
      <div class="page-hero__media"><img src="assets/images/hero/villa-wide.webp" alt="Villa on the Costa Blanca" width="2048" height="1536" /></div>
      <div class="page-hero__inner"><div class="container">
        <p class="breadcrumb reveal"><a href="index.html">Home</a> · Buying &amp; Selling</p>
        <p class="eyebrow hero__eyebrow reveal">Your real estate advisor</p>
        <h1 class="display reveal" data-delay="1">On your side, buying or selling.</h1>
        <p class="reveal" data-delay="2">You get an advisor who works only for you - searching the whole market, valuing honestly, vetting, negotiating and handling the paperwork, start to finish.</p>
      </div></div>
    </section>'''

    explain = f'''    <section class="section">
      <div class="container container--reading">
        <p class="eyebrow reveal">The idea</p>
        <h2 class="reveal">What a buyer's advisor actually does</h2>
        <hr class="rule-accent reveal" />
        <div class="prose reveal stack">
          <p>Most people buying abroad start on the portals, contacting a different agent for every property - each one focused on closing that particular sale. It's hard to tell who is actually looking out for you, or whether the price in front of you is fair.</p>
          <p>That's where I come in. You engage me as your advisor, and I work to your brief: defining what you actually want, searching the whole market (including properties that never reach the portals), inspecting with a critical eye, checking the legal and structural reality, and negotiating on your behalf. When something is wrong, I say so - even if it ends the deal.</p>
        </div>
      </div>
    </section>'''

    compare = f'''    <section class="section section--alt">
      <div class="container">
        <div class="section-head reveal"><p class="eyebrow">The difference</p><h2>The usual way vs. working with Nicolas</h2></div>
        <div class="compare reveal">
          <div class="compare__col compare__col--muted">
            <h3>The usual way</h3>
            <ul>
              <li>{icon(I_CROSS,'1.6')} A different agent for every property</li>
              <li>{icon(I_CROSS,'1.6')} Pressure to close that one sale</li>
              <li>{icon(I_CROSS,'1.6')} Problems easily glossed over</li>
              <li>{icon(I_CROSS,'1.6')} You judge whether the price is fair</li>
              <li>{icon(I_CROSS,'1.6')} Legals and paperwork left to you</li>
            </ul>
          </div>
          <div class="compare__col compare__col--highlight">
            <h3>Working with Nicolas</h3>
            <ul>
              <li>{icon(I_CHECK,'1.8')} One advisor across the whole market</li>
              <li>{icon(I_CHECK,'1.8')} Time taken to get it right for you</li>
              <li>{icon(I_CHECK,'1.8')} Every problem flagged, plainly</li>
              <li>{icon(I_CHECK,'1.8')} 25 years of pricing knowledge on your side</li>
              <li>{icon(I_CHECK,'1.8')} Lawyers, NIE &amp; banking all coordinated</li>
            </ul>
          </div>
        </div>
      </div>
    </section>'''

    steps_data = [
        ("Listen", "We start with a conversation, not a property. What's the home for, what matters, what's the budget - including the true all-in cost, not just the asking price."),
        ("Search", "I scan the whole market across the Costa Blanca North, including quiet, off-portal opportunities, and bring you a shortlist worth your time."),
        ("Inspect", "We view together. I look past the staging - orientation, build quality, noise, legal status, what it will really cost to run and improve."),
        ("Verify", "Lawyers, due diligence, NIE and banking, licences and registry checks. We confirm the property is exactly what it claims to be before any money moves."),
        ("Negotiate", "I negotiate on your behalf, using twenty-five years of local pricing knowledge to reach a number you wouldn't reach alone."),
        ("Complete &amp; settle in", "Notary, signing, utilities, and - if you wish - renovation, interiors and relocation handled by the same hand that bought it."),
    ]
    steps = "".join(f'''<div class="step reveal"><div class="step__num">{i+1}</div><div class="step__body"><h3>{t}</h3><p>{d}</p></div></div>''' for i,(t,d) in enumerate(steps_data))
    process = f'''    <section class="section">
      <div class="container container--reading">
        <div class="section-head reveal"><p class="eyebrow">The process</p><h2>How a purchase unfolds</h2></div>
        <div class="steps">{steps}</div>
      </div>
    </section>'''

    honesty = f'''    <section class="section section--alt">
      <div class="container">
        <div class="split">
          <div class="split__body reveal">
            <p class="eyebrow">Plain truths</p>
            <h2>The things no one tells you up front</h2>
            <div class="stack" style="margin-top:1.5rem;">
              <div><h3 style="font-size:1.2rem;">Budget for ~10–13% on top</h3><p class="text-muted mb-0">Taxes and purchase costs typically add 10–13% above the price (more for a new build). We plan for the real figure from day one.</p></div>
              <div><h3 style="font-size:1.2rem;">The notary doesn't protect you</h3><p class="text-muted mb-0">A notary confirms that signatures are valid. They do not check whether the property is a good or safe purchase. A lawyer protects the buyer - and I insist on one.</p></div>
              <div><h3 style="font-size:1.2rem;">The cheapest deal can be the dearest</h3><p class="text-muted mb-0">A low price often hides legal irregularities or building problems. I'd rather lose a sale than let you inherit someone else's mistake.</p></div>
            </div>
          </div>
          <div class="split__media reveal" data-delay="1"><img src="assets/images/nicolas/meeting-2.jpg" alt="Nicolas Strebel reviewing documents with clients" loading="lazy" width="800" height="600" /></div>
        </div>
      </div>
    </section>'''

    fee = f'''    <section class="section">
      <div class="container container--reading text-center">
        <p class="eyebrow reveal">Why it works</p>
        <h2 class="reveal text-balance">An honest opinion, every time</h2>
        <p class="lead text-muted reveal">Twenty-five years in this exact market, a network of lawyers, architects and craftsmen tested over decades, and the same straight assessment whether it ends in a purchase or an honest “don’t”. That is what you are really paying for.</p>
        <div class="btn-row reveal" style="justify-content:center;margin-top:2rem;"><a class="btn btn--primary" href="{wa('Hello Nicolas, I would like to understand how you work as a buyers advisor.')}" target="_blank" rel="noopener">{WA_ICON}Ask how it works</a></div>
      </div>
    </section>'''

    selling = f'''    <section class="section">
      <div class="container">
        <div class="split split--reverse">
          <div class="split__media reveal"><img src="assets/images/properties/calpe-villa-newbuild/02.webp" alt="A villa presented for sale on the Costa Blanca" loading="lazy" width="800" height="600" /></div>
          <div class="split__body reveal" data-delay="1">
            <p class="eyebrow">Selling your property</p>
            <h2>Sold properly, for the right price</h2>
            {ticklist(["An honest valuation - no inflated promise to win the instruction", "A designer's eye for presentation and staging", "Photography and reach to the right buyers", "Qualified buyers from a 25-year network", "Legals, paperwork and notary handled - a clean, fast sale"])}
            <a class="btn btn--ghost" href="{wa('Hello Nicolas, I am thinking of selling my property on the Costa Blanca.')}" target="_blank" rel="noopener" style="margin-top:0.25rem;">Talk about selling</a>
          </div>
        </div>
      </div>
    </section>'''

    areas = f'''    <section class="section section--navy" id="areas">
      <div class="container text-center">
        <p class="eyebrow reveal" style="color:var(--accent-soft)">Where I work</p>
        <h2 class="reveal">Costa Blanca North</h2>
        <p class="reveal" style="color:rgba(255,255,255,0.82);max-width:50ch;margin-inline:auto;">Moraira · Calpe · Jávea · Benissa · Benitachell · Cumbre del Sol · Altea · Teulada - the stretch of coast I've lived and worked in for twenty-five years.</p>
      </div>
    </section>'''

    relocation = f'''    <section class="section section--alt" id="relocation">
      <div class="container">
        <div class="split">
          <div class="split__body reveal">
            <p class="eyebrow">Relocation</p>
            <h2>Not just a house, a move</h2>
            <p class="text-muted">Buying is the straightforward part; moving your life is the rest. I made that move myself in 1998, and I've guided clients through it ever since - so the practical side of settling on the Costa Blanca doesn't fall on you alone.</p>
            {ticklist(["NIE number, a Spanish bank account and the paperwork that comes with both", "Utilities, insurance and the local registrations sorted", "Trusted contacts - lawyer, gestor, doctors, schools", "An honest read on the towns, and what living here is actually like"])}
            <a class="btn btn--ghost" href="{wa('Hello Nicolas, I am planning to relocate to the Costa Blanca and would like some guidance.')}" target="_blank" rel="noopener" style="margin-top:0.25rem;">Talk about relocating</a>
          </div>
          <div class="split__media reveal" data-delay="1"><img src="assets/images/nicolas/meeting-1.jpg" alt="Settling in on the Costa Blanca with Nicolas Strebel" loading="lazy" width="800" height="600" /></div>
        </div>
      </div>
    </section>'''

    return hero + explain + compare + process + selling + relocation + honesty + fee + areas + cta_band("Considering a move on the Costa Blanca?", "A first conversation is free and without obligation. If now isn't the right time, I'll tell you that too.")


# ---------------------------------------------------------------- CONSTRUCTION
def body_construction():
    hero = f'''    <section class="page-hero page-hero--image">
      <div class="page-hero__media"><img src="assets/images/construction/onsite-crane.jpg" alt="Construction project on the Costa Blanca" width="1600" height="1200" /></div>
      <div class="page-hero__inner"><div class="container">
        <p class="breadcrumb reveal"><a href="index.html">Home</a> · Home Projects</p>
        <p class="eyebrow hero__eyebrow reveal" style="color:#E7D9BD">Division 02 · Home Projects</p>
        <h1 class="display reveal" data-delay="1">Build, renovate, refurbish,<br />and finish it beautifully.</h1>
        <p class="reveal" data-delay="2">New-build villas, renovations and refurbishments, interior design, furniture and full project coordination on the Costa Blanca - one accountable person, from the first permit to the last detail.</p>
      </div></div>
    </section>'''

    intro = f'''    <section class="section">
      <div class="container container--reading">
        <p class="eyebrow eyebrow--sand reveal">An eye for what a place can be</p>
        <h2 class="reveal">I came to building through design</h2>
        <hr class="rule-accent rule-accent--sand reveal" />
        <div class="prose reveal stack">
          <p>My first training was in Fashion Design at Istituto Marangoni in Milan, followed by a high-fashion design team in Düsseldorf - an education in proportion, material, function and detail. I brought that eye to the Costa Blanca and spent twenty-five years delivering new-build and renovation projects here - more than fifty of them - coordinating the architects, builders and craftsmen myself, to a standard I'm proud to put my name to.</p>
          <p>It means I can look at a tired, awkward or unloved property and see the house it could become - and then actually deliver it, because I bring together and direct the whole chain of professionals, independently and on your behalf.</p>
        </div>
      </div>
    </section>'''

    included = f'''    <section class="section section--alt" id="coordination">
      <div class="container">
        <div class="section-head reveal"><p class="eyebrow eyebrow--sand">Project coordination · what's included</p><h2>One project manager for the entire build</h2></div>
        <div class="features">
          <div class="feature reveal"><svg class="feature__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M3 21h18M5 21V8l7-5 7 5v13"/><path d="M9 21v-6h6v6"/></svg><h3>Project management</h3><p>A single point of responsibility for timeline, budget and quality from start to finish.</p></div>
          <div class="feature reveal" data-delay="1"><svg class="feature__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M4 4h16v16H4z"/><path d="M9 9h6v6H9z"/></svg><h3>Legal &amp; permits</h3><p>Licences, architects, technical certificates and the paperwork that keeps a project legal and on track.</p></div>
          <div class="feature reveal" data-delay="2"><svg class="feature__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M14 7l3 3M5 19l9-9 1-4 4-1 1 4-1 4-9 9-5 1z"/></svg><h3>Craftsmen &amp; quality control</h3><p>A network of trades tested over decades, supervised to a standard I'm willing to put my name to.</p></div>
          <div class="feature reveal"><svg class="feature__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M3 9l9-6 9 6v11a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1z"/><path d="M9 22V12h6v10"/></svg><h3>Interiors &amp; furnishing</h3><p>Aesthetics, interior design, furniture and decoration - so the house is ready to live in, not just finished.</p></div>
          <div class="feature reveal" data-delay="1"><svg class="feature__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><circle cx="12" cy="12" r="9"/><path d="M8 12l3 3 5-6"/></svg><h3>Quality control</h3><p>Every stage supervised to the standard I built my reputation on.</p></div>
          <div class="feature reveal" data-delay="2"><svg class="feature__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M12 3v18M3 12h18"/></svg><h3>Coordination</h3><p>Architects, engineers, trades and suppliers - managed by one person, reporting to you.</p></div>
        </div>
      </div>
    </section>'''

    types = f'''    <section class="section" id="services">
      <div class="container">
        <div class="grid grid-3">
          <article class="card reveal" id="new-build"><div class="card__media"><img src="assets/images/properties/calpe-villa-newbuild/05.webp" alt="New-build villa on the Costa Blanca" loading="lazy" width="600" height="400"/></div><div class="card__body"><p class="eyebrow eyebrow--sand" style="margin-bottom:0.4rem;">01</p><h3>New-build villas</h3><p class="text-muted mb-0">From plot and plans to a finished, furnished home - villa construction managed as one continuous project.</p></div></article>
          <article class="card reveal" data-delay="1" id="renovation"><div class="card__media"><img src="assets/images/construction/onsite-nicolas.jpg" alt="Renovation and refurbishment on the Costa Blanca" loading="lazy" width="600" height="400"/></div><div class="card__body"><p class="eyebrow eyebrow--sand" style="margin-bottom:0.4rem;">02</p><h3>Renovation &amp; refurbishment</h3><p class="text-muted mb-0">Reworking a dated or awkward property into something light, modern and genuinely liveable.</p></div></article>
          <article class="card reveal" data-delay="2" id="interiors"><div class="card__media"><img src="assets/images/properties/calpe-villa-residential/05.webp" alt="Interior design and furniture on the Costa Blanca" loading="lazy" width="600" height="400"/></div><div class="card__body"><p class="eyebrow eyebrow--sand" style="margin-bottom:0.4rem;">03</p><h3>Interior design &amp; furniture</h3><p class="text-muted mb-0">Layout, materials, furniture and decoration, finished to a calm, considered standard.</p></div></article>
        </div>
      </div>
    </section>'''

    onground = f'''    <section class="section section--alt">
      <div class="container">
        <div class="split split--reverse">
          <div class="split__media split__media--wide reveal"><img src="assets/images/construction/onsite-crane.jpg" alt="Nicolas Strebel managing a build on site" loading="lazy" width="800" height="600"/></div>
          <div class="split__body reveal" data-delay="1">
            <p class="eyebrow eyebrow--sand">On the ground</p>
            <h2>I'm on site, not behind a desk</h2>
            <p class="text-muted">Coordination only works if someone is actually there - checking the work, catching problems early, keeping trades to schedule. That's the part owners abroad can't do themselves, and it's the part I take off your hands.</p>
            <p class="text-muted">Portfolio and before/after references are available on request, tailored to the kind of project you have in mind.</p>
          </div>
        </div>
      </div>
    </section>'''

    transformations = f'''    <section class="section section--alt" id="transformations">
      <div class="container">
        <div class="section-head reveal"><p class="eyebrow eyebrow--sand">Before &amp; after</p><h2 class="mb-0">See a transformation</h2></div>
        <p class="text-muted reveal" style="max-width:62ch;margin-top:1rem;">Recent projects on the Costa Blanca, coordinated from the first idea to the finished, furnished home. No staging and no stock footage, just the work. Pick a clip to watch.</p>
        {video_gallery([
            ("mar2-before-after", "Apartment, before &amp; after", "0:25", "A recent apartment renovation: before and after, in twenty-five seconds.", True),
            ("enchinent-before-after", "A second apartment", "1:19", "Another recent transformation, start to finish.", True),
            ("mar2-renovation-full", "The full renovation", "2:36", "The complete apartment transformation, start to finish, with sound.", False),
        ])}
      </div>
    </section>'''
    return hero + intro + included + types + transformations + onground + cta_band("Have a property or a plot in mind?", "Send me a photo and a few words. I'll tell you honestly what's possible, and roughly what it would take.")


# ---------------------------------------------------------------- INVESTING
def body_invest():
    hero = f'''    <section class="page-hero page-hero--image">
      <div class="page-hero__media"><img src="assets/images/hero/villa-wide.webp" alt="Villa overlooking the Costa Blanca" width="2048" height="1536" /></div>
      <div class="page-hero__inner"><div class="container">
        <p class="breadcrumb reveal"><a href="index.html">Home</a> · Investing</p>
        <p class="eyebrow hero__eyebrow reveal">A second, honest opinion</p>
        <h1 class="display reveal" data-delay="1">A sober look at the numbers.</h1>
        <p class="reveal" data-delay="2">Property here can be a sound investment - or a quiet mistake. I help you tell the difference, with twenty-five years watching this exact market.</p>
      </div></div>
    </section>'''

    assess = f'''    <section class="section">
      <div class="container">
        <div class="split">
          <div class="split__body reveal">
            <p class="eyebrow">What I assess</p>
            <h2>The figures behind the photos</h2>
            {ticklist(["True all-in cost - taxes, fees and the surprises", "Realistic rental income and occupancy", "Resale demand and exit potential", "Renovation upside, costed with the trades I coordinate", "Legal and structural risk, checked early"])}
            <a class="btn btn--primary" href="{wa('Hello Nicolas, I would like to discuss a property investment on the Costa Blanca.')}" target="_blank" rel="noopener">{WA_ICON}Discuss an investment</a>
          </div>
          <div class="split__media reveal" data-delay="1"><img src="assets/images/hero/area-calpe.webp" alt="Calpe from above" loading="lazy" width="800" height="600" /></div>
        </div>
      </div>
    </section>'''

    why = f'''    <section class="section section--alt">
      <div class="container">
        <div class="section-head reveal"><p class="eyebrow">Why investors work with me</p><h2 class="mb-0">Numbers first, honesty always.</h2></div>
        <div class="features" style="margin-top:2.5rem;">
          <div class="feature reveal"><svg class="feature__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M3 12h4l3 8 4-16 3 8h4"/></svg><h3>An honest yes or no</h3><p>If the numbers don't work, I'll say so - before you commit, not after.</p></div>
          <div class="feature reveal" data-delay="1"><svg class="feature__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M3 21h18M5 21V8l7-5 7 5v13"/></svg><h3>Build &amp; renovate to add value</h3><p>I can cost and manage the works that turn a fair buy into a strong return.</p></div>
          <div class="feature reveal" data-delay="2"><svg class="feature__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg><h3>Twenty-five years of data</h3><p>I've watched prices, rentals and demand on this coast through every cycle.</p></div>
        </div>
      </div>
    </section>'''

    return hero + assess + why + cta_band("Thinking of investing here?", "Send me the property or the budget. I'll give you a straight read on the numbers.")


# ---------------------------------------------------------------- PROPERTIES
def body_properties():
    hero = f'''    <section class="page-hero page-hero--plain">
      <div class="container">
        <p class="breadcrumb reveal"><a href="index.html">Home</a> · Properties</p>
        <h1 class="display reveal" data-delay="1">Properties on the Costa Blanca.</h1>
        <p class="reveal" data-delay="2">Browse the current selection and filter by type, area, size and price. When you're ready for more, I search the whole market - including listings that never reach a public page.</p>
      </div>
    </section>'''

    tcount, rcount = {}, {}
    for _p in PROPERTIES:
        tcount[_p['type']] = tcount.get(_p['type'], 0) + 1
        rcount[_p['region']] = rcount.get(_p['region'], 0) + 1
    type_opts = "".join(f'<option value="{t}">{t} ({tcount[t]})</option>' for t in sorted(tcount))
    region_opts = "".join(f'<option value="{r}">{r} ({rcount[r]})</option>' for r in sorted(rcount))
    n = len(PROPERTIES)
    # cards carry data-order so "newest" sort can restore the default order
    cards = "".join(prop_card(p, idx=i) for i, p in enumerate(PROPERTIES))

    filters = f'''    <section class="section" style="padding-bottom:0;">
      <div class="container">
        <div class="filters reveal" role="group" aria-label="Filter properties">
          <div class="filters__field">
            <label for="f-type">Type</label>
            <select id="f-type" data-filter="type"><option value="">All types</option>{type_opts}</select>
          </div>
          <div class="filters__field">
            <label for="f-region">Area</label>
            <select id="f-region" data-filter="region"><option value="">All areas</option>{region_opts}</select>
          </div>
          <div class="filters__field">
            <label for="f-beds">Bedrooms</label>
            <select id="f-beds" data-filter="beds"><option value="">Any</option><option value="1">1+</option><option value="2">2+</option><option value="3">3+</option><option value="4">4+</option><option value="5">5+</option><option value="6">6+</option></select>
          </div>
          <div class="filters__field">
            <label for="f-price">Price</label>
            <select id="f-price" data-filter="price">
              <option value="">Any price</option>
              <option value="0-300000">Up to €300,000</option>
              <option value="300000-500000">€300,000 – €500,000</option>
              <option value="500000-750000">€500,000 – €750,000</option>
              <option value="750000-1000000">€750,000 – €1,000,000</option>
              <option value="1000000-2000000">€1M – €2M</option>
              <option value="2000000-999999999">€2M and above</option>
            </select>
          </div>
          <div class="filters__field">
            <label for="f-sort">Sort by</label>
            <select id="f-sort" data-sort><option value="">Newest first</option><option value="price-asc">Price: low to high</option><option value="price-desc">Price: high to low</option><option value="beds-desc">Most bedrooms</option></select>
          </div>
          <button class="filters__reset" type="button" data-filter-reset>Reset</button>
        </div>
        <p class="filters__count" data-filter-count>Showing {n} of {n} properties</p>
      </div>
    </section>'''

    grid = f'''    <section class="section" style="padding-top:1.5rem;">
      <div class="container">
        <div class="prop-grid" data-filter-grid>{cards}</div>
        <p class="filters__empty" data-filter-empty hidden>No properties match those filters yet. <a class="link" href="{wa('Hello Nicolas, I am looking for a specific kind of property on the Costa Blanca.')}" target="_blank" rel="noopener">Tell me what you're looking for</a> and I'll search privately.</p>
        <div class="text-center" style="margin-top:3.5rem;">
          <p class="text-muted">This is a curated selection - most of what I find for clients never reaches a public page.</p>
          <a class="btn btn--primary" href="{wa('Hello Nicolas, I am looking for a specific kind of property on the Costa Blanca.')}" target="_blank" rel="noopener" style="margin-top:0.5rem;">{WA_ICON}Request a tailored search</a>
        </div>
      </div>
    </section>'''
    return hero + filters + grid + cta_band()


# ---------------------------------------------------------------- PROPERTY DETAIL
def body_property(p):
    imgs = p.get("gallery") or ([p["cover"]] if p.get("cover") else [PLACEHOLDER_IMG])
    total = p.get("photos", len(imgs))
    tiles = []
    for i, src in enumerate(imgs[:5]):
        overlay = f'<span class="gallery__more">+{total-5} photos</span>' if (i == 4 and total > 5) else ''
        tiles.append(f'<a href="{src}" target="_blank" rel="noopener"><img src="{src}" alt="{p["title"]} - photo {i+1}" loading="lazy" width="600" height="450"/>{overlay}</a>')
    gallery = "".join(tiles)
    spec_rows = []
    if p.get('beds'): spec_rows.append(("Bedrooms", p['beds']))
    if p.get('baths'): spec_rows.append(("Bathrooms", p['baths']))
    if p.get('area'): spec_rows.append(("Built area", p['area']))
    if p.get('plot'): spec_rows.append(("Plot", p['plot']))
    if p.get('pool'): spec_rows.append(("Outdoor", p['pool']))
    if p.get('energy'): spec_rows.append(("Energy rating", p['energy']))
    specs = ('<dl class="spec-list">' + "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in spec_rows) + '</dl>') if spec_rows else ''
    feats_html = "".join(f'<li>{icon(I_CHECK,"1.8")} {f}</li>' for f in p['features'])
    # Only show Highlights when there's enough to be worth a heading - otherwise it looks sparse.
    highlights = (f'''<h3 style="margin:2.5rem 0 1rem;">Highlights</h3>
            <ul class="compare" style="display:block;border:0;background:none;list-style:none;padding:0;margin:0;">
              <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.85rem;">{feats_html}</div>
            </ul>''' if len(p.get('features', [])) >= 3 else '')
    desc = "".join(f'<p>{d}</p>' for d in p['desc'])
    wa_msg = wa(f"Hello Nicolas, I'm interested in the {p['title']} ({p['price']}). Could we arrange a viewing?")

    hero = f'''    <section class="section section--tight" style="padding-bottom:0;">
      <div class="container">
        <p class="breadcrumb reveal" style="color:var(--muted)"><a href="index.html">Home</a> · <a href="properties.html">Properties</a> · {p['title']}</p>
        <div class="reveal" style="display:flex;justify-content:space-between;align-items:flex-end;gap:1.5rem;flex-wrap:wrap;">
          <div>
            <span class="prop-card__loc">{p['loc']}</span>
            <h1 style="margin:0.3rem 0 0;">{p['title']}</h1>
          </div>
          <div class="prop-card__meta" style="font-size:1rem;">{_meta_spans(p)}</div>
        </div>
      </div>
    </section>
    <section class="section section--tight" style="padding-top:1.5rem;">
      <div class="container"><div class="gallery reveal">{gallery}</div></div>
    </section>'''

    main = f'''    <section class="section" style="padding-top:0;">
      <div class="container">
        <div class="detail-layout">
          <div class="reveal">
            <p class="eyebrow">About this property</p>
            <div class="prose stack" style="margin-bottom:2.5rem;">{desc}</div>
            {specs}
            {highlights}
          </div>
          <aside class="detail-aside reveal" data-delay="1">
            <div class="price">{p['price']}<small>Asking price · taxes &amp; purchase costs additional</small></div>
            <form class="enquiry-form" data-enquiry-form data-property-id="{p['id']}" data-property-ref="{p.get('ref','')}">
              <p class="enquiry-form__title">Request details or a viewing</p>
              <input type="text" name="name" autocomplete="name" placeholder="Your name" required />
              <input type="email" name="email" autocomplete="email" placeholder="Email" required />
              <input type="tel" name="phone" autocomplete="tel" placeholder="Phone / WhatsApp" required />
              <textarea name="message" rows="3" placeholder="Anything you'd like to ask? (optional)"></textarea>
              <label class="enquiry-form__consent"><input type="checkbox" name="consent" required /> <span>I agree to be contacted about this enquiry. See the <a href="legal.html#privacy">privacy notice</a>.</span></label>
              <button class="btn btn--primary" type="submit" data-enquiry-submit>Send enquiry</button>
              <p class="enquiry-form__status" data-enquiry-status role="status" hidden></p>
            </form>
            <a class="btn btn--whatsapp" href="{wa_msg}" target="_blank" rel="noopener" style="margin-top:0.75rem;">{WA_ICON}Or message on WhatsApp</a>
            <hr class="divider" style="margin:1.5rem 0 1.25rem;" />
            <p class="text-muted mb-0" style="font-size:0.92rem;">As your buyer's advisor I'll verify the legal status, check the real running costs, and tell you honestly how this compares with others at this price - before you commit.</p>
          </aside>
        </div>
      </div>
    </section>'''
    extras = ""
    if p.get("lat") and p.get("lng"):
        q = f'{p["lat"]},{p["lng"]}'
        extras += f'''    <section class="section section--alt">
      <div class="container">
        <p class="eyebrow reveal">Location</p>
        <h2 class="reveal" style="margin-bottom:1.25rem;">{p['loc']}</h2>
        <div class="map-embed reveal"><iframe loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Map of {p['loc']}" src="https://www.google.com/maps?q={q}&amp;z=14&amp;output=embed"></iframe></div>
        <p class="text-muted" style="margin-top:0.75rem;font-size:0.9rem;">Approximate area. The exact address is shared on viewing.</p>
      </div>
    </section>'''
    _yt = _re.search(r'(?:v=|youtu\.be/|embed/)([A-Za-z0-9_-]{11})', p.get("video", "")) if p.get("video") else None
    if _yt:
        extras += f'''    <section class="section">
      <div class="container container--reading">
        <p class="eyebrow reveal">Video</p>
        <h2 class="reveal" style="margin-bottom:1.25rem;">A closer look</h2>
        <div class="video-embed reveal"><iframe loading="lazy" title="Property video" src="https://www.youtube.com/embed/{_yt.group(1)}" allowfullscreen></iframe></div>
      </div>
    </section>'''
    return hero + main + extras + cta_band("Want a closer look - with someone on your side?", "I'll arrange the viewing, ask the awkward questions for you, and give you a straight assessment.")


# ---------------------------------------------------------------- ABOUT
def body_about():
    hero = f'''    <section class="page-hero page-hero--plain">
      <div class="container">
        <p class="breadcrumb reveal"><a href="index.html">Home</a> · About</p>
        <h1 class="display reveal" data-delay="1">Nicolas Strebel</h1>
        <p class="reveal" data-delay="2">Swiss, Costa Blanca by choice, an independent advisor across real estate, home projects and investment, with twenty-five years on this coast and no ties to any single agency or builder.</p>
      </div>
    </section>'''

    profile = f'''    <section class="section">
      <div class="container">
        <div class="split">
          <div class="split__media reveal"><img src="assets/images/nicolas/portrait-warm.jpg" alt="Nicolas Strebel" loading="lazy" width="976" height="1220" /></div>
          <div class="split__body reveal" data-delay="1">
            <p class="eyebrow">Who you'll work with</p>
            <h2>An advisor and a project partner, not a sales desk</h2>
            <p class="text-muted">Swiss, born in Zurich, I studied Fashion Design at Istituto Marangoni in Milan and then worked in the design team of a high-fashion house in Düsseldorf. I came to the Costa Blanca in 1998 and made it home - and that training in proportion, material, function and detail still shapes how I read a property and what it could become.</p>
            <p class="text-muted">In 2001 I co-founded one of the area's respected agencies. Over the next two decades I sold more than 500 properties and delivered over 50 building and renovation projects, coordinating the architects, builders and craftsmen rather than carrying out the work myself. In 2024 I went fully independent: working directly and honestly with a small number of clients at a time, tied to no single agency or builder.</p>
            <dl class="facts">
              <div><dt>Based in</dt><dd>Teulada</dd></div>
              <div><dt>On this coast</dt><dd>Since 1998</dd></div>
              <div><dt>Track record</dt><dd>500+ sold · 50+ projects</dd></div>
              <div><dt>Languages</dt><dd>DE · ES · EN · FR · IT</dd></div>
            </dl>
          </div>
        </div>
      </div>
    </section>'''

    whatido = f'''    <section class="section section--alt">
      <div class="container">
        <div class="section-head reveal"><p class="eyebrow">What I help with</p><h2 class="mb-0">One advisor, the whole journey</h2></div>
        <div class="features" style="margin-top:2.5rem;">
          <div class="feature reveal">
            <svg class="feature__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M3 11l9-7 9 7M5 10v10h14V10"/><path d="M9 20v-6h6v6"/></svg>
            <h3>Real estate</h3>
            <p>Buying and selling across the whole market - searched, vetted, valued and negotiated, with the legals and paperwork handled either way.</p>
            <a class="text-cta" href="buyers-advisor.html">Buying &amp; selling {ARROW}</a>
          </div>
          <div class="feature reveal" data-delay="1">
            <svg class="feature__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M14 7l3 3M5 19l9-9 1-4 4-1 1 4-1 4-9 9-5 1z"/></svg>
            <h3>Construction &amp; renovation</h3>
            <p>New builds and renovations coordinated end to end - permits, architects, craftsmen, interiors and furnishing, all in one hand.</p>
            <a class="text-cta" href="home-projects.html">Construction {ARROW}</a>
          </div>
          <div class="feature reveal" data-delay="2">
            <svg class="feature__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M3 12h4l3 8 4-16 3 8h4"/></svg>
            <h3>Investing</h3>
            <p>A sober read on the numbers - true all-in cost, realistic yields, resale potential and the risks worth knowing before you commit.</p>
            <a class="text-cta" href="investing.html">Investing {ARROW}</a>
          </div>
        </div>
      </div>
    </section>'''

    chapters = [
        ("01 · Milan", "An eye trained in design", "I studied Fashion Design at Istituto Marangoni in Milan, then worked in the design team of a high-fashion house in Düsseldorf. It taught me proportion, material, function and an intolerance for poor detail that has never left me."),
        ("02 · Arrival", "Costa Blanca, 1998", "I moved to Moraira in 1998 and fell for the light, the architecture and the pace of the Costa Blanca North. It became home - and the place I'd spend the next quarter-century learning house by house."),
        ("03 · Jetvillas", "Building a reputation", "In 2001 I co-founded the Jetvillas agency and spent two decades not only selling homes but delivering the building and renovation projects behind them, coordinating the architects, builders and craftsmen who did the work. Out of it came 500+ properties sold and 50+ projects delivered."),
        ("04 · Independent", "On my own terms, 2024", "In 2024 I sold my Jetvillas shares to work independently with a small number of clients at a time. No volume targets, no divided loyalties - just honest guidance across buying, selling, building and investing, the way I always wanted to give it."),
    ]
    chap_html = ""
    # (src under assets/images/, wide-aspect?, object-position, alt)
    media = [
        ("nicolas/fashion-dusseldorf.jpg", True, "center", "A high-fashion runway show in D&uuml;sseldorf, where Nicolas Strebel worked on the design team"),
        ("hero/moraira-portet.jpg", True, "center", "Playa del Portet, Moraira - the Costa Blanca North cove where Nicolas Strebel made his home in 1998"),
        ("nicolas/portrait-studio.jpg", False, "center", "Nicolas Strebel"),
        ("nicolas/nicolas-desk.jpg", True, "60% center", "Nicolas Strebel working independently from his desk on the Costa Blanca"),
    ]
    for i,(eyebrow,h,t) in enumerate(chapters):
        reverse = " split--reverse" if i % 2 else ""
        src, wide, objpos, alt = media[i]
        wide_cls = " split__media--wide" if wide else ""
        dims = 'width="800" height="600"' if wide else 'width="800" height="1000"'
        chap_html += f'''    <section class="section{' section--alt' if i%2 else ''}">
      <div class="container">
        <div class="split{reverse}">
          <div class="split__media{wide_cls} reveal"><img src="assets/images/{src}" alt="{alt}" loading="lazy" {dims} style="object-position:{objpos};"/></div>
          <div class="split__body reveal" data-delay="1">
            <p class="eyebrow">{eyebrow}</p>
            <h2>{h}</h2>
            <p class="text-muted">{t}</p>
          </div>
        </div>
      </div>
    </section>'''

    principles = f'''    <section class="section">
      <div class="container">
        <div class="section-head text-center reveal"><p class="eyebrow">How I work</p><h2>Three principles I won't bend</h2></div>
        <div class="features">
          <div class="feature reveal"><svg class="feature__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M12 3l2.5 5 5.5.8-4 3.9.9 5.5L12 16.5 7.1 18.2l.9-5.5-4-3.9 5.5-.8z"/></svg><h3>A limited number of clients</h3><p>I take on only a few clients at a time, so each one gets my attention rather than my calendar.</p></div>
          <div class="feature reveal" data-delay="1"><svg class="feature__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M4 12a8 8 0 1 0 16 0 8 8 0 0 0-16 0z"/><path d="M9 12l2 2 4-4"/></svg><h3>I'll tell you when not to buy</h3><p>The advice you remember is the deal someone talked you out of. I'd rather be that person than a salesman.</p></div>
          <div class="feature reveal" data-delay="2"><svg class="feature__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M3 21h18M6 21V11M10 21V7M14 21V9M18 21V5"/></svg><h3>A network tested over 25 years</h3><p>Every professional I bring to you has been proven over decades - not sourced for the occasion.</p></div>
        </div>
      </div>
    </section>'''

    langs = f'''    <section class="section section--navy">
      <div class="container text-center">
        <p class="eyebrow reveal" style="color:var(--accent-soft)">No barrier</p>
        <h2 class="reveal">Five languages, native-level care</h2>
        <p class="reveal" style="color:rgba(255,255,255,0.82);max-width:46ch;margin-inline:auto;">German (native), Spanish (native-level), English, French and Italian. You'll be understood - and so will every contract, every craftsman and every official.</p>
        <div class="pill-row reveal" style="justify-content:center;margin-top:1.75rem;">
          <span class="pill">Deutsch</span><span class="pill">English</span><span class="pill">Español</span><span class="pill">Français</span><span class="pill">Italiano</span>
        </div>
      </div>
    </section>'''

    areas = f'''    <section class="section section--alt" id="areas">
      <div class="container text-center">
        <p class="eyebrow reveal">Where I work</p>
        <h2 class="reveal">Areas I cover on the Costa Blanca North</h2>
        <p class="lead text-muted reveal" style="max-width:56ch;margin-inline:auto;">The stretch of coast I've lived and worked on for twenty-five years - I know these towns, their quiet pockets and their prices, street by street.</p>
        <div class="pill-row reveal" style="justify-content:center;margin-top:1.75rem;">
          <span class="pill">Moraira</span><span class="pill">Calpe</span><span class="pill">Jávea</span><span class="pill">Benissa</span><span class="pill">Benitachell</span><span class="pill">Cumbre del Sol</span><span class="pill">Altea</span><span class="pill">Teulada</span>
        </div>
      </div>
    </section>'''

    return hero + profile + whatido + chap_html + section_stats(navy=False) + principles + areas + langs + cta_band("Let's have a first conversation.", "No obligation, no pressure - just an honest discussion about what you're trying to do.")


# ---------------------------------------------------------------- CONTACT
def body_contact():
    hero = f'''    <section class="page-hero page-hero--plain">
      <div class="container">
        <p class="breadcrumb reveal"><a href="index.html">Home</a> · Contact</p>
        <h1 class="display reveal" data-delay="1">Let's talk.</h1>
        <p class="reveal" data-delay="2">The easiest way to reach me is WhatsApp - I answer personally, usually within a working day. Mornings, Monday to Friday.</p>
      </div>
    </section>'''

    methods = f'''        <div class="contact-methods">
          <a class="contact-method" href="{wa()}" target="_blank" rel="noopener">
            <span class="contact-method__icon">{WA_ICON}</span>
            <span class="contact-method__text"><span class="contact-method__label">WhatsApp · preferred</span><span class="contact-method__value">{PHONE_DISPLAY}</span></span>
          </a>
          <a class="contact-method" href="tel:+{WA_NUMBER}">
            <span class="contact-method__icon">{icon('<path d="M5 4h4l2 5-3 2a12 12 0 0 0 5 5l2-3 5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>','1.6')}</span>
            <span class="contact-method__text"><span class="contact-method__label">Phone</span><span class="contact-method__value">{PHONE_DISPLAY}</span></span>
          </a>
          <a class="contact-method" href="mailto:{EMAIL}">
            <span class="contact-method__icon">{icon('<path d="M3 6h18v12H3zM3 7l9 6 9-6"/>','1.6')}</span>
            <span class="contact-method__text"><span class="contact-method__label">Email</span><span class="contact-method__value">{EMAIL}</span></span>
          </a>
          <div class="contact-method" style="cursor:default;">
            <span class="contact-method__icon">{icon('<path d="M12 21s-7-6-7-11a7 7 0 0 1 14 0c0 5-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>','1.6')}</span>
            <span class="contact-method__text"><span class="contact-method__label">Office · {HOURS}</span><span class="contact-method__value">{ADDRESS}</span></span>
          </div>
        </div>'''

    form = f'''        <form id="contact-form" class="contact-form-card reveal" novalidate>
          <div class="field"><label for="cf-name">Name</label><input id="cf-name" name="name" type="text" autocomplete="name" required placeholder="Your name" /></div>
          <div class="field"><label for="cf-contact">Email or WhatsApp</label><input id="cf-contact" name="contact" type="text" required placeholder="So I can reach you" /></div>
          <div class="field"><label for="cf-intent">What are you looking for?</label>
            <select id="cf-intent" name="intent">
              <optgroup label="Real Estate">
                <option value="Buying">Buying - I'd like an advisor</option>
                <option value="Selling">Selling</option>
                <option value="Property sourcing">Property sourcing</option>
                <option value="Investing">Investing</option>
              </optgroup>
              <optgroup label="Home Projects">
                <option value="New build">New-build villa</option>
                <option value="Renovation">Renovation or refurbishment</option>
                <option value="Interior design">Interior design or furniture</option>
              </optgroup>
              <option value="Relocation">Relocation</option>
              <option value="General enquiry">General enquiry</option>
            </select>
          </div>
          <div class="field"><label for="cf-message">Message</label><textarea id="cf-message" name="message" placeholder="A few words about what you have in mind"></textarea></div>
          <div class="btn-row" style="display:flex;gap:0.75rem;flex-wrap:wrap;">
            <button class="btn btn--whatsapp" type="submit" data-send="whatsapp">{WA_ICON}Send via WhatsApp</button>
            <button class="btn btn--ghost" type="submit" data-send="email">Send via email</button>
          </div>
          <p class="form-note">Your details are used only to reply to you - never shared, never added to a list. By sending you agree to be contacted about your enquiry.</p>
        </form>'''

    body = f'''    <section class="section">
      <div class="container">
        <div class="split" style="align-items:start;">
          <div class="reveal">
            <p class="eyebrow">Reach Nicolas directly</p>
            <h2 style="margin-bottom:1.5rem;">Four ways to get in touch</h2>
            {methods}
          </div>
          <div>
            <p class="eyebrow reveal">Or send a message</p>
            <h2 class="reveal" style="margin-bottom:1.5rem;">Tell me what you need</h2>
            {form}
          </div>
        </div>
      </div>
    </section>'''
    return hero + body


# ---------------------------------------------------------------- STORY
def body_story():
    hero = f'''    <section class="page-hero page-hero--image">
      <div class="page-hero__media"><img src="assets/images/nicolas/portrait-studio.jpg" alt="Nicolas Strebel" width="1600" height="1066" /></div>
      <div class="page-hero__inner"><div class="container">
        <p class="breadcrumb reveal"><a href="index.html">Home</a> · <a href="about.html">About</a> · The story</p>
        <p class="eyebrow hero__eyebrow reveal">The story</p>
        <h1 class="display reveal" data-delay="1">From haute couture<br />to the Costa Blanca.</h1>
        <p class="reveal" data-delay="2">How a Fashion Design graduate from Zurich became the independent advisor Northern-European buyers trust to find, transform and finish a home in Spain.</p>
      </div></div>
    </section>'''

    body = f'''    <section class="section">
      <div class="container container--reading">
        <p class="lead reveal">I didn't come to property the usual way. I came to it through design, through building, and through making - myself, in 1998 - the exact move my clients are about to make.</p>
        <hr class="rule-accent reveal" />
        <div class="prose stack reveal">
          <h2>Milan, and an intolerance for poor detail</h2>
          <p>I studied Fashion Design at Istituto Marangoni in Milan, then worked as part of the design team of a high-fashion house in Düsseldorf. Fashion is an education in proportion, material, function and finish - and in noticing the half-millimetre that's wrong. That eye never left me; today it's the difference between a house that photographs well and one that actually feels right to live in.</p>

          <h2>Costa Blanca, 1998</h2>
          <p>I came to Moraira to visit and stayed. The light, the architecture and the unhurried pace of the Costa Blanca North made the decision for me. I spent the next quarter-century learning this coast the only way that counts - house by house, town by town, deal by deal - until I knew not just the prices but the quiet streets, the building quirks and the people worth trusting.</p>

          <h2>Jetvillas, and a building company</h2>
          <p>In 2001 I co-founded the Jetvillas agency, and that is the part most agents don't have: I wasn't only selling houses, I was responsible for the building and renovation projects behind them, coordinating the architects, builders and craftsmen who did the work, never claiming to be the contractor myself. Out of those years came more than 500 properties sold and over 50 building and renovation projects delivered. More usefully, it left me a tested network of lawyers, architects and craftsmen I'd put my name to, and that I'm tied to none of.</p>

          <h2>Independent, since 2024</h2>
          <p>In 2024 I sold my Jetvillas shares to work on my own terms: a few clients at a time, no volume targets, no seller loyalties pulling the other way. It lets me do the thing I always wanted - be one honest point of contact for the whole journey, from the first viewing to the finished, furnished home. If something is wrong with a property, I say so, even when it costs me the sale. That's the whole point of working with me instead of a sales desk.</p>

          <p class="text-muted">The short version fits on a page. The longer one is better over coffee - which, more often than not, is where my clients' projects begin.</p>
        </div>
      </div>
    </section>'''
    return hero + body + cta_band("Let's start with a conversation.", "No obligation - just an honest talk about what you're trying to do on the Costa Blanca.")


# ---------------------------------------------------------------- LEGAL & PRIVACY
def body_legal():
    hero = f'''    <section class="page-hero page-hero--plain">
      <div class="container">
        <p class="breadcrumb reveal"><a href="index.html">Home</a> · Legal &amp; Privacy</p>
        <h1 class="display reveal" data-delay="1">Legal &amp; privacy</h1>
        <p class="reveal" data-delay="2">Who runs this site, how your information is handled, and the cookies it uses - in plain language.</p>
      </div>
    </section>'''

    body = f'''    <section class="section">
      <div class="container container--reading prose stack">
        <p class="text-muted" style="font-size:0.9rem;">Last updated June 2026. This is a clear-language version; a lawyer-reviewed Spanish text should be added before public launch and takes precedence.</p>

        <h2 id="legal">Legal notice</h2>
        <p>This website is owned and operated by Nicolas Strebel, an independent advisor in real estate, building &amp; renovation projects, and investment on the Costa Blanca North, Spain. Nicolas does not operate a construction company; he coordinates an independent network of trusted professionals.</p>
        <ul>
          <li><strong>Owner:</strong> Nicolas Strebel</li>
          <li><strong>Address:</strong> {ADDRESS}</li>
          <li><strong>Email:</strong> <a href="mailto:{EMAIL}">{EMAIL}</a> · <strong>Phone:</strong> {PHONE_DISPLAY}</li>
          <li><strong>Tax ID (NIF/NIE):</strong> <em>to be added</em></li>
          <li><strong>Activity:</strong> independent real estate advisory; coordination and project management of building &amp; renovation works carried out by third-party professionals; and investment guidance.</li>
        </ul>
        <p>Using this site means you accept this notice. Content is provided for general information; property details, prices and availability are indicative and not a binding offer.</p>

        <h2 id="privacy">Privacy policy</h2>
        <p>I collect only what you choose to send me, and use it only to reply.</p>
        <ul>
          <li><strong>Responsible:</strong> Nicolas Strebel (contact above).</li>
          <li><strong>What I collect:</strong> the name and contact details you enter in the form or send by WhatsApp, email or phone, and anything you tell me about what you're looking for.</li>
          <li><strong>Why:</strong> solely to answer your enquiry and, if you become a client, to provide the service. Legal basis: your consent and steps taken at your request.</li>
          <li><strong>Sharing:</strong> never sold or used for marketing lists. Shared only with the professionals your matter needs - a lawyer, bank or craftsman - and only when you ask me to.</li>
          <li><strong>Retention:</strong> kept only as long as needed for your enquiry or our working relationship, then deleted.</li>
          <li><strong>Your rights:</strong> access, correct, delete or restrict your data at any time - email {EMAIL}. You may also complain to the Spanish Data Protection Agency (AEPD).</li>
        </ul>
        <p>The contact form sends your message straight to me by WhatsApp or email; this website has no database and stores nothing.</p>

        <h2 id="cookies">Cookie policy</h2>
        <p>This site is deliberately light. It uses <strong>no</strong> tracking, analytics or advertising cookies, and does not profile you.</p>
        <ul>
          <li><strong>Essential only:</strong> a small preference is stored in your browser so the cookie notice doesn't reappear and to remember your language choice. It stays on your device and is never sent to a server.</li>
          <li><strong>Third parties:</strong> if you click through to WhatsApp, Google or another external service, that service applies its own cookies under its own policy.</li>
        </ul>
        <p>You can clear this storage any time in your browser settings.</p>
      </div>
    </section>'''
    return hero + body + cta_band()


# ---------------------------------------------------------------- 404
def body_404():
    return f'''    <section class="page-hero page-hero--plain">
      <div class="container" style="text-align:center;">
        <p class="eyebrow reveal">Error 404</p>
        <h1 class="display reveal" data-delay="1">This page isn't here.</h1>
        <p class="reveal" data-delay="2" style="max-width:46ch;margin-inline:auto;">The page you were looking for has moved or never existed. Here's the way back:</p>
        <div class="btn-row reveal" data-delay="3" style="justify-content:center;margin-top:1.75rem;flex-wrap:wrap;gap:0.75rem;">
          <a class="btn btn--primary" href="index.html">Home</a>
          <a class="btn btn--ghost" href="real-estate.html">Real Estate</a>
          <a class="btn btn--ghost" href="home-projects.html">Home Projects</a>
          <a class="btn btn--ghost" href="contact.html">Contact</a>
        </div>
      </div>
    </section>'''



# ---------------------------------------------------------------- TOWN PAGES (local SEO)
TOWNS = [
    ("buy-property-moraira", "Moraira", "Moraira"),
    ("buy-property-benissa", "Benissa", "Benissa"),
    ("buy-property-calpe", "Calpe", "Calpe"),
    ("buy-property-javea", "Javea", "Jávea"),
    ("buy-property-altea", "Altea", "Altea"),
]

def body_town(slug, display, region_key):
    listings = [p for p in PROPERTIES if p.get("region") == region_key]
    hero = f'''    <section class="page-hero page-hero--plain">
      <div class="container">
        <p class="breadcrumb reveal"><a href="index.html">Home</a> · <a href="real-estate.html">Real Estate</a> · Buy in {display}</p>
        <h1 class="display reveal" data-delay="1">Buy property in {display}.</h1>
        <p class="reveal" data-delay="2">Buying in {display} on the Costa Blanca North with an independent advisor on your side: whole-market search, honest viewings, legal and structural due diligence, and negotiation. And if you want to improve what you buy, the same person can coordinate the renovation or build.</p>
      </div>
    </section>'''
    if listings:
        cards = "".join(prop_card(p) for p in listings)
        grid = f'''    <section class="section">
      <div class="container">
        <div class="section-head reveal"><p class="eyebrow">In {display}</p><h2 class="mb-0">A few in {display} right now</h2></div>
        <div class="prop-grid" style="margin-top:2.5rem;">{cards}</div>
        <p class="text-center text-muted" style="margin-top:2rem;">A curated selection. Most of what I find for clients never reaches a public page.</p>
      </div>
    </section>'''
    else:
        grid = f'''    <section class="section">
      <div class="container container--reading text-center">
        <p class="text-muted">I don't have a public listing in {display} at this moment, but I search the whole market for clients, including properties that never reach a portal.</p>
        <a class="btn btn--primary" href="{wa(f'Hello Nicolas, I am looking to buy a property in {display} on the Costa Blanca.')}" target="_blank" rel="noopener" style="margin-top:1rem;">{WA_ICON}Tell me what you want in {display}</a>
      </div>
    </section>'''
    why = f'''    <section class="section section--alt">
      <div class="container container--reading">
        <p class="eyebrow reveal">Why work with me in {display}</p>
        <h2 class="reveal">Local knowledge, on your side</h2>
        <hr class="rule-accent reveal" />
        <div class="prose reveal stack"><p>I've worked this coast for twenty-five years and know {display} closely: which pockets hold value, what a fair price looks like, and what to check before you commit. You get one independent advisor rather than a different agent for every listing, and the same person can coordinate any renovation or build afterwards.</p></div>
        <div class="btn-row reveal" style="margin-top:1.5rem;"><a class="btn btn--ghost" href="real-estate.html">More on buying &amp; selling {ARROW}</a> <a class="btn btn--ghost" href="home-projects.html">Buying to renovate? {ARROW}</a></div>
      </div>
    </section>'''
    return hero + grid + why + cta_band(f"Looking to buy in {display}?", "Book a free, no-obligation consultation. I'll give you a straight read on the market and the property.")


# ---------------------------------------------------------------- HOME-PROJECTS CLUSTER (SEO)
HP_SERVICES = [
    ("new-build-villas-costa-blanca", "New-build villas", "Build a villa on the Costa Blanca.",
     "From plot and plans to a finished, furnished home. New-build villa projects on the Costa Blanca, coordinated end to end by one independent advisor.",
     ["Plot assessment, licences and architects arranged", "A trusted network of builders and trades, coordinated and supervised", "Quality control at every stage, reporting to you", "Interiors and furniture, so it's ready to live in"]),
    ("renovation-refurbishment-costa-blanca", "Renovation & refurbishment", "Renovation and refurbishment on the Costa Blanca.",
     "Reworking a dated or awkward property into something light, modern and genuinely liveable, coordinated end to end.",
     ["A clear, costed plan before anything starts", "Permits and the right trades, coordinated and supervised", "A designer's eye on layout, light and materials", "One point of responsibility from start to finish"]),
    ("interior-design-costa-blanca", "Interior design & furniture", "Interior design on the Costa Blanca.",
     "Layout, materials, furniture and the final details, shaped by a designer's eye and delivered to a calm, considered standard.",
     ["Space planning and material selection", "Furniture, lighting and decoration", "Sourcing and coordination of suppliers", "A finished home that feels right to live in, not just to photograph"]),
    ("project-coordination", "Project coordination & management", "Project management on the Costa Blanca.",
     "One accountable project manager for the whole build: permits, architects, trades and suppliers, all coordinated and reporting to you.",
     ["A single point of responsibility for timeline, budget and quality", "Architects, engineers, trades and suppliers, managed by one person", "On-site supervision, catching problems early", "Honest reporting to you, especially for owners abroad"]),
]

def body_hp_service(slug, label, h1, sub, points):
    hero = f'''    <section class="page-hero page-hero--image">
      <div class="page-hero__media"><img src="assets/images/construction/onsite-crane.jpg" alt="{label} on the Costa Blanca" width="1600" height="1200" /></div>
      <div class="page-hero__inner"><div class="container">
        <p class="breadcrumb reveal"><a href="index.html">Home</a> · <a href="home-projects.html">Home Projects</a> · {label}</p>
        <p class="eyebrow hero__eyebrow reveal" style="color:#E7D9BD">Home Projects</p>
        <h1 class="display reveal" data-delay="1">{h1}</h1>
        <p class="reveal" data-delay="2">{sub}</p>
      </div></div>
    </section>'''
    body = f'''    <section class="section">
      <div class="container container--reading">
        <p class="eyebrow eyebrow--sand reveal">What's involved</p>
        <h2 class="reveal">An independent advisor, a coordinated team</h2>
        <hr class="rule-accent rule-accent--sand reveal" />
        {ticklist(points)}
        <p class="text-muted" style="margin-top:1.5rem;">I don't operate a construction company. I coordinate a trusted, independent network of architects, builders and specialists, and stay accountable to you from the first idea to the last detail.</p>
        <div class="btn-row reveal" style="margin-top:1.5rem;"><a class="btn btn--ghost" href="home-projects.html">All home projects {ARROW}</a></div>
      </div>
    </section>'''
    return hero + body + cta_band("Have a project in mind?", "Send me a few words and a photo. I'll tell you honestly what's possible and roughly what it would take.")


# ---------------------------------------------------------------- INVESTOR'S CLUB (blog / SEO content hub)
# When real articles are written, add them to POSTS (newest first) and rebuild; each becomes
# investors-club-{slug}.html with its own Article schema, and the hub switches from the
# "coming soon" placeholder to a grid of live posts automatically.
#   post = dict(slug, title, tag, date, iso, excerpt, cover (optional), body=[paragraphs])
POSTS = []

# Topics the Club will cover - shown as "coming soon" cards while POSTS is empty (the placeholder state).
CLUB_TOPICS = [
    ("Buying", "The true cost of buying on the Costa Blanca",
     "Taxes, fees and the 10-13% that sits on top of the asking price, broken down line by line so nothing surprises you at the notary."),
    ("Investing", "Where the rental yields actually are",
     "A sober, town-by-town look at what holiday lets and long-term rentals really return here, once costs and seasonality are counted honestly."),
    ("Building", "New-build or renovation: which one pays off?",
     "When it is smarter to build from scratch, and when an older villa in the right location is the better investment."),
    ("Market", "Costa Blanca North market update",
     "How prices are genuinely moving in Moraira, Calpe, Javea and Benissa, in plain numbers rather than headlines."),
    ("Relocation", "Becoming a resident, step by step",
     "NIE, taxes and the practical hurdles that catch Northern-European buyers out, and how to clear them in the right order."),
    ("Investing", "How to read a property like an investor",
     "The handful of questions that separate a sound purchase from an expensive mistake on this coast."),
]

CLUB_INTRO = ("The Costa Blanca Investor's Club is where Nicolas shares what twenty-five years on this coast "
    "actually teaches you: how prices move town by town, what a build or a renovation really costs, where "
    "the value genuinely is, and the mistakes that catch foreign buyers out. No hype, no listings dressed "
    "up as advice - just the straight guidance he gives his own clients.")

I_PEN = '<path d="M4 20h5l9.5-9.5a2.1 2.1 0 0 0-3-3L6 17v3z"/><path d="M13.5 6.5l3 3"/>'

def post_card(tag, title, excerpt, href=None, cover=None, meta=None, soon=False):
    media_inner = (f'<img src="{cover}" alt="{title}" loading="lazy" width="640" height="400" />' if cover
        else f'<span class="post-card__ph">{icon(I_PEN, "1.4")}</span>')
    metacls = " post-card__meta--soon" if soon else ""
    meta_html = f'<span class="post-card__meta{metacls}">{meta}</span>' if meta else ""
    inner = (f'<span class="post-card__media"><span class="post-card__tag">{tag}</span>{media_inner}</span>'
             f'<span class="post-card__body"><h3 class="post-card__title">{title}</h3>'
             f'<span class="post-card__excerpt">{excerpt}</span>{meta_html}</span>')
    if href:
        return f'<a class="post-card reveal" href="{href}">{inner}</a>'
    return f'<article class="post-card reveal">{inner}</article>'

def body_investors_club():
    hero = f'''    <section class="page-hero page-hero--image">
      <div class="page-hero__media"><img src="assets/images/hero/villa-wide.webp" alt="Costa Blanca North" width="1600" height="1066" /></div>
      <div class="page-hero__inner"><div class="container">
        <p class="breadcrumb reveal"><a href="index.html">Home</a> · Investor's Club</p>
        <p class="eyebrow hero__eyebrow reveal">Insights &amp; market intelligence</p>
        <h1 class="display reveal" data-delay="1">Costa Blanca Investor's Club</h1>
        <p class="reveal" data-delay="2">Straight-talking insight on buying, building and investing on the Costa Blanca North - market reality, true costs and the opportunities worth knowing, from Nicolas Strebel.</p>
      </div></div>
    </section>'''

    intro = f'''    <section class="section">
      <div class="container container--reading">
        <p class="eyebrow reveal">What it is</p>
        <h2 class="reveal">An honest read on this market, not a sales pitch</h2>
        <hr class="rule-accent reveal" />
        <p class="lead text-muted reveal">{CLUB_INTRO}</p>
      </div>
    </section>'''

    if POSTS:
        cards = "".join(post_card(p["tag"], p["title"], p["excerpt"],
                                  href=f'investors-club-{p["slug"]}.html', cover=p.get("cover"), meta=p.get("date"))
                        for p in POSTS)
        head = '<div class="section-head reveal"><p class="eyebrow">Latest</p><h2 class="mb-0">From the Club</h2></div>'
    else:
        cards = "".join(post_card(tag, title, excerpt, soon=True, meta="Coming soon") for tag, title, excerpt in CLUB_TOPICS)
        head = ('<div class="section-head reveal"><p class="eyebrow">Coming soon</p>'
                '<h2 class="mb-0">What the Club will cover</h2>'
                '<p class="text-muted" style="max-width:60ch;margin-top:0.6rem;">The first articles are being written. '
                'Here is a taste of what is coming - practical, numbers-first pieces for anyone serious about this coast.</p></div>')

    grid = f'''    <section class="section section--alt">
      <div class="container">
        {head}
        <div class="post-grid">{cards}</div>
      </div>
    </section>'''

    join_mail = ("mailto:" + EMAIL + "?subject=" + quote("Join the Costa Blanca Investor's Club")
                 + "&body=" + quote("Hi Nicolas, please add me to the Costa Blanca Investor's Club so I receive your new articles and market updates."))
    notify = f'''    <section class="section section--navy">
      <div class="container cta-band">
        <p class="eyebrow" style="color:var(--accent-soft)">Be first to read it</p>
        <p class="display">Get new articles as they land.</p>
        <p>No spam and no selling - just genuinely useful pieces on the Costa Blanca property market, sent only when there's something worth your time.</p>
        <div class="btn-row">
          <a class="btn btn--on-dark" href="{join_mail}">Join the list</a>
          <a class="btn btn--ghost" style="color:#fff;border-color:rgba(255,255,255,0.35)" href="{WA_DEFAULT}" target="_blank" rel="noopener">{WA_ICON}Message Nicolas</a>
        </div>
      </div>
    </section>'''

    return hero + intro + grid + notify

def jsonld_post(p):
    cover = p.get("cover", "assets/images/hero/villa-wide.webp")
    return f'''  <script type="application/ld+json">
  {{
    "@context":"https://schema.org","@type":"BlogPosting",
    "headline":"{p['title']}","description":"{p['excerpt']}",
    "datePublished":"{p.get('iso', p.get('date',''))}",
    "author":{{"@type":"Person","name":"Nicolas Strebel"}},
    "publisher":{{"@type":"Person","name":"Nicolas Strebel"}},
    "image":"{SITE}/{cover}","url":"{SITE}/investors-club-{p['slug']}.html",
    "isPartOf":{{"@type":"Blog","name":"Costa Blanca Investor's Club"}}
  }}
  </script>'''

def body_post(p):
    cover = p.get("cover")
    if cover:
        herocls = "page-hero page-hero--image"
        media = f'<div class="page-hero__media"><img src="{cover}" alt="{p["title"]}" width="1600" height="900" /></div>'
    else:
        herocls = "page-hero page-hero--plain"
        media = ""
    paras = "".join(f"<p>{para}</p>" for para in p["body"])
    hero = f'''    <section class="{herocls}">
      {media}
      <div class="page-hero__inner"><div class="container">
        <p class="breadcrumb reveal"><a href="index.html">Home</a> · <a href="investors-club.html">Investor's Club</a> · {p['tag']}</p>
        <p class="eyebrow hero__eyebrow reveal">{p['tag']}</p>
        <h1 class="display reveal" data-delay="1">{p['title']}</h1>
        <p class="reveal" data-delay="2">{p.get('date','')}</p>
      </div></div>
    </section>'''
    body = f'''    <section class="section">
      <div class="container container--reading article reveal">
        {paras}
        <div class="btn-row" style="margin-top:2.25rem;"><a class="btn btn--ghost" href="investors-club.html">All articles {ARROW}</a></div>
      </div>
    </section>'''
    return hero + body + cta_band("Thinking about a move on the Costa Blanca?", "A first conversation is free and without obligation. You'll get an honest read either way.")

JSONLD_BLOG = f'''  <script type="application/ld+json">
  {{
    "@context":"https://schema.org","@type":"Blog",
    "name":"Costa Blanca Investor's Club",
    "description":"Insight on buying, building and investing on the Costa Blanca North - true costs, market updates, rental yields and honest guides from independent advisor Nicolas Strebel.",
    "url":"{SITE}/investors-club.html","inLanguage":"en",
    "author":{{"@type":"Person","name":"Nicolas Strebel"}},
    "publisher":{{"@type":"Person","name":"Nicolas Strebel"}}
  }}
  </script>'''


# ===========================================================================
#  BUILD
# ===========================================================================
def jsonld_property(p):
    img = p.get('cover') or f"{SITE}/{PLACEHOLDER_IMG}"
    locality = p.get('region', 'Costa Blanca')
    desc = _re.sub(r'"', "'", p.get('short', ''))
    offer = ""
    if p.get('price_num'):
        offer = f',\n    "offers":{{"@type":"Offer","price":"{p["price_num"]}","priceCurrency":"EUR","availability":"https://schema.org/InStock"}}'
    return f'''  <script type="application/ld+json">
  {{
    "@context":"https://schema.org","@type":"SingleFamilyResidence","name":"{p['title']}",
    "description":"{desc}","image":"{img}",
    "address":{{"@type":"PostalAddress","addressLocality":"{locality}","addressRegion":"Alicante","addressCountry":"ES"}},
    "numberOfBedrooms":{p['beds']},"numberOfBathroomsTotal":{p['baths']}{offer}
  }}
  </script>'''

FAQ_JSONLD = '''  <script type="application/ld+json">
  {
    "@context":"https://schema.org","@type":"FAQPage","mainEntity":[
      {"@type":"Question","name":"What does a buyer's advisor do?","acceptedAnswer":{"@type":"Answer","text":"A professional who represents the buyer's interests through the entire purchase - searching the whole market, vetting properties, handling legal due diligence and negotiating on the buyer's behalf."}},
      {"@type":"Question","name":"How is Nicolas Strebel different from a typical estate agent?","acceptedAnswer":{"@type":"Answer","text":"Nicolas works across the whole market rather than pushing a single listing, takes on only a few clients at a time, and gives an honest assessment - including advising against a purchase when it is not right."}},
      {"@type":"Question","name":"What are the additional costs of buying property on the Costa Blanca?","acceptedAnswer":{"@type":"Answer","text":"Taxes and purchase costs typically add about 10–13% above the purchase price, and more for a new build. A lawyer - not the notary - protects the buyer's interests."}}
    ]
  }
  </script>'''

def main():
    # HOME
    page("index.html",
         "Nicolas Strebel - Real Estate, Construction & Investment | Costa Blanca",
         "Independent real estate & building consultant on the Costa Blanca North. Honest guidance for buying, building, selling & investing. 25+ years and 500+ properties sold.",
         body_home(), "index.html", extra_head=JSONLD_BUSINESS)

    # HOME - ALTERNATE CONCEPT (mockup only; the live home stays index.html)
    page("index-alt.html",
         "Which path is right for you? - Nicolas Strebel | Costa Blanca",
         "Alternate homepage concept for Nicolas Strebel - independent real estate, construction & investment advisor on the Costa Blanca North. Choose your path.",
         body_home_alt(), "index.html", extra_head=HOME_ALT_CSS + JSONLD_BUSINESS)

    # HOME - CONCEPT 3 (mockup only; cinematic banner hero + service rail)
    page("index-alt2.html",
         "Found, built, and looked after - Nicolas Strebel | Costa Blanca",
         "Third homepage concept for Nicolas Strebel - a single trusted partner for buying, selling, building, renovating and investing on the Costa Blanca North.",
         body_home_v3(), "index.html", extra_head=HOME_V3_CSS + JSONLD_BUSINESS)

    # HOME - CONCEPT 4 (mockup only; editorial split-frame, numbered index)
    page("index-alt3.html",
         "From first viewing to finished home - Nicolas Strebel | Costa Blanca",
         "Fourth homepage concept for Nicolas Strebel - an editorial split layout with a numbered service index, for buying, selling, building, renovating and investing on the Costa Blanca North.",
         body_home_v4(), "index.html", extra_head=HOME_V4_CSS + JSONLD_BUSINESS)

    # REAL ESTATE (division hub)
    page("real-estate.html",
         "Real Estate Costa Blanca - Buy, Sell, Source & Invest | Nicolas Strebel",
         "Costa Blanca real estate with an independent advisor on your side: buying, selling, property sourcing and investment across Moraira, Benissa, Calpe, Javea and Altea. 500+ transactions.",
         body_real_estate(), "real-estate.html",
         og_image="assets/images/hero/villa-wide.webp")

    # BUYING & SELLING
    page("buyers-advisor.html",
         "Buy & Sell Property Costa Blanca - Moraira, Benissa, Calpe, Javea | Nicolas Strebel",
         "Buying or selling property on the Costa Blanca with an advisor on your side: whole-market search, honest valuation, qualified buyers, due diligence and negotiation - start to finish.",
         body_buyers(), "real-estate.html", extra_head=FAQ_JSONLD,
         og_image="assets/images/hero/villa-wide.webp")

    # HOME PROJECTS (division hub - new-build, renovation, interiors, coordination)
    page("home-projects.html",
         "Home Projects Costa Blanca - Build a Villa, Renovation & Project Management | Nicolas Strebel",
         "Build a villa, renovate or refurbish on the Costa Blanca: new-build villa construction, renovation & refurbishment, interior design, furniture and full project management. 50+ projects completed.",
         body_construction(), "home-projects.html",
         og_image="assets/images/construction/onsite-crane.jpg")

    # INVESTING (nested under Real Estate)
    page("investing.html",
         "Property Investment Costa Blanca | Nicolas Strebel",
         "A sober, honest assessment of property investment on the Costa Blanca - true all-in costs, rental and resale reality, renovation upside, and the risks to avoid.",
         body_invest(), "real-estate.html",
         og_image="assets/images/hero/villa-wide.webp")

    # PROPERTIES
    page("properties.html",
         "Curated Properties for Sale on the Costa Blanca | Nicolas Strebel",
         "A small, hand-picked selection of villas and apartments in Calpe and across the Costa Blanca North - chosen and vetted personally, not a faceless portal.",
         body_properties(), "properties.html")

    # PROPERTY DETAILS - clear stale property-*.html first so renamed listings don't linger
    import glob as _glob
    _current = {p["file"] for p in PROPERTIES}
    for _old in _glob.glob(os.path.join(ROOT, "property-*.html")):
        if os.path.basename(_old) not in _current:
            os.remove(_old)
    for p in PROPERTIES:
        page(p["file"],
             f"{p['title']} - {p['price']} | Nicolas Strebel",
             p["short"],
             body_property(p), "properties.html",
             extra_head=jsonld_property(p),
             og_image=p.get("cover") or PLACEHOLDER_IMG)

    # ABOUT
    page("about.html",
         "About Nicolas Strebel - Independent Real Estate & Home Projects Advisor, Costa Blanca",
         "From Fashion Design in Milan to 25 years across Costa Blanca property and building projects. Independent advisor since 2024, coordinating trusted professionals. 5 languages, 500+ sales.",
         body_about(), "about.html", extra_head=JSONLD_PERSON,
         og_image="assets/images/nicolas/portrait-studio.jpg")

    # CONTACT
    page("contact.html",
         "Contact Nicolas Strebel | WhatsApp +34 670 260 445",
         "Talk to Nicolas Strebel directly - WhatsApp, phone or email. Independent buyer's advisor and building consultant, Teulada, Costa Blanca North.",
         body_contact(), "contact.html", extra_head=JSONLD_BUSINESS)

    # (The standalone Story page was removed - the About page covers Nicolas's background.
    #  story.html 301-redirects to about.html via _redirects.)

    # LEGAL & PRIVACY
    page("legal.html",
         "Legal Notice, Privacy & Cookies | Nicolas Strebel",
         "Legal notice, privacy policy and cookie policy for nicolasstrebel.com - plain-language and GDPR-aware.",
         body_legal(), "legal.html")

    # 404 (Cloudflare Pages serves this for not-found - kills the soft-404)
    page("404.html",
         "Page not found | Nicolas Strebel",
         "That page has moved or never existed. Back to Real Estate, Home Projects or home.",
         body_404(), "index.html")

    # TOWN PAGES (local SEO: Buy Property {Town})
    for slug, display, region_key in TOWNS:
        page(f"{slug}.html",
             f"Buy Property {display}, Costa Blanca | Nicolas Strebel",
             f"Buy property in {display} on the Costa Blanca North with an independent advisor on your side: whole-market search, honest valuation, due diligence and negotiation. 25 years, 500+ transactions.",
             body_town(slug, display, region_key), "real-estate.html",
             og_image="assets/images/hero/villa-wide.webp")

    # HOME-PROJECTS CLUSTER (SEO: build a villa / new build / renovation / interior design / project management)
    for slug, label, h1, sub, points in HP_SERVICES:
        page(f"{slug}.html",
             f"{label} Costa Blanca | Nicolas Strebel",
             sub,
             body_hp_service(slug, label, h1, sub, points), "home-projects.html",
             og_image="assets/images/construction/onsite-crane.jpg")

    # INVESTOR'S CLUB (blog / content hub - placeholder now, scales as posts are added)
    page("investors-club.html",
         "Costa Blanca Investor's Club - Property Market Insights | Nicolas Strebel",
         "Insight on buying, building and investing on the Costa Blanca North: true costs, market updates, rental yields and honest guides from independent advisor Nicolas Strebel.",
         body_investors_club(), "investors-club.html", extra_head=JSONLD_BLOG,
         og_image="assets/images/hero/villa-wide.webp")

    # INVESTOR'S CLUB POSTS (added to POSTS as they're written)
    for p in POSTS:
        page(f"investors-club-{p['slug']}.html",
             f"{p['title']} | Costa Blanca Investor's Club",
             p["excerpt"],
             body_post(p), "investors-club.html", extra_head=jsonld_post(p),
             og_image=p.get("cover", "assets/images/hero/villa-wide.webp"))

    # SITEMAP (generated from every real page built above)
    _urls = "".join(f"  <url><loc>{u}</loc><changefreq>weekly</changefreq></url>\n" for u in SITEMAP_URLS)
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                f"{_urls}</urlset>\n")
    print(f"wrote sitemap.xml ({len(SITEMAP_URLS)} urls)")

    # Localised sites (de/nl/fr) - generated from the English pages when translations exist.
    # Isolated as a subprocess so a missing lxml / translations never breaks the English build.
    try:
        import subprocess, sys
        tools = os.path.join(ROOT, "tools")
        if os.path.exists(os.path.join(tools, "i18n", "translations.json")):
            # CRM listing-text map (DE/NL/FR) if per-language data has been synced
            if os.path.exists(os.path.join(ROOT, "data", "sooprema-listings-de.json")):
                subprocess.run([sys.executable, os.path.join(tools, "i18n_listings.py")], check=True)
            subprocess.run([sys.executable, os.path.join(tools, "i18n_build.py")], check=True)
    except Exception as e:
        print("i18n step skipped:", e)

    print("\\nBuild complete.")

if __name__ == "__main__":
    main()
