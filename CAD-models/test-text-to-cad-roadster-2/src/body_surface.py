"""Shared Class-A outer body loft, canopy mold-line, and exact cutting volumes.

Every exterior module (chassis, body, doors, canopy) derives its mating faces
from these exact shared solids so panel shutlines, rocker seams, wheel arches,
and canopy glass edges align to sub-millimetre precision with zero interference.
"""

import build123d as bd
from cad import model
from cad.build123d import memo

from spec import (
    ARCH_F_RADIUS,
    ARCH_R_RADIUS,
    BODY_STATIONS,
    CANOPY_STATIONS,
    DOOR_GAP,
    DOOR_Y_FRONT_BOT,
    DOOR_Y_FRONT_TOP,
    DOOR_Y_REAR_BOT,
    DOOR_Y_REAR_TOP,
    TIRE_F_RADIUS,
    TIRE_R_RADIUS,
    Y_FRONT_AXLE,
    Y_NOSE,
    Y_REAR_AXLE,
    Y_TAIL,
    apply_ano_white,
    apply_gold_glass,
)


def _body_section_face(row):
    """Build one symmetric 10-edge XZ cross-section face at longitudinal Y."""
    (
        y,
        x_flr, z_flr,
        x_rck, z_rck,
        x_shd, z_shd,
        x_rdg, z_rdg,
        x_dck, z_dck,
        z_ctr,
        f_bow, t_bow,
    ) = row

    def pt(x, z):
        return bd.Vector(x, y, z)

    flank_mid_x = 0.5 * (x_rck + x_shd) + f_bow
    flank_mid_z = 0.5 * (z_rck + z_shd) + 8.0
    top_mid_x = 0.5 * (x_shd + x_rdg) + 4.0
    top_mid_z = 0.5 * (z_shd + z_rdg) + t_bow

    edges = [
        bd.Edge.make_line(pt(-x_flr, z_flr), pt(x_flr, z_flr)),
        bd.Edge.make_line(pt(x_flr, z_flr), pt(x_rck, z_rck)),
        bd.Edge.make_spline([
            pt(x_rck, z_rck),
            pt(flank_mid_x, flank_mid_z),
            pt(x_shd, z_shd),
        ]),
        bd.Edge.make_spline([
            pt(x_shd, z_shd),
            pt(top_mid_x, top_mid_z),
            pt(x_rdg, z_rdg),
        ]),
        bd.Edge.make_line(pt(x_rdg, z_rdg), pt(x_dck, z_dck)),
        bd.Edge.make_spline([
            pt(x_dck, z_dck),
            pt(0.0, z_ctr),
            pt(-x_dck, z_dck),
        ]),
        bd.Edge.make_line(pt(-x_dck, z_dck), pt(-x_rdg, z_rdg)),
        bd.Edge.make_spline([
            pt(-x_rdg, z_rdg),
            pt(-top_mid_x, top_mid_z),
            pt(-x_shd, z_shd),
        ]),
        bd.Edge.make_spline([
            pt(-x_shd, z_shd),
            pt(-flank_mid_x, flank_mid_z),
            pt(-x_rck, z_rck),
        ]),
        bd.Edge.make_line(pt(-x_rck, z_rck), pt(-x_flr, z_flr)),
    ]
    return bd.Face(bd.Wire(edges))


def _nose_and_tail_trim_prism():
    """Exact plan-view trapezoidal nose sweep + Kamm-tail overhang volume."""
    # Center DRL leading edge is straight across |X| <= 565 at Y = Y_NOSE;
    # outer fender noses sweep crisply back by ~145 mm toward the outer corners
    # for the iconic dart-wedge front 3/4 silhouette.
    pts_plan = [
        (-1100.0, Y_NOSE + 160.0),
        (-565.0, Y_NOSE),
        (565.0, Y_NOSE),
        (1100.0, Y_NOSE + 160.0),
        (1100.0, Y_TAIL + 200.0),
        (-1100.0, Y_TAIL + 200.0),
    ]
    plan_face = bd.Face(bd.Wire.make_polygon([bd.Vector(x, y, 0.0) for x, y in pts_plan]))
    plan_prism = bd.extrude(plan_face, 1400.0, dir=(0, 0, 1))

    # Gentle clean side-view rake at front nose (keeps cheeks crisp & facet-free)
    # and authentic Kamm-tail undercut at the rear.
    pts_side = [
        (Y_NOSE + 32.0, 0.0),
        (Y_NOSE + 24.0, 200.0),
        (Y_NOSE, 420.0),
        (Y_NOSE - 30.0, 1300.0),
        (Y_TAIL + 20.0, 1300.0),
        (Y_TAIL, 825.0),
        (Y_TAIL - 22.0, 690.0),
        (Y_TAIL - 50.0, 480.0),
        (Y_TAIL - 82.0, 190.0),
        (Y_TAIL - 95.0, 0.0),
    ]
    side_face = bd.Face(bd.Wire.make_polygon([bd.Vector(-1200.0, y, z) for y, z in pts_side]))
    side_prism = bd.extrude(side_face, 2400.0, dir=(1, 0, 0))
    return plan_prism & side_prism


@memo
def master_body_solid():
    """Watertight Class-A outer mold-line solid of the Roadster lower body."""
    sections = [_body_section_face(row) for row in BODY_STATIONS]
    raw_loft = bd.loft(sections, ruled=False)
    trimmed = raw_loft & _nose_and_tail_trim_prism()
    solids = trimmed.solids()
    assert len(solids) == 1, f"Expected 1 master body solid, got {len(solids)}"
    body = solids[0]
    assert body.is_valid, "Master body solid is invalid"
    return body


def _canopy_section_face(row):
    """Build one smooth arched XZ canopy section (rounded fighter-jet dome)."""
    y, w_base, z_base, w_roof, z_roof, z_crown = row

    def pt(x, z):
        return bd.Vector(x, y, z)

    # Smooth continuous spline from +X base over arched roof dome to -X base
    # gives realistic rounded shoulders matching the straight-on front view.
    side_mid_x = 0.5 * (w_base + w_roof) + 18.0
    side_mid_z = 0.5 * (z_base + z_roof) + 16.0
    shldr_x = w_roof * 0.88
    shldr_z = z_roof + (z_crown - z_roof) * 0.42
    z_seat = z_base - 28.0

    edges = [
        bd.Edge.make_line(pt(-w_base, z_seat), pt(w_base, z_seat)),
        bd.Edge.make_line(pt(w_base, z_seat), pt(w_base, z_base)),
        bd.Edge.make_spline([
            pt(w_base, z_base),
            pt(side_mid_x, side_mid_z),
            pt(w_roof, z_roof),
            pt(shldr_x, shldr_z),
            pt(0.0, z_crown),
            pt(-shldr_x, shldr_z),
            pt(-w_roof, z_roof),
            pt(-side_mid_x, side_mid_z),
            pt(-w_base, z_base),
        ]),
        bd.Edge.make_line(pt(-w_base, z_base), pt(-w_base, z_seat)),
    ]
    return bd.Face(bd.Wire(edges))


@memo
def master_canopy_solid():
    """Smooth teardrop fighter-jet canopy outer solid."""
    sections = [_canopy_section_face(row) for row in CANOPY_STATIONS]
    canopy = bd.loft(sections, ruled=False)
    assert canopy.is_valid, "Master canopy solid is invalid"
    return canopy


def rocker_split_volume():
    """Solid volume occupying everything BELOW the rising matte-black rocker line.

    Cutting this volume from the master body leaves the Ano White upper body;
    intersecting it with the master body yields the flush Carbon Black lower
    rocker skirt & rear aero apron with zero overlap and zero z-fighting.
    """
    pts_yz = [
        (Y_NOSE - 120.0, 0.0),
        (Y_TAIL + 120.0, 0.0),
        (Y_TAIL + 120.0, 495.0),
        (Y_REAR_AXLE + 420.0, 455.0),
        (Y_REAR_AXLE + 280.0, 390.0),
        (Y_REAR_AXLE - 380.0, 340.0),
        (DOOR_Y_REAR_BOT + 180.0, 275.0),
        (DOOR_Y_REAR_BOT, 240.0),
        (DOOR_Y_FRONT_BOT, 212.0),
        (Y_FRONT_AXLE, 204.0),
        (Y_NOSE - 120.0, 198.0),
    ]
    face = bd.Face(bd.Wire.make_polygon([bd.Vector(-1200.0, y, z) for y, z in pts_yz]))
    return bd.extrude(face, 2400.0, dir=(1, 0, 0))


def front_trapezoid_intake_cut():
    """Shared trapezoidal front intake cutout between the two front fender cheeks."""
    pts_xz = [
        (-705.0, 175.0),
        (705.0, 175.0),
        (565.0, 404.0),
        (-565.0, 404.0),
    ]
    face = bd.Face(bd.Wire.make_polygon([bd.Vector(x, Y_NOSE - 30.0, z) for x, z in pts_xz]))
    return bd.extrude(face, 145.0, dir=(0, 1, 0))


def wheel_arch_cutters(extra_r=0.0, extra_depth=0.0):
    """List of 4 cylindrical wheel-arch cutting tools (FL, FR, RL, RR)."""
    cutters = []
    # Front arches: inboard to X = ±665 mm (clears 295 tire inner wall at 673 mm
    # without breaking through the recessed hood crease at X = 616 mm!)
    r_f = ARCH_F_RADIUS + extra_r
    depth_f = 395.0 + extra_depth
    for sign in (1, -1):
        cyl = bd.Cylinder(r_f, depth_f)
        cyl = bd.Rot(0, 90, 0) * cyl
        cyl = bd.Pos(sign * (1060.0 - depth_f / 2.0), Y_FRONT_AXLE, TIRE_F_RADIUS) * cyl
        cutters.append(cyl)
    # Rear arches: inboard to X = ±610 mm (generously clears 335 tire inner wall at 647 mm!)
    r_r = ARCH_R_RADIUS + extra_r
    depth_r = 450.0 + extra_depth
    for sign in (1, -1):
        cyl = bd.Cylinder(r_r, depth_r)
        cyl = bd.Rot(0, 90, 0) * cyl
        cyl = bd.Pos(sign * (1060.0 - depth_r / 2.0), Y_REAR_AXLE, TIRE_R_RADIUS) * cyl
        cutters.append(cyl)
    return cutters


def door_aperture_prism(side_sign, inset=0.0):
    """Exact prism bounding the left (+1) or right (-1) butterfly door opening.

    Analytic linear shutline edges guarantee `inset > 0` stays strictly inside
    `inset == 0` at EVERY height Z, ensuring crisp shutlines and zero clash.
    """
    # Front shutline: Y(200) = DOOR_Y_FRONT_BOT (-965), Y(745) = DOOR_Y_FRONT_TOP (-875)
    # Rear shutline : Y(200) = DOOR_Y_REAR_BOT  (+445), Y(865) = DOOR_Y_REAR_TOP  (+570)
    def y_front(z):
        return DOOR_Y_FRONT_BOT + (DOOR_Y_FRONT_TOP - DOOR_Y_FRONT_BOT) * (z - 200.0) / 545.0 + inset

    def y_rear(z):
        return DOOR_Y_REAR_BOT + (DOOR_Y_REAR_TOP - DOOR_Y_REAR_BOT) * (z - 200.0) / 665.0 - inset

    if inset == 0.0:
        z_bot_f, z_bot_r = 180.0, 205.0
    else:
        z_bot_f, z_bot_r = 224.0 + inset, 248.0 + inset

    pts_yz = [
        (y_front(z_bot_f), z_bot_f),
        (y_rear(z_bot_r), z_bot_r),
        (y_rear(865.0), 865.0),
        (y_rear(865.0) - 40.0, 1220.0),
        (y_front(745.0) + 20.0, 1220.0),
        (y_front(745.0), 745.0),
    ]
    x_start = side_sign * 420.0 if side_sign > 0 else -1120.0
    width = 700.0
    face = bd.Face(bd.Wire.make_polygon([bd.Vector(x_start, y, z) for y, z in pts_yz]))
    return bd.extrude(face, width, dir=(1, 0, 0))


def cockpit_interior_cavity():
    """Large recessed interior cabin cavity carved inside the body & canopy."""
    pts_yz = [
        (-960.0, 210.0),
        (560.0, 210.0),
        (680.0, 740.0),
        (500.0, 1080.0),
        (-300.0, 1080.0),
        (-1020.0, 680.0),
    ]
    face = bd.Face(bd.Wire.make_polygon([bd.Vector(-740.0, y, z) for y, z in pts_yz]))
    return bd.extrude(face, 1480.0, dir=(1, 0, 0))


@model
def envelope_preview():
    """Diagnostic model showing the untrimmed-detail master body + canopy mold lines."""
    body = master_body_solid()
    body.label = "master_body"
    apply_ano_white(body)

    canopy = master_canopy_solid() - body
    canopy.label = "master_canopy"
    apply_gold_glass(canopy)

    return bd.Compound(children=[body, canopy], label="roadster_envelope")


if __name__ == "__main__":
    envelope_preview()
