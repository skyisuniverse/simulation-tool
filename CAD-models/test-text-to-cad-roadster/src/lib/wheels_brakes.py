"""Staggered 20"/21" forged wheels, performance tires, and carbon-ceramic brakes.

Local wheel frame (before corner placement):
  - Wheel spin axis along +Y
  - Outboard face toward +Y (for left corners; rotated 180 deg about Z for right)
  - Center of tire contact patch at Z = -tyre_r
"""

from __future__ import annotations

import math

import build123d as bd

from lib.palette import (
    ALLOY_DARK,
    ALLOY_SILVER,
    CALIPER_RED,
    ROTOR_IRON,
    TITANIUM,
    TYRE_RUBBER,
    group,
    style_alloy,
    style_caliper,
    style_rubber,
    style_steel,
)
from lib.surfaces import wheel_specs


def _revolve_y(wire_yz_pts_or_edges):
    """Revolve a closed 2D face in the (Y, Z) plane around the Y axis.

    Input points are ``(y, r)`` where ``r >= 0`` is radial distance from the Y axis.
    In Plane.YZ, local X is global Y and local Y is global Z, so revolving around
    ``bd.Axis.Y`` sweeps a solid of revolution coaxial with the wheel axle.
    """
    face = bd.Plane.YZ * wire_yz_pts_or_edges
    return bd.revolve(face, axis=bd.Axis.Y, revolution_arc=360.0)


def _build_tyre(tyre_r, tyre_w, rim_d):
    """Smooth sidewall splines + exact-radius flat tread with 3 crisp rain grooves (Z_min = 0.00 mm)."""
    hw = tyre_w / 2.0
    rim_r = rim_d / 2.0
    sh_r = tyre_r - 12.0
    bead_r = rim_r - 4.0
    bead_y = hw - 18.0
    inner_r = rim_r + 14.0

    # Left smooth sidewall spline up to exact tread shoulder (no groove overshoot!)
    left_wall = bd.Spline(
        (-bead_y, bead_r),
        (-hw + 3.0, rim_r + 22.0),
        (-hw, rim_r + 0.50 * (tyre_r - rim_r)),
        (-hw + 4.0, sh_r),
        (-hw + 20.0, tyre_r),
        tangents=((-0.2, 1.0), (1.0, 0.0)),
    )

    # Exact-radius flat tread with 3 crisp 2.2 mm recessed circumferential rain channels
    g_d = 2.2
    gw = 5.5
    c1 = hw * 0.42
    tread_pts = [
        (-hw + 20.0, tyre_r),
        (-c1 - gw, tyre_r),
        (-c1 - gw * 0.7, tyre_r - g_d),
        (-c1 + gw * 0.7, tyre_r - g_d),
        (-c1 + gw, tyre_r),
        (-gw, tyre_r),
        (-gw * 0.7, tyre_r - g_d),
        (gw * 0.7, tyre_r - g_d),
        (gw, tyre_r),
        (c1 - gw, tyre_r),
        (c1 - gw * 0.7, tyre_r - g_d),
        (c1 + gw * 0.7, tyre_r - g_d),
        (c1 + gw, tyre_r),
        (hw - 20.0, tyre_r),
    ]
    tread = bd.Polyline(*tread_pts)

    # Right smooth sidewall spline back down to rim bead
    right_wall = bd.Spline(
        (hw - 20.0, tyre_r),
        (hw - 4.0, sh_r),
        (hw, rim_r + 0.50 * (tyre_r - rim_r)),
        (hw - 3.0, rim_r + 22.0),
        (bead_y, bead_r),
        tangents=((1.0, 0.0), (-0.2, -1.0)),
    )

    inner_pts = [
        (bead_y, bead_r),
        (bead_y - 12.0, inner_r),
        (-bead_y + 12.0, inner_r),
        (-bead_y, bead_r),
    ]
    e_inner = bd.Polyline(*inner_pts)
    face = bd.make_face(left_wall + tread + right_wall + e_inner)
    return _revolve_y(face)


def _build_rim(tyre_w, rim_d):
    """Concave forged 10-blade Y-spoke Tesla Roadster performance rim."""
    hw = tyre_w / 2.0
    rim_r = rim_d / 2.0
    barrel_in = rim_r - 17.0
    barrel_out = rim_r - 4.5     # 0.5 mm clearance inside tire bead (bead_r = rim_r - 4.0)
    lip_y = hw - 17.0
    back_y = -hw + 19.0

    # 1. Revolved stepped barrel (outer lip + drop-center inner barrel)
    barrel_pts = [
        (back_y, barrel_in),
        (back_y, barrel_out),
        (lip_y, barrel_out),
        (lip_y + 3.0, rim_r + 2.0),
        (lip_y + 6.0, rim_r + 2.0),
        (lip_y + 6.0, barrel_in + 4.0),
        (lip_y - 16.0, barrel_in),
        (back_y, barrel_in),
    ]
    barrel_face = bd.make_face(bd.Polyline(*barrel_pts))
    barrel = _revolve_y(barrel_face)

    # 2. Concave center hub & lug boss (sits well outboard of brake rotor)
    hub_back_y = hw - 64.0
    hub_front_y = hw - 34.0
    hub_pts = [
        (hub_back_y, 26.0),
        (hub_back_y, 82.0),
        (hub_front_y - 6.0, 74.0),
        (hub_front_y, 58.0),
        (hub_front_y, 26.0),
        (hub_back_y, 26.0),
    ]
    hub_face = bd.make_face(bd.Polyline(*hub_pts))
    hub = _revolve_y(hub_face)

    # 3. 5 pairs of angled split Y-spokes sweeping concavely from hub to outer lip
    spokes = []
    r_start = 66.0
    r_mid = 148.0
    r_end = barrel_in + 6.0
    y_start = hw - 48.0
    y_mid = hw - 32.0
    y_end = lip_y - 4.0

    for i in range(5):
        base_deg = i * 72.0
        for branch in (-1.0, 1.0):
            # Each Y-branch splays smoothly outward from the hub toward the outer barrel
            ang0 = math.radians(base_deg + branch * 7.5)
            ang1 = math.radians(base_deg + branch * 14.0)
            ang2 = math.radians(base_deg + branch * 18.5)

            p0 = bd.Vector(r_start * math.cos(ang0), y_start, r_start * math.sin(ang0))
            p1 = bd.Vector(r_mid * math.cos(ang1), y_mid, r_mid * math.sin(ang1))
            p2 = bd.Vector(r_end * math.cos(ang2), y_end, r_end * math.sin(ang2))

            # Build clean tapered spoke beam by lofting 3 rectangular cross-sections along the ray
            sec_faces = []
            for p, ang, w_t, t_y in (
                (p0, ang0, 18.0, 22.0),
                (p1, ang1, 13.0, 18.0),
                (p2, ang2, 10.0, 15.0),
            ):
                # Tangent direction perpendicular to spoke radial direction in XZ plane
                tx, tz = -math.sin(ang), math.cos(ang)
                rad = bd.Vector(math.cos(ang), 0.0, math.sin(ang))
                plane = bd.Plane(origin=p, x_dir=bd.Vector(tx, 0.0, tz), z_dir=rad)
                sec_faces.append(plane * bd.Rectangle(w_t, t_y))
            spokes.append(bd.loft(sec_faces, ruled=True))

    rim = barrel + hub
    for s in spokes:
        rim = rim + s

    # Center cap (separate darker machined piece sitting flush in hub bore)
    cap_pts = [
        (hub_front_y - 12.0, 0.0),
        (hub_front_y - 12.0, 25.5),
        (hub_front_y + 1.0, 25.5),
        (hub_front_y + 3.0, 20.0),
        (hub_front_y + 3.0, 0.0),
        (hub_front_y - 12.0, 0.0),
    ]
    cap = _revolve_y(bd.make_face(bd.Polyline(*cap_pts)))
    return rim, cap


def _build_brake_unit(tyre_w, rim_d, is_front):
    """Ventilated carbon-ceramic rotor, alloy hat, and 6-piston red caliper."""
    hw = tyre_w / 2.0
    rotor_r = 198.0 if is_front else 206.0
    rotor_y = hw - 98.0      # 34 mm clear inboard of hub_back_y = hw - 64
    rotor_t = 30.0

    # Rotor disc + top-hat bell
    hat_r = 104.0
    rotor_pts = [
        (rotor_y - rotor_t / 2.0, hat_r + 2.0),
        (rotor_y - rotor_t / 2.0, rotor_r),
        (rotor_y + rotor_t / 2.0, rotor_r),
        (rotor_y + rotor_t / 2.0, hat_r + 2.0),
        (rotor_y - rotor_t / 2.0, hat_r + 2.0),
    ]
    rotor = _revolve_y(bd.make_face(bd.Polyline(*rotor_pts)))

    hat_pts = [
        (rotor_y - rotor_t / 2.0 - 12.0, 42.0),
        (rotor_y - rotor_t / 2.0 - 12.0, hat_r + 1.5),
        (rotor_y + rotor_t / 2.0 + 6.0, hat_r + 1.5),
        (rotor_y + rotor_t / 2.0 + 6.0, 42.0),
        (rotor_y - rotor_t / 2.0 - 12.0, 42.0),
    ]
    hat = _revolve_y(bd.make_face(bd.Polyline(*hat_pts)))

    # 6-piston monobloc red caliper positioned toward center of wheelbase (rear of front disc, front of rear disc)
    # In wheel local coords (+X forward for left side, -X forward for right side — wait: we place brakes directly in world or corner!)
    # Let's place caliper at local -X for front (inboard of wheelbase) and +X for rear!
    cal_dir = -1.0 if is_front else 1.0
    cal_in_r = rotor_r - 68.0
    cal_out_r = rotor_r + 20.0
    span_deg = 52.0
    mid_deg = 180.0 if cal_dir < 0 else 0.0

    # Sculpted curved caliper arc in XZ plane, extruded across rotor with rotor slot cut out
    arc_pts = []
    n_arc = 9
    for i in range(n_arc + 1):
        a = math.radians(mid_deg - span_deg / 2.0 + span_deg * i / n_arc)
        arc_pts.append((cal_out_r * math.cos(a), cal_out_r * math.sin(a)))
    for i in range(n_arc, -1, -1):
        a = math.radians(mid_deg - span_deg / 2.0 + span_deg * i / n_arc)
        arc_pts.append((cal_in_r * math.cos(a), cal_in_r * math.sin(a)))

    cal_wire = bd.Wire.make_polygon([bd.Vector(x, rotor_y - 34.0, z) for x, z in arc_pts])
    cal_body = bd.extrude(bd.Face(cal_wire), 64.0, dir=(0, 1, 0))

    # Cut clean 34 mm slot through caliper for rotor clearance (2 mm air gap each face!)
    slot_cyl = bd.Pos(0.0, rotor_y, 0.0) * bd.Rot(-90, 0, 0) * bd.Cylinder(
        radius=rotor_r + 3.0, height=rotor_t + 4.0
    )
    caliper = cal_body - slot_cyl
    return rotor, hat, caliper


def build():
    """Build all four staggered corner assemblies (wheels + stationary brakes)."""
    # Build one front and one rear wheel prototype, reused via placement
    front_proto_specs = None
    rear_proto_specs = None
    for spec in wheel_specs():
        if spec[0] == "front_left":
            front_proto_specs = spec
        elif spec[0] == "rear_left":
            rear_proto_specs = spec

    def _make_wheel_proto(tyre_r, tyre_w, rim_d, tag):
        tyre = style_rubber(_build_tyre(tyre_r, tyre_w, rim_d), f"tyre_{tag}", TYRE_RUBBER)
        rim_s, cap_s = _build_rim(tyre_w, rim_d)
        rim = style_alloy(rim_s, f"rim_{tag}", ALLOY_SILVER, roughness=0.20)
        cap = style_alloy(cap_s, f"center_cap_{tag}", ALLOY_DARK, roughness=0.28)
        return group(f"wheel_{tag}", [tyre, rim, cap])

    front_wheel = _make_wheel_proto(front_proto_specs[5], front_proto_specs[6], front_proto_specs[7], "front")
    rear_wheel = _make_wheel_proto(rear_proto_specs[5], rear_proto_specs[6], rear_proto_specs[7], "rear")

    corners = []
    for name, x, y, z, side, tyre_r, tyre_w, rim_d in wheel_specs():
        is_front = name.startswith("front")
        wheel_proto = front_wheel if is_front else rear_wheel
        # Left side (side=+1): +Y outboard -> rot_z = 0; Right side (side=-1): -Y outboard -> rot_z = 180
        rot_z = 0.0 if side > 0 else 180.0
        wheel_loc = bd.Location((x, y, z), (0.0, 0.0, rot_z))
        wheel_inst = wheel_proto.moved(wheel_loc)
        wheel_inst.label = f"wheel_{name}"

        # Brakes built per side so caliper always sits inboard toward wheelbase center (-X front, +X rear)
        # Note: rotating a front caliper by 180 deg about Z flips -X to +X, so pass effective front flag!
        rotor_s, hat_s, cal_s = _build_brake_unit(tyre_w, rim_d, is_front if side > 0 else (not is_front))
        rotor = style_steel(rotor_s.moved(wheel_loc), f"brake_rotor_{name}", ROTOR_IRON)
        hat = style_alloy(hat_s.moved(wheel_loc), f"brake_hat_{name}", ALLOY_DARK, roughness=0.30)
        caliper = style_caliper(cal_s.moved(wheel_loc), f"brake_caliper_{name}", CALIPER_RED)

        corners.append(group(f"corner_{name}", [wheel_inst, rotor, hat, caliper]))

    return group("wheels_and_brakes", corners)
