"""Complete 1-story (1-floor) wooden shop for 1 person on a monolithic concrete slab foundation.

Root assembly composing five modular sub-models:
- foundation: monolithic thickened-edge concrete slab, entry step, EPDM sill membrane & post shoes
- framing: 2x6 structural timber stud walls, porch columns/braces, exposed king-post truss & rafters
- envelope: OSB sheathing, horizontal shiplap cedar siding, interior birch lining, standing-seam roof, gutters & sign
- openings: articulated glazed oak entrance door (RevoluteJoint) and four timber-framed windows
- interior: 1-person checkout counter with POS, stool, wall display shelving, window bench, rear storage & pendants
"""

import build123d as bd
from cad import model

from envelope import envelope
from foundation import foundation
from framing import framing
from interior import interior
from lib import spec as S
from openings import openings


@model
def wooden_shop():
    """Assembled 1-story 1-person wooden shop on a reinforced concrete foundation slab."""
    parts = [
        foundation().shape,
        framing().shape,
        envelope().shape,
        openings().shape,
        interior().shape,
    ]
    asm = bd.Compound(children=parts, label="wooden_shop")

    # Verify top-level architectural envelope bounds
    bb = asm.bounding_box()
    assert abs(bb.min.Z - 0.0) < 1e-3, f"Expected foundation base at Z=0, got {bb.min.Z}"
    assert bb.max.Z > 3940.0 and bb.max.Z < 4020.0, f"Unexpected roof ridge height: {bb.max.Z}"
    assert abs(bb.size.X - (2 * (S.ROOF_DECK_X + 100.0))) < 1e-2, f"Unexpected width across gutters: {bb.size.X}"
    return asm


if __name__ == "__main__":
    wooden_shop()
