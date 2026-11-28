"""Panoramic wraparound windshield, helmet-visor side windows & frit trim for the Tesla Semi.

Built directly from the shared `@memo` Class-A `build_cab_envelope` NURBS skin so
every curved glass pane and black ceramic frit gasket matches the cab curvature to
sub-millimetre precision with zero interference and realistic recessed flush seating.
"""

import build123d as bd
from bd_materials import glass, plastics
from cad import model

import dims as D
from cab_shell_lib import (
    build_cab_envelope,
    build_side_window_aperture,
    build_windshield_aperture,
)


def _smoked_glass(part):
    part.material = glass.soda_lime()
    part.material.pbr = part.material.pbr.override(
        roughness=0.05,
        transmission=0.88,
        ior=1.52,
        clearcoat=1.0,
        clearcoat_roughness=0.04,
    )
    part.color = D.COLOR_GLASS_TINT
    return part


def _black_frit(part):
    part.material = plastics.abs_()
    part.material.pbr = part.material.pbr.override(
        roughness=0.18, metalness=0.08, clearcoat=0.85, clearcoat_roughness=0.08
    )
    part.color = D.COLOR_TRIM_BLACK
    return part


def _make_windshield():
    """Expansive deeply curved wraparound panoramic windshield + black ceramic frit perimeter."""
    parts = []
    # Glass shell recessed 10 mm inside outer skin (14 mm laminated safety glass: inset 10..24)
    glass_skin = build_cab_envelope(10.0) - build_cab_envelope(24.0)
    ws_glass = glass_skin & build_windshield_aperture(margin=12.0)
    ws_glass.label = "windshield_glass"
    parts.append(_smoked_glass(ws_glass))

    # Flush black ceramic frit / rubber perimeter gasket (1.5 mm clear of silver frame, 1 mm clear of glass)
    frit_skin = build_cab_envelope(6.0) - build_cab_envelope(26.0)
    frit_band = build_windshield_aperture(margin=1.5) - build_windshield_aperture(margin=11.0)
    ws_frit = frit_skin & frit_band
    ws_frit.label = "windshield_frit"
    parts.append(_black_frit(ws_frit))

    return parts


def _make_side_windows():
    """Iconic helmet-visor wraparound side windows (left & right) + black frit & B-pillar bars."""
    parts = []
    glass_skin = build_cab_envelope(10.0) - build_cab_envelope(24.0)
    frit_skin = build_cab_envelope(6.0) - build_cab_envelope(26.0)

    # Crisp gloss-black vertical B-pillar divider bar at Y = 2860 separating door drop-glass
    # from the sleek triangular rear quarter window!
    b_pillar_cut = bd.Pos(0.0, 2860.0, 2030.0) * bd.Box(2800.0, 44.0, 1200.0)
    b_pillar_bar = bd.Pos(0.0, 2860.0, 2030.0) * bd.Box(2800.0, 40.0, 1200.0)

    sw_aperture_glass = build_side_window_aperture(margin=12.0)
    sw_glass_all = (glass_skin & sw_aperture_glass) - b_pillar_cut
    sw_frit_base = (
        build_side_window_aperture(margin=1.5) - build_side_window_aperture(margin=11.0)
    )
    sw_frit_all = frit_skin & (sw_frit_base + (sw_aperture_glass & b_pillar_bar))

    # Split cleanly into left (+X) and right (-X) assemblies
    left_half = bd.Pos(800.0, 2200.0, 2000.0) * bd.Box(1600.0, 3200.0, 2400.0)
    right_half = bd.Pos(-800.0, 2200.0, 2000.0) * bd.Box(1600.0, 3200.0, 2400.0)

    for side, half_box in (("left", left_half), ("right", right_half)):
        sg = sw_glass_all & half_box
        sg.label = f"side_window_glass_{side}"
        parts.append(_smoked_glass(sg))

        sf = sw_frit_all & half_box
        sf.label = f"side_window_frit_{side}"
        parts.append(_black_frit(sf))

    return parts


def _make_rear_cab_window():
    """Flush rear cab bulkhead window overlooking catwalk & fifth wheel (Y = 3562 mm)."""
    parts = []
    # Black outer rubber frame mounted flush on rear structural bulkhead
    frame_outer = bd.Pos(0.0, D.CAB_BULKHEAD_Y + 6.0, 2280.0) * bd.Box(780.0, 10.0, 440.0)
    frame_cut = bd.Pos(0.0, D.CAB_BULKHEAD_Y + 6.0, 2280.0) * bd.Box(720.0, 20.0, 380.0)
    frame = frame_outer - frame_cut
    frame.label = "rear_window_frame"
    parts.append(_black_frit(frame))

    # Smoked rear glass pane seated inside frame (2 mm clear)
    pane = bd.Pos(0.0, D.CAB_BULKHEAD_Y + 6.0, 2280.0) * bd.Box(714.0, 8.0, 374.0)
    pane.label = "rear_window_glass"
    parts.append(_smoked_glass(pane))

    return parts


@model
def glazing():
    """Complete Tesla Semi panoramic windshield, helmet-visor side glazing & rear window."""
    parts = []
    parts.extend(_make_windshield())
    parts.extend(_make_side_windows())
    parts.extend(_make_rear_cab_window())
    return bd.Compound(children=parts, label="glazing")


if __name__ == "__main__":
    glazing()
