"""Active rear wing assembly: cambered two-tone airfoil (Ano White top +
anodized bronze-titanium underside), sculpted angular downturned endplates with
glowing red LED trailing edges, and dual curved dark-titanium swan-neck struts.

Built in its stowed / low-drag cruise position (just above the rear deck with
zero collision) and pivots cleanly +18 deg upward into high-downforce Track pose
about (0, WING_PIVOT_Y, WING_PIVOT_Z).
"""

import build123d as bd
from cad import model
from cad.build123d import memo

from spec import (
    WING_CHORD,
    WING_PIVOT_Y,
    WING_PIVOT_Z,
    WING_SPAN,
    WING_STOWED_Y_LE,
    apply_ano_white,
    apply_bronze_titanium,
    apply_dark_titanium,
    apply_red_led,
)


def _airfoil_section(x, half_span, chord, y_le, z_base, upper=True):
    """Build upper or lower half of an inverted downforce airfoil at lateral X."""
    u = abs(x) / half_span  # 0 at center, 1 at wingtip
    # Gentle aerodynamic center arch (+18 mm at center, tapering cleanly to tips)
    z_arch = z_base + 18.0 * (1.0 - u * u)
    # Subtle rearward sweep of leading edge toward wingtips (+24 mm)
    y0 = y_le + 24.0 * (u * u)
    # Slight chord taper toward wingtips (285 mm center -> 248 mm tip)
    c = chord * (1.0 - 0.13 * u * u)
    # Stowed gentle -2.5 deg deck slope along Y
    dz_te = -10.0

    # Airfoil thickness distribution (cambered inverted downforce profile)
    p_le = bd.Vector(x, y0, z_arch + 8.0)
    p_te = bd.Vector(x, y0 + c, z_arch + 8.0 + dz_te)
    p_mid_split = bd.Vector(x, y0 + 0.45 * c, z_arch + 8.0 + 0.45 * dz_te)

    if upper:
        # Clean crisp Ano White top surface (very slightly crowned)
        p_t1 = bd.Vector(x, y0 + 0.25 * c, z_arch + 21.0 + 0.25 * dz_te)
        p_t2 = bd.Vector(x, y0 + 0.62 * c, z_arch + 18.0 + 0.62 * dz_te)
        outer = bd.Edge.make_spline([p_le, p_t1, p_t2, p_te])
        chord_edge = bd.Edge.make_spline([p_te, p_mid_split, p_le])
    else:
        # Cambered bronze-titanium downforce suction underside
        p_b1 = bd.Vector(x, y0 + 0.28 * c, z_arch - 10.0 + 0.28 * dz_te)
        p_b2 = bd.Vector(x, y0 + 0.65 * c, z_arch - 4.0 + 0.65 * dz_te)
        outer = bd.Edge.make_spline([p_te, p_b2, p_b1, p_le])
        chord_edge = bd.Edge.make_spline([p_le, p_mid_split, p_te])

    return bd.Face(bd.Wire([outer, chord_edge]))


def _wing_main_planes():
    """Two-tone main airfoil: Ano White upper skin + Bronze-Titanium suction underside."""
    half = WING_SPAN / 2.0
    xs = [-half, -half * 0.5, 0.0, half * 0.5, half]
    z_base = 856.0  # Cleanly above rear deck (Z <= 838) in stowed pose!

    top_secs = [_airfoil_section(x, half, WING_CHORD, WING_STOWED_Y_LE, z_base, upper=True) for x in xs]
    bot_secs = [_airfoil_section(x, half, WING_CHORD, WING_STOWED_Y_LE, z_base, upper=False) for x in xs]

    wing_top = bd.loft(top_secs, ruled=False)
    wing_top.label = "wing_top_skin"
    apply_ano_white(wing_top)

    # Shift bottom half down 0.5 mm so top & bottom meet cleanly without sharing volume
    wing_bot = bd.Pos(0.0, 0.0, -0.5) * bd.loft(bot_secs, ruled=False)
    wing_bot.label = "wing_underside"
    apply_bronze_titanium(wing_bot)

    return wing_top, wing_bot


def _wing_endplates(wing_top, wing_bot):
    """Sculpted angular downturned endplates with glowing red LED trailing edges.

    Profile clears the Ano White rear deck (Z <= 838) ahead of Y_TAIL in stowed
    cruise pose and drops boldly downward behind the Kamm tail undercut.
    """
    half = WING_SPAN / 2.0
    y0 = WING_STOWED_Y_LE + 24.0
    c = WING_CHORD * 0.87
    z0 = 860.0

    parts = []
    for side_lbl, sign in (("l", 1), ("r", -1)):
        # Swept aerospace endplate: stays above Z=848 over the rear deck (<=Y_TAIL+4)
        # and drops boldly down behind the undercut Kamm tail (Y = 2284..2310)!
        pts_yz = [
            (y0 - 32.0, z0 + 22.0),
            (2288.0, z0 + 18.0),
            (2310.0, z0 - 60.0),
            (2284.0, z0 - 54.0),
            (2282.0, z0 - 10.0),
            (y0 - 44.0, z0 - 8.0),
        ]
        face = bd.Face(bd.Wire.make_polygon([bd.Vector(0.0, y, z) for y, z in pts_yz]))
        plate = bd.extrude(face, 14.0, dir=(1, 0, 0))
        plate = bd.Pos(-7.0, 0.0, 0.0) * plate
        plate = bd.Pos(0.0, -y0, -z0) * plate
        plate = bd.Rot(0.0, sign * 10.0, 0.0) * plate
        plate = bd.Pos(sign * (half + 8.0), y0, z0) * plate

        # Glowing red LED accent strip along trailing edge (clears Kamm tail cleanly!)
        led_pts = [
            (2284.0, z0 + 12.0),
            (2294.0, z0 + 12.0),
            (2314.0, z0 - 58.0),
            (2302.0, z0 - 58.0),
        ]
        led_face = bd.Face(bd.Wire.make_polygon([bd.Vector(0.0, y, z) for y, z in led_pts]))
        led = bd.extrude(led_face, 10.0, dir=(1, 0, 0))
        led = bd.Pos(-5.0, -y0, -z0) * led
        led = bd.Rot(0.0, sign * 10.0, 0.0) * led
        led = bd.Pos(sign * (half + 8.0), y0, z0) * led
        led = led - [wing_top, wing_bot]
        led.label = f"wing_endplate_led_{side_lbl}"
        apply_red_led(led)

        plate = plate - [led, wing_top, wing_bot]
        plate.label = f"wing_endplate_{side_lbl}"
        apply_ano_white(plate)

        parts.extend([plate, led])
    return parts


def _swan_neck_struts(wing_top, wing_bot):
    """Dual curved dark titanium actuating struts seated cleanly beneath the foil."""
    struts = []
    for side_lbl, sign in (("l", 1), ("r", -1)):
        x_s = sign * 430.0
        # Curved dark titanium arm rising smoothly from internal deck pivot to
        # grip the underside/leading pocket of the wing (clean flush top in cruise!)
        pts_yz = [
            (WING_PIVOT_Y - 10.0, WING_PIVOT_Z - 12.0),
            (WING_PIVOT_Y + 285.0, WING_PIVOT_Z + 48.0),
            (2015.0, 868.0),
            (2060.0, 868.0),
            (1965.0, 845.0),
            (WING_PIVOT_Y + 265.0, WING_PIVOT_Z + 20.0),
            (WING_PIVOT_Y - 10.0, WING_PIVOT_Z + 12.0),
        ]
        face = bd.Face(bd.Wire.make_polygon([bd.Vector(x_s - 10.0, y, z) for y, z in pts_yz]))
        arm = bd.extrude(face, 20.0, dir=(1, 0, 0))

        # Under-wing mounting saddle gripping the bronze-titanium suction underside
        clevis = bd.Pos(x_s, 2036.0, 860.0) * bd.Box(32.0, 68.0, 16.0)
        strut = (arm + clevis) - [wing_top, wing_bot]
        strut.label = f"wing_strut_{side_lbl}"
        apply_dark_titanium(strut)
        struts.append(strut)
    return struts


@memo
def _build_active_wing():
    wing_top, wing_bot = _wing_main_planes()
    endplates = _wing_endplates(wing_top, wing_bot)
    struts = _swan_neck_struts(wing_top, wing_bot)
    return bd.Compound(
        children=[wing_top, wing_bot, *endplates, *struts],
        label="active_wing",
    )


@model
def active_wing():
    """Active rear aero wing (stowed cruise position; pivots +18 deg to Track pose)."""
    return _build_active_wing()


if __name__ == "__main__":
    active_wing()
