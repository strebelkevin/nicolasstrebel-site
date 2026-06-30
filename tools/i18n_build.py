#!/usr/bin/env python3
"""
i18n step 3 - generate /de/, /nl/, /fr/ versions of the core pages from the built English
pages, using tools/i18n/translations.json. The English site (root) is left in place and gets
hreflang tags + a working language switcher. Listing DATA in cards is left as-is for now
(handled from the CRM's own translations in a later pass); only UI/marketing copy is translated.

Run AFTER build.py.  Output: de/<page>.html, nl/<page>.html, fr/<page>.html  + updated root pages.
"""
import os, re, json, glob, pathlib
from lxml import html as LH
from lxml import etree

ROOT = pathlib.Path(__file__).resolve().parent.parent
I18N = ROOT / "tools" / "i18n"
SITE = "https://nicolasstrebel.com"
LANGS = ["de", "nl", "fr"]               # translated languages (en = root)
LANG_LABEL = {"en": "English", "de": "Deutsch", "nl": "Nederlands", "fr": "Français"}
LANG_CODE = {"en": "EN", "de": "DE", "nl": "NL", "fr": "FR"}

CORE = (["index.html", "real-estate.html", "home-projects.html", "buyers-advisor.html",
         "investing.html", "properties.html", "about.html", "contact.html",
         "investors-club.html", "legal.html", "404.html"]
        + [os.path.basename(p) for p in glob.glob(str(ROOT / "buy-property-*.html"))]
        + ["new-build-villas-costa-blanca.html", "renovation-refurbishment-costa-blanca.html",
           "interior-design-costa-blanca.html", "project-coordination.html"])
CORE_SET = set(CORE)

SKIP_TAGS = {"script", "style", "svg", "noscript"}

# Merge all translation sources: UI/marketing copy + property-page chrome + CRM listing text.
TR = json.loads((I18N / "translations.json").read_text(encoding="utf-8"))
for _f in ("chrome_listing_tr.json", "listing_translations.json"):
    _p = I18N / _f
    if _p.exists():
        for k, v in json.loads(_p.read_text(encoding="utf-8")).items():
            TR.setdefault(re.sub(r"\s+", " ", k).strip(), {}).update(v)

def unit(word, lang):
    e = TR.get(word)
    return e.get(lang) if (e and e.get(lang)) else word

def localize_units(htmlstr, lang):
    """Translate the few number-bearing labels that can't be dict-keyed (e.g. '4 bed', '+8 photos')."""
    def rep(pat, fn):
        return re.sub(pat, fn, htmlstr)
    htmlstr = re.sub(r"(\d+)\s+bed\b", lambda m: f"{m.group(1)} {unit('bed', lang)}", htmlstr)
    htmlstr = re.sub(r"(\d+)\s+bath\b", lambda m: f"{m.group(1)} {unit('bath', lang)}", htmlstr)
    htmlstr = re.sub(r"\+(\d+)\s+photos\b", lambda m: f"+{m.group(1)} {unit('photos', lang)}", htmlstr)
    htmlstr = re.sub(r"\bBuilt in (\d{4})", lambda m: f"{unit('Built in', lang)} {m.group(1)}", htmlstr)
    htmlstr = re.sub(r"\bRenovated in (\d{4})", lambda m: f"{unit('Renovated in', lang)} {m.group(1)}", htmlstr)
    htmlstr = re.sub(r"\bBuilt (\d[\d.,]* m²)", lambda m: f"{unit('Built', lang)} {m.group(1)}", htmlstr)
    htmlstr = re.sub(r"\bPlot (\d[\d.,]* m²)", lambda m: f"{unit('Plot', lang)} {m.group(1)}", htmlstr)
    htmlstr = re.sub(r"\bEnergy rating ([A-G])\b", lambda m: f"{unit('Energy rating', lang)} {m.group(1)}", htmlstr)
    return htmlstr


def tr_get(s, lang):
    s2 = re.sub(r"\s+", " ", s).strip()
    e = TR.get(s2)
    return e.get(lang) if (e and e.get(lang)) else None


def repl_text(val, lang):
    if not val or not val.strip():
        return None
    lead = val[:len(val) - len(val.lstrip())]
    trail = val[len(val.rstrip()):]
    core = val.strip()
    t = tr_get(core, lang)
    if t:
        return lead + t + trail
    # handle a "<separator> <translatable>" tail, e.g. breadcrumb "· {property title}"
    m = re.match(r"^([·/|–—-]\s+)(.+)$", core)
    if m:
        t2 = tr_get(m.group(2), lang)
        if t2:
            return lead + m.group(1) + t2 + trail
    return None


def page_path(page, lang):
    """URL path for a page in a given language."""
    base = "" if page == "index.html" else page
    return ("/" + base) if lang == "en" else (f"/{lang}/" + base)


def rewrite_href(href, lang):
    if not href:
        return href
    if href.startswith(("http://", "https://", "mailto:", "tel:", "#", "data:")):
        return href
    # split anchor
    anchor = ""
    if "#" in href:
        href, anchor = href.split("#", 1)
        anchor = "#" + anchor
    if href == "":
        return anchor or href
    if href.startswith(("assets/", "css/", "js/")):
        return "/" + href + anchor
    if href.endswith(".html"):
        return page_path(href, lang) + anchor      # all real pages are localized -> same language
    return href + anchor


SWITCH_SVG = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg>'

def build_switcher(page, cur_lang):
    opts = []
    for L in ["en"] + LANGS:
        href = page_path(page, L)
        cur = ' aria-current="true"' if L == cur_lang else ""
        opts.append(f'<a href="{href}"{cur}>{LANG_LABEL[L]} <small>{LANG_CODE[L]}</small></a>')
    return (f'<button class="lang-toggle" type="button" aria-haspopup="true" aria-expanded="false" data-lang-toggle>'
            f'{LANG_CODE[cur_lang]} {SWITCH_SVG}</button>'
            f'<div class="lang__menu" data-lang-menu>{"".join(opts)}</div>')


def set_head(doc, page, lang):
    head = doc.find(".//head")
    # remove any existing hreflang alternates we may have added before
    for a in head.xpath("link[@rel='alternate'][@hreflang]"):
        head.remove(a)
    # canonical + og:url -> this language's URL
    url = SITE + page_path(page, lang)
    for c in head.xpath("link[@rel='canonical']"):
        c.set("href", url)
    for o in head.xpath("meta[@property='og:url']"):
        o.set("content", url)
    # hreflang alternates for every language + x-default (English)
    frag = []
    for L in ["en"] + LANGS:
        frag.append(f'<link rel="alternate" hreflang="{L}" href="{SITE + page_path(page, L)}" />')
    frag.append(f'<link rel="alternate" hreflang="x-default" href="{SITE + page_path(page, "en")}" />')
    for node in LH.fragments_fromstring("".join(frag)):
        head.append(node)


def process(root, page, lang):
    # root is the <html> element returned by LH.fromstring
    root.set("lang", lang)
    # translate text + attributes
    if lang != "en":
        for t in root.xpath("//title"):
            nt = repl_text(t.text, lang)
            if nt: t.text = nt
        for m in root.xpath("//meta[@name='description']|//meta[@property='og:title']|//meta[@property='og:description']"):
            t = tr_get(m.get("content", ""), lang)
            if t: m.set("content", t)
        for el in root.iter():
            if not isinstance(el.tag, str) or el.tag in SKIP_TAGS:
                continue
            for a in ("alt", "placeholder", "title", "aria-label"):
                v = el.get(a)
                if v:
                    t = tr_get(v, lang)
                    if t: el.set(a, t)
            nt = repl_text(el.text, lang)
            if nt is not None: el.text = nt
            tt = repl_text(el.tail, lang)
            if tt is not None: el.tail = tt
    # rewrite links (translated pages only; English root keeps relative links)
    if lang != "en":
        for el in root.xpath("//*[@href]"):
            el.set("href", rewrite_href(el.get("href"), lang))
        for el in root.xpath("//*[@src]"):
            src = el.get("src")
            if src and src.startswith(("assets/", "css/", "js/")):
                el.set("src", "/" + src)
        # <source src> inside <video>
        for el in root.xpath("//source[@src]"):
            src = el.get("src")
            if src and src.startswith(("assets/", "css/", "js/")):
                el.set("src", "/" + src)
    # language switcher (all pages, incl English)
    for lang_div in root.xpath("//div[contains(@class,'lang')][.//*[@data-lang-toggle]]"):
        for ch in list(lang_div):
            lang_div.remove(ch)
        for node in LH.fragments_fromstring(build_switcher(page, lang)):
            lang_div.append(node)
    # head: canonical / og:url / hreflang
    set_head(root, page, lang)


def render(root):
    return "<!DOCTYPE html>\n" + LH.tostring(root, encoding="unicode", method="html")


def main():
    # All localizable pages: core + every property detail page (listing text comes from the CRM map)
    PAGES = CORE + sorted(os.path.basename(p) for p in glob.glob(str(ROOT / "property-*.html")))
    # English root pages: add hreflang + working switcher (no text/link change)
    for page in PAGES:
        fp = ROOT / page
        if not fp.exists():
            continue
        doc = LH.fromstring(fp.read_text(encoding="utf-8"))
        process(doc, page, "en")
        fp.write_text(render(doc), encoding="utf-8")
    # Translated languages
    for lang in LANGS:
        d = ROOT / lang
        d.mkdir(exist_ok=True)
        n = 0
        for page in PAGES:
            fp = ROOT / page
            if not fp.exists():
                continue
            doc = LH.fromstring(fp.read_text(encoding="utf-8"))
            process(doc, page, lang)
            (d / page).write_text(localize_units(render(doc), lang), encoding="utf-8")
            n += 1
        print(f"  {lang}/: wrote {n} pages")
    # Add the localized URLs to the sitemap (build.py wrote the English ones)
    sm = ROOT / "sitemap.xml"
    if sm.exists():
        content = sm.read_text(encoding="utf-8")
        extra = ""
        for lang in LANGS:
            for page in PAGES:
                if (ROOT / lang / page).exists():
                    extra += f"  <url><loc>{SITE}{page_path(page, lang)}</loc><changefreq>weekly</changefreq></url>\n"
        if "</urlset>" in content and extra:
            sm.write_text(content.replace("</urlset>", extra + "</urlset>"), encoding="utf-8")
            print(f"  sitemap: +{extra.count('<url>')} localized URLs")
    print("i18n build complete.")


if __name__ == "__main__":
    main()
