"""Tesla Cybertruck matte-black exterior cladding, bumpers, lower headlights, rear diffuser,
trapezoidal fender flares, slatted Vault tonneau cover, Gigawiper, and triangular side mirrors.

Dimensions locked strictly to Tesla official specs:
  - Front bumper tip at s = 0.0 mm, rear bumper step at s = 5683.0 mm -> 5683.0 mm exact overall length.
  - Trapezoidal fender flares span X in [-1016.0, +1016.0] -> 2032.0 mm width excl. mirrors.
  - Triangular side mirrors span X in [-1206.5, +1206.5] -> 2413.0 mm width incl. mirrors.
"""

from __future__ import annotations

import math

import build123d as bd
from cad import model

from lib import geometry, materials, spec


def _build_front_bumper_and_headlights() -> list[bd.Solid]:
    """Stepped matte-black front bumper (intake, tow hooks, camera, skid), headlight channel & lower projectors."""
    # 5 evenly spaced X slices for smooth curved-V production bumper sweep matching frunk nose
    x_slices = [-920.0, -460.0, 0.0, 460.0, 920.0]

    bumper_secs = []
    for x in x_slices:
        bow = spec.front_bow_ds(x)
        # At X=0, tip is at s=0.0 mm; sweeps smoothly back ~112 mm at corners
        s_tip = spec.S_BUMPER_TIP + bow
        s_top_back = s_tip + 115.0
        s_chin = s_tip + 58.0
        s_skid_end = 412.0 if abs(x) <= 500.0 else max(s_chin + 45.0, 225.0)
        z_skid_end = 398.0 if abs(x) <= 500.0 else 465.0
        bumper_secs.append([
            (x, spec.s_to_y(s_tip), 664.0),
            (x, spec.s_to_y(s_top_back), 664.0),
            (x, spec.s_to_y(s_top_back), 500.0),
            (x, spec.s_to_y(s_skid_end), z_skid_end + 35.0),
            (x, spec.s_to_y(s_skid_end), z_skid_end),
            (x, spec.s_to_y(s_chin), spec.Z_FRONT_BUMPER_BOT),
            (x, spec.s_to_y(s_tip), 575.0),
        ])
    bumper = bd.loft([bd.Face(bd.Wire.make_polygon(p)) for p in bumper_secs], ruled=False)

    # Side bumper wings wrapping back under trimmed front stainless fenders (Z in [465, 666], s in [195..238])
    for sx in (-1.0, 1.0):
        wing = bd.Pos(sx * 865.0, spec.s_to_y(218.0), 566.0) * bd.Box(110.0, 75.0, 198.0)
        bumper = bumper + wing

    # Cut front lower air-intake grille pocket & twin recessed tow-hook pockets
    y_front = spec.s_to_y(0.0)
    intake_cut = bd.Pos(0.0, y_front + 45.0, 530.0) * bd.Box(780.0, 110.0, 68.0)
    tow_cut_l = bd.Pos(530.0, y_front + 75.0, 588.0) * bd.Box(118.0, 110.0, 56.0)
    tow_cut_r = bd.Pos(-530.0, y_front + 75.0, 588.0) * bd.Box(118.0, 110.0, 56.0)
    bumper = bumper - [intake_cut, tow_cut_l, tow_cut_r]

    # Add crisp horizontal cooling louvers inside intake pocket & central front Tesla Vision camera pod
    louvers = [
        bd.Pos(0.0, y_front + 48.0, z_l) * bd.Box(770.0, 26.0, 8.0)
        for z_l in (512.0, 530.0, 548.0)
    ]
    cam_pod = bd.Pos(0.0, y_front + 22.0, 636.0) * bd.Box(76.0, 40.0, 32.0)
    bumper = bumper + [*louvers, cam_pod]
    materials.apply_mat(bumper, materials.matte_black_cladding, "front_bumper")

    # Twin heavy recovery tow hook shackles recessed cleanly inside the tow-hook pockets
    hooks = []
    for sx in (-1.0, 1.0):
        hx = sx * 530.0
        hy = spec.s_to_y(spec.front_bow_ds(hx) + 26.0)
        ring = bd.Pos(hx, hy, 588.0) * bd.Box(80.0, 44.0, 32.0) - bd.Pos(hx, hy - 4.0, 588.0) * bd.Box(46.0, 32.0, 40.0)
        hooks.append(ring)
    tow_hooks = hooks[0] + hooks[1]
    materials.apply_mat(tow_hooks, materials.underbody_skid_metal, "front_tow_hooks")

    # Recessed dark horizontal headlight channel between front bumper (Z=664) and stainless frunk nose (Z=738)
    # Spans X in [-874, +874] so it stays cleanly inside the 2-deg inward-tucked lower front fender skin (X=885)
    slot_secs = []
    for x in [-874.0, -437.0, 0.0, 437.0, 874.0]:
        s_face = spec.S_NOSE_CENTER + spec.front_bow_ds(x) + 12.0
        y_f = spec.s_to_y(s_face)
        slot_secs.append([
            (x, y_f, 670.0),
            (x, y_f, 732.0),
            (x, y_f + 35.0, 732.0),
            (x, y_f + 35.0, 670.0),
        ])
    slot_backing = bd.loft([bd.Face(bd.Wire.make_polygon(p)) for p in slot_secs], ruled=False)
    materials.apply_mat(slot_backing, materials.dark_charcoal_trim, "headlight_slot_backing")

    # Signature production Cybertruck lower projector headlamps tucked into outer channel ends
    proj_parts = []
    amber_parts = []
    for sx in (-1.0, 1.0):
        # Main low/high beam rectangular projector cluster (X = +-595 .. +-800)
        x_in, x_out = sx * 595.0, sx * 800.0
        p_secs = []
        for xv in (min(x_in, x_out), (x_in + x_out) / 2.0, max(x_in, x_out)):
            s_p = spec.S_NOSE_CENTER + spec.front_bow_ds(xv) + 2.0
            y_p = spec.s_to_y(s_p)
            p_secs.append([
                (xv, y_p, 680.0),
                (xv, y_p, 722.0),
                (xv, y_p + 8.0, 722.0),
                (xv, y_p + 8.0, 680.0),
            ])
        proj_parts.append(bd.loft([bd.Face(bd.Wire.make_polygon(p)) for p in p_secs], ruled=False))

        # Outer amber side-marker lamp (X = +-816 .. +-872, clears front fender inner skin 885 mm!)
        xa_in, xa_out = sx * 816.0, sx * 872.0
        a_secs = []
        for xv in (min(xa_in, xa_out), max(xa_in, xa_out)):
            s_a = spec.S_NOSE_CENTER + spec.front_bow_ds(xv) + 3.0
            y_a = spec.s_to_y(s_a)
            a_secs.append([
                (xv, y_a, 686.0),
                (xv, y_a, 718.0),
                (xv, y_a + 7.0, 718.0),
                (xv, y_a + 7.0, 686.0),
            ])
        amber_parts.append(geometry.ruled_loft_sections(a_secs))

    headlights = proj_parts[0] + proj_parts[1]
    markers = amber_parts[0] + amber_parts[1]
    materials.apply_mat(headlights, materials.headlight_projector, "lower_headlights")
    materials.apply_mat(markers, materials.amber_marker_led, "front_amber_markers")

    return [bumper, tow_hooks, slot_backing, headlights, markers]


def _build_rear_bumper_and_diffuser() -> list[bd.Solid]:
    """Heavy-duty protruding rear bumper (step shelf to s=5683), license recess, lower lamps, & 5-fin diffuser."""
    y_back = spec.s_to_y(spec.S_REAR_BUMPER_END)  # +2841.5 mm exact!
    y_front = spec.s_to_y(5585.0)
    hw_rear = 922.0

    # Main protruding rear bumper beam (Z = 475 .. 646 mm, strictly below tailgate Z >= 658)
    main_yz = [
        (y_front, 475.0),
        (y_front, 646.0),
        (y_back, 646.0),
        (y_back, 555.0),
        (y_back - 32.0, 475.0),
    ]
    rb = geometry.extrude_yz_polygon(main_yz, -hw_rear, hw_rear)

    # Wrap-around lower rear bumper side wings meeting rear fender flares cleanly (s in [5176..5590])
    for sx in (-1.0, 1.0):
        # Linear taper following rear quarter x_rocker(s) from s=5176 to s=5590
        s0, s1 = 5178.0, 5595.0
        x0_out = spec.x_body_lower(s0, 560.0) + 6.0
        x1_out = hw_rear
        wing_f = [
            (sx * (x0_out - 55.0), spec.s_to_y(s0), 475.0),
            (sx * x0_out, spec.s_to_y(s0), 475.0),
            (sx * x0_out, spec.s_to_y(s0), 646.0),
            (sx * (x0_out - 55.0), spec.s_to_y(s0), 646.0),
        ]
        wing_r = [
            (sx * (x1_out - 55.0), spec.s_to_y(s1), 475.0),
            (sx * x1_out, spec.s_to_y(s1), 475.0),
            (sx * x1_out, spec.s_to_y(s1), 646.0),
            (sx * (x1_out - 55.0), spec.s_to_y(s1), 646.0),
        ]
        if sx < 0:
            wing_f = list(reversed(wing_f))
            wing_r = list(reversed(wing_r))
        rb = rb + geometry.ruled_loft_sections([wing_f, wing_r])

    # Angled underbody diffuser pan sweeping forward from rear bumper bottom (s=5650, Z=475) to s=5275, Z=418
    diff_yz = [
        (spec.s_to_y(5275.0), 418.0),
        (spec.s_to_y(5648.0), 475.0),
        (spec.s_to_y(5648.0), 505.0),
        (spec.s_to_y(5275.0), 450.0),
    ]
    diff_pan = geometry.extrude_yz_polygon(diff_yz, -690.0, 690.0)
    rb = rb + diff_pan

    # 5 crisp vertical aerodynamic diffuser strake fins under rear bumper
    fins = []
    fin_yz = [
        (spec.s_to_y(5340.0), 426.0),
        (spec.s_to_y(5642.0), 472.0),
        (spec.s_to_y(5642.0), 440.0),
        (spec.s_to_y(5370.0), 406.0),
    ]
    for fx in (-540.0, -270.0, 0.0, 270.0, 540.0):
        fins.append(geometry.extrude_yz_polygon(fin_yz, fx - 12.0, fx + 12.0))
    rb = rb + fins

    # Carve central license-plate recess pocket & lower bumper auxiliary lamp recesses
    plate_cut = bd.Pos(0.0, y_back + 5.0, 568.0) * bd.Box(
        355.0, 40.0, 128.0, align=(bd.Align.CENTER, bd.Align.MAX, bd.Align.CENTER)
    )
    lamp_cut_l = bd.Pos(710.0, y_back + 5.0, 606.0) * bd.Box(
        246.0, 22.0, 26.0, align=(bd.Align.CENTER, bd.Align.MAX, bd.Align.CENTER)
    )
    lamp_cut_r = bd.Pos(-710.0, y_back + 5.0, 606.0) * bd.Box(
        246.0, 22.0, 26.0, align=(bd.Align.CENTER, bd.Align.MAX, bd.Align.CENTER)
    )
    rb = rb - [plate_cut, lamp_cut_l, lamp_cut_r]
    materials.apply_mat(rb, materials.matte_black_cladding, "rear_bumper")

    # Twin lower federal-regulation rear bumper red lamp bars seated cleanly in recesses
    lamp_l = bd.Pos(710.0, y_back - 3.0, 606.0) * bd.Box(
        236.0, 10.0, 20.0, align=(bd.Align.CENTER, bd.Align.MAX, bd.Align.CENTER)
    )
    lamp_r = bd.Pos(-710.0, y_back - 3.0, 606.0) * bd.Box(
        236.0, 10.0, 20.0, align=(bd.Align.CENTER, bd.Align.MAX, bd.Align.CENTER)
    )
    rear_lamps = lamp_l + lamp_r
    materials.apply_mat(rear_lamps, materials.taillight_red_led, "rear_bumper_lamps")

    return [rb, rear_lamps]


def _build_fender_flares_and_rockers() -> list[bd.Solid]:
    """4 iconic matte-black trapezoidal fender flares (width = 2032 mm exact) + continuous side rockers."""
    flares = []
    for s_axle in (spec.S_FRONT_AXLE, spec.S_REAR_AXLE):
        pts_in = spec.arch_polygon_2d(s_axle, expand=0.0)
        pts_out = spec.arch_polygon_2d(s_axle, expand=spec.FLARE_BAND_W)
        # Beveled outer profile (32 mm narrower band on outer plane X = FLARE_OUTER_X = 1016.0 mm)
        pts_lip = spec.arch_polygon_2d(s_axle, expand=30.0)

        # Build clean beveled frustum between constant-X YZ planes (100% planar!)
        x_in_raw = 890.0
        f_base = bd.Face(bd.Wire.make_polygon([(x_in_raw, y, z) for y, z in pts_out]))
        f_lip = bd.Face(bd.Wire.make_polygon([(spec.FLARE_OUTER_X, y, z) for y, z in pts_lip]))
        flare_raw = bd.loft([f_base, f_lip], ruled=True)

        # Subtract exact trapezoidal wheel-arch opening
        arch_cut = geometry.extrude_yz_polygon(pts_in, x_in_raw - 20.0, spec.FLARE_OUTER_X + 20.0)
        flare_l = flare_raw - arch_cut

        # Trim inboard side cleanly 3.5 mm outside the local tapered stainless body surface so zero overlap!
        s_a = s_axle - 720.0
        s_b = s_axle + 720.0
        hinge_s = spec.S_FRONT_DOOR_SEAM if s_axle == spec.S_FRONT_AXLE else spec.S_REAR_DOOR_SEAM
        stations = sorted({s_a, hinge_s, s_b})
        sec_list = []
        for sv in stations:
            yv = spec.s_to_y(sv)
            x_lo = spec.x_body_lower(sv, 365.0) + 3.5
            x_hi = spec.x_belt(sv) + 3.5
            # Extrapolate slope cleanly down to Z=250 and up to Z=1150 so no clamping kink!
            zb = spec.z_belt(sv)
            slope = (x_hi - x_lo) / (zb - 365.0)
            x_250 = x_lo + slope * (250.0 - 365.0)
            x_1150 = x_lo + slope * (1150.0 - 365.0)
            sec_list.append([
                (800.0, yv, 250.0),
                (x_250, yv, 250.0),
                (x_1150, yv, 1150.0),
                (800.0, yv, 1150.0),
            ])
        inboard_cut = geometry.ruled_loft_sections(sec_list)

        flare_l = flare_l - inboard_cut

        # Trim outer approach/departure tips flush with front/rear bumper bottom planes,
        # and keep front flare trailing edge clear of the front door opening (s <= S_FRONT_DOOR_SEAM - 3)
        if s_axle == spec.S_FRONT_AXLE:
            tip_trim = bd.Pos(980.0, spec.s_to_y(s_axle - 380.0), spec.Z_FRONT_BUMPER_BOT) * bd.Box(
                280.0, 500.0, 260.0, align=(bd.Align.CENTER, bd.Align.MAX, bd.Align.MAX)
            )
            door_clear = bd.Pos(980.0, spec.s_to_y(spec.S_FRONT_DOOR_SEAM - 3.0), 650.0) * bd.Box(
                280.0, 300.0, 900.0, align=(bd.Align.CENTER, bd.Align.MIN, bd.Align.CENTER)
            )
            flare_l = flare_l - [tip_trim, door_clear]
        else:
            tip_trim = bd.Pos(980.0, spec.s_to_y(s_axle + 380.0), spec.Z_REAR_BUMPER_BOT) * bd.Box(
                280.0, 500.0, 260.0, align=(bd.Align.CENTER, bd.Align.MIN, bd.Align.MAX)
            )
            flare_l = flare_l - tip_trim

        flare_r = bd.mirror(flare_l, about=bd.Plane.YZ)
        flares.extend([flare_l, flare_r])

    all_flares = flares[0] + flares[1:]
    materials.apply_mat(all_flares, materials.matte_black_cladding, "trapezoidal_fender_flares")

    # Continuous matte-black lower rocker cladding sills connecting front & rear fender flares cleanly
    # Front flare trailing edge stops at s=1482 (door seam); rear flare front edge starts at s=3849
    s_rk0 = 1486.0
    s_rk1 = 3845.0
    y_rk0, y_rk1 = spec.s_to_y(s_rk0), spec.s_to_y(s_rk1)
    # Cross section strictly clear of battery_skid_pan (|X| <= 920 at Z <= 307) & doors (Z >= 367)
    rk_xz = [
        (932.0, spec.Z_ROCKER_BOT),
        (974.0, spec.Z_ROCKER_BOT + 12.0),
        (978.0, spec.Z_ROCKER_TOP - 2.0),
        (945.0, spec.Z_ROCKER_TOP - 2.0),
        (932.0, 314.0),
    ]
    rk_l = bd.extrude(
        bd.Face(bd.Wire.make_polygon([(x, y_rk0, z) for x, z in rk_xz])),
        amount=(y_rk1 - y_rk0),
        dir=(0, 1, 0),
    )
    rk_r = bd.mirror(rk_l, about=bd.Plane.YZ)
    rockers = rk_l + rk_r
    materials.apply_mat(rockers, materials.matte_black_cladding, "lower_rocker_cladding")

    return [all_flares, rockers]


def _build_vault_tonneau_and_sail_caps() -> list[bd.Solid]:
    """Triangular polymer sail-pillar top bed-rail caps + 28-slat metallic-black Vault tonneau cover."""
    # 1. Left & right flat triangular sail-pillar upper bed-rail caps (tapered flat bed-rail applique)
    # Strictly clear of stainless sail skin (outer edge >= 8 mm inside sail plane) and tailgate (s <= 5600)
    s_c = spec.S_CAB_REAR + 65.0
    s_t = 5600.0
    z_c = spec.z_roof(s_c)
    z_t_in = spec.z_roof(s_t)
    z_t_out = spec.z_belt(s_t) + 4.0

    p_c_top = (spec.TONNEAU_HALF_W, spec.s_to_y(s_c), z_c)
    p_t_in = (spec.TONNEAU_HALF_W, spec.s_to_y(s_t), z_t_in)
    p_t_out = (spec.x_belt(s_t) - 22.0, spec.s_to_y(s_t), z_t_out)

    cap_l = geometry.tri_slab(p_c_top, p_t_in, p_t_out, thickness=7.0, inward_normal_hint=(0.0, 0.0, -1.0))
    cap_r = bd.mirror(cap_l, about=bd.Plane.YZ)
    sail_caps = cap_l + cap_r
    materials.apply_mat(sail_caps, materials.matte_black_cladding, "sail_pillar_top_caps")

    # 2. Iconic retractable slatted metallic-black Vault tonneau cover (28 crisp interlocking transverse slats!)
    n_slats = 28
    s_start = spec.S_CAB_REAR + 6.0   # 3771 mm (cleanly behind rear cab header & CHMSL)
    s_end = 5598.0                    # 8 mm ahead of closed tailgate top cap (s=5606..5638)
    pitch = (s_end - s_start) / n_slats
    slat_len = pitch - 3.5            # 3.5 mm crisp dark slat shadow bevel between slats
    slat_hw = spec.TONNEAU_HALF_W - 4.0  # 731 mm (1462 mm clear span between sail caps)
    slat_thick = 16.0

    # Continuous thin dark under-track plate unifying all 28 slats into one clean solid part
    base_yz = [
        (spec.s_to_y(s_start), spec.z_roof(s_start) - 10.0),
        (spec.s_to_y(s_end), spec.z_roof(s_end) - 10.0),
        (spec.s_to_y(s_end), spec.z_roof(s_end) - 20.0),
        (spec.s_to_y(s_start), spec.z_roof(s_start) - 20.0),
    ]
    tonneau = geometry.extrude_yz_polygon(base_yz, -slat_hw, slat_hw)

    slat_solids = []
    for i in range(n_slats):
        sa = s_start + i * pitch + 1.5
        sb = sa + slat_len
        za = spec.z_roof(sa) - 1.0
        zb = spec.z_roof(sb) - 1.0
        s_yz = [
            (spec.s_to_y(sa), za - 11.0),
            (spec.s_to_y(sa), za),
            (spec.s_to_y(sb), zb),
            (spec.s_to_y(sb), zb - 11.0),
        ]
        slat_solids.append(geometry.extrude_yz_polygon(s_yz, -slat_hw, slat_hw))

    tonneau = tonneau + slat_solids
    materials.apply_mat(tonneau, materials.dark_charcoal_trim, "vault_tonneau_cover")

    return [sail_caps, tonneau]


def _build_cowl_and_gigawiper() -> list[bd.Solid]:
    """Ventilated matte-black cowl grille + iconic vertical driver-side (+X) single Gigawiper."""
    # 1. Cowl grille bridging frunk trailing edge and windshield base
    cowl_secs = []
    for x in [-810.0, -405.0, 0.0, 405.0, 810.0]:
        u = abs(x) / 896.0
        s_f = spec.S_COWL_CENTER + spec.cowl_bow_ds(x) - 6.0
        s_r = s_f + 22.0
        z_top = spec.Z_COWL - 18.0 - 14.0 * (u ** 1.6)
        cowl_secs.append([
            (x, spec.s_to_y(s_f), z_top),
            (x, spec.s_to_y(s_r), z_top),
            (x, spec.s_to_y(s_r), z_top - 16.0),
            (x, spec.s_to_y(s_f), z_top - 16.0),
        ])
    cowl = bd.loft([bd.Face(bd.Wire.make_polygon(p)) for p in cowl_secs], ruled=False)
    materials.apply_mat(cowl, materials.matte_black_cladding, "cowl_grille")

    # 2. The iconic "Gigawiper" parked vertically along the driver-side (+X) windshield edge!
    # Hugs the windshield glass tightly (3-5 mm proud -> zero floating gap, zero glass overlap!).
    s0, s1 = 925.0, 2245.0
    x0, x1 = 776.0, 650.0
    z0 = spec.z_roof(s0) + 5.0
    z1 = spec.z_roof(s1) + 5.0
    y0, y1 = spec.s_to_y(s0), spec.s_to_y(s1)

    # Pivot hub housing at driver cowl base
    pivot = bd.Pos(x0, y0, z0 - 2.0) * bd.Box(68.0, 88.0, 28.0)

    # Main structural wiper arm (lower 58% of reach) + full 1,240 mm flat aero rubber blade
    p_mid = (x0 + 0.58 * (x1 - x0), y0 + 0.58 * (y1 - y0), z0 + 0.58 * (z1 - z0))
    arm_f0 = bd.Face(bd.Wire.make_polygon([
        (x0 - 15.0, y0, z0),
        (x0 + 15.0, y0, z0),
        (x0 + 12.0, y0, z0 + 22.0),
        (x0 - 12.0, y0, z0 + 22.0),
    ]))
    arm_f1 = bd.Face(bd.Wire.make_polygon([
        (p_mid[0] - 10.0, p_mid[1], p_mid[2]),
        (p_mid[0] + 10.0, p_mid[1], p_mid[2]),
        (p_mid[0] + 8.0, p_mid[1], p_mid[2] + 17.0),
        (p_mid[0] - 8.0, p_mid[1], p_mid[2] + 17.0),
    ]))
    arm = bd.loft([arm_f0, arm_f1], ruled=True)

    # Full-length sculpted aero wiper blade sitting tight (3 mm) above outer glass surface
    sb0 = 980.0
    xb0 = x0 + (sb0 - s0) / (s1 - s0) * (x1 - x0) - 8.0
    zb0 = spec.z_roof(sb0) + 2.0
    xb1 = x1 - 8.0
    zb1 = spec.z_roof(s1) + 2.0
    yb0, yb1 = spec.s_to_y(sb0), spec.s_to_y(s1)
    bl_f0 = bd.Face(bd.Wire.make_polygon([
        (xb0 - 11.0, yb0, zb0),
        (xb0 + 11.0, yb0, zb0),
        (xb0 + 6.0, yb0, zb0 + 15.0),
        (xb0 - 6.0, yb0, zb0 + 15.0),
    ]))
    bl_f1 = bd.Face(bd.Wire.make_polygon([
        (xb1 - 11.0, yb1, zb1),
        (xb1 + 11.0, yb1, zb1),
        (xb1 + 6.0, yb1, zb1 + 15.0),
        (xb1 - 6.0, yb1, zb1 + 15.0),
    ]))
    blade = bd.loft([bl_f0, bl_f1], ruled=True)

    wiper = pivot + [arm, blade]
    materials.apply_mat(wiper, materials.dark_charcoal_trim, "gigawiper")

    return [cowl, wiper]


def _build_triangular_side_mirrors() -> list[bd.Solid]:
    """Iconic removable angular triangular Cybertruck side mirrors spanning exactly +/-1206.5 mm (2413 mm)."""
    s_mount = spec.S_FRONT_DOOR_SEAM + 45.0   # 1530 mm (front lower corner of front door)
    y_m = spec.s_to_y(s_mount)
    z_m = spec.z_belt(s_mount) + 34.0         # 1158 mm (bold triangular silhouette visible from front & rear!)
    x_root = spec.x_belt(s_mount) + 1.5       # 986.5 mm (1.5 mm clear of stainless door outer face)
    x_tip = spec.WIDTH_INCL_MIRRORS / 2.0     # 1206.5 mm exact official overall mirror-to-mirror width!

    # Sleek forward-swept mounting stalk emerging from door corner (X = 986.5 .. 1040)
    stalk_f0 = bd.Face(bd.Wire.make_polygon([
        (x_root, y_m - 36.0, z_m - 28.0),
        (x_root, y_m + 38.0, z_m - 28.0),
        (x_root, y_m + 28.0, z_m + 14.0),
        (x_root, y_m - 24.0, z_m + 14.0),
    ]))
    stalk_f1 = bd.Face(bd.Wire.make_polygon([
        (x_root + 52.0, y_m - 12.0, z_m + 14.0),
        (x_root + 52.0, y_m + 42.0, z_m + 14.0),
        (x_root + 52.0, y_m + 36.0, z_m + 48.0),
        (x_root + 52.0, y_m - 6.0, z_m + 48.0),
    ]))
    stalk_l = bd.loft([stalk_f0, stalk_f1], ruled=True)

    # Bold Cybertruck angular triangular housing (146 mm tall inboard tapering to razor tip at x_tip=1206.5!)
    x_in = x_root + 36.0   # 1022.5 mm
    h_in = [
        (x_in, y_m - 54.0, z_m + 36.0),   # sharp forward aero nose
        (x_in, y_m + 50.0, z_m + 12.0),   # lower rear edge
        (x_in, y_m + 50.0, z_m + 158.0),  # tall crisp upper rear corner!
    ]
    h_tip = [
        (x_tip, y_m + 12.0, z_m + 54.0),  # swept-back outer tip nose
        (x_tip, y_m + 56.0, z_m + 40.0),  # outer lower corner
        (x_tip, y_m + 56.0, z_m + 78.0),  # sharp triangular outer apex!
    ]
    housing_l = geometry.ruled_loft_sections([h_in, h_tip])

    mirror_l = stalk_l + housing_l
    mirror_r = bd.mirror(mirror_l, about=bd.Plane.YZ)
    housings = mirror_l + mirror_r
    materials.apply_mat(housings, materials.matte_black_cladding, "triangular_side_mirrors")

    # Reflective silver mirror glass panes seated cleanly 1 mm behind rearward housing face
    mg_in = (x_in + 10.0, y_m + 53.0, z_m + 22.0)
    mg_top = (x_in + 10.0, y_m + 53.0, z_m + 146.0)
    mg_tip_lo = (x_tip - 12.0, y_m + 58.5, z_m + 44.0)
    mg_tip_hi = (x_tip - 12.0, y_m + 58.5, z_m + 72.0)
    glass_l = geometry.quad_slab(mg_in, mg_tip_lo, mg_tip_hi, mg_top, thickness=3.0, inward_normal_hint=(0.0, 1.0, 0.0))
    glass_r = bd.mirror(glass_l, about=bd.Plane.YZ)
    glasses = glass_l + glass_r
    materials.apply_mat(glasses, materials.mirror_glass, "side_mirror_glass")

    return [housings, glasses]


@model
def cybertruck_trim():
    """Complete Cybertruck matte-black cladding, bumpers, lower headlights, flares, tonneau, wiper, and mirrors."""
    front = _build_front_bumper_and_headlights()
    rear = _build_rear_bumper_and_diffuser()
    flares_rockers = _build_fender_flares_and_rockers()
    vault = _build_vault_tonneau_and_sail_caps()
    cowl_wiper = _build_cowl_and_gigawiper()
    mirrors = _build_triangular_side_mirrors()

    assy = bd.Compound(
        children=[*front, *rear, *flares_rockers, *vault, *cowl_wiper, *mirrors],
        label="cybertruck_trim",
    )
    bb = assy.bounding_box()
    assert abs(bb.size.Y - spec.LENGTH) < 2.0, f"Unexpected overall length: {bb.size.Y}"
    assert abs(bb.size.X - spec.WIDTH_INCL_MIRRORS) < 2.0, f"Unexpected width incl mirrors: {bb.size.X}"
    return assy


if __name__ == "__main__":
    cybertruck_trim()
