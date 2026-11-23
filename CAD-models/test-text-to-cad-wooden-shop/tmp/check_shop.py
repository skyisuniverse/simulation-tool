"""Geometric verification checks for the 1-story 1-person wooden shop assembly.

Measures exact B-rep dimensions, bearing contacts (closest_points == 0),
clear circulation clearances, open-door sweep clearance, and solid validity.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import build123d as bd
from cad.build123d import closest_points, leaves, overlap_volume, posed

from lib import spec as S
from wooden_shop import wooden_shop


def find_part(tree, label: str):
    matches = [part for part in leaves(tree) if part.label == label]
    if len(matches) != 1:
        raise ValueError(f"Expected one part labelled {label!r}, found {len(matches)}")
    return matches[0]


def verify_shop(tree, tree_open):
    errors = []

    def check_contact(a_lbl: str, b_lbl: str, tol: float = 0.05):
        a, b = find_part(tree, a_lbl), find_part(tree, b_lbl)
        d = closest_points(a, b).distance
        print(f"  contact {a_lbl} <-> {b_lbl}: {d:.4f} mm")
        if d > tol:
            errors.append(f"Floating gap {d:.3f} mm between {a_lbl} and {b_lbl}")

    print("1. Checking structural load-path bearing contacts (slab -> membrane -> walls -> roof, posts -> shoes):")
    check_contact("concrete_slab", "sill_membrane_main")
    check_contact("concrete_slab", "sill_membrane_front_left")
    check_contact("concrete_slab", "post_shoe_left")
    check_contact("concrete_slab", "post_shoe_mid")
    check_contact("concrete_slab", "post_shoe_right")
    check_contact("sill_membrane_main", "rear_wall_frame_bottom_plate_0")
    check_contact("post_shoe_left", "porch_post_left")
    check_contact("post_shoe_mid", "porch_post_mid")
    check_contact("post_shoe_right", "porch_post_right")
    check_contact("porch_post_left", "porch_front_beam")
    check_contact("porch_front_beam", "porch_truss_king_post")
    check_contact("porch_truss_rafter_right", "roof_deck")
    check_contact("roof_deck", "metal_roof_pan")
    check_contact("concrete_slab", "door_threshold")

    print("\n2. Checking interior furniture contacts on slab & collar-tie pendant mounts:")
    check_contact("concrete_slab", "counter_carcass")
    check_contact("concrete_slab", "wall_shelving_carcass")
    check_contact("concrete_slab", "display_bench_base")
    check_contact("concrete_slab", "stool_legs")
    check_contact("concrete_slab", "rear_credenza_carcass")
    check_contact("collar_tie_1", "pendant_customer_fixture")
    check_contact("collar_tie_3", "pendant_counter_fixture")

    print("\n3. Checking key architectural dimensions & 1-person ergonomic clearances:")
    slab = find_part(tree, "concrete_slab")
    slab_bb = slab.bounding_box()
    print(f"  Concrete foundation bounds: {slab_bb.size.X:.1f} x {slab_bb.size.Y:.1f} x {slab_bb.size.Z:.1f} mm")
    if abs(slab_bb.min.Z) > 0.01 or abs(slab_bb.max.Z - S.SLAB_TOP_Z) > 0.01:
        errors.append(f"Slab Z bounds mismatch: [{slab_bb.min.Z}, {slab_bb.max.Z}]")

    # Clear interior floor area between birch lining walls
    left_lin = find_part(tree, "interior_lining_left").bounding_box().max.X
    right_lin = find_part(tree, "interior_lining_right").bounding_box().min.X
    front_lin = find_part(tree, "interior_lining_front").bounding_box().max.Y
    rear_lin = find_part(tree, "interior_lining_rear").bounding_box().min.Y
    int_w = right_lin - left_lin
    int_d = rear_lin - front_lin
    int_area_m2 = (int_w * int_d) / 1e6
    print(f"  Interior clear room: {int_w:.1f} x {int_d:.1f} mm ({int_area_m2:.2f} m^2)")
    if int_area_m2 < 10.0:
        errors.append(f"Interior floor area too small: {int_area_m2:.2f} m^2")

    # Staff pass-through aisle between left wall shelving & checkout counter
    shelf_max_x = find_part(tree, "wall_shelving_top").bounding_box().max.X
    counter_min_x = find_part(tree, "counter_oak_top").bounding_box().min.X
    staff_aisle = counter_min_x - shelf_max_x
    print(f"  Staff pass-through aisle (shelving to counter): {staff_aisle:.1f} mm")
    if staff_aisle < 750.0:
        errors.append(f"Staff aisle too narrow: {staff_aisle:.1f} mm")

    # Shopkeeper standing/stool zone behind counter (counter back to rear credenza)
    counter_max_y = find_part(tree, "counter_oak_top").bounding_box().max.Y
    credenza_min_y = find_part(tree, "rear_credenza_top").bounding_box().min.Y
    keeper_zone = credenza_min_y - counter_max_y
    print(f"  Shopkeeper work zone behind counter: {keeper_zone:.1f} mm")
    if keeper_zone < 650.0:
        errors.append(f"Shopkeeper zone too tight: {keeper_zone:.1f} mm")

    # Open door clearance to left porch post & jamb at 92 deg open
    door_open = find_part(tree_open, "door_wood_leaf")
    handle_open = find_part(tree_open, "door_handle_ext")
    post_left = find_part(tree_open, "porch_post_left")
    jamb_open = find_part(tree_open, "door_jamb_frame")
    d_post = closest_points(door_open, post_left).distance
    d_handle_post = closest_points(handle_open, post_left).distance
    ov_jamb = overlap_volume(door_open.solids()[0], jamb_open.solids()[0])
    print(f"  Open door (92 deg) clearance to left porch post: leaf={d_post:.1f} mm, handle={d_handle_post:.1f} mm")
    print(f"  Open door (92 deg) overlap with jamb: {ov_jamb:.4f} mm^3")
    if d_post < 50.0 or d_handle_post < 50.0:
        errors.append(f"Open door too close to porch post: leaf={d_post:.1f}, handle={d_handle_post:.1f}")
    if ov_jamb > 0.001:
        errors.append(f"Open door overlaps jamb by {ov_jamb:.2f} mm^3")

    print("\n4. Checking positive volume & validity across all 362 leaf solids:")
    all_parts = leaves(tree)
    inv_count = 0
    invalid_count = 0
    for part in all_parts:
        for s in part.solids():
            if s.volume <= 0:
                inv_count += 1
                errors.append(f"Non-positive volume solid in {part.label}: {s.volume}")
            if not s.is_valid:
                invalid_count += 1
                errors.append(f"Invalid B-rep solid in {part.label}")
    print(f"  Checked {len(all_parts)} parts: inverted={inv_count}, invalid={invalid_count}")

    return errors


if __name__ == "__main__":
    handle = wooden_shop()
    tree = handle.shape
    tree_open = posed(handle, "open")

    errs = verify_shop(tree, tree_open)
    if errs:
        print("\nFAILED checks:")
        for e in errs:
            print("  -", e)
        sys.exit(1)

    # Planted-fault self-test: verify our contact check actually catches a lifted part!
    print("\n5. Planted-fault self-test (verifying contact check detects a 5 mm lifted post shoe):")
    slab = find_part(tree, "concrete_slab")
    shoe = find_part(tree, "post_shoe_left")
    lifted_shoe = bd.Pos(0, 0, 5.0) * shoe
    planted_gap = closest_points(slab, lifted_shoe).distance
    assert abs(planted_gap - 5.0) < 0.05, f"Expected 5.0 mm planted gap, measured {planted_gap}"
    print(f"  Planted 5.0 mm lift correctly caught -> measured gap = {planted_gap:.3f} mm")

    print("\nALL CHECKS PASSED!")
