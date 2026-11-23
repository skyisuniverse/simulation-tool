"""Argon Hall-effect electric propulsion system for SpaceX Starlink V2 Mini.

Mounted cleanly inside the aft (-Y) propulsion bulkhead bay (X in [-420, +420],
Y in [-2050, -1925], Z in [38, 194]) with thruster nozzles extending aft along -Y.

Includes:
- Brushed titanium aft propulsion mounting bulkhead & thermal shield
- Dual SpaceX Argon Hall-effect ion thrusters with radiative cooling fins,
  white Boron Nitride (BN) ceramic annular discharge channels, central magnetic
  core poles, and external hollow-cathode electron neutralizers
- Dual carbon-fiber COPV Argon buffer tanks and titanium propellant manifold
"""

import build123d as bd
from bd_materials import metals, plastics
from cad import model
from cad.build123d import materials

from spec import BUS_Y

BAY_BACK_Y = -BUS_Y / 2.0 + 125.0  # -1925.0 mm (chassis pocket back wall)
BULKHEAD_FRONT_Y = -1943.0         # Thruster & manifold mount plane (facing -Y)
PROP_Z = 116.0                     # Vertical centerline of propulsion bay


def _make_hall_thruster(name: str, cx: float, side_sign: float) -> bd.Compound:
    """Build one Argon Hall-effect thruster pointing along -Y, mounted at Y = BULKHEAD_FRONT_Y."""
    ti = metals.titanium()
    ti.pbr = ti.pbr.override(roughness=0.28)
    ceramic_mat = materials.ceramic("white")
    ceramic_mat.pbr = ceramic_mat.pbr.override(roughness=0.35)
    pole_mat = materials.anodized("#252A32")
    cathode_mat = metals.stainless()
    cathode_mat.pbr = cathode_mat.pbr.override(roughness=0.22)

    # Local frame: +Z of primitive aligned with -Y (thrust exhaust direction) via Rot(90, 0, 0)
    # Wait: Rot(90, 0, 0) maps +Z -> -Y! Verify: Rx(90) * (0,0,1) = (0, -sin(90), cos(90)) = (0, -1, 0).
    orient = bd.Pos(cx, BULKHEAD_FRONT_Y - 1.0, PROP_Z) * bd.Rot(90, 0, 0)

    # 1. Outer magnetic shroud barrel & machined cooling fins (z_local in [0, 152])
    # Flange r = 76 mm keeps Z in [40, 192], clearing bus aft pocket Z in [38, 194] by 2 mm
    flange = bd.Cylinder(radius=76.0, height=14.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    barrel = bd.Pos(0, 0, 14.0) * bd.Cylinder(
        radius=68.0, height=136.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    fins = []
    for fz in (34.0, 56.0, 78.0, 100.0, 122.0):
        fins.append(
            bd.Pos(0, 0, fz)
            * bd.Cylinder(radius=74.5, height=7.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        )
    # Hollow interior for ceramic annular channel (r = 62.8 mm from z = 78 to 156)
    cavity = bd.Pos(0, 0, 78.0) * bd.Cylinder(
        radius=62.8, height=80.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    shroud = (flange + barrel + fins[0] + fins[1] + fins[2] + fins[3] + fins[4]) - cavity
    shroud = orient * shroud
    shroud.label = f"{name}_shroud"
    shroud.material = ti

    # 2. White Boron Nitride (BN) ceramic annular discharge channel (z_local in [80, 158])
    bn_outer = bd.Pos(0, 0, 80.0) * bd.Cylinder(
        radius=62.0, height=78.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    bn_inner_bore = bd.Pos(0, 0, 78.0) * bd.Cylinder(
        radius=33.0, height=84.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    # Deep annular ion-acceleration plasma channel cut into the front face (r in [41, 55], depth 38 mm)
    channel_outer = bd.Pos(0, 0, 120.0) * bd.Cylinder(
        radius=55.0, height=42.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    channel_inner = bd.Pos(0, 0, 118.0) * bd.Cylinder(
        radius=41.0, height=46.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    plasma_slot = channel_outer - channel_inner
    ceramic = (bn_outer - bn_inner_bore) - plasma_slot
    ceramic = orient * ceramic
    ceramic.label = f"{name}_bn_channel"
    ceramic.material = ceramic_mat

    # 3. Central magnetic pole core & graphite cap (r = 32.0 mm, 1.0 mm clear of BN bore r = 33.0)
    pole_stem = bd.Pos(0, 0, 80.0) * bd.Cylinder(
        radius=32.0, height=74.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    pole_tip = bd.Pos(0, 0, 154.0) * bd.Cone(
        bottom_radius=32.0,
        top_radius=22.0,
        height=8.0,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    pole = orient * (pole_stem + pole_tip)
    pole.label = f"{name}_center_pole"
    pole.material = pole_mat

    # 4. External hollow-cathode electron neutralizer + mounting bracket stalk on shroud shoulder
    # At z = 138 (past last cooling fin at z = 129), shroud barrel radius is 70.0 mm.
    # Place stalk radially from r = 70.8 to r = 90.0 along angle ~37 deg -> 0.8 mm clean clearance.
    cath_stalk = (
        bd.Pos(side_sign * 65.0, 49.0, 138.0)
        * bd.Rot(0, 0, side_sign * 37.0)
        * bd.Box(19.0, 9.0, 10.0)
    )
    cath_tube = (
        bd.Pos(side_sign * 74.0, 56.0, 128.0)
        * bd.Rot(0, -side_sign * 26.0, 0)
        * (
            bd.Cylinder(radius=11.0, height=32.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
            + bd.Pos(0, 0, 32.0)
            * bd.Cone(
                bottom_radius=11.0,
                top_radius=5.0,
                height=14.0,
                align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
            )
        )
    )
    cathode = orient * (cath_stalk + cath_tube)
    cathode.label = f"{name}_cathode"
    cathode.material = cathode_mat

    return bd.Compound(children=[shroud, ceramic, pole, cathode], label=name)


def _make_argon_tanks_and_manifold() -> bd.Compound:
    """Build central Argon COPV buffer bottles and propellant regulator manifold."""
    cfrp = plastics.cfrp()
    cfrp.pbr = cfrp.pbr.override(roughness=0.34, metalness=0.18)
    ti = metals.titanium()
    ti.pbr = ti.pbr.override(roughness=0.25)
    gold = metals.gold()
    gold.pbr = gold.pbr.override(roughness=0.25, metalness=0.90)

    parts = []

    # Dual horizontal Argon COPV tanks stacked at Z = 72 and Z = 160 (r = 28 mm),
    # leaving a 32 mm central corridor (26 mm between straps) for the regulator and feed lines
    for idx, tz in enumerate((72.0, 160.0), start=1):
        cyl_len = 160.0
        r = 28.0
        body = bd.Rot(0, 90, 0) * bd.Cylinder(radius=r, height=cyl_len)
        dome_l = bd.Pos(-cyl_len / 2.0, 0.0, 0.0) * bd.Sphere(radius=r)
        dome_r = bd.Pos(cyl_len / 2.0, 0.0, 0.0) * bd.Sphere(radius=r)
        tank = bd.Pos(0.0, -1990.0, tz) * (body + dome_l + dome_r)
        tank.label = f"argon_copv_{idx}"
        tank.material = cfrp
        tank.color = "#232830"
        parts.append(tank)

        # Twin titanium retaining strap collars (annular rings r = 28.5..31.0 so zero overlap with tank)
        for sname, sx in (("l", -52.0), ("r", 52.0)):
            strap = (
                bd.Pos(sx, -1990.0, tz)
                * bd.Rot(0, 90, 0)
                * (bd.Cylinder(radius=31.0, height=12.0) - bd.Cylinder(radius=28.5, height=16.0))
            )
            strap.label = f"copv_strap_{idx}_{sname}"
            strap.material = ti
            parts.append(strap)

    # Central gold-anodized Argon proportional flow regulator block (Z in [105, 127], X in [-43, +43])
    reg = bd.Pos(0.0, -1990.0, PROP_Z) * bd.Box(86.0, 44.0, 22.0)
    reg.label = "propellant_regulator"
    reg.material = gold
    parts.append(reg)

    # Left & Right titanium propellant feed lines (|X| in [44, 194], 1.5 mm clear of thruster fins at 195.5)
    for sname, side in (("port", -1.0), ("stbd", 1.0)):
        pipe = (
            bd.Pos(side * 119.0, -1990.0, PROP_Z)
            * bd.Rot(0, 90, 0)
            * bd.Cylinder(radius=6.0, height=150.0)
        )
        pipe.label = f"feed_line_{sname}"
        pipe.material = ti
        parts.append(pipe)

    return bd.Compound(children=parts, label="argon_propellant_system")


@model
def propulsion_module():
    """Complete aft Argon Hall-effect electric propulsion module."""
    ti = metals.titanium()
    ti.pbr = ti.pbr.override(roughness=0.30)

    # Bulkhead plate seated cleanly inside the bus aft pocket (Y in [-1943, -1926], X in [-416, +416], Z in [40, 192])
    bulkhead = (
        bd.Pos(0.0, -1934.5, PROP_Z)
        * bd.Box(832.0, 16.0, 150.0)
    )
    bulkhead.label = "propulsion_bulkhead"
    bulkhead.material = ti

    thruster_port = _make_hall_thruster("hall_thruster_port", -270.0, -1.0)
    thruster_stbd = _make_hall_thruster("hall_thruster_stbd", 270.0, 1.0)
    argon_sys = _make_argon_tanks_and_manifold()

    return bd.Compound(
        children=[bulkhead, thruster_port, thruster_stbd, argon_sys],
        label="propulsion_module",
    )


if __name__ == "__main__":
    propulsion_module()
