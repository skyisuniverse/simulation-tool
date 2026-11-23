"""Minimalist futuristic 2+2 cockpit interior for the Tesla Roadster (2nd gen).

Signature interior cues visible through the panoramic Targa glass canopy:
  - Ultrawhite leather & dark Alcantara sculpted 2+2 sports bucket seats
  - Open-top butterfly Roadster Yoke steering wheel (driver side, +Y)
  - Iconic floating curved center touchscreen console sweeping down from the dash
  - Low-slung minimalist Alcantara dashboard with brushed aluminum accent bar
"""

from __future__ import annotations

import build123d as bd

from lib.palette import (
    ALLOY_SILVER,
    CARBON_SATIN,
    INTERIOR_SHELL,
    INTERIOR_SUEDE,
    INTERIOR_WHITE,
    SCREEN_GLASS,
    SCREEN_GLOW,
    group,
    style_alloy,
    style_carbon,
    style_emissive,
    style_gloss_black,
    style_leather,
    style_trim,
)
from lib.surfaces import box_between


def _build_cabin_tub_and_floor():
    """Carbon cabin floor pan & raised side sill bolsters."""
    parts = []
    # Cabin floor carpet sitting 7 mm cleanly above the 200 kWh battery pack (Z=233)
    floor = box_between(-840.0, 730.0, -565.0, 565.0, 240.0, 256.0)
    parts.append(style_trim(floor, "cabin_floor", INTERIOR_SUEDE, roughness=0.72))

    # Raised sculpted inner carbon sill thresholds along left/right cabin edges
    for side in (1, -1):
        lbl = "left" if side > 0 else "right"
        y0, y1 = (570.0, 625.0) if side > 0 else (-625.0, -570.0)
        sill = box_between(-780.0, 640.0, y0, y1, 242.0, 355.0)
        parts.append(style_carbon(sill, f"cabin_sill_{lbl}", INTERIOR_SHELL))

    # Rear parcel shelf cleanly behind rear_bulkhead (X <= -940 -> start at -946)
    shelf = box_between(-1440.0, -946.0, -390.0, 390.0, 660.0, 682.0)
    parts.append(style_trim(shelf, "rear_parcel_shelf", INTERIOR_SUEDE, roughness=0.72))
    return parts


def _build_dashboard_and_floating_console():
    """Minimalist sculpted dash + iconic floating curved center touchscreen bridge."""
    parts = []

    # Sculpted curved Alcantara dashboard profile (swept laterally across cabin)
    dash_xz = [
        (720.0, 650.0),
        (720.0, 720.0),
        (610.0, 738.0),
        (485.0, 726.0),
        (445.0, 685.0),
        (465.0, 632.0),
        (600.0, 615.0),
        (720.0, 635.0),
    ]
    dash_wire = bd.Wire.make_polygon([bd.Vector(x, -540.0, z) for x, z in dash_xz])
    dash = bd.extrude(bd.Face(dash_wire), 1080.0, dir=(0, 1, 0))
    parts.append(style_trim(dash, "dashboard_upper", INTERIOR_SUEDE, roughness=0.68))

    # Sleek ultrawhite horizontal dash accent blade sitting cleanly 2 mm proud of dash face (X=426..443)
    accent = box_between(426.0, 443.0, -520.0, 520.0, 672.0, 690.0)
    parts.append(style_leather(accent, "dashboard_trim_blade", INTERIOR_WHITE, roughness=0.45))

    # Iconic Tesla Roadster floating curved glass center touchscreen bridge (trimmed cleanly against dash!)
    spine_pts = [
        (460.0, 665.0),
        (410.0, 645.0),
        (310.0, 575.0),
        (190.0, 505.0),
        (40.0, 462.0),
        (-130.0, 446.0),
        (-310.0, 444.0),
    ]
    lower_pts = [(x, z - 28.0) for x, z in reversed(spine_pts)]
    bridge_wire = bd.Wire.make_polygon([bd.Vector(x, -96.0, z) for x, z in (spine_pts + lower_pts)])
    bridge = bd.extrude(bd.Face(bridge_wire), 192.0, dir=(0, 1, 0)) - dash - accent
    parts.append(style_carbon(bridge, "floating_console_bridge", INTERIOR_SHELL, gloss=True))

    # Glossy curved touchscreen display panel riding 2 mm proud of upper console sweep
    scr_top = [(x, z + 6.0) for x, z in spine_pts[1:5]]
    scr_bot = [(x, z + 1.5) for x, z in reversed(spine_pts[1:5])]
    scr_wire = bd.Wire.make_polygon([bd.Vector(x, -86.0, z) for x, z in (scr_top + scr_bot)])
    screen = bd.extrude(bd.Face(scr_wire), 172.0, dir=(0, 1, 0)) - bridge - dash
    parts.append(style_gloss_black(screen, "center_curved_touchscreen", SCREEN_GLASS))

    # Subtle glowing UI strip cleanly 2 mm proud of center screen
    ui_bar = bd.Pos(340.0, 0.0, 611.0) * bd.Rot(0, -34, 0) * bd.Box(105.0, 136.0, 2.5)
    ui_bar = ui_bar - screen - bridge
    if ui_bar.solids():
        parts.append(style_emissive(ui_bar, "touchscreen_ui_accent", SCREEN_GLOW, intensity=0.8))

    # Twin thin cantilevered pedestal legs cleanly below floating bridge (Z=258..412)
    ped = box_between(-308.0, -180.0, -68.0, 68.0, 258.0, 412.0)
    parts.append(style_carbon(ped, "console_rear_pedestal", CARBON_SATIN))

    return parts


def _build_roadster_yoke():
    """Open-top futuristic Tesla Roadster butterfly Yoke steering wheel (+Y driver)."""
    parts = []
    cy = 330.0
    cz = 665.0
    cx = 312.0

    # Steering column strictly spanning the clear gap between dash trim (X=426) and yoke hub (X=340)
    col_p0 = bd.Vector(422.0, cy, 656.0)
    col_p1 = bd.Vector(cx + 30.0, cy, cz)
    col_v = col_p1 - col_p0
    col_plane = bd.Plane(origin=col_p0, z_dir=col_v.normalized())
    col = col_plane * bd.Cylinder(radius=22.0, height=col_v.length, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    parts.append(style_carbon(col, "steering_column", INTERIOR_SHELL))

    # Yoke tilted 16 deg toward driver in local frame
    yoke_loc = bd.Location((cx, cy, cz), (0.0, -16.0, 0.0))

    # Central sculpted hub
    hub = bd.Rot(0, 90, 0) * bd.Cylinder(radius=46.0, height=28.0)
    # Bottom flat bar + left/right sculpted vertical butterfly grips (open top!)
    bot_bar = bd.Pos(0.0, 0.0, -72.0) * bd.Box(26.0, 255.0, 26.0)
    left_grip = bd.Pos(0.0, 138.0, -4.0) * bd.Rot(10, 0, 0) * bd.Box(28.0, 28.0, 148.0)
    right_grip = bd.Pos(0.0, -138.0, -4.0) * bd.Rot(-10, 0, 0) * bd.Box(28.0, 28.0, 148.0)
    mid_spoke = bd.Pos(0.0, 0.0, -6.0) * bd.Box(22.0, 272.0, 28.0)

    yoke_body = hub + bot_bar + left_grip + right_grip + mid_spoke
    yoke_body = yoke_loc * yoke_body
    parts.append(style_leather(yoke_body, "roadster_yoke_wheel", INTERIOR_SUEDE, roughness=0.52))

    # Brushed silver center trim emblem cleanly 2 mm proud of yoke hub face
    emblem = yoke_loc * (bd.Pos(-18.0, 0.0, 0.0) * bd.Box(4.0, 38.0, 14.0))
    parts.append(style_alloy(emblem, "yoke_center_emblem", ALLOY_SILVER, roughness=0.18))

    return parts


def _build_bucket_seat(x_base, y_center, scale=1.0, label_prefix="front_seat"):
    """Sculpted two-tone Ultrawhite & carbon racing bucket seat."""
    parts = []
    w = 400.0 * scale

    # Reclined sculpted backrest + tapered racing headrest (Ultrawhite front face)
    z_head = 918.0 if scale > 0.9 else 842.0
    back_xz = [
        (x_base - 70.0 * scale, 326.0),
        (x_base - 235.0 * scale, 740.0),
        (x_base - 270.0 * scale, z_head),
        (x_base - 318.0 * scale, z_head - 4.0),
        (x_base - 285.0 * scale, 730.0),
        (x_base - 115.0 * scale, 315.0),
    ]
    back_wire = bd.Wire.make_polygon([bd.Vector(x, y_center - w * 0.43, z) for x, z in back_xz])
    backrest = bd.extrude(bd.Face(back_wire), w * 0.86, dir=(0, 1, 0))
    taper_yz = [
        (y_center - w * 0.45, 290.0),
        (y_center + w * 0.45, 290.0),
        (y_center + w * 0.45, 710.0),
        (y_center + w * 0.27, z_head + 10.0),
        (y_center - w * 0.27, z_head + 10.0),
        (y_center - w * 0.45, 710.0),
    ]
    taper_mask = bd.extrude(
        bd.Face(bd.Wire.make_polygon([bd.Vector(x_base - 400.0, y, z) for y, z in taper_yz])),
        450.0,
        dir=(1, 0, 0),
    )
    backrest = backrest & taper_mask

    # Seat base cushion strictly trimmed clear of backrest (zero overlap!)
    cush_xz = [
        (x_base + 235.0 * scale, 322.0),
        (x_base + 235.0 * scale, 368.0),
        (x_base + 40.0 * scale, 342.0),
        (x_base - 110.0 * scale, 318.0),
        (x_base - 110.0 * scale, 272.0),
        (x_base + 185.0 * scale, 282.0),
    ]
    cush_wire = bd.Wire.make_polygon([bd.Vector(x, y_center - w * 0.44, z) for x, z in cush_xz])
    cushion = bd.extrude(bd.Face(cush_wire), w * 0.88, dir=(0, 1, 0)) - backrest

    parts.append(style_leather(cushion, f"{label_prefix}_cushion", INTERIOR_WHITE))
    parts.append(style_leather(backrest, f"{label_prefix}_backrest", INTERIOR_WHITE))

    # Carbon-fiber structural shell behind backrest (matching tapered racing profile)
    shell_xz = [
        (x_base - 118.0 * scale, 314.0),
        (x_base - 288.0 * scale, 728.0),
        (x_base - 322.0 * scale, z_head - 6.0),
        (x_base - 338.0 * scale, z_head - 12.0),
        (x_base - 306.0 * scale, 722.0),
        (x_base - 136.0 * scale, 306.0),
    ]
    shell_wire = bd.Wire.make_polygon([bd.Vector(x, y_center - w * 0.45, z) for x, z in shell_xz])
    shell = (bd.extrude(bd.Face(shell_wire), w * 0.90, dir=(0, 1, 0)) & taper_mask) - backrest - cushion
    parts.append(style_carbon(shell, f"{label_prefix}_carbon_shell", INTERIOR_SHELL, gloss=True))

    # Raised left & right Alcantara side bolsters hugging driver/passenger (strictly outboard of cushion/backrest!)
    for bside in (1, -1):
        blbl = "l" if bside > 0 else "r"
        by0 = (y_center + w * 0.44 + 2.0) if bside > 0 else (y_center - w * 0.44 - 2.0 - 40.0 * scale)
        bol_xz = [
            (x_base + 195.0 * scale, 330.0),
            (x_base + 195.0 * scale, 410.0),
            (x_base - 30.0 * scale, 405.0),
            (x_base - 195.0 * scale, 705.0),
            (x_base - 238.0 * scale, 695.0),
            (x_base - 80.0 * scale, 325.0),
        ]
        bol_wire = bd.Wire.make_polygon([bd.Vector(x, by0, z) for x, z in bol_xz])
        bolster = bd.extrude(bd.Face(bol_wire), 40.0 * scale, dir=(0, 1, 0))
        parts.append(style_trim(bolster, f"{label_prefix}_bolster_{blbl}", INTERIOR_SUEDE, roughness=0.65))

    return parts


def build():
    """Build the complete Roadster 2+2 minimalist futuristic cockpit."""
    seats = []
    # Front driver (+Y) & passenger (-Y) bucket seats (11 mm clear of floating center console!)
    seats.extend(_build_bucket_seat(-35.0, 330.0, scale=1.0, label_prefix="seat_driver"))
    seats.extend(_build_bucket_seat(-35.0, -330.0, scale=1.0, label_prefix="seat_passenger"))
    # Compact +2 rear sports seats behind front seats
    seats.extend(_build_bucket_seat(-535.0, 265.0, scale=0.76, label_prefix="seat_rear_left"))
    seats.extend(_build_bucket_seat(-535.0, -265.0, scale=0.76, label_prefix="seat_rear_right"))

    return group(
        "interior",
        [
            group("cabin_structure", _build_cabin_tub_and_floor()),
            group("dashboard_and_console", _build_dashboard_and_floating_console()),
            group("steering_yoke", _build_roadster_yoke()),
            group("seats_2plus2", seats),
        ],
    )
