"""SpaceX Starlink V2 Mini flat-panel spacecraft bus chassis.

Includes:
- Chamfered octagonal aluminum-lithium structural frame sized for Falcon 9 fairing stacking
- Recessed port/starboard solar array stowage trays with OSR thermal radiator grids
- Elastomeric solar array hold-down snubber pads
- Central dorsal avionics spine with reaction wheel housings and MLI harness channels
- Recessed aft propulsion bulkhead pocket and port/starboard SADA drive housings
- Four corner Falcon 9 tension-rod stack retention hardpoint lugs
"""

import build123d as bd
from bd_materials import metals, plastics
from cad import model
from cad.build123d import materials

from spec import (
    BUS_CORNER_CHAMFER,
    BUS_X,
    BUS_Y,
    BUS_Z,
    NADIR_RECESS_DEPTH,
    RIM_HALF_Y,
    SADA_Z,
    SPINE_HALF_X,
    STACK_LUG_POSITIONS,
    STOW_FLOOR_Z,
)


def _chamfered_rect_wire(width: float, length: float, chamfer: float) -> bd.Face:
    """Create a symmetric octagon (chamfered rectangle) face centered on XY origin."""
    hx = width / 2.0
    hy = length / 2.0
    c = chamfer
    pts = [
        (-hx + c, -hy),
        (hx - c, -hy),
        (hx, -hy + c),
        (hx, hy - c),
        (hx - c, hy),
        (-hx + c, hy),
        (-hx, hy - c),
        (-hx, -hy + c),
    ]
    return bd.Face(bd.Wire.make_polygon(pts))


def _make_chassis_structure() -> bd.Solid:
    """Build the monolithic machined aluminum-lithium flat-panel bus frame."""
    outer_face = _chamfered_rect_wire(BUS_X, BUS_Y, BUS_CORNER_CHAMFER)
    body = bd.extrude(outer_face, BUS_Z)

    cuts = []

    # 1. Recessed port & starboard solar array stowage trays (+Z deck)
    tray_depth = BUS_Z - STOW_FLOOR_Z + 5.0
    tray_w = BUS_X / 2.0 - SPINE_HALF_X + 10.0
    tray_l = 2.0 * RIM_HALF_Y
    for side in (-1.0, 1.0):
        cx = side * (SPINE_HALF_X + tray_w / 2.0)
        cuts.append(
            bd.Pos(cx, 0.0, STOW_FLOOR_Z)
            * bd.Box(
                tray_w,
                tray_l,
                tray_depth,
                align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
            )
        )

    # 2. Recessed nadir (-Z) Earth-facing communications payload bay
    nadir_face = _chamfered_rect_wire(BUS_X - 150.0, BUS_Y - 150.0, BUS_CORNER_CHAMFER - 20.0)
    nadir_cut = bd.Pos(0.0, 0.0, -2.0) * bd.extrude(nadir_face, NADIR_RECESS_DEPTH + 2.0)
    cuts.append(nadir_cut)

    # 3. Recessed aft (-Y) propulsion bay for dual Argon Hall thrusters & manifold
    cuts.append(
        bd.Pos(0.0, -BUS_Y / 2.0 + 60.0, 38.0)
        * bd.Box(
            840.0,
            130.0,
            156.0,
            align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
        )
    )

    # 4. Recessed port & starboard SADA drive pockets at X = +-1350, Y = 0 (Z in [86, 186])
    for side in (-1.0, 1.0):
        cuts.append(
            bd.Pos(side * (BUS_X / 2.0 - 45.0), 0.0, SADA_Z)
            * bd.Rot(0, 90, 0)
            * bd.Cylinder(radius=50.0, height=110.0)
        )

    # 5. Machined aerospace weight-relief shear pockets along +-X side rails
    pocket_ys = (-1560.0, -1120.0, -680.0, -280.0, 280.0, 680.0, 1120.0, 1560.0)
    for side in (-1.0, 1.0):
        for py in pocket_ys:
            cuts.append(
                bd.Pos(side * (BUS_X / 2.0 - 14.0), py, 98.0)
                * bd.Box(34.0, 320.0, 108.0)
            )

    # 6. Fore (+Y) structural shear relief pockets flanking centerline
    for px in (-820.0, -420.0, 420.0, 820.0):
        cuts.append(
            bd.Pos(px, BUS_Y / 2.0 - 14.0, 120.0)
            * bd.Box(290.0, 34.0, 116.0)
        )

    # 7. Aft (-Y) outer structural shear relief pockets flanking propulsion bay
    for px in (-820.0, 820.0):
        cuts.append(
            bd.Pos(px, -BUS_Y / 2.0 + 14.0, 120.0)
            * bd.Box(290.0, 34.0, 116.0)
        )

    chassis = body - cuts
    chassis.label = "chassis_structure"
    chassis.material = materials.anodized("#59626E")
    return chassis


def _make_radiator_tiles() -> list:
    """Build OSR (Optical Solar Reflector) white thermal radiator panels on trays & spine."""
    parts = []
    white_rad = materials.ceramic("white")
    white_rad.pbr = white_rad.pbr.override(roughness=0.22, clearcoat=0.45)

    # Port & Starboard tray thermal radiators (flush at Z = 196.2..200.2 mm)
    # Placed in clean bays |X| in [240, 680] and [750, 1190] so snubber pads & SADA drums stay clear
    tile_w = 440.0
    tile_l = 800.0
    tile_h = 4.0
    x_cols = (460.0, 970.0)
    y_rows = (-1350.0, -450.0, 450.0, 1350.0)

    for side_name, side in (("port", -1.0), ("stbd", 1.0)):
        tiles = []
        for xc in x_cols:
            for yc in y_rows:
                tiles.append(
                    bd.Pos(side * xc, yc, STOW_FLOOR_Z + 0.2)
                    * bd.Box(
                        tile_w,
                        tile_l,
                        tile_h,
                        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
                    )
                )
        comp = bd.Compound(children=tiles, label=f"radiators_{side_name}")
        for child in comp.children:
            child.material = white_rad
            child.label = f"osr_tile_{side_name}"
        parts.append(comp)

    return parts


def _make_snubber_pads() -> bd.Compound:
    """Build solar array hold-down elastomeric snubber pads in both stowage trays."""
    pad_mat = plastics.rubber()
    pad_mat.pbr = pad_mat.pbr.override(roughness=0.72)

    # Stowed panel P1 bottom sits at Z = 225.0 mm -> pad tops at Z = 223.8 mm (1.2 mm clearance)
    # Placed in structural lanes |X| = 198 and 1265 (clear of OSR tiles and SADA at Y = 0)
    pad_h = 223.8 - STOW_FLOOR_Z
    pads = []
    idx = 0
    for side in (-1.0, 1.0):
        for px in (198.0, 1265.0):
            for py in (-1680.0, -880.0, 880.0, 1680.0):
                idx += 1
                base = bd.Cylinder(radius=28.0, height=pad_h - 6.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
                cap = bd.Pos(0.0, 0.0, pad_h - 6.0) * bd.Cone(
                    bottom_radius=26.0,
                    top_radius=19.0,
                    height=6.0,
                    align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
                )
                pad = bd.Pos(side * px, py, STOW_FLOOR_Z + 0.2) * (base + cap)
                pad.label = f"snubber_pad_{idx}"
                pad.material = pad_mat
                pad.color = "#22262C"
                pads.append(pad)

    return bd.Compound(children=pads, label="snubber_pads")


def _make_dorsal_spine_hardware() -> bd.Compound:
    """Build central dorsal spine avionics covers, 4 reaction wheel housings, and MLI cable raceways."""
    children = []
    cover_mat = materials.anodized("#343B45")
    rw_mat = metals.titanium()
    rw_mat.pbr = rw_mat.pbr.override(roughness=0.32)
    mli_mat = metals.gold()
    mli_mat.pbr = mli_mat.pbr.override(roughness=0.30, metalness=0.92)

    # Main central spine avionics deck plate (X in [-112, +112], Y in [-1760, +1760])
    plate = (
        bd.Pos(0.0, 0.0, BUS_Z + 0.2)
        * bd.Box(
            216.0,
            3480.0,
            6.0,
            align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
        )
    )
    plate.label = "avionics_spine_cover"
    plate.material = cover_mat
    children.append(plate)

    # 4 Reaction Wheel Assembly (RWA) housing domes along the dorsal spine
    for i, ry in enumerate((-1150.0, -450.0, 450.0, 1150.0), start=1):
        flange = bd.Cylinder(radius=84.0, height=8.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        dome = bd.Pos(0.0, 0.0, 8.0) * bd.Cone(
            bottom_radius=78.0,
            top_radius=58.0,
            height=14.0,
            align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
        )
        hub = bd.Pos(0.0, 0.0, 22.0) * bd.Cylinder(
            radius=28.0, height=4.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
        )
        rw = bd.Pos(0.0, ry, BUS_Z + 6.4) * (flange + dome + hub)
        rw.label = f"reaction_wheel_housing_{i}"
        rw.material = rw_mat
        children.append(rw)

    # Twin gold Kapton/MLI thermal harness raceways along dorsal spine edges
    for side_name, side in (("port", -1.0), ("stbd", 1.0)):
        raceway = (
            bd.Pos(side * 120.0, 0.0, BUS_Z + 0.2)
            * bd.Box(
                16.0,
                3520.0,
                10.0,
                align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
            )
        )
        raceway.label = f"mli_harness_{side_name}"
        raceway.material = mli_mat
        children.append(raceway)

    return bd.Compound(children=children, label="dorsal_spine_hardware")


def _make_stack_lugs() -> bd.Compound:
    """Build 4 Falcon 9 corner tension-rod stack retention hardpoints."""
    ti = metals.titanium()
    ti.pbr = ti.pbr.override(roughness=0.28)
    lugs = []

    for i, (lx, ly) in enumerate(STACK_LUG_POSITIONS, start=1):
        base = bd.Cylinder(radius=46.0, height=10.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        collar = bd.Pos(0.0, 0.0, 10.0) * bd.Cone(
            bottom_radius=38.0,
            top_radius=28.0,
            height=18.0,
            align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
        )
        bore = bd.Pos(0.0, 0.0, -1.0) * bd.Cylinder(
            radius=13.0, height=32.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
        )
        lug = bd.Pos(lx, ly, BUS_Z + 0.2) * ((base + collar) - bore)
        lug.label = f"stack_lug_{i}"
        lug.material = ti
        lugs.append(lug)

    return bd.Compound(children=lugs, label="stack_retention_lugs")


def _make_sada_housings() -> bd.Compound:
    """Build port and starboard Solar Array Drive Assembly (SADA) stator housings."""
    ti = metals.titanium()
    ti.pbr = ti.pbr.override(roughness=0.26)
    ring_mat = materials.anodized("#242930")
    parts = []

    for side_name, side in (("port", -1.0), ("stbd", 1.0)):
        # Seated cleanly inside the R=50 recess below STOW_FLOOR_Z: drum X in [1265, 1345], bezel X in [1345.5, 1349.5]
        drum = (
            bd.Pos(side * (BUS_X / 2.0 - 45.0), 0.0, SADA_Z)
            * bd.Rot(0, 90, 0)
            * bd.Cylinder(radius=46.0, height=80.0)
        )
        flange = (
            bd.Pos(side * (BUS_X / 2.0 - 10.0), 0.0, SADA_Z)
            * bd.Rot(0, 90, 0)
            * bd.Cylinder(radius=48.0, height=10.0)
        )
        bore = (
            bd.Pos(side * (BUS_X / 2.0 - 45.0), 0.0, SADA_Z)
            * bd.Rot(0, 90, 0)
            * bd.Cylinder(radius=21.0, height=96.0)
        )
        housing = (drum + flange) - bore
        housing.label = f"sada_housing_{side_name}"
        housing.material = ti
        parts.append(housing)

        # Rotary slip-ring encoder bezel
        bezel = (
            bd.Pos(side * (BUS_X / 2.0 - 2.5), 0.0, SADA_Z)
            * bd.Rot(0, 90, 0)
            * (bd.Cylinder(radius=34.0, height=4.0) - bd.Cylinder(radius=21.0, height=8.0))
        )
        bezel.label = f"sada_bezel_{side_name}"
        bezel.material = ring_mat
        parts.append(bezel)

    return bd.Compound(children=parts, label="sada_housings")


@model
def bus_chassis():
    """Complete SpaceX Starlink V2 Mini spacecraft bus structural assembly."""
    chassis = _make_chassis_structure()
    radiators = _make_radiator_tiles()
    snubbers = _make_snubber_pads()
    spine = _make_dorsal_spine_hardware()
    lugs = _make_stack_lugs()
    sadas = _make_sada_housings()

    assembly = bd.Compound(
        children=[chassis, *radiators, snubbers, spine, lugs, sadas],
        label="bus_chassis",
    )
    bb = assembly.bounding_box()
    assert abs(bb.size.X - BUS_X) < 1.0, f"Unexpected bus X size: {bb.size.X}"
    assert abs(bb.size.Y - BUS_Y) < 1.0, f"Unexpected bus Y size: {bb.size.Y}"
    return assembly


if __name__ == "__main__":
    bus_chassis()
