"""Tesla Cybertruck panoramic glazing, flush gloss-black B/C pillars, CHMSL, and minimalist cabin interior.

Every glass panel sits flush along the master surface cage with crisp clearances from the stainless
cant rails and beltline, while all interior components maintain >= 40 mm air gap from every window
surface to prevent rendering mottling and eliminate interference.
"""

from __future__ import annotations

import build123d as bd
from cad import model

from lib import geometry, materials, spec

T_GLASS = spec.GLASS_THICK  # 8.0 mm


def _side_window_quad(s0: float, s1: float, inset_x: float = 3.0) -> bd.Solid:
    """Build a crisp flush side glass/pillar slab along the upper tumblehome plane on +X."""
    y0, y1 = spec.s_to_y(s0), spec.s_to_y(s1)
    zb0, zb1 = spec.z_belt(s0) + 3.0, spec.z_belt(s1) + 3.0
    # Top edge tucks right under the 14 mm cant rail underside (15 mm below outer edge -> zero slit, zero clash!)
    zr0, zr1 = spec.z_roof_side(s0) - 15.0, spec.z_roof_side(s1) - 15.0

    x0_lo = spec.x_body_upper(s0, zb0) - inset_x
    x1_lo = spec.x_body_upper(s1, zb1) - inset_x
    x0_hi = spec.x_body_upper(s0, zr0) - inset_x
    x1_hi = spec.x_body_upper(s1, zr1) - inset_x

    p0 = (x0_lo, y0, zb0)
    p1 = (x1_lo, y1, zb1)
    p2 = (x1_hi, y1, zr1)
    p3 = (x0_hi, y0, zr0)
    return geometry.quad_slab(p0, p1, p2, p3, thickness=T_GLASS, inward_normal_hint=(-0.92, 0.0, -0.39))


def _build_windshield() -> bd.Solid:
    """Massive ~18 deg raked panoramic windshield with subtle production cowl bow."""
    # 5 evenly spaced X stations sitting cleanly 4 mm inside cant rail inner edge (clears angled bevel!)
    s_top = spec.S_ROOF_APEX - 17.0  # 2453 mm (2 mm ahead of apex header bar)
    w_bot = spec.x_roof(spec.S_COWL_CORNER) - spec.CANT_RAIL_W - 4.5
    w_top = spec.x_roof(s_top) - spec.CANT_RAIL_W - 4.5

    u_vals = [-1.0, -0.5, 0.0, 0.5, 1.0]
    sections = []
    for u in u_vals:
        x_b = u * w_bot
        x_t = u * w_top
        s_b = spec.S_COWL_CENTER + spec.cowl_bow_ds(x_b) + 18.0
        z_b = spec.Z_COWL - 14.0 * (abs(u) ** 1.6)
        z_t = spec.z_roof(s_top) - 2.0
        # Keep each tilted slice strictly vertical-planar (offset along -Z by T_GLASS)
        sections.append([
            (x_b, spec.s_to_y(s_b), z_b),
            (x_t, spec.s_to_y(s_top), z_t),
            (x_t, spec.s_to_y(s_top), z_t - T_GLASS),
            (x_b, spec.s_to_y(s_b), z_b - T_GLASS),
        ])
    faces = [bd.Face(bd.Wire.make_polygon(pts)) for pts in sections]
    ws = bd.loft(faces, ruled=False)
    return materials.apply_mat(ws, materials.automotive_glass, "windshield")


def _build_roof_glass_and_headers() -> list[bd.Solid]:
    """Panoramic dark glass roof, roof apex cross-bar, rear cab header, CHMSL brake light, and rear cab window."""
    # 1. Roof apex flush gloss-black header cross-bar (s in [S_ROOF_APEX - 15, S_ROOF_APEX + 25])
    s_a0 = spec.S_ROOF_APEX - 15.0
    s_a1 = spec.S_ROOF_APEX + 25.0
    w_a = spec.x_roof(spec.S_ROOF_APEX) - spec.CANT_RAIL_W - 4.0  # 673 mm
    apex_sec_l = [
        (w_a, spec.s_to_y(s_a0), spec.z_roof(s_a0) - 1.0),
        (w_a, spec.s_to_y(spec.S_ROOF_APEX), spec.Z_ROOF_APEX - 1.0),
        (w_a, spec.s_to_y(s_a1), spec.z_roof(s_a1) - 1.0),
        (w_a, spec.s_to_y(s_a1), spec.z_roof(s_a1) - 16.0),
        (w_a, spec.s_to_y(spec.S_ROOF_APEX), spec.Z_ROOF_APEX - 16.0),
        (w_a, spec.s_to_y(s_a0), spec.z_roof(s_a0) - 16.0),
    ]
    apex_bar = bd.extrude(bd.Face(bd.Wire.make_polygon(apex_sec_l)), amount=w_a * 2.0, dir=(-1, 0, 0))

    # 2. Rear cab roof header cross-bar (s in [S_CAB_REAR - 52, S_CAB_REAR - 4])
    s_r0 = spec.S_CAB_REAR - 52.0
    s_r1 = spec.S_CAB_REAR - 4.0
    w_r = spec.x_roof(spec.S_CAB_REAR) - spec.CANT_RAIL_W - 4.0  # 683 mm
    rear_sec_l = [
        (w_r, spec.s_to_y(s_r0), spec.z_roof(s_r0) - 1.0),
        (w_r, spec.s_to_y(s_r1), spec.z_roof(s_r1) - 1.0),
        (w_r, spec.s_to_y(s_r1), spec.z_roof(s_r1) - 24.0),
        (w_r, spec.s_to_y(s_r0), spec.z_roof(s_r0) - 24.0),
    ]
    rear_bar = bd.extrude(bd.Face(bd.Wire.make_polygon(rear_sec_l)), amount=w_r * 2.0, dir=(-1, 0, 0))
    headers = apex_bar + rear_bar
    materials.apply_mat(headers, materials.gloss_black_pillar, "roof_header_bars")

    # 3. High-Mount Red LED Center Brake Light (CHMSL) inset along rear face of rear cab header
    chmsl = bd.Pos(0.0, spec.s_to_y(s_r1) + 2.0, spec.z_roof(s_r1) - 12.0) * bd.Box(
        460.0, 6.0, 12.0, align=(bd.Align.CENTER, bd.Align.MIN, bd.Align.CENTER)
    )
    materials.apply_mat(chmsl, materials.taillight_red_led, "chmsl_brake_light")

    # 4. Panoramic dark roof glass between apex bar (s_a1 + 2) and rear cab header (s_r0 - 2)
    s_g0 = s_a1 + 2.0
    s_g1 = s_r0 - 2.0
    w_g0 = spec.x_roof(s_g0) - spec.CANT_RAIL_W - 4.5
    w_g1 = spec.x_roof(s_g1) - spec.CANT_RAIL_W - 4.5
    p0 = (w_g0, spec.s_to_y(s_g0), spec.z_roof(s_g0) - 2.0)
    p1 = (w_g1, spec.s_to_y(s_g1), spec.z_roof(s_g1) - 2.0)
    p2 = (-w_g1, spec.s_to_y(s_g1), spec.z_roof(s_g1) - 2.0)
    p3 = (-w_g0, spec.s_to_y(s_g0), spec.z_roof(s_g0) - 2.0)
    roof_pane = geometry.quad_slab(p0, p1, p2, p3, thickness=T_GLASS, inward_normal_hint=(0.0, 0.0, -1.0))
    materials.apply_mat(roof_pane, materials.roof_glass, "panoramic_roof_glass")

    # 5. Rear cab vertical-ish tinted backlight glass (s = S_CAB_REAR - 45)
    z_bl_bot = spec.z_belt(spec.S_CAB_REAR) - 4.0
    z_bl_top = spec.z_roof(s_r0) - 28.0
    back_glass = bd.Pos(0.0, spec.s_to_y(s_r0) + 12.0, (z_bl_bot + z_bl_top) / 2.0) * bd.Box(
        1330.0, T_GLASS, z_bl_top - z_bl_bot
    )
    materials.apply_mat(back_glass, materials.roof_glass, "rear_cab_window")

    return [headers, chmsl, roof_pane, back_glass]


def _build_side_glasshouse() -> list[bd.Solid]:
    """Flush dark side windows (quarter, front door, rear door) + gloss-black B & C pillars."""
    parts = []

    # 1. Front triangular fixed quarter glass (s = 1074 .. 1480 at beltline, rising to cowl corner)
    s_q_top_f = spec.S_COWL_CORNER + 20.0   # 930 mm (clears fender shoulder & cant rail)
    s_q_bot_f = spec.S_QUARTER_GLASS_FWD + 8.0  # 1078 mm
    s_q_r = spec.S_FRONT_DOOR_SEAM - 4.0    # 1481 mm

    zb_f = spec.z_belt(s_q_bot_f) + 4.0
    zb_r = spec.z_belt(s_q_r) + 4.0
    zr_f = spec.z_roof_side(s_q_top_f) - 18.0
    zr_r = spec.z_roof_side(s_q_r) - 18.0

    q_l = geometry.quad_slab(
        (spec.x_body_upper(s_q_bot_f, zb_f) - 3.0, spec.s_to_y(s_q_bot_f), zb_f),
        (spec.x_body_upper(s_q_r, zb_r) - 3.0, spec.s_to_y(s_q_r), zb_r),
        (spec.x_body_upper(s_q_r, zr_r) - 3.0, spec.s_to_y(s_q_r), zr_r),
        (spec.x_body_upper(s_q_top_f, zr_f) - 3.0, spec.s_to_y(s_q_top_f), zr_f),
        thickness=T_GLASS,
        inward_normal_hint=(-0.92, 0.0, -0.39),
    )
    q_r = bd.mirror(q_l, about=bd.Plane.YZ)
    parts.append(materials.apply_mat(q_l, materials.automotive_glass, "quarter_glass_l"))
    parts.append(materials.apply_mat(q_r, materials.automotive_glass, "quarter_glass_r"))

    # 2. Front door frameless glass (split at S_ROOF_APEX so upper edge tracks the crisp roof peak!)
    fg_a = _side_window_quad(spec.S_FRONT_DOOR_SEAM + 4.0, spec.S_ROOF_APEX, inset_x=3.0)
    fg_b = _side_window_quad(spec.S_ROOF_APEX, spec.S_B_PILLAR - 52.0, inset_x=3.0)
    fg_l = fg_a + fg_b
    fg_r = bd.mirror(fg_l, about=bd.Plane.YZ)
    parts.append(materials.apply_mat(fg_l, materials.automotive_glass, "front_door_glass_l"))
    parts.append(materials.apply_mat(fg_r, materials.automotive_glass, "front_door_glass_r"))

    # 3. Flush gloss-black B-pillar applique (s in [S_B_PILLAR - 48, S_B_PILLAR + 48])
    bp_l = _side_window_quad(spec.S_B_PILLAR - 48.0, spec.S_B_PILLAR + 48.0, inset_x=2.0)
    bp_r = bd.mirror(bp_l, about=bd.Plane.YZ)
    parts.append(materials.apply_mat(bp_l, materials.gloss_black_pillar, "b_pillar_l"))
    parts.append(materials.apply_mat(bp_r, materials.gloss_black_pillar, "b_pillar_r"))

    # 4. Rear door frameless glass (s in [S_B_PILLAR + 52, S_REAR_DOOR_SEAM - 3])
    rg_l = _side_window_quad(spec.S_B_PILLAR + 52.0, spec.S_REAR_DOOR_SEAM - 3.0, inset_x=3.0)
    rg_r = bd.mirror(rg_l, about=bd.Plane.YZ)
    parts.append(materials.apply_mat(rg_l, materials.automotive_glass, "rear_door_glass_l"))
    parts.append(materials.apply_mat(rg_r, materials.automotive_glass, "rear_door_glass_r"))

    # 5. Flush gloss-black C-pillar applique bridging rear door window to stainless sail pillar
    cp_l = _side_window_quad(spec.S_REAR_DOOR_SEAM + 1.0, spec.S_CAB_REAR - 2.0, inset_x=2.0)
    cp_r = bd.mirror(cp_l, about=bd.Plane.YZ)
    parts.append(materials.apply_mat(cp_l, materials.gloss_black_pillar, "c_pillar_l"))
    parts.append(materials.apply_mat(cp_r, materials.gloss_black_pillar, "c_pillar_r"))

    return parts


def _build_interior() -> list[bd.Solid]:
    """Minimalist Cybertruck cabin interior: angular dash, white accent bar, 18.5" screen, squircle wheel, seats."""
    # All coordinates stay strictly inside cabin tub (s in [1200, 3660], |X| <= 760, Z >= 400)
    # and >= 60 mm clear of all glass surfaces.

    # 1. Angular minimalist dashboard + white tactical accent strip + center console
    y_d0 = spec.s_to_y(1240.0)
    y_d1 = spec.s_to_y(1770.0)
    dash_yz = [
        (y_d0, 820.0),
        (y_d0, 1045.0),
        (y_d1, 1020.0),
        (y_d1, 880.0),
        (y_d0 + 260.0, 820.0),
    ]
    dash_body = geometry.extrude_yz_polygon(dash_yz, -750.0, 750.0)

    # Center console storage bridge between front seats
    y_c0 = spec.s_to_y(1790.0)
    y_c1 = spec.s_to_y(2740.0)
    console = bd.Pos(0.0, (y_c0 + y_c1) / 2.0, 410.0) * bd.Box(
        310.0, y_c1 - y_c0, 390.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )

    # Front angular Cybertruck bucket seats (Left driver +X, Right passenger -X)
    seats = [dash_body, console]
    for sx in (-1.0, 1.0):
        xc = sx * 425.0
        # Seat cushion + sculpted angled backrest + angular headrest
        cushion = bd.Pos(xc, spec.s_to_y(2340.0), 560.0) * bd.Box(
            490.0, 500.0, 130.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
        )
        pedestal = bd.Pos(xc, spec.s_to_y(2360.0), 410.0) * bd.Box(
            360.0, 380.0, 150.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
        )
        backrest = (
            bd.Pos(xc, spec.s_to_y(2565.0), 660.0)
            * bd.Rot(18.0, 0.0, 0.0)
            * bd.Box(470.0, 115.0, 620.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        )
        headrest = (
            bd.Pos(xc, spec.s_to_y(2655.0), 1255.0)
            * bd.Rot(12.0, 0.0, 0.0)
            * bd.Box(260.0, 95.0, 185.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        )
        seats.extend([cushion, pedestal, backrest, headrest])

    # Rear angular bench seat + 3 headrests (s = 3050 .. 3560)
    rear_cush = bd.Pos(0.0, spec.s_to_y(3240.0), 560.0) * bd.Box(
        1380.0, 480.0, 140.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    rear_ped = bd.Pos(0.0, spec.s_to_y(3280.0), 410.0) * bd.Box(
        1280.0, 400.0, 150.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    rear_back = (
        bd.Pos(0.0, spec.s_to_y(3485.0), 680.0)
        * bd.Rot(16.0, 0.0, 0.0)
        * bd.Box(1360.0, 120.0, 560.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    )
    seats.extend([rear_cush, rear_ped, rear_back])
    for hx in (-440.0, 0.0, 440.0):
        r_head = (
            bd.Pos(hx, spec.s_to_y(3565.0), 1215.0)
            * bd.Rot(10.0, 0.0, 0.0)
            * bd.Box(240.0, 90.0, 165.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        )
        seats.append(r_head)

    # Signature Cybertruck squircle steering wheel & column on driver's side (+X = +425 mm)
    col = (
        bd.Pos(425.0, spec.s_to_y(1820.0), 1005.0)
        * bd.Rot(-68.0, 0.0, 0.0)
        * bd.Cylinder(38.0, 210.0)
    )
    # Squircle rim (outer chamfered rectangle minus inner opening)
    rim_outer = bd.Box(345.0, 235.0, 32.0)
    rim_inner = bd.Box(275.0, 165.0, 40.0)
    hub_spoke = bd.Box(310.0, 55.0, 30.0) + bd.Pos(0.0, -55.0, 0.0) * bd.Box(65.0, 95.0, 30.0)
    squircle = (
        bd.Pos(425.0, spec.s_to_y(1925.0), 1045.0)
        * bd.Rot(68.0, 0.0, 0.0)
        * ((rim_outer - rim_inner) + hub_spoke)
    )
    seats.extend([col, squircle])

    cabin = seats[0] + seats[1:]
    materials.apply_mat(cabin, materials.interior_charcoal, "cabin_interior")

    # Signature Cybertruck white tactical dash accent trim bar (cleanly 2 mm aft of dash_body y_d1)
    white_trim = bd.Pos(0.0, y_d1 + 12.0, 965.0) * bd.Box(1480.0, 18.0, 50.0)
    # Cut clearance pocket where steering column emerges on driver side (+X = 425)
    col_cut = bd.Pos(425.0, y_d1 + 12.0, 965.0) * bd.Box(110.0, 40.0, 90.0)
    white_trim = white_trim - col_cut
    materials.apply_mat(white_trim, materials.interior_white_accent, "dash_white_trim")

    # Iconic floating 18.5-inch central landscape infotainment touchscreen (s = 1845, cleanly aft of dash trim)
    screen = (
        bd.Pos(0.0, spec.s_to_y(1845.0), 1040.0)
        * bd.Rot(78.0, 0.0, 0.0)
        * bd.Box(440.0, 265.0, 16.0)
    )
    materials.apply_mat(screen, materials.touchscreen_glow, "infotainment_screen")

    return [cabin, white_trim, screen]


@model
def cybertruck_glazing():
    """Complete Cybertruck glazing, flush gloss-black B/C pillars, CHMSL, and minimalist cabin interior."""
    ws = _build_windshield()
    roof_items = _build_roof_glass_and_headers()
    side_items = _build_side_glasshouse()
    interior_items = _build_interior()

    return bd.Compound(
        children=[ws, *roof_items, *side_items, *interior_items],
        label="cybertruck_glazing",
    )


if __name__ == "__main__":
    cybertruck_glazing()
