# pinholegames.com

The website of Pinhole Games: a home page, a page for Lumen & Leaf and the game's privacy policy,
served by GitHub Pages from this repository's `main` branch at https://pinholegames.com.

| Path | Page |
|---|---|
| `index.html` | `/`: the studio |
| `lumen-and-leaf/index.html` | `/lumen-and-leaf/`: the game |
| `lumen-and-leaf/privacy/index.html` | `/lumen-and-leaf/privacy`: the game's privacy policy, the URL given in Play Console and opened by the game's settings |
| `404.html` | any other address |
| `assets/` | the stylesheet, the mark (`pinhole.svg`, also the favicon) and the game's pictures |

Plain HTML and one stylesheet: no build step, no scripts, no web fonts, no cookies, no analytics and
nothing loaded from another site, so a visitor's browser talks to pinholegames.com alone (the privacy
policy says so). `.nojekyll` turns off GitHub's Jekyll build; `CNAME` holds the custom domain.

## Editing

Edit a file, open it in a browser to check it (any static server works: `python3 -m http.server`),
commit and push to `main`. GitHub Pages publishes it within a minute or two.

## The privacy policy

Its source is the game repository's `docs/store/privacy_policy.md`; this page is that text as HTML.
Change both together, with a new effective date, before anything the policy describes changes in the
game (the policy promises that).

## The pictures

From the game repository: `assets/lumen-and-leaf/icon.png` is the Play Store icon
(`docs/store/icon/prism_rose/play_store_512.png`, at 256 px), `feature.jpg` the feature graphic
(`docs/store/feature_graphic/prism.png`) and the three screenshots are the English phone store
screenshots (`tools/store_screenshots.gd`: 03, 05 and 06) at half size.

## DNS and hosting

The domain is registered with Vercel, which also serves its DNS; nothing is hosted on Vercel. GitHub
Pages needs, for `pinholegames.com`: A records 185.199.108.153, 185.199.109.153, 185.199.110.153 and
185.199.111.153; AAAA records 2606:50c0:8000::153, 2606:50c0:8001::153, 2606:50c0:8002::153 and
2606:50c0:8003::153; and for `www`, a CNAME to `yeaimjason.github.io`. The domain is verified for the
GitHub account (a `_github-pages-challenge-yeaimjason` TXT record, which must stay), so no other account
can publish a Pages site on it. The MX and SPF TXT records are ImprovMX's email forwarding
(support@pinholegames.com): leave them as they are.
