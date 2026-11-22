"""SpaceX Super Heavy Booster (Block 1 / Flight 5 configuration, 71.0 m tall with Hot-Stage Ring).

Exports:
- `super_heavy_core`: Rigid booster structure + 33 Raptor 2 SL engines + Hot-Stage Ring (Z = 0 .. 71,000 mm).
- `super_heavy_booster`: Complete Super Heavy Booster with 4 articulated waffle grid fins.
"""

import math

import build123d as bd
from cad import model
from cad.build123d import mechanism_state, memo

from grid_fin import grid_fin
from hot_stage_ring import hot_stage_ring
from lib import dims
from lib.materials import (
    apply_dark_trim,
    apply_grid_fin_steel,
    apply_hot_stage_shield,
    apply_stainless_304l,
    apply_stainless_structural,
)
from raptor import raptor_sl


@memo
def _build_booster_hull():
    """Revolve the 9.0 m diameter Super Heavy stainless tank barrel with subtle ring-weld seams."""
    r_out = dims.HULL_R
    r_in = dims.SH_SKIRT_IN_R
    z_bot = dims.Z_SH_SKIRT_BOT
    z_deck = dims.Z_SH_THRUST_DECK
    z_top = dims.Z_SH_BODY_TOP

    # Subtle chamfered barrel ring weld seams every 3.6 m along the main tank wall
    groove_d = dims.WELD_GROOVE_DEPTH
    groove_hh = dims.WELD_GROOVE_HALF_H
    seam_zs = []
    z_s = 6800.0
    while z_s <= z_top - 2200.0:
        seam_zs.append(z_s)
        z_s += dims.RING_STEP

    pts = [
        (r_in, z_bot),
        (r_out, z_bot),
    ]
    for zc in seam_zs:
        pts.append((r_out, zc - groove_hh))
        pts.append((r_out - groove_d, zc))
        pts.append((r_out, zc + groove_hh))
    pts.extend(
        [
            (r_out, z_top),
            (0.0, z_top),
            (0.0, z_deck),
            (r_in, z_deck),
        ]
    )

    with bd.BuildSketch(bd.Plane.XZ) as sk:
        bd.Polygon(*pts, align=None)
    hull = bd.revolve(sk.sketch, axis=bd.Axis.Z, revolution_arc=360)
    hull.label = "booster_tank_hull"
    apply_stainless_304l(hull)
    return hull


def _build_aft_cuff_and_baffle():
    """Build the lower aft engine protective cuff and internal 20/13 engine bay heatshield divider."""
    r_out = dims.HULL_R
    z_bot = dims.Z_SH_SKIRT_BOT
    z_cuff_top = 2400.0
    cuff_t = 45.0

    # Tapered aft protective apron cuff hugging R = 4500..4545 from Z = 400 to 2400
    cuff_pts = [
        (r_out, z_bot),
        (r_out + cuff_t, z_bot),
        (r_out + cuff_t, z_cuff_top - 120.0),
        (r_out, z_cuff_top),
    ]
    with bd.BuildSketch(bd.Plane.XZ) as cuff_sk:
        bd.Polygon(*cuff_pts, align=None)
    aft_cuff = bd.revolve(cuff_sk.sketch, axis=bd.Axis.Z, revolution_arc=360)
    aft_cuff.label = "aft_heatshield_cuff"
    apply_stainless_structural(aft_cuff)

    # Internal circular heatshield baffle separating outer 20 boost engines from inner 13 gimbal engines
    baffle_z_bot = 850.0
    baffle_h = dims.Z_SH_THRUST_DECK - baffle_z_bot
    r_div = dims.SH_DIVIDER_RING_R
    baffle = bd.Pos(0, 0, baffle_z_bot) * (
        bd.Cylinder(r_div + 40.0, baffle_h, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        - bd.Cylinder(r_div - 40.0, baffle_h, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    )
    baffle.label = "engine_bay_divider"
    apply_hot_stage_shield(baffle)

    return aft_cuff, baffle


def _build_chines_and_raceway():
    """Build the 2 long ±X COPV aerodynamic chines and the +Y avionics/propellant raceway + BQD."""
    r_out = dims.HULL_R
    hull_clip = bd.Pos(0, 0, dims.Z_SH_SKIRT_BOT) * bd.Cylinder(
        r_out,
        dims.Z_SH_BODY_TOP - dims.Z_SH_SKIRT_BOT,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )

    parts = []
    # Two streamlined COPV / manifold chines on +X (0°) and -X (180°)
    z0 = 2450.0  # Starts cleanly above aft cuff (2400 mm)
    z1 = dims.CHINE_Z_TOP
    h_chine = z1 - z0
    w_base = dims.CHINE_WIDTH
    w_top = 620.0
    protr = dims.CHINE_PROTRUSION

    # Build chine cross-section on XY plane (extending outward along +X from R-120 to R+protr)
    # Tapered at top (Z = z1 - 2400..z1) and bottom (Z = z0..z0 + 900) via clean lofted sections
    def _chine_section(z_level: float, scale_w: float, scale_p: float):
        x_in = r_out - 120.0
        x_out = r_out + protr * scale_p
        wb = w_base * scale_w / 2.0
        wt = w_top * scale_w / 2.0
        pts = [
            (x_in, -wb),
            (x_out, -wt),
            (x_out, wt),
            (x_in, wb),
        ]
        with bd.BuildSketch(bd.Plane.XY.offset(z_level)) as sk:
            bd.Polygon(*pts, align=None)
        return sk.sketch

    chine_raw = bd.loft(
        [
            _chine_section(z0, 0.45, 0.08),
            _chine_section(z0 + 1100.0, 1.0, 1.0),
            _chine_section(z1 - 2600.0, 1.0, 1.0),
            _chine_section(z1, 0.30, 0.06),
        ],
        ruled=True,
    )
    chine_stbd = chine_raw - hull_clip
    chine_stbd.label = "chine_starboard"
    apply_stainless_structural(chine_stbd)

    chine_port = bd.Rot(0, 0, 180) * chine_stbd
    chine_port.label = "chine_port"
    parts.extend([chine_stbd, chine_port])

    # +Y Leeward avionics/propellant raceway + Booster Quick Disconnect (BQD) panel
    rw_z0 = 2450.0
    rw_z1 = dims.Z_SH_BODY_TOP - 250.0
    rw_pts = [
        (-280.0, r_out - 80.0),
        (280.0, r_out - 80.0),
        (170.0, r_out + 250.0),
        (-170.0, r_out + 250.0),
    ]
    with bd.BuildSketch(bd.Plane.XY.offset(rw_z0)) as rw_sk:
        bd.Polygon(*rw_pts, align=None)
    rw_body = bd.extrude(rw_sk.sketch, amount=rw_z1 - rw_z0)

    # BQD umbilical housing integrated cleanly into the lower raceway (Z = 4800..6600)
    bqd_box = bd.Pos(0, r_out + 180.0, 5700.0) * bd.Box(740.0, 320.0, 1750.0)
    raceway = rw_body.fuse(bqd_box) - hull_clip
    raceway.label = "booster_raceway_and_bqd"
    apply_dark_trim(raceway)
    parts.append(raceway)

    return parts


def _build_catch_pins_and_actuators():
    """Build the 2 ±X Mechazilla catch pins and 4 asymmetric grid-fin actuator housings."""
    r_out = dims.HULL_R
    hull_clip = bd.Pos(0, 0, 58000.0) * bd.Cylinder(
        r_out,
        dims.Z_SH_BODY_TOP - 58000.0,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )

    parts = []

    # 1. Two heavy Mechazilla lifting / catch pins at +X (0°) and -X (180°)
    z_pin = dims.SH_CATCH_PIN_Z
    # Load-spreader doubler pad + heavy cylindrical shaft + rounded catch stop collar
    pad = bd.Pos(r_out - 120.0, 0, z_pin) * bd.Box(
        220.0, 1300.0, 2000.0, align=(bd.Align.MIN, bd.Align.CENTER, bd.Align.CENTER)
    )
    shaft = (
        bd.Pos(r_out, 0, z_pin)
        * bd.Rot(0, 90, 0)
        * bd.Cylinder(
            dims.SH_CATCH_PIN_R,
            dims.SH_CATCH_PIN_LEN - 120.0,
            align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
        )
    )
    tip_collar = (
        bd.Pos(r_out + dims.SH_CATCH_PIN_LEN - 260.0, 0, z_pin)
        * bd.Rot(0, 90, 0)
        * bd.Cylinder(
            dims.SH_CATCH_PIN_R + 75.0,
            190.0,
            align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
        )
    )
    tip_cap = bd.Pos(r_out + dims.SH_CATCH_PIN_LEN - 70.0, 0, z_pin) * bd.Sphere(
        dims.SH_CATCH_PIN_R + 30.0
    )
    pin_stbd = pad.fuse(shaft, tip_collar, tip_cap) - hull_clip
    pin_stbd.label = "catch_pin_starboard"
    apply_grid_fin_steel(pin_stbd)

    pin_port = bd.Rot(0, 0, 180) * pin_stbd
    pin_port.label = "catch_pin_port"
    parts.extend([pin_stbd, pin_port])

    # 2. Four streamlined grid fin actuator gearbox blisters at 60°, 120°, 240°, 300°
    # Each housing terminates in a crisp vertical circular boss face at R = HULL_R + GRID_FIN_ROOT_OFFSET (4960 mm)
    z_gf = dims.GRID_FIN_Z
    r_pivot = r_out + dims.GRID_FIN_ROOT_OFFSET  # 4960.0 mm

    def _act_section(z_off: float, w_y: float, x_reach: float):
        x0 = r_out - 140.0
        pts = [
            (x0, -w_y / 2.0),
            (x_reach, -w_y * 0.34),
            (x_reach, w_y * 0.34),
            (x0, w_y / 2.0),
        ]
        with bd.BuildSketch(bd.Plane.XY.offset(z_gf + z_off)) as sk:
            bd.Polygon(*pts, align=None)
        return sk.sketch

    blister = bd.loft(
        [
            _act_section(-1350.0, 900.0, r_out + 80.0),
            _act_section(-750.0, 1550.0, r_pivot - 110.0),
            _act_section(750.0, 1550.0, r_pivot - 110.0),
            _act_section(1350.0, 900.0, r_out + 80.0),
        ],
        ruled=True,
    )
    # Cylindrical actuator pivot hub extending cleanly to exact plane X = r_pivot (4960 mm)
    hub_cyl = (
        bd.Pos(r_out - 50.0, 0, z_gf)
        * bd.Rot(0, 90, 0)
        * bd.Cylinder(
            335.0,
            dims.GRID_FIN_ROOT_OFFSET + 50.0,
            align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
        )
    )
    act_proto = blister.fuse(hub_cyl) - hull_clip
    apply_stainless_structural(act_proto)

    for idx, ang in enumerate(dims.GRID_FIN_ANGLES_DEG, start=1):
        act = bd.Rot(0, 0, ang) * act_proto
        act.label = f"grid_fin_actuator_{idx}"
        parts.append(act)

    return parts


def _build_33_raptor_cluster(sl_shape):
    """Arrange 33 Raptor 2 Sea-Level engines (20 outer + 10 middle + 3 center) inside the booster skirt."""
    outer = []
    for i in range(dims.SH_OUTER_COUNT):
        ang = i * (360.0 / dims.SH_OUTER_COUNT)
        rad = math.radians(ang)
        x = dims.SH_OUTER_RING_R * math.cos(rad)
        y = dims.SH_OUTER_RING_R * math.sin(rad)
        eng = bd.Pos(x, y, dims.Z_NOZZLE_EXIT) * bd.Rot(0, 0, ang) * sl_shape
        eng.label = f"raptor_outer_{i + 1:02d}"
        outer.append(eng)

    mid = []
    for i in range(dims.SH_MID_COUNT):
        ang = 9.0 + i * (360.0 / dims.SH_MID_COUNT)
        rad = math.radians(ang)
        x = dims.SH_MID_RING_R * math.cos(rad)
        y = dims.SH_MID_RING_R * math.sin(rad)
        eng = bd.Pos(x, y, dims.Z_NOZZLE_EXIT) * bd.Rot(0, 0, ang) * sl_shape
        eng.label = f"raptor_mid_{i + 1:02d}"
        mid.append(eng)

    inner = []
    for i in range(dims.SH_INNER_COUNT):
        ang = i * (360.0 / dims.SH_INNER_COUNT)
        rad = math.radians(ang)
        x = dims.SH_INNER_RING_R * math.cos(rad)
        y = dims.SH_INNER_RING_R * math.sin(rad)
        eng = bd.Pos(x, y, dims.Z_NOZZLE_EXIT) * bd.Rot(0, 0, ang) * sl_shape
        eng.label = f"raptor_center_{i + 1:02d}"
        inner.append(eng)

    return bd.Compound(
        children=[
            bd.Compound(children=outer, label="outer_ring_20"),
            bd.Compound(children=mid, label="middle_ring_10"),
            bd.Compound(children=inner, label="center_cluster_3"),
        ],
        label="raptor_33_cluster",
    )


@model
def super_heavy_core():
    """Super Heavy rigid booster core (hull, 33 Raptor 2 engines, chines, catch pins, actuators, HSR)."""
    hull = _build_booster_hull()
    aft_cuff, baffle = _build_aft_cuff_and_baffle()
    chines_rw = _build_chines_and_raceway()
    pins_acts = _build_catch_pins_and_actuators()
    engines = _build_33_raptor_cluster(raptor_sl().shape)

    hsr = bd.Pos(0, 0, dims.Z_HSR_BOT) * hot_stage_ring().shape
    hsr.label = "hot_stage_ring"

    core = bd.Compound(
        children=[hull, aft_cuff, baffle, *chines_rw, *pins_acts, engines, hsr],
        label="super_heavy_core",
    )
    bb = core.bounding_box()
    assert abs(bb.min.Z - dims.Z_NOZZLE_EXIT) < 1.0, bb
    assert abs(bb.max.Z - dims.Z_HSR_TOP) < 1.0, bb
    return core


def attach_grid_fins(core, fin_proto):
    """Place and hinge-connect the 4 Super Heavy waffle grid fins onto `core` via RevoluteJoints."""
    r_pivot = dims.HULL_R + dims.GRID_FIN_ROOT_OFFSET
    z_gf = dims.GRID_FIN_Z
    fins = []
    for idx, ang in enumerate(dims.GRID_FIN_ANGLES_DEG, start=1):
        rad = math.radians(ang)
        ux, uy = math.cos(rad), math.sin(rad)
        px, py = r_pivot * ux, r_pivot * uy

        fin = bd.Pos(px, py, z_gf) * bd.Rot(0, 0, ang) * fin_proto
        fin.label = f"grid_fin_{idx}"

        jname = f"grid_fin_{idx}"
        axis = bd.Axis((px, py, z_gf), (ux, uy, 0.0))
        hinge = bd.RevoluteJoint(jname, core, axis=axis, angular_range=(-30.0, 30.0))
        bd.RigidJoint(jname, fin, hinge.location)
        hinge.connect_to(fin.joints[jname], angle=0.0)
        fins.append(fin)
    return fins


@model
def super_heavy_booster():
    """Complete SpaceX Super Heavy Booster (71.0 m) with 4 articulated waffle grid fins."""
    core = super_heavy_core().shape
    fins = attach_grid_fins(core, grid_fin().shape)
    booster = bd.Compound(children=[core, *fins], label="super_heavy_booster")
    mechanism_state(
        booster,
        "ascent_neutral",
        grid_fin_1=0.0,
        grid_fin_2=0.0,
        grid_fin_3=0.0,
        grid_fin_4=0.0,
    )
    mechanism_state(
        booster,
        "descent_pitch",
        grid_fin_1=22.0,
        grid_fin_2=-22.0,
        grid_fin_3=-22.0,
        grid_fin_4=22.0,
    )
    return booster


if __name__ == "__main__":
    super_heavy_booster()
