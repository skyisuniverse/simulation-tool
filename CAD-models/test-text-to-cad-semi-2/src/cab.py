"""Sculpted Class-A aerodynamic cab, bumper, headlights, mirrors & trim for the original Tesla Semi.

Builds the iconic original 2017/2022 Tesla Semi exterior with zero part overlaps:
  - Seamless metallic-silver bullet cab & 13-ft sweeping parabolic aero roof fairing
  - Sculpted matte-obsidian composite front bumper with trapezoidal intake, radar, slats & air curtains
  - Signature original swept stealth-blade LED headlight pods (curved DRL + triple projectors + amber)
  - 3D sculpted Tesla "T" nose emblem & 5 amber DOT clearance lights
  - Recessed two-step entry pockets with non-slip aluminum step treads & dark pocket liners
  - Flush front wheel arch lip moldings, flush Tesla door handles, MCS Megacharger port & side markers
  - Streamlined aerodynamic dual-arm wing side mirrors with reflective glass & Autopilot camera pods
  - Twin windshield wipers, conforming curved rear aero edge seal & rear bulkhead work light
"""

import math
import build123d as bd
from bd_materials import metals, plastics
from cad import model
from cad.build123d import closest_points

import dims as D
import cab_surface as CS
from cab_shell_lib import (
    build_cab_envelope,
    build_side_window_aperture,
    build_windshield_aperture,
)

# Wheel arch cutout radius (26 mm wider than tire arch opening to host flush black arch lip!)
ARCH_CUT_R = D.FRONT_ARCH_R + 26.0  # 641.0 mm


def _body_silver(part):
    part.material = metals.aluminum()
    part.material.pbr = part.material.pbr.override(
        roughness=0.22, metalness=0.82, clearcoat=0.9, clearcoat_roughness=0.08
    )
    part.color = D.COLOR_BODY_SILVER
    return part


def _dark_composite(part, color=D.COLOR_BUMPER_DARK, roughness=0.48, metalness=0.08):
    part.material = plastics.abs_()
    part.material.pbr = part.material.pbr.override(roughness=roughness, metalness=metalness)
    part.color = color
    return part


def _gloss_black(part, color=D.COLOR_TRIM_BLACK, roughness=0.16, metalness=0.1):
    part.material = plastics.abs_()
    part.material.pbr = part.material.pbr.override(
        roughness=roughness, metalness=metalness, clearcoat=0.85, clearcoat_roughness=0.1
    )
    part.color = color
    return part


def _chrome(part, color=D.COLOR_CHROME, roughness=0.14, metalness=0.96):
    part.material = metals.stainless()
    part.material.pbr = part.material.pbr.override(roughness=roughness, metalness=metalness)
    part.color = color
    return part


def _emissive(part, color, rgb_lin, intensity=2.4):
    part.material = plastics.pmma()
    part.material.pbr = part.material.pbr.override(
        roughness=0.12, emissive=rgb_lin, emissive_intensity=intensity
    )
    part.color = color
    return part


def _max_outer_x(outer, sgn, ys, zs):
    """Return exact maximum |X| of `outer` sampled over a small patch of (Y, Z) points."""
    mx = 0.0
    for y in ys:
        for z in zs:
            pt = closest_points(bd.Vertex(sgn * 1650.0, y, z), outer).point_b
            mx = max(mx, abs(pt.X))
    return mx


def _make_headlight_recess_tools():
    """Left & right sleek swept-blade cutting volumes hugging the outer front fender cheeks."""
    tools = []
    for sgn in (1.0, -1.0):
        with bd.BuildSketch(bd.Plane.YZ) as sk:
            with bd.BuildLine():
                bd.Polyline(
                    (282.0, 825.0),
                    (472.0, 825.0),
                    (740.0, 1182.0),
                    (662.0, 1240.0),
                    close=True,
                )
            bd.make_face()
        # Start cleanly outboard at |X| = 965 so zero inboard sliver cuts into the center silver nose
        x0 = 965.0 if sgn > 0 else -1315.0
        pod = bd.Pos(x0, 0.0, 0.0) * bd.extrude(sk.sketch.face(), amount=350.0, dir=(1, 0, 0))
        tools.append(pod)
    return tools


def _make_main_cab_shell():
    """Carve the hollow aerodynamic metallic-silver cab shell from the Class-A outer loft."""
    outer = build_cab_envelope(0.0)
    inner = build_cab_envelope(68.0)

    # 1. Hollow cockpit interior cavity (Y = 920 .. 3485, Z = 1138 .. 2780)
    cabin_box = bd.Pos(0.0, 2202.0, 1960.0) * bd.Box(2600.0, 2565.0, 1645.0)
    cabin_cavity = inner & cabin_box

    # 2. Under-floor chassis & battery tunnel (|X| < 948, Z < 1142, Y >= 420)
    chassis_tunnel = bd.Pos(0.0, 2230.0, 560.0) * bd.Box(1896.0, 3660.0, 1164.0)

    # 3. Split off lower front bumper zone (Y < 715, Z < 812) for separate matte-black bumper
    bumper_split = bd.Pos(0.0, 325.0, 406.0) * bd.Box(2800.0, 780.0, 812.0)

    # 4. Sculpted front steer wheel well cutouts (R = ARCH_CUT_R to host flush black arch lip!)
    wheel_wells = []
    for sgn in (1.0, -1.0):
        ww = (
            bd.Pos(sgn * 1118.0, D.Y_FRONT_AXLE, D.TIRE_R)
            * bd.Rot(0, 90, 0)
            * bd.Cylinder(ARCH_CUT_R, 566.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.CENTER))
        )
        ww_bot = (
            bd.Pos(sgn * 1118.0, D.Y_FRONT_AXLE, D.TIRE_R / 2.0 - 40.0)
            * bd.Box(566.0, ARCH_CUT_R * 2.0, D.TIRE_R + 80.0)
        )
        wheel_wells.append(ww + ww_bot)

    # 5. Deep rear aerodynamic cab-extender C-channel pocket (Y = 3560 .. 4050)
    rear_pocket = bd.Pos(0.0, 3810.0, 1980.0) * bd.Box(2220.0, 500.0, 3440.0)

    # 6. Recessed two-step entry pockets beneath both mid-cab doors (inward to |X| = 1020)
    step_pockets = []
    for sgn in (1.0, -1.0):
        pkt = (
            bd.Pos(sgn * 1180.0, (D.STEP_Y_FRONT + D.STEP_Y_REAR) / 2.0, 692.0)
            * bd.Box(320.0, D.STEP_Y_REAR - D.STEP_Y_FRONT, 706.0)
        )
        step_pockets.append(pkt)

    # 7. Panoramic windshield & helmet-visor side window openings
    ws_cut = build_windshield_aperture(0.0)
    sw_cut = build_side_window_aperture(0.0)

    # 8. Contoured recessed front cheek pockets for the original vertical LED headlights
    hl_cuts = _make_headlight_recess_tools()

    shell = outer - [bumper_split, chassis_tunnel, rear_pocket]
    shell = shell - wheel_wells
    shell = shell - [cabin_cavity, ws_cut, sw_cut]
    shell = shell - step_pockets

    hl_skin = outer - build_cab_envelope(24.0)
    hl_recesses = [hl_skin & pod for pod in hl_cuts]
    hl_recesses = [r for r in hl_recesses if r is not None and len(r.solids()) > 0]
    assert len(hl_recesses) == 2, f"Expected 2 headlight recesses, got {len(hl_recesses)}"
    shell = shell - hl_recesses

    shell.label = "cab_monocoque"
    return _body_silver(shell)


def _make_front_bumper():
    """Sculpted matte-obsidian composite front bumper, trapezoidal cooling grille & chin air dam."""
    parts = []
    outer = build_cab_envelope(0.0)

    bumper_vol = bd.Pos(0.0, 325.0, 404.0) * bd.Box(2800.0, 772.0, 808.0)
    bumper = outer & bumper_vol

    clear_cuts = [
        bd.Pos(0.0, 610.0, 540.0) * bd.Box(1900.0, 320.0, 620.0),
    ]
    for sgn in (1.0, -1.0):
        clear_cuts.append(
            bd.Pos(sgn * 1118.0, D.Y_FRONT_AXLE, D.TIRE_R)
            * bd.Rot(0, 90, 0)
            * bd.Cylinder(ARCH_CUT_R, 580.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.CENTER))
        )

    # Recessed wide trapezoidal central cooling intake opening on front face (Z = 340 .. 585)
    with bd.BuildSketch(bd.Plane.XZ) as isk:
        with bd.BuildLine():
            bd.Polyline(
                (-480.0, 340.0),
                (480.0, 340.0),
                (555.0, 585.0),
                (-555.0, 585.0),
                close=True,
            )
        bd.make_face()
    intake_cut = bd.Pos(0.0, -50.0, 0.0) * bd.extrude(isk.sketch.face(), amount=320.0, dir=(0, 1, 0))
    clear_cuts.append(intake_cut)

    # Flanking vertical aerodynamic cheek air-curtain slots (left & right lower bumper corners)
    for sgn in (1.0, -1.0):
        cheek_slot = (
            bd.Pos(sgn * 805.0, 145.0, 520.0)
            * bd.Rot(0, 0, sgn * 22.0)
            * bd.Box(145.0, 260.0, 285.0)
        )
        clear_cuts.append(cheek_slot)

    bumper = bumper - clear_cuts
    bumper.label = "front_bumper"
    parts.append(_dark_composite(bumper, color=D.COLOR_BUMPER_DARK, roughness=0.45))

    # Center forward Autopilot radar sensor dome centered in intake
    radar = bd.Pos(0.0, 108.0, 468.0) * bd.Box(150.0, 32.0, 125.0)
    radar.label = "front_autopilot_radar"
    parts.append(_gloss_black(radar, color="#121418", roughness=0.14))

    # Crisp horizontal aerodynamic intake grille louver slats (notched cleanly around Autopilot radar!)
    radar_clear = bd.Pos(0.0, 114.0, 468.0) * bd.Box(162.0, 70.0, 134.0)
    for idx, gz in enumerate((382.0, 440.0, 498.0, 552.0)):
        gw = 920.0 + idx * 35.0
        slat = bd.Pos(0.0, 125.0, gz) * bd.Box(gw, 40.0, 14.0)
        slat = slat - radar_clear
        slat.label = f"bumper_grille_slat_{idx + 1}"
        parts.append(_gloss_black(slat, color="#171A1F", roughness=0.35))

    # Front license plate mount seated cleanly 3 mm ahead of curved front bumper face
    y_plate = min(
        closest_points(bd.Vertex(px, -80.0, pz), bumper).point_b.Y
        for px in (-155.0, 0.0, 155.0)
        for pz in (620.0, 692.0, 762.0)
    )
    plate_pad = bd.Pos(0.0, y_plate - 9.0, 692.0) * bd.Box(310.0, 10.0, 148.0)
    plate_pad.label = "front_license_plate"
    parts.append(_dark_composite(plate_pad, color="#D8DDE4", roughness=0.35))

    return bd.Compound(children=parts, label="front_bumper_assembly")


def _make_headlights():
    """Iconic original 2017/2022 Tesla Semi swept stealth-blade LED headlight pods (left & right).

    Every optical element is strictly disjoint inside the carved 24 mm recess:
      - Gloss-black housing: inset 12..22 (2 mm clear of recess floor & 8 mm inside perimeter)
      - White LED DRL blade: inset 2.5..9.5 inside shrunk_pod
      - Triple LED projectors: inset 2.5..9.5 inside shrunk_pod minus expanded DRL & amber masks
      - Upper amber LED corner marker: inset 2.5..9.5 inside shrunk_pod minus expanded DRL mask
    """
    parts = []
    housing_skin = build_cab_envelope(12.0) - build_cab_envelope(22.0)
    led_skin = build_cab_envelope(2.5) - build_cab_envelope(9.5)

    for side, sgn in (("left", 1.0), ("right", -1.0)):
        with bd.BuildSketch(bd.Plane.YZ) as hsk:
            with bd.BuildLine():
                bd.Polyline(
                    (294.0, 833.0),
                    (463.0, 833.0),
                    (729.0, 1181.0),
                    (664.0, 1230.0),
                    close=True,
                )
            bd.make_face()
        # Keep 10 mm clear inboard of recess wall (965 -> 975)
        x0 = 975.0 if sgn > 0 else -1310.0
        shrunk_pod = bd.Pos(x0, 0.0, 0.0) * bd.extrude(hsk.sketch.face(), amount=335.0, dir=(1, 0, 0))

        # 1. Contoured gloss-black inner housing
        housing = housing_skin & shrunk_pod
        assert housing is not None and len(housing.solids()) > 0, f"Empty headlight housing {side}"
        housing.label = f"headlight_housing_{side}"
        parts.append(_gloss_black(housing, color="#12151A", roughness=0.14))

        # 2. Sweeping boomerang white LED DRL blade
        with bd.BuildSketch(bd.Plane.YZ) as dsk:
            with bd.BuildLine():
                bd.Polyline(
                    (304.0, 840.0),
                    (458.0, 840.0),
                    (668.0, 1118.0),
                    (644.0, 1134.0),
                    (442.0, 868.0),
                    (320.0, 868.0),
                    close=True,
                )
            bd.make_face()
        drl_vol = bd.Pos(x0, 0.0, 0.0) * bd.extrude(dsk.sketch.face(), amount=335.0, dir=(1, 0, 0))
        # Expanded guard band around DRL so projectors & amber never graze it
        with bd.BuildSketch(bd.Plane.YZ) as dsk_pad:
            with bd.BuildLine():
                bd.Polyline(
                    (294.0, 830.0),
                    (466.0, 830.0),
                    (678.0, 1114.0),
                    (634.0, 1146.0),
                    (436.0, 878.0),
                    (312.0, 878.0),
                    close=True,
                )
            bd.make_face()
        drl_guard = bd.Pos(x0 - 5.0, 0.0, 0.0) * bd.extrude(dsk_pad.sketch.face(), amount=345.0, dir=(1, 0, 0))

        drl = (led_skin & shrunk_pod) & drl_vol
        assert drl is not None and len(drl.solids()) > 0, f"Empty headlight DRL {side}"
        drl.label = f"headlight_drl_{side}"
        parts.append(_emissive(drl, D.COLOR_LED_WHITE, (0.95, 0.98, 1.0), intensity=3.2))

        # 3. Upper outer trailing amber LED corner marker (strictly clear of DRL guard)
        with bd.BuildSketch(bd.Plane.YZ) as ask:
            with bd.BuildLine():
                bd.Polyline(
                    (646.0, 1152.0),
                    (686.0, 1132.0),
                    (724.0, 1182.0),
                    (670.0, 1222.0),
                    close=True,
                )
            bd.make_face()
        amber_vol = bd.Pos(x0, 0.0, 0.0) * bd.extrude(ask.sketch.face(), amount=335.0, dir=(1, 0, 0))
        amber = ((led_skin & shrunk_pod) & amber_vol) - drl_guard
        assert amber is not None and len(amber.solids()) > 0, f"Empty amber marker {side}"
        amber.label = f"headlight_amber_{side}"
        parts.append(_emissive(amber, D.COLOR_LED_AMBER, (1.0, 0.52, 0.0), intensity=2.2))

        # 4. Three stacked crystalline LED projector pods strictly inside shrunk_pod & clear of DRL/amber
        proj_cyls = []
        for py, pz in (
            (402.0, 938.0),
            (494.0, 1026.0),
            (584.0, 1112.0),
        ):
            c = (
                bd.Pos(sgn * 1095.0, py, pz)
                * bd.Rot(0.0, 90.0, 0.0)
                * bd.Cylinder(29.0, 410.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.CENTER))
            )
            proj_cyls.append(c)
        proj_region = (shrunk_pod - drl_guard) - amber_vol
        projectors = (led_skin & proj_region) & bd.Compound(children=proj_cyls)
        assert projectors is not None and len(projectors.solids()) > 0, f"Empty projectors {side}"
        projectors.label = f"headlight_projectors_{side}"
        parts.append(_emissive(projectors, "#E8F2FF", (0.88, 0.94, 1.0), intensity=2.6))

    return bd.Compound(children=parts, label="headlights")


def _make_tesla_badge_and_markers():
    """Sculpted 3D Tesla 'T' emblem on bullet nose + 5 DOT clearance lights + flush wipers."""
    parts = []
    outer = build_cab_envelope(0.0)

    # --- 1. Sculpted 3D Tesla 'T' Emblem seated cleanly proud of center bullet nose ---
    y_b = 355.0
    slope = CS.nose_slope_deg(y_b)
    rad = math.radians(slope)
    ny, nz = -math.sin(rad), math.cos(rad)
    # Query exact surface point on nose centerline via closest_points
    pt_b = closest_points(bd.Vertex(0.0, y_b + ny * 300.0, CS.z_top_at(y_b) + nz * 300.0), outer).point_b

    with bd.BuildSketch(bd.Plane.XY) as t_top_sk:
        with bd.BuildLine():
            bd.ThreePointArc((-102.0, 76.0), (0.0, 96.0), (102.0, 76.0))
            bd.Line((102.0, 76.0), (94.0, 61.0))
            bd.ThreePointArc((94.0, 61.0), (0.0, 79.0), (-94.0, 61.0))
            bd.Line((-94.0, 61.0), (-102.0, 76.0))
        bd.make_face()
    top_bar = bd.extrude(t_top_sk.sketch.face(), amount=10.0, dir=(0, 0, 1))

    with bd.BuildSketch(bd.Plane.XY) as t_stem_sk:
        with bd.BuildLine():
            bd.Polyline(
                (-82.0, 48.0),
                (-20.0, 60.0),
                (0.0, 42.0),
                (20.0, 60.0),
                (82.0, 48.0),
                (65.0, 30.0),
                (22.0, 35.0),
                (0.0, -108.0),
                (-22.0, 35.0),
                (-65.0, 30.0),
                close=True,
            )
        bd.make_face()
    stem = bd.extrude(t_stem_sk.sketch.face(), amount=10.0, dir=(0, 0, 1))
    badge_raw = top_bar + stem

    # Advance badge along outward nose normal until guaranteed >= 1.5 mm clear of convex nose skin
    badge = None
    for off in (14.0, 18.0, 22.0, 26.0, 30.0, 36.0, 42.0):
        cand = (
            bd.Pos(0.0, pt_b.Y + ny * off, pt_b.Z + nz * off)
            * bd.Rot(slope - 3.0, 0.0, 0.0)
            * badge_raw
        )
        if closest_points(cand, outer).distance >= 1.5:
            badge = cand
            break
    assert badge is not None, "Could not place nose emblem clear of cab nose"
    badge.label = "tesla_nose_emblem"
    parts.append(_gloss_black(badge, color="#262B32", roughness=0.16, metalness=0.85))

    # --- 2. Five DOT Amber Roof Clearance / Identification Marker Lights above windshield ---
    y_m = 1915.0
    m_slope = CS.nose_slope_deg(y_m)
    m_rad = math.radians(m_slope)
    mny, mnz = -math.sin(m_rad), math.cos(m_rad)
    marker_xs = (-620.0, -145.0, 0.0, 145.0, 620.0)
    for idx, mx in enumerate(marker_xs):
        probe = bd.Vertex(mx, y_m + mny * 400.0, CS.z_top_at(y_m) + mnz * 400.0)
        pt_m = closest_points(probe, outer).point_b
        # Place lens box cleanly 12 mm proud along roof normal so outer corners never dip into curved roof
        m_pos = bd.Pos(mx, pt_m.Y + mny * 14.0, pt_m.Z + mnz * 14.0) * bd.Rot(m_slope, 0.0, 0.0)
        lens = m_pos * bd.Box(74.0, 30.0, 14.0)
        lens.label = f"dot_clearance_light_{idx + 1}"
        parts.append(_emissive(lens, D.COLOR_LED_AMBER, (1.0, 0.55, 0.0), intensity=2.4))

    # --- 3. Twin Articulated Heavy-Duty Windshield Wipers tucked cleanly at windshield base ---
    y_w = 805.0
    z_w = CS.z_top_at(y_w)
    w_slope = CS.nose_slope_deg(y_w)
    w_rad = math.radians(w_slope)
    wny, wnz = -math.sin(w_rad), math.cos(w_rad)
    for side, sgn in (("left", 1.0), ("right", -1.0)):
        w_frame = (
            bd.Pos(sgn * 340.0, y_w + wny * 4.0, z_w + wnz * 4.0)
            * bd.Rot(w_slope, 0.0, -sgn * 4.0)
        )
        blade = w_frame * bd.Box(590.0, 20.0, 14.0)
        arm = (
            bd.Pos(sgn * 120.0, y_w - 22.0 + wny * 4.0, z_w - 22.0 + wnz * 4.0)
            * bd.Rot(w_slope, 0.0, sgn * 8.0)
            * bd.Box(220.0, 16.0, 12.0)
        )
        wiper = blade + arm
        wiper.label = f"windshield_wiper_{side}"
        parts.append(_dark_composite(wiper, color=D.COLOR_TRIM_BLACK, roughness=0.55))

    return bd.Compound(children=parts, label="nose_emblem_and_markers")


def _make_steps_handles_and_trim():
    """Recessed entry step treads, flush wheel arch moldings, door handles & conforming aero seal."""
    parts = []
    outer = build_cab_envelope(0.0)

    for side, sgn in (("left", 1.0), ("right", -1.0)):
        y_mid_step = (D.STEP_Y_FRONT + D.STEP_Y_REAR) / 2.0
        step_len = (D.STEP_Y_REAR - D.STEP_Y_FRONT) - 18.0

        # Back dark textured step-well liner panel seated cleanly inside pocket (pocket goes inward to 1020)
        liner = (
            bd.Pos(sgn * 1034.0, y_mid_step, 692.0)
            * bd.Box(16.0, step_len, 686.0)
        )
        liner.label = f"step_pocket_liner_{side}"
        parts.append(_dark_composite(liner, color=D.COLOR_TRIM_BLACK, roughness=0.68))

        # Lower & upper brushed non-slip metallic step treads (clear outboard of liner at |X| = 1044)
        for lvl, sz in (("lower", 435.0), ("upper", 755.0)):
            tread = (
                bd.Pos(sgn * 1126.0, y_mid_step, sz)
                * bd.Box(146.0, step_len, 26.0)
            )
            tread.label = f"entry_step_{lvl}_{side}"
            tread.material = metals.aluminum()
            tread.material.pbr = tread.material.pbr.override(roughness=0.42, metalness=0.82)
            tread.color = "#8E96A0"
            parts.append(tread)

        # Signature flush Tesla door handle seated cleanly 2 mm proud of exact outer NURBS skin
        xh = _max_outer_x(outer, sgn, (2720.0, 2810.0, 2900.0), (1460.0, 1480.0, 1500.0))
        handle = bd.Pos(sgn * (xh + 7.0), 2810.0, 1480.0) * bd.Box(10.0, 175.0, 34.0)
        handle.label = f"flush_door_handle_{side}"
        parts.append(_chrome(handle, color=D.COLOR_CHROME, roughness=0.18))

        # Crisp black vertical door shutline reveal trim seated cleanly 2 mm proud of outer skin
        for edge_name, dy in (("front", D.DOOR_Y_FRONT), ("rear", D.DOOR_Y_REAR)):
            xd = _max_outer_x(outer, sgn, (dy,), (1080.0, 1285.0, 1490.0))
            seam = bd.Pos(sgn * (xd + 4.5), dy, 1285.0) * bd.Box(4.0, 7.0, 420.0)
            seam.label = f"door_seam_{edge_name}_{side}"
            parts.append(_dark_composite(seam, color=D.COLOR_TRIM_BLACK, roughness=0.5))

        # Amber DOT side marker / turn repeater lights along the lower aero side skirt
        for idx, my in enumerate((1945.0, 3760.0)):
            xm = _max_outer_x(outer, sgn, (my - 45.0, my, my + 45.0), (450.0, 465.0, 480.0))
            sm = bd.Pos(sgn * (xm + 6.5), my, 465.0) * bd.Box(9.0, 92.0, 26.0)
            sm.label = f"side_marker_{idx + 1}_{side}"
            parts.append(_emissive(sm, D.COLOR_LED_AMBER, (1.0, 0.55, 0.0), intensity=2.0))

        # OEM flush matte-black front wheel arch fender lip molding (R = 615..639, 2 mm clear of R=641 cut!)
        with bd.BuildSketch(bd.Plane.YZ) as arch_sk:
            with bd.BuildLine():
                pts_o, pts_i = [], []
                for k in range(19):
                    ang = math.radians(-10.0 + 200.0 * (k / 18.0))
                    pts_o.append((D.Y_FRONT_AXLE + 639.0 * math.cos(ang), D.TIRE_R + 639.0 * math.sin(ang)))
                    pts_i.append((D.Y_FRONT_AXLE + 615.0 * math.cos(ang), D.TIRE_R + 615.0 * math.sin(ang)))
                bd.Spline(*pts_o)
                bd.Line(pts_o[-1], pts_i[-1])
                bd.Spline(*list(reversed(pts_i)))
                bd.Line(pts_i[0], pts_o[0])
            bd.make_face()
        x_ring = 960.0 if sgn > 0 else -1360.0
        arch_ring = bd.Pos(x_ring, 0.0, 0.0) * bd.extrude(arch_sk.sketch.face(), amount=400.0, dir=(1, 0, 0))
        lip = outer & arch_ring
        lip = lip - bd.Pos(sgn * 1160.0, D.Y_FRONT_AXLE, 148.0) * bd.Box(500.0, 1500.0, 300.0)
        lip.label = f"front_wheel_arch_lip_{side}"
        parts.append(_dark_composite(lip, color=D.COLOR_BUMPER_DARK, roughness=0.52))

    # Conforming matte-black flexible rubber aero edge seal following EXACT curved rear cab contour!
    # 24 mm thick at Y = 3962..3986 (2 mm clear behind cab 3960 & 8 mm clear ahead of quarter fender 3994!)
    rear_slice_box = bd.Pos(0.0, D.CAB_EXTENDER_Y - 12.0, 2130.0) * bd.Box(2650.0, 24.0, 3700.0)
    rear_inner_cut = bd.Pos(0.0, D.CAB_EXTENDER_Y - 12.0, 1980.0) * bd.Box(2310.0, 100.0, 3540.0)
    aero_seal = bd.Pos(0.0, 26.0, 0.0) * ((outer & rear_slice_box) - rear_inner_cut)
    aero_seal.label = "rear_cab_aero_seal"
    parts.append(_dark_composite(aero_seal, color=D.COLOR_TRIM_BLACK, roughness=0.78))

    # Left-side (+X) MCS Megacharger port door seated cleanly 2 mm proud of exact outer skin
    xmcs = _max_outer_x(outer, 1.0, (3105.0, 3250.0, 3395.0), (835.0, 960.0, 1085.0))
    mcs_port = bd.Pos(xmcs + 4.5, 3250.0, 960.0) * bd.Box(5.0, 290.0, 250.0)
    mcs_port.label = "megacharger_port_door"
    parts.append(_dark_composite(mcs_port, color="#2D323A", roughness=0.35))

    # Rear cab bulkhead high-mount LED work light overlooking catwalk & fifth wheel
    work_light = bd.Pos(0.0, D.CAB_BULKHEAD_Y + 14.0, 2720.0) * bd.Box(260.0, 22.0, 56.0)
    work_light.label = "rear_cab_work_light"
    parts.append(_emissive(work_light, D.COLOR_LED_WHITE, (0.95, 0.97, 1.0), intensity=2.0))

    return bd.Compound(children=parts, label="steps_handles_and_trim")


def _make_side_mirrors():
    """Streamlined original production Tesla Semi dual-arm wing side mirrors & Autopilot camera pods."""
    parts = []
    outer = build_cab_envelope(0.0)

    for side, sgn in (("left", 1.0), ("right", -1.0)):
        # Anchor cleanly 4 mm outboard of solid A-pillar & fuse stalks into mirror housing (zero overlaps!)
        y_hi, z_hi = 1715.0, 2135.0
        y_lo, z_lo = 1485.0, 1745.0
        x_root_hi = _max_outer_x(outer, sgn, (y_hi - 20.0, y_hi, y_hi + 20.0), (z_hi - 20.0, z_hi, z_hi + 20.0))
        x_root_lo = _max_outer_x(outer, sgn, (y_lo - 20.0, y_lo, y_lo + 20.0), (z_lo - 20.0, z_lo, z_lo + 20.0))
        x_head = 1485.0
        y_head = 1495.0

        # Route upper & lower airfoil stalks into the FRONT-inner side of the mirror housing
        # (well ahead of the rear-facing mirror glass panes at local Y = +40.5!)
        stalk_hi_path = bd.Spline(
            (sgn * (x_root_hi + 16.0), y_hi, z_hi),
            (sgn * (x_head - 145.0), y_head - 24.0, 2160.0),
            (sgn * (x_head - 35.0), y_head - 28.0, 2175.0),
        )
        prof_hi = bd.Plane(origin=stalk_hi_path @ 0, z_dir=stalk_hi_path % 0) * bd.Ellipse(22.0, 11.0)
        stalk_hi = bd.sweep(prof_hi, path=stalk_hi_path)

        stalk_lo_path = bd.Spline(
            (sgn * (x_root_lo + 16.0), y_lo, z_lo),
            (sgn * (x_head - 145.0), y_head - 24.0, 1790.0),
            (sgn * (x_head - 35.0), y_head - 28.0, 1805.0),
        )
        prof_lo = bd.Plane(origin=stalk_lo_path @ 0, z_dir=stalk_lo_path % 0) * bd.Ellipse(22.0, 11.0)
        stalk_lo = bd.sweep(prof_lo, path=stalk_lo_path)

        # Tall aerodynamic vertical mirror housing fused seamlessly with both airfoil stalks
        mirror_frame = bd.Pos(sgn * x_head, y_head - 10.0, 1990.0) * bd.Rot(0.0, 0.0, -sgn * 8.0)
        head = mirror_frame * bd.Box(182.0, 74.0, 482.0)
        head = head.fillet(22.0, head.edges().filter_by(bd.Axis.Z))
        mirror_body = head + stalk_hi + stalk_lo
        mirror_body.label = f"mirror_housing_{side}"
        parts.append(_gloss_black(mirror_body, color=D.COLOR_TRIM_BLACK, roughness=0.22))

        # Main & spotter mirror glass panes placed in mirror_frame (+40 mm local Y => 1 mm clear of 37 mm back!)
        glass_main = mirror_frame * bd.Pos(0.0, 40.5, 63.0) * bd.Box(150.0, 4.0, 310.0)
        glass_main.label = f"mirror_glass_main_{side}"
        glass_main.material = metals.silver()
        glass_main.material.pbr = glass_main.material.pbr.override(roughness=0.04, metalness=0.98)
        glass_main.color = D.COLOR_GLASS_MIRROR
        parts.append(glass_main)

        glass_spot = mirror_frame * bd.Pos(0.0, 40.5, -167.0) * bd.Box(150.0, 4.0, 118.0)
        glass_spot.label = f"mirror_glass_spotter_{side}"
        glass_spot.material = metals.silver()
        glass_spot.material.pbr = glass_spot.material.pbr.override(roughness=0.05, metalness=0.98)
        glass_spot.color = D.COLOR_GLASS_MIRROR
        parts.append(glass_spot)

        # Forward-facing amber LED mirror turn-signal strip (-40.5 mm local Y => clear of -37 mm front!)
        sig = mirror_frame * bd.Pos(0.0, -40.5, 0.0) * bd.Box(128.0, 4.0, 22.0)
        sig.label = f"mirror_turn_signal_{side}"
        parts.append(_emissive(sig, D.COLOR_LED_AMBER, (1.0, 0.55, 0.0), intensity=2.2))

        # Sleek lower Autopilot side-repeater camera pod mounted cleanly proud of front fender flank
        xc = _max_outer_x(outer, sgn, (1715.0, 1790.0, 1865.0), (1250.0, 1280.0, 1310.0))
        cam_pod = bd.Pos(sgn * (xc + 24.0), 1790.0, 1280.0) * bd.Box(44.0, 145.0, 52.0)
        cam_pod.label = f"autopilot_camera_pod_{side}"
        parts.append(_gloss_black(cam_pod, color=D.COLOR_TRIM_BLACK, roughness=0.2))

    return bd.Compound(children=parts, label="side_mirrors")


@model
def cab():
    """Complete sculpted aerodynamic original Tesla Semi cab, bumper, headlights & mirrors."""
    children = [
        _make_main_cab_shell(),
        _make_front_bumper(),
        _make_headlights(),
        _make_tesla_badge_and_markers(),
        _make_steps_handles_and_trim(),
        _make_side_mirrors(),
    ]
    asm = bd.Compound(children=children, label="cab")
    bb = asm.bounding_box()
    assert abs(bb.max.Z - D.TOTAL_HEIGHT) < 25.0, f"Cab height mismatch: {bb.max.Z}"
    return asm


if __name__ == "__main__":
    cab()
