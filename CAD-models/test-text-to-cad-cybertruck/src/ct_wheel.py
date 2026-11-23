"""20-inch Tesla Cybertruck Cyber Wheel, 7-spoke geometric aero cover, and 285/65R20 AT tire.

Local frame:
  Origin (0, 0, 0) is the wheel center.
  +X is outboard (exterior aero-cover face for a left-side wheel); -X is inboard.
  Revolving around X places the wheel upright so its outer diameter spans Y and Z (+/-439.5 mm).
"""

from __future__ import annotations

import math

import build123d as bd
from cad import model

from lib import materials, spec

NUM_SPOKES = 7
NUM_SHOULDER_LUGS = 28  # 4x7 harmonious AT tread pitch


def _build_tire() -> bd.Solid:
    """Build the 285/65R20 Goodyear Wrangler Territory RT tire with tread grooves and 7 sidewall lugs."""
    r_od = spec.TIRE_RADIUS          # 439.5 mm
    r_bead = spec.RIM_RADIUS - 2.0   # 252.0 mm (sits cleanly over rim flange)
    hw = spec.TIRE_WIDTH / 2.0       # 138.0 mm
    tread_hw = 114.0                 # tread contact patch half-width
    g_depth = 8.5                    # circumferential groove depth
    g_w = 5.5                        # groove half-width

    # Cross-section in XZ plane (X = axial, Z = radial > 0), revolved 360 deg around X axis.
    # Four circumferential tread grooves built directly into the revolved profile.
    pts_xz = [
        (-102.0, r_bead),
        (-112.0, r_bead + 12.0),
        (-hw + 4.0, 315.0),
        (-hw, 355.0),
        (-hw + 5.0, 398.0),
        (-tread_hw - 10.0, r_od - 12.0),
        (-tread_hw, r_od - 2.0),
        # Outer tread crown with 4 clean circumferential grooves
        (-74.0, r_od),
        (-71.0, r_od - g_depth),
        (-61.0, r_od - g_depth),
        (-58.0, r_od),
        (-28.0, r_od),
        (-25.0, r_od - g_depth),
        (-15.0, r_od - g_depth),
        (-12.0, r_od),
        (12.0, r_od),
        (15.0, r_od - g_depth),
        (25.0, r_od - g_depth),
        (28.0, r_od),
        (58.0, r_od),
        (61.0, r_od - g_depth),
        (71.0, r_od - g_depth),
        (74.0, r_od),
        (tread_hw, r_od - 2.0),
        (tread_hw + 10.0, r_od - 12.0),
        (hw - 5.0, 398.0),
        (hw, 355.0),
        (hw - 4.0, 315.0),
        (112.0, r_bead + 12.0),
        (102.0, r_bead),
        # Inner cavity return (thick hollow tire carcass wall)
        (96.0, r_bead + 24.0),
        (106.0, 360.0),
        (94.0, r_od - 36.0),
        (-94.0, r_od - 36.0),
        (-106.0, 360.0),
        (-96.0, r_bead + 24.0),
    ]
    wire = bd.Wire.make_polygon([(x, 0.0, z) for x, z in pts_xz])
    face = bd.Face(wire)
    tire = bd.revolve(face, axis=bd.Axis.X, revolution_arc=360.0)

    # Cut 28 bold all-terrain radial tread notches across both outer shoulders in one batch
    notch_tools = []
    for i in range(NUM_SHOULDER_LUGS):
        deg = i * (360.0 / NUM_SHOULDER_LUGS)
        rad = math.radians(deg)
        # Alternate subtle pitch offset for authentic AT tread
        r_mid = r_od - 5.0
        for side_sign in (-1.0, 1.0):
            # Angled shoulder lug notch block
            block = bd.Box(54.0, 16.0, 26.0)
            block = (
                bd.Rot(deg, 0.0, 0.0)
                * bd.Pos(side_sign * 96.0, 0.0, r_mid)
                * bd.Rot(0.0, 0.0, side_sign * 14.0)
                * block
            )
            notch_tools.append(block)
        # Center cross-sipe notches every second pitch
        if i % 2 == 0:
            c_notch = bd.Box(112.0, 11.0, 18.0)
            c_notch = (
                bd.Rot(deg + 6.4, 0.0, 0.0)
                * bd.Pos(0.0, 0.0, r_od - 2.0)
                * bd.Rot(0.0, 0.0, 12.0)
                * c_notch
            )
            notch_tools.append(c_notch)
    tire = tire - notch_tools

    # Add the signature Cybertruck Goodyear 7 geometric raised sidewall alignment lugs on outboard (+X) face
    sidewall_lugs = []
    for k in range(NUM_SPOKES):
        deg = k * (360.0 / NUM_SPOKES)
        # Faceted trapezoidal raised rubber rib continuing each aero wheel spoke onto the sidewall
        p_in = (122.0, 0.0, 266.0)
        # Tapered faceted rubber sidewall lug flush with tire max width (hw = 138 mm)
        lug_yz = [
            (-36.0, 266.0),
            (-26.0, 368.0),
            (26.0, 368.0),
            (36.0, 266.0),
        ]
        f_inner = bd.Face(bd.Wire.make_polygon([(120.0, y, z) for y, z in lug_yz]))
        lug_outer_yz = [
            (-24.0, 272.0),
            (-16.0, 356.0),
            (16.0, 356.0),
            (24.0, 272.0),
        ]
        f_outer = bd.Face(bd.Wire.make_polygon([(hw - 1.5, y, z) for y, z in lug_outer_yz]))
        lug = bd.loft([f_inner, f_outer], ruled=True)
        lug = bd.Rot(deg, 0.0, 0.0) * lug
        sidewall_lugs.append(lug)

    tire = tire + sidewall_lugs
    return materials.apply_mat(tire, materials.tire_rubber, "tire")


def _build_alloy_rim() -> bd.Solid:
    """Build the 20x9J forged dark-gunmetal alloy wheel barrel & hub mounting face."""
    r_flange = spec.RIM_RADIUS - 3.0  # 251.0 mm (1 mm radial clearance inside tire bead 252.0)
    r_barrel = r_flange - 13.0        # 238.0 mm outer barrel
    r_inner = r_barrel - 12.0         # 226.0 mm inner barrel bore
    r_hub = 88.0
    r_bore = 35.0

    # Clean non-self-intersecting revolved cross-section in XZ (X in [-102, +104], Z in [35, 251]):
    # Outer boundary runs left-to-right at top; inner boundary runs right-to-left below it.
    pts_xz = [
        (-102.0, r_flange),
        (-92.0, r_flange),
        (-86.0, r_barrel),
        (86.0, r_barrel),
        (94.0, r_flange),
        (104.0, r_flange),
        (104.0, r_inner),
        (22.0, r_inner),
        (22.0, r_hub),
        (16.0, r_bore),
        (-28.0, r_bore),
        (-34.0, r_hub),
        (-34.0, r_inner),
        (-102.0, r_inner),
    ]
    face = bd.Face(bd.Wire.make_polygon([(x, 0.0, z) for x, z in pts_xz]))
    rim = bd.revolve(face, axis=bd.Axis.X, revolution_arc=360.0)

    # Add 7 structural inner spokes connecting the hub web to the outer barrel
    spokes = []
    for k in range(NUM_SPOKES):
        deg = k * (360.0 / NUM_SPOKES)
        spoke_yz = [
            (-22.0, r_hub - 8.0),
            (-16.0, r_inner + 4.0),
            (16.0, r_inner + 4.0),
            (22.0, r_hub - 8.0),
        ]
        f_a = bd.Face(bd.Wire.make_polygon([(16.0, y, z) for y, z in spoke_yz]))
        f_b = bd.Face(bd.Wire.make_polygon([(68.0, y, z) for y, z in spoke_yz]))
        spoke = bd.Rot(deg, 0.0, 0.0) * bd.loft([f_a, f_b], ruled=True)
        spokes.append(spoke)

    rim = rim + spokes
    return materials.apply_mat(rim, materials.alloy_wheel_rim, "alloy_rim")


def _build_aero_cover() -> tuple[bd.Solid, bd.Solid]:
    """Build the iconic 7-spoke Cybertruck geometric aero wheel cover & dark vent backing.

    Returns (aero_cover, aero_vents) sitting cleanly on the outboard face X in [+105, +136].
    """
    r_outer = spec.RIM_RADIUS + 4.0  # 258.0 mm covers rim flange cleanly
    # 1. Recessed dark charcoal backing plate with 7-sided faceted dish (X = 105..114)
    back_xz = [
        (105.0, 44.0),
        (105.0, r_outer - 10.0),
        (114.0, r_outer - 4.0),
        (114.0, 44.0),
    ]
    backing = bd.revolve(
        bd.Face(bd.Wire.make_polygon([(x, 0.0, z) for x, z in back_xz])),
        axis=bd.Axis.X,
        revolution_arc=360.0,
    )
    # Cut 7 crisp angular ventilation slots through the backing ring
    vent_cutters = []
    for k in range(NUM_SPOKES):
        deg = (k + 0.5) * (360.0 / NUM_SPOKES)
        slot_yz = [
            (-20.0, 128.0),
            (-42.0, 218.0),
            (42.0, 218.0),
            (20.0, 128.0),
        ]
        f_s = bd.Face(bd.Wire.make_polygon([(102.0, y, z) for y, z in slot_yz]))
        cutter = bd.Rot(deg, 0.0, 0.0) * bd.extrude(f_s, amount=18.0, dir=(1, 0, 0))
        vent_cutters.append(cutter)
    backing = backing - vent_cutters
    materials.apply_mat(backing, materials.dark_charcoal_trim, "aero_cover_backing")

    # 2. Outer geometric 7-spoke Cybertruck aero cover (X = 114.5..136.0)
    # Central heptagonal (7-sided) concave-beveled hub cap
    r_hub_base = 86.0
    r_hub_top = 66.0
    hep_base = [
        (114.5, r_hub_base * math.sin(math.radians(k * 360.0 / NUM_SPOKES)), r_hub_base * math.cos(math.radians(k * 360.0 / NUM_SPOKES)))
        for k in range(NUM_SPOKES)
    ]
    hep_top = [
        (134.0, r_hub_top * math.sin(math.radians(k * 360.0 / NUM_SPOKES)), r_hub_top * math.cos(math.radians(k * 360.0 / NUM_SPOKES)))
        for k in range(NUM_SPOKES)
    ]
    cover = bd.loft(
        [bd.Face(bd.Wire.make_polygon(hep_base)), bd.Face(bd.Wire.make_polygon(hep_top))],
        ruled=True,
    )

    # Outer segmented faceted ring (sits cleanly at X = 114.5..127.0)
    ring_xz = [
        (114.5, 224.0),
        (114.5, r_outer),
        (124.0, r_outer),
        (127.0, 240.0),
        (122.0, 224.0),
    ]
    outer_ring = bd.revolve(
        bd.Face(bd.Wire.make_polygon([(x, 0.0, z) for x, z in ring_xz])),
        axis=bd.Axis.X,
        revolution_arc=360.0,
    )
    cover = cover + outer_ring

    # 7 iconic bold angular Cybertruck spoke blades with sharp central spine ridge
    spokes = []
    for k in range(NUM_SPOKES):
        deg = k * (360.0 / NUM_SPOKES)
        # Base footprint at X = 114.5 (broad geometric Cybertruck aero-disc spoke blades)
        base_yz = [
            (-40.0, 72.0),
            (-56.0, 158.0),
            (-42.0, r_outer + 2.0),
            (42.0, r_outer + 2.0),
            (56.0, 158.0),
            (40.0, 72.0),
        ]
        # Raised chamfered ridge at X = 135.5
        top_yz = [
            (-20.0, 76.0),
            (-32.0, 158.0),
            (-22.0, r_outer - 4.0),
            (22.0, r_outer - 4.0),
            (32.0, 158.0),
            (20.0, 76.0),
        ]
        f0 = bd.Face(bd.Wire.make_polygon([(114.5, y, z) for y, z in base_yz]))
        f1 = bd.Face(bd.Wire.make_polygon([(135.5, y, z) for y, z in top_yz]))
        blade = bd.Rot(deg, 0.0, 0.0) * bd.loft([f0, f1], ruled=True)
        spokes.append(blade)

    cover = cover + spokes

    # Subtle Cybertruck silhouette recess on the center heptagon cap
    cap_recess = bd.Pos(131.5, 0.0, 0.0) * bd.Rot(0.0, 90.0, 0.0) * bd.Cylinder(32.0, 5.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    cover = cover - cap_recess

    materials.apply_mat(cover, materials.aero_wheel_cover, "aero_cover")
    return cover, backing


@model
def cyber_wheel():
    """Complete 20-inch Tesla Cybertruck wheel + 7-spoke aero cover + 285/65R20 AT tire."""
    tire = _build_tire()
    rim = _build_alloy_rim()
    cover, backing = _build_aero_cover()
    assy = bd.Compound(children=[tire, rim, backing, cover], label="cyber_wheel")

    bb = assy.bounding_box()
    assert abs(bb.size.Z - spec.TIRE_OD) < 2.0, f"Unexpected tire OD: {bb.size.Z}"
    return assy


if __name__ == "__main__":
    cyber_wheel()
