# pinholegames.com

The website of Pinhole Games: a home page, a page for Lumen & Leaf and the game's privacy policy,
served by GitHub Pages from this repository's `main` branch at https://pinholegames.com.

| Path | Page |
|---|---|
| `index.html` | `/`: Lumen & Leaf's landing page, its styles inline |
| `lumen-and-leaf/index.html` | `/lumen-and-leaf/`: sends visitors to `/` |
| `lumen-and-leaf/privacy.html` | `/lumen-and-leaf/privacy` (GitHub Pages serves a `.html` file without its extension): the game's privacy policy, the URL given in Play Console and opened by the game's settings |
| `404.html` | any other address |
| `assets/site.css` | the plain pages' styles (the privacy policy, the 404, the redirect) |
| `assets/` | the game's font and its pictures and trailer |
| `tools/hero/` | how the desktop hero's wide painting was made |

The landing page is one column, the same on a phone and a desktop: the painted meadow and greenhouse filling the
screen with the game's name lettered over the sky as its title screen letters it (Open Sans SemiBold, the game's
font, in its gold with a dark edge), a "Coming soon to Google Play" button (no Google badge until the listing
exists) and a "Watch the trailer" link; three phone screenshots; a few words about the game; a small footer. It
uses the game's colours (`src/game/palette.gd`). Plain HTML: no build step, no cookies, no analytics and nothing
loaded from another site, as the privacy policy says. The one script, inline in `index.html`, opens the trailer
over the page; without it the link opens the video itself. `.nojekyll` turns off GitHub's Jekyll build; `CNAME`
holds the custom domain.

## Editing

Edit a file, open it in a browser to check it (any static server works: `python3 -m http.server`),
commit and push to `main`. GitHub Pages publishes it within a minute or two.

## The privacy policy

Its source is the game repository's `docs/store/privacy_policy.md`; this page is that text as HTML.
Change both together, with a new effective date, before anything the policy describes changes in the
game (the policy promises that).

## The pictures, the trailer and the font

Each picture is AVIF with a JPEG for older browsers. From the game repository (`~/Documents/lumen-and-leaf`):

- `hero-tall.*` (phones and any screen taller than wide): the title screen's painting, `assets/final/title/background.png`.
- `hero-wide-1600.*`, `hero-wide-2560.*` (screens wider than tall): a wide painting of the same scene, made by
  `tools/hero/`: `blender -b --factory-startup -P tools/hero/wide_title.py` renders the title's Blender scene
  (`tools/art/airy_estate.py`) through a 16:9 camera into `~/lumenleaf-art/site_hero/renders/` (about 5 minutes), then,
  with ComfyUI running, `~/ComfyUI/.venv/bin/python tools/hero/paint_wide.py` paints it as the game's title is painted
  (`tools/art/airy_estate_paint.py`: Z-Image Turbo at its denoise, the meadow's brush finish) and lays the game's
  painted clouds in its sky: `~/lumenleaf-art/site_hero/hero_wide.png` (about 5 minutes).
- `shot-herb-house.*`, `shot-rose-garden.*`, `shot-fern-grotto.*`: the English phone store screenshots 02, 03 and 04
  (`tools/store_screenshots.gd`) at half size.
- `trailer.mp4`: `builds/trailer/lumen_and_leaf_trailer.mp4` (`scripts/record_trailer.sh`) for the web, 1080x1920:
  `ffmpeg -i lumen_and_leaf_trailer.mp4 -c:v libx264 -preset slow -crf 25 -maxrate 3M -bufsize 6M -pix_fmt yuv420p
  -c:a aac -b:a 128k -movflags +faststart trailer.mp4`; `trailer-poster.jpg` its frame at 2 seconds. Both load only
  when the trailer is opened.
- `feature.jpg`: the store's feature graphic (`docs/store/feature_graphic/prism.png`), the picture a shared link shows.
- The favicons: the app icon (`docs/store/icon/prism_rose/`).

`assets/fonts/open-sans-semibold.woff2` is the game's `assets/fonts/open_sans_semibold.ttf` cut to Latin characters
(SIL Open Font License 1.1, `assets/fonts/OFL.txt`):

    uv run --no-project --with fonttools==4.60.1 --with brotli==1.1.0 pyftsubset open_sans_semibold.ttf \
        --unicodes="U+0020-007E,U+00A0-00FF,U+2013-2014,U+2018-2019,U+201C-201D,U+2022,U+2026,U+2190,U+2192" \
        --layout-features='kern,liga' --flavor=woff2 --output-file=assets/fonts/open-sans-semibold.woff2

## DNS and hosting

The domain is registered with Vercel, which also serves its DNS; nothing is hosted on Vercel. GitHub
Pages needs, for `pinholegames.com`: A records 185.199.108.153, 185.199.109.153, 185.199.110.153 and
185.199.111.153; AAAA records 2606:50c0:8000::153, 2606:50c0:8001::153, 2606:50c0:8002::153 and
2606:50c0:8003::153; and for `www`, a CNAME to `yeaimjason.github.io`. The domain is verified for the
GitHub account (a `_github-pages-challenge-Yeaimjason` TXT record, which must stay), so no other account
can publish a Pages site on it. The MX and SPF TXT records are ImprovMX's email forwarding
(support@pinholegames.com): leave them as they are.
