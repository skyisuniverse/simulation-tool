"""Calibrated architectural materials with realistic densities and clean scalar PBR looks.

Every custom material uses explicit scalar PBR properties without unrendered bitmap texture maps,
keeping viewer/snapshot rendering clean and mass calculations physically accurate.
"""

from bd_materials import glass, metals, plastics, resins, wood
from cad.build123d import materials as cad_materials
from threejs_materials.library import PbrMaps, PbrProperties, PbrValues


def _hex_to_rgb(hex_color: str) -> list[float]:
    h = hex_color.lstrip("#")
    return [int(h[i : i + 2], 16) / 255.0 for i in (0, 2, 4)]


def _scalar_pbr(
    name: str,
    hex_color: str,
    *,
    roughness: float = 0.75,
    metalness: float = 0.0,
    emissive: str | None = None,
    emissive_intensity: float = 0.0,
) -> PbrProperties:
    kwargs = dict(
        color=_hex_to_rgb(hex_color),
        metalness=metalness,
        roughness=roughness,
    )
    if emissive is not None:
        kwargs["emissive"] = _hex_to_rgb(emissive)
        kwargs["emissive_intensity"] = emissive_intensity
    return PbrProperties(
        id=name,
        name=name,
        source="custom",
        url="",
        license="",
        values=PbrValues(**kwargs),
        maps=PbrMaps(),
    )


def apply_material(shape, mat, hex_color: str | None = None):
    """Assign material and optional explicit display color to a shape."""
    shape.material = mat
    if hex_color is not None:
        shape.color = hex_color
    return shape


# --- Concrete & Foundation ---

def concrete_slab():
    """Cast-in-place structural concrete (2400 kg/m^3, warm architectural grey)."""
    pbr = _scalar_pbr("concrete_slab", "#A8A6A1", roughness=0.90)
    return resins.custom_resin("concrete_c25", 2400.0, pbr=pbr)


def epdm_membrane():
    """Bitumen / EPDM damp-proof sill membrane (1200 kg/m^3, matte charcoal)."""
    pbr = _scalar_pbr("epdm_membrane", "#25272A", roughness=0.88)
    return plastics.custom_plastic("epdm_dpc", 1200.0, pbr=pbr)


# --- Structural & Architectural Woods ---

def framing_spruce():
    """Kiln-dried structural spruce-pine-fir framing lumber (510 kg/m^3)."""
    pbr = _scalar_pbr("framing_spruce", "#D7B482", roughness=0.76)
    return wood.custom_wood("spruce_c24", 510.0, family="softwood", pbr=pbr)


def heavy_timber():
    """Planed Douglas fir / glulam porch posts, beams & exposed truss (550 kg/m^3)."""
    pbr = _scalar_pbr("heavy_timber", "#BE8E58", roughness=0.68)
    return wood.custom_wood("douglas_fir_glulam", 550.0, family="softwood", pbr=pbr)


def osb_sheathing():
    """Structural OSB / plywood wall & roof sheathing (620 kg/m^3)."""
    pbr = _scalar_pbr("osb_sheathing", "#C7A36B", roughness=0.84)
    return wood.custom_wood("osb_sheathing", 620.0, family="engineered", pbr=pbr)


def cedar_siding():
    """Oiled western red cedar / larch exterior shiplap siding (480 kg/m^3)."""
    pbr = _scalar_pbr("cedar_siding", "#B47442", roughness=0.68)
    return wood.custom_wood("western_red_cedar", 480.0, family="softwood", pbr=pbr)


def walnut_trim():
    """Dark stained timber trim, fascia, corner boards & window frames (640 kg/m^3)."""
    pbr = _scalar_pbr("walnut_trim", "#4E3728", roughness=0.62)
    return wood.custom_wood("stained_timber_trim", 640.0, family="hardwood", pbr=pbr)


def birch_lining():
    """Light matte birch/pine interior tongue-and-groove wall lining (580 kg/m^3)."""
    pbr = _scalar_pbr("birch_lining", "#E5D3B3", roughness=0.68)
    return wood.custom_wood("birch_lining", 580.0, family="hardwood", pbr=pbr)


def oak_millwork():
    """Clear-oiled white oak for service countertop, shelves, door & stool (720 kg/m^3)."""
    pbr = _scalar_pbr("oak_millwork", "#C4955E", roughness=0.52)
    return wood.custom_wood("white_oak", 720.0, family="hardwood", pbr=pbr)


def sign_cream():
    """Painted timber fascia signboard face (580 kg/m^3, warm off-white)."""
    pbr = _scalar_pbr("sign_cream", "#EFE9DC", roughness=0.60)
    return wood.custom_wood("painted_signboard", 580.0, family="hardwood", pbr=pbr)


# --- Metals & Hardware ---

def standing_seam_steel():
    """Anthracite matte coated steel standing-seam roofing & gutters."""
    return cad_materials.powder_coat("#32383F", finish="matte", substrate=metals.mild_steel())


def galvanized_steel():
    """Hot-dip galvanized structural steel post shoes, anchors & thresholds."""
    return cad_materials.zinc_plated("clear", substrate=metals.mild_steel())


def brushed_brass():
    """Satin brushed brass for door handles, hinges, sign letters & pulls."""
    m = metals.brass()
    m.pbr = m.pbr.override(color=_hex_to_rgb("#C8A355"), roughness=0.32, metalness=0.90)
    return m


def matte_black_steel():
    """Matte black powder-coated steel for sconces, shelf brackets & POS stand."""
    return cad_materials.powder_coat("#22252A", finish="matte", substrate=metals.mild_steel())


# --- Glazing & Lighting ---

def architectural_glass():
    """Clear tempered architectural glazing with subtle cool tint."""
    m = glass.soda_lime()
    m.pbr = m.pbr.override(
        color=_hex_to_rgb("#DCEBF2"),
        roughness=0.05,
        transmission=1.0,
        opacity=0.32,
    )
    return m


def warm_lamp_globe():
    """Frosted warm-glow architectural luminaire diffuser."""
    pbr = _scalar_pbr(
        "warm_lamp_globe",
        "#FFF3D6",
        roughness=0.35,
        emissive="#FFD891",
        emissive_intensity=0.8,
    )
    return resins.custom_resin("frosted_lamp_glass", 2500.0, pbr=pbr)
