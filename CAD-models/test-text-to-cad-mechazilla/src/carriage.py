"""Vertical-travel catch carriage with I-beam roller bogies, truss spine, hinge clevises, and traveling sheaves."""

import build123d as bd
from cad import model

import spec as S
from foundation import _build_sheave


def _build_rail_bogie():
    """Single wrap-around guide rail roller bogie truck (height 28 mm, centered at Y=0, Z_local=0..28).

    Wraps the I-beam rail head (X: 76.5..80.5, Y: -7..+7; web X: 71.5..76.5, Y: -3..+3)
    with >= 0.6 mm clearance on every rail face so sliding motion has zero overlap.
    """
    h = 28.0
    gap = 0.7
    # Outer side cheek plates (Y: +/-7.7 .. +/-11.2, X: 72.2 .. 86.5)
    parts = []
    for sy in (-1, 1):
        y_in = sy * (S.RAIL_FLANGE_W / 2.0 + gap)  # +/-7.7
        y_out = sy * 11.2
        yc = (y_in + y_out) / 2.0
        parts.append(
            bd.Pos(72.2, yc, 0)
            * bd.Box(
                S.CARRIAGE_SPINE_X0 - 72.2,  # 14.3 mm
                abs(y_out - y_in),
                h,
                align=(bd.Align.MIN, bd.Align.CENTER, bd.Align.MIN),
            )
        )
        # Rear anti-pulloff hook tucked cleanly inside rail throat (X: 72.2..75.8, Y: +/-3.7..+/-7.8)
        y_hook_in = sy * (S.RAIL_WEB_W / 2.0 + gap)  # +/-3.7
        y_hook_out = sy * 8.0
        parts.append(
            bd.Pos(72.2, (y_hook_in + y_hook_out) / 2.0, 0)
            * bd.Box(
                3.6,  # 72.2 -> 75.8 (clears 71.5 back flange and 76.5 front head by 0.7 mm!)
                abs(y_hook_out - y_hook_in),
                h,
                align=(bd.Align.MIN, bd.Align.CENTER, bd.Align.MIN),
            )
        )
        # Visible roller bearing wheel bosses on outer cheek faces (upper & lower rollers)
        for zr in (6.5, h - 6.5):
            parts.append(
                bd.Pos(79.0, sy * 11.2, zr)
                * bd.Rot(90, 0, 0)
                * bd.Cylinder(3.4, 2.2)
            )
    # Front bridge plate connecting cleanly to carriage spine (X: 81.2 .. 86.5, clears rail front 80.5!)
    parts.append(
        bd.Pos(S.RAIL_FRONT_X + gap, 0, 0)
        * bd.Box(
            S.CARRIAGE_SPINE_X0 - (S.RAIL_FRONT_X + gap),  # 5.3 mm
            22.4,
            h,
            align=(bd.Align.MIN, bd.Align.CENTER, bd.Align.MIN),
        )
    )
    return parts[0] + parts[1:]


def _build_carriage_frame():
    """Main carriage structural steel spine, bogies, X-braced bridge, and chopstick hinge clevises."""
    z0 = S.CARRIAGE_Z_BUILT
    h = S.CARRIAGE_H
    x0 = S.CARRIAGE_SPINE_X0
    x1 = S.CARRIAGE_SPINE_X1
    dx = x1 - x0  # 20.0 mm
    xc = (x0 + x1) / 2.0
    yh = S.CARRIAGE_Y_HALF  # 76.0 mm

    parts = []

    # 1. Four wrap-around guide rail bogies (upper & lower on Port & Starboard rails)
    bogie_proto = _build_rail_bogie()
    for sy in (-1, 1):
        for zb in (2.0, h - 30.0):
            parts.append(bd.Pos(0, sy * S.COL_HALF, z0 + zb) * bogie_proto)

    # 2. Heavy bottom and top horizontal box girders spanning full width (Y: -76..+76)
    parts.append(
        bd.Pos(xc, 0, z0)
        * bd.Box(dx, 2.0 * yh, 22.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    )
    parts.append(
        bd.Pos(xc, 0, z0 + h - 22.0)
        * bd.Box(dx, 2.0 * yh, 22.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    )

    # 3. Heavy vertical side columns (at rail line Y=+/-60 and outer hinge posts Y=+/-70)
    for sy in (-1, 1):
        parts.append(
            bd.Pos(xc, sy * 67.0, z0 + 22.0)
            * bd.Box(dx, 18.0, h - 44.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        )
        # Inner vertical frame posts at Y=+/-24
        parts.append(
            bd.Pos(xc, sy * 24.0, z0 + 22.0)
            * bd.Box(14.0, 6.0, h - 44.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        )

    # 4. Mid horizontal tie girder + central X-bracing across the open bridge window
    parts.append(
        bd.Pos(xc, 0, z0 + h / 2.0)
        * bd.Box(12.0, 2.0 * 60.0, 6.5)
    )
    # Central X-braces inside Y in [-58, +58], Z_local in [22, 118]
    for zb0, zb1 in ((22.0, h / 2.0), (h / 2.0, h - 22.0)):
        for y_a, y_b in ((-58.0, -24.0), (-24.0, 24.0), (24.0, 58.0)):
            for p0, p1 in (
                ((xc, y_a, z0 + zb0), (xc, y_b, z0 + zb1)),
                ((xc, y_b, z0 + zb0), (xc, y_a, z0 + zb1)),
            ):
                v0, v1 = bd.Vector(*p0), bd.Vector(*p1)
                d = v1 - v0
                pl = bd.Plane(origin=v0, x_dir=bd.Vector(1, 0, 0), z_dir=d.normalized())
                parts.append(
                    pl
                    * bd.Box(
                        7.0,
                        4.2,
                        d.length,
                        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
                    )
                )

    # 5. Triple-lug chopstick hinge clevises projecting forward from X=x1 (106.5) to HINGE_X (119.5)
    ear_r = 10.5
    for sy in (-1, 1):
        hy = sy * S.HINGE_Y
        for zl0, zl1 in S.CLEVIS_Z_LUGS:
            lug_h = zl1 - zl0
            # Rectangular stem from spine front (x1 - 2) to hinge center (HINGE_X)
            stem = bd.Pos(x1 - 2.0, hy, z0 + zl0) * bd.Box(
                S.HINGE_X - (x1 - 2.0),
                2.0 * ear_r,
                lug_h,
                align=(bd.Align.MIN, bd.Align.CENTER, bd.Align.MIN),
            )
            # Rounded cylindrical nose centered on hinge pin
            nose = bd.Pos(S.HINGE_X, hy, z0 + zl0) * bd.Cylinder(
                ear_r, lug_h, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
            )
            parts.append(stem)
            parts.append(nose)

    frame = parts[0] + parts[1:]

    # Bore clean R=4.8 mm hinge pin holes through all 6 clevis ears (pin R = 4.5 mm!)
    bores = []
    for sy in (-1, 1):
        bores.append(
            bd.Pos(S.HINGE_X, sy * S.HINGE_Y, z0 + 40.0)
            * bd.Cylinder(
                S.HINGE_PIN_R + 0.3,
                84.0,
                align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
            )
        )
    frame = frame - bores
    frame.label = "carriage_frame"
    S.apply_material(frame, S.mat_carriage_steel())
    return frame


def _build_hinge_pins():
    """Twin heavy vertical steel hinge pins with top hydraulic rotary swing-drive caps."""
    z0 = S.CARRIAGE_Z_BUILT
    z_bot = z0 + S.CLEVIS_Z_LUGS[0][0]  # 520 + 46 = 566
    z_top = z0 + S.CLEVIS_Z_LUGS[2][1]  # 520 + 116 = 636
    shaft_h = z_top - z_bot

    shaft = bd.Pos(0, 0, z_bot) * bd.Cylinder(
        S.HINGE_PIN_R, shaft_h, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    cap_bot = bd.Pos(0, 0, z_bot - 2.5) * bd.Cylinder(
        7.2, 2.5, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    # Stepped hydraulic rotary swing-drive housing atop the upper hinge clevis
    drive_flange = bd.Pos(0, 0, z_top) * bd.Cylinder(
        8.6, 3.5, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    drive_motor = bd.Pos(0, 0, z_top + 3.5) * bd.Cylinder(
        6.8, 7.5, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    pin_proto = shaft + [cap_bot, drive_flange, drive_motor]
    S.apply_material(pin_proto, S.mat_guide_rail())

    pin_port = bd.Pos(S.HINGE_X, S.HINGE_Y, 0) * pin_proto
    pin_stbd = bd.Pos(S.HINGE_X, -S.HINGE_Y, 0) * pin_proto
    pin_port.label = "hinge_pin_port"
    pin_stbd.label = "hinge_pin_stbd"

    # Hydraulic Power Unit (HPU) & control manifold enclosure mounted cleanly on front of bottom girder
    hpu = bd.Pos(S.CARRIAGE_SPINE_X1, 0, z0 + 3.0) * bd.Box(
        9.0, 38.0, 16.0, align=(bd.Align.MIN, bd.Align.CENTER, bd.Align.MIN)
    )
    hpu.label = "carriage_hpu"
    S.apply_material(hpu, S.mat_cladding())
    return [pin_port, pin_stbd, hpu]


def _build_traveling_sheave_block():
    """Top carriage drawworks traveling sheave block aligned below the crown front sheaves."""
    z_top = S.CARRIAGE_Z_BUILT + S.CARRIAGE_H  # 660.0
    xc = S.FRONT_CABLE_X + 4.0                 # 94.0 (centered cleanly on top girder X: 86.5..106.5)
    sheave_z = z_top + 13.0
    pitch_r = 7.5
    outer_r = 8.8

    # Cheek housing plates sitting cleanly on top of carriage top girder (Z = 660.0)
    cheeks = []
    for y_pos in (-23.0, -13.0, 13.0, 23.0):
        cheeks.append(
            bd.Pos(xc, y_pos, z_top)
            * bd.Box(16.0, 2.6, 22.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        )
    base_plate = bd.Pos(xc, 0, z_top) * bd.Box(
        18.0, 50.0, 3.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    axle_bore = bd.Pos(xc, 0, sheave_z) * bd.Rot(90, 0, 0) * bd.Cylinder(2.5, 56.0)
    block = (base_plate + cheeks) - axle_bore
    block.label = "traveling_block_housing"
    S.apply_material(block, S.mat_tower_steel())

    axle = bd.Pos(xc, 0, sheave_z) * bd.Rot(90, 0, 0) * bd.Cylinder(2.2, 51.0)
    axle.label = "traveling_block_axle"
    S.apply_material(axle, S.mat_guide_rail())

    wheel_proto = _build_sheave(pitch_r, outer_r, 4.6)
    S.apply_material(wheel_proto, S.mat_sheave())
    p_port = bd.Pos(xc, S.CABLE_Y, sheave_z) * wheel_proto
    p_stbd = bd.Pos(xc, -S.CABLE_Y, sheave_z) * wheel_proto
    p_port.label = "traveling_sheave_port"
    p_stbd.label = "traveling_sheave_stbd"

    return [block, axle, p_port, p_stbd]


@model
def carriage():
    """Complete Mechazilla vertical-travel catch carriage (built at Z = 520..660 mm)."""
    frame = _build_carriage_frame()
    pins = _build_hinge_pins()
    traveling = _build_traveling_sheave_block()
    return bd.Compound(children=[frame, *pins, *traveling], label="carriage")


if __name__ == "__main__":
    carriage()
