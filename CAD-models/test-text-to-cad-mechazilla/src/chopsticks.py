"""Articulated Mechazilla 'Chopsticks' (Catch & Lift Arms) and Sliding Booster Catch Trolleys."""

import build123d as bd
from cad import model

import spec as S


def _arm_top_z(x_rel):
    """Sloped top chord height (relative to arm base Z) along arm length x_rel in [0, ARM_LEN]."""
    if x_rel <= 24.0:
        return S.ARM_ROOT_H
    t = max(0.0, min(1.0, (x_rel - 24.0) / (S.ARM_LEN - 24.0)))
    return S.ARM_ROOT_H * (1.0 - t) + S.ARM_TIP_H * t


def _build_port_arm_parts():
    """Build Port (+Y) chopstick arm boom, damped catch rail, and nose bumper in world as-built coords."""
    hx = S.HINGE_X
    hy = S.HINGE_Y
    z0 = S.CARRIAGE_Z_BUILT + S.ARM_ROOT_Z0_LOCAL  # 576.8 mm
    w = S.ARM_BOOM_W                                # 12.0 mm

    # 1. Twin cylindrical root hinge knuckles (fit cleanly in the carriage's two clevis slots!)
    knuckle_bot_h = S.CLEVIS_Z_LUGS[1][0] - S.CLEVIS_Z_LUGS[0][1] - 2.0 * S.KNUCKLE_CLEAR_Z  # 18.4
    knuckle_top_z = S.CARRIAGE_Z_BUILT + S.CLEVIS_Z_LUGS[1][1] + S.KNUCKLE_CLEAR_Z          # 606.8
    knuckle_top_h = S.CLEVIS_Z_LUGS[2][0] - S.CLEVIS_Z_LUGS[1][1] - 2.0 * S.KNUCKLE_CLEAR_Z  # 18.4

    k_bot = bd.Pos(hx, hy, z0) * bd.Cylinder(
        S.ARM_KNUCKLE_R, knuckle_bot_h, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    k_top = bd.Pos(hx, hy, knuckle_top_z) * bd.Cylinder(
        S.ARM_KNUCKLE_R, knuckle_top_h, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )

    # 2. Angled gooseneck transition from hinge (x_rel=0, Y=74) to parallel boom (x_rel=82, Y=57)
    # Constructed as an exact lofted/extruded plan profile trimmed vertically by the sloped top silhouette!
    gx1 = S.ARM_GOOSENECK_X  # 82.0
    boom_yc = S.ARM_BOOM_CENTER_Y  # 57.0
    half_w = w / 2.0               # 6.0

    # Gooseneck plan polygon (world XY): starts ahead of knuckle center, smoothly joins straight boom at x_rel=82
    g_pts = [
        (hx + 4.0, hy + half_w),
        (hx + gx1 + 1.0, boom_yc + half_w),
        (hx + gx1 + 1.0, boom_yc - half_w),
        (hx + 4.0, hy - half_w),
    ]
    g_prism = bd.Pos(0, 0, z0) * bd.extrude(bd.Polygon(g_pts, align=None), S.ARM_ROOT_H, dir=(0, 0, 1))

    # Cut sloped top bevel + clean vertical clearance around the middle carriage clevis ear!
    # Side-view silhouette mask in XZ (extruded wide in Y) to give the entire gooseneck + boom a crisp slope
    sloped_pts = [
        (hx - 15.0, z0),
        (hx + S.ARM_LEN + 25.0, z0),
        (hx + S.ARM_LEN + 25.0, z0 + S.ARM_TIP_H - 1.5),
        (hx + S.ARM_LEN, z0 + S.ARM_TIP_H),
        (hx + 24.0, z0 + S.ARM_ROOT_H),
        (hx - 15.0, z0 + S.ARM_ROOT_H),
    ]
    slope_mask = bd.Pos(0, hy + 20.0, 0) * bd.Rot(90, 0, 0) * bd.extrude(
        bd.Polygon(sloped_pts, align=None), 90.0, dir=(0, 0, 1)
    )
    gooseneck = g_prism & slope_mask

    # Carve two bold lightening windows through the gooseneck side web
    g_cut = bd.Polygon(
        [
            (hx + 22.0, z0 + 6.0),
            (hx + 68.0, z0 + 6.0),
            (hx + 68.0, z0 + _arm_top_z(68.0) - 6.0),
            (hx + 22.0, z0 + _arm_top_z(22.0) - 6.0),
        ],
        align=None,
    )
    # Keep a crisp diagonal strut dividing the gooseneck window
    g_web_cut1 = bd.Polygon(
        [
            (hx + 22.0, z0 + 6.5),
            (hx + 63.0, z0 + 6.5),
            (hx + 22.0, z0 + _arm_top_z(22.0) - 9.0),
        ],
        align=None,
    )
    g_web_cut2 = bd.Polygon(
        [
            (hx + 27.0, z0 + _arm_top_z(27.0) - 6.5),
            (hx + 72.0, z0 + 9.0),
            (hx + 72.0, z0 + _arm_top_z(72.0) - 6.5),
        ],
        align=None,
    )
    for tri in (g_web_cut1, g_web_cut2):
        cutter = bd.Pos(0, hy + 20.0, 0) * bd.Rot(90, 0, 0) * bd.extrude(tri, 90.0, dir=(0, 0, 1))
        gooseneck = gooseneck - cutter

    # 3. Main Straight Tapered Open-Web Truss Boom (x_rel: 82 -> 332, centered at Y=57.0)
    bx0 = hx + gx1          # 201.5
    bx1 = hx + S.ARM_LEN - 13.0  # 451.5
    boom_xz = bd.Polygon(
        [
            (bx0, z0),
            (bx1, z0),
            (bx1, z0 + _arm_top_z(S.ARM_LEN - 13.0)),
            (bx0, z0 + _arm_top_z(gx1)),
        ],
        align=None,
    )
    # Carve 6 alternating Warren-truss triangular bays directly in 2D before extruding!
    n_bays = 6
    bay_len = (bx1 - bx0 - 10.0) / n_bays
    chord_t = 4.6
    strut_gap = 2.4
    face_2d = boom_xz
    for i in range(n_bays):
        x_a = bx0 + 5.0 + i * bay_len
        x_b = x_a + bay_len
        x_m = (x_a + x_b) / 2.0
        z_bot = z0 + chord_t
        z_top_a = z0 + _arm_top_z(x_a - hx) - chord_t
        z_top_b = z0 + _arm_top_z(x_b - hx) - chord_t
        z_top_m = z0 + _arm_top_z(x_m - hx) - chord_t

        # Lower upright triangle
        t_low = bd.Polygon(
            [
                (x_a + strut_gap, z_bot),
                (x_b - strut_gap, z_bot),
                (x_m, z_top_m - 1.2),
            ],
            align=None,
        )
        # Upper left & right inverted triangles
        t_ul = bd.Polygon(
            [
                (x_a + 1.0, z_top_a),
                (x_m - strut_gap, z_top_m),
                (x_a + 1.0, z_bot + 3.0),
            ],
            align=None,
        )
        t_ur = bd.Polygon(
            [
                (x_m + strut_gap, z_top_m),
                (x_b - 1.0, z_top_b),
                (x_b - 1.0, z_bot + 3.0),
            ],
            align=None,
        )
        face_2d = face_2d - t_low - t_ul - t_ur

    # Extrude the crisp Warren-truss boom across Y in [51.0, 63.0]
    # Note: Polygon in XY rotated +90 about X maps local +X -> +X, local +Y -> +Z, local +Z -> -Y!
    # So origin at Y = boom_yc + half_w (63.0) with dir=(0, 0, 1) extrudes in -Y to 51.0!
    main_boom = (
        bd.Pos(0, boom_yc + half_w, 0)
        * bd.Rot(90, 0, 0)
        * bd.extrude(face_2d, w, dir=(0, 0, 1))
    )

    # Top and bottom wide welded box-flange caps on outer/upper boom edges (clear of catch rail!)
    # Bottom flange cap: Y in [50.5, 64.5], Z in [z0, z0 + 2.4]
    bot_flange = bd.Pos(bx0, boom_yc + 0.5, z0) * bd.Box(
        bx1 - bx0,
        w + 2.0,  # 14.0 mm -> Y in [50.5, 64.5]
        2.4,
        align=(bd.Align.MIN, bd.Align.CENTER, bd.Align.MIN),
    )

    # 4. Outward-flared tapered catch tip / funnel nose (x_rel: 332 -> 348)
    tx0 = bx1
    tx1 = hx + S.ARM_LEN + 3.0  # 467.5
    tip_h0 = _arm_top_z(S.ARM_LEN - 13.0)
    tip_plan = bd.Polygon(
        [
            (tx0, boom_yc - half_w),
            (tx1, boom_yc + 2.5),
            (tx1, boom_yc + half_w + 3.0),
            (tx0, boom_yc + half_w),
        ],
        align=None,
    )
    tip_prism = bd.Pos(0, 0, z0) * bd.extrude(tip_plan, tip_h0, dir=(0, 0, 1))
    tip_solid = tip_prism & slope_mask

    # Combine structural boom solid & carve exact hinge pin bore + middle clevis clearance!
    boom_raw = k_bot + [k_top, gooseneck, main_boom, bot_flange, tip_solid]

    # Cut clean R=5.0 mm vertical hinge bore (around R=4.5 pin) + R=11.8 mm middle clevis slot!
    pin_bore = bd.Pos(hx, hy, z0 - 2.0) * bd.Cylinder(
        S.HINGE_BORE_R, S.ARM_ROOT_H + 4.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    mid_clevis_slot = bd.Pos(hx, hy, z0 + knuckle_bot_h) * bd.Cylinder(
        11.8,
        knuckle_top_z - (z0 + knuckle_bot_h),  # 11.6 mm exact clearance around Z_local [76..86] ear!
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    boom = boom_raw - [pin_bore, mid_clevis_slot]
    boom.label = "arm_boom_port"
    S.apply_material(boom, S.mat_tower_steel())

    # 5. High-contrast Damped Energy-Absorbing Catch Rail on inboard boom face
    # Bar sits cleanly at Y in [46.0, 49.5], Z_rel in [11.5, 17.0], supported by 7 damper stanchions to Y=51.0
    rx0 = hx + S.CATCH_RAIL_X0  # 205.5
    rx1 = hx + S.CATCH_RAIL_X1  # 445.5
    rail_len = rx1 - rx0
    rail_z0 = z0 + 11.5
    rail_h = 5.5

    rail_bar = bd.Pos(rx0, S.CATCH_RAIL_INNER_Y, rail_z0) * bd.Box(
        rail_len,
        S.CATCH_RAIL_W,  # 3.5 mm -> Y in [46.0, 49.5]
        rail_h,
        align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN),
    )
    # Seven shock-absorber stanchion blocks connecting rail back (49.5) flush to boom face (51.0)
    stanchions = []
    n_stanchions = 7
    for i in range(n_stanchions):
        sx = rx0 + 8.0 + i * ((rail_len - 16.0) / (n_stanchions - 1))
        stanchions.append(
            bd.Pos(sx, S.CATCH_RAIL_INNER_Y + S.CATCH_RAIL_W, rail_z0 + 1.0)
            * bd.Box(
                7.0,
                S.ARM_BOOM_INNER_Y - (S.CATCH_RAIL_INNER_Y + S.CATCH_RAIL_W),  # 1.5 mm exact span!
                rail_h - 2.0,
                align=(bd.Align.CENTER, bd.Align.MIN, bd.Align.MIN),
            )
        )
    catch_rail = rail_bar + stanchions
    catch_rail.label = "catch_rail_port"
    S.apply_material(catch_rail, S.mat_catch_rail())

    # 6. Amber/orange elastomeric nose guide bumper mounted cleanly on the flared inboard tip bevel
    bumper_pts = [
        (tx0 + 1.5, boom_yc - half_w - 1.6),
        (tx1 - 1.0, boom_yc + 0.9),
        (tx1 - 1.5, boom_yc + 2.2),
        (tx0 + 0.8, boom_yc - half_w - 0.1),
    ]
    nose_bumper = bd.Pos(0, 0, z0 + 4.0) * bd.extrude(
        bd.Polygon(bumper_pts, align=None), 11.0, dir=(0, 0, 1)
    )
    nose_bumper = nose_bumper - boom
    nose_bumper.label = "nose_bumper_port"
    S.apply_material(nose_bumper, S.mat_bumper_pad())

    return boom, catch_rail, nose_bumper


def _build_port_trolley():
    """Sliding booster-translation catch trolley riding smoothly along Port damped catch rail.

    Wraps the catch rail (Y: CATCH_RAIL_INNER_Y .. +3.5, Z_rel: 11.5..17.0) with 0.6 mm running
    gap and stops 0.3 mm short of the damper stanchions. Inner trolley wall sits at Y = +46.1 mm
    (92.2 mm clear inner gap for 90.0 mm Starship/Super Heavy fuselage).
    """
    tx = S.HINGE_X + S.TROLLEY_X_BUILT  # 119.5 + 180.5 = 300.0 mm (exact Rocket CL!)
    z0 = S.CARRIAGE_Z_BUILT + S.ARM_ROOT_Z0_LOCAL  # 576.8
    t_len = S.TROLLEY_LEN               # 36.0 mm
    rail_y0 = S.CATCH_RAIL_INNER_Y      # 49.5
    gap = 0.6
    y_inner = rail_y0 - gap - 2.8       # 46.1 mm (92.2 mm total clear span!)
    y_outer = rail_y0 + S.CATCH_RAIL_W - 0.3  # 52.7 mm (0.3 mm clear of stanchions at 53.0!)
    saddle_w = y_outer - y_inner        # 6.6 mm

    # C-channel trolley carriage body (inboard wall + top lifting saddle + bottom guide shoe)
    side_wall = bd.Pos(tx, y_inner, z0 + 8.2) * bd.Box(
        t_len,
        2.8,
        12.8,
        align=(bd.Align.CENTER, bd.Align.MIN, bd.Align.MIN),
    )
    # Top lifting saddle overhanging rail top (Z_rel: 17.6..21.0)
    top_saddle = bd.Pos(tx, y_inner, z0 + 17.6) * bd.Box(
        t_len,
        saddle_w,
        3.4,
        align=(bd.Align.CENTER, bd.Align.MIN, bd.Align.MIN),
    )
    # Bottom anti-uplift guide shoe under rail (Z_rel: 8.2..10.9)
    bot_shoe = bd.Pos(tx, y_inner, z0 + 8.2) * bd.Box(
        t_len,
        saddle_w,
        2.7,
        align=(bd.Align.CENTER, bd.Align.MIN, bd.Align.MIN),
    )
    # Stabilizer end gussets on inboard face (projecting only 0.9 mm -> inner face Y=45.2, 90.4 mm clear!)
    ribs = []
    for sx in (-12.0, 0.0, 12.0):
        ribs.append(
            bd.Pos(tx + sx, y_inner - 0.9, z0 + 9.0)
            * bd.Box(2.4, 0.9, 11.2, align=(bd.Align.CENTER, bd.Align.MIN, bd.Align.MIN))
        )
    body = side_wall + [top_saddle, bot_shoe, *ribs]
    body.label = "trolley_body_port"
    S.apply_material(body, S.mat_trolley_body())

    # High-visibility orange elastomeric booster catch-pin shock pad on top of lifting saddle
    pad = bd.Pos(tx, y_inner + 0.4, z0 + 21.0) * bd.Box(
        t_len - 5.0,
        saddle_w - 0.8,
        2.2,
        align=(bd.Align.CENTER, bd.Align.MIN, bd.Align.MIN),
    )
    pad.label = "catch_pad_port"
    S.apply_material(pad, S.mat_bumper_pad())

    return bd.Compound(children=[body, pad], label="catch_trolley_port")


@model
def chopstick_port():
    """Port (+Y) Mechazilla Catch & Lift Arm ('Chopstick') with damped catch rail and bumper."""
    boom, rail, bumper = _build_port_arm_parts()
    return bd.Compound(children=[boom, rail, bumper], label="chopstick_port")


@model
def chopstick_stbd():
    """Starboard (-Y) Mechazilla Catch & Lift Arm (mirror-symmetric across XZ plane)."""
    boom_p, rail_p, bumper_p = _build_port_arm_parts()
    boom = bd.mirror(boom_p, about=bd.Plane.XZ)
    rail = bd.mirror(rail_p, about=bd.Plane.XZ)
    bumper = bd.mirror(bumper_p, about=bd.Plane.XZ)
    boom.label = "arm_boom_stbd"
    rail.label = "catch_rail_stbd"
    bumper.label = "nose_bumper_stbd"
    S.apply_material(boom, S.mat_tower_steel())
    S.apply_material(rail, S.mat_catch_rail())
    S.apply_material(bumper, S.mat_bumper_pad())
    return bd.Compound(children=[boom, rail, bumper], label="chopstick_stbd")


@model
def catch_trolley_port():
    """Port (+Y) sliding booster catch & alignment trolley."""
    return _build_port_trolley()


@model
def catch_trolley_stbd():
    """Starboard (-Y) sliding booster catch & alignment trolley."""
    t_port = _build_port_trolley()
    parts = []
    for child in t_port.children:
        m = bd.mirror(child, about=bd.Plane.XZ)
        if "pad" in child.label:
            m.label = "catch_pad_stbd"
            S.apply_material(m, S.mat_bumper_pad())
        else:
            m.label = "trolley_body_stbd"
            S.apply_material(m, S.mat_trolley_body())
        parts.append(m)
    return bd.Compound(children=parts, label="catch_trolley_stbd")


if __name__ == "__main__":
    chopstick_port()
    chopstick_stbd()
    catch_trolley_port()
    catch_trolley_stbd()
