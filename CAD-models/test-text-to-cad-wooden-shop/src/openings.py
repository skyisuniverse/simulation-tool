"""Articulated glazed wooden entrance door (RevoluteJoint) and shop windows."""

import build123d as bd
from cad import model
from cad.build123d import configuration_sequence, mechanism_state

from lib import materials as mat
from lib import spec as S
from lib.geom import box_bounds


# Front door hinge axis (just proud of exterior jamb face so leaf swings cleanly outward onto porch)
DOOR_HINGE_X = -1410.0
DOOR_HINGE_Y = S.EXT_Y_MIN - 9.0  # -1746.0
DOOR_HINGE_ZS = (560.0, 1350.0, 2140.0)


def _build_front_door():
    """Build the front entrance door frame and hinged glazed oak door leaf with RevoluteJoint."""
    trim_mat = mat.walnut_trim()
    oak = mat.oak_millwork()
    galv = mat.galvanized_steel()
    brass = mat.brushed_brass()
    glass_mat = mat.architectural_glass()

    y_ext = S.EXT_Y_MIN      # -1737.0
    y_int = S.ROOM_Y_MIN     # -1545.0
    jamb_t = 42.0
    thresh_h = 24.0
    z_thresh_top = S.DOOR_Z_MIN + thresh_h  # 324.0

    # 1. Fixed Door Threshold (galvanized aluminum/steel resting on concrete slab Z = 300)
    threshold = box_bounds(
        S.DOOR_X_MIN, S.DOOR_X_MAX, y_ext - 6.0, y_int, S.DOOR_Z_MIN, z_thresh_top
    )
    threshold.label = "door_threshold"
    mat.apply_material(threshold, galv)

    # 2. Fixed Door Jamb Frame + Interior Door Stop
    jamb_l = box_bounds(S.DOOR_X_MIN, S.DOOR_X_MIN + jamb_t, y_ext, y_int, z_thresh_top, S.DOOR_Z_MAX - jamb_t)
    jamb_r = box_bounds(S.DOOR_X_MAX - jamb_t, S.DOOR_X_MAX, y_ext, y_int, z_thresh_top, S.DOOR_Z_MAX - jamb_t)
    jamb_h = box_bounds(S.DOOR_X_MIN, S.DOOR_X_MAX, y_ext, y_int, S.DOOR_Z_MAX - jamb_t, S.DOOR_Z_MAX)

    # Interior door stop strip behind the closed door leaf (leaf sits at Y = -1732 .. -1686)
    stop_y0, stop_y1 = -1684.0, -1662.0
    stop_l = box_bounds(S.DOOR_X_MIN + jamb_t, S.DOOR_X_MIN + jamb_t + 14.0, stop_y0, stop_y1, z_thresh_top, S.DOOR_Z_MAX - jamb_t - 14.0)
    stop_r = box_bounds(S.DOOR_X_MAX - jamb_t - 14.0, S.DOOR_X_MAX - jamb_t, stop_y0, stop_y1, z_thresh_top, S.DOOR_Z_MAX - jamb_t - 14.0)
    stop_t = box_bounds(S.DOOR_X_MIN + jamb_t, S.DOOR_X_MAX - jamb_t, stop_y0, stop_y1, S.DOOR_Z_MAX - jamb_t - 14.0, S.DOOR_Z_MAX - jamb_t)

    door_jamb = jamb_l + jamb_r + jamb_h + stop_l + stop_r + stop_t
    door_jamb.label = "door_jamb_frame"
    mat.apply_material(door_jamb, trim_mat)

    # Frame-side brass hinge knuckles (lower half of each barrel, 1 mm clear of door knuckles)
    frame_hinges = []
    for i, hz in enumerate(DOOR_HINGE_ZS):
        knuckle = bd.Pos(DOOR_HINGE_X, DOOR_HINGE_Y, hz - 44.0) * bd.Cylinder(
            7.0, 43.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
        )
        # Mounting tab bridging knuckle back to front edge of left jamb (X = -1445 .. -1410, Y = -1737)
        tab = box_bounds(DOOR_HINGE_X - 32.0, DOOR_HINGE_X, DOOR_HINGE_Y + 2.0, y_ext, hz - 44.0, hz - 1.0)
        hk = knuckle + tab
        hk.label = f"door_hinge_frame_{i}"
        mat.apply_material(hk, brass)
        frame_hinges.append(hk)

    # 3. Moving Door Leaf (crafted white-oak stile-and-rail door with 4-lite upper glazing & brass levers)
    dx0 = S.DOOR_X_MIN + jamb_t + 4.0   # -1404.0 (4 mm reveal)
    dx1 = S.DOOR_X_MAX - jamb_t - 4.0   # -546.0  (858 mm wide leaf)
    dz0 = z_thresh_top + 6.0            # 330.0   (6 mm sweep clearance)
    dz1 = S.DOOR_Z_MAX - jamb_t - 4.0   # 2408.0  (2078 mm tall leaf)
    dy0 = y_ext + 5.0                   # -1732.0 (exterior face)
    dy1 = dy0 + 46.0                    # -1686.0 (46 mm solid door thickness)
    dy_mid = 0.5 * (dy0 + dy1)          # -1709.0

    stile_w = 115.0
    bot_rail_h = 220.0
    top_rail_h = 120.0
    lock_z0, lock_z1 = 1185.0, 1315.0   # Lock rail centered at Z = 1250 (950 mm above slab)

    in_x0 = dx0 + stile_w               # -1289.0
    in_x1 = dx1 - stile_w               # -661.0
    low_z0 = dz0 + bot_rail_h           # 550.0
    glaze_z1 = dz1 - top_rail_h         # 2288.0

    # Stile-and-rail wooden door carcass
    stile_l = box_bounds(dx0, in_x0, dy0, dy1, dz0, dz1)
    stile_r = box_bounds(in_x1, dx1, dy0, dy1, dz0, dz1)
    rail_bot = box_bounds(in_x0, in_x1, dy0, dy1, dz0, low_z0)
    rail_lock = box_bounds(in_x0, in_x1, dy0, dy1, lock_z0, lock_z1)
    rail_top = box_bounds(in_x0, in_x1, dy0, dy1, glaze_z1, dz1)
    lower_panel = box_bounds(in_x0, in_x1, dy_mid - 11.0, dy_mid + 11.0, low_z0, lock_z0)

    # 2x2 wooden muntin cross dividing upper glazing into 4 crisp shop panes
    mx_mid = 0.5 * (in_x0 + in_x1)      # -975.0
    mz_mid = 0.5 * (lock_z1 + glaze_z1) # 1801.5
    mun_w = 26.0
    mun_d = 34.0
    muntin_v = box_bounds(mx_mid - mun_w / 2, mx_mid + mun_w / 2, dy_mid - mun_d / 2, dy_mid + mun_d / 2, lock_z1, glaze_z1)
    muntin_h = box_bounds(in_x0, in_x1, dy_mid - mun_d / 2, dy_mid + mun_d / 2, mz_mid - mun_w / 2, mz_mid + mun_w / 2)

    door_wood = stile_l + stile_r + rail_bot + rail_lock + rail_top + lower_panel + muntin_v + muntin_h
    door_wood.label = "door_wood_leaf"
    mat.apply_material(door_wood, oak)

    # 4 individual clear tempered glass panes fitted cleanly in the 2x2 muntin bays (zero overlap)
    panes = []
    x_bays = [(in_x0, mx_mid - mun_w / 2), (mx_mid + mun_w / 2, in_x1)]
    z_bays = [(lock_z1, mz_mid - mun_w / 2), (mz_mid + mun_w / 2, glaze_z1)]
    p_idx = 0
    for bx0, bx1 in x_bays:
        for bz0, bz1 in z_bays:
            pane = box_bounds(bx0, bx1, dy_mid - 4.0, dy_mid + 4.0, bz0, bz1)
            pane.label = f"door_glass_pane_{p_idx}"
            mat.apply_material(pane, glass_mat)
            panes.append(pane)
            p_idx += 1

    # Brushed-brass door handles (exterior & interior escutcheons + lever handles) & leaf hinge knuckles
    hw_x = dx1 - 62.0   # -608.0 (centered on right lock stile)
    hw_z = 1250.0
    hw_parts = []

    for side_lbl, face_y, out_y in (("ext", dy0, -1.0), ("int", dy1, 1.0)):
        py0, py1 = (face_y - 8.0, face_y) if out_y < 0 else (face_y, face_y + 8.0)
        plate = box_bounds(hw_x - 22.0, hw_x + 22.0, py0, py1, hw_z - 95.0, hw_z + 65.0)
        stem_y0, stem_y1 = (face_y - 52.0, py0) if out_y < 0 else (py1, face_y + 52.0)
        stem = bd.Pos(hw_x, 0.5 * (stem_y0 + stem_y1), hw_z) * bd.Rot(90.0, 0, 0) * bd.Cylinder(9.0, 44.0)
        lever_y0, lever_y1 = (face_y - 68.0, face_y - 50.0) if out_y < 0 else (face_y + 50.0, face_y + 68.0)
        lever = box_bounds(hw_x - 125.0, hw_x + 12.0, lever_y0, lever_y1, hw_z - 10.0, hw_z + 10.0)
        # Keyhole cylinder boss below handle
        lock_y0, lock_y1 = (face_y - 16.0, py0) if out_y < 0 else (py1, face_y + 16.0)
        key_boss = bd.Pos(hw_x, 0.5 * (lock_y0 + lock_y1), hw_z - 55.0) * bd.Rot(90.0, 0, 0) * bd.Cylinder(11.0, 8.0)
        handle = plate + stem + lever + key_boss
        handle.label = f"door_handle_{side_lbl}"
        mat.apply_material(handle, brass)
        hw_parts.append(handle)

    # Door-side brass hinge knuckles (upper half of each barrel, 1 mm clear above frame knuckle)
    for i, hz in enumerate(DOOR_HINGE_ZS):
        knuckle = bd.Pos(DOOR_HINGE_X, DOOR_HINGE_Y, hz) * bd.Cylinder(
            7.0, 43.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
        )
        # Cranked brass hinge strap clearing the left jamb cleanly in front of Y = -1737
        strap_front = box_bounds(DOOR_HINGE_X, dx0 + 30.0, DOOR_HINGE_Y + 2.0, y_ext - 2.0, hz, hz + 43.0)
        strap_return = box_bounds(dx0, dx0 + 30.0, y_ext - 2.0, dy0, hz, hz + 43.0)
        dk = knuckle + strap_front + strap_return
        dk.label = f"door_hinge_leaf_{i}"
        mat.apply_material(dk, brass)
        hw_parts.append(dk)

    # Assemble leaf sub-compound and connect with native build123d RevoluteJoint
    door_leaf = bd.Compound(children=[door_wood, *panes, *hw_parts], label="door_leaf")

    # RevoluteJoint on door_jamb (fixed parent), axis pointing -Z so +angle swings door outward (-Y)
    hinge_axis = bd.Axis((DOOR_HINGE_X, DOOR_HINGE_Y, 1350.0), (0, 0, -1))
    hinge = bd.RevoluteJoint("front_door_hinge", door_jamb, axis=hinge_axis, angular_range=(0.0, 100.0))
    bd.RigidJoint("front_door_hinge", door_leaf, hinge.location)
    hinge.connect_to(door_leaf.joints["front_door_hinge"], angle=0.0)

    door_frame = bd.Compound(
        children=[threshold, door_jamb, *frame_hinges],
        label="door_frame",
    )
    return bd.Compound(children=[door_frame, door_leaf], label="front_door")


def _build_window(
    name: str,
    axis: str,
    u0: float,
    u1: float,
    z0: float,
    z1: float,
    v_ext: float,
    v_int: float,
    *,
    frame_t: float = 52.0,
    sash_t: float = 34.0,
    n_panes: int = 2,
    interior_sill_depth: float = 0.0,
):
    """Build a multi-pane timber-framed architectural window spanning rough opening [u0, u1] x [z0, z1].

    axis = 'X' for front/rear walls (u along X, v along Y);
    axis = 'Y' for left/right walls (u along Y, v along X).
    """
    trim_mat = mat.walnut_trim()
    oak = mat.oak_millwork()
    glass_mat = mat.architectural_glass()

    v_lo, v_hi = min(v_ext, v_int), max(v_ext, v_int)
    v_mid = 0.5 * (v_lo + v_hi)

    def mk(ua, ub, va, vb, za, zb):
        if axis == "X":
            return box_bounds(ua, ub, va, vb, za, zb)
        return box_bounds(va, vb, ua, ub, za, zb)

    # Outer perimeter window frame filling full wall thickness (v_lo .. v_hi)
    f_bot = mk(u0, u1, v_lo, v_hi, z0, z0 + frame_t)
    f_top = mk(u0, u1, v_lo, v_hi, z1 - frame_t, z1)
    f_l = mk(u0, u0 + frame_t, v_lo, v_hi, z0 + frame_t, z1 - frame_t)
    f_r = mk(u1 - frame_t, u1, v_lo, v_hi, z0 + frame_t, z1 - frame_t)
    outer_frame = f_bot + f_top + f_l + f_r

    # Recessed sash surround + vertical mullions dividing into n_panes bays
    su0, su1 = u0 + frame_t, u1 - frame_t
    sz0, sz1 = z0 + frame_t, z1 - frame_t
    sash_d = 64.0
    sv0, sv1 = v_mid - sash_d / 2, v_mid + sash_d / 2

    s_bot = mk(su0, su1, sv0, sv1, sz0, sz0 + sash_t)
    s_top = mk(su0, su1, sv0, sv1, sz1 - sash_t, sz1)
    s_l = mk(su0, su0 + sash_t, sv0, sv1, sz0 + sash_t, sz1 - sash_t)
    s_r = mk(su1 - sash_t, su1, sv0, sv1, sz0 + sash_t, sz1 - sash_t)

    frame_solid = outer_frame + s_bot + s_top + s_l + s_r

    # Clear glazing opening inside sash
    gu0, gu1 = su0 + sash_t, su1 - sash_t
    gz0, gz1 = sz0 + sash_t, sz1 - sash_t
    mul_w = 46.0
    bay_w = ((gu1 - gu0) - (n_panes - 1) * mul_w) / n_panes

    panes = []
    for i in range(n_panes):
        bu0 = gu0 + i * (bay_w + mul_w)
        bu1 = bu0 + bay_w
        pane = mk(bu0, bu1, v_mid - 5.0, v_mid + 5.0, gz0, gz1)
        pane.label = f"{name}_glass_{i}"
        mat.apply_material(pane, glass_mat)
        panes.append(pane)
        if i < n_panes - 1:
            mul = mk(bu1, bu1 + mul_w, sv0, sv1, gz0, gz1)
            frame_solid = frame_solid + mul

    frame_solid.label = f"{name}_frame"
    mat.apply_material(frame_solid, trim_mat)

    parts = [frame_solid, *panes]

    # Optional interior white-oak window sill ledge protruding cleanly into the room
    if interior_sill_depth > 0.0:
        in_dir = 1.0 if v_int > v_ext else -1.0
        sv_a, sv_b = (v_int, v_int + interior_sill_depth) if in_dir > 0 else (v_int - interior_sill_depth, v_int)
        sill = mk(u0 - 30.0, u1 + 30.0, sv_a, sv_b, z0 - 28.0, z0)
        sill.label = f"{name}_interior_sill"
        mat.apply_material(sill, oak)
        parts.append(sill)

    return bd.Compound(children=parts, label=name)


@model
def openings():
    """Articulated front entrance door and all four timber-framed shop windows."""
    front_door = _build_front_door()

    front_window = _build_window(
        "front_showcase_window",
        axis="X",
        u0=S.FRONT_WIN_X_MIN,
        u1=S.FRONT_WIN_X_MAX,
        z0=S.FRONT_WIN_Z_MIN,
        z1=S.FRONT_WIN_Z_MAX,
        v_ext=S.EXT_Y_MIN,
        v_int=S.ROOM_Y_MIN,
        frame_t=52.0,
        sash_t=36.0,
        n_panes=2,
        interior_sill_depth=45.0,
    )
    right_window = _build_window(
        "right_side_window",
        axis="Y",
        u0=S.RIGHT_WIN_Y_MIN,
        u1=S.RIGHT_WIN_Y_MAX,
        z0=S.RIGHT_WIN_Z_MIN,
        z1=S.RIGHT_WIN_Z_MAX,
        v_ext=S.EXT_X_MAX,
        v_int=S.ROOM_X_MAX,
        frame_t=52.0,
        sash_t=34.0,
        n_panes=2,
        interior_sill_depth=45.0,
    )
    left_transom = _build_window(
        "left_clerestory_window",
        axis="Y",
        u0=S.LEFT_WIN_Y_MIN,
        u1=S.LEFT_WIN_Y_MAX,
        z0=S.LEFT_WIN_Z_MIN,
        z1=S.LEFT_WIN_Z_MAX,
        v_ext=S.EXT_X_MIN,
        v_int=S.ROOM_X_MIN,
        frame_t=40.0,
        sash_t=28.0,
        n_panes=2,
    )
    rear_transom = _build_window(
        "rear_clerestory_window",
        axis="X",
        u0=S.REAR_WIN_X_MIN,
        u1=S.REAR_WIN_X_MAX,
        z0=S.REAR_WIN_Z_MIN,
        z1=S.REAR_WIN_Z_MAX,
        v_ext=S.EXT_Y_MAX,
        v_int=S.ROOM_Y_MAX,
        frame_t=40.0,
        sash_t=28.0,
        n_panes=3,
    )

    asm = bd.Compound(
        children=[front_door, front_window, right_window, left_transom, rear_transom],
        label="openings",
    )
    mechanism_state(asm, "closed", front_door_hinge=0.0)
    mechanism_state(asm, "ajar", front_door_hinge=35.0)
    mechanism_state(asm, "open", front_door_hinge=92.0)
    return configuration_sequence(
        asm,
        "door_cycle",
        [(0.0, "closed"), (2.0, "open"), (3.5, "open"), (5.5, "closed")],
    )


if __name__ == "__main__":
    openings()
