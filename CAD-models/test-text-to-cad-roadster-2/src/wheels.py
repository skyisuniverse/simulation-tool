"""20-inch front (295/30R20) and 21-inch rear (335/30R21) signature dual-tone
5-spoke aero wheels, Pirelli P Zero Trofeo semi-slick tires, drilled
carbon-ceramic brake rotors, and 6-piston billet calipers.

Each wheel is built centered at the origin with its outer face pointing +X
(driver's left side), and mirrored / rotated cleanly for the -X passenger side.
"""

import math

import build123d as bd
from cad import model
from cad.build123d import memo

from spec import (
    ROTOR_F_RADIUS,
    ROTOR_R_RADIUS,
    TIRE_F_RADIUS,
    TIRE_F_RIM_R,
    TIRE_F_WIDTH,
    TIRE_R_RADIUS,
    TIRE_R_RIM_R,
    TIRE_R_WIDTH,
    apply_aero_blade,
    apply_brake_rotor,
    apply_dark_gloss,
    apply_dark_titanium,
    apply_tire_rubber,
    apply_titanium,
)


def _revolved_tire(r_outer, r_rim, width):
    """Smooth revolved low-profile semi-slick tire with exact outer diameter & 3 grooves."""
    hw = width / 2.0
    r_sh = r_outer - 14.0
    r_mid = 0.5 * (r_rim + r_outer)

    # Piecewise crisp arcs + flat tread crown so exact outer radius == r_outer (no spline overshoot!)
    p0 = bd.Vector(r_rim + 2.0, -hw + 8.0, 0.0)
    p1 = bd.Vector(r_mid, -hw - 3.0, 0.0)
    p2 = bd.Vector(r_sh, -hw + 5.0, 0.0)
    p3 = bd.Vector(r_outer, -hw + 26.0, 0.0)
    p4 = bd.Vector(r_outer, hw - 26.0, 0.0)
    p5 = bd.Vector(r_sh, hw - 5.0, 0.0)
    p6 = bd.Vector(r_mid, hw + 3.0, 0.0)
    p7 = bd.Vector(r_rim + 2.0, hw - 8.0, 0.0)

    edges = [
        bd.Edge.make_three_point_arc(p0, p1, p2),
        bd.Edge.make_three_point_arc(p2, bd.Vector(r_outer - 3.0, -hw + 12.0, 0.0), p3),
        bd.Edge.make_line(p3, p4),
        bd.Edge.make_three_point_arc(p4, bd.Vector(r_outer - 3.0, hw - 12.0, 0.0), p5),
        bd.Edge.make_three_point_arc(p5, p6, p7),
        bd.Edge.make_line(p7, p0),
    ]
    prof = bd.Face(bd.Wire(edges))

    # Revolve around Y axis -> tire axle is Y; rotate -90 around Z so axle is X!
    tire = bd.revolve(prof, axis=bd.Axis.Y, revolution_arc=360.0)
    tire = bd.Rot(0.0, 0.0, -90.0) * tire

    # Carve 3 sleek circumferential semi-slick Pirelli Trofeo tread grooves
    grooves = []
    for gx in (-width * 0.24, 0.0, width * 0.24):
        g_ring = bd.Cylinder(r_outer + 5.0, 9.0) - bd.Cylinder(r_outer - 6.0, 11.0)
        g_ring = bd.Pos(gx, 0.0, 0.0) * (bd.Rot(0.0, 90.0, 0.0) * g_ring)
        grooves.append(g_ring)
    tire = tire - grooves
    tire.label = "tire"
    apply_tire_rubber(tire)
    return tire


def _rim_and_spokes(r_rim, width):
    """Dark machined rim barrel + bold 5-spoke star + flush bright silver aero inserts."""
    hw = width / 2.0
    r_barrel_in = r_rim - 14.0

    # 1. Rim barrel (spans axial X in [-hw+12, +hw-12], clears tire bead cleanly)
    barrel_len = width - 26.0
    barrel = bd.Cylinder(r_rim + 1.0, barrel_len) - bd.Cylinder(r_barrel_in, barrel_len + 4.0)
    # Recessed outer lip flange
    outer_lip = bd.Pos(0.0, 0.0, barrel_len / 2.0 - 9.0) * (
        bd.Cylinder(r_rim + 4.0, 18.0) - bd.Cylinder(r_rim - 12.0, 22.0)
    )
    barrel = barrel + outer_lip

    # 2. Bold 5-spoke dark machined star radiating from center hub (X = +hw-28 .. +hw-6)
    z_face = barrel_len / 2.0 - 12.0
    hub = bd.Pos(0.0, 0.0, z_face - 6.0) * bd.Cylinder(68.0, 28.0)

    spoke_solids = [barrel, hub]
    for i in range(5):
        ang = i * 72.0 + 18.0  # matches vertical top spoke orientation in side view!
        # Trapezoidal sculpted dark spoke (56 mm wide at hub -> 44 mm at outer rim)
        pts = [
            (-26.0, 52.0),
            (26.0, 52.0),
            (21.0, r_rim - 4.0),
            (-21.0, r_rim - 4.0),
        ]
        s_face = bd.Face(bd.Wire.make_polygon([bd.Vector(x, y, z_face - 12.0) for x, y in pts]))
        spoke = bd.extrude(s_face, 24.0, dir=(0, 0, 1))
        # Crisp machined center flute groove along each spoke
        flute = bd.Pos(0.0, 0.5 * (65.0 + r_rim), z_face + 10.0) * bd.Box(7.5, r_rim - 75.0, 8.0)
        spoke = spoke - flute
        spoke = bd.Rot(0.0, 0.0, ang) * spoke
        spoke_solids.append(spoke)

    wheel_star = spoke_solids[0]
    for s in spoke_solids[1:]:
        wheel_star = wheel_star + s
    # Trim cleanly inside outer rim OD
    wheel_star = wheel_star & bd.Cylinder(r_rim + 4.0, barrel_len + 20.0)
    wheel_star = bd.Rot(0.0, 90.0, 0.0) * wheel_star
    wheel_star.label = "wheel_spokes"
    apply_dark_gloss(wheel_star)

    # 3. 5 Signature Flush Silver-White Aero Blade Inserts tucked behind the 5 black spokes
    # Circular outer arc hugs the rim cleanly; crisp 15 mm radial vent slots flank each spoke!
    z_blade = z_face - 18.0
    blade_solids = []
    for i in range(5):
        ang_mid = i * 72.0 + 18.0 + 36.0
        r_in = 76.0
        r_out = r_barrel_in - 4.0
        a_out = math.radians(21.5)
        a_in = math.radians(15.5)
        p_o1 = bd.Vector(r_out * math.sin(-a_out), r_out * math.cos(-a_out), z_blade)
        p_om = bd.Vector(0.0, r_out, z_blade)
        p_o2 = bd.Vector(r_out * math.sin(a_out), r_out * math.cos(a_out), z_blade)
        p_i2 = bd.Vector(r_in * math.sin(a_in), r_in * math.cos(a_in), z_blade)
        p_im = bd.Vector(0.0, r_in, z_blade)
        p_i1 = bd.Vector(r_in * math.sin(-a_in), r_in * math.cos(-a_in), z_blade)
        b_edges = [
            bd.Edge.make_three_point_arc(p_o1, p_om, p_o2),
            bd.Edge.make_line(p_o2, p_i2),
            bd.Edge.make_three_point_arc(p_i2, p_im, p_i1),
            bd.Edge.make_line(p_i1, p_o1),
        ]
        blade = bd.extrude(bd.Face(bd.Wire(b_edges)), 8.0, dir=(0, 0, 1))
        blade = bd.Rot(0.0, 0.0, ang_mid) * blade
        blade_solids.append(blade)

    aero_blades = blade_solids[0]
    for b in blade_solids[1:]:
        aero_blades = aero_blades + b
    aero_blades = bd.Rot(0.0, 90.0, 0.0) * aero_blades
    aero_blades.label = "aero_blades"
    apply_aero_blade(aero_blades)

    # 4. Machined titanium center-cap ring emblem
    cap_ring = bd.Pos(0.0, 0.0, z_face + 13.5) * (
        bd.Cylinder(38.0, 5.0) - bd.Cylinder(30.0, 7.0)
    )
    cap_ring = bd.Rot(0.0, 90.0, 0.0) * cap_ring
    cap_ring.label = "center_cap_ring"
    apply_titanium(cap_ring)

    return wheel_star, aero_blades, cap_ring


def _brake_assembly(r_rotor, width, caliper_rear_facing=True):
    """Carbon-ceramic brake disc + machined hub hat + 6-piston billet brake caliper."""
    # Positioned cleanly inboard behind the spokes & inside the rim barrel (zero clash!)
    x_disc = -8.0
    r_eff = min(r_rotor, 188.0)
    disc = bd.Cylinder(r_eff, 32.0) - bd.Cylinder(104.0, 36.0)
    hat = bd.Pos(0.0, 0.0, 18.0) * (bd.Cylinder(104.0, 36.0) - bd.Cylinder(45.0, 42.0))
    rotor = bd.Pos(x_disc, 0.0, 0.0) * (bd.Rot(0.0, 90.0, 0.0) * (disc + hat))
    rotor.label = "brake_rotor"
    apply_brake_rotor(rotor)

    # Sculpted 6-piston caliper straddling the rotor edge with exact cylindrical disc slot
    y_dir = 1.0 if caliper_rear_facing else -1.0
    cal_outer = bd.Pos(x_disc, y_dir * (r_eff - 30.0), 0.0) * bd.Box(68.0, 76.0, 156.0)
    rotor_clearance = bd.Pos(x_disc, 0.0, 0.0) * (
        bd.Rot(0.0, 90.0, 0.0) * bd.Cylinder(r_eff + 3.0, 38.0)
    )
    caliper = cal_outer - rotor_clearance
    caliper.label = "brake_caliper"
    apply_dark_titanium(caliper)

    return rotor, caliper


@memo
def _build_wheel(r_outer, r_rim, width, r_rotor, caliper_rear_facing, label, flip_right=False):
    tire = _revolved_tire(r_outer, r_rim, width)
    spokes, blades, cap = _rim_and_spokes(r_rim, width)
    rotor, caliper = _brake_assembly(r_rotor, width, caliper_rear_facing)
    tire = tire - spokes
    tire.label = "tire"
    apply_tire_rubber(tire)
    wheel = bd.Compound(
        children=[tire, spokes, blades, cap, rotor, caliper],
        label=label,
    )
    if flip_right:
        # Proper rigid right-handed 180 deg rotation about Z (keeps outward surface normals!)
        wheel = bd.Rot(0.0, 0.0, 180.0) * wheel
        wheel.label = label
    return wheel


@model
def wheel_front():
    """20-inch front-left dual-tone 5-spoke aero wheel (295/30R20 Trofeo + brake)."""
    return _build_wheel(
        TIRE_F_RADIUS, TIRE_F_RIM_R, TIRE_F_WIDTH, ROTOR_F_RADIUS, True, "wheel_front", False
    )


@model
def wheel_front_right():
    """20-inch front-right dual-tone 5-spoke aero wheel (proper right-handed build)."""
    return _build_wheel(
        TIRE_F_RADIUS, TIRE_F_RIM_R, TIRE_F_WIDTH, ROTOR_F_RADIUS, False, "wheel_front_right", True
    )


@model
def wheel_rear():
    """21-inch rear-left dual-tone 5-spoke aero wheel (335/30R21 Trofeo + brake)."""
    return _build_wheel(
        TIRE_R_RADIUS, TIRE_R_RIM_R, TIRE_R_WIDTH, ROTOR_R_RADIUS, False, "wheel_rear", False
    )


@model
def wheel_rear_right():
    """21-inch rear-right dual-tone 5-spoke aero wheel (proper right-handed build)."""
    return _build_wheel(
        TIRE_R_RADIUS, TIRE_R_RIM_R, TIRE_R_WIDTH, ROTOR_R_RADIUS, True, "wheel_rear_right", True
    )


if __name__ == "__main__":
    wheel_front()
    wheel_front_right()
    wheel_rear()
    wheel_rear_right()
