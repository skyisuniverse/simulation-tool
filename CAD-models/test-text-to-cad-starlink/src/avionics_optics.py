"""Optical Inter-Satellite Link ("Space Laser") terminals and attitude sensors for Starlink V2 Mini.

All zenith-mounted hardware sits either on the raised fore/aft equipment bulkheads
(|Y| >= 1865 mm) or along the central dorsal spine (|X| <= 112 mm), remaining
100% clear of the stowed dual accordion solar array wings.

Includes:
- 3 gimbaled Optical ISL (200 Gbps laser communication) telescope turrets
  (1 forward +Y, 2 aft-quarter port/starboard)
- Dual angled optical Star Trackers with conical stray-light baffle hoods
- Central GNSS/GPS zenith patch antenna and fore/aft coarse sun sensors
"""

import build123d as bd
from bd_materials import glass, metals
from cad import model
from cad.build123d import materials

from spec import BUS_Z, ISL_AFT_PORT_POS, ISL_AFT_STBD_POS, ISL_FWD_POS


def _make_isl_terminal(name: str, pos: tuple[float, float, float], yaw_deg: float, elev_deg: float = 12.0) -> bd.Compound:
    """Build one gimbaled Optical Inter-Satellite Link laser communication turret.

    Local frame before placement: optical aperture points along +Y, rotated up by elev_deg,
    then yawed around +Z by yaw_deg (0 deg = +Y forward, 180 deg = -Y aft).
    """
    base_mat = materials.anodized("#2E343D")
    ti = metals.titanium()
    ti.pbr = ti.pbr.override(roughness=0.25)
    head_mat = materials.anodized("#464F5B")
    baffle_mat = materials.anodized_black()
    lens_mat = glass.borosilicate()
    lens_mat.pbr = lens_mat.pbr.override(transmission=0.88, roughness=0.05)

    # 1. Circular azimuth base pedestal (Z in [0, 22])
    pedestal = (
        bd.Cylinder(radius=56.0, height=10.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        + bd.Pos(0, 0, 10.0)
        * bd.Cylinder(radius=46.0, height=12.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    )
    pedestal.label = f"{name}_pedestal"
    pedestal.material = base_mat

    # 2. Azimuth U-yoke (Z in [22.5, 92], clear of pedestal by 0.5 mm)
    yoke_floor = bd.Pos(0, 0, 22.5) * bd.Box(
        118.0, 44.0, 12.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    arm_l = bd.Pos(-53.0, 0, 34.5) * bd.Box(
        12.0, 38.0, 60.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    arm_r = bd.Pos(53.0, 0, 34.5) * bd.Box(
        12.0, 38.0, 60.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    cap_l = bd.Pos(-53.0, 0, 94.5) * bd.Rot(0, 90, 0) * bd.Cylinder(radius=19.0, height=12.0)
    cap_r = bd.Pos(53.0, 0, 94.5) * bd.Rot(0, 90, 0) * bd.Cylinder(radius=19.0, height=12.0)
    yoke = yoke_floor + arm_l + arm_r + cap_l + cap_r
    yoke.label = f"{name}_gimbal_yoke"
    yoke.material = ti

    # 3. Elevation optical head centered at (0, 0, 94.5), spanning X in [-44, +44] (3 mm clear of arms at +-47)
    # Orient local +Z along +Y via Rot(-90, 0, 0), then pitch upward by +elev_deg around X
    head_xf = bd.Pos(0.0, 0.0, 94.5) * bd.Rot(elev_deg, 0.0, 0.0) * bd.Rot(-90.0, 0.0, 0.0)

    # Rear transceiver barrel + cooling ring fins (z_local in [-52, +30])
    barrel = bd.Pos(0, 0, -48.0) * bd.Cylinder(
        radius=42.0, height=78.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    rear_cap = bd.Pos(0, 0, -54.0) * bd.Cylinder(
        radius=36.0, height=6.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    # Hollow optical bench recess at the front (z_local in [8, 32], r = 34.5 mm)
    front_bore = bd.Pos(0, 0, 8.0) * bd.Cylinder(
        radius=34.5, height=26.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    head_body = head_xf * ((barrel + rear_cap) - front_bore)
    head_body.label = f"{name}_optical_head"
    head_body.material = head_mat

    # Primary glass optical aperture lens (z_local in [20, 26], leaving 12 mm air gap to bench & 1 mm radial gap)
    lens = head_xf * (
        bd.Pos(0, 0, 20.0)
        * bd.Cylinder(radius=33.5, height=6.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    )
    lens.label = f"{name}_aperture_lens"
    lens.material = lens_mat
    lens.color = "#4B86B4"

    # Matte-black stray-light optical baffle hood extending forward (z_local in [30.5, 68])
    baffle_outer = bd.Pos(0, 0, 30.5) * bd.Cone(
        bottom_radius=41.5,
        top_radius=45.0,
        height=38.0,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    baffle_inner = bd.Pos(0, 0, 29.0) * bd.Cone(
        bottom_radius=35.0,
        top_radius=40.5,
        height=41.0,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    baffle = head_xf * (baffle_outer - baffle_inner)
    baffle.label = f"{name}_baffle"
    baffle.material = baffle_mat

    turret = bd.Compound(children=[pedestal, yoke, head_body, lens, baffle], label=name)
    return bd.Pos(*pos) * bd.Rot(0.0, 0.0, yaw_deg) * turret


def _make_star_tracker(name: str, cx: float, cy: float, tilt_y_deg: float) -> bd.Compound:
    """Build one optical Star Tracker with a flared matte-black stray-light sun baffle."""
    ti = metals.titanium()
    ti.pbr = ti.pbr.override(roughness=0.28)
    baffle_mat = materials.anodized_black()
    lens_mat = glass.borosilicate()
    lens_mat.pbr = lens_mat.pbr.override(transmission=0.88, roughness=0.05)

    # Electronics housing block + angled optical mount boss (Z = BUS_Z + 0.2)
    box = bd.Box(68.0, 68.0, 24.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    opt_xf = bd.Pos(0.0, 0.0, 28.0) * bd.Rot(-12.0, tilt_y_deg, 0.0)
    collar = opt_xf * bd.Cylinder(
        radius=25.0, height=16.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    base = box + collar
    base.label = f"{name}_housing"
    base.material = ti

    # Recessed glass lens sitting cleanly on top of optical mount boss (z_local in [16.5, 20.5])
    lens = opt_xf * (
        bd.Pos(0, 0, 16.5)
        * bd.Cylinder(radius=18.8, height=4.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    )
    lens.label = f"{name}_lens"
    lens.material = lens_mat
    lens.color = "#5E9CC4"

    # Flared hollow sun-shade baffle cone cleanly shrouding the lens perimeter (z_local in [16.5, 96])
    hood_outer = bd.Pos(0, 0, 16.5) * bd.Cone(
        bottom_radius=24.8,
        top_radius=46.0,
        height=79.5,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    hood_inner = bd.Pos(0, 0, 15.5) * bd.Cone(
        bottom_radius=19.6,
        top_radius=41.0,
        height=82.0,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    hood = opt_xf * (hood_outer - hood_inner)
    hood.label = f"{name}_baffle"
    hood.material = baffle_mat

    st = bd.Compound(children=[base, lens, hood], label=name)
    return bd.Pos(cx, cy, BUS_Z + 0.2) * st


def _make_gnss_and_sun_sensors() -> bd.Compound:
    """Build central zenith GNSS/GPS patch antenna and fore/aft coarse sun sensors on dorsal spine."""
    ceramic = materials.ceramic("white")
    gold = metals.gold()
    gold.pbr = gold.pbr.override(roughness=0.25, metalness=0.90)
    dark = materials.anodized("#282D35")

    parts = []
    # Spine avionics cover top is at Z = BUS_Z + 6.2 = 246.2 mm -> mount at Z = 246.5 mm
    z_mount = BUS_Z + 6.5

    # Central GNSS/GPS zenith patch receiver at (0, 0, 246.5)
    gnss_base = bd.Pos(0.0, 0.0, z_mount) * bd.Box(
        118.0, 118.0, 12.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    gnss_base.label = "gnss_housing"
    gnss_base.material = dark

    gnss_cer = bd.Pos(0.0, 0.0, z_mount + 12.2) * bd.Box(
        96.0, 96.0, 5.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    gnss_cer.label = "gnss_ceramic"
    gnss_cer.material = ceramic

    gnss_patch = bd.Pos(0.0, 0.0, z_mount + 17.4) * bd.Box(
        70.0, 70.0, 1.8, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    gnss_patch.label = "gnss_patch"
    gnss_patch.material = gold

    parts.extend([gnss_base, gnss_cer, gnss_patch])

    # Fore and Aft coarse sun-sensor pyramids on spine ends (Y = +-1560)
    for sname, sy in (("sun_sensor_fwd", 1560.0), ("sun_sensor_aft", -1560.0)):
        pyr = bd.Pos(0.0, sy, z_mount) * bd.Cone(
            bottom_radius=34.0,
            top_radius=12.0,
            height=22.0,
            align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
        )
        pyr.label = sname
        pyr.material = dark
        parts.append(pyr)

    return bd.Compound(children=parts, label="gnss_and_sun_sensors")


@model
def avionics_optics():
    """Optical Inter-Satellite Link laser terminals, star trackers, and GNSS/sun sensors."""
    # 3 Optical ISL terminals positioned on fore/aft raised bulkheads (clear of stowed wings)
    isl_fwd = _make_isl_terminal("isl_laser_fwd", (ISL_FWD_POS[0], ISL_FWD_POS[1], BUS_Z + 0.2), yaw_deg=0.0, elev_deg=10.0)
    isl_aft_port = _make_isl_terminal(
        "isl_laser_aft_port", (ISL_AFT_PORT_POS[0], ISL_AFT_PORT_POS[1], BUS_Z + 0.2), yaw_deg=145.0, elev_deg=14.0
    )
    isl_aft_stbd = _make_isl_terminal(
        "isl_laser_aft_stbd", (ISL_AFT_STBD_POS[0], ISL_AFT_STBD_POS[1], BUS_Z + 0.2), yaw_deg=-145.0, elev_deg=14.0
    )

    # Dual Star Trackers on forward raised bulkhead flanking the forward ISL laser
    st_port = _make_star_tracker("star_tracker_port", -430.0, 1955.0, tilt_y_deg=-26.0)
    st_stbd = _make_star_tracker("star_tracker_stbd", 430.0, 1955.0, tilt_y_deg=26.0)

    gnss = _make_gnss_and_sun_sensors()

    return bd.Compound(
        children=[isl_fwd, isl_aft_port, isl_aft_stbd, st_port, st_stbd, gnss],
        label="avionics_optics",
    )


if __name__ == "__main__":
    avionics_optics()
