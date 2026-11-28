"""Carbon monocoque chassis, ground-effect floor, rising carbon rocker skirts,
front aero splitter & intake, rear diffuser housing, 4 ducted suction fans,
4 rear cold-gas thrusters, and 4 underside perimeter thruster nozzles.
"""

import math

import build123d as bd
from cad import model
from cad.build123d import memo

from body_surface import (
    front_trapezoid_intake_cut,
    master_body_solid,
    rocker_split_volume,
    wheel_arch_cutters,
)
from spec import (
    DOOR_Y_FRONT_BOT,
    DOOR_Y_REAR_BOT,
    TIRE_F_RADIUS,
    TIRE_R_RADIUS,
    Y_FRONT_AXLE,
    Y_NOSE,
    Y_REAR_AXLE,
    Y_TAIL,
    Z_FLOOR,
    apply_bronze_titanium,
    apply_carbon_black,
    apply_dark_gloss,
    apply_dark_titanium,
    apply_titanium,
)


def _front_splitter():
    """Sleek carbon-fiber front splitter hugging the nose cheeks & chin intake."""
    pts_plan = [
        (-865.0, Y_NOSE + 390.0),
        (-785.0, Y_NOSE + 148.0),
        (-595.0, Y_NOSE - 12.0),
        (595.0, Y_NOSE - 12.0),
        (785.0, Y_NOSE + 148.0),
        (865.0, Y_NOSE + 390.0),
    ]
    face = bd.Face(bd.Wire.make_polygon([bd.Vector(x, y, Z_FLOOR) for x, y in pts_plan]))
    slab = bd.extrude(face, 30.0, dir=(0, 0, 1))

    # Crisp forward-swept chin chamfer on the leading edge
    bevel_pts = [
        (Y_NOSE - 18.0, Z_FLOOR + 24.0),
        (Y_NOSE + 12.0, Z_FLOOR),
        (Y_NOSE - 18.0, Z_FLOOR),
    ]
    bevel_face = bd.Face(bd.Wire.make_polygon([bd.Vector(-1000.0, y, z) for y, z in bevel_pts]))
    bevel_cut = bd.extrude(bevel_face, 2000.0, dir=(1, 0, 0))
    splitter = slab - bevel_cut
    splitter = splitter - wheel_arch_cutters(extra_r=8.0, extra_depth=35.0)
    splitter.label = "front_splitter"
    apply_carbon_black(splitter)
    return splitter


def _front_intake_grille():
    """Recessed satin-dark front nose fascia, horizontal aero vane, and deep intake duct."""
    # Intersected strictly with front_trapezoid_intake_cut() so it seats flush inside
    # the front nose mouth carved in body.py with ZERO overlap against ano_white_body!
    backing = bd.Pos(0.0, Y_NOSE + 95.0, 272.0) * bd.Box(1400.0, 46.0, 250.0)
    upper_fascia = bd.Pos(0.0, Y_NOSE + 42.0, 355.0) * bd.Box(1220.0, 56.0, 88.0)
    aero_vane = bd.Pos(0.0, Y_NOSE + 46.0, 224.0) * bd.Box(1260.0, 62.0, 16.0)
    master = master_body_solid()
    intake_vol = front_trapezoid_intake_cut() & master
    grille = (backing + upper_fascia + aero_vane) & intake_vol
    grille.label = "front_intake_fascia"
    apply_dark_gloss(grille)
    return grille


def _lower_rocker_and_tub():
    """Flush carbon lower rocker skirts, flat suction undertray, and cabin entry sills."""
    master = master_body_solid()
    lower = master & rocker_split_volume()

    # Cut wheel arches (slightly wider than tire so wheel wells look crisp)
    lower = lower - wheel_arch_cutters(extra_r=2.0)

    # Carve front intake mouth cavity at the nose
    front_mouth = bd.Pos(0.0, Y_NOSE + 35.0, 225.0) * bd.Box(1180.0, 130.0, 165.0)
    lower = lower - front_mouth

    # Carve deep central rear diffuser bay (housing the 4 thrusters + 4 suction fans)
    diffuser_cut = bd.Pos(0.0, Y_TAIL - 180.0, 305.0) * bd.Box(1220.0, 360.0, 380.0)
    # Carve outer rear corner aero vents beneath the light bar
    rear_corner_l = bd.Pos(775.0, Y_TAIL - 90.0, 445.0) * bd.Box(260.0, 180.0, 140.0)
    rear_corner_r = bd.Pos(-775.0, Y_TAIL - 90.0, 445.0) * bd.Box(260.0, 180.0, 140.0)
    lower = lower - [diffuser_cut, rear_corner_l, rear_corner_r]

    # Carve cabin interior footwell / seat recess down to floor thickness (Z = 165)
    cabin_floor_cut = bd.Pos(0.0, -180.0, 365.0) * bd.Box(1420.0, 1420.0, 400.0)
    lower = lower - cabin_floor_cut

    # Add crisp sculpted carbon cabin entry door sills + front/rear tub bulkheads
    # (visible when the dihedral doors swing upward in showroom pose!)
    sill_l = bd.Pos(775.0, -240.0, 192.0) * bd.Box(135.0, 1420.0, 44.0)
    sill_r = bd.Pos(-775.0, -240.0, 192.0) * bd.Box(135.0, 1420.0, 44.0)
    lower = (lower + sill_l + sill_r) & master

    # Subtle protective underbody suction floor plate extending cleanly across rear
    undertray = bd.Pos(0.0, 120.0, Z_FLOOR + 16.0) * bd.Box(1360.0, 3500.0, 32.0)
    undertray = undertray & master
    lower = lower + undertray

    lower.label = "carbon_chassis_rockers"
    apply_carbon_black(lower)
    return lower


def _rear_diffuser_structure():
    """Carbon rear diffuser surround frame, 2 ground-sealing side strakes,
    horizontal bay shelf, and 3 vertical fan-tunnel partition fins.
    """
    y_back = Y_TAIL - 78.0  # Flush with undercut rear diffuser plane
    parts = []

    # Deep rear diffuser backing bulkhead
    back_wall = bd.Pos(0.0, y_back - 190.0, 308.0) * bd.Box(1230.0, 30.0, 385.0)
    parts.append(back_wall)

    # Top arched surround beam framing the 4 upper thrusters
    top_beam = bd.Pos(0.0, y_back - 75.0, 488.0) * bd.Box(1250.0, 210.0, 26.0)
    parts.append(top_beam)

    # Bottom diffuser floor lip curving gently upward at exit
    bot_floor = bd.Pos(0.0, y_back - 80.0, 118.0) * bd.Box(1240.0, 220.0, 20.0)
    parts.append(bot_floor)

    # Horizontal divider shelf separating upper 4 thrusters from lower 4 suction fans
    mid_shelf = bd.Pos(0.0, y_back - 70.0, 344.0) * bd.Box(1210.0, 200.0, 18.0)
    parts.append(mid_shelf)

    # 2 bold vertical ground-sealing side strakes / skegs (descending to Z = 95 mm!)
    for sign in (1, -1):
        strake_pts = [
            (y_back - 210.0, 102.0),
            (y_back + 28.0, 95.0),
            (y_back + 12.0, 145.0),
            (y_back - 10.0, 486.0),
            (y_back - 210.0, 486.0),
        ]
        s_face = bd.Face(
            bd.Wire.make_polygon([bd.Vector(sign * 612.0 - 14.0, y, z) for y, z in strake_pts])
        )
        strake = bd.extrude(s_face, 28.0, dir=(1, 0, 0))
        parts.append(strake)

    # 3 vertical carbon partition fins dividing the lower bay into 4 fan tunnels
    for x_fin in (-264.0, 0.0, 264.0):
        fin_pts = [
            (y_back - 190.0, 124.0),
            (y_back + 10.0, 124.0),
            (y_back - 6.0, 340.0),
            (y_back - 190.0, 340.0),
        ]
        f_face = bd.Face(
            bd.Wire.make_polygon([bd.Vector(x_fin - 8.0, y, z) for y, z in fin_pts])
        )
        fin = bd.extrude(f_face, 16.0, dir=(1, 0, 0))
        parts.append(fin)

    diffuser = parts[0]
    for p in parts[1:]:
        diffuser = diffuser + p
    diffuser.label = "rear_diffuser"
    apply_carbon_black(diffuser)
    return diffuser


def _single_thruster_nozzle():
    """One machined aerospace cold-gas thruster nozzle (bright titanium lip + bronze bell)."""
    # Outer metallic titanium collar ring (Y in [-18, +18])
    outer_rim = bd.Cylinder(58.0, 36.0) - bd.Cylinder(47.0, 42.0)
    outer_rim = bd.Rot(-90, 0, 0) * outer_rim
    outer_rim.label = "nozzle_rim"
    apply_titanium(outer_rim)

    # Tapered de Laval expansion cone inside (Y in [-100, +10])
    bell_outer = bd.Cone(46.0, 34.0, 110.0)
    bell_inner = bd.Pos(0, 0, 12.0) * bd.Cone(42.0, 24.0, 102.0)
    bell = bell_outer - bell_inner
    bell = bd.Pos(0, -45.0, 0) * (bd.Rot(-90, 0, 0) * bell)
    bell.label = "nozzle_bell"
    apply_bronze_titanium(bell)

    # Dark inner throat core seated cleanly behind the bell (Y in [-126, -101])
    throat = bd.Pos(0, -113.5, 0) * (bd.Rot(-90, 0, 0) * bd.Cylinder(28.0, 25.0))
    throat.label = "nozzle_throat"
    apply_dark_gloss(throat)

    return bd.Compound(children=[outer_rim, bell, throat], label="rear_thruster")


def _single_suction_fan():
    """One circular multi-mode ducted suction fan (shroud + bullet hub + 7 twisted blades)."""
    # Built facing +Y rearward, centered at origin
    shroud = bd.Cylinder(100.0, 95.0) - bd.Cylinder(88.0, 105.0)
    shroud = bd.Rot(-90, 0, 0) * shroud
    shroud.label = "fan_shroud"
    apply_dark_titanium(shroud)

    # Central bullet spinner hub + recessed dark center bore
    hub_cyl = bd.Cylinder(31.0, 62.0)
    hub_cone = bd.Pos(0, 0, 44.0) * bd.Cone(31.0, 19.0, 26.0)
    hub_bore = bd.Pos(0, 0, 52.0) * bd.Cylinder(12.0, 24.0)
    hub = (hub_cyl + hub_cone) - hub_bore
    hub = bd.Rot(-90, 0, 0) * hub
    hub.label = "fan_hub"
    apply_dark_titanium(hub)

    # 7 pitched aero fan blades trimmed cleanly between hub OD (31.5) and shroud ID (86.5)
    blade_solids = []
    for i in range(7):
        ang = i * (360.0 / 7.0)
        b = bd.Box(58.0, 34.0, 5.5)
        b = bd.Rot(32.0, 0, 0) * b
        b = bd.Pos(56.0, 0.0, 0.0) * b
        b = bd.Rot(0, 0, ang) * b
        blade_solids.append(b)
    blades = blade_solids[0]
    for b in blade_solids[1:]:
        blades = blades + b
    blades = (blades & bd.Cylinder(86.5, 90.0)) - bd.Cylinder(31.5, 95.0)
    blades = bd.Rot(-90, 0, 0) * blades
    blades.label = "fan_blades"
    apply_carbon_black(blades)

    return bd.Compound(children=[shroud, hub, blades], label="suction_fan")


PERIMETER_NOZZLE_PLACEMENTS = (
    ("thruster_fl", (720.0, -910.0, 130.0)),
    ("thruster_fr", (-720.0, -910.0, 130.0)),
    ("thruster_rl", (725.0, 1875.0, 148.0)),
    ("thruster_rr", (-725.0, 1875.0, 148.0)),
)


def _perimeter_vertical_nozzles():
    """4 downward-facing vertical cold-gas perimeter thruster nozzles (Rocket/Thrust spec)."""
    # Cone height=56 -> Z in [-28, +28]; actuator height=24 seated at Z=+40.5 -> Z in [28.5, 52.5]
    bell_o = bd.Cone(28.0, 17.0, 56.0)
    bell_i = bd.Pos(0, 0, -6.0) * bd.Cone(24.0, 12.0, 52.0)
    bell = bell_o - bell_i
    bell.label = "perimeter_bell"
    apply_bronze_titanium(bell)

    mount = bd.Pos(0, 0, 40.5) * bd.Cylinder(22.0, 24.0)
    mount.label = "perimeter_actuator"
    apply_dark_titanium(mount)

    proto = bd.Compound(children=[bell, mount], label="perimeter_nozzle")

    children = []
    for name, pos in PERIMETER_NOZZLE_PLACEMENTS:
        inst = bd.Pos(*pos) * proto
        inst.label = name
        children.append(inst)
    return bd.Compound(children=children, label="perimeter_thrusters")


@memo
def _build_chassis():
    y_back = Y_TAIL - 78.0

    rockers = _lower_rocker_and_tub()
    splitter = _front_splitter()
    grille = _front_intake_grille()
    diffuser = _rear_diffuser_structure()

    # Fuse unified structural carbon chassis (rockers + splitter + rear diffuser)
    # Trim cleanly to rocker_split_volume (zero overlap with ano_white_body!) and
    # carve generous wheel-well clearance (zero overlap with all 4 tires/spokes!).
    nozzle_pockets = [
        bd.Pos(pos[0], pos[1], pos[2] + 14.0) * bd.Cylinder(32.0, 100.0)
        for _, pos in PERIMETER_NOZZLE_PLACEMENTS
    ]
    carbon_chassis = (rockers + splitter + diffuser) & rocker_split_volume()
    carbon_chassis = carbon_chassis - [
        grille,
        *nozzle_pockets,
        *wheel_arch_cutters(extra_r=8.0, extra_depth=35.0),
    ]
    carbon_chassis.label = "carbon_chassis"
    apply_carbon_black(carbon_chassis)

    # 4 Rear Cold-Gas Thruster Nozzles (upper diffuser bay)
    thruster_proto = _single_thruster_nozzle()
    thrusters = []
    for idx, x_pos in enumerate((-375.0, -125.0, 125.0, 375.0), start=1):
        t = bd.Pos(x_pos, y_back - 32.0, 416.0) * thruster_proto
        t.label = f"rear_thruster_{idx}"
        thrusters.append(t)
    thruster_bank = bd.Compound(children=thrusters, label="rear_thrusters")

    # 4 Circular Multi-Mode Suction Fans (lower diffuser bay)
    fan_proto = _single_suction_fan()
    fans = []
    for idx, x_pos in enumerate((-396.0, -132.0, 132.0, 396.0), start=1):
        f = bd.Pos(x_pos, y_back - 85.0, 230.0) * fan_proto
        f.label = f"suction_fan_{idx}"
        fans.append(f)
    fan_bank = bd.Compound(children=fans, label="suction_fans")

    perimeter = _perimeter_vertical_nozzles()

    return bd.Compound(
        children=[
            carbon_chassis,
            grille,
            thruster_bank,
            fan_bank,
            perimeter,
        ],
        label="chassis",
    )


@model
def chassis():
    """Complete carbon chassis, front splitter, rising rockers, diffuser, 4 fans & 8 thrusters."""
    return _build_chassis()


if __name__ == "__main__":
    chassis()
