"""PBR material & colour helpers for the SpaceX Starship & Super Heavy Booster CAD assembly.

All material factories are functions (never module-level kernel/material singletons)
so importing this module stays lazy and lightweight.
Every factory uses untextured native `bd_materials` entries plus scalar PBR overrides
and an explicit sRGB hex colour set after `.material`, avoiding missing-texture warnings.
"""


def _apply(shape, mat, color_hex: str):
    shape.material = mat
    shape.color = color_hex
    return shape


def apply_stainless_304l(shape):
    """Bright brushed/rolled 304L stainless steel for Starship & Super Heavy tank skins."""
    from bd_materials import metals

    mat = metals.stainless()
    mat.pbr = mat.pbr.override(metalness=0.94, roughness=0.25, anisotropy=0.35)
    return _apply(shape, mat, "#D6DCE2")


def apply_stainless_structural(shape):
    """Slightly darker satin structural stainless steel for skirts, rings, flanges, and chines."""
    from bd_materials import metals

    mat = metals.stainless()
    mat.pbr = mat.pbr.override(metalness=0.88, roughness=0.38)
    return _apply(shape, mat, "#A4ACB5")


def apply_tps_ceramic(shape):
    """Matte charcoal-black silica ceramic Thermal Protection System (TPS) heat shield tiles."""
    from bd_materials import resins

    mat = resins.ceramic()
    mat.pbr = mat.pbr.override(metalness=0.05, roughness=0.82)
    return _apply(shape, mat, "#22252B")


def apply_grid_fin_steel(shape):
    """Dark heat-treated alloy steel for Super Heavy waffle grid fins & actuator hubs."""
    from bd_materials import metals

    mat = metals.alloy_steel()
    mat.pbr = mat.pbr.override(metalness=0.84, roughness=0.44)
    return _apply(shape, mat, "#464C54")


def apply_hot_stage_shield(shape):
    """Dark heat-tinted blast deflector & hot-stage ring interior alloy."""
    from bd_materials import metals

    mat = metals.alloy_steel()
    mat.pbr = mat.pbr.override(metalness=0.78, roughness=0.52)
    return _apply(shape, mat, "#363A42")


def apply_raptor_nozzle(shape):
    """Dark gunmetal superalloy for Raptor 2 regenerative bell nozzles."""
    from bd_materials import metals

    mat = metals.titanium()
    mat.pbr = mat.pbr.override(metalness=0.90, roughness=0.30)
    return _apply(shape, mat, "#525760")


def apply_raptor_copper(shape):
    """Heat-tinted bronze/copper-alloy accent for Raptor cooling manifolds and turbopump hardware."""
    from bd_materials import metals

    mat = metals.bronze()
    mat.pbr = mat.pbr.override(metalness=0.86, roughness=0.34)
    return _apply(shape, mat, "#916B4B")


def apply_dark_trim(shape):
    """Matte dark trim for raceways, QD panels, latch hardware, and RCS pods."""
    from bd_materials import plastics

    mat = plastics.peek()
    mat.pbr = mat.pbr.override(metalness=0.16, roughness=0.60)
    return _apply(shape, mat, "#2C3037")
