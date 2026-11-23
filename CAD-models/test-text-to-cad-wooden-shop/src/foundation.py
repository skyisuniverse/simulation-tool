"""Monolithic concrete foundation slab, entry step, damp-proof membrane, and porch post shoes."""

import build123d as bd
from cad import model

from lib import materials as mat
from lib import spec as S
from lib.geom import box_bounds


def _build_concrete_slab():
    """Build the monolithic thickened-edge concrete slab with front entry step and control joints."""
    footing = box_bounds(
        -S.FOOTING_W / 2,
        S.FOOTING_W / 2,
        S.FOOTING_Y_MIN,
        S.FOOTING_Y_MAX,
        0.0,
        S.FOOTING_H,
    )
    upper = box_bounds(
        -S.SLAB_W / 2,
        S.SLAB_W / 2,
        S.SLAB_Y_MIN,
        S.SLAB_Y_MAX,
        S.FOOTING_H,
        S.SLAB_TOP_Z,
    )
    step = box_bounds(
        S.STEP_X_MIN,
        S.STEP_X_MAX,
        S.STEP_Y_MIN,
        S.SLAB_Y_MIN,
        0.0,
        S.STEP_H,
    )

    slab = footing + upper + step

    # Chamfer outer top edges of the upper slab (Z = 300) for a realistic troweled concrete edge
    top_edges = slab.edges().filter_by(lambda e: abs(e.bounding_box().min.Z - S.SLAB_TOP_Z) < 0.5 and abs(e.bounding_box().max.Z - S.SLAB_TOP_Z) < 0.5)
    slab = slab.chamfer(8.0, None, top_edges)

    # Chamfer the front nose edge of the entry step (Z = 150, Y = STEP_Y_MIN)
    step_nose = slab.edges().filter_by(
        lambda e: abs(e.bounding_box().min.Z - S.STEP_H) < 0.5
        and abs(e.bounding_box().max.Z - S.STEP_H) < 0.5
        and abs(e.bounding_box().min.Y - S.STEP_Y_MIN) < 0.5
    )
    if step_nose:
        slab = slab.chamfer(6.0, None, step_nose)

    # Shallow expansion/control joint grooves cut into the finished slab surface (6 mm wide x 6 mm deep)
    grooves = [
        # Interior cross control joints (clear of walls & door)
        box_bounds(-1560.0, 1560.0, 397.0, 403.0, S.SLAB_TOP_Z - 6.0, S.SLAB_TOP_Z + 1.0),
        box_bounds(-3.0, 3.0, -1480.0, 2280.0, S.SLAB_TOP_Z - 6.0, S.SLAB_TOP_Z + 1.0),
        # Porch apron architectural score joints (clear of porch post shoes)
        box_bounds(-1048.0, -1042.0, S.SLAB_Y_MIN + 25.0, S.SHOP_Y_MIN - 45.0, S.SLAB_TOP_Z - 6.0, S.SLAB_TOP_Z + 1.0),
        box_bounds(677.0, 683.0, S.SLAB_Y_MIN + 25.0, S.SHOP_Y_MIN - 45.0, S.SLAB_TOP_Z - 6.0, S.SLAB_TOP_Z + 1.0),
    ]
    slab = slab - grooves

    slab.label = "concrete_slab"
    mat.apply_material(slab, mat.concrete_slab())
    return slab


def _build_sill_membrane():
    """Build 4 mm EPDM damp-proof sill membrane under all four perimeter wall bottom plates."""
    z0 = S.SLAB_TOP_Z
    z1 = S.WALL_BASE_Z

    front_left = box_bounds(S.SHOP_X_MIN, S.DOOR_X_MIN, S.SHOP_Y_MIN, S.INNER_Y_MIN, z0, z1)
    front_left.label = "sill_membrane_front_left"
    mat.apply_material(front_left, mat.epdm_membrane())

    # Continuous C-loop: front-right + right + rear + left wall bases (no doorway interrupt)
    front_right = box_bounds(S.DOOR_X_MAX, S.SHOP_X_MAX, S.SHOP_Y_MIN, S.INNER_Y_MIN, z0, z1)
    right_wall = box_bounds(S.INNER_X_MAX, S.SHOP_X_MAX, S.INNER_Y_MIN, S.INNER_Y_MAX, z0, z1)
    rear_wall = box_bounds(S.SHOP_X_MIN, S.SHOP_X_MAX, S.INNER_Y_MAX, S.SHOP_Y_MAX, z0, z1)
    left_wall = box_bounds(S.SHOP_X_MIN, S.INNER_X_MIN, S.INNER_Y_MIN, S.INNER_Y_MAX, z0, z1)

    main_loop = front_right + right_wall + rear_wall + left_wall
    main_loop.label = "sill_membrane_main"
    mat.apply_material(main_loop, mat.epdm_membrane())

    return [front_left, main_loop]


def _build_post_shoe(cx: float, cy: float, label: str):
    """Build a galvanized steel U-shaped porch post base shoe anchored on the concrete slab."""
    z0 = S.SLAB_TOP_Z
    z_plate = z0 + S.POST_SHOE_BASE_H            # 308.0
    z_seat = S.POST_BASE_Z                        # 324.0
    z_ear_top = z_plate + S.POST_SHOE_EAR_H       # 448.0
    half_p = S.POST_SIZE / 2                      # 60.0

    # Base flange widened along X (176 x 140 mm) to expose 4 concrete anchor bolts cleanly
    base = box_bounds(cx - 88.0, cx + 88.0, cy - 70.0, cy + 70.0, z0, z_plate)
    # Moisture-break standoff pedestal directly beneath the 120 x 120 mm wooden column
    standoff = box_bounds(cx - half_p, cx + half_p, cy - half_p, cy + half_p, z_plate, z_seat)
    # Front and back vertical steel ears hugging the post's -Y and +Y faces cleanly
    ear_front = box_bounds(
        cx - half_p, cx + half_p, cy - half_p - S.POST_SHOE_EAR_T, cy - half_p, z_plate, z_ear_top
    )
    ear_back = box_bounds(
        cx - half_p, cx + half_p, cy + half_p, cy + half_p + S.POST_SHOE_EAR_T, z_plate, z_ear_top
    )

    shoe = base + standoff + ear_front + ear_back

    # 4 concrete anchor bolt washers + hex heads on the exposed X flanges
    bolts = []
    for sx in (-1.0, 1.0):
        for sy in (-1.0, 1.0):
            bx = cx + sx * 74.0
            by = cy + sy * 44.0
            washer = bd.Pos(bx, by, z_plate) * bd.Cylinder(
                10.0, 3.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
            )
            hex_head = bd.Pos(bx, by, z_plate + 3.0) * bd.extrude(
                bd.RegularPolygon(8.5, 6), amount=8.0
            )
            bolts.append(washer + hex_head)

    # 2 pairs of side through-bolt heads protruding outward from the vertical steel ears
    for bz in (z_seat + 40.0, z_seat + 92.0):
        for sy in (-1.0, 1.0):
            ear_outer_y = cy + sy * (half_p + S.POST_SHOE_EAR_T)
            nut = bd.Pos(cx, ear_outer_y, bz) * bd.Rot(90.0 * (-sy), 0, 0) * bd.Cylinder(
                8.0, 8.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
            )
            bolts.append(nut)

    for b in bolts:
        shoe = shoe + b

    shoe.label = label
    mat.apply_material(shoe, mat.galvanized_steel())
    return shoe


@model
def foundation():
    """Complete concrete slab foundation with damp-proof membrane and galvanized post shoes."""
    slab = _build_concrete_slab()
    membranes = _build_sill_membrane()
    shoe_labels = ("post_shoe_left", "post_shoe_mid", "post_shoe_right")
    shoes = [
        _build_post_shoe(cx, S.PORCH_POST_Y, lbl)
        for cx, lbl in zip(S.PORCH_POST_XS, shoe_labels)
    ]

    # Verify exact overall dimensions on built geometry
    bb = slab.bounding_box()
    assert abs(bb.min.Z - 0.0) < 1e-4, bb
    assert abs(bb.max.Z - S.SLAB_TOP_Z) < 1e-4, bb
    assert abs(bb.size.X - S.FOOTING_W) < 1e-4, bb

    return bd.Compound(
        children=[
            slab,
            bd.Compound(children=membranes, label="sill_membrane"),
            bd.Compound(children=shoes, label="porch_post_shoes"),
        ],
        label="foundation",
    )


if __name__ == "__main__":
    foundation()
