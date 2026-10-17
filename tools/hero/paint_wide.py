#!/usr/bin/env python3
"""Paints the wide title render (wide_title.py) as tools/art/airy_estate_paint.py paints the title's land (Z-Image
Turbo image to image at its DENOISE in tiles, despeckled, muted, keeping the render's colour; the meadow's painted
finish), then lays the game's own painted clouds (assets/final/title/cloud_<k>.png) high in its sky: the website's
desktop hero, ~/lumenleaf-art/site_hero/hero_wide.png.

    ~/ComfyUI/.venv/bin/python paint_wide.py [--seed 151] [--force] [--server http://127.0.0.1:8188]
"""

import argparse
import json
import os
import sys

import numpy as np

sys.dont_write_bytecode = True
PROJECT = os.path.expanduser("~/Documents/lumen-and-leaf")
sys.path.insert(0, os.path.join(PROJECT, "tools", "art"))
os.chdir(PROJECT)  # the ComfyUI workflow's path is relative to the project
import airy_estate_paint as ap  # noqa: E402

FOLDER = os.path.expanduser("~/lumenleaf-art/site_hero")
RENDERS, PAINTED = os.path.join(FOLDER, "renders"), os.path.join(FOLDER, "painted")
CLOUD_ART = os.path.join(PROJECT, "assets", "final", "title")
# Each cloud as laid in the wide sky: its centre across (a share of the width), its foot down (a share of the height)
# and its scale, all above the trees.
CLOUDS = {1: (0.16, 0.21, 0.6), 2: (0.84, 0.18, 0.55), 3: (0.52, 0.11, 0.4)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=ap.SEED)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--server", default="http://127.0.0.1:8188")
    args = parser.parse_args()
    os.makedirs(PAINTED, exist_ok=True)
    context = ap.load(os.path.join(RENDERS, "title_meadow_context.png"))[..., :3]
    cover = ap.load(os.path.join(RENDERS, "title_meadow.png"))[..., 3]
    height, width = context.shape[:2]
    spec = json.load(open(ap.SPEC, encoding="utf-8"))
    stage, style = spec["stage"], spec["style"]
    house = (width * 0.3, width * 0.7)  # the columns the house stands in

    def words(x, y, tile):
        across, down = x + tile / 2.0, y + tile / 2.0
        if house[0] <= across <= house[1]:
            key = "house"
        else:
            key = "far" if down < height * 0.5 else "meadow"
        return ap.TITLE[key] + " " + style

    target = os.path.join(PAINTED, "hero_wide_land.png")
    if args.force or not os.path.exists(target):
        painted = ap.tiled(args.server, stage, context, words, args.seed + 1)
        ap.save(painted, target)
        print("painted", target, flush=True)
    painted = ap.load(target)[..., :3]
    # The meadow's finish as the game's: strokes from its far edge (the first row the grass covers across most of
    # the picture) to the picture's foot.
    rows = np.nonzero(cover.mean(axis=1) > 0.6)[0]
    ap.LAND_TOP, ap.CANVAS, ap.MEADOW_FAR = 0, (width, height), int(rows.min()) if len(rows) else int(height * 0.6)
    finished = ap.meadow_finish(painted, cover)
    canvas = finished.copy()
    for k, (centre, foot, scale) in CLOUDS.items():
        cloud = ap.load(os.path.join(CLOUD_ART, "cloud_%d.png" % k))
        cloud = ap.resize(cloud, (round(cloud.shape[1] * scale), round(cloud.shape[0] * scale)))
        ap.paste(canvas, cloud, round(centre * width - cloud.shape[1] / 2), round(foot * height - cloud.shape[0]))
    out = os.path.join(FOLDER, "hero_wide.png")
    ap.save(canvas, out)
    print("wrote", out, "meadow far row", ap.MEADOW_FAR, flush=True)


if __name__ == "__main__":
    main()
