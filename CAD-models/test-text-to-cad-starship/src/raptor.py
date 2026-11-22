"""Parametric SpaceX Raptor 2 Sea-Level (SL) and Raptor Vacuum (RVac) rocket engines.

Local frame for both engines:
- Z = 0: nozzle exit rim plane.
- Z = height (3100 mm SL, 3900 mm RVac): top gimbal/thrust-deck mating plane.
- Centered on the Z axis.
"""

import math

import build123d as bd
from cad import model

from lib import dims
from lib.materials import (
    apply_raptor_copper,
    apply_raptor_nozzle,
    apply_stainless_structural,
)


def _parabolic_bell_and_chamber(
    total_h: float,
    bell_h: float,
    exit_r: float,
    throat_r: float,
    wall_t: float,
    chamber_r: float,
    gimbal_r: float,
    hoop_fracs: tuple[float, ...],
):
    """Build a smooth revolved hollow parabolic bell nozzle + MCC + gimbal collar."""
    # Bell outer contour: smooth ThreePointArc from exit rim (exit_r, 0) up to throat (throat_r, bell_h)
    # Control midpoint bulges slightly outward like a real Rao-optimum parabolic bell!
    mid_z = bell_h * 0.46
    mid_r = throat_r + (exit_r - throat_r) * 0.68

    # Inner bell wall offset inward by wall_t
    in_exit_r = exit_r - wall_t
    in_mid_r = mid_r - wall_t * 0.85
    in_throat_r = max(45.0, throat_r - wall_t * 1.1)

    chamber_top_z = total_h - 420.0
    gimbal_bot_z = total_h - 240.0

    with bd.BuildSketch(bd.Plane.XZ) as profile:
        with bd.BuildLine() as ln:
            # Bottom nozzle lip (Z = 0)
            bd.Line((in_exit_r, 0.0), (exit_r, 0.0))
            # Outer parabolic bell up to throat
            bd.ThreePointArc((exit_r, 0.0), (mid_r, mid_z), (throat_r, bell_h))
            # Diverging into Main Combustion Chamber (MCC)
            bd.Line((throat_r, bell_h), (chamber_r, bell_h + 260.0))
            bd.Line((chamber_r, bell_h + 260.0), (chamber_r, chamber_top_z))
            # Injector shoulder tapering to gimbal neck
            bd.Line((chamber_r, chamber_top_z), (gimbal_r * 0.78, gimbal_bot_z))
            bd.Line((gimbal_r * 0.78, gimbal_bot_z), (gimbal_r, gimbal_bot_z))
            bd.Line((gimbal_r, gimbal_bot_z), (gimbal_r, total_h))
            # Top gimbal mounting plane to centerline
            bd.Line((gimbal_r, total_h), (0.0, total_h))
            # Down centerline to injector face inside throat
            bd.Line((0.0, total_h), (0.0, bell_h + 160.0))
            # Internal chamber roof curving to inner throat
            bd.Line((0.0, bell_h + 160.0), (in_throat_r, bell_h))
            # Inner parabolic bell down to exit rim
            bd.ThreePointArc((in_throat_r, bell_h), (in_mid_r, mid_z), (in_exit_r, 0.0))
        bd.make_face()

    bell = bd.revolve(profile.sketch, axis=bd.Axis.Z, revolution_arc=360)

    # Add crisp regenerative cooling stiffener hoops around outer bell surface
    # Sample approximate radius along the arc using circle through the 3 points
    p1 = (exit_r, 0.0)
    p2 = (mid_r, mid_z)
    p3 = (throat_r, bell_h)
    cx, cz, arc_r = _circle_from_3pts(p1, p2, p3)

    hoops = []
    hoop_h = 36.0
    hoop_proud = 18.0
    for f in hoop_fracs:
        z_h = bell_h * f
        dz = z_h - cz
        # Point on circle with larger radial coordinate (right side of circle center if cx < exit_r)
        rad_at_z = cx + math.sqrt(max(0.0, arc_r**2 - dz**2)) if cx < exit_r else cx - math.sqrt(max(0.0, arc_r**2 - dz**2))
        # Clamp outer hoop radius strictly inside exit_r so cluster clearances remain exact
        r_out = min(exit_r - 2.0, rad_at_z + hoop_proud)
        r_in = rad_at_z - 12.0
        ring = bd.Pos(0, 0, z_h - hoop_h / 2.0) * (
            bd.Cylinder(r_out, hoop_h, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
            - bd.Cylinder(r_in, hoop_h, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        )
        hoops.append(ring)

    # Exit stiffening lip collar flush with exit_r (inner lip extends inward slightly for crisp rim)
    lip_h = 42.0
    lip = bd.Pos(0, 0, 0.0) * (
        bd.Cylinder(exit_r, lip_h, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        - bd.Cylinder(exit_r - wall_t, lip_h, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    )
    hoops.append(lip)

    body = bell.fuse(*hoops)
    return body


def _circle_from_3pts(p1, p2, p3):
    """Return (cx, cz, radius) of the circle passing through three 2D points."""
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    d = 2.0 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
    ux = (
        (x1**2 + y1**2) * (y2 - y3)
        + (x2**2 + y2**2) * (y3 - y1)
        + (x3**2 + y3**2) * (y1 - y2)
    ) / d
    uy = (
        (x1**2 + y1**2) * (x3 - x2)
        + (x2**2 + y2**2) * (x1 - x3)
        + (x3**2 + y3**2) * (x2 - x1)
    ) / d
    r = math.hypot(x1 - ux, y1 - uy)
    return ux, uy, r


def _turbopump_hardware(
    z_base: float,
    chamber_r: float,
    max_env_r: float,
    chamber_solid,
    is_vac: bool = False,
):
    """Build dual LOX/CH4 turbopump housings & regenerative feed manifolds plumbed cleanly to the MCC."""
    parts = []
    # Two opposite turbopump volute housings (LOX pump + CH4 pump) positioned outside chamber_r,
    # physically connected to the chamber via top & bottom radial manifold stubs (cut flush by chamber_solid).
    pump_r = 110.0 if not is_vac else 130.0
    pump_h = 460.0 if not is_vac else 540.0
    radial_offset = chamber_r + pump_r + 22.0
    assert radial_offset + pump_r <= max_env_r, "Turbopump exceeds engine envelope!"

    for sign, label in ((1, "lox_turbopump"), (-1, "ch4_turbopump")):
        volute = bd.Pos(sign * radial_offset, 0, z_base) * bd.Cylinder(
            pump_r, pump_h, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
        )
        # Upper preburner cap dome
        cap = bd.Pos(sign * radial_offset, 0, z_base + pump_h) * bd.Cone(
            pump_r, pump_r * 0.55, 130.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
        )
        # Upper and lower radial feed-transfer manifold stubs connecting pump into chamber wall
        stub_len = radial_offset - chamber_r + 60.0
        stub_r = 52.0 if not is_vac else 62.0
        stub_x_start = sign * (chamber_r - 40.0)
        rot_y = 90.0 if sign > 0 else -90.0
        low_stub = (
            bd.Pos(stub_x_start, 0, z_base + 110.0)
            * bd.Rot(0, rot_y, 0)
            * bd.Cylinder(stub_r, stub_len, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        )
        hi_stub = (
            bd.Pos(stub_x_start, 0, z_base + pump_h - 90.0)
            * bd.Rot(0, rot_y, 0)
            * bd.Cylinder(stub_r, stub_len, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        )
        # Fuse pump + stubs, then trim inner stub end flush to chamber_solid so gap=0, overlap=0!
        pump = volute.fuse(cap, low_stub, hi_stub) - chamber_solid
        pump.label = label
        apply_raptor_copper(pump)
        parts.append(pump)

    # Two lateral propellant transfer ducts on ±Y sides, connected cleanly via upper & lower brackets
    duct_r = 60.0 if not is_vac else 72.0
    duct_h = 540.0 if not is_vac else 620.0
    duct_offset = chamber_r + duct_r + 22.0
    assert duct_offset + duct_r <= max_env_r, "Feed duct exceeds engine envelope!"
    for sign, label in ((1, "regen_duct_pos_y"), (-1, "regen_duct_neg_y")):
        duct_pipe = bd.Pos(0, sign * duct_offset, z_base - 20.0) * bd.Cylinder(
            duct_r, duct_h, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
        )
        rot_x = -90.0 if sign > 0 else 90.0
        tie_len = duct_offset - chamber_r + 60.0
        tie_y_start = sign * (chamber_r - 40.0)
        low_tie = (
            bd.Pos(0, tie_y_start, z_base + 70.0)
            * bd.Rot(rot_x, 0, 0)
            * bd.Cylinder(40.0, tie_len, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        )
        hi_tie = (
            bd.Pos(0, tie_y_start, z_base + duct_h - 110.0)
            * bd.Rot(rot_x, 0, 0)
            * bd.Cylinder(40.0, tie_len, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        )
        duct = duct_pipe.fuse(low_tie, hi_tie) - chamber_solid
        duct.label = label
        apply_stainless_structural(duct)
        parts.append(duct)

    return parts


@model
def raptor_sl():
    """SpaceX Raptor 2 Sea-Level rocket engine (3.1 m tall, 1.16 m bell exit diameter)."""
    chamber_r = 250.0
    gimbal_r = 260.0
    bell = _parabolic_bell_and_chamber(
        total_h=dims.RAPTOR_SL_HEIGHT,
        bell_h=dims.RAPTOR_SL_BELL_H,
        exit_r=dims.RAPTOR_SL_EXIT_R,
        throat_r=dims.RAPTOR_SL_THROAT_R,
        wall_t=dims.RAPTOR_SL_WALL,
        chamber_r=chamber_r,
        gimbal_r=gimbal_r,
        hoop_fracs=(0.24, 0.50, 0.76),
    )
    bell.label = "nozzle_and_chamber"
    apply_raptor_nozzle(bell)

    hardware = _turbopump_hardware(
        z_base=dims.RAPTOR_SL_BELL_H + 220.0,
        chamber_r=chamber_r,
        max_env_r=dims.RAPTOR_SL_EXIT_R - 10.0,  # Strictly inside 570 mm radius for 33-engine cluster!
        chamber_solid=bell,
        is_vac=False,
    )

    eng = bd.Compound(children=[bell, *hardware], label="raptor_sl")
    bb = eng.bounding_box()
    assert abs(bb.size.Z - dims.RAPTOR_SL_HEIGHT) < 1.0, bb.size
    return eng


@model
def raptor_vac():
    """SpaceX Raptor Vacuum (RVac) rocket engine (3.9 m tall, 2.30 m bell exit diameter)."""
    chamber_r = 280.0
    gimbal_r = 290.0
    bell = _parabolic_bell_and_chamber(
        total_h=dims.RAPTOR_VAC_HEIGHT,
        bell_h=dims.RAPTOR_VAC_BELL_H,
        exit_r=dims.RAPTOR_VAC_EXIT_R,
        throat_r=dims.RAPTOR_VAC_THROAT_R,
        wall_t=dims.RAPTOR_VAC_WALL,
        chamber_r=chamber_r,
        gimbal_r=gimbal_r,
        hoop_fracs=(0.18, 0.36, 0.54, 0.72, 0.88),
    )
    bell.label = "vac_nozzle_and_chamber"
    apply_raptor_nozzle(bell)

    hardware = _turbopump_hardware(
        z_base=dims.RAPTOR_VAC_BELL_H + 250.0,
        chamber_r=chamber_r,
        max_env_r=dims.RAPTOR_VAC_EXIT_R - 50.0,
        chamber_solid=bell,
        is_vac=True,
    )

    eng = bd.Compound(children=[bell, *hardware], label="raptor_vac")
    bb = eng.bounding_box()
    assert abs(bb.size.Z - dims.RAPTOR_VAC_HEIGHT) < 1.0, bb.size
    return eng


if __name__ == "__main__":
    raptor_sl()
    raptor_vac()
