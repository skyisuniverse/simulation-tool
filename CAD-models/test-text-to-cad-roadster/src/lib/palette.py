"""Materials and colour palette for the Tesla Roadster (2nd generation).

Colours are sRGB hex strings. Native `bd_materials` materials provide physical
densities and PBR response (clearcoat paint, satin carbon fiber, forged alloy,
smoked automotive glass, and ultrawhite cockpit leather).
"""

from __future__ import annotations

import build123d as bd
from bd_materials import glass, metals, plastics, textile


# ---------------------------------------------------------------------------
# Signature Tesla Roadster Crimson Multi-Coat Red palette
# ---------------------------------------------------------------------------

PAINT_RED = "#C81022"          # Deep Tesla Roadster Crimson Red Multi-Coat
PAINT_RED_DARK = "#7A0A16"     # Recessed panel returns / shutline shadow
CARBON_SATIN = "#1D2126"       # Exposed carbon splitter, diffuser, aero trim
CARBON_GLOSS = "#252A30"       # Gloss carbon mirror caps / trim accents
CARBON_TUB = "#191C20"         # Structural monocoque & battery enclosure
BLACK_GLOSS = "#141619"        # Piano black window surrounds & A-pillar trim
TRIM_DARK = "#262B31"          # Wheel well liners, seals, intake mesh

ALLOY_SILVER = "#B8BFC7"       # Forged lightweight wheel spokes & Tesla T badge
ALLOY_DARK = "#4A5058"         # Wheel inner barrel, suspension uprights
TITANIUM = "#8A9098"           # Suspension links, aero stays, hub hardware
ROTOR_IRON = "#7E848C"         # Carbon-ceramic / ventilated brake rotor face
CALIPER_RED = "#D91626"        # Signature performance brake caliper

TYRE_RUBBER = "#17191C"        # Performance slick/tread rubber
TYRE_SIDEWALL = "#1E2125"      # Slightly lighter sidewall read

GLASS_TINT = "#4D5B6B"         # Smoked panoramic glass (mid tint for clean transmission)
GLASS_ROOF = "#404E5E"         # Slightly darker tinted removable Targa glass
GLASS_REAR = "#3B4755"         # Fastback rear glass
LENS_HEAD = "#6A7888"          # Clear/lightly smoked headlight cover lens
LENS_TAIL = "#7A1622"          # Smoked crimson taillight lens
LED_WHITE = "#EEF6FF"          # Razor LED headlight / DRL emitters
LED_RED = "#FF2233"            # Full-width LED tail light blades

INTERIOR_WHITE = "#E6E8EB"     # Iconic Roadster Ultrawhite seat bolsters & trim
INTERIOR_SUEDE = "#353A42"     # Dark charcoal Alcantara dash & seat inserts
INTERIOR_SHELL = "#1F2329"     # Carbon seat backs & center console base
SCREEN_GLASS = "#11161D"       # Floating curved center touchscreen
SCREEN_GLOW = "#2A6DA8"        # Subtle UI glow accent on center display


def _make_paint(hex_color, clearcoat=1.0, roughness=0.14):
    mat = metals.aluminum()
    mat.pbr = mat.pbr.override(
        metalness=0.35,
        roughness=roughness,
        clearcoat=clearcoat,
        clearcoat_roughness=0.06,
    )
    return mat, hex_color


def _make_carbon(hex_color, roughness=0.32, clearcoat=0.45):
    mat = plastics.cfrp()
    mat.pbr = mat.pbr.override(
        metalness=0.08,
        roughness=roughness,
        clearcoat=clearcoat,
        clearcoat_roughness=0.18,
    )
    return mat, hex_color


def _make_alloy(hex_color, roughness=0.22, metalness=0.92):
    mat = metals.aluminum()
    mat.pbr = mat.pbr.override(
        metalness=metalness,
        roughness=roughness,
    )
    return mat, hex_color


def _make_steel(hex_color, roughness=0.35):
    mat = metals.alloy_steel()
    mat.pbr = mat.pbr.override(
        metalness=0.85,
        roughness=roughness,
    )
    return mat, hex_color


def _make_rubber(hex_color, roughness=0.78):
    mat = plastics.rubber()
    mat.pbr = mat.pbr.override(
        metalness=0.0,
        roughness=roughness,
    )
    return mat, hex_color


def _make_glass(hex_color, transmission=0.82, roughness=0.04):
    mat = glass.soda_lime()
    mat.pbr = mat.pbr.override(
        metalness=0.0,
        roughness=roughness,
        transmission=transmission,
        ior=1.52,
        clearcoat=0.8,
        clearcoat_roughness=0.03,
    )
    return mat, hex_color


def _make_emissive(hex_color, intensity=2.5):
    mat = plastics.pmma()
    mat.pbr = mat.pbr.override(
        metalness=0.0,
        roughness=0.1,
        emissive=hex_color,
        emissive_intensity=intensity,
    )
    return mat, hex_color


def _make_leather(hex_color, roughness=0.58):
    mat = textile.leather()
    mat.pbr = mat.pbr.override(
        metalness=0.0,
        roughness=roughness,
    )
    return mat, hex_color


def _make_trim(hex_color, roughness=0.45):
    mat = plastics.abs_()
    mat.pbr = mat.pbr.override(
        metalness=0.05,
        roughness=roughness,
    )
    return mat, hex_color


def style_paint(shape, label, hex_color=PAINT_RED):
    shape.label = label
    mat, col = _make_paint(hex_color)
    shape.material = mat
    shape.color = col
    return shape


def style_carbon(shape, label, hex_color=CARBON_SATIN, gloss=False):
    shape.label = label
    mat, col = _make_carbon(
        hex_color,
        roughness=0.20 if gloss else 0.34,
        clearcoat=0.85 if gloss else 0.35,
    )
    shape.material = mat
    shape.color = col
    return shape


def style_gloss_black(shape, label, hex_color=BLACK_GLOSS):
    shape.label = label
    mat, col = _make_paint(hex_color, clearcoat=1.0, roughness=0.10)
    shape.material = mat
    shape.color = col
    return shape


def style_alloy(shape, label, hex_color=ALLOY_SILVER, roughness=0.20):
    shape.label = label
    mat, col = _make_alloy(hex_color, roughness=roughness)
    shape.material = mat
    shape.color = col
    return shape


def style_steel(shape, label, hex_color=ROTOR_IRON, roughness=0.32):
    shape.label = label
    mat, col = _make_steel(hex_color, roughness=roughness)
    shape.material = mat
    shape.color = col
    return shape


def style_caliper(shape, label, hex_color=CALIPER_RED):
    shape.label = label
    mat, col = _make_paint(hex_color, clearcoat=0.9, roughness=0.18)
    shape.material = mat
    shape.color = col
    return shape


def style_rubber(shape, label, hex_color=TYRE_RUBBER):
    shape.label = label
    mat, col = _make_rubber(hex_color)
    shape.material = mat
    shape.color = col
    return shape


def style_glass(shape, label, hex_color=GLASS_TINT, transmission=0.82):
    shape.label = label
    mat, col = _make_glass(hex_color, transmission=transmission)
    shape.material = mat
    shape.color = col
    return shape


def style_emissive(shape, label, hex_color=LED_WHITE, intensity=2.5):
    shape.label = label
    mat, col = _make_emissive(hex_color, intensity=intensity)
    shape.material = mat
    shape.color = col
    return shape


def style_leather(shape, label, hex_color=INTERIOR_WHITE, roughness=0.58):
    shape.label = label
    mat, col = _make_leather(hex_color, roughness=roughness)
    shape.material = mat
    shape.color = col
    return shape


def style_trim(shape, label, hex_color=TRIM_DARK, roughness=0.48):
    shape.label = label
    mat, col = _make_trim(hex_color, roughness=roughness)
    shape.material = mat
    shape.color = col
    return shape


def group(label, children):
    kids = [c for c in children if c is not None]
    if not kids:
        raise RuntimeError(f"group {label!r} has no children")
    return bd.Compound(children=kids, label=label)
