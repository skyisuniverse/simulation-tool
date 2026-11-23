"""Foundation, concrete plinth, steel column base plates, and drawworks winch house for Mechazilla."""

import build123d as bd
from cad import model

import spec as S


def _build_sheave(pitch_r, outer_r, width):
    """Build a grooved structural steel cable sheave centered at origin, rotating about Y."""
    half_w = width / 2.0
    groove_top_w = 1.9
    groove_bot_w = 1.35  # Clears CABLE_R=1.1 cleanly inside groove
    groove_bot_r = pitch_r - 1.35  # Bottom of cable sits at pitch_r - 1.1 > groove_bot_r
    # Revolved profile in XZ plane about Z, then rotated so axis aligns with Y
    pts = [
        (3.2, -half_w),
        (outer_r, -half_w),
        (outer_r, -groove_top_w),
        (groove_bot_r, -groove_bot_w),
        (groove_bot_r, groove_bot_w),
        (outer_r, groove_top_w),
        (outer_r, half_w),
        (3.2, half_w),
        (3.2, -half_w),
    ]
    wire = bd.Wire.make_polygon([bd.Vector(r, 0, z) for r, z in pts])
    face = bd.Face(wire)
    wheel = bd.revolve(face, axis=bd.Axis.Z, revolution_arc=360)
    # Recessed weight-relief side pockets on web
    for sign in (-1, 1):
        recess = (
            bd.Pos(0, 0, sign * (half_w - 0.8))
            * bd.Cylinder(groove_bot_r - 1.2, 1.6)
            - bd.Pos(0, 0, sign * (half_w - 0.8))
            * bd.Cylinder(5.2, 1.8)
        )
        wheel = wheel - recess
    # Orient axle along Y
    return bd.Rot(90, 0, 0) * wheel


def _base_plate_solid():
    """Single square steel column anchor base plate with 4 corner anchor bolt bosses (Z: 47..50)."""
    plate = bd.Pos(0, 0, S.PLINTH_HIGH_TOP_Z) * bd.Box(
        S.BASE_PLATE_SIZE,
        S.BASE_PLATE_SIZE,
        S.BASE_PLATE_H,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    # Corner anchor bolt lugs sitting around the column footprint (clear of R=6.0 column)
    bolt_off = 8.4
    bolts = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            bolts.append(
                bd.Pos(sx * bolt_off, sy * bolt_off, S.TOWER_BASE_Z)
                * bd.Cylinder(1.2, 1.8, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
            )
    return plate + bolts


def _winch_bunker():
    """Blast-shielded drawworks winch house sitting on apron (Z: 10..56)."""
    x0, x1 = S.WINCH_X_MIN, S.WINCH_X_MAX
    dx = x1 - x0
    xc = (x0 + x1) / 2.0
    dy = 2.0 * S.WINCH_Y_HALF
    z0 = S.APRON_H
    h = S.WINCH_H

    # Main sloped blast bunker shell (built in XZ profile, extruded across Y)
    profile = bd.Polygon(
        [
            (x0, z0),
            (x1, z0),
            (x1, z0 + h - 10.0),
            (x1 - 14.0, z0 + h),
            (x0 + 8.0, z0 + h),
            (x0, z0 + h - 6.0),
        ],
        align=None,
    )
    shell = bd.Rot(90, 0, 0) * bd.extrude(profile, dy / 2.0, both=True)

    # Hollow front cable portal bay so the drawworks winch drum is clearly visible
    portal = bd.Pos(x1 - 24.0, 0, z0 + 2.5) * bd.Box(
        56.0,
        74.0,
        34.0,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    shell = shell - portal

    # Exterior blast-wall stiffening pilasters along side walls and rear wall
    ribs = []
    for rx in (x0 + 16.0, x0 + 36.0, x0 + 56.0, x0 + 74.0):
        for sy in (-1, 1):
            ribs.append(
                bd.Pos(rx, sy * (S.WINCH_Y_HALF + 1.0), z0)
                * bd.Box(4.0, 2.2, h - 8.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
            )
    for ry in (-32.0, 0.0, 32.0):
        ribs.append(
            bd.Pos(x0 - 1.0, ry, z0)
            * bd.Box(2.2, 5.0, h - 7.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        )
    # Rooftop HVAC / cooling housing
    ribs.append(
        bd.Pos(xc - 8.0, 0.0, z0 + h)
        * bd.Box(32.0, 44.0, 5.5, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    )
    shell = shell + ribs
    return shell


def _winch_drum_assembly():
    """Grooved drawworks cable drum, motor gearboxes, and pillow blocks inside the winch bunker."""
    cx, cz = S.WINCH_DRUM_X, S.WINCH_DRUM_Z
    drum_len = 52.0
    # Main cylindrical drum barrel + heavy end flanges (bottom at 28 - 13.5 = 14.5 > 12.5 floor)
    barrel = bd.Pos(cx, 0, cz) * bd.Rot(90, 0, 0) * bd.Cylinder(S.WINCH_DRUM_R, drum_len)
    flange_l = bd.Pos(cx, -drum_len / 2.0 - 1.5, cz) * bd.Rot(90, 0, 0) * bd.Cylinder(13.5, 3.0)
    flange_r = bd.Pos(cx, drum_len / 2.0 + 1.5, cz) * bd.Rot(90, 0, 0) * bd.Cylinder(13.5, 3.0)
    axle = bd.Pos(cx, 0, cz) * bd.Rot(90, 0, 0) * bd.Cylinder(3.8, 70.0)
    drum = barrel + [flange_l, flange_r, axle]
    drum.label = "winch_drum"
    S.apply_material(drum, S.mat_carriage_steel())

    # Twin electric motor drive housings & pillow blocks sitting on bunker floor (Z = 12.5), bored for axle
    drives = []
    axle_bore = bd.Pos(cx, 0, cz) * bd.Rot(90, 0, 0) * bd.Cylinder(4.2, 80.0)
    for sy, side in ((1, "port"), (-1, "stbd")):
        ped = bd.Pos(cx, sy * 32.5, S.APRON_H + 2.5) * bd.Box(
            20.0, 6.5, 22.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
        )
        ped = ped - axle_bore
        ped.label = f"winch_drive_{side}"
        S.apply_material(ped, S.mat_tower_steel())
        drives.append(ped)

    # Horizontal wire rope spans from drum top tangent (Z=39.2) to lower deflector sheaves (X=-88)
    cables = []
    cable_z = cz + S.WINCH_DRUM_R + S.CABLE_R + 0.1  # 39.2 mm exact clearance above drum barrel
    cable_len = S.REAR_SHEAVE_X - cx
    for sy, side in ((1, "port"), (-1, "stbd")):
        rope = (
            bd.Pos(cx, sy * S.CABLE_Y, cable_z)
            * bd.Rot(0, 90, 0)
            * bd.Cylinder(
                S.CABLE_R,
                cable_len,
                align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
            )
        )
        rope.label = f"winch_cable_{side}"
        S.apply_material(rope, S.mat_cable())
        cables.append(rope)

    return [drum, *drives, *cables]


def _lower_sheave_assembly():
    """Lower deflector sheave A-frame stand & twin pulleys turning haul cables vertical at X=-76."""
    sx, sz = S.REAR_SHEAVE_X, S.REAR_SHEAVE_Z
    z0 = S.APRON_H

    # Steel A-frame cheek pedestals standing cleanly on apron between winch house (-102) and plinth (-82)
    cheeks = []
    for y_pos in (-25.0, -11.0, 11.0, 25.0):
        profile = bd.Polygon(
            [
                (-99.0, z0),
                (-83.0, z0),
                (-83.5, sz + 5.5),
                (-92.5, sz + 5.5),
            ],
            align=None,
        )
        cheek = bd.Pos(0, y_pos, 0) * bd.Rot(90, 0, 0) * bd.extrude(profile, 1.8, both=True)
        cheeks.append(cheek)
    # Cross base plate & upper tie bar
    tie_bot = bd.Pos(-91.0, 0, z0) * bd.Box(
        16.0, 54.0, 3.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    tie_mid = bd.Pos(-91.0, 0, z0 + 18.0) * bd.Box(
        12.0, 50.0, 3.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    axle_bore = bd.Pos(sx, 0, sz) * bd.Rot(90, 0, 0) * bd.Cylinder(3.2, 60.0)
    stand = (tie_bot + [tie_mid, *cheeks]) - axle_bore
    stand.label = "lower_sheave_stand"
    S.apply_material(stand, S.mat_tower_steel())

    # Axle shaft
    axle = (
        bd.Pos(sx, 0, sz)
        * bd.Rot(90, 0, 0)
        * bd.Cylinder(3.0, 55.0)
    )
    axle.label = "lower_sheave_axle"
    S.apply_material(axle, S.mat_guide_rail())

    # Twin grooved pulleys at Y = +/-18.0
    wheel = _build_sheave(S.SHEAVE_PITCH_R, S.SHEAVE_OUTER_R, 5.8)
    sheaves = []
    for sy, side in ((1, "port"), (-1, "stbd")):
        p = bd.Pos(sx, sy * S.CABLE_Y, sz) * wheel
        p.label = f"lower_sheave_{side}"
        S.apply_material(p, S.mat_sheave())
        sheaves.append(p)

    return [stand, axle, *sheaves]


@model
def foundation():
    """Complete concrete launch tower pad, stepped plinth, column anchor plates, and drawworks house."""
    # 1. Concrete apron pad (Z: 0 -> 10)
    apron_dx = S.APRON_X_MAX - S.APRON_X_MIN
    apron_xc = (S.APRON_X_MIN + S.APRON_X_MAX) / 2.0
    apron = bd.Pos(apron_xc, 0, 0) * bd.Box(
        apron_dx,
        2.0 * S.APRON_Y_HALF,
        S.APRON_H,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    top_edges = apron.edges().filter_by(lambda e: abs(e.center().Z - S.APRON_H) < 0.1)
    apron = apron.chamfer(2.0, None, top_edges)
    apron.label = "apron_slab"
    S.apply_material(apron, S.mat_concrete_dark())

    # 2. Stepped reinforced concrete tower plinth (Z: 10 -> 47)
    tier1 = bd.Pos(0, 0, S.APRON_H) * bd.Box(
        2.0 * S.PLINTH_LOW_HALF,
        2.0 * S.PLINTH_LOW_HALF,
        S.PLINTH_LOW_TOP_Z - S.APRON_H,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    tier1_top = tier1.edges().filter_by(lambda e: abs(e.center().Z - S.PLINTH_LOW_TOP_Z) < 0.1)
    tier1 = tier1.chamfer(2.5, None, tier1_top)

    tier2 = bd.Pos(0, 0, S.PLINTH_LOW_TOP_Z) * bd.Box(
        2.0 * S.PLINTH_HIGH_HALF,
        2.0 * S.PLINTH_HIGH_HALF,
        S.PLINTH_HIGH_TOP_Z - S.PLINTH_LOW_TOP_Z,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    tier2_top = tier2.edges().filter_by(lambda e: abs(e.center().Z - S.PLINTH_HIGH_TOP_Z) < 0.1)
    tier2 = tier2.chamfer(1.8, None, tier2_top)

    plinth = tier1 + tier2
    plinth.label = "tower_plinth"
    S.apply_material(plinth, S.mat_concrete())

    # 3. Four heavy steel column sole plates (Z: 47 -> 50)
    bp_proto = _base_plate_solid()
    S.apply_material(bp_proto, S.mat_carriage_steel())
    base_plates = []
    for sx, nx in ((1, "front"), (-1, "rear")):
        for sy, ny in ((1, "port"), (-1, "stbd")):
            bp = bd.Pos(sx * S.COL_HALF, sy * S.COL_HALF, 0) * bp_proto
            bp.label = f"base_plate_{nx}_{ny}"
            base_plates.append(bp)

    # 4. Drawworks winch bunker + drum + lower deflector sheaves
    bunker = _winch_bunker()
    bunker.label = "drawworks_bunker"
    S.apply_material(bunker, S.mat_cladding())

    winch_parts = _winch_drum_assembly()
    sheave_parts = _lower_sheave_assembly()

    assy = bd.Compound(
        children=[apron, plinth, *base_plates, bunker, *winch_parts, *sheave_parts],
        label="foundation",
    )
    bb = assy.bounding_box()
    assert abs(bb.min.Z - 0.0) < 1e-4, bb
    return assy


if __name__ == "__main__":
    foundation()
