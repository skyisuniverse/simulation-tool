"""Exterior painted body panels sliced cleanly from the Roadster master shell.

Every panel is cut out of one unified thin-walled master surface (``body_skin()``)
with explicit ``SHUTLINE_GAP`` clearances so highlights flow seamlessly across
shutlines and adjacent panels never interpenetrate.
"""

from __future__ import annotations

import build123d as bd

from lib.palette import (
    PAINT_RED,
    group,
    style_paint,
)
from lib.surfaces import (
    BUMPER_FENDER_X,
    DOOR_FRONT_X,
    DOOR_REAR_X,
    HOOD_FRONT_X,
    HOOD_REAR_X,
    HOOP_REAR_X,
    SHUTLINE_GAP,
    SPOILER_FRONT_X,
    SPOILER_HALF_W,
    SPOILER_REAR_X,
    TARGA_REAR_X,
    body_section_face,
    body_section_face_inset,
    body_skin,
    box_between,
    canopy_glass_shell,
)

DOOR_SILL_Z = 248.0
DOOR_IN_Y = 660.0
# Rear deck-to-bumper seam cleanly ahead of the active spoiler (X = -1965 > SPOILER_FRONT_X = -1975)
REAR_FASCIA_X = -1965.0


def _hood_prism(inset=0.0):
    """Tapered planform prism for the Roadster frunk hood."""
    x0 = HOOD_REAR_X + inset
    x1 = HOOD_FRONT_X - inset
    y_rear = 660.0 - inset
    y_mid = 605.0 - inset
    y_front = 480.0 - inset
    x_mid = 0.55 * x0 + 0.45 * x1
    pts = [
        (x0, -y_rear),
        (x_mid, -y_mid),
        (x1, -y_front),
        (x1, y_front),
        (x_mid, y_mid),
        (x0, y_rear),
    ]
    wire = bd.Wire.make_polygon([bd.Vector(x, y, 520.0) for x, y in pts])
    return bd.extrude(bd.Face(wire), 420.0)


def _door_region(side, inset=0.0):
    x0 = DOOR_REAR_X + inset
    x1 = DOOR_FRONT_X - inset
    z0 = DOOR_SILL_Z + inset
    z1 = 960.0
    if side > 0:
        return box_between(x0, x1, DOOR_IN_Y, 1250.0, z0, z1)
    return box_between(x0, x1, -1250.0, -DOOR_IN_Y, z0, z1)


def _spoiler_region(inset=0.0):
    return box_between(
        SPOILER_REAR_X + inset,
        SPOILER_FRONT_X - inset,
        -(SPOILER_HALF_W - inset),
        SPOILER_HALF_W - inset,
        828.0,
        940.0,
    )


def _cabin_cutout():
    """Open the cockpit deck strictly INSIDE the teardrop canopy footprint."""
    pts = [
        (680.0, -470.0),
        (460.0, -575.0),
        (100.0, -615.0),
        (-450.0, -595.0),
        (-860.0, -500.0),
        (-1280.0, -370.0),
        (-1600.0, -230.0),
        (-1600.0, 230.0),
        (-1280.0, 370.0),
        (-860.0, 500.0),
        (-450.0, 595.0),
        (100.0, 615.0),
        (460.0, 575.0),
        (680.0, 470.0),
    ]
    wire = bd.Wire.make_polygon([bd.Vector(x, y, 600.0) for x, y in pts])
    return bd.extrude(bd.Face(wire), 400.0)


def _aero_recess_cutouts():
    """Subtract lower chin splitter pocket, rear diffuser cavity, and taillight slot."""
    # Lower front chin intake strictly BELOW the unbroken grille-less nose lip!
    front_mouth = box_between(1900.0, 2240.0, -630.0, 630.0, 80.0, 198.0)
    # Massive rear diffuser cavity at lower rear fascia (Z up to 540 at tail)
    rear_diffuser_bay = box_between(-2300.0, -1930.0, -685.0, 685.0, 100.0, 540.0)
    # Slim recessed taillight blade slot across upper rear transom
    rear_lamp_slot = box_between(-2300.0, -2195.0, -725.0, 725.0, 748.0, 794.0)
    # Underfloor cut for flat EV structural battery tray
    underfloor_cut = box_between(-1680.0, 1780.0, -740.0, 740.0, 60.0, 152.0)
    return [front_mouth, rear_diffuser_bay, rear_lamp_slot, underfloor_cut]


def _headlight_cutouts():
    """Razor-slim swept LED blade recesses tucked tightly along the front brow."""
    cuts = []
    for side in (1, -1):
        bar = bd.Box(240.0, 290.0, 40.0)
        bar = bd.Rot(0, -15, side * -32) * bar
        bar = bd.Pos(2025.0, side * 665.0, 522.0) * bar
        cuts.append(bar)
    return cuts


def _safe_keep(shape):
    if shape is None:
        return None
    if not shape.solids():
        return None
    return shape


def build():
    """Build painted exterior panels and the Targa B-pillar roll hoop.

    Returns ``(fixed_body_group, door_left_skin, door_right_skin, spoiler_skin)``.
    """
    g = SHUTLINE_GAP / 2.0

    skin = body_skin()
    skin = skin - _cabin_cutout()
    skin = skin - _aero_recess_cutouts()
    skin = skin - _headlight_cutouts()

    # 1. Tapered hood (frunk lid)
    hood_keep = _hood_prism(inset=g)
    hood_cut = _hood_prism(inset=-g)
    hood = _safe_keep(skin & hood_keep)
    assert hood is not None and hood.bounding_box().max.Z < 815.0, (
        f"Hood boolean produced invalid bounds: {hood.bounding_box() if hood else None}"
    )

    # 2. Seamless grille-less front bumper wrapping smoothly back to front wheel arches!
    # Forward of BUMPER_FENDER_X (+1795) and outside hood_cut
    bumper_box = box_between(BUMPER_FENDER_X + g, 2320.0, -1200.0, 1200.0, 100.0, 950.0)
    front_fascia = _safe_keep((skin & bumper_box) - hood_cut)

    # 3. Front fenders (left & right), cleanly between door front and bumper seam, outside hood
    fender_x_box = box_between(DOOR_FRONT_X + g, BUMPER_FENDER_X - g, -1200.0, 1200.0, 100.0, 950.0)
    fenders_both = (skin & fender_x_box) - hood_cut
    front_fender_left = _safe_keep(fenders_both & box_between(0.0, 2300.0, 0.0, 1250.0, 0.0, 1000.0))
    front_fender_right = _safe_keep(fenders_both & box_between(0.0, 2300.0, -1250.0, 0.0, 0.0, 1000.0))

    # 4. Flush sculpted doors (separate moving skins)
    door_left_skin = _safe_keep(skin & _door_region(1, inset=g))
    door_right_skin = _safe_keep(skin & _door_region(-1, inset=g))

    # 5. Fixed lower rocker sills beneath doors
    rocker_left = _safe_keep(
        skin & box_between(DOOR_REAR_X + g, DOOR_FRONT_X - g, 500.0, 1250.0, 100.0, DOOR_SILL_Z - g)
    )
    rocker_right = _safe_keep(
        skin & box_between(DOOR_REAR_X + g, DOOR_FRONT_X - g, -1250.0, -500.0, 100.0, DOOR_SILL_Z - g)
    )

    # 6. Flush deployable active rear spoiler (clean 4.5 mm well gap cut deep through deck skin)
    spoiler_keep = _spoiler_region(inset=g)
    spoiler_cut = box_between(
        SPOILER_REAR_X - g,
        SPOILER_FRONT_X + g,
        -(SPOILER_HALF_W + g),
        SPOILER_HALF_W + g,
        795.0,
        960.0,
    )
    spoiler_skin = _safe_keep(skin & spoiler_keep)

    # 7. Muscular rear haunches & fastback deck (cleanly ahead of active spoiler: X >= -1962.75)
    rear_quarters = _safe_keep(
        skin & box_between(REAR_FASCIA_X + g, DOOR_REAR_X - g, -1250.0, 1250.0, -50.0, 1050.0)
    )

    # 8. Kammback rear bumper & closed 16 mm rear transom (houses entire active spoiler, lamps & diffuser)
    rb_outer = bd.loft(
        [body_section_face(x) for x in (-2250.0, -2220.0, -2160.0, -2060.0, REAR_FASCIA_X - g)]
    )
    rb_inner = bd.loft(
        [body_section_face_inset(x, 14.0) for x in (-2234.0, -2210.0, -2160.0, -2060.0, REAR_FASCIA_X + 12.0)]
    )
    rear_bumper = _safe_keep((rb_outer - rb_inner) - _aero_recess_cutouts() - spoiler_cut)

    # 9. Iconic Tesla Roadster Targa B-pillar roll hoop (cut from canopy shell)
    canopy = canopy_glass_shell()
    hoop_box = box_between(HOOP_REAR_X + g, TARGA_REAR_X - g, -900.0, 900.0, 740.0, 1250.0)
    targa_hoop = _safe_keep(canopy & hoop_box)

    fixed_parts = []
    for shape, lbl in [
        (front_fascia, "front_fascia"),
        (hood, "hood"),
        (front_fender_left, "front_fender_left"),
        (front_fender_right, "front_fender_right"),
        (rocker_left, "rocker_left"),
        (rocker_right, "rocker_right"),
        (rear_quarters, "rear_quarters"),
        (rear_bumper, "rear_bumper"),
        (targa_hoop, "targa_roll_hoop"),
    ]:
        assert shape is not None and shape.volume > 0.0, f"Body panel {lbl!r} invalid or missing"
        fixed_parts.append(style_paint(shape, lbl, PAINT_RED))

    assert door_left_skin is not None and door_left_skin.volume > 0.0
    assert door_right_skin is not None and door_right_skin.volume > 0.0
    assert spoiler_skin is not None and spoiler_skin.volume > 0.0
    door_left_skin = style_paint(door_left_skin, "door_skin_left", PAINT_RED)
    door_right_skin = style_paint(door_right_skin, "door_skin_right", PAINT_RED)
    spoiler_skin = style_paint(spoiler_skin, "active_spoiler_panel", PAINT_RED)

    return group("body_fixed", fixed_parts), door_left_skin, door_right_skin, spoiler_skin
