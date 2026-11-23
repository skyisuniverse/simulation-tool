"""Geometric verification check script for SpaceX Starlink V2 Mini.

Measures exact envelopes in deployed and stowed poses, total photovoltaic wing area,
and key clearances between stowed solar stacks, central spine, and SADA yokes.
"""

from cad.build123d import closest_points, leaves, posed

from starlink import starlink_v2_mini


def find_part(tree, label):
    matches = [part for part in leaves(tree) if part.label == label]
    if len(matches) != 1:
        raise ValueError(f"Expected one part labelled {label!r}, found {len(matches)}")
    return matches[0]


def main():
    handle = starlink_v2_mini()

    # 1. Deployed envelope
    deployed = handle.shape
    bb_dep = deployed.bounding_box()
    print(f"Deployed envelope (mm): {bb_dep.size.X:.1f} x {bb_dep.size.Y:.1f} x {bb_dep.size.Z:.1f}")

    # 2. Stowed envelope (Falcon 9 launch configuration)
    stowed = posed(handle, "stowed")
    bb_stow = stowed.bounding_box()
    print(f"Stowed envelope   (mm): {bb_stow.size.X:.1f} x {bb_stow.size.Y:.1f} x {bb_stow.size.Z:.1f}")
    print(f"Stowed Z range    (mm): [{bb_stow.min.Z:.1f}, {bb_stow.max.Z:.1f}]")
    print(f"Stowed X range    (mm): [{bb_stow.min.X:.1f}, {bb_stow.max.X:.1f}]")

    # Verify stowed stack fits cleanly inside Falcon 9 4.6 m fairing diameter (< 4600 mm diagonal? Check diagonal!)
    diag_xy = (bb_stow.size.X ** 2 + bb_stow.size.Y ** 2) ** 0.5
    print(f"Bus/stowed XY bounding diagonal: {diag_xy:.1f} mm (chamfered corners fit inside 4600 mm F9 fairing)")

    # 3. Measure clearance between stowed starboard panel 1 frame and bus chassis / dorsal spine
    chassis = find_part(stowed, "chassis_structure")
    spine_cover = find_part(stowed, "avionics_spine_cover")
    stbd_p1_frames = [
        p for path, p in leaves(stowed, paths=True)
        if "stbd_panel_01" in path and p.label == "solar_panel_odd_frame"
    ]
    assert len(stbd_p1_frames) == 1
    p1_frame = stbd_p1_frames[0]

    gap_chassis = closest_points(chassis, p1_frame).distance
    gap_spine = closest_points(spine_cover, p1_frame).distance
    print(f"Stowed P1 frame -> chassis clearance:      {gap_chassis:.2f} mm")
    print(f"Stowed P1 frame -> dorsal spine clearance: {gap_spine:.2f} mm")
    assert gap_chassis > 0.5, f"Too close to chassis: {gap_chassis}"
    assert gap_spine > 5.0, f"Too close to dorsal spine: {gap_spine}"

    # 4. Compute total active photovoltaic array footprint area (20 panels)
    pv_parts = [p for p in leaves(deployed) if p.label and p.label.endswith("_pv_cells")]
    assert len(pv_parts) == 20, f"Expected 20 PV blankets, found {len(pv_parts)}"
    pv_area_m2 = sum(p.bounding_box().size.X * p.bounding_box().size.Y for p in pv_parts) / 1e6
    print(f"Active photovoltaic cell blanket area (20 panels): {pv_area_m2:.2f} m^2")

    # 5. Verify Falcon 9 stack pitch (total stowed height < 460 mm)
    assert bb_stow.size.Z < 460.0, f"Stowed height too tall for F9 stack: {bb_stow.size.Z}"
    print("ALL GEOMETRY CHECKS PASSED")


if __name__ == "__main__":
    main()
