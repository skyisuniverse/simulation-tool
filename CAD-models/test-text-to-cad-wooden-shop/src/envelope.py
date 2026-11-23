"""Building envelope: wall sheathing, shiplap cedar siding, interior lining, standing-seam roof, trim, gutters, signage."""

import build123d as bd
from cad import model

from lib import materials as mat
from lib import spec as S
from lib.geom import box_bounds, extrude_xz_polygon, extrude_yz_polygon


def _gable_wall_polygon_xz(x_half: float, z0: float) -> list[tuple[float, float]]:
    """Full gable wall outline in XZ from z0 up to the sloped rafter underside line."""
    return [
        (-x_half, z0),
        (x_half, z0),
        (x_half, S.rafter_bot_z(x_half)),
        (0.0, S.rafter_bot_z(0.0)),
        (-x_half, S.rafter_bot_z(x_half)),
    ]


def _shiplap_profile_yz(y_in: float, y_out: float, z0: float, z1: float, pitch: float = 160.0):
    """Build a horizontal bevelled shiplap/clapboard wall cross-section in YZ (facing -Y if y_out < y_in, else +Y)."""
    # Outward normal sign along Y: -1 for front wall, +1 for rear wall
    s = 1.0 if y_out > y_in else -1.0
    groove_d = 6.0
    groove_h = 10.0
    pts = [(y_in, z0), (y_out, z0)]
    z = z0 + pitch
    while z < z1 - groove_h:
        pts.append((y_out, z - groove_h))
        pts.append((y_out - s * groove_d, z - groove_h / 2.0))
        pts.append((y_out, z))
        z += pitch
    pts.append((y_out, z1))
    pts.append((y_in, z1))
    return pts


def _build_shiplap_front_or_rear(label: str, x_half: float, y0: float, y1: float, facing_sign: float, cutouts: list):
    """Build a shiplap cedar wall along X, trimmed cleanly to the gable roof line and cutouts."""
    y_in = y1 if facing_sign < 0 else y0
    y_out = y0 if facing_sign < 0 else y1
    z_max_bound = S.rafter_bot_z(0.0) + 10.0
    profile_yz = _shiplap_profile_yz(y_in, y_out, S.WALL_BASE_Z, z_max_bound)
    plank_slab = extrude_yz_polygon(profile_yz, -x_half, x_half)
    # Intersect with exact gable envelope prism so top edge follows rafter_bot_z(|x|) cleanly
    gable_mask = extrude_xz_polygon(_gable_wall_polygon_xz(x_half, S.WALL_BASE_Z), y0 - 1.0, y1 + 1.0)
    wall = plank_slab & gable_mask
    if cutouts:
        wall = wall - cutouts
    wall.label = label
    mat.apply_material(wall, mat.cedar_siding())
    return wall


def _build_shiplap_side(label: str, x0: float, x1: float, y0: float, y1: float, facing_sign: float, cutouts: list):
    """Build a shiplap cedar side wall along Y, trimmed cleanly to the sloped rafter underside."""
    x_in = x1 if facing_sign < 0 else x0
    x_out = x0 if facing_sign < 0 else x1
    s = 1.0 if x_out > x_in else -1.0
    groove_d = 6.0
    groove_h = 10.0
    z_top_bound = S.rafter_bot_z(min(abs(x0), abs(x1))) + 10.0

    # Shiplap cross-section in XZ, extruded along Y from y0 to y1
    pts = [(x_in, S.WALL_BASE_Z), (x_out, S.WALL_BASE_Z)]
    z = S.WALL_BASE_Z + 160.0
    while z < z_top_bound - groove_h:
        pts.append((x_out, z - groove_h))
        pts.append((x_out - s * groove_d, z - groove_h / 2.0))
        pts.append((x_out, z))
        z += 160.0
    pts.append((x_out, z_top_bound))
    pts.append((x_in, z_top_bound))

    plank_slab = extrude_xz_polygon(pts, y0, y1)
    # Trim top to exact sloped rafter underside plane
    slope_mask = extrude_xz_polygon(
        [
            (x0, S.WALL_BASE_Z),
            (x1, S.WALL_BASE_Z),
            (x1, S.rafter_bot_z(abs(x1))),
            (x0, S.rafter_bot_z(abs(x0))),
        ],
        y0 - 1.0,
        y1 + 1.0,
    )
    wall = plank_slab & slope_mask
    if cutouts:
        wall = wall - cutouts
    wall.label = label
    mat.apply_material(wall, mat.cedar_siding())
    return wall


def _build_wall_sheathing():
    """Build 15 mm OSB/plywood structural sheathing around all 4 exterior walls."""
    osb = mat.osb_sheathing()
    x_sh = S.SHOP_X_MAX + S.SHEATH_T  # 1815.0

    # Front sheathing (Y: -1715 .. -1700), notched for door, window, ridge beam, and side porch beams
    front_cuts = [
        box_bounds(S.DOOR_X_MIN, S.DOOR_X_MAX, S.SHOP_Y_MIN - S.SHEATH_T - 2, S.SHOP_Y_MIN + 2, S.DOOR_Z_MIN - 2, S.DOOR_Z_MAX),
        box_bounds(S.FRONT_WIN_X_MIN, S.FRONT_WIN_X_MAX, S.SHOP_Y_MIN - S.SHEATH_T - 2, S.SHOP_Y_MIN + 2, S.FRONT_WIN_Z_MIN, S.FRONT_WIN_Z_MAX),
        box_bounds(-S.RIDGE_HALF_W, S.RIDGE_HALF_W, S.SHOP_Y_MIN - S.SHEATH_T - 2, S.SHOP_Y_MIN + 2, S.RIDGE_BOT_Z, 4000.0),
        box_bounds(S.SHOP_X_MIN, S.SHOP_X_MIN + S.POST_SIZE, S.SHOP_Y_MIN - S.SHEATH_T - 2, S.SHOP_Y_MIN + 2, S.PORCH_BEAM_BOT_Z, S.WALL_TOP_Z + 5),
        box_bounds(S.SHOP_X_MAX - S.POST_SIZE, S.SHOP_X_MAX, S.SHOP_Y_MIN - S.SHEATH_T - 2, S.SHOP_Y_MIN + 2, S.PORCH_BEAM_BOT_Z, S.WALL_TOP_Z + 5),
    ]
    front = extrude_xz_polygon(_gable_wall_polygon_xz(x_sh, S.WALL_BASE_Z), S.SHOP_Y_MIN - S.SHEATH_T, S.SHOP_Y_MIN) - front_cuts
    front.label = "sheathing_front"
    mat.apply_material(front, osb)

    # Rear sheathing (Y: +2500 .. +2515), notched for transom window and ridge beam
    rear_cuts = [
        box_bounds(S.REAR_WIN_X_MIN, S.REAR_WIN_X_MAX, S.SHOP_Y_MAX - 2, S.SHOP_Y_MAX + S.SHEATH_T + 2, S.REAR_WIN_Z_MIN, S.REAR_WIN_Z_MAX),
        box_bounds(-S.RIDGE_HALF_W, S.RIDGE_HALF_W, S.SHOP_Y_MAX - 2, S.SHOP_Y_MAX + S.SHEATH_T + 2, S.RIDGE_BOT_Z, 4000.0),
    ]
    rear = extrude_xz_polygon(_gable_wall_polygon_xz(x_sh, S.WALL_BASE_Z), S.SHOP_Y_MAX, S.SHOP_Y_MAX + S.SHEATH_T) - rear_cuts
    rear.label = "sheathing_rear"
    mat.apply_material(rear, osb)

    # Left sheathing (X: -1815 .. -1800, Y: -1700 .. +2500)
    left_pts = [
        (-x_sh, S.WALL_BASE_Z),
        (S.SHOP_X_MIN, S.WALL_BASE_Z),
        (S.SHOP_X_MIN, S.rafter_bot_z(S.SHOP_X_MAX)),
        (-x_sh, S.rafter_bot_z(x_sh)),
    ]
    left_cut = box_bounds(-x_sh - 2, S.SHOP_X_MIN + 2, S.LEFT_WIN_Y_MIN, S.LEFT_WIN_Y_MAX, S.LEFT_WIN_Z_MIN, S.LEFT_WIN_Z_MAX)
    left = extrude_xz_polygon(left_pts, S.SHOP_Y_MIN, S.SHOP_Y_MAX) - left_cut
    left.label = "sheathing_left"
    mat.apply_material(left, osb)

    # Right sheathing (X: +1800 .. +1815, Y: -1700 .. +2500)
    right_pts = [
        (S.SHOP_X_MAX, S.WALL_BASE_Z),
        (x_sh, S.WALL_BASE_Z),
        (x_sh, S.rafter_bot_z(x_sh)),
        (S.SHOP_X_MAX, S.rafter_bot_z(S.SHOP_X_MAX)),
    ]
    right_cut = box_bounds(S.SHOP_X_MAX - 2, x_sh + 2, S.RIGHT_WIN_Y_MIN, S.RIGHT_WIN_Y_MAX, S.RIGHT_WIN_Z_MIN, S.RIGHT_WIN_Z_MAX)
    right = extrude_xz_polygon(right_pts, S.SHOP_Y_MIN, S.SHOP_Y_MAX) - right_cut
    right.label = "sheathing_right"
    mat.apply_material(right, osb)

    return bd.Compound(children=[front, rear, left, right], label="wall_sheathing")


def _build_exterior_cladding_and_trim():
    """Build horizontal shiplap cedar siding, corner boards, window/door casings, and storefront window ledge."""
    trim_mat = mat.walnut_trim()
    cedar = mat.cedar_siding()

    y_sh_f = S.SHOP_Y_MIN - S.SHEATH_T  # -1715.0
    y_sh_r = S.SHOP_Y_MAX + S.SHEATH_T  # +2515.0
    x_sh = S.SHOP_X_MAX + S.SHEATH_T    # +1815.0

    # 1. Shiplap cedar siding panels on all 4 walls
    front_cuts = [
        box_bounds(S.DOOR_X_MIN, S.DOOR_X_MAX, S.EXT_Y_MIN - 5, y_sh_f + 5, S.DOOR_Z_MIN - 2, S.DOOR_Z_MAX),
        box_bounds(S.FRONT_WIN_X_MIN, S.FRONT_WIN_X_MAX, S.EXT_Y_MIN - 5, y_sh_f + 5, S.FRONT_WIN_Z_MIN, S.FRONT_WIN_Z_MAX),
        box_bounds(-S.RIDGE_HALF_W, S.RIDGE_HALF_W, S.EXT_Y_MIN - 5, y_sh_f + 5, S.RIDGE_BOT_Z, 4000.0),
        box_bounds(S.SHOP_X_MIN, S.SHOP_X_MIN + S.POST_SIZE, S.EXT_Y_MIN - 5, y_sh_f + 5, S.PORCH_BEAM_BOT_Z, S.WALL_TOP_Z + 5),
        box_bounds(S.SHOP_X_MAX - S.POST_SIZE, S.SHOP_X_MAX, S.EXT_Y_MIN - 5, y_sh_f + 5, S.PORCH_BEAM_BOT_Z, S.WALL_TOP_Z + 5),
    ]
    siding_front = _build_shiplap_front_or_rear(
        "siding_front", S.EXT_X_MAX, S.EXT_Y_MIN, y_sh_f, -1.0, front_cuts
    )

    rear_cuts = [
        box_bounds(S.REAR_WIN_X_MIN, S.REAR_WIN_X_MAX, y_sh_r - 5, S.EXT_Y_MAX + 5, S.REAR_WIN_Z_MIN, S.REAR_WIN_Z_MAX),
        box_bounds(-S.RIDGE_HALF_W, S.RIDGE_HALF_W, y_sh_r - 5, S.EXT_Y_MAX + 5, S.RIDGE_BOT_Z, 4000.0),
    ]
    siding_rear = _build_shiplap_front_or_rear(
        "siding_rear", S.EXT_X_MAX, y_sh_r, S.EXT_Y_MAX, 1.0, rear_cuts
    )

    left_cuts = [
        box_bounds(S.EXT_X_MIN - 5, -x_sh + 5, S.LEFT_WIN_Y_MIN, S.LEFT_WIN_Y_MAX, S.LEFT_WIN_Z_MIN, S.LEFT_WIN_Z_MAX),
    ]
    siding_left = _build_shiplap_side(
        "siding_left", S.EXT_X_MIN, -x_sh, y_sh_f, y_sh_r, -1.0, left_cuts
    )

    right_cuts = [
        box_bounds(x_sh - 5, S.EXT_X_MAX + 5, S.RIGHT_WIN_Y_MIN, S.RIGHT_WIN_Y_MAX, S.RIGHT_WIN_Z_MIN, S.RIGHT_WIN_Z_MAX),
    ]
    siding_right = _build_shiplap_side(
        "siding_right", x_sh, S.EXT_X_MAX, y_sh_f, y_sh_r, 1.0, right_cuts
    )

    siding_group = bd.Compound(
        children=[siding_front, siding_rear, siding_left, siding_right],
        label="cedar_siding",
    )

    # 2. Vertical walnut corner trim boards wrapping all 4 outer corners cleanly (zero overlap)
    trim_parts = []
    ct_w = S.CORNER_TRIM_W
    ct_t = S.CORNER_TRIM_T
    z_eave_trim = S.rafter_bot_z(S.EXT_X_MAX + ct_t) - 1.0  # 2803.5 mm, safely clears rafters

    # Front-face corner strips (stop cleanly under side porch beams at Z = 2724)
    for lbl, x0, x1 in (
        ("corner_trim_fl_y", S.EXT_X_MIN, S.EXT_X_MIN + ct_w),
        ("corner_trim_fr_y", S.EXT_X_MAX - ct_w, S.EXT_X_MAX),
    ):
        b = box_bounds(x0, x1, S.EXT_Y_MIN - ct_t, S.EXT_Y_MIN, S.WALL_BASE_Z, S.PORCH_BEAM_BOT_Z)
        b.label = lbl
        mat.apply_material(b, trim_mat)
        trim_parts.append(b)

    # Rear-face corner strips (stop cleanly under sloped eave)
    for lbl, x0, x1 in (
        ("corner_trim_rl_y", S.EXT_X_MIN, S.EXT_X_MIN + ct_w),
        ("corner_trim_rr_y", S.EXT_X_MAX - ct_w, S.EXT_X_MAX),
    ):
        b = box_bounds(x0, x1, S.EXT_Y_MAX, S.EXT_Y_MAX + ct_t, S.WALL_BASE_Z, z_eave_trim)
        b.label = lbl
        mat.apply_material(b, trim_mat)
        trim_parts.append(b)

    # Side-face corner strips lapping cleanly over front/rear corner strip edges
    for lbl, x0, x1, y0, y1 in (
        ("corner_trim_fl_x", S.EXT_X_MIN - ct_t, S.EXT_X_MIN, S.EXT_Y_MIN - ct_t, S.EXT_Y_MIN + ct_w),
        ("corner_trim_fr_x", S.EXT_X_MAX, S.EXT_X_MAX + ct_t, S.EXT_Y_MIN - ct_t, S.EXT_Y_MIN + ct_w),
        ("corner_trim_rl_x", S.EXT_X_MIN - ct_t, S.EXT_X_MIN, S.EXT_Y_MAX - ct_w, S.EXT_Y_MAX + ct_t),
        ("corner_trim_rr_x", S.EXT_X_MAX, S.EXT_X_MAX + ct_t, S.EXT_Y_MAX - ct_w, S.EXT_Y_MAX + ct_t),
    ):
        b = box_bounds(x0, x1, y0, y1, S.WALL_BASE_Z, z_eave_trim)
        b.label = lbl
        mat.apply_material(b, trim_mat)
        trim_parts.append(b)

    # 3. Exterior door & window casings (85 mm wide, 22 mm proud of siding)
    def add_casing(prefix: str, axis: str, u0: float, u1: float, z0: float, z1: float, v_face: float, out_dir: float, has_sill: bool):
        w = 85.0
        t = 22.0
        v0, v1 = (v_face, v_face + t) if out_dir > 0 else (v_face - t, v_face)

        def mk(u_a, u_b, z_a, z_b, v_a=v0, v_b=v1):
            if axis == "X":
                return box_bounds(u_a, u_b, v_a, v_b, z_a, z_b)
            return box_bounds(v_a, v_b, u_a, u_b, z_a, z_b)

        left_j = mk(u0 - w, u0, z0, z1)
        right_j = mk(u1, u1 + w, z0, z1)
        head = mk(u0 - w - 12.0, u1 + w + 12.0, z1, z1 + 95.0)
        casing = left_j + right_j + head
        if has_sill:
            v_s0, v_s1 = (v_face, v_face + t + 24.0) if out_dir > 0 else (v_face - t - 24.0, v_face)
            sill = mk(u0 - w - 12.0, u1 + w + 12.0, z0 - 44.0, z0, v_s0, v_s1)
            casing = casing + sill
        casing.label = f"casing_{prefix}"
        mat.apply_material(casing, trim_mat)
        trim_parts.append(casing)

    # Front door casing (no bottom sill — stops cleanly at slab level Z = 304)
    add_casing("front_door", "X", S.DOOR_X_MIN, S.DOOR_X_MAX, S.WALL_BASE_Z, S.DOOR_Z_MAX, S.EXT_Y_MIN, -1.0, False)
    # Front showcase window casing (bottom is replaced by the proud exterior cedar display ledge)
    add_casing("front_window", "X", S.FRONT_WIN_X_MIN, S.FRONT_WIN_X_MAX, S.FRONT_WIN_Z_MIN, S.FRONT_WIN_Z_MAX, S.EXT_Y_MIN, -1.0, False)
    # Side & rear window casings
    add_casing("right_window", "Y", S.RIGHT_WIN_Y_MIN, S.RIGHT_WIN_Y_MAX, S.RIGHT_WIN_Z_MIN, S.RIGHT_WIN_Z_MAX, S.EXT_X_MAX, 1.0, True)
    add_casing("left_transom", "Y", S.LEFT_WIN_Y_MIN, S.LEFT_WIN_Y_MAX, S.LEFT_WIN_Z_MIN, S.LEFT_WIN_Z_MAX, S.EXT_X_MIN, -1.0, True)
    add_casing("rear_transom", "X", S.REAR_WIN_X_MIN, S.REAR_WIN_X_MAX, S.REAR_WIN_Z_MIN, S.REAR_WIN_Z_MAX, S.EXT_Y_MAX, 1.0, True)

    # 4. Exterior storefront display ledge under front showcase window + 3 cedar corbel brackets
    ledge_x0 = S.FRONT_WIN_X_MIN - 95.0
    ledge_x1 = S.FRONT_WIN_X_MAX + 95.0
    ledge_z0 = S.FRONT_WIN_Z_MIN - 38.0
    ledge_z1 = S.FRONT_WIN_Z_MIN
    ledge = box_bounds(ledge_x0, ledge_x1, S.EXT_Y_MIN - 200.0, S.EXT_Y_MIN, ledge_z0, ledge_z1)
    front_edge = ledge.edges().filter_by(
        lambda e: abs(e.bounding_box().min.Y - (S.EXT_Y_MIN - 200.0)) < 0.5
        and abs(e.bounding_box().max.Y - (S.EXT_Y_MIN - 200.0)) < 0.5
        and abs(e.bounding_box().min.Z - ledge_z1) < 0.5
    )
    if front_edge:
        ledge = ledge.chamfer(6.0, None, front_edge)
    ledge.label = "front_window_display_ledge"
    mat.apply_material(ledge, mat.heavy_timber())
    trim_parts.append(ledge)

    corbel_pts_yz = [
        (S.EXT_Y_MIN, ledge_z0),
        (S.EXT_Y_MIN - 165.0, ledge_z0),
        (S.EXT_Y_MIN - 165.0, ledge_z0 - 35.0),
        (S.EXT_Y_MIN - 25.0, ledge_z0 - 165.0),
        (S.EXT_Y_MIN, ledge_z0 - 165.0),
    ]
    for i, cx in enumerate((S.FRONT_WIN_X_MIN + 60.0, 0.5 * (S.FRONT_WIN_X_MIN + S.FRONT_WIN_X_MAX), S.FRONT_WIN_X_MAX - 60.0)):
        c = extrude_yz_polygon(corbel_pts_yz, cx - 22.0, cx + 22.0)
        c.label = f"window_ledge_corbel_{i}"
        mat.apply_material(c, cedar)
        trim_parts.append(c)

    return bd.Compound(
        children=[siding_group, bd.Compound(children=trim_parts, label="exterior_trim")],
        label="exterior_cladding",
    )


def _build_interior_lining():
    """Build 15 mm light birch interior wall paneling and oak baseboards."""
    birch = mat.birch_lining()
    oak = mat.oak_millwork()
    parts = []

    # Left & Right interior wall panels (Y: -1560 .. +2360, Z: 304 .. 2904)
    left_cut = box_bounds(S.INNER_X_MIN - 2, S.ROOM_X_MIN + 2, S.LEFT_WIN_Y_MIN, S.LEFT_WIN_Y_MAX, S.LEFT_WIN_Z_MIN, S.LEFT_WIN_Z_MAX)
    left = box_bounds(S.INNER_X_MIN, S.ROOM_X_MIN, S.INNER_Y_MIN, S.INNER_Y_MAX, S.WALL_BASE_Z, S.WALL_TOP_Z) - left_cut
    left.label = "interior_lining_left"
    mat.apply_material(left, birch)
    parts.append(left)

    right_cut = box_bounds(S.ROOM_X_MAX - 2, S.INNER_X_MAX + 2, S.RIGHT_WIN_Y_MIN, S.RIGHT_WIN_Y_MAX, S.RIGHT_WIN_Z_MIN, S.RIGHT_WIN_Z_MAX)
    right = box_bounds(S.ROOM_X_MAX, S.INNER_X_MAX, S.INNER_Y_MIN, S.INNER_Y_MAX, S.WALL_BASE_Z, S.WALL_TOP_Z) - right_cut
    right.label = "interior_lining_right"
    mat.apply_material(right, birch)
    parts.append(right)

    # Front & Rear interior wall panels rising into the vaulted gable ceiling (X: -1645 .. +1645)
    front_cuts = [
        box_bounds(S.DOOR_X_MIN, S.DOOR_X_MAX, S.INNER_Y_MIN - 2, S.ROOM_Y_MIN + 2, S.DOOR_Z_MIN - 2, S.DOOR_Z_MAX),
        box_bounds(S.FRONT_WIN_X_MIN, S.FRONT_WIN_X_MAX, S.INNER_Y_MIN - 2, S.ROOM_Y_MIN + 2, S.FRONT_WIN_Z_MIN, S.FRONT_WIN_Z_MAX),
        box_bounds(-S.RIDGE_HALF_W, S.RIDGE_HALF_W, S.INNER_Y_MIN - 2, S.ROOM_Y_MIN + 2, S.RIDGE_BOT_Z, 4000.0),
    ]
    front = extrude_xz_polygon(_gable_wall_polygon_xz(S.ROOM_X_MAX, S.WALL_BASE_Z), S.INNER_Y_MIN, S.ROOM_Y_MIN) - front_cuts
    front.label = "interior_lining_front"
    mat.apply_material(front, birch)
    parts.append(front)

    rear_cuts = [
        box_bounds(S.REAR_WIN_X_MIN, S.REAR_WIN_X_MAX, S.ROOM_Y_MAX - 2, S.INNER_Y_MAX + 2, S.REAR_WIN_Z_MIN, S.REAR_WIN_Z_MAX),
        box_bounds(-S.RIDGE_HALF_W, S.RIDGE_HALF_W, S.ROOM_Y_MAX - 2, S.INNER_Y_MAX + 2, S.RIDGE_BOT_Z, 4000.0),
    ]
    rear = extrude_xz_polygon(_gable_wall_polygon_xz(S.ROOM_X_MAX, S.WALL_BASE_Z), S.ROOM_Y_MAX, S.INNER_Y_MAX) - rear_cuts
    rear.label = "interior_lining_rear"
    mat.apply_material(rear, birch)
    parts.append(rear)

    # Interior oak baseboards (Z: 300 -> 385, 16 mm thick, interrupted cleanly at doorway)
    z0, z1 = S.SLAB_TOP_Z, S.SLAB_TOP_Z + S.BASEBOARD_H
    t = S.BASEBOARD_T
    bb_fl = box_bounds(S.ROOM_X_MIN + t, S.DOOR_X_MIN, S.ROOM_Y_MIN, S.ROOM_Y_MIN + t, z0, z1)
    bb_fr = box_bounds(S.DOOR_X_MAX, S.ROOM_X_MAX - t, S.ROOM_Y_MIN, S.ROOM_Y_MIN + t, z0, z1)
    bb_r = box_bounds(S.ROOM_X_MIN + t, S.ROOM_X_MAX - t, S.ROOM_Y_MAX - t, S.ROOM_Y_MAX, z0, z1)
    bb_l = box_bounds(S.ROOM_X_MIN, S.ROOM_X_MIN + t, S.ROOM_Y_MIN, S.ROOM_Y_MAX, z0, z1)
    bb_rt = box_bounds(S.ROOM_X_MAX - t, S.ROOM_X_MAX, S.ROOM_Y_MIN, S.ROOM_Y_MAX, z0, z1)
    for lbl, b in (
        ("baseboard_front_left", bb_fl),
        ("baseboard_front_right", bb_fr),
        ("baseboard_rear", bb_r),
        ("baseboard_left", bb_l),
        ("baseboard_right", bb_rt),
    ):
        b.label = lbl
        mat.apply_material(b, oak)
        parts.append(b)

    return bd.Compound(children=parts, label="interior_lining")


def _build_roof_assembly():
    """Build roof deck, fascia & rake trim, standing-seam metal roofing, ridge cap, gutters & downspouts."""
    osb = mat.osb_sheathing()
    trim_mat = mat.walnut_trim()
    roof_steel = mat.standing_seam_steel()

    def z_deck_top(abs_x: float) -> float:
        return S.rafter_top_z(abs_x) + S.ROOF_DECK_VERT_H

    def z_pan_top(abs_x: float) -> float:
        return z_deck_top(abs_x) + S.METAL_PAN_VERT_H

    def z_rib_top(abs_x: float) -> float:
        return z_pan_top(abs_x) + S.SEAM_RIB_VERT_H

    # 1. Plywood / timber roof decking (flush on rafter_top_z)
    dx = S.ROOF_DECK_X  # 2175.0
    deck_pts = [
        (-dx, S.rafter_top_z(dx)),
        (0.0, S.rafter_top_z(0.0)),
        (dx, S.rafter_top_z(dx)),
        (dx, z_deck_top(dx)),
        (0.0, z_deck_top(0.0)),
        (-dx, z_deck_top(dx)),
    ]
    roof_deck = extrude_xz_polygon(deck_pts, S.ROOF_DECK_Y_MIN, S.ROOF_DECK_Y_MAX)
    roof_deck.label = "roof_deck"
    mat.apply_material(roof_deck, osb)

    # 2. Timber eave fascia boards & gable rake trim boards
    fascia_parts = []
    fascia_bot = S.rafter_bot_z(S.EAVE_X) - 10.0  # 2649.0 (subtle 10 mm drip edge below rafter tail)
    for lbl, x0, x1 in (
        ("eave_fascia_left", -S.ROOF_DECK_X, -S.EAVE_X),
        ("eave_fascia_right", S.EAVE_X, S.ROOF_DECK_X),
    ):
        pts = [
            (x0, fascia_bot),
            (x1, fascia_bot),
            (x1, S.rafter_top_z(abs(x1))),
            (x0, S.rafter_top_z(abs(x0))),
        ]
        fb = extrude_xz_polygon(pts, S.ROOF_Y_MIN, S.ROOF_Y_MAX)
        fb.label = lbl
        mat.apply_material(fb, trim_mat)
        fascia_parts.append(fb)

    # Front & rear gable rake fascia boards (covering fly-rafters cleanly from ridge to eaves)
    rake_pts = [
        (-S.ROOF_DECK_X, S.rafter_bot_z(S.ROOF_DECK_X) - 8.0),
        (0.0, S.rafter_bot_z(0.0) - 8.0),
        (S.ROOF_DECK_X, S.rafter_bot_z(S.ROOF_DECK_X) - 8.0),
        (S.ROOF_DECK_X, S.rafter_top_z(S.ROOF_DECK_X)),
        (0.0, S.rafter_top_z(0.0)),
        (-S.ROOF_DECK_X, S.rafter_top_z(S.ROOF_DECK_X)),
    ]
    for lbl, y0, y1 in (
        ("gable_rake_front", S.ROOF_DECK_Y_MIN, S.ROOF_Y_MIN),
        ("gable_rake_rear", S.ROOF_Y_MAX, S.ROOF_DECK_Y_MAX),
    ):
        rk = extrude_xz_polygon(rake_pts, y0, y1)
        rk.label = lbl
        mat.apply_material(rk, trim_mat)
        fascia_parts.append(rk)

    fascia_group = bd.Compound(children=fascia_parts, label="roof_fascia")

    # 3. Anthracite standing-seam metal roof: flat pan + 13 raised ribs per slope + ridge cap
    mx = S.METAL_ROOF_X  # 2205.0
    pan_pts = [
        (-mx, z_deck_top(mx)),
        (0.0, z_deck_top(0.0)),
        (mx, z_deck_top(mx)),
        (mx, z_pan_top(mx)),
        (0.0, z_pan_top(0.0)),
        (-mx, z_pan_top(mx)),
    ]
    metal_pan = extrude_xz_polygon(pan_pts, S.METAL_ROOF_Y_MIN, S.METAL_ROOF_Y_MAX)
    metal_pan.label = "metal_roof_pan"
    mat.apply_material(metal_pan, roof_steel)

    # Ridge cap crowning cleanly over X in [-140, +140]
    rc_x = 140.0
    ridge_cap_pts = [
        (-rc_x, z_pan_top(rc_x)),
        (0.0, z_pan_top(0.0)),
        (rc_x, z_pan_top(rc_x)),
        (rc_x, z_rib_top(rc_x) + 6.0),
        (0.0, z_rib_top(0.0) + 6.0),
        (-rc_x, z_rib_top(rc_x) + 6.0),
    ]
    ridge_cap = extrude_xz_polygon(ridge_cap_pts, S.METAL_ROOF_Y_MIN - 5.0, S.METAL_ROOF_Y_MAX + 5.0)
    ridge_cap.label = "metal_ridge_cap"
    mat.apply_material(ridge_cap, roof_steel)

    # 13 raised standing-seam ribs per slope (starting flush at |x| = 140 out to drip edge |x| = 2205)
    rib_parts = []
    rib_ys = [-3040.0 + i * 480.0 for i in range(13)]
    for i, cy in enumerate(rib_ys):
        ry0, ry1 = cy - S.SEAM_RIB_W / 2, cy + S.SEAM_RIB_W / 2
        for side, s_lbl in ((-1.0, "left"), (1.0, "right")):
            x_a, x_b = (rc_x, mx) if side > 0 else (-mx, -rc_x)
            pts = [
                (x_a, z_pan_top(abs(x_a))),
                (x_b, z_pan_top(abs(x_b))),
                (x_b, z_rib_top(abs(x_b))),
                (x_a, z_rib_top(abs(x_a))),
            ]
            rib = extrude_xz_polygon(pts, ry0, ry1)
            rib.label = f"standing_seam_{s_lbl}_{i}"
            mat.apply_material(rib, roof_steel)
            rib_parts.append(rib)

    metal_roof_group = bd.Compound(
        children=[metal_pan, ridge_cap, bd.Compound(children=rib_parts, label="standing_seams")],
        label="metal_roof",
    )

    # 4. Eave rain gutters & rear corner downspouts (matching anthracite steel)
    gutter_parts = []
    gut_z0, gut_z1 = 2665.0, 2750.0
    gut_w = 100.0
    gut_t = 6.0
    for side, s_lbl in ((-1.0, "left"), (1.0, "right")):
        gx0 = side * S.ROOF_DECK_X if side > 0 else -(S.ROOF_DECK_X + gut_w)
        gx1 = (S.ROOF_DECK_X + gut_w) if side > 0 else -S.ROOF_DECK_X
        outer = box_bounds(gx0, gx1, S.ROOF_DECK_Y_MIN, S.ROOF_DECK_Y_MAX, gut_z0, gut_z1)
        cavity = box_bounds(
            gx0 + gut_t, gx1 - gut_t, S.ROOF_DECK_Y_MIN + gut_t, S.ROOF_DECK_Y_MAX - gut_t, gut_z0 + gut_t, gut_z1 + 2.0
        )
        gutter = outer - cavity
        gutter.label = f"rain_gutter_{s_lbl}"
        mat.apply_material(gutter, roof_steel)
        gutter_parts.append(gutter)

        # Rear corner downspout at Y = +2480 connecting gutter bottom down beside rear side corner trim
        dy = 2480.0
        r_pipe = 28.0
        x_gut = side * (S.ROOF_DECK_X + gut_w / 2.0)   # +-2225.0
        x_wall = side * (S.EXT_X_MAX + S.CORNER_TRIM_T + 36.0)  # +-1895.0 (8 mm clear of corner trim 1859)
        x_out = side * (S.SLAB_W / 2.0 - 25.0)         # +-1975.0 (discharging right at concrete edge)

        path_pts = [
            bd.Vector(x_gut, dy, gut_z0),
            bd.Vector(x_gut, dy, gut_z0 - 65.0),
            bd.Vector(x_wall, dy, gut_z0 - 295.0),
            bd.Vector(x_wall, dy, 395.0),
            bd.Vector(x_out, dy, 335.0),
        ]
        # Construct smooth tangent-filleted pipe centerline
        edges = [bd.Edge.make_line(path_pts[k], path_pts[k + 1]) for k in range(len(path_pts) - 1)]
        wire = bd.Wire(edges)
        profile = bd.Plane(origin=path_pts[0], z_dir=(0, 0, -1)) * bd.Circle(r_pipe)
        pipe = bd.sweep(profile, path=wire, transition=bd.Transition.ROUND)
        pipe.label = f"downspout_{s_lbl}"
        mat.apply_material(pipe, roof_steel)
        gutter_parts.append(pipe)

        # 3 clean pipe strap brackets anchoring downspout to the side corner trim (|x| = 1859)
        trim_face = side * (S.EXT_X_MAX + S.CORNER_TRIM_T)
        pipe_inner = x_wall - side * r_pipe
        sx0, sx1 = min(trim_face, pipe_inner), max(trim_face, pipe_inner)
        for j, bz in enumerate((650.0, 1450.0, 2200.0)):
            strap = box_bounds(sx0, sx1, dy - 14.0, dy + 14.0, bz - 12.0, bz + 12.0)
            strap.label = f"downspout_strap_{s_lbl}_{j}"
            mat.apply_material(strap, roof_steel)
            gutter_parts.append(strap)

    gutters_group = bd.Compound(children=gutter_parts, label="gutters_and_downspouts")

    return bd.Compound(
        children=[roof_deck, fascia_group, metal_roof_group, gutters_group],
        label="roof",
    )


def _build_storefront_accents():
    """Build the wooden fascia signboard ('WOODEN SHOP') and two architectural exterior wall sconces."""
    trim_mat = mat.walnut_trim()
    cream = mat.sign_cream()
    brass = mat.brushed_brass()
    black_steel = mat.matte_black_steel()
    lamp_glass = mat.warm_lamp_globe()

    # 1. Framed wooden storefront signboard mounted flush on front porch beam (Y = -2800)
    sx0, sx1 = -1150.0, 1150.0   # 2300 mm wide
    sz0, sz1 = 2714.0, 2934.0    # 220 mm tall
    sy_back = S.PORCH_Y_MIN      # -2800.0
    sy_face = sy_back - 28.0     # -2828.0

    # Backing board (warm cream painted wood)
    sign_board = box_bounds(sx0 + 28.0, sx1 - 28.0, sy_face, sy_back, sz0 + 28.0, sz1 - 28.0)
    sign_board.label = "signboard_panel"
    mat.apply_material(sign_board, cream)

    # Raised dark-walnut border frame wrapping all 4 edges cleanly (zero overlap with panel)
    fw = 28.0
    f_front = sy_face - 12.0
    f_top = box_bounds(sx0, sx1, f_front, sy_back, sz1 - fw, sz1)
    f_bot = box_bounds(sx0, sx1, f_front, sy_back, sz0, sz0 + fw)
    f_left = box_bounds(sx0, sx0 + fw, f_front, sy_back, sz0 + fw, sz1 - fw)
    f_right = box_bounds(sx1 - fw, sx1, f_front, sy_back, sz0 + fw, sz1 - fw)
    sign_frame = f_top + f_bot + f_left + f_right
    sign_frame.label = "signboard_frame"
    mat.apply_material(sign_frame, trim_mat)

    # Subtle brushed-brass decorative accent bars flanking the sign title
    accent_bars = []
    for lbl, ax0, ax1 in (("sign_bar_left", -1040.0, -760.0), ("sign_bar_right", 760.0, 1040.0)):
        bar = box_bounds(ax0, ax1, sy_face - 6.0, sy_face, 2819.0, 2829.0)
        bar.label = lbl
        mat.apply_material(bar, brass)
        accent_bars.append(bar)

    # Clean 3D brushed-brass storefront lettering mounted proud on signboard face (Y = sy_face -> sy_face - 8)
    sign_plane = bd.Plane(origin=(0.0, sy_face, 2824.0), x_dir=(1, 0, 0), z_dir=(0, -1, 0))
    text_faces = sign_plane * bd.Text("WOODEN SHOP", font_size=110.0, font_style=bd.FontStyle.BOLD)
    letters = bd.extrude(text_faces, amount=8.0)
    letters.label = "signboard_lettering"
    mat.apply_material(letters, brass)

    sign_group = bd.Compound(
        children=[sign_board, sign_frame, letters, *accent_bars],
        label="shop_signboard",
    )

    # 2. Two exterior architectural wall sconces on front facade (X = -1635 and X = -350, Y = -1737)
    sconces = []
    for lbl, cx in (("sconce_left", -1635.0), ("sconce_mid", -350.0)):
        cz = 2160.0
        y_wall = S.EXT_Y_MIN
        backplate = box_bounds(cx - 38.0, cx + 38.0, y_wall - 16.0, y_wall, cz - 75.0, cz + 75.0)
        arm = box_bounds(cx - 12.0, cx + 12.0, y_wall - 105.0, y_wall - 16.0, cz + 25.0, cz + 45.0)
        hood_outer = bd.Pos(cx, y_wall - 95.0, cz + 25.0) * bd.Cone(
            75.0, 22.0, 48.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MAX)
        )
        hood_inner = bd.Pos(cx, y_wall - 95.0, cz + 20.0) * bd.Cone(
            68.0, 16.0, 44.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MAX)
        )
        hood = hood_outer - hood_inner
        hood_cap = bd.Pos(cx, y_wall - 95.0, cz + 25.0) * bd.Cylinder(
            22.0, 20.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
        )
        body = backplate + arm + hood + hood_cap
        body.label = f"{lbl}_body"
        mat.apply_material(body, black_steel)

        # Warm glowing frosted lamp globe nestled cleanly inside the hollow shade
        globe = bd.Pos(cx, y_wall - 95.0, cz - 46.0) * bd.Sphere(36.0)
        globe.label = f"{lbl}_globe"
        mat.apply_material(globe, lamp_glass)

        sconces.append(bd.Compound(children=[body, globe], label=lbl))

    return bd.Compound(
        children=[sign_group, bd.Compound(children=sconces, label="exterior_sconces")],
        label="storefront_accents",
    )


@model
def envelope():
    """Complete wooden shop building envelope (sheathing, siding, lining, roof, gutters, signage)."""
    sheathing = _build_wall_sheathing()
    cladding = _build_exterior_cladding_and_trim()
    lining = _build_interior_lining()
    roof = _build_roof_assembly()
    accents = _build_storefront_accents()

    return bd.Compound(
        children=[sheathing, cladding, lining, roof, accents],
        label="envelope",
    )


if __name__ == "__main__":
    envelope()
