"""Top crown platform, drawworks cable sheave gantry headframe, beacons, and lightning arrestor mast."""

import build123d as bd
from cad import model

import spec as S
from foundation import _build_sheave


def _build_crown_deck():
    """Heavy steel cap deck at Z=1355..1363 with perimeter blast parapet & gantry clearances."""
    z0 = S.TOWER_TOP_Z
    dh = S.CROWN_DECK_H
    half = S.CROWN_DECK_HALF

    deck = bd.Pos(0, 0, z0) * bd.Box(
        2.0 * half,
        2.0 * half,
        dh,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    # Chamfer bottom underside bevel slightly for crisp overhang shadow
    bot_edges = deck.edges().filter_by(lambda e: abs(e.center().Z - z0) < 0.1)
    deck = deck.chamfer(2.0, None, bot_edges)

    # Perimeter safety parapet walls (Z: 1363..1374), split open at Y in [-29, +29] on +/-X for sheave gantry
    zp = z0 + dh
    ph = S.CROWN_PARAPET_H
    pw = 2.6
    walls = [
        # Port (+Y) and Starboard (-Y) continuous parapets
        bd.Pos(0, half - pw / 2.0, zp)
        * bd.Box(2.0 * half, pw, ph, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)),
        bd.Pos(0, -half + pw / 2.0, zp)
        * bd.Box(2.0 * half, pw, ph, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)),
    ]
    # Split +/-X parapets outside the gantry corridor (Y in [30, 70] and [-70, -30])
    seg_len = half - 30.0  # 40.0 mm
    seg_yc = 30.0 + seg_len / 2.0
    for sx in (-1, 1):
        for sy in (-1, 1):
            walls.append(
                bd.Pos(sx * (half - pw / 2.0), sy * seg_yc, zp)
                * bd.Box(pw, seg_len, ph, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
            )

    full_deck = deck + walls
    full_deck.label = "crown_deck"
    S.apply_material(full_deck, S.mat_tower_steel())
    return full_deck


def _build_sheave_gantry():
    """Cantilevered crown pulley headframe holding front (+78) and rear (-64) drawworks sheaves."""
    z0 = S.TOWER_TOP_Z + S.CROWN_DECK_H  # 1363.0
    z_top = S.CROWN_SHEAVE_Z + 16.0      # 1408.0
    x_rear = S.CROWN_REAR_AXLE_X - 11.0  # -75.0 (clears rear cable at X=-76.0!)
    x_front = S.CROWN_FRONT_AXLE_X + 11.0  # +89.0 (clears front cable tangent X=+90.0!)

    # Side gantry girder cheek profile in XZ (cantilevers cleanly over front & rear sheaves)
    cheek_poly = bd.Polygon(
        [
            (-64.0, z0),
            (66.0, z0),
            (x_front, z0 + 18.0),
            (x_front, z_top - 6.0),
            (x_front - 8.0, z_top),
            (x_rear + 8.0, z_top),
            (x_rear, z_top - 6.0),
            (x_rear, z0 + 18.0),
        ],
        align=None,
    )
    # Truss lightening cutouts in the side wall (keeping clear of axle bearings and mast center)
    cut1 = bd.Polygon(
        [(-50.0, z0 + 8.0), (-16.0, z0 + 8.0), (-16.0, z_top - 9.0), (-44.0, z_top - 9.0)],
        align=None,
    )
    cut2 = bd.Polygon(
        [(16.0, z0 + 8.0), (58.0, z0 + 8.0), (54.0, z_top - 9.0), (16.0, z_top - 9.0)],
        align=None,
    )
    cheek_face = cheek_poly - cut1 - cut2
    cheek_proto = bd.Rot(90, 0, 0) * bd.extrude(cheek_face, 1.8, both=True)

    # Four cheek plates flanking the two sheave tracks at Y = +/-18 (leaves Y in [-9.2, +9.2] open for mast!)
    cheek_ys = (-25.0, -11.0, 11.0, 25.0)
    parts = [bd.Pos(0, y, 0) * cheek_proto for y in cheek_ys]

    # Cross tie beams connecting each pair of cheeks cleanly (avoiding central lightning mast corridor!)
    for sy in (-1, 1):
        yc = sy * S.CABLE_Y
        parts.append(
            bd.Pos(-40.0, yc, z0)
            * bd.Box(16.0, 10.4, 5.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        )
        parts.append(
            bd.Pos(44.0, yc, z0)
            * bd.Box(18.0, 10.4, 5.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        )

    # Top transverse tie-bars positioned cleanly BELOW the horizontal cables (cable bottom = 1402.9)
    parts.append(
        bd.Pos(-32.0, 0, z_top - 11.5)
        * bd.Box(10.0, 52.0, 4.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    )
    parts.append(
        bd.Pos(36.0, 0, z_top - 11.5)
        * bd.Box(10.0, 52.0, 4.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    )

    # Bore clean R=3.2 axle clearances for both front and rear sheave shafts
    bores = [
        bd.Pos(S.CROWN_REAR_AXLE_X, 0, S.CROWN_SHEAVE_Z) * bd.Rot(90, 0, 0) * bd.Cylinder(3.2, 60.0),
        bd.Pos(S.CROWN_FRONT_AXLE_X, 0, S.CROWN_SHEAVE_Z) * bd.Rot(90, 0, 0) * bd.Cylinder(3.2, 60.0),
    ]
    gantry = (parts[0] + parts[1:]) - bores
    gantry.label = "sheave_gantry"
    S.apply_material(gantry, S.mat_carriage_steel())
    return gantry


def _build_crown_sheaves_and_cables():
    """Four crown grooved pulley wheels, twin axle shafts, and horizontal top crossover haul cables."""
    sz = S.CROWN_SHEAVE_Z
    wheel_proto = _build_sheave(S.SHEAVE_PITCH_R, S.SHEAVE_OUTER_R, 5.8)
    S.apply_material(wheel_proto, S.mat_sheave())

    items = []
    # Front and rear axle shafts
    for ax_x, pos_name in ((S.CROWN_REAR_AXLE_X, "rear"), (S.CROWN_FRONT_AXLE_X, "front")):
        axle = bd.Pos(ax_x, 0, sz) * bd.Rot(90, 0, 0) * bd.Cylinder(3.0, 56.0)
        axle.label = f"crown_axle_{pos_name}"
        S.apply_material(axle, S.mat_guide_rail())
        items.append(axle)

        for sy, side in ((1, "port"), (-1, "stbd")):
            w = bd.Pos(ax_x, sy * S.CABLE_Y, sz) * wheel_proto
            w.label = f"crown_sheave_{pos_name}_{side}"
            items.append(w)

    # Horizontal top crossover cables running across the tops of rear (-64) & front (+78) sheaves
    cable_z = sz + S.SHEAVE_PITCH_R  # 1404.0 mm
    cable_len = S.CROWN_FRONT_AXLE_X - S.CROWN_REAR_AXLE_X  # 142.0 mm
    for sy, side in ((1, "port"), (-1, "stbd")):
        rope = (
            bd.Pos(S.CROWN_REAR_AXLE_X, sy * S.CABLE_Y, cable_z)
            * bd.Rot(0, 90, 0)
            * bd.Cylinder(
                S.CABLE_R,
                cable_len,
                align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
            )
        )
        rope.label = f"crown_cable_{side}"
        S.apply_material(rope, S.mat_cable())
        items.append(rope)

    return items


def _build_lightning_mast_and_beacons():
    """Central tapered lightning arrestor spire (Z: 1363..1500 mm) and red aviation beacons."""
    z0 = S.LIGHTNING_MAST_BASE_Z  # 1363.0

    # Stepped/tapered octagonal-to-conical tubular spire (base R=7.8 fits cleanly in Y in [-9.2, +9.2]!)
    base_flange = bd.Pos(0, 0, z0) * bd.Cylinder(
        8.2, 4.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    lower_cone = bd.Pos(0, 0, z0 + 4.0) * bd.Cone(
        6.5, 4.2, 54.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    mid_cone = bd.Pos(0, 0, z0 + 58.0) * bd.Cone(
        4.2, 2.2, 46.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    upper_rod = bd.Pos(0, 0, z0 + 104.0) * bd.Cone(
        2.2, 0.7, 30.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    # Telemetry & anemometer cross-arms at Z = 1422 and Z = 1465
    ring1 = bd.Pos(0, 0, z0 + 58.0) * bd.Cylinder(9.0, 1.8) - bd.Pos(0, 0, z0 + 58.0) * bd.Cylinder(
        6.8, 2.2
    )
    arm1_x = bd.Pos(0, 0, z0 + 58.0) * bd.Box(17.0, 1.6, 1.6)
    arm1_y = bd.Pos(0, 0, z0 + 58.0) * bd.Box(1.6, 17.0, 1.6)
    arm2_x = bd.Pos(0, 0, z0 + 102.0) * bd.Box(14.0, 1.4, 1.4)
    arm2_y = bd.Pos(0, 0, z0 + 102.0) * bd.Box(1.4, 14.0, 1.4)

    mast = base_flange + [lower_cone, mid_cone, upper_rod, ring1, arm1_x, arm1_y, arm2_x, arm2_y]
    mast.label = "lightning_mast"
    S.apply_material(mast, S.mat_cladding())

    # Aviation obstruction beacons: 1 at mast apex (Z=1497..1500) + 4 on crown parapet corners
    beacons = []
    apex_beacon = bd.Pos(0, 0, S.LIGHTNING_MAST_TOP_Z - 3.0) * bd.Cylinder(
        1.5, 3.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    apex_beacon.label = "beacon_apex"
    S.apply_material(apex_beacon, S.mat_beacon_red())
    beacons.append(apex_beacon)

    beacon_proto = bd.Cylinder(
        1.6, 3.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    S.apply_material(beacon_proto, S.mat_beacon_red())
    zb = S.TOWER_TOP_Z + S.CROWN_DECK_H + S.CROWN_PARAPET_H
    corner_pos = S.CROWN_DECK_HALF - 1.3
    for sx, nx in ((1, "front"), (-1, "rear")):
        for sy, ny in ((1, "port"), (-1, "stbd")):
            b = bd.Pos(sx * corner_pos, sy * corner_pos, zb) * beacon_proto
            b.label = f"beacon_{nx}_{ny}"
            beacons.append(b)

    return [mast, *beacons]


@model
def crown():
    """Complete Mechazilla top crown deck, drawworks sheave gantry, pulleys, and lightning mast."""
    deck = _build_crown_deck()
    gantry = _build_sheave_gantry()
    sheaves = _build_crown_sheaves_and_cables()
    mast_and_beacons = _build_lightning_mast_and_beacons()

    assy = bd.Compound(
        children=[deck, gantry, *sheaves, *mast_and_beacons],
        label="crown",
    )
    bb = assy.bounding_box()
    assert abs(bb.max.Z - S.LIGHTNING_MAST_TOP_Z) < 1e-4, bb
    return assy


if __name__ == "__main__":
    crown()
