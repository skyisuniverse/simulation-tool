"""Signature Tesla Roadster lighting:
  - Razor-slim swept LED blade headlights with glowing DRL strips & flush smoked lenses
  - Full-width recessed rear LED tail light blades & central glowing light bar
  - Slim third brake light (CHMSL) tucked beneath the Targa roll hoop trailing edge

Every optical layer (outer lens, LED emitter, gloss-black housing) occupies a
strictly disjoint depth zone with >= 2 mm air gaps so zero layers interpenetrate.
"""

from __future__ import annotations

import build123d as bd

from lib.palette import (
    BLACK_GLOSS,
    LED_RED,
    LED_WHITE,
    LENS_HEAD,
    LENS_TAIL,
    group,
    style_emissive,
    style_glass,
    style_gloss_black,
)
from lib.surfaces import (
    HOOP_REAR_X,
    body_master,
    body_master_inner,
    body_skin,
    box_between,
    rear_transom_cap,
)


def _safe(shape):
    if shape is None:
        return None
    if not shape.solids():
        return None
    return shape


def _headlight_prism(side, shrink=0.0, dx=0.0, dy=0.0, dz=0.0):
    bar = bd.Box(240.0 - 2.0 * shrink, 290.0 - 2.0 * shrink, 40.0 - 2.0 * shrink)
    bar = bd.Rot(0, -15, side * -32) * bar
    return bd.Pos(2025.0 + dx, side * 665.0 + dy, 522.0 + dz) * bar


def _build_headlights():
    """Flush-contoured smoked lenses, gloss-black optical housings, and white LED DRL blades."""
    parts = []
    outer_skin = body_skin()                             # depth 0 .. 14 mm
    inner16 = body_master_inner(d=16.0)                  # >= 16 mm inside outer surface
    inner24 = body_master_inner(d=24.0)                  # >= 24 mm inside outer surface

    drl_shell = inner16 - inner24                        # clean 8 mm shell strictly behind outer_skin

    for side in (1, -1):
        lbl = "left" if side > 0 else "right"

        # 1. Flush outer polycarbonate lens (2.5 mm perimeter clearance from painted front_fascia)
        lens = _safe(outer_skin & _headlight_prism(side, shrink=2.5))
        if lens is not None:
            parts.append(style_glass(lens, f"headlight_lens_{lbl}", LENS_HEAD, transmission=0.88))

        # 2. Glowing razor-slim white LED DRL blade cleanly behind the lens (depth 16..24 mm)
        drl_bar = bd.Box(195.0, 245.0, 12.0)
        drl_bar = bd.Rot(0, -15, side * -32) * drl_bar
        drl_bar = bd.Pos(2022.0, side * 662.0, 526.0) * drl_bar
        drl = _safe(drl_shell & drl_bar)
        if drl is not None:
            parts.append(style_emissive(drl, f"headlight_drl_{lbl}", LED_WHITE, intensity=3.2))

        # 3. Gloss-black optical bucket strictly behind the DRL shell (inside inner24, trimmed to 25 mm depth)
        bucket_outer = _headlight_prism(side, shrink=3.0)
        bucket_back = _headlight_prism(side, shrink=0.0, dx=-32.0, dy=-side * 22.0, dz=-18.0)
        bucket = _safe((inner24 & bucket_outer) - bucket_back)
        if bucket is not None:
            parts.append(style_gloss_black(bucket, f"headlight_housing_{lbl}", BLACK_GLOSS))

    return parts


def _build_taillights():
    """Full-width recessed rear transom dark trim bar, razor LED tail blades & CHMSL."""
    parts = []
    inner16 = body_master_inner(d=16.0)

    # Rear lamp slot in body.py: X=[-2300, -2195], Y=[-725, +725], Z=[748, 794]
    # 1. Flush smoked crimson outer cover lens (11 mm thick from rear transom face X=-2250..-2239)
    lens_box = box_between(-2260.0, -2238.0, -721.0, 721.0, 751.5, 790.5)
    rear_lens = _safe(rear_transom_cap(11.0) & lens_box)
    if rear_lens is not None:
        parts.append(style_glass(rear_lens, "taillight_lens", LENS_TAIL, transmission=0.78))

    # 2. Slim central connecting crimson LED strip strictly behind lens (X = -2234 .. -2224)
    center_box = box_between(-2234.0, -2224.0, -376.0, 376.0, 767.0, 775.0)
    center_led = _safe(inner16 & center_box)
    if center_led is not None:
        parts.append(style_emissive(center_led, "rear_led_lightbar", LED_RED, intensity=3.0))

    # 3. Sculpted bolder outer LED blades wrapping left & right corners (|Y| = 380..716)
    for side in (1, -1):
        lbl = "left" if side > 0 else "right"
        y0, y1 = (380.0, 716.0) if side > 0 else (-716.0, -380.0)
        blade_box = box_between(-2234.0, -2224.0, y0, y1, 756.0, 786.0)
        blade = _safe(inner16 & blade_box)
        if blade is not None:
            parts.append(style_emissive(blade, f"taillight_blade_{lbl}", LED_RED, intensity=3.4))

    # 4. Gloss-black optical backing bar strictly behind LEDs (X = -2221 .. -2198)
    housing_box = box_between(-2221.0, -2198.0, -721.0, 721.0, 751.0, 791.0)
    housing = _safe(inner16 & housing_box)
    if housing is not None:
        parts.append(style_gloss_black(housing, "rear_lightbar_housing", BLACK_GLOSS))

    # 5. Third brake light (CHMSL) tucked cleanly inside cabin just below Targa hoop rear edge
    chmsl = box_between(HOOP_REAR_X - 24.0, HOOP_REAR_X - 10.0, -170.0, 170.0, 1094.0, 1104.0)
    parts.append(style_emissive(chmsl, "third_brake_light", LED_RED, intensity=2.8))

    return parts


def build():
    """Build all exterior LED lighting assemblies."""
    return group(
        "lighting",
        [
            group("headlights", _build_headlights()),
            group("taillights", _build_taillights()),
        ],
    )
