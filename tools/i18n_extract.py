#!/usr/bin/env python3
"""
i18n step 1 - extract translatable units from the built English pages.

Writes tools/i18n/units.json: a sorted list of distinct human strings (text nodes +
translatable attributes) that make up the site's UI and marketing copy. Listing DATA
(property cards / detail) is skipped on purpose - that comes from the CRM's own
DE/NL/FR translations in the build, not from this static layer.
"""
import os, re, json, glob, pathlib
from lxml import html as LH

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "tools" / "i18n"
OUT.mkdir(parents=True, exist_ok=True)

# Pages whose chrome/copy we translate here. Property detail pages are handled in the build
# (CRM-translated data); they are NOT in this list.
CORE = (["index.html", "real-estate.html", "home-projects.html", "buyers-advisor.html",
         "investing.html", "properties.html", "about.html", "contact.html",
         "investors-club.html", "legal.html", "404.html"]
        + [os.path.basename(p) for p in glob.glob(str(ROOT / "buy-property-*.html"))]
        + ["new-build-villas-costa-blanca.html", "renovation-refurbishment-costa-blanca.html",
           "interior-design-costa-blanca.html", "project-coordination.html"])

# Containers whose inner text is listing DATA (translated via the CRM, not here).
SKIP_CLASS = re.compile(r"\b(prop-card|listing|prop-grid)\b")
ATTRS = ("alt", "placeholder", "title", "aria-label", "content")
SKIP_TAGS = {"script", "style", "svg", "noscript"}

def translatable(s):
    s = (s or "").strip()
    if len(s) < 2 or not re.search(r"[A-Za-zÀ-ÿ]", s):
        return False
    if s.startswith(("http", "assets/", "css/", "js/", "#", "mailto:", "tel:", "+34")):
        return False
    if re.fullmatch(r"[\d\s.,+%€·/–-]+", s):   # pure numbers / separators
        return False
    return True

def in_skip(el):
    p = el
    while p is not None:
        cls = p.get("class") or ""
        if SKIP_CLASS.search(cls):
            return True
        p = p.getparent()
    return False

units = set()
per_page = {}
for fn in CORE:
    fp = ROOT / fn
    if not fp.exists():
        continue
    doc = LH.fromstring(fp.read_text(encoding="utf-8"))
    found = set()
    # <title> + meta description + og
    for t in doc.xpath("//title"):
        if t.text and translatable(t.text):
            found.add(t.text.strip())
    for m in doc.xpath("//meta[@name='description']|//meta[@property='og:title']|//meta[@property='og:description']"):
        c = m.get("content")
        if c and translatable(c):
            found.add(c.strip())
    for el in doc.iter():
        if not isinstance(el.tag, str) or el.tag in SKIP_TAGS:
            continue
        if in_skip(el):
            continue
        for a in ATTRS:
            if a == "content":
                continue
            v = el.get(a)
            if v and translatable(v):
                found.add(v.strip())
        for txt in (el.text, el.tail):
            if txt and translatable(txt):
                found.add(re.sub(r"\s+", " ", txt).strip())
    per_page[fn] = sorted(found)
    units |= found

units = sorted(units)
(OUT / "units.json").write_text(json.dumps(units, ensure_ascii=False, indent=1), encoding="utf-8")
(OUT / "per_page.json").write_text(json.dumps(per_page, ensure_ascii=False, indent=1), encoding="utf-8")
print("pages:", len(per_page), "| distinct translatable units:", len(units))
