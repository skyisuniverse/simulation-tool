"""Tesla Semi iconic central-driver cockpit interior.

Visible through the expansive wraparound smoked panoramic windshield:
  - Standing-height cabin floor deck
  - Sculpted minimalist wraparound dashboard & center console
  - Central steering column & 3-spoke Tesla steering wheel
  - Twin flanking 15-inch floating Tesla touchscreens angled toward the driver
  - Central high-back bolstered air-ride driver's seat with twin armrests
  - Rear-right folding jump seat (authentic Tesla Semi 1+1 layout)
"""

import build123d as bd
from bd_materials import metals, plastics
from cad import model

import dims as D


def _matte(part, color=D.COLOR_INTERIOR_DARK, roughness=0.72):
    part.material = plastics.abs_()
    part.material.pbr = part.material.pbr.override(roughness=roughness, metalness=0.05)
    part.color = color
    return part


def _leather(part, color=D.COLOR_SEAT_LEATHER, roughness=0.62):
    part.material = plastics.tpu()
    part.material.pbr = part.material.pbr.override(roughness=roughness, metalness=0.04)
    part.color = color
    return part


def _metal(part, color=D.COLOR_CHROME, roughness=0.28, metalness=0.88):
    part.material = metals.aluminum()
    part.material.pbr = part.material.pbr.override(roughness=roughness, metalness=metalness)
    part.color = color
    return part


def _make_floor_and_dash():
    """Cabin floor deck and sculpted minimalist wraparound dashboard."""
    parts = []

    # Flat standing cabin floor (Z = 1152 .. 1182, well above wheel arch peak 1131)
    with bd.BuildSketch(bd.Plane.XY) as fsk:
        with bd.BuildLine():
            bd.Polyline(
                (-740.0, 1080.0),
                (740.0, 1080.0),
                (860.0, 1850.0),
                (880.0, 3420.0),
                (-880.0, 3420.0),
                (-860.0, 1850.0),
                close=True,
            )
        bd.make_face()
    floor = bd.Pos(0, 0, 1152.0) * bd.extrude(fsk.sketch.face(), amount=30.0, dir=(0, 0, 1))
    floor.label = "cabin_floor"
    parts.append(_matte(floor, color="#1D2026", roughness=0.82))

    # Minimalist curved wraparound dashboard shelf (Y = 1040 .. 1420, Z = 1520 .. 1645)
    with bd.BuildSketch(bd.Plane.XY) as dsk:
        with bd.BuildLine():
            s_front = bd.ThreePointArc((-760.0, 1210.0), (0.0, 1040.0), (760.0, 1210.0))
            l_r = bd.Line((760.0, 1210.0), (740.0, 1450.0))
            s_back = bd.ThreePointArc((740.0, 1450.0), (0.0, 1340.0), (-740.0, 1450.0))
            l_l = bd.Line((-740.0, 1450.0), (-760.0, 1210.0))
        bd.make_face()
    dash = bd.Pos(0, 0, 1525.0) * bd.extrude(dsk.sketch.face(), amount=115.0, dir=(0, 0, 1))
    dash.label = "dashboard_upper"
    parts.append(_matte(dash, color=D.COLOR_INTERIOR_DARK, roughness=0.65))

    # Central lower pedestal console supporting steering column (Z = 1185 .. 1522)
    console = (
        bd.Pos(0.0, 1265.0, 1353.0)
        * bd.Box(340.0, 260.0, 336.0)
    )
    console.label = "center_console"
    parts.append(_matte(console, color="#22262C", roughness=0.68))

    # Brushed aluminum curved horizontal dash accent trim bar facing the driver (4 mm aft of dash)
    with bd.BuildSketch(bd.Plane.XY) as tsk:
        with bd.BuildLine():
            s_front = bd.ThreePointArc((-680.0, 1448.0), (0.0, 1346.0), (680.0, 1448.0))
            l_r = bd.Line((680.0, 1448.0), (680.0, 1460.0))
            s_back = bd.ThreePointArc((680.0, 1460.0), (0.0, 1358.0), (-680.0, 1460.0))
            l_l = bd.Line((-680.0, 1460.0), (-680.0, 1448.0))
        bd.make_face()
    trim = bd.Pos(0, 0, 1578.0) * bd.extrude(tsk.sketch.face(), amount=22.0, dir=(0, 0, 1))
    trim.label = "dash_accent_trim"
    parts.append(_metal(trim, color="#AEB6C0", roughness=0.3))

    return parts


def _make_steering_and_screens():
    """Central steering column, 3-spoke Tesla steering wheel, and twin 15-inch displays."""
    parts = []

    # Tilted central steering column (clear of dash trim ahead and steering wheel hub aft)
    col_frame = bd.Pos(0.0, 1552.0, 1662.0) * bd.Rot(-66, 0, 0)
    column = col_frame * bd.Cylinder(42.0, 290.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.CENTER))
    column.label = "steering_column"
    parts.append(_matte(column, color="#1D2025", roughness=0.55))

    # 3-spoke Tesla steering wheel positioned cleanly at the driver end of the column
    wheel_frame = bd.Pos(0.0, 1718.0, 1735.0) * bd.Rot(-66, 0, 0)
    # Thick outer steering rim (torus: major R=192, minor r=18)
    rim = wheel_frame * bd.Torus(192.0, 18.0)
    # Central airbag hub
    hub = wheel_frame * bd.Cylinder(68.0, 42.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.CENTER))
    # 3 spokes (left, right, bottom)
    spoke_l = wheel_frame * bd.Pos(126.0, 0.0, 0.0) * bd.Box(118.0, 34.0, 22.0)
    spoke_r = wheel_frame * bd.Pos(-126.0, 0.0, 0.0) * bd.Box(118.0, 34.0, 22.0)
    spoke_b = wheel_frame * bd.Pos(0.0, -126.0, 0.0) * bd.Box(38.0, 118.0, 22.0)
    steering_wheel = rim + hub + spoke_l + spoke_r + spoke_b
    steering_wheel.label = "steering_wheel"
    parts.append(_leather(steering_wheel, color="#1A1D22", roughness=0.5))

    # Twin flanking 15-inch floating Tesla touchscreens (left +X, right -X)
    for side, sgn in (("left", 1.0), ("right", -1.0)):
        # Angled 18 deg INWARD toward central driver (+sgn*18 about Z) and tilted 14 deg back
        scr_frame = bd.Pos(sgn * 430.0, 1565.0, 1745.0) * bd.Rot(-14, 0, sgn * 18)

        # Slim matte-black aluminum display housing (360 x 232 x 16 mm)
        bezel = scr_frame * bd.Box(360.0, 16.0, 232.0)
        bezel.label = f"touchscreen_bezel_{side}"
        parts.append(_matte(bezel, color=D.COLOR_SCREEN_BEZEL, roughness=0.32))

        # Active glossy glass display panel facing driver (+Y local), 1 mm clear of bezel face
        glass = scr_frame * bd.Pos(0.0, 10.5, 0.0) * bd.Box(342.0, 3.0, 214.0)
        glass.label = f"touchscreen_display_{side}"
        glass.material = plastics.pmma()
        glass.material.pbr = glass.material.pbr.override(
            roughness=0.08,
            clearcoat=1.0,
            emissive=(0.12, 0.22, 0.36),
            emissive_intensity=0.8,
        )
        glass.color = D.COLOR_SCREEN_UI
        parts.append(glass)

        # Sleek mounting stalk from dash into back of display bezel
        stalk = (
            bd.Pos(sgn * 430.0, 1465.0, 1665.0)
            * bd.Rot(-32, 0, 0)
            * bd.Cylinder(18.0, 155.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.CENTER))
        )
        stalk.label = f"touchscreen_stalk_{side}"
        parts.append(_matte(stalk, color="#1E2126", roughness=0.45))

    return parts


def _make_driver_seat():
    """Central air-ride bolstered Tesla Semi driver's seat + rear-right folding jump seat."""
    parts = []
    yc = 2210.0

    # Air-ride accordion pedestal resting cleanly on cabin floor (Z = 1184 .. 1490)
    pedestal = (
        bd.Pos(0.0, yc, 1337.0)
        * bd.Box(310.0, 340.0, 304.0)
    )
    pedestal.label = "driver_seat_pedestal"
    parts.append(_matte(pedestal, color="#1B1E23", roughness=0.72))

    # Contoured lower seat cushion + side bolsters (Z = 1492 .. 1615)
    cushion_main = bd.Pos(0.0, yc - 25.0, 1548.0) * bd.Box(490.0, 510.0, 108.0)
    bolster_l = bd.Pos(245.0, yc - 20.0, 1582.0) * bd.Box(72.0, 495.0, 128.0)
    bolster_r = bd.Pos(-245.0, yc - 20.0, 1582.0) * bd.Box(72.0, 495.0, 128.0)
    seat_base = cushion_main + bolster_l + bolster_r
    seat_base.label = "driver_seat_cushion"
    parts.append(_leather(seat_base))

    # Tall sculpted high-back backrest with integrated headrest (reclined 13 deg rearward)
    back_frame = bd.Pos(0.0, yc + 234.0, 1988.0) * bd.Rot(13, 0, 0)
    back_main = back_frame * bd.Box(470.0, 115.0, 680.0)
    back_bol_l = back_frame * bd.Pos(235.0, -28.0, -30.0) * bd.Box(76.0, 145.0, 590.0)
    back_bol_r = back_frame * bd.Pos(-235.0, -28.0, -30.0) * bd.Box(76.0, 145.0, 590.0)
    headrest = back_frame * bd.Pos(0.0, -10.0, 435.0) * bd.Box(290.0, 110.0, 210.0)
    backrest = back_main + back_bol_l + back_bol_r + headrest
    backrest.label = "driver_seat_backrest"
    parts.append(_leather(backrest))

    # Twin flip-down ergonomic armrests (left & right of central driver seat)
    for side, sgn in (("left", 1.0), ("right", -1.0)):
        arm = bd.Pos(sgn * 320.0, yc + 35.0, 1800.0) * bd.Box(72.0, 370.0, 58.0)
        arm.label = f"driver_armrest_{side}"
        parts.append(_leather(arm, color="#252930"))

    # Authentic Tesla Semi rear-right passenger / trainer folding jump seat
    jx, jy = -520.0, 2940.0
    jump_ped = bd.Pos(jx, jy, 1345.0) * bd.Box(240.0, 260.0, 320.0)
    jump_cush = bd.Pos(jx, jy - 15.0, 1550.0) * bd.Box(420.0, 420.0, 86.0)
    jump_back = bd.Pos(jx, jy + 185.0, 1915.0) * bd.Rot(10, 0, 0) * bd.Box(410.0, 92.0, 660.0)
    jump_seat = jump_ped + jump_cush + jump_back
    jump_seat.label = "passenger_jump_seat"
    parts.append(_leather(jump_seat, color="#24282F"))

    return parts


@model
def interior():
    """Complete Tesla Semi central-driver fighter-jet cockpit interior."""
    parts = []
    parts.extend(_make_floor_and_dash())
    parts.extend(_make_steering_and_screens())
    parts.extend(_make_driver_seat())
    return bd.Compound(children=parts, label="interior")


if __name__ == "__main__":
    interior()
