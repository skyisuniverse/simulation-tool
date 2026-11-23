"""Tesla Cybertruck powered frunk lid, V-bowed stainless front nose fascia, and full-width white LED DRL lightbar.

Built in world coordinates (closed / as-built position) so the root assembly can attach it directly
with a clean RevoluteJoint hinge near the cowl edge.
"""

from __future__ import annotations

import build123d as bd
from cad import model

from lib import geometry, materials, spec

# 5 evenly spaced lateral stations for a single smooth B-spline sweep (zero vertical facet bands!)
_X_SLICES = [-896.0, -448.0, 0.0, 448.0, 896.0]


def _smooth_loft(sections_3d: list[list[tuple[float, float, float]]]) -> bd.Solid:
    """Create a single smooth swept solid through evenly spaced planar cross-sections."""
    faces = [bd.Face(bd.Wire.make_polygon(pts)) for pts in sections_3d]
    return bd.loft(faces, ruled=False)


def _hood_section_at_x(x: float) -> list[tuple[float, float, float]]:
    """Return a 4-point YZ cross-section of the stainless steel frunk hood at lateral coordinate x."""
    # Outer edges stop 6 mm inside the front fender shoulder / cant-rail seam
    u = abs(x) / 896.0
    # Front lip follows subtle curved-V bow; cowl trailing edge follows gentle cowl bow
    s_front = spec.S_NOSE_CENTER + spec.front_bow_ds(x)
    s_rear = spec.S_COWL_CENTER + spec.cowl_bow_ds(x) - 10.0  # 10 mm cowl vent gap ahead of windshield
    # Hood width tapers smoothly from 896 mm at front lip to 866 mm at cowl: scale x along hood
    x_front = x
    x_rear = x * (866.0 / 896.0)

    # Laser-straight horizontal front hood lip matching the full-width DRL lightbar cleanly
    z_front = spec.Z_DRL_TOP + 5.0
    z_rear = spec.Z_COWL - 16.0 * (u ** 1.6)
    thick = 9.0

    return [
        (x_front, spec.s_to_y(s_front), z_front),
        (x_rear, spec.s_to_y(s_rear), z_rear),
        (x_rear, spec.s_to_y(s_rear), z_rear - thick),
        (x_front, spec.s_to_y(s_front), z_front - thick),
    ]


def _build_frunk_hood() -> bd.Solid:
    """Crisp gently-bowed stainless steel powered frunk hood panel."""
    sections = [_hood_section_at_x(x) for x in _X_SLICES]
    hood = _smooth_loft(sections)
    return materials.apply_mat(hood, materials.stainless_30x, "frunk_hood")


def _build_front_fascia() -> bd.Solid:
    """Vertical-ish raked stainless steel front nose panel directly below the full-width DRL lightbar."""
    # Spans X in [-876, +876] so it clears the 2-deg inward-tucked lower front fender skin (X=885) cleanly.
    fascia_slices = [-876.0, -438.0, 0.0, 438.0, 876.0]
    sections = []
    for x in fascia_slices:
        s_top = spec.S_NOSE_CENTER + spec.front_bow_ds(x) + 4.0
        s_bot = s_top - 22.0
        z_top = spec.Z_DRL_BOT - 3.0            # 1005 mm
        z_bot = spec.Z_HEADLIGHT_SLOT_TOP + 3.0  # 738 mm
        thick = 12.0
        sections.append([
            (x, spec.s_to_y(s_top), z_top),
            (x, spec.s_to_y(s_bot), z_bot),
            (x, spec.s_to_y(s_bot) + thick, z_bot),
            (x, spec.s_to_y(s_top) + thick, z_top),
        ])
    fascia = _smooth_loft(sections)
    return materials.apply_mat(fascia, materials.stainless_30x, "frunk_front_fascia")


def _build_drl_lightbar() -> tuple[bd.Solid, bd.Solid]:
    """Full-width continuous bright-white front LED DRL lightbar seated in its slim dark bezel."""
    bezel_secs = []
    lens_secs = []
    for x in _X_SLICES:
        s_face = spec.S_NOSE_CENTER + spec.front_bow_ds(x) + 5.0
        y_f = spec.s_to_y(s_face)
        # Bezel housing (Z = 1006 .. 1040, sits strictly behind lens y_f + 4.5..22 and under hood >= 1041)
        bezel_secs.append([
            (x, y_f + 5.0, spec.Z_DRL_BOT - 1.5),
            (x, y_f + 5.0, spec.Z_DRL_TOP - 5.0),
            (x, y_f + 22.0, spec.Z_DRL_TOP - 5.0),
            (x, y_f + 22.0, spec.Z_DRL_BOT - 1.5),
        ])
        # Emissive white LED light blade (Z = 1012 .. 1036, strictly ahead of bezel y_f - 2..+3.5)
        x_lens = x * 0.996
        lens_secs.append([
            (x_lens, y_f - 2.0, spec.Z_DRL_BOT + 4.0),
            (x_lens, y_f - 2.0, spec.Z_DRL_TOP - 9.0),
            (x_lens, y_f + 3.5, spec.Z_DRL_TOP - 9.0),
            (x_lens, y_f + 3.5, spec.Z_DRL_BOT + 4.0),
        ])

    bezel = _smooth_loft(bezel_secs)
    lens = _smooth_loft(lens_secs)
    return (
        materials.apply_mat(bezel, materials.dark_charcoal_trim, "front_drl_bezel"),
        materials.apply_mat(lens, materials.drl_white_led, "front_drl_lightbar"),
    )


@model
def cybertruck_frunk():
    """Complete powered frunk lid assembly (hood + front stainless nose fascia + full-width DRL lightbar)."""
    hood = _build_frunk_hood()
    fascia = _build_front_fascia()
    bezel, lens = _build_drl_lightbar()
    return bd.Compound(
        children=[hood, fascia, bezel, lens],
        label="cybertruck_frunk",
    )


if __name__ == "__main__":
    cybertruck_frunk()
