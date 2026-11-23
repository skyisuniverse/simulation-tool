"""Exposed carbon-fiber aerodynamics, vents, wing mirrors, spoiler actuators, and badges.

Signature Tesla Roadster aero elements:
  - Sculpted carbon front chin splitter & recessed lower aero intake with horizontal strake
  - Low-slung carbon side skirt rocker blades & rear-haunch aero winglets
  - Massive monolithic 7-fin carbon-fiber rear diffuser (pure EV — zero exhaust pipes!)
  - Hollow twin brushed-titanium actuator barrels & telescoping spoiler pistons
  - Aerodynamic teardrop side mirrors (returned per side to ride with moving doors!)
  - Polished brushed-silver Tesla "T" front nose emblem & rear accent plaque
"""

from __future__ import annotations

import build123d as bd

from lib.palette import (
    ALLOY_SILVER,
    CARBON_GLOSS,
    CARBON_SATIN,
    PAINT_RED,
    TITANIUM,
    TRIM_DARK,
    group,
    style_alloy,
    style_carbon,
    style_paint,
    style_trim,
)
from lib.surfaces import (
    DOOR_FRONT_X,
    HALF_WIDTH,
    SPOILER_FRONT_X,
    SPOILER_REAR_X,
    body_master,
    box_between,
)


def _safe(shape):
    if shape is None:
        return None
    if not shape.solids():
        return None
    return shape


def _build_front_aero():
    """Curved carbon front splitter, recessed lower chin intake, and outer winglets."""
    parts = []
    outer = body_master()

    # 1. Curved carbon front chin splitter blade cleanly below body floor (Z = 95..110)
    xs = [1800, 1920, 2030, 2120, 2195, 2245, 2274]
    ys = [845, 810, 720, 580, 415, 235, 95]
    pts_right = [(x, -y) for x, y in zip(xs, ys)]
    pts_left = [(x, y) for x, y in zip(reversed(xs), reversed(ys))]
    wire = bd.Wire.make_polygon([bd.Vector(x, y, 95.0) for x, y in (pts_right + pts_left)])
    splitter = bd.extrude(bd.Face(wire), 14.0)
    splitter = _safe(splitter - outer)
    if splitter is not None:
        parts.append(style_carbon(splitter, "front_carbon_splitter", CARBON_SATIN, gloss=True))

    # 2. Recessed lower chin intake backing wall closing front_mouth (Z=[113..194])
    intake_back = box_between(2035.0, 2080.0, -616.0, 616.0, 113.0, 194.0)
    parts.append(style_trim(intake_back, "front_intake_backing", TRIM_DARK))

    # Horizontal gloss-carbon aero strake floating cleanly across lower intake mouth
    intake_strake = box_between(2084.0, 2166.0, -555.0, 555.0, 146.0, 158.0)
    parts.append(style_carbon(intake_strake, "front_intake_strake", CARBON_GLOSS, gloss=True))

    # 3. Twin vertical corner aero winglets flanking the front splitter edges
    for side in (1, -1):
        lbl = "left" if side > 0 else "right"
        y0 = side * 830.0
        fin = box_between(1815.0, 1985.0, y0 - 8.0, y0 + 8.0, 111.0, 154.0)
        fin = _safe(fin - outer)
        if fin is not None:
            parts.append(style_carbon(fin, f"front_splitter_winglet_{lbl}", CARBON_SATIN, gloss=True))

    return parts


def _build_side_aero():
    """Exposed carbon rocker skirt blades running cleanly between front and rear arches."""
    parts = []
    outer = body_master()
    for side in (1, -1):
        lbl = "left" if side > 0 else "right"
        y_in = 720.0
        y_out_f = 860.0
        y_out_r = 890.0
        pts_2d = [
            (955.0, side * y_in),
            (955.0, side * y_out_f),
            (-955.0, side * y_out_r),
            (-955.0, side * y_in),
        ]
        if side < 0:
            pts_2d = list(reversed(pts_2d))
        wire = bd.Wire.make_polygon([bd.Vector(x, y, 96.0) for x, y in pts_2d])
        blade = bd.extrude(bd.Face(wire), 14.0)
        blade = _safe(blade - outer)
        if blade is not None:
            parts.append(style_carbon(blade, f"side_skirt_blade_{lbl}", CARBON_SATIN, gloss=True))

        # Swept triangular carbon aero winglet just ahead of the rear wheel arch
        fin_y = side * 882.0
        fin_xz = [
            (-955.0, 111.0),
            (-810.0, 111.0),
            (-955.0, 195.0),
        ]
        f_wire = bd.Wire.make_polygon([bd.Vector(x, fin_y - 6.0, z) for x, z in fin_xz])
        fin = bd.extrude(bd.Face(f_wire), 12.0, dir=(0, 1, 0))
        fin = _safe(fin - outer)
        if fin is not None:
            parts.append(style_carbon(fin, f"side_skirt_fin_{lbl}", CARBON_SATIN, gloss=True))

    return parts


def _build_rear_diffuser():
    """Monolithic autoclave-molded 7-fin carbon-fiber rear diffuser & upper valance."""
    parts = []

    # 1. Swept upward curved carbon diffuser floor tunnel + 7 tall strakes + side cheeks fused cleanly
    tunnel_xz = [
        (-1768.0, 148.0),
        (-1930.0, 222.0),
        (-2090.0, 318.0),
        (-2242.0, 412.0),
        (-2242.0, 434.0),
        (-2090.0, 344.0),
        (-1930.0, 250.0),
        (-1768.0, 170.0),
    ]
    tun_wire = bd.Wire.make_polygon([bd.Vector(x, -678.0, z) for x, z in tunnel_xz])
    diffuser = bd.extrude(bd.Face(tun_wire), 1356.0, dir=(0, 1, 0))

    # Seven tall razor-sharp vertical carbon-fiber diffuser strakes fused into tunnel underside
    fin_ys = [-565.0, -378.0, -190.0, 0.0, 190.0, 378.0, 565.0]
    for fy in fin_ys:
        drop = 132.0 if abs(fy) < 420.0 else 104.0
        fin_xz = [
            (-1790.0, 155.0),
            (-1940.0, 225.0),
            (-2100.0, 320.0),
            (-2244.0, 414.0),
            (-2244.0, 414.0 - drop),
            (-2140.0, 245.0),
            (-1950.0, 148.0),
            (-1790.0, 128.0),
        ]
        f_wire = bd.Wire.make_polygon([bd.Vector(x, fy - 7.0, z) for x, z in fin_xz])
        diffuser = diffuser + bd.extrude(bd.Face(f_wire), 14.0, dir=(0, 1, 0))

    # Left & right vertical diffuser side cheek walls fused cleanly to outer tunnel edges
    for side in (1, -1):
        y0, y1 = (656.0, 678.0) if side > 0 else (-678.0, -656.0)
        cheek_xz = [
            (-1934.0, 248.0),
            (-2238.0, 430.0),
            (-2238.0, 534.0),
            (-1934.0, 534.0),
        ]
        c_wire = bd.Wire.make_polygon([bd.Vector(x, y0, z) for x, z in cheek_xz])
        diffuser = diffuser + bd.extrude(bd.Face(c_wire), y1 - y0, dir=(0, 1, 0))

    # Upper rear valance bulkhead panel closing the rear diffuser bay cleanly up to Z = 534
    valance = box_between(-2238.0, -2195.0, -678.0, 678.0, 430.0, 534.0)
    diffuser = diffuser + valance

    parts.append(style_carbon(diffuser, "rear_carbon_diffuser_7fin", CARBON_GLOSS, gloss=True))
    return parts


def _build_spoiler_mounts():
    """Recessed spoiler tray (with actuator pass-through bores) and hollow titanium barrels."""
    parts = []
    x_act = 0.5 * (SPOILER_FRONT_X + SPOILER_REAR_X)
    tray = box_between(SPOILER_REAR_X + 12.0, SPOILER_FRONT_X - 12.0, -645.0, 645.0, 804.0, 818.0)
    # Cut clean 28 mm clearance bores through the well tray for the telescoping pistons!
    for side in (1, -1):
        bore = bd.Pos(x_act, side * 395.0, 811.0) * bd.Cylinder(radius=14.5, height=30.0)
        tray = tray - bore
    parts.append(style_carbon(tray, "spoiler_well_tray", CARBON_SATIN))

    # Twin hollow actuator barrels cleanly below tray (Z = 700..802, r_in = 14 > piston r = 11.5)
    for side in (1, -1):
        lbl = "left" if side > 0 else "right"
        outer_c = bd.Cylinder(radius=19.0, height=102.0)
        inner_c = bd.Cylinder(radius=14.0, height=106.0)
        barrel = bd.Pos(x_act, side * 395.0, 751.0) * (outer_c - inner_c)
        parts.append(style_alloy(barrel, f"spoiler_actuator_barrel_{lbl}", TITANIUM, roughness=0.26))

    return parts


def build_spoiler_struts():
    """Upper telescoping pistons fastened to the moving active spoiler panel."""
    struts = []
    x_act = 0.5 * (SPOILER_FRONT_X + SPOILER_REAR_X)
    for side in (1, -1):
        lbl = "left" if side > 0 else "right"
        # Top at Z = 822 (cleanly shy of active_spoiler_panel curved underside), bottom at 706 inside barrel
        rod = bd.Pos(x_act, side * 395.0, 764.0) * bd.Cylinder(radius=11.5, height=116.0)
        struts.append(style_alloy(rod, f"spoiler_piston_{lbl}", ALLOY_SILVER, roughness=0.16))
    return struts


def build_wing_mirror(side):
    """Sleek razor-slim aerodynamic side wing mirror mounted on the front door shoulder."""
    lbl = "left" if side > 0 else "right"
    outer = body_master()
    x0 = DOOR_FRONT_X - 185.0
    y_door = side * (HALF_WIDTH(x0) - 20.0)
    z0 = 782.0

    # Sleek airfoil teardrop mirror housing cap (crimson painted)
    mx = x0 - 44.0
    my = y_door + side * 124.0
    mz = z0 + 36.0
    cap_raw = bd.Pos(mx, my, mz) * bd.Rot(0, 0, side * -14) * bd.scale(bd.Sphere(1.0), by=(76.0, 66.0, 26.0))
    cut_rear = box_between(mx - 115.0, mx - 22.0, my - 95.0, my + 95.0, mz - 45.0, mz + 45.0)
    cap = _safe(cap_raw - cut_rear)

    # Reflective mirror glass insert strictly behind the flat cut plane X = mx - 22 (zero overlap!)
    mirror_glass = box_between(mx - 28.0, mx - 24.0, my - 46.0, my + 46.0, mz - 15.0, mz + 15.0)

    # Forward-swept gloss-carbon mirror stalk strictly trimmed between door outer skin and cap
    stalk_pts = [
        bd.Vector(x0, y_door, z0),
        bd.Vector(x0 - 22.0, y_door + side * 52.0, z0 + 14.0),
        bd.Vector(x0 - 42.0, y_door + side * 102.0, z0 + 28.0),
    ]
    stalk_path = bd.Spline(*stalk_pts)
    stalk_sec = bd.Plane(origin=stalk_pts[0], z_dir=(stalk_pts[1] - stalk_pts[0]).normalized()) * bd.Ellipse(14.0, 7.0)
    stalk = bd.sweep(stalk_sec, path=stalk_path)
    stalk = _safe(stalk - outer - cap_raw)

    kids = []
    if stalk is not None:
        kids.append(style_carbon(stalk, f"mirror_stalk_{lbl}", CARBON_GLOSS, gloss=True))
    if cap is not None:
        kids.append(style_paint(cap, f"mirror_cap_{lbl}", PAINT_RED))
    kids.append(style_alloy(mirror_glass, f"mirror_glass_{lbl}", ALLOY_SILVER, roughness=0.05))
    return group(f"wing_mirror_{lbl}", kids)


def _build_badges():
    """Polished silver Tesla 'T' shield emblem (right-side-up!) on nose + rear Tesla plaque."""
    parts = []
    outer = body_master()

    # Sculpted Tesla 'T' emblem resting cleanly proud of the shark-nose tip
    # Note: local -X points UP/BACK toward windshield (top of T); local +X points DOWN/FORWARD toward nose tip (bottom stem of T)!
    loc_t = bd.Location((2182.0, 0.0, 424.0), (0.0, 33.0, 0.0))
    brow = bd.Pos(-32.0, 0.0, 0.0) * bd.Box(5.5, 70.0, 8.0)
    top_bar = bd.Pos(-21.0, 0.0, 0.0) * bd.Box(10.0, 76.0, 8.0)
    stem_pts = [
        (-15.0, -13.0),
        (-15.0, 13.0),
        (36.0, 3.5),
        (36.0, -3.5),
    ]
    stem_wire = bd.Wire.make_polygon([bd.Vector(x, y, -4.0) for x, y in stem_pts])
    stem = bd.extrude(bd.Face(stem_wire), 8.0)
    t_badge = _safe((loc_t * (brow + top_bar + stem)) - outer)
    if t_badge is not None:
        parts.append(style_alloy(t_badge, "tesla_front_emblem", ALLOY_SILVER, roughness=0.12))

    # Minimalist brushed-silver rear center badge plaque flush on rear light bar center
    rear_badge = box_between(-2257.0, -2251.5, -92.0, 92.0, 765.0, 777.0)
    rear_badge = _safe(rear_badge - outer)
    if rear_badge is not None:
        parts.append(style_alloy(rear_badge, "tesla_rear_badge", ALLOY_SILVER, roughness=0.14))

    return parts


def build():
    """Build fixed aero package (splitter, side skirts, 7-fin diffuser, mounts, badges)."""
    return group(
        "aero_and_trim",
        [
            group("front_aero", _build_front_aero()),
            group("side_aero", _build_side_aero()),
            group("rear_diffuser", _build_rear_diffuser()),
            group("spoiler_hardware", _build_spoiler_mounts()),
            group("badges", _build_badges()),
        ],
    )
