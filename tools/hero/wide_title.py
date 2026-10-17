"""The title screen's scene (tools/art/airy_estate.py) through a wide camera, for the website's desktop hero:
the same meadow, house, trees, hills and sky, framed 16:9. Uses the repo's own scene code, changing only the camera,
the meadow's width (it fills the camera's view) and a few more trees at the sides the wide view shows.

    blender -b --factory-startup -P wide_title.py -- [--out ~/lumenleaf-art/site_hero/renders]
        [--only title_meadow] [--samples 96] [--scale 100] [--no-masks]
"""

import math
import os
import random
import sys

import bmesh
import bpy
import mathutils.noise
from mathutils import Matrix, Vector

sys.path.insert(0, os.path.expanduser("~/Documents/lumen-and-leaf/tools/art"))
import airy_estate as ae  # noqa: E402
import board_toon as toon  # noqa: E402

ae.OUT = "~/lumenleaf-art/site_hero/renders"
ae.CANVAS = (2560, 1440)
# A level eye at the meadow's edge as the game's, a little farther back and looking a touch up, so the sky holds the
# name over the house; the same lens, its 36 mm across the picture's width (the game's spans its height).
AT = (0.0, -19.5, 2.05)
PITCH = 91.6
LENS = 34.0
ae.TITLE_CAMERA = {"at": AT, "pitch": PITCH, "lens": LENS}
SPREAD = 0.6  # half the view's width a cell ahead (tan 27.9 degrees, 0.53), with a margin for the wind
ae.BLADES = 115000


def title_camera(scene, scale):
    camera = scene.camera
    camera.data.type = "PERSP"
    camera.data.sensor_fit = "HORIZONTAL"
    camera.data.sensor_width = 36.0
    camera.data.lens = LENS
    camera.data.clip_end = 1000.0
    camera.location = AT
    camera.rotation_euler = (math.radians(PITCH), 0.0, 0.0)
    scene.render.resolution_x, scene.render.resolution_y = ae.CANVAS
    scene.render.pixel_aspect_x = scene.render.pixel_aspect_y = 1.0
    scene.render.resolution_percentage = scale


def meadow(coll, mats, rng, near, far, count, tall=ae.BLADE_TALL, flowers=True):
    """airy_estate.meadow() across the wide view (SPREAD for its 0.26)."""
    cam_x, cam_y, _ = AT
    verts, faces, sways, tints = [], [], [], []
    area_near, area_far = near * near, far * far
    for _ in range(count):
        distance = math.sqrt(area_near + rng.random() * (area_far - area_near))
        x = cam_x + rng.uniform(-1.0, 1.0) * (SPREAD * distance + 0.6)
        y = cam_y + distance
        patch = mathutils.noise.noise(Vector((x * 0.18, y * 0.18, 0.5)))
        height = rng.uniform(*tall) * (0.8 + 0.2 * rng.random()) * (1.0 + 0.22 * patch)
        width = rng.uniform(0.02, 0.034) * (1.0 + distance * 0.014)
        lean_dir = rng.uniform(-0.5, 0.5) + 0.45
        lean = rng.uniform(0.06, 0.26)
        face = rng.uniform(0.0, math.pi)
        tint = min(1.0, max(0.0, rng.gauss(0.42 - 0.22 * patch, 0.13)))
        across = Vector((math.cos(face), math.sin(face), 0.0))
        lean_vec = Vector((math.sin(lean_dir), math.cos(lean_dir) * 0.4, 0.0))
        base = len(verts)
        steps = 4
        for k in range(steps + 1):
            t = k / steps
            centre = Vector((x, y, 0.0)) + lean_vec * (lean * height * t * t) \
                + Vector((0.0, 0.0, height * t * (1.0 - 0.18 * lean * t)))
            half = width * 0.5 * (1.0 - t) ** 0.8 + 0.002
            for side in (-1.0, 1.0):
                verts.append(tuple(centre + across * half * side))
                sways.append(t ** 1.3)
                tints.append(tint)
        for k in range(steps):
            a = base + 2 * k
            faces.append((a, a + 1, a + 3, a + 2))
    mesh = bpy.data.meshes.new("airy_grass")
    mesh.from_pydata(verts, [], faces)
    mesh.validate()
    obj = bpy.data.objects.new("airy_grass", mesh)
    coll.objects.link(obj)
    mesh.materials.append(mats.grass)
    ae.set_point_attribute(obj, "sway", sways)
    ae.set_point_attribute(obj, "tint", tints)
    for poly in mesh.polygons:
        poly.use_smooth = True
    if flowers:
        wildflowers(coll, mats, rng, near, far, count // 30)
    return obj


def wildflowers(coll, mats, rng, near, far, count):
    """airy_estate.wildflowers() across the wide view."""
    cam_x, cam_y, _ = AT
    heads = {name: bmesh.new() for name in ae.FLOWERS}
    stems = bmesh.new()
    kinds = ("white", "butter", "white", "lavender", "butter", "blush")
    area_near, area_far = near * near, far * far
    placed = 0
    while placed < count:
        distance = math.sqrt(area_near + rng.random() * (area_far - area_near))
        x = cam_x + rng.uniform(-1.0, 1.0) * (SPREAD * distance + 0.6)
        y = cam_y + distance
        drift = mathutils.noise.noise(Vector((x * 0.32, y * 0.32, 4.0)))
        if drift < 0.12 or rng.random() > (drift - 0.12) * 2.5:
            continue
        placed += 1
        tall = rng.uniform(0.5, 0.95)
        kind = kinds[int((mathutils.noise.noise(Vector((x * 0.12, y * 0.12, 9.0))) * 0.5 + 0.5) * len(kinds))
                     % len(kinds)]
        radius = rng.uniform(0.028, 0.045) * (1.0 + distance * 0.012)
        toon.disc(stems, (x, y, 0.0), 0.006, tall)
        made = bmesh.ops.create_cone(heads[kind], cap_ends=True, segments=10, radius1=radius, radius2=radius * 0.6,
                                     depth=radius * 0.3)
        bmesh.ops.transform(heads[kind], verts=made["verts"],
                            matrix=Matrix.Translation((x, y, tall)) @ Matrix.Rotation(math.radians(-62.0), 4, "X"))
    stem_obj = toon.mesh_object("airy_flower_stems", coll, stems, mats.stems)
    ae.set_point_attribute(stem_obj, "sway", [min(1.0, v.co.z / 0.95) ** 1.3 for v in stem_obj.data.vertices])
    for name, bm in heads.items():
        obj = toon.mesh_object("airy_flowers_" + name, coll, bm, mats.meadow_flowers[name])
        ae.set_point_attribute(obj, "sway", [1.0] * len(obj.data.vertices))


# The game's trees, and more where the wide view reaches past them: far ones along the meadow's back, a near one each
# side to frame the house, a couple more poplars.
FAR_TREES = ((-10.5, 26.0, 5.6), (-7.0, 30.0, 6.4), (-3.6, 34.0, 5.2), (3.4, 33.0, 5.8), (7.8, 29.0, 6.6),
             (11.0, 25.0, 5.0), (-14.0, 22.0, 4.8), (14.5, 21.0, 5.4), (0.4, 40.0, 6.0),
             (-18.0, 27.0, 6.2), (-22.5, 23.0, 5.2), (-26.5, 30.0, 6.8), (-31.0, 25.0, 5.6), (-35.0, 33.0, 6.4),
             (18.5, 26.0, 5.8), (22.0, 31.0, 6.6), (26.0, 24.0, 5.0), (30.5, 29.0, 6.2), (34.5, 23.0, 5.4))
NEAR_TREES = ((-7.8, 8.5, 4.8), (8.2, 9.5, 5.2), (-10.8, 12.5, 5.4), (11.0, 13.5, 4.6),
              (-15.5, 9.5, 5.6), (16.0, 11.0, 5.0), (-20.0, 14.0, 5.2), (20.5, 15.5, 5.8))
POPLARS = ((-12.0, 34.0), (-11.0, 36.0), (12.5, 38.0), (-24.0, 38.0), (23.5, 36.0), (28.0, 40.0))


def title_scene(coll_by_layer, mats):
    """airy_estate.title_scene() with the wide view's trees."""
    rng = random.Random(7)
    hills = coll_by_layer["title_hills"]
    ridges = ((-70.0, 230.0, 110.0, 40.0, 26.0, 0), (60.0, 250.0, 120.0, 40.0, 30.0, 0), (5.0, 215.0, 70.0, 30.0, 18.0, 0),
              (-45.0, 160.0, 60.0, 26.0, 13.0, 1), (40.0, 150.0, 58.0, 24.0, 11.0, 1), (-5.0, 135.0, 34.0, 18.0, 7.0, 1),
              (-28.0, 92.0, 30.0, 14.0, 5.0, 2), (26.0, 88.0, 34.0, 14.0, 4.6, 2))
    for k, (cx, cy, sx, sy, sz, tone) in enumerate(ridges):
        bm = bmesh.new()
        toon.ball(bm, (0.0, 0.0, 0.0), 1.0, segments=(48, 24))
        obj = toon.mesh_object("airy_hill_%d" % k, hills, bm, mats.hills[tone])
        obj.matrix_basis = Matrix.Translation((cx, cy, -sz * 0.3)) @ Matrix.Diagonal((sx, sy, sz, 1.0))
    trees = coll_by_layer["title_trees"]
    far_canopy, far_trunk, near_canopy, near_trunk, columns = (bmesh.new() for _ in range(5))
    for x, y, tall in FAR_TREES:
        ae.tree(trees, far_canopy, far_trunk, rng, (x, y), tall, 2.0 + 0.2 * tall)
    for x, y, tall in NEAR_TREES:
        ae.tree(trees, near_canopy, near_trunk, rng, (x, y), tall, 1.9 + 0.2 * tall)
    for x, y in POPLARS:
        ae.poplar(columns, rng, (x, y), 9.0)
    made = [toon.mesh_object("airy_far_canopy", trees, far_canopy, mats.far_canopy),
            toon.mesh_object("airy_far_trunks", trees, far_trunk, mats.far_trunk),
            toon.mesh_object("airy_near_canopy", trees, near_canopy, mats.near_canopy),
            toon.mesh_object("airy_near_trunks", trees, near_trunk, mats.near_trunk),
            toon.mesh_object("airy_poplars", trees, columns, mats.poplar)]
    ae.sway_by_height(made[0], 2.0, 6.6, 1.2)
    ae.sway_by_height(made[2], 1.8, 5.4, 1.2)
    ae.sway_by_height(made[4], 1.0, 9.0, 1.5)
    house = coll_by_layer["title_house"]
    ae.estate.greenhouse(house, mats, "herb_house")
    for obj in house.objects:
        if obj.name.startswith("estate_glass"):
            obj["glass"] = 1.0
    ground = coll_by_layer["title_meadow"]
    lawn = ae.Geometry()
    lawn.box(-80.0, -40.0, -0.2, 80.0, 90.0, 0.0)
    lawn.to_object("airy_ground", ground, mats.lawn)
    meadow(ground, mats, rng, 1.2, 27.0, ae.BLADES)


ae.title_camera = title_camera
ae.meadow = meadow
ae.wildflowers = wildflowers
ae.title_scene = title_scene

if __name__ == "__main__":
    # Only the title's layers: airy_estate.main() renders whatever --only names.
    if "--" not in sys.argv:
        sys.argv += ["--"]
    if not any(arg.startswith("--only") for arg in sys.argv[sys.argv.index("--"):]):
        sys.argv += ["--only", ",".join(ae.TITLE_LAYERS)]
    if not any(arg.startswith("--out") for arg in sys.argv[sys.argv.index("--"):]):
        sys.argv += ["--out", ae.OUT]
    ae.main()
