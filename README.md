# nicolasstrebel.com

Marketing website for **Nicolas Strebel** — independent buyer's advisor (Personal
Shopper Inmobiliario) & building consultant on the Costa Blanca North, Spain.

Plain, static **HTML + CSS + vanilla JS**. No build step, no dependencies. Deploy by
uploading this folder to Netlify, Vercel, Cloudflare Pages, GitHub Pages, or any host.

## Pages (all built)
| File | Page |
|---|---|
| `index.html` | Home |
| `buyers-advisor.html` | Buyer's Advisor (the PSI concept, agent-vs-advisor, process, honest costs) |
| `construction.html` | Construction & Renovation |
| `properties.html` | Curated properties |
| `property-villa-newbuild-calpe.html` | New-build villa, Calpe — €1,300,000 |
| `property-villa-calpe.html` | Villa, Calpe — €499,000 |
| `property-apartment-calpe.html` | Apartment, La Fossa, Calpe — €399,000 |
| `about.html` | Nicolas's story, principles, languages |
| `contact.html` | WhatsApp-forward contact + form |
| `styleguide.html` | Design-system preview (not linked, `noindex`) |

## Preview locally
```bash
cd nicolasstrebel-site
python3 -m http.server 8000
# open http://localhost:8000/index.html
```
> Open it via the server URL, **not** by double-clicking the file — `file://` blocks the
> stylesheet and it looks unstyled.

## What's real vs. placeholder
- **All photography is real**, pulled from Nicolas's own sites and the photos you provided.
  Portraits, the on-site construction shots, and the three Calpe listings (with real
  prices, sizes, beds/baths) all come from `nicolasstrebel.com` / `nicolas-strebel.paagees.com`.
- **No AI-generated images are used anywhere.**
- **Testimonials are placeholders** — clearly labelled on the homepage as "representative
  client experiences." Replace with real quotes when you have them (in `build.py` →
  `body_home()` → `testimonials`, or directly in `index.html`).

## Editing later (for a non-expert)
- **Text & listings:** edit the `.html` files directly — find the words, change them.
- **Property details/prices:** in each `property-*.html`, or in `build.py` (the `PROPERTIES`
  list) if you prefer to regenerate.
- **Colours, fonts, spacing:** the `:root { … }` block at the top of `css/styles.css`.
- **WhatsApp number / email:** search the files for `34670260445` and `info@nicolasstrebel.com`.

## Adding a property listing (scales to any number)
The Properties page is a filterable catalog (Type · Area · Bedrooms · Price) that grows
automatically as you add listings. To add one:

1. Drop its photos in `assets/images/properties/<slug>/` named `01.webp`, `02.webp`, …
   (`01` is the cover unless you set `cover` to another file).
2. Add the listing data, either:
   - **Hand-curated (featured quality):** a dict in the `PROPERTIES` list at the top of
     `build.py` (these three appear in the homepage "Featured" strip), **or**
   - **Bulk/imported:** an object in `listings.json` (catalog only). Fields: `id`, `slug`,
     `file`, `tag`, `type`, `region`, `title`, `loc`, `price`, `price_num`, `beds`,
     `baths`, `area`, `pool`, `short`, `desc_full`, `img_count`.
3. Run `python3 build.py`. The card, filters, count, detail page, gallery, OG image and
   JSON-LD are all generated for you.

The homepage "Featured" strip = the 3 curated `PROPERTIES`; the Properties page = those 3
**plus** everything in `listings.json` (compact filterable grid).

> **Currently 11 real listings** are populated — across Calpe, Jávea, Moraira and Benissa
> (villas, apartment, penthouse, townhouse, country house). The rest of his ~30 live
> listings can be imported the same way. The filter bar's Type/Area options generate
> themselves from the data, so they expand automatically as you add more.
>
> Note: skip any source photos that carry another agency's watermark (one Teulada listing
> was dropped for this reason). Imported `area` = built size; `plot` is shown as a feature.

## How it was built
`build.py` is an optional generator that emits the flat HTML so the shared nav/footer/SEO
stay identical across pages. You do **not** need it to host or to edit content. If you change
the nav or footer and want it applied everywhere at once, edit `build.py` and run
`python3 build.py`.

## SEO
Per-page `<title>`/meta/canonical, Open Graph + Twitter cards, semantic headings, and
JSON-LD (`RealEstateAgent`, `Person`, `Residence` per listing, `FAQPage`). `robots.txt`
and `sitemap.xml` included. Update the `SITE` constant in `build.py` if the domain changes.

## Design system at a glance
| Token | Value |
|---|---|
| Signature accent | `#7993AD` |
| Navy (authority) | `#22323F` |
| Sand (construction arm) | `#BFA171` |
| Page background | `#F7F4EF` (warm stone) |
| Headlines | Cormorant Garamond |
| Body | Plus Jakarta Sans |

Conversion: WhatsApp is the primary action everywhere (header button on desktop, persistent
floating button on mobile, CTAs throughout). The contact form composes a prefilled WhatsApp
or email message — no backend required.
