"""1-person wooden shop interior millwork: service counter, stool, shelving, display bench, pendants."""

import math

import build123d as bd
from cad import model

from lib import materials as mat
from lib import spec as S
from lib.geom import box_bounds


def _build_window_display_bench():
    """Built-in low oak showcase display bench beneath the front storefront window."""
    oak = mat.oak_millwork()
    walnut = mat.walnut_trim()
    z0 = S.SLAB_TOP_Z  # 300.0

    x0, x1 = -150.0, 1550.0
    y0, y1 = -1520.0, -1000.0
    top_t = 36.0
    z_top = z0 + 620.0          # 920.0 (106 mm clear under interior window sill)
    z_under = z_top - top_t     # 884.0

    # Solid oak display top with crisp chamfered top edges
    top = box_bounds(x0, x1, y0, y1, z_under, z_top)
    top_edges = top.edges().filter_by(
        lambda e: abs(e.bounding_box().min.Z - z_top) < 0.5 and abs(e.bounding_box().max.Z - z_top) < 0.5
    )
    top = top.chamfer(4.0, None, top_edges)
    top.label = "display_bench_top"
    mat.apply_material(top, oak)

    # 4 vertical walnut uprights + lower display shelf creating 3 open cubbies
    t = 28.0
    xs = [x0 + 20.0, x0 + 570.0, x0 + 1110.0, x1 - 20.0 - t]
    uprights = [box_bounds(ux, ux + t, y0 + 18.0, y1 - 18.0, z0, z_under) for ux in xs]
    shelves = []
    for i in range(len(xs) - 1):
        shelves.append(box_bounds(xs[i] + t, xs[i + 1], y0 + 22.0, y1 - 22.0, z0 + 110.0, z0 + 136.0))
    frame = uprights[0]
    for u in uprights[1:] + shelves:
        frame = frame + u
    frame.label = "display_bench_base"
    mat.apply_material(frame, walnut)

    return bd.Compound(children=[top, frame], label="window_display_bench")


def _build_left_wall_shelving():
    """Tall floor-standing craftsman display shelving unit with lower closed cabinet along left wall."""
    oak = mat.oak_millwork()
    walnut = mat.walnut_trim()
    brass = mat.brushed_brass()
    z0 = S.SLAB_TOP_Z

    x0, x1 = -1622.0, -1242.0   # 380 mm deep (7 mm clear of left baseboard)
    y0, y1 = -750.0, 1650.0     # 2400 mm long
    z_plinth = z0 + 85.0        # 385.0
    z_cab = z0 + 520.0          # 820.0 (lower cabinet top)
    z_top = z0 + 1680.0         # 1980.0 (74 mm clear below left clerestory window)

    # Recessed toe-kick + lower cabinet carcass + thin upper back panel + vertical bay dividers
    plinth = box_bounds(x0, x1 - 45.0, y0 + 10.0, y1 - 10.0, z0, z_plinth)
    cab_body = box_bounds(x0, x1 - 18.0, y0, y1, z_plinth, z_cab - 28.0)
    back_panel = box_bounds(x0, x0 + 14.0, y0, y1, z_cab, z_top - 28.0)

    div_t = 28.0
    bay_ys = [y0, y0 + 790.0, y0 + 1580.0, y1 - div_t]
    carcass = plinth + cab_body + back_panel
    for by in bay_ys:
        carcass = carcass + box_bounds(x0 + 14.0, x1, by, by + div_t, z_cab, z_top - 28.0)
    carcass.label = "wall_shelving_carcass"
    mat.apply_material(carcass, walnut)

    # Solid oak cabinet counter ledge + 3 upper open display shelves
    ledge = box_bounds(x0, x1, y0, y1, z_cab - 28.0, z_cab)
    ledge.label = "wall_shelving_ledge"
    mat.apply_material(ledge, oak)

    crown = box_bounds(x0, x1, y0, y1, z_top - 28.0, z_top)
    crown.label = "wall_shelving_top"
    mat.apply_material(crown, oak)

    shelves = [ledge, crown]
    for s_idx, sz in enumerate((z0 + 890.0, z0 + 1260.0)):
        for b_idx in range(len(bay_ys) - 1):
            sh = box_bounds(x0 + 14.0, x1, bay_ys[b_idx] + div_t, bay_ys[b_idx + 1], sz, sz + 26.0)
            sh.label = f"wall_shelf_{s_idx}_{b_idx}"
            mat.apply_material(sh, oak)
            shelves.append(sh)

    # 4 lower cabinet doors + brushed-brass bar pulls facing +X into the shop
    doors = []
    pulls = []
    n_doors = 4
    door_span = (y1 - y0 - (n_doors + 1) * 4.0) / n_doors
    for i in range(n_doors):
        dy0 = y0 + 4.0 + i * (door_span + 4.0)
        dy1 = dy0 + door_span
        d = box_bounds(x1 - 18.0, x1, dy0, dy1, z_plinth + 4.0, z_cab - 32.0)
        d.label = f"wall_cabinet_door_{i}"
        mat.apply_material(d, oak)
        doors.append(d)

        py = dy1 - 45.0 if i % 2 == 0 else dy0 + 45.0
        pz = z_cab - 105.0
        p_top = box_bounds(x1, x1 + 20.0, py - 5.0, py + 5.0, pz + 35.0, pz + 45.0)
        p_bot = box_bounds(x1, x1 + 20.0, py - 5.0, py + 5.0, pz - 45.0, pz - 35.0)
        p_bar = box_bounds(x1 + 20.0, x1 + 28.0, py - 5.0, py + 5.0, pz - 45.0, pz + 45.0)
        pull = p_top + p_bot + p_bar
        pull.label = f"wall_cabinet_pull_{i}"
        mat.apply_material(pull, brass)
        pulls.append(pull)

    return bd.Compound(
        children=[carcass, *shelves, *doors, *pulls],
        label="wall_shelving_unit",
    )


def _build_service_counter():
    """1-person checkout & service counter with slatted cedar front, butcher-block oak top & POS terminal."""
    oak = mat.oak_millwork()
    walnut = mat.walnut_trim()
    cedar = mat.cedar_siding()
    black_steel = mat.matte_black_steel()
    brass = mat.brushed_brass()
    z0 = S.SLAB_TOP_Z

    x0, x1 = -380.0, 1590.0     # 1970 mm wide (862 mm staff pass-through on left)
    y0, y1 = 580.0, 1180.0      # 600 mm deep (740 mm clear shopkeeper station behind)
    z_kick = z0 + 95.0          # 395.0
    z_under = z0 + 880.0        # 1180.0
    z_top = z0 + 920.0          # 1220.0 (920 mm counter height)

    # 1. Recessed toe-kick + open-back walnut cabinet carcass with shopkeeper shelf & cash drawer front
    kick = box_bounds(x0 + 20.0, x1 - 20.0, y0 + 55.0, y1 - 15.0, z0, z_kick)
    front_backing = box_bounds(x0, x1, y0 + 26.0, y0 + 54.0, z_kick, z_under)
    side_l = box_bounds(x0, x0 + 28.0, y0 + 54.0, y1, z_kick, z_under)
    side_r = box_bounds(x1 - 28.0, x1, y0 + 54.0, y1, z_kick, z_under)
    mid_div = box_bounds(585.0, 613.0, y0 + 54.0, y1 - 10.0, z_kick, z_under)
    bot_deck = box_bounds(x0 + 28.0, x1 - 28.0, y0 + 54.0, y1, z_kick, z_kick + 26.0)
    mid_shelf_l = box_bounds(x0 + 28.0, 585.0, y0 + 54.0, y1 - 20.0, z0 + 460.0, z0 + 486.0)
    mid_shelf_r = box_bounds(613.0, x1 - 28.0, y0 + 54.0, y1 - 20.0, z0 + 460.0, z0 + 486.0)
    carcass = kick + front_backing + side_l + side_r + mid_div + bot_deck + mid_shelf_l + mid_shelf_r
    carcass.label = "counter_carcass"
    mat.apply_material(carcass, walnut)

    # Under-counter shopkeeper utility drawer (facing +Y behind counter, right bay)
    drawer_face = box_bounds(618.0, x1 - 33.0, y1 - 22.0, y1, z0 + 700.0, z_under - 12.0)
    drawer_face.label = "counter_drawer_front"
    mat.apply_material(drawer_face, oak)
    dx_mid = 0.5 * (618.0 + x1 - 33.0)
    dz_mid = 0.5 * (z0 + 700.0 + z_under - 12.0)
    dp_l = box_bounds(dx_mid - 50.0, dx_mid - 40.0, y1, y1 + 18.0, dz_mid - 5.0, dz_mid + 5.0)
    dp_r = box_bounds(dx_mid + 40.0, dx_mid + 50.0, y1, y1 + 18.0, dz_mid - 5.0, dz_mid + 5.0)
    dp_bar = box_bounds(dx_mid - 50.0, dx_mid + 50.0, y1 + 18.0, y1 + 26.0, dz_mid - 5.0, dz_mid + 5.0)
    drawer_pull = dp_l + dp_r + dp_bar
    drawer_pull.label = "counter_drawer_pull"
    mat.apply_material(drawer_pull, brass)

    # 2. Vertical slatted cedar decorative customer apron (28 slats across front -Y face)
    slats = []
    n_slats = 28
    slat_w = 34.0
    span_x = (x1 - 20.0) - (x0 + 20.0) - slat_w
    pitch = span_x / (n_slats - 1)
    for i in range(n_slats):
        sx = x0 + 20.0 + i * pitch
        slat = box_bounds(sx, sx + slat_w, y0, y0 + 26.0, z_kick, z_under)
        slat.label = f"counter_slat_{i}"
        mat.apply_material(slat, cedar)
        slats.append(slat)

    # 3. Butcher-block solid white-oak countertop with 40 mm customer-side overhang
    ctop = box_bounds(x0 - 20.0, x1 + 15.0, y0 - 40.0, y1 + 10.0, z_under, z_top)
    ctop_edges = ctop.edges().filter_by(
        lambda e: abs(e.bounding_box().min.Z - z_top) < 0.5 and abs(e.bounding_box().max.Z - z_top) < 0.5
    )
    ctop = ctop.chamfer(5.0, None, ctop_edges)
    ctop.label = "counter_oak_top"
    mat.apply_material(ctop, oak)

    # 4. Minimalist POS checkout terminal & cash drawer seated flush on countertop (Z = 1220)
    px0, px1 = -240.0, 140.0
    py0, py1 = 720.0, 1040.0
    cash_box = box_bounds(px0, px1, py0, py1, z_top, z_top + 88.0)
    cash_box.label = "pos_cash_drawer"
    mat.apply_material(cash_box, black_steel)

    # Angled sleek touchscreen stand mounted on top of cash drawer facing shopkeeper (+Y)
    pcx, pcy = 0.5 * (px0 + px1), 0.5 * (py0 + py1)
    stand_base = box_bounds(pcx - 65.0, pcx + 65.0, pcy - 55.0, pcy + 55.0, z_top + 88.0, z_top + 100.0)
    neck = box_bounds(pcx - 18.0, pcx + 18.0, pcy - 15.0, pcy + 15.0, z_top + 100.0, z_top + 225.0)
    screen = (
        bd.Pos(pcx, pcy + 20.0, z_top + 245.0)
        * bd.Rot(32.0, 0, 0)
        * bd.Box(260.0, 18.0, 175.0)
    )
    pos_stand = stand_base + neck + screen
    pos_stand.label = "pos_display_terminal"
    mat.apply_material(pos_stand, black_steel)

    return bd.Compound(
        children=[
            carcass,
            drawer_face,
            drawer_pull,
            bd.Compound(children=slats, label="counter_front_slats"),
            ctop,
            bd.Compound(children=[cash_box, pos_stand], label="pos_terminal"),
        ],
        label="service_counter",
    )


def _build_shopkeeper_stool():
    """Ergonomic 1-person wooden counter stool positioned behind the service counter."""
    oak = mat.oak_millwork()
    walnut = mat.walnut_trim()
    z0 = S.SLAB_TOP_Z

    cx, cy = 620.0, 1520.0
    seat_bot_z = z0 + 605.0    # 905.0
    seat_top_z = z0 + 640.0    # 940.0 (640 mm seat height for 920 mm counter)

    # 4 splayed tapered wooden legs meeting concrete floor Z = 300 cleanly up to seat underside Z = 905
    r_bot = 185.0
    r_top = 122.0
    legs = []
    for k in range(4):
        ang = math.radians(45.0 + k * 90.0)
        p0 = bd.Vector(cx + r_bot * math.cos(ang), cy + r_bot * math.sin(ang), z0)
        p1 = bd.Vector(cx + r_top * math.cos(ang), cy + r_top * math.sin(ang), seat_bot_z)
        axis_v = (p1 - p0).normalized()
        leg_len = (p1 - p0).length
        # Build tapered cylinder along leg axis, then clip bottom & top cleanly at Z = z0 and Z = seat_bot_z
        p_ext0 = p0 - axis_v * 20.0
        leg_plane = bd.Plane(origin=p_ext0, z_dir=axis_v)
        raw_leg = leg_plane * bd.Cone(
            17.0, 21.0, leg_len + 40.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
        )
        clip_box = box_bounds(cx - 300.0, cx + 300.0, cy - 300.0, cy + 300.0, z0, seat_bot_z)
        legs.append(raw_leg & clip_box)

    # Cross footrest rungs joining opposite legs at Z = z0 + 210 (510 mm)
    z_rung = z0 + 210.0
    r_rung = r_bot - (r_bot - r_top) * (210.0 / 605.0)
    rungs = []
    for k in range(2):
        ang = math.radians(45.0 + k * 90.0)
        p_a = bd.Vector(cx + r_rung * math.cos(ang), cy + r_rung * math.sin(ang), z_rung)
        p_b = bd.Vector(cx - r_rung * math.cos(ang), cy - r_rung * math.sin(ang), z_rung)
        d = (p_b - p_a)
        rung_plane = bd.Plane(origin=p_a, z_dir=d.normalized())
        rungs.append(rung_plane * bd.Cylinder(11.0, d.length, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)))

    stool_base = legs[0]
    for part in legs[1:] + rungs:
        stool_base = stool_base + part
    stool_base.label = "stool_legs"
    mat.apply_material(stool_base, walnut)

    # Sculpted round white-oak seat (Ø360 mm, chamfered rim resting flush on legs at Z = 905)
    seat = bd.Pos(cx, cy, seat_bot_z) * bd.Cylinder(
        180.0, seat_top_z - seat_bot_z, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    seat = seat.fillet(8.0, seat.edges())
    seat.label = "stool_seat"
    mat.apply_material(seat, oak)

    return bd.Compound(children=[stool_base, seat], label="shopkeeper_stool")


def _build_rear_storage():
    """Rear back-wall storage credenza and two floating white-oak shelves with matte-black steel brackets."""
    oak = mat.oak_millwork()
    walnut = mat.walnut_trim()
    brass = mat.brushed_brass()
    black_steel = mat.matte_black_steel()
    z0 = S.SLAB_TOP_Z

    x0, x1 = -1080.0, 1560.0    # 2640 mm wide
    y0, y1 = 1920.0, 2322.0     # 402 mm deep (7 mm clear of rear baseboard)
    z_kick = z0 + 85.0
    z_under = z0 + 805.0        # 1105.0
    z_top = z0 + 840.0          # 1140.0

    # Credenza base carcass
    kick = box_bounds(x0 + 10.0, x1 - 10.0, y0 + 45.0, y1, z0, z_kick)
    body = box_bounds(x0, x1, y0 + 18.0, y1, z_kick, z_under)
    carcass = kick + body
    carcass.label = "rear_credenza_carcass"
    mat.apply_material(carcass, walnut)

    # Oak top
    top = box_bounds(x0 - 10.0, x1 + 10.0, y0 - 10.0, y1, z_under, z_top)
    top.label = "rear_credenza_top"
    mat.apply_material(top, oak)

    # 5 storage cabinet doors facing -Y toward shopkeeper + brass bar pulls
    doors = []
    pulls = []
    n_doors = 5
    dw = (x1 - x0 - (n_doors + 1) * 4.0) / n_doors
    for i in range(n_doors):
        dx0 = x0 + 4.0 + i * (dw + 4.0)
        dx1 = dx0 + dw
        d = box_bounds(dx0, dx1, y0, y0 + 18.0, z_kick + 4.0, z_under - 4.0)
        d.label = f"rear_credenza_door_{i}"
        mat.apply_material(d, oak)
        doors.append(d)

        px = dx1 - 45.0 if i % 2 == 0 else dx0 + 45.0
        pz = z_under - 85.0
        p1 = box_bounds(px - 5.0, px + 5.0, y0 - 20.0, y0, pz + 35.0, pz + 45.0)
        p2 = box_bounds(px - 5.0, px + 5.0, y0 - 20.0, y0, pz - 45.0, pz - 35.0)
        pb = box_bounds(px - 5.0, px + 5.0, y0 - 28.0, y0 - 20.0, pz - 45.0, pz + 45.0)
        pull = p1 + p2 + pb
        pull.label = f"rear_credenza_pull_{i}"
        mat.apply_material(pull, brass)
        pulls.append(pull)

    # Two upper wall-mounted oak shelves anchored to rear birch interior wall (Y = 2345)
    shelves = []
    brackets = []
    sx0, sx1 = -1040.0, 1520.0
    sy0, sy1 = S.ROOM_Y_MAX - 250.0, S.ROOM_Y_MAX
    bracket_xs = (-840.0, -140.0, 560.0, 1320.0)
    for j, sz in enumerate((1480.0, 1800.0)):
        sh = box_bounds(sx0, sx1, sy0, sy1, sz, sz + 32.0)
        sh.label = f"rear_wall_shelf_{j}"
        mat.apply_material(sh, oak)
        shelves.append(sh)

        for k, bx in enumerate(bracket_xs):
            vert = box_bounds(bx - 12.0, bx + 12.0, sy1 - 10.0, sy1, sz - 150.0, sz)
            horiz = box_bounds(bx - 12.0, bx + 12.0, sy0 + 25.0, sy1 - 10.0, sz - 10.0, sz)
            br = vert + horiz
            br.label = f"rear_shelf_bracket_{j}_{k}"
            mat.apply_material(br, black_steel)
            brackets.append(br)

    return bd.Compound(
        children=[carcass, top, *doors, *pulls, *shelves, *brackets],
        label="rear_storage",
    )


def _build_ceiling_pendants():
    """Two minimalist dome pendant lamps suspended directly from interior collar ties."""
    black_steel = mat.matte_black_steel()
    oak = mat.oak_millwork()
    lamp_glass = mat.warm_lamp_globe()

    # Hang cleanly from collar ties at Y = -450 (customer floor) and Y = +750 (above service counter)
    specs = [
        ("pendant_customer", 50.0, -450.0, 2560.0),
        ("pendant_counter", 560.0, 750.0, 2380.0),
    ]
    pendants = []
    for lbl, cx, cy, z_shade_top in specs:
        z_ceil = S.COLLAR_BOT_Z  # 3260.0

        # Canopy flush against collar tie underside (40 x 40 mm fits cleanly inside 45 mm collar tie)
        canopy = box_bounds(cx - 20.0, cx + 20.0, cy - 20.0, cy + 20.0, z_ceil - 22.0, z_ceil)
        cord = bd.Pos(cx, cy, z_shade_top + 48.0) * bd.Cylinder(
            5.0, (z_ceil - 22.0) - (z_shade_top + 48.0), align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
        )
        # Hollow matte-black steel pendant dome shade
        dome_outer = bd.Pos(cx, cy, z_shade_top) * bd.Cone(
            145.0, 34.0, 145.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MAX)
        )
        dome_inner = bd.Pos(cx, cy, z_shade_top - 6.0) * bd.Cone(
            136.0, 28.0, 140.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MAX)
        )
        shade = canopy + cord + (dome_outer - dome_inner)
        shade.label = f"{lbl}_fixture"
        mat.apply_material(shade, black_steel)

        # Warm white-oak decorative neck cap sitting flush on top of steel shade
        cap = bd.Pos(cx, cy, z_shade_top) * bd.Cylinder(
            34.0, 48.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
        )
        cap.label = f"{lbl}_wood_cap"
        mat.apply_material(cap, oak)

        # Warm glowing frosted bulb nestled cleanly inside hollow dome
        bulb = bd.Pos(cx, cy, z_shade_top - 102.0) * bd.Sphere(42.0)
        bulb.label = f"{lbl}_bulb"
        mat.apply_material(bulb, lamp_glass)

        pendants.append(bd.Compound(children=[shade, cap, bulb], label=lbl))

    return bd.Compound(children=pendants, label="ceiling_pendants")


@model
def interior():
    """Complete 1-person shop interior millwork and lighting."""
    bench = _build_window_display_bench()
    shelving = _build_left_wall_shelving()
    counter = _build_service_counter()
    stool = _build_shopkeeper_stool()
    rear = _build_rear_storage()
    pendants = _build_ceiling_pendants()

    return bd.Compound(
        children=[bench, shelving, counter, stool, rear, pendants],
        label="interior",
    )


if __name__ == "__main__":
    interior()
