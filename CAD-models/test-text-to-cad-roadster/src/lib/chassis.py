"""EV skateboard chassis, 200 kWh structural battery pack, tri-motor drive units,
wheel-well liners, and double-wishbone suspension.

Everything sits cleanly inside the body inner shell with generous clearance from
tires, brakes, and exterior panels.
"""

from __future__ import annotations

import build123d as bd

from lib.palette import (
    ALLOY_DARK,
    ALLOY_SILVER,
    CALIPER_RED,
    CARBON_TUB,
    TITANIUM,
    TRIM_DARK,
    group,
    style_alloy,
    style_caliper,
    style_carbon,
    style_trim,
)
from lib.surfaces import (
    ARCH_INNER_Y,
    FRONT_ARCH_R,
    FRONT_AXLE_X,
    FRONT_HUB_Y,
    FRONT_HUB_Z,
    REAR_ARCH_R,
    REAR_AXLE_X,
    REAR_HUB_Y,
    REAR_HUB_Z,
    body_master_inner,
    box_between,
    wheel_specs,
)


def _strut_between(p0, p1, radius):
    """Build a solid cylindrical link/wishbone arm connecting 3D points p0 and p1."""
    v0 = bd.Vector(*p0)
    v1 = bd.Vector(*p1)
    dv = v1 - v0
    length = dv.length
    if length < 1e-3:
        return None
    plane = bd.Plane(origin=v0, z_dir=dv.normalized())
    return plane * bd.Cylinder(radius=radius, height=length, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))


def _build_battery_skateboard():
    """Flat aerodynamic undertray + 200 kWh structural battery skateboard enclosure."""
    parts = []

    # Main structural battery pack spanning between axles (low center of gravity!)
    # Z: 118 .. 248 (clears ground by 118 mm, sits cleanly inside underfloor_cut of body_skin!)
    pack_pts = [
        (1000.0, -560.0),
        (1000.0, 560.0),
        (680.0, 690.0),
        (-680.0, 690.0),
        (-980.0, 560.0),
        (-980.0, -560.0),
        (-680.0, -690.0),
        (680.0, -690.0),
    ]
    pack_wire = bd.Wire.make_polygon([bd.Vector(x, y, 118.0) for x, y in pack_pts])
    pack = bd.extrude(bd.Face(pack_wire), 115.0)
    parts.append(style_carbon(pack, "battery_pack_200kwh", CARBON_TUB))

    # Front and rear flat aero underfloor skid trays extending cleanly to axles (5 mm clear of battery & diffuser)
    front_tray = box_between(1005.0, 1735.0, -490.0, 490.0, 120.0, 150.0)
    rear_tray = box_between(-1758.0, -985.0, -490.0, 490.0, 126.0, 160.0)
    parts.append(style_carbon(front_tray, "undertray_front", CARBON_TUB))
    parts.append(style_carbon(rear_tray, "undertray_rear", CARBON_TUB))

    # Carbon monocoque bulkhead walls framing the cockpit (strictly clear of battery pack, seats & body)
    firewall = box_between(745.0, 815.0, -555.0, 555.0, 238.0, 690.0)
    rear_bulkhead = box_between(-940.0, -860.0, -565.0, 565.0, 238.0, 735.0)
    parts.append(style_carbon(firewall, "front_firewall", CARBON_TUB))
    parts.append(style_carbon(rear_bulkhead, "rear_bulkhead", CARBON_TUB))

    return parts


def _build_tri_motor_powertrain():
    """Front single-motor and rear dual-motor EV drive units + cast subframes."""
    parts = []

    # Front & rear cast aluminum subframe rails (cleanly clear of battery pack & sloped rear floor!)
    for side in (1, -1):
        lbl = "left" if side > 0 else "right"
        rail_f = box_between(1005.0, 1730.0, side * 380.0 - 38.0, side * 380.0 + 38.0, 175.0, 255.0)
        parts.append(style_alloy(rail_f, f"front_subframe_rail_{lbl}", ALLOY_DARK, roughness=0.35))
        rail_r = box_between(-1620.0, -985.0, side * 385.0 - 40.0, side * 385.0 + 40.0, 232.0, 312.0)
        parts.append(style_alloy(rail_r, f"rear_subframe_rail_{lbl}", ALLOY_DARK, roughness=0.35))

    # Front electric drive unit (centered on front axle)
    front_motor = bd.Pos(FRONT_AXLE_X, 0.0, FRONT_HUB_Z) * bd.Rot(-90, 0, 0) * bd.Cylinder(
        radius=112.0, height=540.0
    )
    parts.append(style_alloy(front_motor, "front_drive_unit", ALLOY_SILVER, roughness=0.28))

    # Dual rear Plaid/Roadster tri-motor drive units (twin coaxial motors + inverter box)
    rear_motor = bd.Pos(REAR_AXLE_X, 0.0, REAR_HUB_Z) * bd.Rot(-90, 0, 0) * bd.Cylinder(
        radius=128.0, height=620.0
    )
    rear_inverter = box_between(REAR_AXLE_X - 140.0, REAR_AXLE_X + 140.0, -260.0, 260.0, REAR_HUB_Z + 132.0, REAR_HUB_Z + 220.0)
    parts.append(style_alloy(rear_motor, "rear_dual_drive_unit", ALLOY_SILVER, roughness=0.28))
    parts.append(style_alloy(rear_inverter, "rear_inverter_housing", ALLOY_DARK, roughness=0.32))

    return parts


def _tube_between(p0, p1, r_out, r_in):
    """Build a hollow cylindrical tube/spring sleeve between p0 and p1."""
    v0 = bd.Vector(*p0)
    v1 = bd.Vector(*p1)
    dv = v1 - v0
    length = dv.length
    if length < 1e-3:
        return None
    plane = bd.Plane(origin=v0, z_dir=dv.normalized())
    outer = plane * bd.Cylinder(radius=r_out, height=length, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    inner = plane * bd.Cylinder(radius=r_in, height=length + 2.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    return outer - inner


def _build_suspension():
    """Double-wishbone aluminum suspension A-arms, uprights, half-shafts & coilovers."""
    parts = []
    for name, x, y, z, side, tyre_r, tyre_w, _ in wheel_specs():
        is_front = name.startswith("front")
        y_upright = side * (abs(y) - 70.0)
        # Inboard pickup sits 7 mm outside subframe rails (|Y| = 425), outboard 12 mm inside upright (|Y| - 22)
        y_frame = side * 434.0
        y_out = y_upright - side * 34.0

        # Upright block (vertical aluminum knuckle)
        up = box_between(x - 36.0, x + 36.0, y_upright - 22.0, y_upright + 22.0, z - 120.0, z + 125.0)
        parts.append(style_alloy(up, f"upright_{name}", ALLOY_DARK, roughness=0.30))

        # Half-shaft axle cleanly between drive unit and upright
        y_motor_end = side * (276.0 if is_front else 316.0)
        shaft = _strut_between((x, y_motor_end, z), (x, y_upright - side * 26.0, z), 19.0)
        parts.append(style_alloy(shaft, f"half_shaft_{name}", TITANIUM, roughness=0.28))

        # Single fused lower and upper A-arm wishbones per corner (wide stance framing coilover cleanly!)
        z_low_in = 192.0 if is_front else 212.0
        z_up_in = 395.0 if is_front else 420.0
        p_low_out = (x, y_out, z - 102.0)
        p_up_out = (x, y_out, z + 108.0)

        low_arm = _strut_between((x - 160.0, y_frame, z_low_in), p_low_out, 12.0) + _strut_between(
            (x + 160.0, y_frame, z_low_in), p_low_out, 12.0
        )
        up_arm = _strut_between((x - 165.0, y_frame, z_up_in), p_up_out, 10.5) + _strut_between(
            (x + 165.0, y_frame, z_up_in), p_up_out, 10.5
        )
        parts.append(style_alloy(low_arm, f"lower_wishbone_{name}", ALLOY_SILVER, roughness=0.25))
        parts.append(style_alloy(up_arm, f"upper_wishbone_{name}", ALLOY_SILVER, roughness=0.25))

        # Coilover damper + hollow red spring sleeve passing cleanly between upper A-arm legs above half-shaft
        p_coil_bot = (x, y_out - side * 62.0, z + 38.0)
        p_coil_top = (x, side * 468.0, z + 235.0)
        damper = _strut_between(p_coil_bot, p_coil_top, 14.0)
        v0, v1 = bd.Vector(*p_coil_bot), bd.Vector(*p_coil_top)
        sp0 = v0 + (v1 - v0) * 0.24
        sp1 = v0 + (v1 - v0) * 0.74
        spring = _tube_between((sp0.X, sp0.Y, sp0.Z), (sp1.X, sp1.Y, sp1.Z), 26.0, 17.0)
        parts.append(style_alloy(damper, f"damper_{name}", TITANIUM, roughness=0.22))
        parts.append(style_caliper(spring, f"coil_spring_{name}", CALIPER_RED))

    return parts


def _build_wheel_well_liners():
    """Dark curved wheelhouse inner arch liners trimmed strictly inside the inner body shell."""
    parts = []
    inner_body = body_master_inner(d=20.0)
    for name, x, y, z, side, _, _, _ in wheel_specs():
        is_front = name.startswith("front")
        r_in = (FRONT_ARCH_R if is_front else REAR_ARCH_R) + 4.0
        r_out = r_in + 10.0
        y_in = side * (ARCH_INNER_Y - 12.0)
        y_out = side * (ARCH_INNER_Y + 280.0)
        y_mid = (y_in + y_out) / 2.0
        length = abs(y_out - y_in)

        c_out = bd.Rot(-90, 0, 0) * bd.Cylinder(radius=r_out, height=length)
        c_in = bd.Rot(-90, 0, 0) * bd.Cylinder(radius=r_in, height=length + 4.0)
        ring = bd.Pos(x, y_mid, z) * (c_out - c_in)
        # Keep strictly inside the inner body shell and above wishbones
        liner = (ring & inner_body) & box_between(
            x - r_out - 5.0, x + r_out + 5.0, -1200.0, 1200.0, 260.0, z + r_out + 5.0
        )
        if liner.solids():
            parts.append(style_trim(liner, f"wheel_liner_{name}", TRIM_DARK))
    return parts


def build():
    """Build complete EV chassis, powertrain, suspension, and wheel liners."""
    return group(
        "chassis_and_drivetrain",
        [
            group("battery_skateboard", _build_battery_skateboard()),
            group("tri_motor_powertrain", _build_tri_motor_powertrain()),
            group("double_wishbone_suspension", _build_suspension()),
            group("wheel_well_liners", _build_wheel_well_liners()),
        ],
    )
