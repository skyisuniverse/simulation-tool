"""Structural timber framing: 2x6 stud walls, porch heavy timber, king-post truss, and roof rafters."""

import math

import build123d as bd
from cad import model

from lib import materials as mat
from lib import spec as S
from lib.geom import box_bounds, extrude_xz_polygon, extrude_yz_polygon


def _wall_box(axis: str, u0: float, u1: float, v0: float, v1: float, z0: float, z1: float):
    if axis == "X":
        return box_bounds(u0, u1, v0, v1, z0, z1)
    return box_bounds(v0, v1, u0, u1, z0, z1)


def _build_framed_wall(
    name: str,
    axis: str,
    u_min: float,
    u_max: float,
    v_min: float,
    v_max: float,
    upper_u_min: float,
    upper_u_max: float,
    openings: list[tuple[float, float, float, float, bool]],
    stud_pitch: float = 600.0,
):
    """Build a complete timber-framed wall with plates, studs, headers, sills, cripples, and sill anchors.

    openings: list of (u0, u1, z0, z1, is_door)
    """
    spruce = mat.framing_spruce()
    galv = mat.galvanized_steel()
    parts = []
    anchors = []

    z_b0, z_b1 = S.WALL_BASE_Z, S.STUD_BASE_Z              # 304 .. 349 (bottom plate)
    z_s0, z_s1 = S.STUD_BASE_Z, S.STUD_TOP_Z               # 349 .. 2814 (studs)
    z_t1_0, z_t1_1 = S.STUD_TOP_Z, S.STUD_TOP_Z + S.PLATE_H  # 2814 .. 2859 (lower top plate)
    z_t2_0, z_t2_1 = z_t1_1, S.WALL_TOP_Z                  # 2859 .. 2904 (upper top plate)

    # Bottom plate segments (interrupted across doorway rough openings)
    door_cuts = sorted((u0, u1) for u0, u1, _, _, is_door in openings if is_door)
    cursor = u_min
    b_idx = 0
    for du0, du1 in door_cuts:
        if du0 > cursor + 1.0:
            p = _wall_box(axis, cursor, du0, v_min, v_max, z_b0, z_b1)
            p.label = f"{name}_bottom_plate_{b_idx}"
            mat.apply_material(p, spruce)
            parts.append(p)
            b_idx += 1
        cursor = max(cursor, du1)
    if u_max > cursor + 1.0:
        p = _wall_box(axis, cursor, u_max, v_min, v_max, z_b0, z_b1)
        p.label = f"{name}_bottom_plate_{b_idx}"
        mat.apply_material(p, spruce)
        parts.append(p)

    # Double top plates (upper plate uses interlocking corner extents)
    ltp = _wall_box(axis, u_min, u_max, v_min, v_max, z_t1_0, z_t1_1)
    ltp.label = f"{name}_lower_top_plate"
    mat.apply_material(ltp, spruce)
    parts.append(ltp)

    utp = _wall_box(axis, upper_u_min, upper_u_max, v_min, v_max, z_t2_0, z_t2_1)
    utp.label = f"{name}_upper_top_plate"
    mat.apply_material(utp, spruce)
    parts.append(utp)

    # Track occupied u-intervals along the bottom plate (for clear anchor placement & no stud clashes)
    occupied: list[tuple[float, float]] = []

    def add_member(label: str, u0: float, u1: float, z0: float, z1: float, on_sill: bool = True):
        m = _wall_box(axis, u0, u1, v_min, v_max, z0, z1)
        m.label = label
        mat.apply_material(m, spruce)
        parts.append(m)
        if on_sill:
            occupied.append((u0, u1))

    # End corner studs
    add_member(f"{name}_end_stud_0", u_min, u_min + S.STUD_W, z_s0, z_s1)
    add_member(f"{name}_end_stud_1", u_max - S.STUD_W, u_max, z_s0, z_s1)

    # Framing around each door / window rough opening
    opening_excl: list[tuple[float, float]] = []
    for i, (ou0, ou1, oz0, oz1, is_door) in enumerate(openings):
        jack_l = (ou0 - S.STUD_W, ou0)
        jack_r = (ou1, ou1 + S.STUD_W)
        king_l = (ou0 - 2 * S.STUD_W, ou0 - S.STUD_W)
        king_r = (ou1 + S.STUD_W, ou1 + 2 * S.STUD_W)
        opening_excl.append((king_l[0], king_r[1]))

        # King studs (full height)
        add_member(f"{name}_op{i}_king_l", king_l[0], king_l[1], z_s0, z_s1)
        add_member(f"{name}_op{i}_king_r", king_r[0], king_r[1], z_s0, z_s1)

        # Jack / trimmer studs supporting header
        add_member(f"{name}_op{i}_jack_l", jack_l[0], jack_l[1], z_s0, oz1)
        add_member(f"{name}_op{i}_jack_r", jack_r[0], jack_r[1], z_s0, oz1)

        # Double lintel header spanning jack-to-jack
        hdr_top = oz1 + S.HEADER_H
        add_member(f"{name}_op{i}_header", jack_l[0], jack_r[1], oz1, hdr_top, on_sill=False)

        # Cripple studs above header
        c_u = math.ceil((ou0 + 180.0) / stud_pitch) * stud_pitch
        c_idx = 0
        while c_u <= ou1 - 180.0:
            add_member(
                f"{name}_op{i}_top_cripple_{c_idx}",
                c_u - S.STUD_W / 2,
                c_u + S.STUD_W / 2,
                hdr_top,
                z_s1,
                on_sill=False,
            )
            c_u += stud_pitch
            c_idx += 1

        if is_door:
            occupied.append((ou0, ou1))
        else:
            # Window rough sill beam and lower cripple studs
            sill_bot = oz0 - S.PLATE_H
            add_member(f"{name}_op{i}_sill", ou0, ou1, sill_bot, oz0, on_sill=False)
            c_u = math.ceil((ou0 + 180.0) / stud_pitch) * stud_pitch
            c_idx = 0
            while c_u <= ou1 - 180.0:
                add_member(
                    f"{name}_op{i}_bot_cripple_{c_idx}",
                    c_u - S.STUD_W / 2,
                    c_u + S.STUD_W / 2,
                    z_s0,
                    sill_bot,
                    on_sill=True,
                )
                c_u += stud_pitch
                c_idx += 1

    # Regular full-height wall studs on 600 mm module (where clear of corners & openings)
    u = math.ceil((u_min + S.STUD_W + 120.0) / stud_pitch) * stud_pitch
    s_idx = 0
    while u <= u_max - S.STUD_W - 120.0:
        su0, su1 = u - S.STUD_W / 2, u + S.STUD_W / 2
        clashes = any(not (su1 <= ex0 - 5.0 or su0 >= ex1 + 5.0) for ex0, ex1 in opening_excl)
        if not clashes:
            add_member(f"{name}_stud_{s_idx}", su0, su1, z_s0, z_s1)
            s_idx += 1
        u += stud_pitch

    # Sill-plate galvanized anchor bolt washers + hex nuts seated cleanly in open stud bays
    v_mid = (v_min + v_max) / 2.0
    anchor_idx = 0

    # Find widest open bays along bottom sill plate (clear of doors and studs)
    merged = []
    for o0, o1 in sorted(occupied):
        if merged and o0 <= merged[-1][1] + 1.0:
            merged[-1] = (merged[-1][0], max(merged[-1][1], o1))
        else:
            merged.append((o0, o1))

    open_bays = []
    prev = u_min
    for m0, m1 in merged:
        if m0 - prev >= 140.0:
            open_bays.append((prev, m0))
        prev = max(prev, m1)
    if u_max - prev >= 140.0:
        open_bays.append((prev, u_max))

    # Place up to 3 evenly distributed sill anchors per wall
    chosen_bays = open_bays if len(open_bays) <= 3 else [open_bays[0], open_bays[len(open_bays) // 2], open_bays[-1]]
    for b0, b1 in chosen_bays:
        au = 0.5 * (b0 + b1)
        # Ensure bay is not inside a door cutout
        if any(du0 <= au <= du1 for du0, du1 in door_cuts):
            continue
        ax, ay = (au, v_mid) if axis == "X" else (v_mid, au)
        washer = bd.Pos(ax, ay, z_s0) * bd.Box(
            42.0, 42.0, 4.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
        )
        nut = bd.Pos(ax, ay, z_s0 + 4.0) * bd.extrude(bd.RegularPolygon(11.0, 6), amount=10.0)
        stub = bd.Pos(ax, ay, z_s0 + 14.0) * bd.Cylinder(
            6.0, 6.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
        )
        anchor = washer + nut + stub
        anchor.label = f"{name}_sill_anchor_{anchor_idx}"
        mat.apply_material(anchor, galv)
        anchors.append(anchor)
        anchor_idx += 1

    children = parts
    if anchors:
        children = parts + [bd.Compound(children=anchors, label=f"{name}_anchors")]
    return bd.Compound(children=children, label=name)


def _build_gable_end_studs(name: str, y0: float, y1: float):
    """Build vertical gable triangle infill studs above the front or rear top plate."""
    spruce = mat.framing_spruce()
    studs = []
    xs = (-1350.0, -900.0, -450.0, 0.0, 450.0, 900.0, 1350.0)
    for idx, cx in enumerate(xs):
        x0 = cx - S.STUD_W / 2
        x1 = cx + S.STUD_W / 2
        if abs(cx) < 1.0:
            # Center stud terminates flat underneath the ridge beam
            s = box_bounds(x0, x1, y0, y1, S.WALL_TOP_Z, S.RIDGE_BOT_Z)
        else:
            z_left = min(S.rafter_bot_z(abs(x0)), S.RIDGE_BOT_Z)
            z_right = min(S.rafter_bot_z(abs(x1)), S.RIDGE_BOT_Z)
            pts = [
                (x0, S.WALL_TOP_Z),
                (x1, S.WALL_TOP_Z),
                (x1, z_right),
                (x0, z_left),
            ]
            s = extrude_xz_polygon(pts, y0, y1)
        s.label = f"{name}_stud_{idx}"
        mat.apply_material(s, spruce)
        studs.append(s)
    return bd.Compound(children=studs, label=name)


def _knee_brace_xz(u_post: float, direction: float, z_beam: float, y0: float, y1: float):
    """Build a 45-degree mitered knee brace in the XZ plane flush against post and beam."""
    c = S.KNEE_BRACE_SIZE * math.sqrt(2.0)
    span = S.KNEE_BRACE_SPAN
    pts = [
        (u_post, z_beam - span),
        (u_post, z_beam - span + c),
        (u_post + direction * (span - c), z_beam),
        (u_post + direction * span, z_beam),
    ]
    return extrude_xz_polygon(pts, y0, y1)


def _knee_brace_yz(y_post: float, direction: float, z_beam: float, x0: float, x1: float):
    """Build a 45-degree mitered knee brace in the YZ plane flush against post and side beam."""
    c = S.KNEE_BRACE_SIZE * math.sqrt(2.0)
    span = S.KNEE_BRACE_SPAN
    pts = [
        (y_post, z_beam - span),
        (y_post, z_beam - span + c),
        (y_post + direction * (span - c), z_beam),
        (y_post + direction * span, z_beam),
    ]
    return extrude_yz_polygon(pts, x0, x1)


def _build_porch_frame():
    """Build the 3 heavy timber porch columns, header beams, and 6 chamfered 45-deg knee braces."""
    timber = mat.heavy_timber()
    parts = []
    half_p = S.POST_SIZE / 2

    # 3 heavy 120 x 120 mm timber columns seated on galvanized steel post shoes (Z = 324 -> 2724)
    post_names = ("porch_post_left", "porch_post_mid", "porch_post_right")
    for cx, name in zip(S.PORCH_POST_XS, post_names):
        post = box_bounds(
            cx - half_p,
            cx + half_p,
            S.PORCH_Y_MIN,
            S.PORCH_Y_MAX,
            S.POST_BASE_Z,
            S.PORCH_BEAM_BOT_Z,
        )
        post.label = name
        mat.apply_material(post, timber)
        parts.append(post)

    # Front continuous porch header beam (Z = 2724 -> 2904, top flush with main wall top plates)
    front_beam = box_bounds(
        S.SHOP_X_MIN,
        S.SHOP_X_MAX,
        S.PORCH_Y_MIN,
        S.PORCH_Y_MAX,
        S.PORCH_BEAM_BOT_Z,
        S.WALL_TOP_Z,
    )
    front_beam.label = "porch_front_beam"
    mat.apply_material(front_beam, timber)
    parts.append(front_beam)

    # Left & right side porch beams tying front beam back to main shop framing
    left_beam = box_bounds(
        S.SHOP_X_MIN,
        S.SHOP_X_MIN + S.POST_SIZE,
        S.PORCH_Y_MAX,
        S.SHOP_Y_MIN,
        S.PORCH_BEAM_BOT_Z,
        S.WALL_TOP_Z,
    )
    left_beam.label = "porch_side_beam_left"
    mat.apply_material(left_beam, timber)
    parts.append(left_beam)

    right_beam = box_bounds(
        S.SHOP_X_MAX - S.POST_SIZE,
        S.SHOP_X_MAX,
        S.PORCH_Y_MAX,
        S.SHOP_Y_MIN,
        S.PORCH_BEAM_BOT_Z,
        S.WALL_TOP_Z,
    )
    right_beam.label = "porch_side_beam_right"
    mat.apply_material(right_beam, timber)
    parts.append(right_beam)

    # 6 mitered 45-deg knee braces (4 along front beam, 2 along side porch beams)
    by0 = S.PORCH_POST_Y - S.KNEE_BRACE_SIZE / 2
    by1 = S.PORCH_POST_Y + S.KNEE_BRACE_SIZE / 2
    front_braces = [
        ("knee_brace_front_ll", S.PORCH_POST_XS[0] + half_p, 1.0),
        ("knee_brace_front_ml", S.PORCH_POST_XS[1] - half_p, -1.0),
        ("knee_brace_front_mr", S.PORCH_POST_XS[1] + half_p, 1.0),
        ("knee_brace_front_rr", S.PORCH_POST_XS[2] - half_p, -1.0),
    ]
    for lbl, u_post, direction in front_braces:
        br = _knee_brace_xz(u_post, direction, S.PORCH_BEAM_BOT_Z, by0, by1)
        br.label = lbl
        mat.apply_material(br, timber)
        parts.append(br)

    for lbl, cx in (("knee_brace_side_left", S.PORCH_POST_XS[0]), ("knee_brace_side_right", S.PORCH_POST_XS[2])):
        bx0 = cx - S.KNEE_BRACE_SIZE / 2
        bx1 = cx + S.KNEE_BRACE_SIZE / 2
        br = _knee_brace_yz(S.PORCH_Y_MAX, 1.0, S.PORCH_BEAM_BOT_Z, bx0, bx1)
        br.label = lbl
        mat.apply_material(br, timber)
        parts.append(br)

    return bd.Compound(children=parts, label="porch_frame")


def _rafter_polygon_xz(side: float) -> list[tuple[float, float]]:
    """2D XZ polygon for one sloped rafter with authentic horizontal birdsmouth seat on WALL_TOP_Z.

    side = +1.0 for right (+X) rafter, -1.0 for left (-X) rafter.
    """
    pts_pos = [
        (S.RIDGE_HALF_W, S.rafter_bot_z(S.RIDGE_HALF_W)),   # ridge bottom
        (S.INNER_X_MAX, S.WALL_TOP_Z),                      # inner seat corner (1660, 2904)
        (S.SHOP_X_MAX, S.WALL_TOP_Z),                       # outer seat corner (1800, 2904)
        (S.SHOP_X_MAX, S.rafter_bot_z(S.SHOP_X_MAX)),       # vertical birdsmouth heel (1800, 2834)
        (S.EAVE_X, S.rafter_bot_z(S.EAVE_X)),               # eave bottom plumb cut (2150, 2659)
        (S.EAVE_X, S.rafter_top_z(S.EAVE_X)),               # eave top plumb cut (2150, 2815.5)
        (S.RIDGE_HALF_W, S.rafter_top_z(S.RIDGE_HALF_W)),   # ridge top (30, 3875.5)
    ]
    if side > 0:
        return pts_pos
    return [(-x, z) for x, z in reversed(pts_pos)]


def _build_roof_framing():
    """Build ridge beam, exposed front king-post porch truss, rafters, collar ties, and gable outlookers."""
    spruce = mat.framing_spruce()
    timber = mat.heavy_timber()
    parts = []

    # Continuous central ridge beam with beveled top matching 6:12 roof pitch
    ridge_pts = [
        (-S.RIDGE_HALF_W, S.RIDGE_BOT_Z),
        (S.RIDGE_HALF_W, S.RIDGE_BOT_Z),
        (S.RIDGE_HALF_W, S.rafter_top_z(S.RIDGE_HALF_W)),
        (0.0, S.RIDGE_PEAK_Z),
        (-S.RIDGE_HALF_W, S.rafter_top_z(S.RIDGE_HALF_W)),
    ]
    ridge = extrude_xz_polygon(ridge_pts, S.ROOF_Y_MIN, S.ROOF_Y_MAX)
    ridge.label = "ridge_beam"
    mat.apply_material(ridge, timber)
    parts.append(ridge)

    # Exposed front porch heavy king-post gable truss (Y: -2785 .. -2695, 90 mm thick)
    truss_y0, truss_y1 = S.PORCH_POST_Y - 45.0, S.PORCH_POST_Y + 45.0
    truss_parts = []
    for side, s_lbl in ((-1.0, "left"), (1.0, "right")):
        pr = extrude_xz_polygon(_rafter_polygon_xz(side), truss_y0, truss_y1)
        pr.label = f"porch_truss_rafter_{s_lbl}"
        mat.apply_material(pr, timber)
        truss_parts.append(pr)

    # Central king post (90 x 90 mm, beveled top shoulders to clear principal rafters cleanly)
    kp_half = 45.0
    kp_pts = [
        (-kp_half, S.WALL_TOP_Z),
        (kp_half, S.WALL_TOP_Z),
        (kp_half, S.rafter_bot_z(kp_half)),
        (S.RIDGE_HALF_W, S.RIDGE_BOT_Z),
        (-S.RIDGE_HALF_W, S.RIDGE_BOT_Z),
        (-kp_half, S.rafter_bot_z(kp_half)),
    ]
    king_post = extrude_xz_polygon(kp_pts, truss_y0, truss_y1)
    king_post.label = "porch_truss_king_post"
    mat.apply_material(king_post, timber)
    truss_parts.append(king_post)

    # Two diagonal timber struts in the front porch king-post truss (70 mm thick)
    strut_y0, strut_y1 = S.PORCH_POST_Y - 35.0, S.PORCH_POST_Y + 35.0
    for side, s_lbl in ((-1.0, "left"), (1.0, "right")):
        pts_pos = [
            (kp_half, 2995.0),
            (kp_half, 3085.0),
            (720.0, S.rafter_bot_z(720.0)),
            (850.0, S.rafter_bot_z(850.0)),
        ]
        pts = pts_pos if side > 0 else [(-x, z) for x, z in reversed(pts_pos)]
        strut = extrude_xz_polygon(pts, strut_y0, strut_y1)
        strut.label = f"porch_truss_strut_{s_lbl}"
        mat.apply_material(strut, timber)
        truss_parts.append(strut)

    parts.append(bd.Compound(children=truss_parts, label="front_porch_truss"))

    # Standard sloped roof rafters (45 mm thick)
    rafter_spans = [
        ("fly_front", S.ROOF_Y_MIN, S.ROOF_Y_MIN + S.RAFTER_W),
        ("porch_mid", -2250.0 - S.RAFTER_W / 2, -2250.0 + S.RAFTER_W / 2),
        ("wall_front", S.SHOP_Y_MIN, S.SHOP_Y_MIN + S.RAFTER_W),
    ]
    for i, cy in enumerate(S.INTERIOR_RAFTER_YS):
        rafter_spans.append((f"int_{i}", cy - S.RAFTER_W / 2, cy + S.RAFTER_W / 2))
    rafter_spans.extend([
        ("wall_rear", S.SHOP_Y_MAX - S.RAFTER_W, S.SHOP_Y_MAX),
        ("fly_rear", S.ROOF_Y_MAX - S.RAFTER_W, S.ROOF_Y_MAX),
    ])

    rafter_parts = []
    for tag, y0, y1 in rafter_spans:
        for side, s_lbl in ((-1.0, "left"), (1.0, "right")):
            r = extrude_xz_polygon(_rafter_polygon_xz(side), y0, y1)
            r.label = f"rafter_{tag}_{s_lbl}"
            mat.apply_material(r, spruce)
            rafter_parts.append(r)
    parts.append(bd.Compound(children=rafter_parts, label="rafters"))

    # Interior raised collar ties (flush trapezoid seated cleanly between left & right rafters)
    x_bot = S.INNER_X_MAX - (S.COLLAR_BOT_Z - S.WALL_TOP_Z) / S.ROOF_SLOPE  # 948.0
    x_top = S.INNER_X_MAX - (S.COLLAR_TOP_Z - S.WALL_TOP_Z) / S.ROOF_SLOPE  # 768.0
    collar_pts = [
        (-x_bot, S.COLLAR_BOT_Z),
        (x_bot, S.COLLAR_BOT_Z),
        (x_top, S.COLLAR_TOP_Z),
        (-x_top, S.COLLAR_TOP_Z),
    ]
    collars = []
    for i, cy in enumerate(S.INTERIOR_RAFTER_YS):
        ct = extrude_xz_polygon(collar_pts, cy - S.RAFTER_W / 2, cy + S.RAFTER_W / 2)
        ct.label = f"collar_tie_{i}"
        mat.apply_material(ct, timber)
        collars.append(ct)
    parts.append(bd.Compound(children=collars, label="collar_ties"))

    # Gable overhang outlooker purlins connecting fly-rafters cleanly to front truss & rear wall rafter
    outlookers = []
    out_spans = [
        ("front", S.ROOF_Y_MIN + S.RAFTER_W, truss_y0),
        ("rear", S.SHOP_Y_MAX, S.ROOF_Y_MAX - S.RAFTER_W),
    ]
    for end_lbl, oy0, oy1 in out_spans:
        for side, s_lbl in ((-1.0, "left"), (1.0, "right")):
            for j, abs_x in enumerate((700.0, 1450.0)):
                ox0 = side * abs_x - 22.5
                ox1 = side * abs_x + 22.5
                z_lo_l = S.rafter_bot_z(abs(ox0)) + 2.0
                z_lo_r = S.rafter_bot_z(abs(ox1)) + 2.0
                z_hi_l = S.rafter_top_z(abs(ox0)) - 2.0
                z_hi_r = S.rafter_top_z(abs(ox1)) - 2.0
                pts = [(ox0, z_lo_l), (ox1, z_lo_r), (ox1, z_hi_r), (ox0, z_hi_l)]
                ob = extrude_xz_polygon(pts, oy0, oy1)
                ob.label = f"outlooker_{end_lbl}_{s_lbl}_{j}"
                mat.apply_material(ob, spruce)
                outlookers.append(ob)
    parts.append(bd.Compound(children=outlookers, label="gable_outlookers"))

    return bd.Compound(children=parts, label="roof_framing")


@model
def framing():
    """Complete structural timber framing for the 1-story wooden shop."""
    front_wall = _build_framed_wall(
        name="front_wall_frame",
        axis="X",
        u_min=S.SHOP_X_MIN,
        u_max=S.SHOP_X_MAX,
        v_min=S.SHOP_Y_MIN,
        v_max=S.INNER_Y_MIN,
        upper_u_min=S.INNER_X_MIN,
        upper_u_max=S.INNER_X_MAX,
        openings=[
            (S.DOOR_X_MIN, S.DOOR_X_MAX, S.DOOR_Z_MIN, S.DOOR_Z_MAX, True),
            (S.FRONT_WIN_X_MIN, S.FRONT_WIN_X_MAX, S.FRONT_WIN_Z_MIN, S.FRONT_WIN_Z_MAX, False),
        ],
    )
    rear_wall = _build_framed_wall(
        name="rear_wall_frame",
        axis="X",
        u_min=S.SHOP_X_MIN,
        u_max=S.SHOP_X_MAX,
        v_min=S.INNER_Y_MAX,
        v_max=S.SHOP_Y_MAX,
        upper_u_min=S.INNER_X_MIN,
        upper_u_max=S.INNER_X_MAX,
        openings=[
            (S.REAR_WIN_X_MIN, S.REAR_WIN_X_MAX, S.REAR_WIN_Z_MIN, S.REAR_WIN_Z_MAX, False),
        ],
    )
    left_wall = _build_framed_wall(
        name="left_wall_frame",
        axis="Y",
        u_min=S.INNER_Y_MIN,
        u_max=S.INNER_Y_MAX,
        v_min=S.SHOP_X_MIN,
        v_max=S.INNER_X_MIN,
        upper_u_min=S.SHOP_Y_MIN,
        upper_u_max=S.SHOP_Y_MAX,
        openings=[
            (S.LEFT_WIN_Y_MIN, S.LEFT_WIN_Y_MAX, S.LEFT_WIN_Z_MIN, S.LEFT_WIN_Z_MAX, False),
        ],
    )
    right_wall = _build_framed_wall(
        name="right_wall_frame",
        axis="Y",
        u_min=S.INNER_Y_MIN,
        u_max=S.INNER_Y_MAX,
        v_min=S.INNER_X_MAX,
        v_max=S.SHOP_X_MAX,
        upper_u_min=S.SHOP_Y_MIN,
        upper_u_max=S.SHOP_Y_MAX,
        openings=[
            (S.RIGHT_WIN_Y_MIN, S.RIGHT_WIN_Y_MAX, S.RIGHT_WIN_Z_MIN, S.RIGHT_WIN_Z_MAX, False),
        ],
    )

    front_gable = _build_gable_end_studs("front_gable_studs", S.SHOP_Y_MIN, S.INNER_Y_MIN)
    rear_gable = _build_gable_end_studs("rear_gable_studs", S.INNER_Y_MAX, S.SHOP_Y_MAX)
    porch = _build_porch_frame()
    roof = _build_roof_framing()

    asm = bd.Compound(
        children=[
            bd.Compound(
                children=[front_wall, rear_wall, left_wall, right_wall, front_gable, rear_gable],
                label="wall_framing",
            ),
            porch,
            roof,
        ],
        label="framing",
    )

    bb = asm.bounding_box()
    assert abs(bb.min.Z - S.WALL_BASE_Z) < 1e-3, bb
    assert abs(bb.max.Z - S.RIDGE_PEAK_Z) < 1e-2, bb
    return asm


if __name__ == "__main__":
    framing()
