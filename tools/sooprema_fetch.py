#!/usr/bin/env python3
"""
Sooprema Frontend API client + secure credential handling for nicolasstrebel.com.

SECURITY MODEL  (key is SERVER-SIDE ONLY)
-----------------------------------------
- The API *secret key* is NEVER stored in the website project or in anything we deploy.
- It lives only in ~/.config/sooprema/credentials.json  (chmod 600), or in environment
  variables (for CI / server builds). The browser never sees it.
- This script runs on the build machine. It fetches listing DATA from the CRM and writes
  only the (public) listing data to a JSON file. The static site is generated from that
  file - so the deployed site contains listings, never the key.

Credentials are read in this priority:
  1. Env vars: SOOPREMA_AGENCY, SOOPREMA_PUBLIC_KEY, SOOPREMA_SECRET_KEY, SOOPREMA_URL, SOOPREMA_LANG
  2. ~/.config/sooprema/credentials.json

Commands:
  import-creds <config.php>      one-time: copy creds from the SDK's config.php into the secure store
  test                           live test: fetch a few properties and print a summary (no secrets shown)
  sync [--out FILE] [--per N]    fetch ALL properties -> JSON file (public listing data only)
"""
import os, sys, json, time, hmac, hashlib, ssl, re, pathlib
import urllib.request, urllib.parse, urllib.error

CRED_PATH = pathlib.Path.home() / ".config" / "sooprema" / "credentials.json"


def load_creds():
    env = {
        "agency": os.environ.get("SOOPREMA_AGENCY"),
        "publicKey": os.environ.get("SOOPREMA_PUBLIC_KEY"),
        "secretKey": os.environ.get("SOOPREMA_SECRET_KEY"),
        "url": os.environ.get("SOOPREMA_URL"),
        "language": os.environ.get("SOOPREMA_LANG", "es"),
    }
    if env["agency"] and env["publicKey"] and env["secretKey"] and env["url"]:
        return env
    if CRED_PATH.exists():
        return json.loads(CRED_PATH.read_text())
    sys.exit("No credentials found. Run: sooprema_fetch.py import-creds <config.php>, "
             "or set SOOPREMA_* env vars.")


def import_creds(config_php_path):
    txt = pathlib.Path(config_php_path).read_text(errors="ignore")

    def grab(key):
        m = re.search(r"'%s'\s*=>\s*'([^']*)'" % re.escape(key), txt)
        return m.group(1) if m else None

    creds = {k: grab(k) for k in ("agency", "publicKey", "secretKey", "url", "language")}
    creds["language"] = creds.get("language") or "es"
    missing = [k for k in ("agency", "publicKey", "secretKey", "url") if not creds[k]]
    if missing:
        sys.exit("config.php is missing: " + ", ".join(missing))

    CRED_PATH.parent.mkdir(parents=True, exist_ok=True)
    CRED_PATH.write_text(json.dumps(creds, indent=2))
    os.chmod(CRED_PATH, 0o600)
    try:
        os.chmod(CRED_PATH.parent, 0o700)
    except OSError:
        pass
    pk = creds["publicKey"]
    print("Stored credentials securely at %s (chmod 600)." % CRED_PATH)
    print("  agency:    %s" % creds["agency"])
    print("  url:       %s" % creds["url"])
    print("  publicKey: %s...%s" % (pk[:6], pk[-4:]))
    print("  secretKey: [stored, hidden - never printed, never deployed]")


def endpoint(path, args=None, creds=None, timeout=30):
    creds = creds or load_creds()
    args = dict(args or {})
    args.setdefault("agency", creds["agency"])
    args.setdefault("language", creds.get("language", "es"))

    ts = str(int(time.time()))
    digest = hmac.new(creds["secretKey"].encode(), ts.encode(), hashlib.sha256).hexdigest()
    headers = {
        "Authorization": "Basic %s:%s" % (creds["publicKey"], digest),
        "X-Timestamp": ts,
        "Accept": "application/json",
    }
    url = creds["url"].rstrip("/") + "/" + path.lstrip("/")
    body = urllib.parse.urlencode(args).encode()
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    ctx = ssl.create_default_context()  # SSL verification ON (the PHP sample disabled it; we don't)
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"response": {"status": "error", "reason": "HTTP %s: %s" % (e.code, e.read().decode("utf-8", "ignore")[:300])}}
    except Exception as e:
        return {"response": {"status": "error", "reason": "%s: %s" % (type(e).__name__, e)}}


def is_error(d):
    try:
        return d.get("response", {}).get("status") != "ok"
    except Exception:
        return True


def _results(d):
    return d.get("response", {}).get("results", {}) or {}


def cmd_test():
    creds = load_creds()
    print("Calling %sproperties  (agency=%s)\n" % (creds["url"], creds["agency"]))
    d = endpoint("/properties", {"perPage": 3, "image": "special", "images": "source"}, creds=creds)
    if is_error(d):
        print("API ERROR:", d.get("response", {}).get("reason"))
        sys.exit(1)
    res = _results(d)
    info = res.get("info", {})
    items = res.get("items", []) or ([res["item"]] if res.get("item") else [])
    print("OK - status:", d["response"]["status"], "| time:", d["response"].get("time"))
    print("TOTAL listings in CRM:", info.get("total"), "| returned this page:", info.get("count"))
    if items:
        it = items[0]
        print("\nSample listing - available fields (%d):" % len(it))
        print(", ".join(sorted(it.keys())))
        def g(k):
            v = it.get(k)
            return v if not isinstance(v, (list, dict)) else "<%s>" % type(v).__name__
        print("\nSample values:")
        for k in ("id", "salesReference", "salesTitle", "salesPrice", "cityName", "areaName",
                  "bedrooms", "bathrooms", "buildSize", "plotSize", "salesLabel", "energyCertificate", "latlng"):
            if k in it:
                print("  %-18s %s" % (k + ":", g(k)))
        img = it.get("image")
        imgs = it.get("images")
        print("\nMain image (special):", (img if isinstance(img, str) else json.dumps(img)[:120]) if img else "(none)")
        if isinstance(imgs, list):
            print("Image list (source): %d images; first: %s" % (len(imgs), imgs[0] if imgs else "-"))
        elif imgs:
            print("Images field:", json.dumps(imgs)[:200])


# Public-facing fields ONLY. The CRM also returns internal data (commission, privateNote,
# contact phones/emails, keys, visit annotations, owner info). We never download those:
# requesting an explicit `fields` allowlist means the sensitive fields never leave the CRM.
PUBLIC_FIELDS = ",".join([
    "id", "created", "modified", "sales", "salesType", "sold", "booked",
    "salesReference", "salesPrice", "salesNoPrice", "salesOffers", "salesLabel", "salesLabelColor",
    "salesFeatured", "salesHome", "salesFirstPosition",
    "salesTitle", "salesDescription", "salesSummary", "salesSlug",
    "bedrooms", "bathrooms", "toilets", "lounges",
    "buildSize", "plotSize", "usefulSize", "terraceSize", "buildYear", "renovationYear", "floors",
    "typeName", "cityName", "areaName", "provinceName",
    "poolName", "orientationName", "viewName", "heatingName", "kitchenName", "furnituresTypeName",
    "equipment", "features", "distances", "ibi", "ibiPeriod",
    "energyCertificate", "energyCertificateConsumption", "latlng", "video", "tour360",
])

# The public site is English, so pull the English title/description/slug for every listing.
SITE_LANG = "en"


def cmd_sync(out="data/sooprema-listings.json", per=50):
    creds = load_creds()
    all_items, page = [], 1
    while True:
        d = endpoint("/properties", {"page": page, "perPage": per, "sales": 1, "language": SITE_LANG,
                                      "fields": PUBLIC_FIELDS, "image": "special", "images": "source"}, creds=creds)
        if is_error(d):
            sys.exit("API error on page %d: %s" % (page, d.get("response", {}).get("reason")))
        res = _results(d)
        items = res.get("items", []) or []
        all_items.extend(items)
        info = res.get("info", {})
        total = info.get("total", 0)
        print("  page %d -> +%d (%d/%s)" % (page, len(items), len(all_items), total))
        if not items or len(all_items) >= (total or 0) or page > 200:
            break
        page += 1
    outp = pathlib.Path(out)
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(json.dumps({"fetched": int(time.time()), "count": len(all_items), "items": all_items},
                               ensure_ascii=False, indent=1))
    print("Wrote %d listings to %s (public data only - no credentials)." % (len(all_items), outp))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
    cmd = sys.argv[1]
    if cmd == "import-creds":
        import_creds(sys.argv[2])
    elif cmd == "test":
        cmd_test()
    elif cmd == "sync":
        out, per = "data/sooprema-listings.json", 50
        a = sys.argv[2:]
        if "--out" in a:
            out = a[a.index("--out") + 1]
        if "--per" in a:
            per = int(a[a.index("--per") + 1])
        cmd_sync(out, per)
    else:
        sys.exit("Unknown command: %s" % cmd)


if __name__ == "__main__":
    main()
