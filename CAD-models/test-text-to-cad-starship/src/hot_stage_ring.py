"""SpaceX Super Heavy 1.8 m Vented Hot-Stage Ring (HSR).

Local frame:
- Z = 0: bottom flange mating plane (sits flush on Super Heavy top at Z = 69,200 mm).
- Z = 1800 mm: top docking flange mating plane (supports Starship aft skirt at Z = 71,000 mm).
- Outer radius = 4500 mm (9.0 m diameter).
"""

import math

import build123d as bd
from cad import model

from lib import dims
from lib.materials import (
    apply_dark_trim,
    apply_hot_stage_shield,
    apply_stainless_structural,
)


@model
def hot_stage_ring():
    """Vented hot-stage interstage ring with 24 structural pillars and internal blast deflector dome."""
    r_out = dims.HULL_R
    r_in = dims.HSR_IN_R
    h_tot = dims.HSR_HEIGHT
    h_bot = dims.HSR_BOT_FLANGE_H
    h_top = dims.HSR_TOP_FLANGE_H
    h_pillar = h_tot - h_bot - h_top

    # 1. Structural lower ring + upper docking ring + 24 radial vent pillars (one solid frame)
    bot_ring = bd.Cylinder(
        r_out, h_bot, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    ) - bd.Cylinder(
        r_in - 80.0, h_bot, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )

    top_ring = bd.Pos(0, 0, h_tot - h_top) * (
        bd.Cylinder(r_out, h_top, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        - bd.Cylinder(r_in - 60.0, h_top, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    )

    # 24 structural vent pillars around the perimeter (spaced every 15°)
    pillars = []
    pillar_rad_thick = dims.HSR_WALL
    pillar_r_center = r_in + pillar_rad_thick / 2.0
    for i in range(dims.HSR_PILLAR_COUNT):
        ang = i * (360.0 / dims.HSR_PILLAR_COUNT)
        # Slightly overlap top/bottom rings axially by 20 mm for rock-solid boolean fuse
        strut = (
            bd.Rot(0, 0, ang)
            * bd.Pos(pillar_r_center, 0, h_bot - 20.0)
            * bd.Box(
                pillar_rad_thick,
                dims.HSR_PILLAR_W,
                h_pillar + 40.0,
                align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
            )
        )
        pillars.append(strut)

    # Clip pillars cleanly to exact outer hull radius R = 4500 mm
    outer_clip = bd.Cylinder(r_out, h_tot, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    frame_raw = bot_ring.fuse(top_ring, *pillars)
    ring_frame = frame_raw & outer_clip
    ring_frame.label = "hsr_structural_frame"
    apply_stainless_structural(ring_frame)

    # 2. Internal convex exhaust blast deflector dome (deflects Starship Raptor plumes out the 24 vents)
    # Sits cleanly inside inner bore (R <= r_in - 85 mm -> clean 5 mm radial gap to bot_ring ledge)
    dome_r = r_in - 85.0
    dome_base_z = 80.0
    dome_peak_z = dims.HSR_DOME_PEAK_Z - dims.Z_HSR_BOT  # 1220.0 mm
    dome_t = 110.0

    with bd.BuildSketch(bd.Plane.XZ) as dome_sk:
        with bd.BuildLine():
            # Outer smooth dome arc from rim (dome_r, dome_base_z) to apex (0, dome_peak_z)
            # Midpoint raised smoothly for elliptical/spherical blast-cone shape
            mid_r = dome_r * 0.56
            mid_z = dome_base_z + (dome_peak_z - dome_base_z) * 0.72
            bd.ThreePointArc((dome_r, dome_base_z), (mid_r, mid_z), (0.0, dome_peak_z))
            bd.Line((0.0, dome_peak_z), (0.0, dome_peak_z - dome_t))
            bd.ThreePointArc(
                (0.0, dome_peak_z - dome_t),
                (mid_r - 15.0, mid_z - dome_t),
                (dome_r - dome_t, dome_base_z),
            )
            bd.Line((dome_r - dome_t, dome_base_z), (dome_r, dome_base_z))
        bd.make_face()

    blast_dome = bd.revolve(dome_sk.sketch, axis=bd.Axis.Z, revolution_arc=360)
    blast_dome.label = "blast_deflector_dome"
    apply_hot_stage_shield(blast_dome)

    # 3. Four external stage-separation hold-down clamp latches at 45°, 135°, 225°, 315°
    clamps = []
    hull_cut = bd.Cylinder(r_out, h_tot, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    for i, ang in enumerate((45.0, 135.0, 225.0, 315.0), start=1):
        # Conforms cleanly to outer cylinder radius R = 4500 mm with zero overlap and zero corner gap
        raw_clamp = (
            bd.Rot(0, 0, ang)
            * bd.Pos(r_out - 40.0, 0, h_tot - h_top)
            * bd.Box(180.0, 420.0, h_top, align=(bd.Align.MIN, bd.Align.CENTER, bd.Align.MIN))
        )
        clamp = raw_clamp - hull_cut
        clamp.label = f"stage_clamp_{i}"
        apply_dark_trim(clamp)
        clamps.append(clamp)

    hsr = bd.Compound(children=[ring_frame, blast_dome, *clamps], label="hot_stage_ring")
    bb = hsr.bounding_box()
    assert abs(bb.size.Z - dims.HSR_HEIGHT) < 1.0, bb.size
    return hsr


if __name__ == "__main__":
    hot_stage_ring()
