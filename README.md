# pinholegames.com

The website of Pinhole Games: a home page, a page for Lumen & Leaf and the game's privacy policy,
served by GitHub Pages from this repository's `main` branch at https://pinholegames.com.

| Path | Page |
|---|---|
| `index.html` | `/`: Lumen & Leaf, the studio's game, in the game's own look |
| `lumen-and-leaf/index.html` | `/lumen-and-leaf/`: sends visitors to `/` (the game's page, until there is a second game) |
| `lumen-and-leaf/privacy.html` | `/lumen-and-leaf/privacy` (GitHub Pages serves a `.html` file without its extension): the game's privacy policy, the URL given in Play Console and opened by the game's settings |
| `404.html` | any other address |
| `assets/` | the stylesheet, the game's font and its pictures |

The page wears the game's look rather than a web template's: its title painting
(`assets/final/title/background.png` in the game repository) with the name lettered over the sky as
the title screen letters it (Open Sans SemiBold, the game's font, in its gold with a dark edge), its
colours (`src/game/palette.gd`), its store screenshots, and the store listing's words. The privacy
policy and the 404 page are plain pages. Plain HTML and one stylesheet: no build step, no scripts, no
cookies, no analytics and nothing loaded from another site (the font is served from here), so a
visitor's browser talks to pinholegames.com alone, as the privacy policy says. `.nojekyll` turns off
GitHub's Jekyll build; `CNAME` holds the custom domain.

## Editing

Edit a file, open it in a browser to check it (any static server works: `python3 -m http.server`),
commit and push to `main`. GitHub Pages publishes it within a minute or two.

## The privacy policy

Its source is the game repository's `docs/store/privacy_policy.md`; this page is that text as HTML.
Change both together, with a new effective date, before anything the policy describes changes in the
game (the policy promises that).

## The pictures and the font

From the game repository: `assets/lumen-and-leaf/title.jpg` is the title screen's painting
(`assets/final/title/background.png`), `feature.jpg` the store's feature graphic (`docs/store/feature_graphic/prism.png`,
the picture a shared link shows), the four screenshots the English phone store screenshots
(`tools/store_screenshots.gd`: 02, 03, 05 and 06) at half size, and the favicons the app icon
(`docs/store/icon/prism_rose/`). `assets/fonts/open-sans-semibold.woff2` is the game's
`assets/fonts/open_sans_semibold.ttf` cut to Latin characters (SIL Open Font License 1.1,
`assets/fonts/OFL.txt`):

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
