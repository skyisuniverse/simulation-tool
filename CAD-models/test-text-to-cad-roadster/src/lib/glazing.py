"""Teardrop panoramic glazing for the Tesla Roadster (2nd generation).

All glazing panels are sliced cleanly from ``canopy_glass_shell()`` with exact
``SHUTLINE_GAP`` clearances against each other and against the painted Targa
B-pillar roll hoop:
  - Panoramic curved windshield framed by continuous gloss-black A-pillars
  - Removable Targa glass roof panel (stows / lifts open!)
  - Frameless left and right side door glass (rides with the doors!)
  - Sweeping teardrop fastback rear glass
"""

from __future__ import annotations

import build123d as bd

from lib.palette import (
    BLACK_GLOSS,
    GLASS_REAR,
    GLASS_ROOF,
    GLASS_TINT,
    group,
    style_glass,
    style_gloss_black,
)
from lib.surfaces import (
    HOOP_REAR_X,
    REAR_GLASS_END_X,
    SHUTLINE_GAP,
    TARGA_FRONT_X,
    TARGA_REAR_X,
    box_between,
    canopy_glass_shell,
)

# Roof-rail Z separating removable Targa overhead panel from frameless side glass
ROOF_RAIL_Z = 1072.0


def _safe(shape):
    if shape is None:
        return None
    if not shape.solids():
        return None
    return shape


def _xz_prism(xz_pts, y0, y1):
    wire = bd.Wire.make_polygon([bd.Vector(x, y0, z) for x, z in xz_pts])
    return bd.extrude(bd.Face(wire), y1 - y0, dir=(0, 1, 0))


def build():
    """Build canopy glazing and return ``(fixed_glazing_group, targa_roof_glass, door_glass_l, door_glass_r)``."""
    g = SHUTLINE_GAP / 2.0
    canopy = canopy_glass_shell()

    # Angled A-pillar front line from windshield base (X=710, Z=740) smoothly up to header (X=175, Z=1185)
    # 1. Panoramic curved front windshield (forward of A-pillar front line)
    ws_pts = [
        (1000.0, 680.0),
        (1000.0, 1260.0),
        (TARGA_FRONT_X + g, 1260.0),
        (TARGA_FRONT_X + g, 1140.0),
        (710.0 + g, 680.0),
    ]
    windshield = _safe(canopy & _xz_prism(ws_pts, -850.0, 850.0))

    # 2. Continuous sleek gloss-black A-pillar trim along the windshield side edges (below ROOF_RAIL_Z)
    # Wait: make the A-pillar sweep straight up to ROOF_RAIL_Z seamlessly!
    # At Z = ROOF_RAIL_Z (1072), the A-pillar front line is at X = 710 - (710 - 175) * (1072 - 680) / (1140 - 680) = 254.
    x_ap_top = 254.0
    ap_pts = [
        (x_ap_top - g, ROOF_RAIL_Z - g),
        (710.0 - g, 680.0),
        (652.0 + g, 680.0),
        (x_ap_top - 58.0 + g, ROOF_RAIL_Z - g),
    ]
    a_pillar_left = _safe(canopy & _xz_prism(ap_pts, 400.0, 850.0))
    a_pillar_right = _safe(canopy & _xz_prism(ap_pts, -850.0, -400.0))

    # 3. Removable Targa glass roof panel (between windshield header and Targa roll hoop, above ROOF_RAIL_Z)
    targa_pts = [
        (TARGA_FRONT_X - g, 1260.0),
        (TARGA_FRONT_X - g, 1140.0),
        (x_ap_top - g, ROOF_RAIL_Z + g),
        (TARGA_REAR_X + g, ROOF_RAIL_Z + g),
        (TARGA_REAR_X + g, 1260.0),
    ]
    targa_roof = _safe(canopy & _xz_prism(targa_pts, -850.0, 850.0))

    # 4. Frameless side door windows (below ROOF_RAIL_Z - g, tucked cleanly behind A-pillar and ahead of Targa hoop)
    door_win_pts = [
        (x_ap_top - 58.0 - g, ROOF_RAIL_Z - g),
        (652.0 - g, 680.0),
        (TARGA_REAR_X + g, 680.0),
        (TARGA_REAR_X + g, ROOF_RAIL_Z - g),
    ]
    door_glass_left = _safe(canopy & _xz_prism(door_win_pts, 350.0, 850.0))
    door_glass_right = _safe(canopy & _xz_prism(door_win_pts, -850.0, -350.0))

    # 5. Sweeping teardrop fastback rear glass (tapering smoothly to X = -1940!)
    rear_glass_region = box_between(
        REAR_GLASS_END_X - 80.0, HOOP_REAR_X - g, -850.0, 850.0, 720.0, 1260.0
    )
    rear_glass = _safe(canopy & rear_glass_region)

    fixed = []
    if windshield is not None:
        fixed.append(style_glass(windshield, "windshield", GLASS_TINT, transmission=0.88))
    if a_pillar_left is not None:
        fixed.append(style_gloss_black(a_pillar_left, "a_pillar_left", BLACK_GLOSS))
    if a_pillar_right is not None:
        fixed.append(style_gloss_black(a_pillar_right, "a_pillar_right", BLACK_GLOSS))
    if rear_glass is not None:
        fixed.append(style_glass(rear_glass, "fastback_rear_glass", GLASS_REAR, transmission=0.82))

    if targa_roof is not None:
        targa_roof = style_glass(targa_roof, "targa_roof_glass", GLASS_ROOF, transmission=0.84)
    if door_glass_left is not None:
        door_glass_left = style_glass(door_glass_left, "door_glass_left", GLASS_TINT, transmission=0.86)
    if door_glass_right is not None:
        door_glass_right = style_glass(door_glass_right, "door_glass_right", GLASS_TINT, transmission=0.86)

    return group("glazing_fixed", fixed), targa_roof, door_glass_left, door_glass_right
