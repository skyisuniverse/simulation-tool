"""Minimalist 'Supersonic' two-seat cockpit interior (per official interior photo):
- Two fixed low-slung bucket seats with Ultrawhite center pads & Alcantara bolsters
- Wide sculpted Ultrawhite structural center console spine & recessed charger tray
- Dark Alcantara/carbon full-width dashboard shelf & rear cabin bulkhead
- Central floating 15-inch landscape touchscreen + two forward telemetry displays
- Steer-by-wire Ultrawhite aerospace yoke (LHD, +X driver position)
"""

import build123d as bd
from cad import model
from cad.build123d import memo

from spec import (
    apply_alcantara,
    apply_carbon_black,
    apply_dark_gloss,
    apply_dark_titanium,
    apply_titanium,
    apply_ultrawhite_interior,
)


def _fixed_bucket_seat(side_sign, label):
    """Fixed low-slung racing bucket seat (Alcantara shell/bolsters + Ultrawhite pads)."""
    cx = side_sign * 390.0

    # 1. Alcantara outer bucket shell & tall contoured side bolsters
    # Side-view L-recline profile: cushion Y=-240..+190, backrest reclined ~26 deg up to Z=860
    shell_pts = [
        (-255.0, 215.0),
        (190.0, 215.0),
        (460.0, 775.0),
        (415.0, 865.0),
        (345.0, 865.0),
        (130.0, 315.0),
        (-240.0, 295.0),
    ]
    s_face = bd.Face(bd.Wire.make_polygon([bd.Vector(cx - 215.0, y, z) for y, z in shell_pts]))
    outer_shell = bd.extrude(s_face, 430.0, dir=(1, 0, 0))

    # Carve central cushion recess leaving sculpted side bolsters on both sides
    recess_pts = [
        (-260.0, 280.0),
        (145.0, 305.0),
        (365.0, 875.0),
        (260.0, 875.0),
        (55.0, 395.0),
        (-260.0, 385.0),
    ]
    r_face = bd.Face(bd.Wire.make_polygon([bd.Vector(cx - 145.0, y, z) for y, z in recess_pts]))
    recess = bd.extrude(r_face, 290.0, dir=(1, 0, 0))
    bolsters = outer_shell - recess
    bolsters.label = f"{label}_bolsters"
    apply_alcantara(bolsters)

    # 2. Crisp Ultrawhite center seat cushion + backrest + integrated headrest pad
    pad_pts = [
        (-235.0, 295.0),
        (132.0, 315.0),
        (346.0, 862.0),
        (308.0, 876.0),
        (95.0, 372.0),
        (-235.0, 348.0),
    ]
    p_face = bd.Face(bd.Wire.make_polygon([bd.Vector(cx - 138.0, y, z) for y, z in pad_pts]))
    white_pad = bd.extrude(p_face, 276.0, dir=(1, 0, 0))
    white_pad = white_pad - bolsters
    white_pad.label = f"{label}_cushion"
    apply_ultrawhite_interior(white_pad)

    return bd.Compound(children=[bolsters, white_pad], label=label)


def _center_console_spine():
    """Wide sculpted Ultrawhite center tunnel spine + dark forward charger well."""
    # Rear sculpted Ultrawhite center console bridge between the two fixed seats
    pts_yz = [
        (-520.0, 215.0),
        (450.0, 215.0),
        (450.0, 445.0),
        (-360.0, 435.0),
        (-520.0, 340.0),
    ]
    face = bd.Face(bd.Wire.make_polygon([bd.Vector(-140.0, y, z) for y, z in pts_yz]))
    spine = bd.extrude(face, 280.0, dir=(1, 0, 0))
    # Subtle side bevels along upper console edges for sleek sculptural feel
    bevel_l = bd.Pos(135.0, -35.0, 445.0) * (bd.Rot(0.0, 35.0, 0.0) * bd.Box(55.0, 990.0, 55.0))
    bevel_r = bd.Pos(-135.0, -35.0, 445.0) * (bd.Rot(0.0, -35.0, 0.0) * bd.Box(55.0, 990.0, 55.0))
    spine = spine - [bevel_l, bevel_r]
    spine.label = "center_console_spine"
    apply_ultrawhite_interior(spine)

    # Dark carbon recessed wireless charger & control tray extending forward to dash
    tray = bd.Pos(0.0, -640.0, 330.0) * bd.Box(240.0, 236.0, 225.0)
    tray_cut = bd.Pos(0.0, -610.0, 425.0) * bd.Box(190.0, 175.0, 65.0)
    tray = tray - tray_cut
    tray.label = "center_console_tray"
    apply_carbon_black(tray)

    return spine, tray


def _dashboard_and_displays():
    """Minimalist dark Alcantara dash shelf, floating 15" touchscreen, & dual forward displays."""
    # 1. Full-width minimalist dark Alcantara upper dash shelf
    dash_pts = [
        (-920.0, 575.0),
        (-615.0, 585.0),
        (-615.0, 668.0),
        (-920.0, 682.0),
    ]
    d_face = bd.Face(bd.Wire.make_polygon([bd.Vector(-685.0, y, z) for y, z in dash_pts]))
    dash = bd.extrude(d_face, 1370.0, dir=(1, 0, 0))
    dash.label = "dashboard_shelf"
    apply_alcantara(dash)

    # 2. Central floating landscape touchscreen (tilted cleanly toward cockpit)
    screen = bd.Box(355.0, 14.0, 212.0)
    screen = bd.Rot(14.0, 0.0, 0.0) * screen
    screen = bd.Pos(0.0, -568.0, 645.0) * screen
    screen.label = "center_touchscreen"
    apply_dark_gloss(screen)

    # Slim titanium mounting neck connecting screen to dash
    mount = bd.Pos(0.0, -596.0, 635.0) * bd.Box(90.0, 38.0, 70.0)
    mount = mount - [dash, screen]
    mount.label = "screen_mount"
    apply_dark_titanium(mount)

    # 3. Two smaller forward telemetry displays ahead of driver yoke (per official copy!)
    disp_left = bd.Box(150.0, 12.0, 66.0)
    disp_left = bd.Rot(16.0, 0.0, 0.0) * disp_left
    disp_left = bd.Pos(470.0, -695.0, 710.0) * disp_left
    disp_left.label = "forward_display_outer"
    apply_dark_gloss(disp_left)

    disp_right = bd.Box(135.0, 12.0, 62.0)
    disp_right = bd.Rot(16.0, 0.0, 0.0) * disp_right
    disp_right = bd.Pos(295.0, -695.0, 708.0) * disp_right
    disp_right.label = "forward_display_inner"
    apply_dark_gloss(disp_right)

    return dash, screen, mount, disp_left, disp_right


def _steer_by_wire_yoke():
    """Compact aerospace steer-by-wire yoke (Ultrawhite outer rim + dark faceted center hub)."""
    # Built in local coordinates (wheel plane = XZ, facing +Y toward driver), then tilted & placed!
    # Outer flattened-stadium yoke rim: width 310 mm, height 178 mm, tube thickness 26 mm
    outer_box = bd.Box(310.0, 28.0, 178.0)
    outer_box = outer_box.fillet(46.0, outer_box.edges().filter_by(bd.Axis.Y))
    inner_cut = bd.Box(244.0, 42.0, 118.0)
    inner_cut = inner_cut.fillet(26.0, inner_cut.edges().filter_by(bd.Axis.Y))
    # Subtle aerospace U-notch across the top center of the yoke rim (per 'Supersonic' photo!)
    top_notch = bd.Pos(0.0, 0.0, 88.0) * bd.Box(125.0, 42.0, 40.0)
    rim = outer_box - [inner_cut, top_notch]
    rim.label = "yoke_rim"
    apply_ultrawhite_interior(rim)

    # Faceted dark central airbag hub & horizontal lower spokes
    hub = bd.Box(108.0, 44.0, 96.0)
    hub = hub.fillet(16.0, hub.edges().filter_by(bd.Axis.Y))
    spokes = bd.Pos(0.0, -6.0, -14.0) * bd.Box(262.0, 22.0, 30.0)
    center = (hub + spokes) - rim
    center.label = "yoke_hub"
    apply_dark_titanium(center)

    # Steering column barrel reaching forward cleanly to meet the dash front face
    col = bd.Pos(0.0, -78.0, 0.0) * (bd.Rot(90.0, 0.0, 0.0) * bd.Cylinder(26.0, 110.0))
    col = col - center
    col.label = "steering_column"
    apply_carbon_black(col)

    yoke = bd.Compound(children=[rim, center, col], label="steer_by_wire_yoke")
    # Place on driver's left (+X = 390 mm), tilted 16 deg ergonomically toward driver
    return bd.Pos(390.0, -455.0, 622.0) * (bd.Rot(16.0, 0.0, 0.0) * yoke)


def _rear_bulkhead_and_floor_mat():
    """Dark Alcantara rear cabin firewall panel and smooth cockpit carpet floor."""
    # Rear cabin bulkhead panel closing the space cleanly behind the two bucket seats
    firewall = bd.Pos(0.0, 495.0, 520.0) * bd.Box(1320.0, 32.0, 560.0)
    firewall.label = "rear_bulkhead"
    apply_alcantara(firewall)

    # Flat cabin floor carpet seated cleanly at Z = 190..212 (above chassis floor Z=165)
    carpet = bd.Pos(0.0, -210.0, 200.0) * bd.Box(1360.0, 1340.0, 24.0)
    carpet.label = "cabin_floor"
    apply_carbon_black(carpet)

    return firewall, carpet


@memo
def _build_interior():
    seat_l = _fixed_bucket_seat(1, "seat_driver")
    seat_r = _fixed_bucket_seat(-1, "seat_passenger")
    spine, tray = _center_console_spine()
    dash, screen, mount, d_out, d_in = _dashboard_and_displays()
    yoke = _steer_by_wire_yoke()
    firewall, carpet = _rear_bulkhead_and_floor_mat()

    return bd.Compound(
        children=[
            seat_l,
            seat_r,
            spine,
            tray,
            dash,
            screen,
            mount,
            d_out,
            d_in,
            yoke,
            firewall,
            carpet,
        ],
        label="interior",
    )


@model
def interior():
    """Minimalist 'Supersonic' two-seat cockpit interior."""
    return _build_interior()


if __name__ == "__main__":
    interior()
