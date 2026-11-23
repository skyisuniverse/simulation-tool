"""Earth-facing (-Z nadir) communications payload suite for SpaceX Starlink V2 Mini.

Includes:
- 4 multi-sector Ku-band high-throughput phased-array antennas with sub-array tile grooves
  and low-reflectivity dielectric dark radome finish (astronomical glare mitigation)
- 2 circular Ka/E-band parabolic gateway reflector dishes with tripod waveguide feed horns
- Central E-band backhaul phased-array module
- Forward and aft S-band TT&C telemetry microstrip patch antennas
"""

import build123d as bd
from bd_materials import metals, plastics
from cad import model
from cad.build123d import materials

from spec import NADIR_RECESS_DEPTH


def _make_ku_sector(name: str, cx: float, cy: float, w: float, l: float, corner_x: float, corner_y: float) -> bd.Compound:
    """Build one Ku-band phased-array antenna sector with anodized bezel and tiled dark radome."""
    # Corner chamfer only on the outer spacecraft corner
    hx = w / 2.0
    hy = l / 2.0
    ch = 115.0

    # Build polygon vertices in local XY, chamfering the single corner at (corner_x, corner_y)
    corners = [(-hx, -hy), (hx, -hy), (hx, hy), (-hx, hy)]
    pts = []
    for vx, vy in corners:
        if (vx * corner_x > 0) and (vy * corner_y > 0):
            # Replace outer corner with two chamfer vertices
            if vx > 0 and vy > 0:
                pts.extend([(vx, vy - ch), (vx - ch, vy)])
            elif vx < 0 and vy > 0:
                pts.extend([(vx + ch, vy), (vx, vy - ch)])
            elif vx < 0 and vy < 0:
                pts.extend([(vx, vy + ch), (vx + ch, vy)])
            else:
                pts.extend([(vx - ch, vy), (vx, vy + ch)])
        else:
            pts.append((vx, vy))

    outer_face = bd.Face(bd.Wire.make_polygon(pts))
    # Mount inside nadir recess: Z in [1.0, 13.5] (0.5 mm below recess ceiling Z = 14.0)
    bezel_solid = bd.Pos(0.0, 0.0, 2.0) * bd.extrude(outer_face, NADIR_RECESS_DEPTH - 2.5)

    # Inner stepped radome plate (inset 24 mm, proud to Z = -1.0 mm)
    inner_pts = []
    inset = 24.0
    for vx, vy in corners:
        ix = vx - (inset if vx > 0 else -inset)
        iy = vy - (inset if vy > 0 else -inset)
        if (vx * corner_x > 0) and (vy * corner_y > 0):
            ic = ch - inset * 0.82
            if vx > 0 and vy > 0:
                inner_pts.extend([(ix, iy - ic), (ix - ic, iy)])
            elif vx < 0 and vy > 0:
                inner_pts.extend([(ix + ic, iy), (ix, iy - ic)])
            elif vx < 0 and vy < 0:
                inner_pts.extend([(ix, iy + ic), (ix + ic, iy)])
            else:
                inner_pts.extend([(ix - ic, iy), (ix, iy + ic)])
        else:
            inner_pts.append((ix, iy))

    inner_face = bd.Face(bd.Wire.make_polygon(inner_pts))
    bezel_pocket = bd.Pos(0.0, 0.0, 1.0) * bd.extrude(inner_face, 9.0)
    bezel = bezel_solid - bezel_pocket

    # Radome plate inset 1.0 mm inside bezel pocket for zero-interference fit
    rad_pts = []
    rad_inset = inset + 1.0
    for vx, vy in corners:
        rx = vx - (rad_inset if vx > 0 else -rad_inset)
        ry = vy - (rad_inset if vy > 0 else -rad_inset)
        if (vx * corner_x > 0) and (vy * corner_y > 0):
            rc = ch - rad_inset * 0.82
            if vx > 0 and vy > 0:
                rad_pts.extend([(rx, ry - rc), (rx - rc, ry)])
            elif vx < 0 and vy > 0:
                rad_pts.extend([(rx + rc, ry), (rx, ry - rc)])
            elif vx < 0 and vy < 0:
                rad_pts.extend([(rx, ry + rc), (rx + rc, ry)])
            else:
                rad_pts.extend([(rx - rc, ry), (rx, ry + rc)])
        else:
            rad_pts.append((rx, ry))
    radome_face = bd.Face(bd.Wire.make_polygon(rad_pts))

    # Dark low-albedo dielectric radome face with crisp sub-array tile grooves (3x4 mosaic)
    radome_block = bd.Pos(0.0, 0.0, -1.0) * bd.extrude(radome_face, 10.6)
    grooves = []
    # 2 vertical (along Y) and 3 horizontal (along X) tile seam grooves on the -Z face
    for gx in (-w / 6.0, w / 6.0):
        grooves.append(
            bd.Pos(gx, 0.0, -1.5)
            * bd.Box(4.0, l, 3.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        )
    for gy in (-l / 4.0, 0.0, l / 4.0):
        grooves.append(
            bd.Pos(0.0, gy, -1.5)
            * bd.Box(w, 4.0, 3.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        )
    radome = radome_block - grooves

    bezel = bd.Pos(cx, cy, 0.0) * bezel
    radome = bd.Pos(cx, cy, 0.0) * radome

    bezel.label = f"{name}_bezel"
    bezel.material = materials.anodized("#2E343D")

    radome.label = f"{name}_radome"
    radome_mat = plastics.cfrp()
    radome_mat.pbr = radome_mat.pbr.override(roughness=0.42, metalness=0.15)
    radome.material = radome_mat
    radome.color = "#1B2028"

    return bd.Compound(children=[bezel, radome], label=name)


def _make_ka_gateway_dish(name: str, cx: float, cy: float) -> bd.Compound:
    """Build a circular Ka/E-band parabolic gateway reflector dish with tripod waveguide feed."""
    # Smooth spline parabolic reflector shell facing -Z, mounted from Z = 13.5 down to rim at Z = -4.0
    r_hub = 34.8
    r_inner = 276.0
    r_outer = 290.0
    z_top = 13.5
    z_rim = -4.0

    n_pts = 7
    front_pts = []
    back_pts = []
    for i in range(n_pts):
        t = i / (n_pts - 1)
        r = r_hub + t * (r_inner - r_hub)
        z = z_top - 4.0 - (z_top - 4.0 - z_rim) * (t * t)
        front_pts.append((r, 0.0, z))
        back_pts.append((r, 0.0, z + 3.5))

    e_front = bd.Edge.make_spline([bd.Vector(*p) for p in front_pts])
    e_rim_bot = bd.Edge.make_line(bd.Vector(*front_pts[-1]), bd.Vector(r_outer, 0.0, z_rim))
    e_rim_out = bd.Edge.make_line(bd.Vector(r_outer, 0.0, z_rim), bd.Vector(r_outer, 0.0, z_rim + 4.5))
    e_rim_top = bd.Edge.make_line(bd.Vector(r_outer, 0.0, z_rim + 4.5), bd.Vector(*back_pts[-1]))
    e_back = bd.Edge.make_spline([bd.Vector(*p) for p in reversed(back_pts)])
    e_inner = bd.Edge.make_line(bd.Vector(*back_pts[0]), bd.Vector(*front_pts[0]))
    dish_face = bd.Face(bd.Wire([e_front, e_rim_bot, e_rim_out, e_rim_top, e_back, e_inner]))
    dish = bd.revolve(dish_face, axis=bd.Axis.Z, revolution_arc=360.0)

    # Outer RF choke / glare-baffle shroud collar (r = 291..308 mm, clear of dish r = 290 mm)
    collar = (
        bd.Pos(0.0, 0.0, -6.5)
        * (
            bd.Cylinder(radius=r_outer + 18.0, height=19.8, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
            - bd.Cylinder(radius=r_outer + 1.0, height=22.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        )
    )

    # Central waveguide feed horn and sub-reflector pointing toward -Z (r <= 34 mm, clear of dish r_hub = 34.8)
    hub = bd.Pos(0.0, 0.0, -2.0) * bd.Cylinder(
        radius=34.0, height=15.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    horn = bd.Pos(0.0, 0.0, -34.0) * bd.Cone(
        bottom_radius=26.0,
        top_radius=14.0,
        height=32.0,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    sub_cap = bd.Pos(0.0, 0.0, -40.0) * bd.Cylinder(
        radius=34.0, height=6.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    feed = hub + horn + sub_cap

    # 3 radial tripod feed struts connecting outer collar rim to sub-reflector cap, cleanly clear of dish
    struts = []
    for deg in (30.0, 150.0, 270.0):
        # Endpoints: inner (r=36, z=-37) to outer (r=288, z=-9), length ~253.5 mm, slope +6.34 deg
        strut = (
            bd.Rot(0, 0, deg)
            * bd.Pos(162.0, 0.0, -23.0)
            * bd.Rot(0, -6.34, 0)
            * bd.Box(250.0, 8.0, 5.5)
        )
        struts.append(strut)
    tripod = struts[0] + struts[1] + struts[2]

    dish = bd.Pos(cx, cy, 0.0) * dish
    collar = bd.Pos(cx, cy, 0.0) * collar
    feed = bd.Pos(cx, cy, 0.0) * feed
    tripod = bd.Pos(cx, cy, 0.0) * tripod

    dish.label = f"{name}_reflector"
    dish_mat = metals.aluminum()
    dish_mat.pbr = dish_mat.pbr.override(roughness=0.22, metalness=0.88)
    dish.material = dish_mat
    dish.color = "#C9D0D8"

    collar.label = f"{name}_collar"
    collar.material = materials.anodized_black()

    feed.label = f"{name}_feed_horn"
    feed_mat = metals.gold()
    feed_mat.pbr = feed_mat.pbr.override(roughness=0.25, metalness=0.90)
    feed.material = feed_mat

    tripod.label = f"{name}_tripod"
    tripod.material = materials.anodized("#343B44")

    return bd.Compound(children=[dish, collar, feed, tripod], label=name)


def _make_eband_and_sband() -> list:
    """Build central E-band backhaul array and fore/aft S-band TT&C telemetry patches."""
    parts = []

    # Central E-band high-capacity backhaul array between the two Ka gateway dishes
    eb_frame = bd.Pos(0.0, 0.0, 1.5) * (
        bd.Box(310.0, 560.0, 12.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        - bd.Pos(0.0, 0.0, -1.0)
        * bd.Box(274.0, 524.0, 9.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    )
    eb_frame.label = "eband_frame"
    eb_frame.material = materials.anodized("#363D48")

    eb_face = bd.Pos(0.0, 0.0, -1.5) * bd.Box(
        270.0, 520.0, 10.5, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    eb_grooves = []
    for gy in (-170.0, 0.0, 170.0):
        eb_grooves.append(
            bd.Pos(0.0, gy, -2.0)
            * bd.Box(274.0, 3.5, 3.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        )
    eb_face = eb_face - eb_grooves
    eb_face.label = "eband_radome"
    eb_face.material = materials.ceramic("tan")
    eb_face.color = "#A9895B"
    parts.append(bd.Compound(children=[eb_frame, eb_face], label="eband_array"))

    # Fore and Aft S-band TT&C telemetry microstrip patch antennas
    for name, py in (("sband_fwd", 1875.0), ("sband_aft", -1875.0)):
        sub = bd.Pos(0.0, py, 2.0) * bd.Box(
            180.0, 110.0, 11.5, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
        )
        sub.label = f"{name}_substrate"
        sub.material = materials.ceramic("white")

        patch = bd.Pos(0.0, py, -0.4) * bd.Box(
            128.0, 74.0, 2.2, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
        )
        patch.label = f"{name}_patch"
        patch.material = metals.gold()

        parts.append(bd.Compound(children=[sub, patch], label=name))

    return parts


@model
def payload_antennas():
    """Earth-facing (-Z) Ku/Ka/E-band and S-band communications payload assembly."""
    # 4 large Ku-band phased-array sectors arranged in a symmetric 2x2 mosaic
    # Fore sectors: Y in [390, 1810] (center 1100, length 1420)
    # Aft sectors:  Y in [-1810, -390] (center -1100, length 1420)
    # Port/Stbd:    |X| in [42, 1182] (center +-612, width 1140)
    ku_sectors = [
        _make_ku_sector("ku_array_fwd_port", -612.0, 1100.0, 1140.0, 1420.0, -1.0, 1.0),
        _make_ku_sector("ku_array_fwd_stbd", 612.0, 1100.0, 1140.0, 1420.0, 1.0, 1.0),
        _make_ku_sector("ku_array_aft_port", -612.0, -1100.0, 1140.0, 1420.0, -1.0, -1.0),
        _make_ku_sector("ku_array_aft_stbd", 612.0, -1100.0, 1140.0, 1420.0, 1.0, -1.0),
    ]

    # Dual circular Ka-band / E-band gateway dishes flanking center at Y = 0
    ka_port = _make_ka_gateway_dish("ka_gateway_port", -620.0, 0.0)
    ka_stbd = _make_ka_gateway_dish("ka_gateway_stbd", 620.0, 0.0)

    aux = _make_eband_and_sband()

    return bd.Compound(
        children=[*ku_sectors, ka_port, ka_stbd, *aux],
        label="payload_antennas",
    )


if __name__ == "__main__":
    payload_antennas()
