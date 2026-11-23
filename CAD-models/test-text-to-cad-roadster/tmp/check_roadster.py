"""Geometry and clearance verification script for the Tesla Roadster CAD model."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import build123d as bd
from cad.build123d import closest_points, leaves

from roadster import tesla_roadster


def find_part(tree, label):
    matches = [part for part in leaves(tree) if part.label == label]
    if len(matches) != 1:
        raise ValueError(f"Expected one part labelled {label!r}, found {len(matches)}")
    return matches[0]


def main():
    doc = tesla_roadster().shape
    bb = doc.bounding_box()
    print(f"Overall bounds: X=[{bb.min.X:.1f}, {bb.max.X:.1f}] ({bb.size.X:.1f} mm)")
    print(f"                Y=[{bb.min.Y:.1f}, {bb.max.Y:.1f}] ({bb.size.Y:.1f} mm)")
    print(f"                Z=[{bb.min.Z:.1f}, {bb.max.Z:.1f}] ({bb.size.Z:.1f} mm)")

    # Verify all 4 tires touch Z = 0 ground plane cleanly
    all_leaves = list(leaves(doc, paths=True))
    tyres = [(path, p) for path, p in all_leaves if "tyre_" in p.label]
    print(f"Found {len(tyres)} tyres:")
    for path, t in tyres:
        tbb = t.bounding_box()
        print(f"  {'/'.join(path)}: Z_min={tbb.min.Z:.2f} mm, Z_max={tbb.max.Z:.2f} mm, Y=[{tbb.min.Y:.1f}, {tbb.max.Y:.1f}]")
        assert abs(tbb.min.Z) < 0.5, f"Tyre {path} does not sit on ground Z=0: {tbb.min.Z}"

    # Verify front splitter ground clearance (>= 90 mm)
    splitter = find_part(doc, "front_carbon_splitter")
    sbb = splitter.bounding_box()
    print(f"Front splitter ground clearance: {sbb.min.Z:.1f} mm")
    assert sbb.min.Z >= 90.0

    # Verify battery pack ground clearance (>= 110 mm)
    batt = find_part(doc, "battery_pack_200kwh")
    bbb = batt.bounding_box()
    print(f"Battery pack ground clearance: {bbb.min.Z:.1f} mm")
    assert bbb.min.Z >= 110.0

    # Verify brake caliper clears rim cleanly on front_left
    cal_fl = find_part(doc, "brake_caliper_front_left")
    rim_fl = [p for path, p in all_leaves if path[-1] == "rim_front" and "corner_front_left" in path][0]
    cal_gap = closest_points(cal_fl, rim_fl).distance
    print(f"Front-left caliper-to-rim clearance: {cal_gap:.2f} mm")
    assert cal_gap > 2.0, f"Caliper too close to rim: {cal_gap}"

    print("ALL GEOMETRY CHECKS PASSED!")


if __name__ == "__main__":
    main()
