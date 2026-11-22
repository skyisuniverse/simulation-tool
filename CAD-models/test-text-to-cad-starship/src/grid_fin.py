"""Super Heavy Booster welded steel waffle grid fin.

Local frame:
- Origin (0, 0, 0): pivot shoulder face mating flush to the booster actuator housing.
- +X: radially outward along the fin span (X = 0 .. GRID_FIN_SPAN).
- ±Y: tangential fin width (tapers from GRID_FIN_ROOT_WIDTH at root to GRID_FIN_WIDTH at tip).
- ±Z: axial lattice depth (-GRID_FIN_DEPTH/2 .. +GRID_FIN_DEPTH/2).
- Pitch rotation occurs cleanly about the local X axis (Axis.X).
"""

import build123d as bd
from cad import model

from lib import dims
from lib.materials import apply_grid_fin_steel, apply_stainless_structural


def _trapezoid_face(x0: float, x1: float, w0: float, w1: float, fillet_r: float):
    """Create a symmetric rounded trapezoidal 2D face on the XY plane."""
    pts = [
        (x0, -w0 / 2.0),
        (x1, -w1 / 2.0),
        (x1, w1 / 2.0),
        (x0, w0 / 2.0),
    ]
    with bd.BuildSketch(bd.Plane.XY) as sk:
        bd.Polygon(*pts, align=None)
        if fillet_r > 0:
            bd.fillet(sk.vertices(), radius=fillet_r)
    return sk.sketch


@model
def grid_fin():
    """Super Heavy waffle grid fin with diagonal diamond lattice and pivot yoke."""
    hub_len = 260.0  # Root structural yoke length from X=0 to waffle frame start
    x_start = hub_len
    x_end = dims.GRID_FIN_SPAN
    w_root = dims.GRID_FIN_ROOT_WIDTH
    w_tip = dims.GRID_FIN_WIDTH
    depth = dims.GRID_FIN_DEPTH
    frame_t = dims.GRID_FIN_FRAME_T
    rib_t = dims.GRID_FIN_RIB_T

    # 1. Outer perimeter frame (hollow rounded trapezoid extruded along Z)
    outer_sk = _trapezoid_face(x_start, x_end, w_root, w_tip, fillet_r=260.0)
    inner_sk = _trapezoid_face(
        x_start + frame_t,
        x_end - frame_t,
        w_root - 2.0 * frame_t,
        w_tip - 2.0 * frame_t,
        fillet_r=max(40.0, 260.0 - frame_t),
    )

    frame_2d = outer_sk - inner_sk
    outer_frame = bd.extrude(frame_2d, amount=depth / 2.0, both=True)

    # 2. Diagonal ±45° waffle lattice clipped to inner aperture (slightly overlapping frame by 20 mm for clean fuse)
    clip_sk = _trapezoid_face(
        x_start + frame_t * 0.6,
        x_end - frame_t * 0.6,
        w_root - 1.2 * frame_t,
        w_tip - 1.2 * frame_t,
        fillet_r=max(40.0, 260.0 - frame_t * 0.6),
    )
    clip_solid = bd.extrude(clip_sk, amount=(depth - 40.0) / 2.0, both=True)

    # Generate diagonal rib bars in ±45° directions centered on fin midpoint
    x_mid = 0.5 * (x_start + x_end)
    bar_len = 5600.0
    pitch = 620.0  # Crisp ~440 mm diamond cells (authentic Super Heavy open waffle look)
    rib_h = depth - 40.0

    ribs = []
    for angle in (45.0, -45.0):
        for idx in range(-4, 5):
            offset = idx * pitch
            bar = (
                bd.Pos(x_mid, 0, 0)
                * bd.Rot(0, 0, angle)
                * bd.Pos(0, offset, 0)
                * bd.Box(bar_len, rib_t, rib_h)
            )
            ribs.append(bar)

    raw_lattice = ribs[0].fuse(*ribs[1:])
    clipped_lattice = raw_lattice & clip_solid

    # 3. Root structural clevis / load spreader yoke connecting pivot shaft (X=0) to frame (X=hub_len)
    # Tapered solid collar + gusset block into frame root (starts behind 75 mm pivot flange)
    yoke = (
        bd.Pos(0, 0, 0)
        * bd.Rot(0, 90, 0)
        * bd.Cylinder(235.0, hub_len + frame_t * 0.6, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    )
    flange_len = 75.0
    web_len = (hub_len - flange_len) + frame_t * 0.6
    root_web = bd.Pos(flange_len, 0, 0) * bd.Box(
        web_len,
        1150.0,
        depth * 0.72,
        align=(bd.Align.MIN, bd.Align.CENTER, bd.Align.CENTER),
    )

    fin_body = outer_frame.fuse(clipped_lattice, yoke, root_web)
    fin_body.label = "waffle_blade"
    apply_grid_fin_steel(fin_body)

    # 4. Precision pivot flange collar at X = 0 (flush mating face with actuator housing)
    flange = (
        bd.Pos(0, 0, 0)
        * bd.Rot(0, 90, 0)
        * bd.Cylinder(275.0, flange_len, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    )
    # Cut flange overlap with yoke by making flange an outer collar (R = 235..275)
    flange_ring = flange - (
        bd.Pos(0, 0, 0)
        * bd.Rot(0, 90, 0)
        * bd.Cylinder(235.0, flange_len, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    )
    flange_ring.label = "pivot_collar"
    apply_stainless_structural(flange_ring)

    assembly = bd.Compound(children=[fin_body, flange_ring], label="grid_fin")
    bb = assembly.bounding_box()
    assert abs(bb.min.X) < 1.0, bb
    assert abs(bb.max.X - dims.GRID_FIN_SPAN) < 5.0, bb
    return assembly


if __name__ == "__main__":
    grid_fin()
