"""Gold Glazed wrap-around fighter-jet glass canopy (windshield, continuous
arched glass roof, tapered fastback rear glass, fixed rear quarter windows),
slim satin-titanium A-pillar & roof-rail trim, and interior rearview mirror.
"""

import build123d as bd
from cad import model
from cad.build123d import memo

from body_surface import (
    door_aperture_prism,
    master_body_solid,
    master_canopy_solid,
)
from spec import (
    CANOPY_STATIONS,
    apply_alcantara,
    apply_dark_gloss,
    apply_gold_glass,
    apply_titanium,
)


def _hollow_canopy_shell(thickness=14.0):
    """Build a thin-walled laminated glass canopy shell (hollow inside for cabin view)."""
    outer = master_canopy_solid()

    # Build a clean inner cavity loft inset by `thickness` along X and Z
    inner_sections = []
    for y, w_base, z_base, w_roof, z_roof, z_crown in CANOPY_STATIONS:
        wb = max(w_base - thickness, 40.0)
        wr = max(w_roof - thickness, 35.0)
        zr = z_roof - thickness
        zc = z_crown - thickness
        zb = z_base - 35.0

        def pt(x, z, _y=y):
            return bd.Vector(x, _y, z)

        side_mid_x = 0.5 * (wb + wr) + 16.0
        side_mid_z = 0.5 * (z_base + zr) + 14.0
        shldr_x = wr * 0.88
        shldr_z = zr + (zc - zr) * 0.42

        edges = [
            bd.Edge.make_line(pt(-wb, zb), pt(wb, zb)),
            bd.Edge.make_line(pt(wb, zb), pt(wb, z_base)),
            bd.Edge.make_spline([
                pt(wb, z_base),
                pt(side_mid_x, side_mid_z),
                pt(wr, zr),
                pt(shldr_x, shldr_z),
                pt(0.0, zc),
                pt(-shldr_x, shldr_z),
                pt(-wr, zr),
                pt(-side_mid_x, side_mid_z),
                pt(-wb, z_base),
            ]),
            bd.Edge.make_line(pt(-wb, z_base), pt(-wb, zb)),
        ]
        inner_sections.append(bd.Face(bd.Wire(edges)))

    inner = bd.loft(inner_sections, ruled=False)
    # Trim both cleanly above master body beltline and subtract inner core
    shell = outer - inner
    return shell


def _door_glass_window_cut(side_sign, inset=0.0):
    """Volume capturing ONLY the side door glass below the A-pillar / roof rail."""
    # Follows the roof rail curve (x_roof + clearance) so the continuous glass
    # windshield + arched roof stay intact while the side door window swings up!
    door_prism = door_aperture_prism(side_sign, inset=inset)

    # Roof-rail inboard boundary slab: only cut glass OUTBOARD of the roof rail!
    # At Y = -880..+580, roof rail edge runs along |X| ~ 580 -> 495.
    pts_xy = [
        (side_sign * (615.0 + inset), -960.0),
        (side_sign * (582.0 + inset), -360.0),
        (side_sign * (560.0 + inset), -60.0),
        (side_sign * (535.0 + inset), 240.0),
        (side_sign * (505.0 + inset), 620.0),
        (side_sign * 1050.0, 620.0),
        (side_sign * 1050.0, -960.0),
    ]
    if side_sign < 0:
        pts_xy = list(reversed(pts_xy))
    face = bd.Face(bd.Wire.make_polygon([bd.Vector(x, y, 650.0) for x, y in pts_xy]))
    outboard = bd.extrude(face, 600.0, dir=(0, 0, 1))
    return door_prism & outboard


def _a_pillar_and_roof_rails():
    """Slim satin-titanium A-pillar & canopy header rails framing the Gold Glazed glass."""
    rails = []
    # Sweep crisp 16 x 14 mm architectural rails along left & right roof edges
    for side_lbl, sign in (("l", 1), ("r", -1)):
        pts = [
            bd.Vector(sign * (w_roof - 2.0), y, z_roof - 2.0)
            for y, _wb, _zb, w_roof, z_roof, _zc in CANOPY_STATIONS[:-1]
        ]
        path = bd.Wire(bd.Edge.make_spline(pts))
        start_dir = pts[1] - pts[0]
        prof = bd.Plane(origin=pts[0], z_dir=start_dir) * bd.Rectangle(18.0, 14.0)
        rail = bd.sweep(prof, path=path)
        rail.label = f"canopy_rail_{side_lbl}"
        apply_titanium(rail)
        rails.append(rail)
    return rails


def _interior_rearview_mirror():
    """Compact triangular-mounted interior rearview mirror hanging from windshield header."""
    # Triangular ceiling stem (per official 'Supersonic' interior shot!)
    stem_pts = [
        (-42.0, 0.0),
        (42.0, 0.0),
        (12.0, -52.0),
        (-12.0, -52.0),
    ]
    stem_face = bd.Face(bd.Wire.make_polygon([bd.Vector(x, -430.0, 1075.0 + z) for x, z in stem_pts]))
    stem = bd.extrude(stem_face, 16.0, dir=(0, 1, 0))
    stem.label = "mirror_mount"
    apply_alcantara(stem)

    housing = bd.Pos(0.0, -422.0, 1006.0) * bd.Box(182.0, 22.0, 48.0)
    housing.label = "rearview_mirror"
    apply_dark_gloss(housing)

    stem = stem - housing
    stem.label = "mirror_mount"
    apply_alcantara(stem)
    return stem, housing


@memo
def _build_canopy():
    body_oml = master_body_solid()
    glass_shell = _hollow_canopy_shell(thickness=14.0)

    # Keep only glass cleanly above the Ano White body deck
    # and carve out the left & right frameless door side windows
    win_cut_l = _door_glass_window_cut(1, inset=0.0)
    win_cut_r = _door_glass_window_cut(-1, inset=0.0)

    rails = _a_pillar_and_roof_rails()
    canopy_glass = glass_shell - [body_oml, win_cut_l, win_cut_r, *rails]
    canopy_glass.label = "gold_glazed_canopy"
    apply_gold_glass(canopy_glass)

    # Trim rails cleanly above the body deck so they seat flush on the cowl & buttresses
    trimmed_rails = []
    for r in rails:
        lbl = r.label
        tr = r - body_oml
        tr.label = lbl
        apply_titanium(tr)
        trimmed_rails.append(tr)

    mirror_mount, mirror = _interior_rearview_mirror()

    return bd.Compound(
        children=[canopy_glass, *trimmed_rails, mirror_mount, mirror],
        label="canopy",
    )


@model
def canopy():
    """Gold Glazed continuous windshield, roof, fastback glass, titanium rails & mirror."""
    return _build_canopy()


if __name__ == "__main__":
    canopy()
