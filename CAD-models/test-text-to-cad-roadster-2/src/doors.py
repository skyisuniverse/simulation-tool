"""Left and right articulated dihedral / butterfly doors.

Each door is carved directly from the shared master body & canopy mold lines
with crisp DOOR_GAP shutline clearance so it seats 100% flush in 'cruise' pose
and swings high upward & outward on its compound dihedral hinge axis in
'showroom' pose, exposing the carbon door card and red ambient LED accent.
"""

import build123d as bd
from cad import model
from cad.build123d import memo

from body_surface import (
    cockpit_interior_cavity,
    door_aperture_prism,
    master_body_solid,
    rocker_split_volume,
)
from canopy import _door_glass_window_cut, _hollow_canopy_shell
from spec import (
    DOOR_GAP,
    DOOR_Y_FRONT_BOT,
    DOOR_Y_REAR_BOT,
    apply_alcantara,
    apply_ano_white,
    apply_carbon_black,
    apply_gold_glass,
    apply_red_led,
)


@memo
def _build_door(side_sign):
    side_lbl = "left" if side_sign > 0 else "right"
    master = master_body_solid()

    # 1. Flush Ano White outer door panel carved directly from master body OML
    door_cut = door_aperture_prism(side_sign, inset=DOOR_GAP)
    # Keep upper door waist sill extending inboard to X = 752 so the frameless
    # Gold Glazed door window seats directly onto the door sill with zero gap!
    inboard_trim = bd.Pos(side_sign * 376.0, -200.0, 520.0) * bd.Box(752.0, 1900.0, 900.0)
    upper_body = master - rocker_split_volume()
    outer_skin = (upper_body & door_cut) - [cockpit_interior_cavity(), inboard_trim]

    # Hollow only the lower inner door panel recess (leaving top waist sill intact!)
    inner_recess = bd.Pos(side_sign * 814.0, -220.0, 480.0) * bd.Box(110.0, 1220.0, 410.0)
    outer_skin = outer_skin - inner_recess
    outer_skin.label = f"door_skin_{side_lbl}"
    apply_ano_white(outer_skin)

    # 2. Frameless Gold Glazed side window (carved from shared hollow canopy shell)
    glass_shell = _hollow_canopy_shell(thickness=14.0)
    win_prism = _door_glass_window_cut(side_sign, inset=DOOR_GAP + 2.5)
    door_glass = (glass_shell & win_prism) - master
    door_glass.label = f"door_glass_{side_lbl}"
    apply_gold_glass(door_glass)

    # 3. Sculpted dark carbon/Alcantara interior door card (inset inside door skin)
    # Positioned cleanly inboard of outer_skin with zero overlap
    card_pts = [
        (DOOR_Y_FRONT_BOT + 125.0, 295.0),
        (DOOR_Y_REAR_BOT - 80.0, 325.0),
        (DOOR_Y_REAR_BOT - 40.0, 685.0),
        (DOOR_Y_FRONT_BOT + 175.0, 645.0),
    ]
    x_card = side_sign * 828.0 if side_sign > 0 else -858.0
    card_face = bd.Face(bd.Wire.make_polygon([bd.Vector(x_card, y, z) for y, z in card_pts]))
    door_card = bd.extrude(card_face, 30.0, dir=(1, 0, 0))
    door_card = (door_card & door_cut) - outer_skin

    # Signature diagonal crimson ambient LED strip recessed in the inner door pocket
    # (visible in official 'Supersonic' interior shot & open-door twilight shot!)
    led_pts = [
        (DOOR_Y_FRONT_BOT + 205.0, 468.0),
        (DOOR_Y_REAR_BOT - 155.0, 505.0),
        (DOOR_Y_REAR_BOT - 155.0, 523.0),
        (DOOR_Y_FRONT_BOT + 205.0, 486.0),
    ]
    x_led = side_sign * 820.0 if side_sign > 0 else -832.0
    led_face = bd.Face(bd.Wire.make_polygon([bd.Vector(x_led, y, z) for y, z in led_pts]))
    ambient_led = bd.extrude(led_face, 12.0, dir=(1, 0, 0))
    ambient_led = ambient_led - outer_skin
    ambient_led.label = f"door_ambient_led_{side_lbl}"
    apply_red_led(ambient_led)

    door_card = door_card - ambient_led
    door_card.label = f"door_card_{side_lbl}"
    apply_alcantara(door_card)

    # 4. Black carbon lower structural door sill seal strip
    seal = bd.Pos(side_sign * 862.0, -255.0, 260.0) * bd.Box(34.0, 1220.0, 24.0)
    seal = (seal & door_cut) - [outer_skin, door_card]
    seal.label = f"door_seal_{side_lbl}"
    apply_carbon_black(seal)

    return bd.Compound(
        children=[outer_skin, door_glass, door_card, ambient_led, seal],
        label=f"door_{side_lbl}",
    )


@model
def door_left():
    """Driver-side (+X) articulated dihedral butterfly door."""
    return _build_door(1)


@model
def door_right():
    """Passenger-side (-X) articulated dihedral butterfly door."""
    return _build_door(-1)


if __name__ == "__main__":
    door_left()
    door_right()
