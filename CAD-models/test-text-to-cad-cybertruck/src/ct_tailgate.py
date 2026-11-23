"""Tesla Cybertruck flat 30X stainless steel tailgate, full-width crimson LED taillight bar, and top cap.

Built in world coordinates (closed / as-built position) so the root assembly can attach it with a
clean bottom RevoluteJoint hinge that swings open 90 degrees flat.
"""

from __future__ import annotations

import build123d as bd
from cad import model

from lib import geometry, materials, spec


def _build_tailgate_panel() -> bd.Solid:
    """Flat slightly-raked stainless steel tailgate panel with recessed upper taillight channel."""
    hw_top = 905.0  # crisp clearance inside +/-915 mm inner rear quarter panels
    hw_bot = 880.0  # matches 2 deg inward lower tuck inside +/-887 mm lower inner rear quarters
    z_bot = spec.Z_TAILGATE_BOT + 14.0  # 664 mm (clears rear bumper shelf Z=646 even at 90 deg open!)
    z_top = spec.Z_BELT_REAR            # 1368 mm (top polymer cap sits at 1368..1380)
    y_bot_out = spec.s_to_y(spec.S_TAILGATE_TOP + 9.0)   # s = 5644
    y_top_out = spec.s_to_y(spec.S_TAILGATE_TOP + 3.0)   # s = 5638 (inner face at s=5606, clears bed 5597 & tonneau 5598!)
    thick = 32.0

    # Ruled loft from bottom to top trapezoidal horizontal cross-sections
    sec_bot = [
        (hw_bot, y_bot_out, z_bot),
        (-hw_bot, y_bot_out, z_bot),
        (-hw_bot, y_bot_out - thick, z_bot),
        (hw_bot, y_bot_out - thick, z_bot),
    ]
    sec_top = [
        (hw_top, y_top_out, z_top),
        (-hw_top, y_top_out, z_top),
        (-hw_top, y_top_out - thick, z_top),
        (hw_top, y_top_out - thick, z_top),
    ]
    panel = geometry.ruled_loft_sections([sec_bot, sec_top])

    # Cut horizontal full-width recess channel across the upper tailgate for the red LED lightbar
    y_ch = y_top_out + 2.0
    channel = bd.Pos(0.0, y_ch, 1336.0) * bd.Box(
        hw_top * 2.0 + 10.0,
        24.0,
        42.0,
        align=(bd.Align.CENTER, bd.Align.MAX, bd.Align.CENTER),
    )
    panel = panel - channel
    return materials.apply_mat(panel, materials.stainless_30x, "tailgate_panel")


def _build_rear_lightbar() -> tuple[bd.Solid, bd.Solid]:
    """Full-width recessed gloss-black bezel & glowing crimson-red rear LED taillight blade."""
    hw = 903.0
    y_rear = spec.s_to_y(spec.S_TAILGATE_TOP + 3.0)

    # Dark housing bezel nested cleanly inside the 42 mm recess (Z = 1316 .. 1356)
    bezel = bd.Pos(0.0, y_rear - 5.0, 1336.0) * bd.Box(
        hw * 2.0,
        14.0,
        38.0,
        align=(bd.Align.CENTER, bd.Align.MAX, bd.Align.CENTER),
    )

    # Signature full-width red LED light blade (Z = 1326 .. 1346, sitting flush with tailgate face)
    center_bar = bd.Pos(0.0, y_rear - 4.5, 1336.0) * bd.Box(
        1330.0,
        7.0,
        20.0,
        align=(bd.Align.CENTER, bd.Align.MIN, bd.Align.CENTER),
    )
    outer_l = bd.Pos(788.0, y_rear - 4.5, 1336.0) * bd.Box(
        224.0,
        7.0,
        20.0,
        align=(bd.Align.CENTER, bd.Align.MIN, bd.Align.CENTER),
    )
    outer_r = bd.Pos(-788.0, y_rear - 4.5, 1336.0) * bd.Box(
        224.0,
        7.0,
        20.0,
        align=(bd.Align.CENTER, bd.Align.MIN, bd.Align.CENTER),
    )
    lens = center_bar + [outer_l, outer_r]

    return (
        materials.apply_mat(bezel, materials.gloss_black_pillar, "tailgate_light_bezel"),
        materials.apply_mat(lens, materials.taillight_red_led, "rear_taillight_bar"),
    )


def _build_top_cap() -> bd.Solid:
    """Matte-black heavy-duty polymer upper tailgate lip / spoiler cap (Z = 1369..1381)."""
    hw = 905.0
    y_top_out = spec.s_to_y(spec.S_TAILGATE_TOP + 3.0)
    cap = bd.Pos(0.0, y_top_out - 16.0, spec.Z_BELT_REAR + 0.8) * bd.Box(
        hw * 2.0,
        32.0,
        12.0,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    return materials.apply_mat(cap, materials.matte_black_cladding, "tailgate_top_cap")


@model
def cybertruck_tailgate():
    """Complete Cybertruck tailgate assembly (stainless steel panel + red LED lightbar + top cap)."""
    panel = _build_tailgate_panel()
    bezel, lens = _build_rear_lightbar()
    cap = _build_top_cap()
    return bd.Compound(
        children=[panel, bezel, lens, cap],
        label="cybertruck_tailgate",
    )


if __name__ == "__main__":
    cybertruck_tailgate()
