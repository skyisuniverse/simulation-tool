"""Tesla Cybertruck structural chassis, flat battery armor skid pan, wheel wells, brakes, Vault bed, and frunk tub.

All parts stay strictly inside the stainless exoskeleton envelope (inset >= 10 mm) and clear of all
four 285/65R20 wheels (|X| <= 690 mm in wheelhouse regions; brakes inside 20-inch rim barrel).
"""

from __future__ import annotations

import build123d as bd
from cad import model

from lib import geometry, materials, spec


def _build_underbody_skid() -> bd.Solid:
    """Flat armored battery belly pan (Z = 257 mm ground clearance) with approach & departure ramps."""
    # Centerline belly profile in YZ: slopes cleanly up fore/aft for off-road clearance
    # Fore ramp stops at s=420 (front bumper skid meets it cleanly ahead of that);
    # Aft ramp stops at s=5260 (rear bumper diffuser meets it behind that).
    pts_mid = [
        (spec.s_to_y(420.0), 400.0),
        (spec.s_to_y(700.0), spec.Z_BELLY),
        (spec.s_to_y(4950.0), spec.Z_BELLY),
        (spec.s_to_y(5260.0), 420.0),
        (spec.s_to_y(5260.0), 465.0),
        (spec.s_to_y(4920.0), spec.Z_BELLY + 50.0),
        (spec.s_to_y(730.0), spec.Z_BELLY + 50.0),
        (spec.s_to_y(420.0), 445.0),
    ]
    core_pan = geometry.extrude_yz_polygon(pts_mid, -660.0, 660.0)

    # Wide side battery sill extensions between the front and rear wheel wells (s in [1540, 3850])
    sill_y0 = spec.s_to_y(1540.0)
    sill_y1 = spec.s_to_y(3850.0)
    side_box = bd.Pos(0.0, (sill_y0 + sill_y1) / 2.0, spec.Z_BELLY + 25.0) * bd.Box(
        1840.0, sill_y1 - sill_y0, 50.0
    )
    pan = core_pan + side_box
    return materials.apply_mat(pan, materials.underbody_skid_metal, "battery_skid_pan")


def _build_structural_tub() -> bd.Solid:
    """Dark inner unibody chassis core, door seam backing, wheelhouse tubs, and rear bulkhead."""
    # 1. Lower structural inner shell backing the stainless doors & fenders (inset 14 mm from skin).
    # Starts at s=265 (aft of front bumper, headlight backing, DRL bezel) and ends at s=5575 (ahead of rear bumper).
    stations = [
        (265.0, 675.0),
        (878.3, 370.0),
        (1485.0, 370.0),
        (2630.0, 370.0),
        (3730.0, 370.0),
        (4513.3, 370.0),
        (5160.0, 370.0),
        (5575.0, 655.0),
    ]
    sections = []
    for s, z_lo in stations:
        y = spec.s_to_y(s)
        xb_lo = spec.x_rocker(s) - 24.0
        xb_hi = spec.x_belt(s) - 16.0
        zb_hi = spec.z_belt(s) - 10.0
        sections.append([
            (xb_lo, y, z_lo),
            (xb_hi, y, zb_hi),
            (-xb_hi, y, zb_hi),
            (-xb_lo, y, z_lo),
        ])
    tub = geometry.ruled_loft_sections(sections)

    # Subtract deep wheelhouse pockets at front and rear axles so tires + suspension clear generously
    # Pocket extends inward to |X| = 685 mm (51 mm clear of tire inner sidewall at 736 mm)
    for s_axle in (spec.S_FRONT_AXLE, spec.S_REAR_AXLE):
        yc = spec.s_to_y(s_axle)
        # Trapezoidal wheel well pocket slightly larger than arch opening
        pts_well = [
            (yc - 590.0, 290.0),
            (yc - 350.0, 960.0),
            (yc + 350.0, 960.0),
            (yc + 590.0, 290.0),
        ]
        left_well = geometry.extrude_yz_polygon(pts_well, 685.0, 1100.0)
        right_well = geometry.extrude_yz_polygon(pts_well, -1100.0, -685.0)
        tub = tub - [left_well, right_well]

    # Carve out the cabin interior footwell/seating volume (s in [1220, 3720], Z >= 380)
    # Keeping the firewall solid ahead of s=1220 seals the rear of the front wheelhouse completely.
    cab_y0 = spec.s_to_y(1220.0)
    cab_y1 = spec.s_to_y(3720.0)
    cab_cut = bd.Pos(0.0, (cab_y0 + cab_y1) / 2.0, 380.0) * bd.Box(
        1680.0,
        cab_y1 - cab_y0,
        1100.0,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )

    # Carve out the Vault cargo bed cavity (s in [3775, 5620], Z >= 835, |X| <= 725)
    bed_y0 = spec.s_to_y(3775.0)
    bed_y1 = spec.s_to_y(5620.0)
    bed_cut = bd.Pos(0.0, (bed_y0 + bed_y1) / 2.0, 835.0) * bd.Box(
        1450.0,
        bed_y1 - bed_y0,
        900.0,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )

    # Carve out the front frunk tub cavity & low-lip opening (s in [190, 770], Z >= 700, |X| <= 620)
    frunk_y0 = spec.s_to_y(190.0)
    frunk_y1 = spec.s_to_y(770.0)
    frunk_cut = bd.Pos(0.0, (frunk_y0 + frunk_y1) / 2.0, 700.0) * bd.Box(
        1240.0,
        frunk_y1 - frunk_y0,
        550.0,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )

    tub = tub - [cab_cut, bed_cut, frunk_cut]

    # Add upper dark inner sail-pillar / cab-bulkhead structural backing (inset behind stainless sail pillars)
    s_c = spec.S_CAB_REAR
    s_t = spec.S_TAILGATE_TOP - 35.0
    bulk_pts = [
        (spec.s_to_y(s_c - 30.0), spec.z_belt(s_c) - 10.0),
        (spec.s_to_y(s_c - 30.0), spec.z_roof(s_c) - 45.0),
        (spec.s_to_y(s_c + 10.0), spec.z_roof(s_c) - 45.0),
        (spec.s_to_y(s_c + 10.0), spec.z_belt(s_c) - 10.0),
    ]
    rear_bulkhead_top = geometry.extrude_yz_polygon(bulk_pts, -715.0, 715.0)
    tub = tub + rear_bulkhead_top

    # Carve out front & rear axle / drive-unit bays so drivetrain_axles and suspension clear completely
    axle_cuts = []
    for s_axle in (spec.S_FRONT_AXLE, spec.S_REAR_AXLE):
        yc = spec.s_to_y(s_axle)
        bay = bd.Pos(0.0, yc, 250.0) * bd.Box(
            1800.0, 420.0, 340.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
        )
        axle_cuts.append(bay)

    # Ensure strictly above battery skid pan ramps (s<=710 & s>=4940) and front/rear bumper wings
    fore_ramp_cut = bd.Pos(0.0, spec.s_to_y(500.0), 672.0) * bd.Box(
        2200.0, 620.0, 500.0, align=(bd.Align.CENTER, bd.Align.MAX, bd.Align.MAX)
    )
    fore_skid_cut = bd.Pos(0.0, spec.s_to_y(715.0), 460.0) * bd.Box(
        1600.0, 400.0, 300.0, align=(bd.Align.CENTER, bd.Align.MAX, bd.Align.MAX)
    )
    aft_ramp_cut = bd.Pos(0.0, spec.s_to_y(5155.0), 652.0) * bd.Box(
        2200.0, 720.0, 500.0, align=(bd.Align.CENTER, bd.Align.MIN, bd.Align.MAX)
    )
    aft_skid_cut = bd.Pos(0.0, spec.s_to_y(4940.0), 475.0) * bd.Box(
        1600.0, 450.0, 300.0, align=(bd.Align.CENTER, bd.Align.MIN, bd.Align.MAX)
    )
    below_cut = bd.Pos(0.0, 0.0, 368.0) * bd.Box(
        2400.0, 6200.0, 400.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MAX)
    )
    tub = tub - [below_cut, fore_ramp_cut, fore_skid_cut, aft_ramp_cut, aft_skid_cut, *axle_cuts]

    # Add matte-black inner wheelhouse arch shields sealing the top of all 4 wheel wells (zero daylight!)
    # Sits strictly outboard of vault_bed_liner (718) & cabin dash (750) and inboard of stainless skin (885)
    liners = []
    for s_axle in (spec.S_FRONT_AXLE, spec.S_REAR_AXLE):
        pts_in = spec.arch_polygon_2d(s_axle, expand=6.0)
        pts_out = spec.arch_polygon_2d(s_axle, expand=24.0)
        shield_outer = geometry.extrude_yz_polygon(pts_out, 755.0, 885.0)
        shield_inner = geometry.extrude_yz_polygon(pts_in, 745.0, 895.0)
        shield_l = shield_outer - shield_inner
        trim_lo = bd.Pos(820.0, spec.s_to_y(s_axle), 685.0) * bd.Box(
            260.0, 1600.0, 500.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MAX)
        )
        shield_l = shield_l - trim_lo
        shield_r = bd.mirror(shield_l, about=bd.Plane.YZ)
        liners.extend([shield_l, shield_r])
    tub = tub + liners

    return materials.apply_mat(tub, materials.dark_charcoal_trim, "structural_tub")


def _build_vault_bed() -> bd.Solid:
    """The Vault: ribbed 6-foot composite cargo bed floor, sloped inner walls, and front bulkhead."""
    y0 = spec.s_to_y(spec.BED_S_FRONT)
    y1 = spec.s_to_y(spec.BED_S_REAR - 8.0)  # s=5597 (11 mm clear ahead of closed tailgate s=5608)
    bed_len = y1 - y0
    y_mid = (y0 + y1) / 2.0
    hw_floor = spec.BED_INNER_HALF_W       # 647.5 mm (1295 mm floor width)
    hw_outer = 718.0                        # fits strictly inside bed_cut (725 mm)
    z_floor_bot = 838.0
    z_floor_top = spec.Z_BED_FLOOR          # 865.0 mm

    # Bed floor slab
    floor = bd.Pos(0.0, y_mid, z_floor_bot) * bd.Box(
        hw_outer * 2.0,
        bed_len,
        z_floor_top - z_floor_bot,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )

    # 9 longitudinal anti-slip cargo ribs on the Vault bed floor
    ribs = []
    for i in range(-4, 5):
        rx = i * 138.0
        rib = bd.Pos(rx, y_mid, z_floor_top) * bd.Box(
            26.0,
            bed_len - 40.0,
            7.0,
            align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
        )
        ribs.append(rib)

    # Sloped left & right inner cargo bed walls rising to just below the tonneau cover track
    z_top_f = spec.z_roof(spec.BED_S_FRONT) - 38.0
    z_top_r = spec.z_roof(spec.BED_S_REAR) - 38.0
    wall_yz = [
        (y0, z_floor_top),
        (y0, z_top_f),
        (y1, z_top_r),
        (y1, z_floor_top),
    ]
    left_wall = geometry.extrude_yz_polygon(wall_yz, hw_floor, hw_outer)
    right_wall = geometry.extrude_yz_polygon(wall_yz, -hw_outer, -hw_floor)

    # Front bed bulkhead wall
    front_wall = bd.Pos(0.0, y0 + 18.0, z_floor_top) * bd.Box(
        hw_outer * 2.0,
        36.0,
        z_top_f - z_floor_top,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )

    bed = floor + [left_wall, right_wall, front_wall, *ribs]
    return materials.apply_mat(bed, materials.dark_charcoal_trim, "vault_bed_liner")


def _build_frunk_tub() -> bd.Solid:
    """Molded composite front trunk (frunk) cargo basin with Cybertruck's signature low front lip."""
    y0 = spec.s_to_y(220.0)
    y1 = spec.s_to_y(755.0)
    y_mid = (y0 + y1) / 2.0
    length = y1 - y0
    outer_w = 1200.0
    wall_t = 22.0
    z_bot = 710.0
    z_rear_top = 980.0
    z_front_lip = 755.0

    # Tapered tub outer shell following the sloped hood clearance
    yz_outer = [
        (y0, z_bot),
        (y0, z_front_lip),
        (y0 + 140.0, 920.0),
        (y1, z_rear_top),
        (y1, z_bot),
    ]
    outer = geometry.extrude_yz_polygon(yz_outer, -outer_w / 2.0, outer_w / 2.0)

    # Hollow interior storage volume
    yz_inner = [
        (y0 + wall_t, z_bot + 24.0),
        (y0 + wall_t, z_front_lip + 40.0),
        (y1 - wall_t, z_rear_top + 40.0),
        (y1 - wall_t, z_bot + 24.0),
    ]
    inner = geometry.extrude_yz_polygon(yz_inner, -outer_w / 2.0 + wall_t, outer_w / 2.0 - wall_t)
    tub = outer - inner
    return materials.apply_mat(tub, materials.matte_black_cladding, "frunk_tub")


def _build_drivetrain_and_brakes() -> list[bd.Solid]:
    """Dual drive axles, suspension control-arm links, 390 mm ventilated brake rotors, and calipers."""
    parts = []
    z_ax = spec.AXLE_Z

    # Axle half-shaft housings & suspension struts (clear of skid pan Z <= 308 and inner rim |X| <= 834)
    axles_all = None
    for s_axle in (spec.S_FRONT_AXLE, spec.S_REAR_AXLE):
        yc = spec.s_to_y(s_axle)
        # Main transverse drive unit / axle shaft (|X| <= 786 mm, clears rotor inner face 798 mm)
        shaft = (
            bd.Pos(0.0, yc, z_ax)
            * bd.Rot(0.0, 90.0, 0.0)
            * bd.Cylinder(34.0, 1572.0)
        )
        # Central motor / differential housing block
        diff = bd.Pos(0.0, yc, z_ax) * bd.Box(340.0, 230.0, 190.0)
        # Upper & lower A-arm suspension links (between X = +-640 and X = +-775)
        arms = []
        for sx in (-1.0, 1.0):
            arm_lo = bd.Pos(sx * 700.0, yc, z_ax - 75.0) * bd.Box(145.0, 110.0, 26.0)
            arm_hi = bd.Pos(sx * 700.0, yc, z_ax + 90.0) * bd.Box(135.0, 90.0, 24.0)
            upright = bd.Pos(sx * 772.0, yc, z_ax) * bd.Box(28.0, 115.0, 200.0)
            arms.extend([arm_lo, arm_hi, upright])
        grp = shaft + [diff, *arms]
        axles_all = grp if axles_all is None else (axles_all + grp)

    parts.append(materials.apply_mat(axles_all, materials.underbody_skid_metal, "drivetrain_axles"))

    # 4 Ventilated Brake Rotors (R = 188 mm, |X| in [798, 818] -> strictly inside 20" rim R_in=226, web X=840)
    rotors_all = None
    calipers_all = None
    for s_axle in (spec.S_FRONT_AXLE, spec.S_REAR_AXLE):
        yc = spec.s_to_y(s_axle)
        for sx in (-1.0, 1.0):
            x_rot = sx * (spec.TRACK_HALF - 66.0)  # +/-808 mm (extends 798..818)
            disc = (
                bd.Pos(x_rot, yc, z_ax)
                * bd.Rot(0.0, 90.0, 0.0)
                * bd.Cylinder(188.0, 20.0)
            )
            hat = (
                bd.Pos(x_rot, yc, z_ax)
                * bd.Rot(0.0, 90.0, 0.0)
                * bd.Cylinder(88.0, 24.0)
            )
            bore = (
                bd.Pos(x_rot, yc, z_ax)
                * bd.Rot(0.0, 90.0, 0.0)
                * bd.Cylinder(40.0, 40.0)
            )
            rotor = (disc + hat) - bore
            rotors_all = rotor if rotors_all is None else (rotors_all + rotor)

            # Heavy brake caliper gripping the disc (|X| in [789, 827] -> 13 mm clear of rim web at 840!)
            cal_y = yc + (135.0 if s_axle == spec.S_FRONT_AXLE else -135.0)
            cal_outer = bd.Pos(x_rot, cal_y, z_ax + 24.0) * bd.Box(38.0, 82.0, 136.0)
            # Carve disc slot through caliper so it never overlaps the rotor
            slot = (
                bd.Pos(x_rot, yc, z_ax)
                * bd.Rot(0.0, 90.0, 0.0)
                * bd.Cylinder(192.0, 26.0)
            )
            caliper = cal_outer - slot
            calipers_all = caliper if calipers_all is None else (calipers_all + caliper)

    parts.append(materials.apply_mat(rotors_all, materials.brake_rotor_steel, "brake_rotors"))
    parts.append(materials.apply_mat(calipers_all, materials.brake_caliper, "brake_calipers"))
    return parts


@model
def cybertruck_chassis():
    """Complete Cybertruck underbody armor, structural inner tub, Vault cargo bed, frunk tub, and brakes."""
    skid = _build_underbody_skid()
    tub = _build_structural_tub()
    bed = _build_vault_bed()
    frunk = _build_frunk_tub()
    drivetrain = _build_drivetrain_and_brakes()

    assy = bd.Compound(
        children=[skid, tub, bed, frunk, *drivetrain],
        label="cybertruck_chassis",
    )
    bb_skid = skid.bounding_box()
    assert abs(bb_skid.min.Z - spec.GROUND_CLEARANCE) < 1.0, (
        f"Unexpected underbody ground clearance: {bb_skid.min.Z}"
    )
    return assy


if __name__ == "__main__":
    cybertruck_chassis()
