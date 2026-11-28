"""Ano White exterior bodywork, hidden diagonal headlights, full-width front DRL,
side aero camera/marker pods, full-width red rear light bar, recessed RDSTR
license plate, and rear deck wing-strut slots.
"""

import build123d as bd
from cad import model
from cad.build123d import memo

from body_surface import (
    cockpit_interior_cavity,
    door_aperture_prism,
    front_trapezoid_intake_cut,
    master_body_solid,
    master_canopy_solid,
    rocker_split_volume,
    wheel_arch_cutters,
)
from spec import (
    BODY_SKIN_THICKNESS,
    Y_NOSE,
    Y_TAIL,
    apply_amber_led,
    apply_ano_white,
    apply_carbon_black,
    apply_dark_gloss,
    apply_dark_titanium,
    apply_red_led,
    apply_titanium,
    apply_white_led,
)


def _frunk_seam_grooves():
    """Crisp 4 mm recessed hood-to-fender diagonal panel gap grooves."""
    grooves = []
    for sign in (1, -1):
        pts = [
            bd.Vector(sign * 562.0, Y_NOSE - 10.0, 412.0),
            bd.Vector(sign * 576.0, -2040.0, 520.0),
            bd.Vector(sign * 594.0, -1720.0, 624.0),
            bd.Vector(sign * 616.0, -1400.0, 704.0),
            bd.Vector(sign * 645.0, -1200.0, 712.0),
        ]
        path = bd.Wire(bd.Edge.make_spline(pts))
        profile = bd.Plane(origin=pts[0], z_dir=pts[1] - pts[0]) * bd.Rectangle(4.0, 14.0)
        grooves.append(bd.sweep(profile, path=path))
    return grooves


def _rear_wing_strut_slots():
    """Two narrow rear-deck strut slots + internal actuator clearance bays."""
    slots = []
    for sign in (1, -1):
        # Upper deck pass-through slot (extended forward to clear +21 deg deploy arc)
        deck_slot = bd.Pos(sign * 430.0, 1900.0, 815.0) * bd.Box(44.0, 360.0, 140.0)
        # Internal under-deck pivot swing cavity
        inner_bay = bd.Pos(sign * 430.0, 1805.0, 725.0) * bd.Box(48.0, 520.0, 155.0)
        slots.extend([deck_slot, inner_bay])
    return slots


def _hidden_headlights():
    """Signature concealed forward-facing white diagonal triangular LED headlight
    wedges tucked cleanly along the hood-to-fender crease (per 'Hidden Aero' photo).
    """
    lenses = []
    housings = []
    for sign in (1, -1):
        cx = sign * 635.0
        cy = -2050.0
        cz = 532.0
        # Slim dark recessed housing behind the glowing white diagonal LED wedge
        pocket = bd.Box(118.0, 38.0, 26.0)
        pocket = bd.Rot(19.0, sign * -16.0, sign * -6.0) * pocket
        pocket = bd.Pos(cx, cy + 28.0, cz + 10.0) * pocket
        housings.append(pocket)

        # Prominent forward-facing glowing white LED slit flush with the fender step
        led = bd.Box(122.0, 68.0, 24.0)
        led = bd.Rot(19.0, sign * -16.0, sign * -6.0) * led
        led = bd.Pos(cx, cy - 12.0, cz + 2.0) * led
        lenses.append(led)
    return housings, lenses


def _front_drl_strip(master):
    """Razor-thin full-width horizontal white LED DRL blade along front nose edge."""
    raw = bd.Pos(0.0, Y_NOSE + 12.0, 412.0) * bd.Box(1152.0, 32.0, 13.0)
    # Trim cleanly to master body mold line so ends sit flush with fender cheeks
    drl = raw & master
    drl.label = "front_drl"
    apply_white_led(drl)
    return drl


def _rear_lightbar_assembly(master):
    """Edge-to-edge recessed rear light channel, bright primary red LED bar,
    and subtle secondary lower red reflection blade (per hero & close-up views).
    """
    # Recessed dark channel spanning full width across Kamm tail
    slot_cut = bd.Pos(0.0, Y_TAIL - 24.0, 728.0) * bd.Box(1940.0, 82.0, 66.0)

    # Dark gloss recessed inner bezel
    bezel = bd.Pos(0.0, Y_TAIL - 52.0, 728.0) * bd.Box(1860.0, 26.0, 62.0)
    bezel = bezel & master
    bezel.label = "rear_light_housing"
    apply_dark_gloss(bezel)

    # Primary continuous edge-to-edge glowing red LED bar (Z = 735..753)
    bar_main = bd.Pos(0.0, Y_TAIL - 20.0, 744.0) * bd.Box(1880.0, 42.0, 18.0)
    bar_main = (bar_main & master) - bezel
    bar_main.label = "rear_lightbar_main"
    apply_red_led(bar_main)

    # Secondary thin red LED reflection blade right below (Z = 707..715)
    bar_sub = bd.Pos(0.0, Y_TAIL - 24.0, 711.0) * bd.Box(1850.0, 34.0, 8.0)
    bar_sub = (bar_sub & master) - bezel
    bar_sub.label = "rear_lightbar_accent"
    apply_red_led(bar_sub)

    return slot_cut, bezel, bar_main, bar_sub


def _rear_license_plate():
    """Recessed central rectangular 'RDSTR' license plate beneath the rear light bar."""
    y_plate = Y_TAIL - 46.0
    z_plate = 584.0
    # Slight backward tilt matching Kamm tail angle (~11 deg)
    plate_slab = bd.Box(304.0, 12.0, 150.0)
    plate_slab = bd.Rot(10.0, 0.0, 0.0) * plate_slab
    plate_slab = bd.Pos(0.0, y_plate, z_plate) * plate_slab
    plate_slab.label = "license_plate"
    apply_ano_white(plate_slab)

    # 3D raised 'RDSTR' typography facing straight rearward (+Y)
    txt_2d = bd.Text("RDSTR", font_size=56.0, font_style=bd.FontStyle.BOLD)
    txt_3d = bd.extrude(txt_2d, 4.0)
    # Text is built in XY facing +Z -> rotate to face +Y (rearward, readable from behind!)
    # Looking from +Y toward -Y: +X is left, -X is right -> rotate X by +90, Z by 180
    txt_3d = bd.Rot(0.0, 0.0, 180.0) * (bd.Rot(90.0, 0.0, 0.0) * txt_3d)
    txt_3d = bd.Rot(10.0, 0.0, 0.0) * txt_3d
    txt_3d = bd.Pos(0.0, y_plate + 6.5, z_plate) * txt_3d
    txt_3d.label = "license_plate_text"
    apply_dark_titanium(txt_3d)

    pocket_cut = bd.Pos(0.0, y_plate + 18.0, z_plate) * bd.Box(318.0, 56.0, 162.0)
    pocket_cut = bd.Rot(10.0, 0.0, 0.0) * (bd.Pos(0.0, -y_plate - 18.0, -z_plate) * pocket_cut)
    pocket_cut = bd.Pos(0.0, y_plate + 18.0, z_plate) * pocket_cut
    return pocket_cut, plate_slab, txt_3d


def _side_camera_marker_pods(master):
    """Flush slim black horizontal aero pods with amber side-marker LED behind front arches."""
    cutters = []
    pods = []
    leds = []
    for sign in (1, -1):
        # Positioned cleanly ahead of front door shutline (Y = -1056 .. -922, Z = 602..628)
        raw_pod = bd.Pos(sign * 948.0, -989.0, 615.0) * bd.Box(72.0, 134.0, 25.0)
        pod = raw_pod & master
        pod.label = f"side_pod_{'l' if sign > 0 else 'r'}"

        raw_led = bd.Pos(sign * 958.0, -1012.0, 615.0) * bd.Box(62.0, 62.0, 11.0)
        led = raw_led & master
        led.label = f"side_marker_{'l' if sign > 0 else 'r'}"
        apply_amber_led(led)

        pod = pod - led
        apply_dark_gloss(pod)

        cutters.append(bd.Pos(sign * 948.0, -989.0, 615.0) * bd.Box(78.0, 138.0, 29.0))
        pods.append(pod)
        leds.append(led)
    return cutters, pods, leds


def _rear_corner_vent_cut(sign):
    """Sculpted trapezoidal rear corner aero exit vent flowing under the light bar."""
    pts_xz = [
        (sign * 635.0, 488.0),
        (sign * 925.0, 488.0),
        (sign * 935.0, 675.0),
        (sign * 710.0, 645.0),
    ]
    if sign < 0:
        pts_xz = list(reversed(pts_xz))
    face = bd.Face(bd.Wire.make_polygon([bd.Vector(x, Y_TAIL - 95.0, z) for x, z in pts_xz]))
    return bd.extrude(face, 125.0, dir=(0, 1, 0))


@memo
def _build_body():
    master = master_body_solid()
    canopy = master_canopy_solid()

    # Start with Ano White upper outer mold line (everything above carbon rockers)
    shell = master - rocker_split_volume()

    # Cut wheel arches, butterfly door apertures, and hollow interior cockpit
    door_l = door_aperture_prism(1, inset=0.0)
    door_r = door_aperture_prism(-1, inset=0.0)
    cabin = cockpit_interior_cavity()

    # Cut front trapezoidal dark intake mouth, hood panel grooves, wing strut slots
    front_intake_cut = front_trapezoid_intake_cut()
    hood_grooves = _frunk_seam_grooves()
    wing_slots = _rear_wing_strut_slots()

    # Rear lightbar recess & license plate pocket & outer rear corner sculpted vents
    rear_slot_cut, rear_bezel, rear_bar_main, rear_bar_sub = _rear_lightbar_assembly(master)
    plate_cut, plate_slab, plate_text = _rear_license_plate()
    rear_vent_l = _rear_corner_vent_cut(1)
    rear_vent_r = _rear_corner_vent_cut(-1)

    # Hidden headlights & side camera/marker pods
    hl_housings, hl_lenses = _hidden_headlights()
    pod_cuts, side_pods, side_leds = _side_camera_marker_pods(master)

    # Front DRL
    drl = _front_drl_strip(master)
    drl_cut = bd.Pos(0.0, Y_NOSE + 12.0, 412.0) * bd.Box(1158.0, 38.0, 18.0)

    # Trim headlight lenses & housings cleanly to master body outer mold line
    hl_parts = []
    for idx, (h_raw, l_raw) in enumerate(zip(hl_housings, hl_lenses), start=1):
        side_lbl = "l" if idx == 1 else "r"
        lens = l_raw & master
        lens.label = f"headlight_led_{side_lbl}"
        apply_white_led(lens)
        housing = (h_raw & master) - lens
        housing.label = f"headlight_housing_{side_lbl}"
        apply_dark_gloss(housing)
        hl_parts.extend([housing, lens])

    # Rear corner dark aero vent backing plates seated cleanly inside sculpted vents
    rear_vent_backs = []
    for side_lbl, sign, vent_vol in (("l", 1, rear_vent_l), ("r", -1, rear_vent_r)):
        vb_slab = bd.Pos(sign * 785.0, Y_TAIL - 88.0, 580.0) * bd.Box(310.0, 20.0, 200.0)
        vb = (vb_slab & vent_vol) & master
        vb.label = f"rear_corner_vent_{side_lbl}"
        apply_carbon_black(vb)
        rear_vent_backs.append(vb)

    # Apply all subtractions cleanly to the Ano White body shell
    all_cuts = [
        *wheel_arch_cutters(extra_r=0.0),
        door_l,
        door_r,
        cabin,
        front_intake_cut,
        drl_cut,
        rear_slot_cut,
        plate_cut,
        rear_vent_l,
        rear_vent_r,
        *wing_slots,
        *hood_grooves,
        *hl_housings,
        *hl_lenses,
        *rear_vent_backs,
        *pod_cuts,
        # Slight relief under rear glass seating edge so canopy glass sits flush
        canopy,
    ]
    body_shell = shell - all_cuts
    body_shell.label = "ano_white_body"
    apply_ano_white(body_shell)

    return bd.Compound(
        children=[
            body_shell,
            drl,
            *hl_parts,
            *side_pods,
            *side_leds,
            rear_bezel,
            rear_bar_main,
            rear_bar_sub,
            plate_slab,
            plate_text,
            *rear_vent_backs,
        ],
        label="body",
    )


@model
def body():
    """Ano White sculpted Roadster exterior bodywork with lighting, pods, and RDSTR plate."""
    return _build_body()


if __name__ == "__main__":
    body()
