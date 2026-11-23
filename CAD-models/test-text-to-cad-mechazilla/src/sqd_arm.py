"""Ship Quick Disconnect (SQD) cantilevered hinge outrigger, swinging lattice boom, cryo lines, and QD hood."""

import math

import build123d as bd
from cad import model

import spec as S


@model
def sqd_outrigger():
    """Fixed cantilevered hinge outrigger mounted cleanly on the -Y face of Tower Module 6 (Z ~ 825)."""
    hx = S.SQD_HINGE_X  # 46.0 (strictly behind front guide rail at X=68.5!)
    hy = S.SQD_HINGE_Y  # -98.0
    y_mount = -(S.COL_HALF + S.BEAM_SIZE / 2.0)  # -62.8 (flush on -Y face of Module 6 girders!)
    # Module 6 Z spans 775..920; horizontal girders sit at Z = 779.5 and Z = 847.5 (Z_top=850.3, Z_bot=844.7)
    z_clevis_bot = 809.0
    z_clevis_top = 843.0
    ear_h = 6.0
    ear_r = 8.0

    # Mounting backplate anchored cleanly against the -Y face of the Z=847.5 girder & vertical side frame
    # Spans X in [20.0, 50.0] (strictly clear of front column R=6 at X=54..66!)
    # Wait: Module 6 diagonal X-bracing sits at Y=-60 +/- 1.9 = -61.9, so Y <= -62.8 is 100% clear!
    back_plate = bd.Pos(35.0, y_mount, 809.0) * bd.Box(
        30.0,
        2.5,  # Y: -65.3 .. -62.8
        41.3,  # Z: 809.0 .. 850.3 (reaches right up to Module 6 mid-girder face!)
        align=(bd.Align.CENTER, bd.Align.MAX, bd.Align.MIN),
    )

    # Twin triangular cantilevered outrigger gusset webs reaching from Y=-65.3 out to hinge at (46, -98)
    parts = [back_plate]
    for z_ear in (z_clevis_bot, z_clevis_top - ear_h):
        # Horizontal clevis arm polygon in XY from backplate (Y=-65) out to hinge circle (46, -98)
        arm_poly = bd.Polygon(
            [
                (22.0, y_mount - 2.0),
                (50.0, y_mount - 2.0),
                (hx + ear_r, hy),
                (hx - ear_r, hy),
            ],
            align=None,
        )
        arm_ext = bd.Pos(0, 0, z_ear) * bd.extrude(arm_poly, ear_h, dir=(0, 0, 1))
        nose = bd.Pos(hx, hy, z_ear) * bd.Cylinder(
            ear_r, ear_h, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
        )
        parts.append(arm_ext)
        parts.append(nose)

    # Vertical stiffening web connecting top & bottom outrigger arms (stopping clear of hinge knuckle R=7.8!)
    stiff_poly = bd.Polygon(
        [
            (32.0, y_mount - 2.0),
            (46.0, y_mount - 2.0),
            (46.0, hy + 11.5),
            (36.0, hy + 11.5),
        ],
        align=None,
    )
    parts.append(
        bd.Pos(0, 0, z_clevis_bot + ear_h)
        * bd.extrude(stiff_poly, z_clevis_top - z_clevis_bot - 2.0 * ear_h, dir=(0, 0, 1))
    )

    pin_bore = bd.Pos(hx, hy, z_clevis_bot - 1.0) * bd.Cylinder(
        S.SQD_PIN_R + 0.3,
        z_clevis_top - z_clevis_bot + 2.0,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    bracket = (parts[0] + parts[1:]) - pin_bore
    bracket.label = "sqd_outrigger_bracket"
    S.apply_material(bracket, S.mat_tower_steel())

    # Vertical SQD Hinge Pin
    pin_shaft = bd.Pos(hx, hy, z_clevis_bot - 1.5) * bd.Cylinder(
        S.SQD_PIN_R,
        z_clevis_top - z_clevis_bot + 3.0,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    pin_cap_top = bd.Pos(hx, hy, z_clevis_top) * bd.Cylinder(
        5.5, 2.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    pin_cap_bot = bd.Pos(hx, hy, z_clevis_bot - 2.0) * bd.Cylinder(
        5.5, 2.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    pin = pin_shaft + [pin_cap_top, pin_cap_bot]
    pin.label = "sqd_hinge_pin"
    S.apply_material(pin, S.mat_guide_rail())

    return bd.Compound(children=[bracket, pin], label="sqd_outrigger")


def _build_sqd_boom_local():
    """Build SQD lattice boom, cryo lines, and curved Starship QD hood in arm-local frame.

    Arm-local frame:
      - Origin (0, 0, 0) at SQD hinge center (46.0, -98.0, 826.0)
      - +X points along boom toward Starship aft QD port (length = SQD_DEPLOY_LEN ~ 230.8 mm)
      - Z centered on 0 (height 20.4 mm -> Z in [-10.2, +10.2], fitting cleanly in clevis slot [-11.0, +11.0]!)
    """
    boom_len = S.SQD_DEPLOY_LEN - 10.0  # ~220.8 mm to hood root
    h_root = 20.4  # Fits inside 22.0 mm clevis slot with 0.8 mm top & bottom clearance!
    h_tip = 16.0
    w_boom = 11.6

    # 1. Hinge knuckle cylinder + tapered open-web lattice truss boom
    knuckle = bd.Cylinder(7.0, h_root)

    # Build side-truss silhouette in XZ (centered on Z=0), carve 6 open lattice windows
    side_pts = [
        (0.0, -h_root / 2.0),
        (boom_len, -h_tip / 2.0),
        (boom_len, h_tip / 2.0),
        (0.0, h_root / 2.0),
    ]
    side_face = bd.Polygon(side_pts, align=None)
    n_bays = 6
    x_start = 14.0
    bay_w = (boom_len - x_start - 8.0) / n_bays
    for i in range(n_bays):
        xa = x_start + i * bay_w
        xb = xa + bay_w
        xm = (xa + xb) / 2.0
        t_a = xa / boom_len
        t_b = xb / boom_len
        t_m = xm / boom_len
        ha = (h_root * (1 - t_a) + h_tip * t_a) / 2.0 - 2.6
        hb = (h_root * (1 - t_b) + h_tip * t_b) / 2.0 - 2.6
        hm = (h_root * (1 - t_m) + h_tip * t_m) / 2.0 - 2.6
        tri1 = bd.Polygon([(xa + 1.8, -ha), (xb - 1.8, -hb), (xm, hm - 1.0)], align=None)
        tri2 = bd.Polygon([(xa + 0.8, ha), (xm - 1.8, hm), (xa + 0.8, -ha + 2.4)], align=None)
        tri3 = bd.Polygon([(xm + 1.8, hm), (xb - 0.8, hb), (xb - 0.8, -hb + 2.4)], align=None)
        side_face = side_face - tri1 - tri2 - tri3

    # Two parallel lattice side walls (left & right webs) connected by top & bottom cross ties!
    wall_t = 2.4
    wall_proto = bd.Rot(90, 0, 0) * bd.extrude(side_face, wall_t / 2.0, both=True)
    wall_pos = bd.Pos(0, w_boom / 2.0 - wall_t / 2.0, 0) * wall_proto
    wall_neg = bd.Pos(0, -(w_boom / 2.0 - wall_t / 2.0), 0) * wall_proto

    # Top & bottom cross-ties bridging the two side lattice walls
    ties = []
    for i in range(n_bays + 1):
        xt = x_start + i * bay_w
        t_x = xt / boom_len
        hz = (h_root * (1 - t_x) + h_tip * t_x) / 2.0 - 1.3
        for sz in (-1, 1):
            ties.append(bd.Pos(xt, 0, sz * hz) * bd.Box(3.6, w_boom, 2.4))

    # Solid root block bridging knuckle to twin side walls
    root_bridge = bd.Pos(8.0, 0, 0) * bd.Box(14.0, w_boom, h_root)

    pin_bore = bd.Cylinder(S.SQD_PIN_R + 0.5, h_root + 4.0)  # R=4.0 bore around R=3.5 pin
    boom = (knuckle + [root_bridge, wall_pos, wall_neg, *ties]) - pin_bore
    boom.label = "sqd_lattice_boom"
    S.apply_material(boom, S.mat_sqd_steel())

    # 2. Twin insulated stainless cryogenic propellant feedlines running cleanly along the top of boom
    # Plus crisp steel saddle clamps anchoring the pipes down onto the tapered top cross-ties!
    cryo_lines = []
    pipe_z = 12.0
    pipe_r = 1.5
    for cy, name in ((-3.2, "sqd_lox_line"), (3.2, "sqd_ch4_line")):
        pipe = (
            bd.Pos(14.0, cy, pipe_z)
            * bd.Rot(0, 90, 0)
            * bd.Cylinder(
                pipe_r,
                boom_len - 18.0,
                align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
            )
        )
        pipe.label = name
        S.apply_material(pipe, S.mat_stainless())
        cryo_lines.append(pipe)

    # Pipe saddle pedestals bridging from each top cross-tie up to pipe undersides (Z = 10.5)
    saddles = []
    for i in range(1, n_bays):
        xt = x_start + i * bay_w
        t_x = xt / boom_len
        tie_top_z = (h_root * (1 - t_x) + h_tip * t_x) / 2.0
        ped_h = (pipe_z - pipe_r) - tie_top_z
        if ped_h > 0.2:
            saddles.append(
                bd.Pos(xt, 0, tie_top_z)
                * bd.Box(
                    2.6,
                    9.4,
                    ped_h,
                    align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
                )
            )
    if saddles:
        pipe_rack = saddles[0] + saddles[1:] if len(saddles) > 1 else saddles[0]
        pipe_rack = pipe_rack - boom
        pipe_rack.label = "sqd_pipe_supports"
        S.apply_material(pipe_rack, S.mat_tower_steel())
        cryo_lines.append(pipe_rack)

    # 3. Iconic Curved Starship Quick Disconnect Hood & Stabilizer Claw at tip!
    # Positioned at x = SQD_DEPLOY_LEN (~230.8) and counter-rotated by -SQD_DEPLOY_ANGLE_DEG
    # so the concave hood wraps cleanly around Starship's R=45 mm fuselage facing +X!
    hood_h = 24.0
    r_in = S.ROCKET_RADIUS + 1.5   # 46.5 mm inner concave arc (1.5 mm clearance off Starship skin!)
    r_out = r_in + 5.5             # 52.0 mm outer hood shell
    arc_half = 24.0                # +/-24 deg arc around Starship fuselage (~38 mm wide claw!)

    # Build curved claw profile in hood-local XY (rocket center at (+r_in, 0))
    pts_outer = []
    pts_inner = []
    n_seg = 12
    for k in range(n_seg + 1):
        ang = math.radians(180.0 - arc_half + 2.0 * arc_half * (k / n_seg))
        pts_outer.append((r_in + r_out * math.cos(ang), r_out * math.sin(ang)))
        pts_inner.append((r_in + r_in * math.cos(ang), r_in * math.sin(ang)))
    claw_pts = pts_outer + list(reversed(pts_inner))
    claw_shell = bd.Pos(0, 0, -hood_h / 2.0) * bd.extrude(
        bd.Polygon(claw_pts, align=None), hood_h, dir=(0, 0, 1)
    )
    # Rear mounting box & umbilical manifold block joining claw to boom tip
    rear_box = bd.Pos(-7.5, 0, 0) * bd.Box(12.0, 18.0, 18.0)
    hood_local = claw_shell + rear_box

    # Place hood at boom tip, angled to align with world +X (Starship fuselage normal)
    hood = (
        bd.Pos(S.SQD_DEPLOY_LEN - 2.0, 0, 0)
        * bd.Rot(0, 0, -S.SQD_DEPLOY_ANGLE_DEG)
        * hood_local
    )
    # Trim any tiny overlap with boom tip cleanly so hood & boom touch face-to-face
    hood = hood - boom
    hood.label = "sqd_umbilical_hood"
    S.apply_material(hood, S.mat_carriage_steel())

    # Twin stainless cryo QD coupler nozzles protruding cleanly inside the concave hood
    nozzles = []
    for ny, nname in ((-4.5, "sqd_coupler_lox"), (4.5, "sqd_coupler_ch4")):
        noz = (
            bd.Pos(S.SQD_DEPLOY_LEN - 2.0, 0, 0)
            * bd.Rot(0, 0, -S.SQD_DEPLOY_ANGLE_DEG)
            * bd.Pos(0.5, ny, 0)
            * bd.Rot(0, 90, 0)
            * bd.Cylinder(2.2, 5.5, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        )
        noz.label = nname
        S.apply_material(noz, S.mat_stainless())
        nozzles.append(noz)

    return [boom, *cryo_lines, hood, *nozzles]


@model
def sqd_arm():
    """Swinging Starship Quick Disconnect (SQD) arm built in Deployed pose (connected to Ship port)."""
    # Hinge center at (SQD_HINGE_X, SQD_HINGE_Y, 826.0), rotated +SQD_DEPLOY_ANGLE_DEG toward (255, 0)
    hinge_z = 826.0  # Exact midpoint of clevis slot [815.0 .. 837.0]
    world_xf = bd.Pos(S.SQD_HINGE_X, S.SQD_HINGE_Y, hinge_z) * bd.Rot(
        0, 0, S.SQD_DEPLOY_ANGLE_DEG
    )
    children = [world_xf * part for part in _build_sqd_boom_local()]
    return bd.Compound(children=children, label="sqd_arm")


if __name__ == "__main__":
    sqd_outrigger()
    sqd_arm()
