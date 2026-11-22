"""SpaceX Starship Upper Stage (Block 1 / Flight 5 configuration, 50.3 m tall, 9.0 m diameter).

Exports:
- `aft_flap_stbd`, `aft_flap_port`: Tapered stainless + black-TPS aft aerodynamic flaps.
- `fwd_flap_stbd`, `fwd_flap_port`: Tapered stainless + black-TPS forward nosecone flaps.
- `starship_core`: Rigid spacecraft body (304L stainless leeward hull + G1 tangent ogive,
  matte-black ceramic TPS windward hull & 360° stagnation nose cap, circular thrust deck,
  3 Raptor SL + 3 Raptor Vacuum engines, 4 hinge aero-covers & clevises, catch pins,
  raceway, Starlink payload bay door, and RCS pods).
- `starship`: Complete Starship Upper Stage with all 4 articulated aerodynamic flaps.
"""

import math

import build123d as bd
from cad import model
from cad.build123d import mechanism_state, memo

from lib import dims
from lib.materials import (
    apply_dark_trim,
    apply_grid_fin_steel,
    apply_hot_stage_shield,
    apply_stainless_304l,
    apply_stainless_structural,
    apply_tps_ceramic,
)
from raptor import raptor_sl, raptor_vac


def _arc_mid_on_circle(cx: float, cz: float, radius: float, p0: tuple[float, float], p1: tuple[float, float]):
    """Exact midpoint along the shorter circular arc between p0 and p1 centered at (cx, cz)."""
    a0 = math.atan2(p0[1] - cz, p0[0] - cx)
    a1 = math.atan2(p1[1] - cz, p1[0] - cx)
    da = (a1 - a0 + math.pi) % (2.0 * math.pi) - math.pi
    am = a0 + 0.5 * da
    return (cx + radius * math.cos(am), cz + radius * math.sin(am))


@memo
def _build_starship_hull_and_tps():
    """Build Starship's 304L leeward hull, windward ceramic TPS belly, 360° nose cap, and thrust deck.

    The leeward stainless half (Y >= 0) and windward ceramic TPS half (Y <= 0) meet cleanly on the flat
    Y = 0 meridian plane and Z = 119,500 mm cap plane rather than overlapping as nested thin shells,
    eliminating coarse-mesh bleed-through while keeping a crisp 55 mm physical TPS tile step along ±X.
    """
    r_steel = dims.HULL_R
    r_tps = dims.HULL_R + dims.TPS_THICKNESS
    r_in = dims.SHIP_SKIRT_IN_R
    z_bot = dims.Z_SHIP_BOT
    z_deck = dims.Z_SHIP_THRUST_DECK       # 75,400.0 mm
    z_deck_top = z_deck + 400.0            # 75,800.0 mm
    z_puck = dims.Z_SHIP_SL_EXIT + dims.RAPTOR_SL_HEIGHT  # 74,900.0 mm
    r_puck = 1520.0
    z_nose0 = dims.Z_NOSE_BASE
    z_cap_split = dims.Z_TPS_FULL_CAP      # 119,500.0 mm

    r_steel_split = dims.nose_radius_at_z(z_cap_split, outer_tps=False)
    r_tps_split = dims.nose_radius_at_z(z_cap_split, outer_tps=True)

    # 1. Uniform 360° Aft Engine Thrust Deck & Central SL Thrust Puck (Z = 74,900 .. 75,800, R <= 4400)
    with bd.BuildSketch(bd.Plane.XZ) as deck_sk:
        bd.Polygon(
            (0.0, z_puck),
            (r_puck, z_puck),
            (r_puck, z_deck),
            (r_in, z_deck),
            (r_in, z_deck_top),
            (0.0, z_deck_top),
            align=None,
        )
    thrust_deck = bd.revolve(deck_sk.sketch, axis=bd.Axis.Z, revolution_arc=360)
    thrust_deck.label = "ship_thrust_deck"
    apply_hot_stage_shield(thrust_deck)

    # 2. Leeward 180° 304L Stainless Steel Hull (Y >= 0, Z = 71,000 .. 119,500)
    p_s_sh = (r_steel, z_nose0)
    p_s_sp = (r_steel_split, z_cap_split)
    mid_s_og = _arc_mid_on_circle(
        dims.NOSE_OGIVE_CX, z_nose0, dims.NOSE_OGIVE_RHO_STEEL, p_s_sh, p_s_sp
    )

    groove_d = dims.WELD_GROOVE_DEPTH
    groove_hh = dims.WELD_GROOVE_HALF_H
    seam_zs = []
    z_s = z_bot + 4500.0
    while z_s <= z_nose0 - 2000.0:
        seam_zs.append(z_s)
        z_s += dims.RING_STEP

    with bd.BuildSketch(bd.Plane.XZ) as steel_sk:
        with bd.BuildLine():
            bd.Line((r_in, z_bot), (r_steel, z_bot))
            prev = (r_steel, z_bot)
            for zc in seam_zs:
                p1 = (r_steel, zc - groove_hh)
                p2 = (r_steel - groove_d, zc)
                p3 = (r_steel, zc + groove_hh)
                bd.Line(prev, p1)
                bd.Line(p1, p2)
                bd.Line(p2, p3)
                prev = p3
            bd.Line(prev, p_s_sh)
            bd.ThreePointArc(p_s_sh, mid_s_og, p_s_sp)
            bd.Line(p_s_sp, (0.0, z_cap_split))
            bd.Line((0.0, z_cap_split), (0.0, z_deck_top))
            bd.Line((0.0, z_deck_top), (r_in, z_deck_top))
            bd.Line((r_in, z_deck_top), (r_in, z_bot))
        bd.make_face()

    steel_hull = bd.revolve(steel_sk.sketch, axis=bd.Axis.Z, revolution_arc=180)
    steel_hull.label = "starship_steel_hull"
    apply_stainless_304l(steel_hull)

    # 3. Windward 180° Matte-Black Ceramic TPS Hull (Y <= 0, Z = 71,000 .. 119,500, R_outer = R_steel + 55)
    p_t_sh = (r_tps, z_nose0)
    p_t_sp = (r_tps_split, z_cap_split)
    mid_t_og = _arc_mid_on_circle(
        dims.NOSE_OGIVE_CX, z_nose0, dims.NOSE_OGIVE_RHO_OUTER, p_t_sh, p_t_sp
    )

    band_zs = []
    z_b = z_bot + 3600.0
    while z_b <= z_nose0 - 1800.0:
        band_zs.append(z_b)
        z_b += dims.RING_STEP

    with bd.BuildSketch(bd.Plane.XZ) as tps_sk:
        with bd.BuildLine():
            bd.Line((r_in, z_bot), (r_tps, z_bot))
            prev = (r_tps, z_bot)
            for zc in band_zs:
                p1 = (r_tps, zc - 14.0)
                p2 = (r_tps - 6.0, zc)
                p3 = (r_tps, zc + 14.0)
                bd.Line(prev, p1)
                bd.Line(p1, p2)
                bd.Line(p2, p3)
                prev = p3
            bd.Line(prev, p_t_sh)
            bd.ThreePointArc(p_t_sh, mid_t_og, p_t_sp)
            bd.Line(p_t_sp, (0.0, z_cap_split))
            bd.Line((0.0, z_cap_split), (0.0, z_deck_top))
            bd.Line((0.0, z_deck_top), (r_in, z_deck_top))
            bd.Line((r_in, z_deck_top), (r_in, z_bot))
        bd.make_face()

    tps_belly = bd.Rot(0, 0, 180) * bd.revolve(tps_sk.sketch, axis=bd.Axis.Z, revolution_arc=180)
    tps_belly.label = "tps_windward_heat_shield"
    apply_tps_ceramic(tps_belly)

    # 4. Full 360° Matte-Black Ceramic Stagnation Nose Cap (Z = 119,500 .. 121,300)
    p_out_tan = (dims.NOSE_TAN_R_OUTER, dims.NOSE_TAN_Z_OUTER)
    p_out_apex = (0.0, dims.Z_SHIP_TOP)
    mid_out_og2 = _arc_mid_on_circle(
        dims.NOSE_OGIVE_CX, z_nose0, dims.NOSE_OGIVE_RHO_OUTER, p_t_sp, p_out_tan
    )
    mid_out_cap = _arc_mid_on_circle(
        0.0, dims.NOSE_CAP_CZ, dims.NOSE_CAP_R_OUTER, p_out_tan, p_out_apex
    )

    with bd.BuildSketch(bd.Plane.XZ) as cap_sk:
        with bd.BuildLine():
            bd.Line((0.0, z_cap_split), p_t_sp)
            bd.ThreePointArc(p_t_sp, mid_out_og2, p_out_tan)
            bd.ThreePointArc(p_out_tan, mid_out_cap, p_out_apex)
            bd.Line(p_out_apex, (0.0, z_cap_split))
        bd.make_face()

    tps_cap = bd.revolve(cap_sk.sketch, axis=bd.Axis.Z, revolution_arc=360)
    tps_cap.label = "tps_stagnation_nose_cap"
    apply_tps_ceramic(tps_cap)

    return thrust_deck, steel_hull, tps_belly, tps_cap


def _build_flap_pair_geometry(
    root_len: float,
    span: float,
    tip_z0: float,
    tip_z1: float,
    hinge_r: float,
    tip_half_t: float,
    tps_t: float,
    side_sign: int,
    label_prefix: str,
):
    """Build a tapered two-material aero flap (stainless leeward structure + black ceramic windward TPS)."""
    sx = float(side_sign)
    y_root_split = -(hinge_r - tps_t)
    y_tip_split = -(tip_half_t - tps_t * 0.65)
    y_tip_tps = -tip_half_t
    y_tip_lee = tip_half_t

    def _yz_rect(x_plane: float, y0: float, y1: float, z0: float, z1: float):
        with bd.BuildSketch(bd.Plane.YZ.offset(x_plane)) as sk:
            bd.Polygon((y0, z0), (y1, z0), (y1, z1), (y0, z1), align=None)
        return sk.sketch

    steel_wing = bd.loft(
        [
            _yz_rect(0.0, y_root_split, hinge_r, 0.0, root_len),
            _yz_rect(sx * span, y_tip_split, y_tip_lee, tip_z0, tip_z1),
        ],
        ruled=True,
    )
    knuckle_full = bd.Cylinder(
        hinge_r, root_len, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    inner_half_box = bd.Pos(-sx * hinge_r, 0.0, 0.0) * bd.Box(
        2.0 * hinge_r,
        2.2 * hinge_r,
        root_len,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    knuckle_inner = knuckle_full & inner_half_box
    steel_split_box = bd.Pos(0.0, y_root_split, 0.0) * bd.Box(
        3.0 * hinge_r,
        3.0 * hinge_r,
        root_len,
        align=(bd.Align.CENTER, bd.Align.MIN, bd.Align.MIN),
    )
    tps_split_box = bd.Pos(0.0, y_root_split, 0.0) * bd.Box(
        3.0 * hinge_r,
        3.0 * hinge_r,
        root_len,
        align=(bd.Align.CENTER, bd.Align.MAX, bd.Align.MIN),
    )

    steel_body = steel_wing.fuse(knuckle_inner & steel_split_box)
    steel_body.label = f"{label_prefix}_structure"
    apply_stainless_304l(steel_body)

    tps_wing = bd.loft(
        [
            _yz_rect(0.0, -hinge_r, y_root_split, 0.0, root_len),
            _yz_rect(sx * span, y_tip_tps, y_tip_split, tip_z0, tip_z1),
        ],
        ruled=True,
    )
    tps_body = tps_wing.fuse(knuckle_inner & tps_split_box)
    tps_body.label = f"{label_prefix}_tps"
    apply_tps_ceramic(tps_body)

    return bd.Compound(children=[steel_body, tps_body], label=label_prefix)


@model
def aft_flap_stbd():
    """Starboard (+X) Starship aft aerodynamic flap (16.0 m root chord, 3.9 m span)."""
    return _build_flap_pair_geometry(
        root_len=dims.AFT_FLAP_Z_TOP - dims.AFT_FLAP_Z_BOT,
        span=dims.AFT_FLAP_SPAN,
        tip_z0=1050.0,
        tip_z1=6650.0,
        hinge_r=190.0,
        tip_half_t=85.0,
        tps_t=48.0,
        side_sign=1,
        label_prefix="aft_flap_stbd",
    )


@model
def aft_flap_port():
    """Port (-X) Starship aft aerodynamic flap (16.0 m root chord, 3.9 m span)."""
    return _build_flap_pair_geometry(
        root_len=dims.AFT_FLAP_Z_TOP - dims.AFT_FLAP_Z_BOT,
        span=dims.AFT_FLAP_SPAN,
        tip_z0=1050.0,
        tip_z1=6650.0,
        hinge_r=190.0,
        tip_half_t=85.0,
        tps_t=48.0,
        side_sign=-1,
        label_prefix="aft_flap_port",
    )


@model
def fwd_flap_stbd():
    """Starboard (+X) Starship forward nosecone aerodynamic flap."""
    return _build_flap_pair_geometry(
        root_len=dims.FWD_HINGE_LEN,
        span=dims.FWD_FLAP_SPAN,
        tip_z0=1050.0,
        tip_z1=3550.0,
        hinge_r=135.0,
        tip_half_t=65.0,
        tps_t=42.0,
        side_sign=1,
        label_prefix="fwd_flap_stbd",
    )


@model
def fwd_flap_port():
    """Port (-X) Starship forward nosecone aerodynamic flap."""
    return _build_flap_pair_geometry(
        root_len=dims.FWD_HINGE_LEN,
        span=dims.FWD_FLAP_SPAN,
        tip_z0=1050.0,
        tip_z1=3550.0,
        hinge_r=135.0,
        tip_half_t=65.0,
        tps_t=42.0,
        side_sign=-1,
        label_prefix="fwd_flap_port",
    )


def _build_ship_6_raptors(sl_shape, vac_shape):
    """Arrange 3 Raptor SL (center) + 3 Raptor Vacuum (outer) inside Starship's aft engine skirt."""
    sl_engines = []
    for i, ang in enumerate((30.0, 150.0, 270.0), start=1):
        rad = math.radians(ang)
        x = dims.SHIP_SL_RING_R * math.cos(rad)
        y = dims.SHIP_SL_RING_R * math.sin(rad)
        eng = bd.Pos(x, y, dims.Z_SHIP_SL_EXIT) * bd.Rot(0, 0, ang) * sl_shape
        eng.label = f"ship_raptor_sl_{i}"
        sl_engines.append(eng)

    vac_engines = []
    for i, ang in enumerate((90.0, 210.0, 330.0), start=1):
        rad = math.radians(ang)
        x = dims.SHIP_VAC_RING_R * math.cos(rad)
        y = dims.SHIP_VAC_RING_R * math.sin(rad)
        eng = bd.Pos(x, y, dims.Z_SHIP_RVAC_EXIT) * bd.Rot(0, 0, ang) * vac_shape
        eng.label = f"ship_raptor_vac_{i}"
        vac_engines.append(eng)

    return bd.Compound(
        children=[
            bd.Compound(children=sl_engines, label="ship_raptor_sl_3"),
            bd.Compound(children=vac_engines, label="ship_raptor_vac_3"),
        ],
        label="ship_propulsion_6",
    )


def _trim_against_body(shape, steel_hull, tps_belly, tps_cap):
    """Trim an external fairing cleanly against each Starship hull solid sequentially (zero overlap)."""
    res = shape - steel_hull
    res = res - tps_belly
    res = res - tps_cap
    return res


def _build_aero_covers_and_clevises(steel_hull, tps_belly, tps_cap):
    """Build windward hinge aero-covers and structural hinge clevises for all 4 flaps."""
    parts = []

    # --- 1. Aft Flap Windward Aero-Covers & Top/Bottom Hinge Clevises (±X) ---
    hx = dims.AFT_FLAP_HINGE_X   # 4680.0
    hy = dims.AFT_FLAP_HINGE_Y   # 580.0
    z0 = dims.AFT_FLAP_Z_BOT     # 71350.0
    z1 = dims.AFT_FLAP_Z_TOP     # 87350.0
    hinge_r = 190.0

    y_cover_back = hy - (hinge_r + 22.0)  # 368.0 mm
    y_cover_front = 0.0                   # Starts flush at the Y=0 TPS meridian (clean single-solid contact!)
    cover_z0 = dims.Z_SHIP_BOT + 100.0
    cover_z1 = z1 + 750.0
    x_in_aft = dims.HULL_R - 70.0         # 4430.0 mm: strictly outside R_in=4400 (clears ship_thrust_deck!)

    # Crisp extruded profile + clean top bevel cut (planar faces -> fast, exact OCCT booleans)
    aft_pts = [
        (x_in_aft, y_cover_front),
        (hx + 250.0, y_cover_back - 90.0),
        (hx + 250.0, y_cover_back),
        (x_in_aft, y_cover_back),
    ]
    with bd.BuildSketch(bd.Plane.XY.offset(cover_z0)) as aft_sk:
        bd.Polygon(*aft_pts, align=None)
    aft_cov_raw = bd.extrude(aft_sk.sketch, amount=cover_z1 - cover_z0)
    # Taper the top 750 mm smoothly into the hull with a planar 45° bevel cut
    top_bevel_cut = (
        bd.Pos(dims.HULL_R + 40.0, 0.0, cover_z1)
        * bd.Rot(0, 38.0, 0)
        * bd.Box(1200.0, 1200.0, 1200.0, align=(bd.Align.MIN, bd.Align.CENTER, bd.Align.MIN))
    )
    hinge_clear = bd.Pos(hx, hy, cover_z0 - 100.0) * bd.Cylinder(
        hinge_r + 22.0, cover_z1 - cover_z0 + 200.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    aft_cov_stbd = _trim_against_body(
        aft_cov_raw - top_bevel_cut - hinge_clear, steel_hull, tps_belly, tps_cap
    )
    aft_cov_stbd.label = "aft_hinge_aerocover_stbd"
    apply_tps_ceramic(aft_cov_stbd)

    aft_cov_port = bd.mirror(aft_cov_stbd, about=bd.Plane.YZ)
    aft_cov_port.label = "aft_hinge_aerocover_port"
    apply_tps_ceramic(aft_cov_port)
    parts.extend([aft_cov_stbd, aft_cov_port])

    # Bottom and top structural hinge clevis brackets (flush with Z=z0 and Z=z1 of aft flap)
    clevis_h = 240.0
    clev_bot_raw = bd.Pos(x_in_aft, hy, z0 - clevis_h) * bd.Box(
        (hx - x_in_aft) + hinge_r,
        2.0 * hinge_r,
        clevis_h,
        align=(bd.Align.MIN, bd.Align.CENTER, bd.Align.MIN),
    )
    clev_top_raw = bd.Pos(x_in_aft, hy, z1) * bd.Box(
        (hx - x_in_aft) + hinge_r,
        2.0 * hinge_r,
        clevis_h,
        align=(bd.Align.MIN, bd.Align.CENTER, bd.Align.MIN),
    )
    aft_clev_stbd = _trim_against_body(clev_bot_raw.fuse(clev_top_raw), steel_hull, tps_belly, tps_cap)
    aft_clev_stbd.label = "aft_hinge_clevis_stbd"
    apply_stainless_structural(aft_clev_stbd)

    aft_clev_port = bd.mirror(aft_clev_stbd, about=bd.Plane.YZ)
    aft_clev_port.label = "aft_hinge_clevis_port"
    apply_stainless_structural(aft_clev_port)
    parts.extend([aft_clev_stbd, aft_clev_port])

    # --- 2. Forward Flap Windward Aero-Covers & Continuous Spine Clevis (on Ogive Nosecone, ±X) ---
    fwd_loc_stbd = _fwd_hinge_location(side_sign=1)
    fwd_r = 135.0
    fwd_len = dims.FWD_HINGE_LEN
    fy_back = -(fwd_r + 22.0)   # -157.0 mm in local hinge frame -> Y_world = +323 mm
    fy_front = -475.0           # Y_world = +5 mm (cleanly on leeward side of Y=0 TPS cliff!)

    # Planar polygon extrusion along the inclined hinge axis (zero twisted loft faces -> clean OCCT booleans!)
    fwd_pts = [
        (-620.0, fy_front),
        (fwd_r + 50.0, fy_back - 70.0),
        (fwd_r + 50.0, fy_back),
        (-620.0, fy_back),
    ]
    with bd.BuildSketch(bd.Plane.XY.offset(-200.0)) as fwd_sk:
        bd.Polygon(*fwd_pts, align=None)
    fwd_cov_local = bd.extrude(fwd_sk.sketch, amount=fwd_len + 400.0)
    fwd_clear_local = bd.Pos(0, 0, -500.0) * bd.Cylinder(
        fwd_r + 22.0, fwd_len + 1000.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    fwd_cov_stbd = (fwd_loc_stbd * (fwd_cov_local - fwd_clear_local)) - steel_hull
    fwd_cov_stbd.label = "fwd_hinge_aerocover_stbd"
    apply_tps_ceramic(fwd_cov_stbd)

    fwd_cov_port = bd.mirror(fwd_cov_stbd, about=bd.Plane.YZ)
    fwd_cov_port.label = "fwd_hinge_aerocover_port"
    apply_tps_ceramic(fwd_cov_port)
    parts.extend([fwd_cov_stbd, fwd_cov_port])

    # Top, bottom, and continuous inner spine fairing connecting hinge cleanly to curved ogive
    fc_h = 200.0
    fc_bot_loc = bd.Pos(-650.0, 0.0, -fc_h) * bd.Box(
        650.0 + fwd_r, 2.0 * fwd_r, fc_h, align=(bd.Align.MIN, bd.Align.CENTER, bd.Align.MIN)
    )
    fc_top_loc = bd.Pos(-650.0, 0.0, fwd_len) * bd.Box(
        650.0 + fwd_r, 2.0 * fwd_r, fc_h, align=(bd.Align.MIN, bd.Align.CENTER, bd.Align.MIN)
    )
    spine_x_max = -(fwd_r + 22.0)  # -157.0 mm in hinge frame (22 mm clear of R=135 hinge barrel)
    fc_spine_loc = bd.Pos(-750.0, 0.0, -fc_h) * bd.Box(
        750.0 + spine_x_max,
        2.0 * fwd_r,
        fwd_len + 2.0 * fc_h,
        align=(bd.Align.MIN, bd.Align.CENTER, bd.Align.MIN),
    )
    fwd_spine_world = fwd_loc_stbd * (fc_spine_loc - fwd_clear_local)
    fwd_endcaps_world = fwd_loc_stbd * fc_bot_loc.fuse(fc_top_loc)
    fwd_clev_stbd = _trim_against_body(
        fwd_spine_world.fuse(fwd_endcaps_world), steel_hull, tps_belly, tps_cap
    )
    fwd_clev_stbd.label = "fwd_hinge_clevis_stbd"
    apply_stainless_structural(fwd_clev_stbd)

    fwd_clev_port = bd.mirror(fwd_clev_stbd, about=bd.Plane.YZ)
    fwd_clev_port.label = "fwd_hinge_clevis_port"
    apply_stainless_structural(fwd_clev_port)
    parts.extend([fwd_clev_stbd, fwd_clev_port])

    return parts


def _build_ship_details(steel_hull, tps_belly, tps_cap):
    """Build Starship leeward raceway, Starlink payload bay door frame, forward catch pins & RCS pods."""
    r_out = dims.HULL_R
    parts = []

    # 1. Leeward (+Y) Avionics/Propellant Raceway & Ship Quick Disconnect (SQD)
    rw_z0 = dims.Z_SHIP_BOT + 300.0
    rw_z1 = 98200.0
    rw_pts = [
        (-250.0, r_out - 80.0),
        (250.0, r_out - 80.0),
        (150.0, r_out + 220.0),
        (-150.0, r_out + 220.0),
    ]
    with bd.BuildSketch(bd.Plane.XY.offset(rw_z0)) as rw_sk:
        bd.Polygon(*rw_pts, align=None)
    rw_raw = bd.extrude(rw_sk.sketch, amount=rw_z1 - rw_z0)
    sqd_box = bd.Pos(0, r_out + 150.0, dims.Z_SHIP_BOT + 3200.0) * bd.Box(640.0, 260.0, 1450.0)
    ship_rw = _trim_against_body(rw_raw.fuse(sqd_box), steel_hull, tps_belly, tps_cap)
    ship_rw.label = "ship_raceway_and_sqd"
    apply_dark_trim(ship_rw)
    parts.append(ship_rw)

    # 2. Starlink Payload Bay "Pez Dispenser" Door Frame on leeward (+Y) side (Z = 99,800 .. 104,600)
    door_z0 = 99800.0
    door_h = 4800.0
    door_w = 2400.0
    door_frame_w = 180.0
    frame_outer = bd.Pos(0, r_out - 250.0, door_z0) * bd.Box(
        door_w, 305.0, door_h, align=(bd.Align.CENTER, bd.Align.MIN, bd.Align.MIN)
    )
    frame_cut = bd.Pos(0, r_out - 250.0, door_z0 + door_frame_w) * bd.Box(
        door_w - 2.0 * door_frame_w,
        350.0,
        door_h - 2.0 * door_frame_w,
        align=(bd.Align.CENTER, bd.Align.MIN, bd.Align.MIN),
    )
    door_outer_clip = bd.Pos(0, 0, door_z0 - 100.0) * bd.Cylinder(
        r_out + 55.0, door_h + 200.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    pez_frame = _trim_against_body((frame_outer - frame_cut) & door_outer_clip, steel_hull, tps_belly, tps_cap)
    pez_frame.label = "starlink_payload_door_frame"
    apply_stainless_structural(pez_frame)
    parts.append(pez_frame)

    # 3. Two Forward Lifting / Mechazilla Catch Pins (slightly leeward of ±X at Z = 104,400 mm)
    z_pin = dims.SHIP_CATCH_PIN_Z
    pad = bd.Pos(r_out - 120.0, 0, z_pin) * bd.Box(
        200.0, 960.0, 1450.0, align=(bd.Align.MIN, bd.Align.CENTER, bd.Align.CENTER)
    )
    shaft = (
        bd.Pos(r_out, 0, z_pin)
        * bd.Rot(0, 90, 0)
        * bd.Cylinder(
            dims.SHIP_CATCH_PIN_R,
            dims.SHIP_CATCH_PIN_LEN - 90.0,
            align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
        )
    )
    tip = bd.Pos(r_out + dims.SHIP_CATCH_PIN_LEN - 90.0, 0, z_pin) * bd.Sphere(
        dims.SHIP_CATCH_PIN_R + 45.0
    )
    for ang, label in ((15.0, "ship_catch_pin_stbd"), (165.0, "ship_catch_pin_port")):
        pin = _trim_against_body(bd.Rot(0, 0, ang) * pad.fuse(shaft, tip), steel_hull, tps_belly, tps_cap)
        pin.label = label
        apply_grid_fin_steel(pin)
        parts.append(pin)

    # 4. Two Leeward RCS / Ullage Cold-Gas Thruster Blister Pods at Z = 106,000, ±38° from +Y (52°, 128°)
    z_rcs = 106000.0
    pod_raw = bd.Pos(r_out - 100.0, 0, z_rcs) * bd.Box(
        340.0, 620.0, 1350.0, align=(bd.Align.MIN, bd.Align.CENTER, bd.Align.CENTER)
    )
    for ang, label in ((52.0, "rcs_pod_stbd"), (128.0, "rcs_pod_port")):
        pod = _trim_against_body(bd.Rot(0, 0, ang) * pod_raw, steel_hull, tps_belly, tps_cap)
        pod.label = label
        apply_dark_trim(pod)
        parts.append(pod)

    return parts


def _fwd_hinge_location(side_sign: int):
    """Exact world Location of the forward flap hinge frame (Z along inclined ogive hinge, Y = world +Y)."""
    px = side_sign * dims.FWD_HINGE_P0[0]
    py = dims.FWD_HINGE_P0[1]
    pz = dims.FWD_HINGE_P0[2]
    return bd.Pos(px, py, pz) * bd.Rot(0, -side_sign * dims.FWD_HINGE_TILT_DEG, 0)


@model
def starship_core():
    """Starship rigid spacecraft core (hull, TPS heat shield, 6 Raptor engines, aero-covers & details)."""
    thrust_deck, steel_hull, tps_belly, tps_cap = _build_starship_hull_and_tps()
    engines = _build_ship_6_raptors(raptor_sl().shape, raptor_vac().shape)
    covers = _build_aero_covers_and_clevises(steel_hull, tps_belly, tps_cap)
    details = _build_ship_details(steel_hull, tps_belly, tps_cap)

    core = bd.Compound(
        children=[thrust_deck, steel_hull, tps_belly, tps_cap, engines, *covers, *details],
        label="starship_core",
    )
    bb = core.bounding_box()
    assert abs(bb.min.Z - dims.Z_SHIP_BOT) < 1.0, bb
    assert abs(bb.max.Z - dims.Z_SHIP_TOP) < 1.0, bb
    return core


def attach_starship_flaps(core, aft_s, aft_p, fwd_s, fwd_p):
    """Place and hinge-connect all 4 Starship aero flaps onto `core` via RevoluteJoints."""
    flaps = []

    loc_as = bd.Pos(dims.AFT_FLAP_HINGE_X, dims.AFT_FLAP_HINGE_Y, dims.AFT_FLAP_Z_BOT)
    f_as = loc_as * aft_s
    f_as.label = "aft_flap_stbd"
    ax_as = bd.Axis((dims.AFT_FLAP_HINGE_X, dims.AFT_FLAP_HINGE_Y, dims.AFT_FLAP_Z_BOT), (0, 0, 1))
    j_as = bd.RevoluteJoint("aft_flap_stbd", core, axis=ax_as, angular_range=(0.0, 65.0))
    bd.RigidJoint("aft_flap_stbd", f_as, j_as.location)
    j_as.connect_to(f_as.joints["aft_flap_stbd"], angle=0.0)
    flaps.append(f_as)

    loc_ap = bd.Pos(-dims.AFT_FLAP_HINGE_X, dims.AFT_FLAP_HINGE_Y, dims.AFT_FLAP_Z_BOT)
    f_ap = loc_ap * aft_p
    f_ap.label = "aft_flap_port"
    ax_ap = bd.Axis((-dims.AFT_FLAP_HINGE_X, dims.AFT_FLAP_HINGE_Y, dims.AFT_FLAP_Z_BOT), (0, 0, -1))
    j_ap = bd.RevoluteJoint("aft_flap_port", core, axis=ax_ap, angular_range=(0.0, 65.0))
    bd.RigidJoint("aft_flap_port", f_ap, j_ap.location)
    j_ap.connect_to(f_ap.joints["aft_flap_port"], angle=0.0)
    flaps.append(f_ap)

    loc_fs = _fwd_hinge_location(side_sign=1)
    f_fs = loc_fs * fwd_s
    f_fs.label = "fwd_flap_stbd"
    ax_fs = bd.Axis(dims.FWD_HINGE_P0, dims.FWD_HINGE_DIR)
    j_fs = bd.RevoluteJoint("fwd_flap_stbd", core, axis=ax_fs, angular_range=(0.0, 65.0))
    bd.RigidJoint("fwd_flap_stbd", f_fs, j_fs.location)
    j_fs.connect_to(f_fs.joints["fwd_flap_stbd"], angle=0.0)
    flaps.append(f_fs)

    loc_fp = _fwd_hinge_location(side_sign=-1)
    f_fp = loc_fp * fwd_p
    f_fp.label = "fwd_flap_port"
    p0_port = (-dims.FWD_HINGE_P0[0], dims.FWD_HINGE_P0[1], dims.FWD_HINGE_P0[2])
    dir_port_neg = (dims.FWD_HINGE_DIR[0], 0.0, -dims.FWD_HINGE_DIR[2])
    ax_fp = bd.Axis(p0_port, dir_port_neg)
    j_fp = bd.RevoluteJoint("fwd_flap_port", core, axis=ax_fp, angular_range=(0.0, 65.0))
    bd.RigidJoint("fwd_flap_port", f_fp, j_fp.location)
    j_fp.connect_to(f_fp.joints["fwd_flap_port"], angle=0.0)
    flaps.append(f_fp)

    return flaps


@model
def starship():
    """Complete SpaceX Starship Upper Stage (50.3 m) with 4 articulated flaps & 6 Raptor engines."""
    core = starship_core().shape
    flaps = attach_starship_flaps(
        core,
        aft_flap_stbd().shape,
        aft_flap_port().shape,
        fwd_flap_stbd().shape,
        fwd_flap_port().shape,
    )
    ship = bd.Compound(children=[core, *flaps], label="starship")
    mechanism_state(
        ship,
        "launch_neutral",
        aft_flap_stbd=0.0,
        aft_flap_port=0.0,
        fwd_flap_stbd=0.0,
        fwd_flap_port=0.0,
    )
    mechanism_state(
        ship,
        "reentry_belly_flop",
        aft_flap_stbd=55.0,
        aft_flap_port=55.0,
        fwd_flap_stbd=55.0,
        fwd_flap_port=55.0,
    )
    return ship


if __name__ == "__main__":
    starship()
