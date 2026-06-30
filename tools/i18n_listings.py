#!/usr/bin/env python3
"""
i18n step 2b - build tools/i18n/listing_translations.json: a map of English listing TEXT
(title / summary / description paragraphs) -> {de,nl,fr}, taken from the CRM's own
multilingual data (data/sooprema-listings-<lang>.json), paired by listing id.

These are merged into the translation lookup so the localized pages show German/Dutch/French
property titles and descriptions, not just translated chrome.
"""
import json, re, html as H, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT / "tools" / "i18n" / "listing_translations.json"
LANGS = ["de", "nl", "fr"]


def load(lang):
    f = DATA / ("sooprema-listings.json" if lang == "en" else f"sooprema-listings-{lang}.json")
    if not f.exists():
        return {}
    return {str(i["id"]): i for i in json.loads(f.read_text(encoding="utf-8")).get("items", [])}


def norm(s):
    return re.sub(r"\s+", " ", H.unescape(s or "")).strip()


def title_of(it):
    # mirrors build._map_listing: cleaned, unescaped, quote-normalized (NOT html-escaped)
    return norm(it.get("salesTitle") or "").replace('"', "”")


def paras_of(it):
    raw = it.get("salesDescription") or ""
    txt = re.sub(r"(?i)</p\s*>|<br\s*/?>|</h[1-6]\s*>", "\n", H.unescape(raw))
    txt = re.sub(r"(?i)<li[^>]*>", "\n- ", txt)
    txt = H.unescape(re.sub(r"<[^>]+>", "", txt))
    return [p.strip() for p in re.split(r"\n\s*\n|\n", txt) if p.strip()]


def main():
    en = load("en")
    langs = {L: load(L) for L in LANGS}
    tr = {}

    def add(en_str, vals):
        en_str = norm(en_str)
        if len(en_str) < 2 or not re.search(r"[A-Za-zÀ-ÿ]", en_str):
            return
        if any(vals.get(L) for L in LANGS):
            tr.setdefault(en_str, {}).update({L: norm(v) for L, v in vals.items() if v})

    paired = 0
    for pid, e in en.items():
        present = {L: langs[L].get(pid) for L in LANGS}
        if not any(present.values()):
            continue
        paired += 1
        # title (when the EN listing has no title, build.py generates "<type> for sale in <city>";
        # map that generated string to the CRM's localized title where one exists)
        en_title = title_of(e)
        if en_title:
            add(en_title, {L: title_of(o) for L, o in present.items() if o})
        else:
            typ = (e.get("typeName") or "Property").strip()
            city = (e.get("cityName") or "").strip()
            gen = (f"{typ} for sale in {city}" if city else f"{typ} for sale on the Costa Blanca")
            add(gen, {L: title_of(o) for L, o in present.items() if o and title_of(o)})
        # summary
        if e.get("salesSummary"):
            add(e["salesSummary"], {L: o.get("salesSummary") for L, o in present.items() if o})
        # description paragraphs (only when paragraph counts line up)
        ep = paras_of(e)
        for i, p in enumerate(ep):
            vals = {}
            for L, o in present.items():
                if not o:
                    continue
                lp = paras_of(o)
                if len(lp) == len(ep):
                    vals[L] = lp[i]
            add(p, vals)

    OUT.write_text(json.dumps(tr, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"paired listings: {paired} | listing text strings mapped: {len(tr)}")


if __name__ == "__main__":
    main()
