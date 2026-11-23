"""Quantitative engineering geometry & clearance check for Mechazilla Tower (1:100 scale)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import build123d as bd
from cad.build123d import closest_points, leaves, posed

import spec as S
from mechazilla import mechazilla


def find_part(tree, label):
    matches = [part for part in leaves(tree) if part.label == label]
    if len(matches) != 1:
        raise ValueError(f"Expected one part labelled {label!r}, found {len(matches)}")
    return matches[0]


def verify_mechazilla():
    handle = mechazilla()
    tree = handle.shape
    bb = tree.bounding_box()

    # 1. Overall envelope checks (1:100 scale -> 1,500 mm = 150.0 m total tower height)
    assert abs(bb.min.Z - 0.0) < 1e-4, f"Ground Z mismatch: {bb.min.Z}"
    assert abs(bb.max.Z - 1500.0) < 1e-4, f"Total height mismatch: {bb.max.Z}"

    # 2. Structural contact checks (parts resting on foundation & guide rails on tower)
    apron = find_part(tree, "apron_slab")
    plinth = find_part(tree, "tower_plinth")
    bp_fp = find_part(tree, "base_plate_front_port")
    rail_p = find_part(tree, "guide_rail_port")
    assert closest_points(apron, plinth).distance < 1e-3, "Plinth floating off apron"
    assert closest_points(plinth, bp_fp).distance < 1e-3, "Base plate floating off plinth"

    # 3. 9.0 m (90.0 mm) Starship / Super Heavy booster fit check between closed sliding trolleys
    trol_p = find_part(tree, "trolley_body_port")
    trol_s = find_part(tree, "trolley_body_stbd")
    pad_p = find_part(tree, "catch_pad_port")
    pad_s = find_part(tree, "catch_pad_stbd")

    trolley_inner_gap = trol_p.bounding_box().min.Y - trol_s.bounding_box().max.Y
    pad_inner_gap = pad_p.bounding_box().min.Y - pad_s.bounding_box().max.Y
    trolley_x_center = (trol_p.bounding_box().min.X + trol_p.bounding_box().max.X) / 2.0

    # Verify Starship 90 mm fuselage fits cleanly between trolleys (>= 90.0 mm) & centered on X = 300 mm!
    assert trolley_inner_gap > 90.0, f"Trolleys too narrow for 90 mm Starship: {trolley_inner_gap:.2f} mm"
    assert abs(trolley_x_center - S.ROCKET_CENTER_X) < 0.05, f"Trolley X center {trolley_x_center:.2f} != 300"

    # 4. Catch rail & trolley running clearance (must be > 0, no overlap)
    crail_p = find_part(tree, "catch_rail_port")
    trol_rail_gap = closest_points(crail_p, trol_p).distance
    assert 0.25 < trol_rail_gap < 1.0, f"Unexpected trolley-rail clearance: {trol_rail_gap:.3f} mm"

    # 5. Carriage bogie vs vertical guide rail running clearance
    carr = find_part(tree, "carriage_frame")
    bogie_rail_gap = closest_points(carr, rail_p).distance
    assert 0.4 < bogie_rail_gap < 1.2, f"Unexpected bogie-rail clearance: {bogie_rail_gap:.3f} mm"

    # 6. Posed kinematic verification: catch_approach opens arm tips wide & raises carriage
    catch_tree = posed(handle, "catch_approach")
    open_pad_p = find_part(catch_tree, "catch_pad_port")
    open_pad_s = find_part(catch_tree, "catch_pad_stbd")
    open_span = open_pad_p.bounding_box().min.Y - open_pad_s.bounding_box().max.Y
    open_z = open_pad_p.bounding_box().min.Z
    built_z = pad_p.bounding_box().min.Z
    assert abs((open_z - built_z) - 440.0) < 0.1, f"Carriage lift delta mismatch: {open_z - built_z:.2f}"
    assert open_span > 220.0, f"Catch approach mouth not wide enough: {open_span:.2f} mm"

    # 7. Posed verification: SQD stowed clears carriage passing Z=825 (expect >= 20 mm = 2.0 m)
    pass_tree = posed(handle, {"carriage_lift": 300.0, "sqd_swing": -205.0})
    pass_carr = find_part(pass_tree, "carriage_frame")
    pass_sqd = find_part(pass_tree, "sqd_lattice_boom")
    pass_clearance = closest_points(pass_carr, pass_sqd).distance
    assert pass_clearance > 20.0, f"Carriage passing stowed SQD too close: {pass_clearance:.2f} mm"

    # 8. Planted-fault self-test: verify closest_points detects a 2 mm clash when trolley is shifted into rail
    faulty_trolley = bd.Pos(0, 2.0, 0) * trol_p
    fault_gap = closest_points(crail_p, faulty_trolley).distance
    assert fault_gap < 1e-6, f"Planted fault check failed to catch rail penetration: {fault_gap}"

    print("ALL MECHAZILLA GEOMETRY & CLEARANCE CHECKS PASSED:")
    print(f"  Total height:               {bb.max.Z:.1f} mm ({bb.max.Z / 10:.1f} m at 1:100)")
    print(f"  Footprint (as built):       {bb.size.X:.1f} x {bb.size.Y:.1f} mm")
    print(f"  Closed trolley clear span:  {trolley_inner_gap:.2f} mm ({trolley_inner_gap / 10:.2f} m; clears 9.0 m Booster)")
    print(f"  Closed catch pad span:      {pad_inner_gap:.2f} mm ({pad_inner_gap / 10:.2f} m; supports catch pins)")
    print(f"  Trolley X center:           {trolley_x_center:.2f} mm (Rocket CL = {S.ROCKET_CENTER_X:.1f} mm)")
    print(f"  Trolley-to-rail gap:        {trol_rail_gap:.2f} mm")
    print(f"  Bogie-to-guide-rail gap:    {bogie_rail_gap:.2f} mm")
    print(f"  Catch approach open span:   {open_span:.2f} mm ({open_span / 10:.2f} m at pads)")
    print(f"  Carriage lift delta check:  +{open_z - built_z:.1f} mm (exact +440.0 mm)")
    print(f"  Carriage-to-stowed-SQD gap: {pass_clearance:.1f} mm")


if __name__ == "__main__":
    verify_mechazilla()
