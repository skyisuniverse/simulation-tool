"""Geometry & specification verification check script for the original Tesla Semi CAD assembly."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import build123d as bd
from cad.build123d import closest_points, leaves

import dims as D
from tesla_semi import tesla_semi


def find_part(tree, label):
    matches = [part for part in leaves(tree) if part.label == label]
    if len(matches) != 1:
        raise ValueError(f"Expected one part labelled {label!r}, found {len(matches)}")
    return matches[0]


def main():
    doc = tesla_semi().shape
    bb = doc.bounding_box()
    print(f"Overall bounds (mm): X={bb.size.X:.1f}, Y={bb.size.Y:.1f}, Z={bb.size.Z:.1f}")
    print(f"  X: [{bb.min.X:.1f}, {bb.max.X:.1f}] (mirrors included)")
    print(f"  Y: [{bb.min.Y:.1f}, {bb.max.Y:.1f}]")
    print(f"  Z: [{bb.min.Z:.1f}, {bb.max.Z:.1f}]")

    # Verify tires sit squarely on ground plane Z = 0
    assert abs(bb.min.Z) < 1.0, f"Ground contact error: min.Z = {bb.min.Z}"

    # Verify cab body width (excluding side mirrors)
    cab_shell = find_part(doc, "cab_monocoque")
    cab_bb = cab_shell.bounding_box()
    print(f"Cab body width (excl. mirrors): {cab_bb.size.X:.1f} mm (target {D.BODY_WIDTH:.0f} mm)")
    print(f"Cab roof peak Z: {cab_bb.max.Z:.1f} mm (target {D.TOTAL_HEIGHT:.0f} mm)")
    assert 2500.0 <= cab_bb.size.X <= 2591.0, f"Cab width out of Class 8 envelope: {cab_bb.size.X}"
    assert abs(cab_bb.max.Z - D.TOTAL_HEIGHT) < 10.0

    # Verify fifth wheel height (standard 48 in = 1220 mm)
    fw_plate = find_part(doc, "fifth_wheel_plate")
    fw_z = fw_plate.bounding_box().max.Z
    print(f"Fifth wheel top saddle height: {fw_z:.1f} mm (target {D.FIFTH_WHEEL_Z_TOP:.0f} mm)")
    assert abs(fw_z - D.FIFTH_WHEEL_Z_TOP) < 2.0

    # Verify tire-to-cab arch clearance (front steer tire vs cab_monocoque)
    steer_tires = [
        part for path, part in leaves(doc, paths=True)
        if path[-2:] == ("steer_wheel_left", "tire")
    ]
    assert len(steer_tires) == 1
    arch_gap = closest_points(steer_tires[0], cab_shell).distance
    print(f"Front steer tire to cab wheel-arch clearance: {arch_gap:.1f} mm")
    assert arch_gap > 50.0, f"Insufficient wheel arch clearance: {arch_gap:.1f} mm"

    # Verify rear dual drive tire to rear quarter fender clearance
    qf_left = find_part(doc, "quarter_fender_left")
    drive_tires = [
        part for path, part in leaves(doc, paths=True)
        if path[-2] == "drive_wheels_fwd_left" and "tire" in path[-1]
    ]
    for dt in drive_tires:
        qf_gap = closest_points(dt, qf_left).distance
        print(f"Forward drive {dt.label} to quarter fender clearance: {qf_gap:.1f} mm")
        assert qf_gap > 35.0, f"Quarter fender too close to tire: {qf_gap:.1f} mm"

    # Verify windshield to steering wheel & dashboard clearance
    ws = find_part(doc, "windshield_glass")
    dash = find_part(doc, "dashboard_upper")
    dash_gap = closest_points(ws, dash).distance
    print(f"Panoramic windshield to dashboard clearance: {dash_gap:.1f} mm")
    assert dash_gap > 20.0, f"Dashboard too close to windshield: {dash_gap:.1f} mm"

    print("ALL TESLA SEMI GEOMETRY CHECKS PASSED!")


if __name__ == "__main__":
    main()
