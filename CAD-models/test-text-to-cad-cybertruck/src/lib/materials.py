"""Calibrated PBR materials for the production Tesla Cybertruck.

All bd_materials calls live inside factory functions so importing this module
does not load the OCCT kernel in the caller process.
"""

from __future__ import annotations


def stainless_30x():
    """30X cold-rolled stainless steel exoskeleton: bright raw metallic brushed silver."""
    from bd_materials import metals

    mat = metals.stainless()
    mat.pbr = mat.pbr.override(
        metalness=0.80,
        roughness=0.28,
        anisotropy=0.35,
    )
    return mat, "#d5dbe2"


def stainless_cant_rail():
    """Bright satin stainless finish for the slim roof cant rails."""
    from bd_materials import metals

    mat = metals.stainless()
    mat.pbr = mat.pbr.override(
        metalness=0.82,
        roughness=0.24,
        anisotropy=0.30,
    )
    return mat, "#dce2e8"


def matte_black_cladding():
    """Textured matte-black polypropylene for bumpers, trapezoidal fender flares, rockers, mirror housings."""
    from bd_materials import plastics

    mat = plastics.pp()
    mat.pbr = mat.pbr.override(
        metalness=0.04,
        roughness=0.78,
    )
    return mat, "#22252a"


def dark_charcoal_trim():
    """Deep satin charcoal for panel seam backing, tonneau slats, cowl grille, bed vault liner, wiper arm."""
    from bd_materials import plastics

    mat = plastics.abs_()
    mat.pbr = mat.pbr.override(
        metalness=0.08,
        roughness=0.58,
    )
    return mat, "#181b20"


def gloss_black_pillar():
    """Flush gloss-black B-pillar and C-pillar glasshouse appliques."""
    from bd_materials import plastics

    mat = plastics.pc()
    mat.pbr = mat.pbr.override(
        metalness=0.05,
        roughness=0.10,
        clearcoat=0.9,
        clearcoat_roughness=0.06,
    )
    return mat, "#111317"


def automotive_glass():
    """Sleek dark-smoked Tesla automotive glazing (subtle interior visibility without looking hollow)."""
    from bd_materials import glass

    mat = glass.soda_lime()
    mat.pbr = mat.pbr.override(
        metalness=0.04,
        roughness=0.04,
        ior=1.52,
        transmission=0.52,
        clearcoat=1.0,
        clearcoat_roughness=0.03,
        opacity=0.88,
    )
    return mat, "#1d232b"


def roof_glass():
    """Deep dark factory-tinted panoramic roof & rear cab privacy glass."""
    from bd_materials import glass

    mat = glass.soda_lime()
    mat.pbr = mat.pbr.override(
        metalness=0.05,
        roughness=0.04,
        ior=1.52,
        transmission=0.25,
        clearcoat=1.0,
        clearcoat_roughness=0.03,
        opacity=0.95,
    )
    return mat, "#14181f"


def mirror_glass():
    """Reflective silver automotive side mirror surface."""
    from bd_materials import metals

    mat = metals.silver()
    mat.pbr = mat.pbr.override(
        metalness=0.98,
        roughness=0.04,
    )
    return mat, "#dce3ea"


def tire_rubber():
    """All-terrain Goodyear Wrangler Territory RT matte vulcanized tire rubber."""
    from bd_materials import plastics

    mat = plastics.rubber()
    mat.pbr = mat.pbr.override(
        metalness=0.0,
        roughness=0.88,
    )
    return mat, "#1c1e21"


def aero_wheel_cover():
    """Satin dark gunmetal-graphite polymer for the 7-spoke Cybertruck aero wheel cover."""
    from bd_materials import plastics

    mat = plastics.abs_()
    mat.pbr = mat.pbr.override(
        metalness=0.22,
        roughness=0.38,
    )
    return mat, "#383e46"


def alloy_wheel_rim():
    """Dark gunmetal forged aluminum 20-inch wheel barrel."""
    from bd_materials import metals

    mat = metals.aluminum()
    mat.pbr = mat.pbr.override(
        metalness=0.82,
        roughness=0.32,
    )
    return mat, "#3c4148"


def brake_rotor_steel():
    """Machined cast iron / steel ventilated brake disc."""
    from bd_materials import metals

    mat = metals.mild_steel()
    mat.pbr = mat.pbr.override(
        metalness=0.88,
        roughness=0.28,
    )
    return mat, "#9aa2ab"


def brake_caliper():
    """Satin anodized charcoal-silver brake caliper."""
    from bd_materials import metals

    mat = metals.aluminum()
    mat.pbr = mat.pbr.override(
        metalness=0.55,
        roughness=0.38,
    )
    return mat, "#333840"


def drl_white_led():
    """Crisp bright-white full-width front LED DRL lightbar."""
    from bd_materials import plastics

    mat = plastics.pc()
    mat.pbr = mat.pbr.override(
        metalness=0.0,
        roughness=0.12,
        emissive=(0.96, 0.98, 1.0),
        emissive_intensity=2.4,
    )
    return mat, "#f2f8ff"


def headlight_projector():
    """Warm-white high-intensity lower projector headlamp lens."""
    from bd_materials import plastics

    mat = plastics.pc()
    mat.pbr = mat.pbr.override(
        metalness=0.05,
        roughness=0.08,
        emissive=(0.92, 0.96, 1.0),
        emissive_intensity=2.0,
    )
    return mat, "#e8f2ff"


def taillight_red_led():
    """Iconic crimson-red full-width rear LED lightbar & CHMSL."""
    from bd_materials import plastics

    mat = plastics.pc()
    mat.pbr = mat.pbr.override(
        metalness=0.0,
        roughness=0.14,
        emissive=(0.95, 0.08, 0.06),
        emissive_intensity=2.6,
    )
    return mat, "#e01a16"


def amber_marker_led():
    """Front amber side-marker lamp."""
    from bd_materials import plastics

    mat = plastics.pc()
    mat.pbr = mat.pbr.override(
        metalness=0.0,
        roughness=0.18,
        emissive=(0.95, 0.45, 0.04),
        emissive_intensity=1.6,
    )
    return mat, "#f08214"


def underbody_skid_metal():
    """Heavy-duty satin dark-grey structural aluminum / steel underbody armor."""
    from bd_materials import metals

    mat = metals.aluminum()
    mat.pbr = mat.pbr.override(
        metalness=0.65,
        roughness=0.52,
    )
    return mat, "#383d44"


def interior_charcoal():
    """Cybertruck minimalist charcoal vegan-leather & composite interior."""
    from bd_materials import textile

    mat = textile.leather()
    mat.pbr = mat.pbr.override(
        metalness=0.02,
        roughness=0.72,
    )
    return mat, "#282c32"


def interior_white_accent():
    """Cybertruck signature light-grey / tactical white dashboard & seat trim accent."""
    from bd_materials import plastics

    mat = plastics.abs_()
    mat.pbr = mat.pbr.override(
        metalness=0.02,
        roughness=0.55,
    )
    return mat, "#d4d8dd"


def touchscreen_glow():
    """Central 18.5-inch floating Cybertruck infotainment display."""
    from bd_materials import plastics

    mat = plastics.pc()
    mat.pbr = mat.pbr.override(
        metalness=0.05,
        roughness=0.08,
        emissive=(0.18, 0.24, 0.32),
        emissive_intensity=0.8,
    )
    return mat, "#2a384a"


def apply_mat(shape, factory, label: str):
    """Assign label, material, and explicit hex color in the required order."""
    mat, hex_color = factory()
    shape.label = label
    shape.material = mat
    shape.color = hex_color
    return shape
