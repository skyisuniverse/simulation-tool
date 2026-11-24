# Rougher as-printed surfaces

From [DMLS-Direct-Metal-Laser-Sintering.md](ideas/production/production-methodology/integrated-products/cnc-machines/processes/metal/DMLS/DMLS-Direct-Metal-Laser-Sintering.md)

> - **Limitations**: High equipment and operating costs, build-volume limits, thermal stress/warping risks, support structures needed for overhangs, and **rougher as-printed surfaces**.

From conversation with Gemini on [rougher as-printed surfaces](https://share.google/aimode/WY78PA2tIksUZ6API)

> What are rougher as-printed surfaces?

**Rougher as-printed surfaces** refer to the grainy, sand-cast-like texture (typically **Ra 6–15 µm**) that DMLS parts have straight out of the printer—significantly rougher than standard CNC-machined metal (typically **Ra 0.8–3.2 µm**).


## Why As-Printed DMLS Surfaces Are Rough

- **Partially melted powder particles**: Along the outer boundary of every laser scan, surrounding loose metal powder touches the hot melt pool and partially fuses ("sticks") to the outside wall without fully melting flat.
- **The "stair-stepping" effect**: Because parts are built from discrete flat layers (20–60 µm thick), curved or angled surfaces show tiny microscopic steps between each layer—most noticeable on shallow slopes.
- **Down-facing (overhang) surfaces**: Surfaces facing downward into loose powder conduct heat poorly, causing the melt pool to sag slightly and fuse extra powder underneath, making downward faces noticeably rougher than upward or vertical faces.
- **Laser scan tracks and spatter**: Tiny ripples along individual laser melt beads and microscopic droplets of molten spatter landing on the surface add minor texture.


## Why It Matters in Real Parts

- **Fatigue life**: Microscopic surface valleys act as tiny stress risers where cracks can initiate under repeated cyclic loads.
- **Fluid flow**: Rough internal channels create higher friction and pressure drop for liquids or gases flowing through them.
- **Mating and sealing**: Rough surfaces cannot form watertight O-ring seals or smooth sliding bearing fits without secondary finishing.


## How Engineers Smooth Them

- **Mechanical finishing**: Bead blasting, vibratory tumbling, or **CNC machining** for accessible external faces (bringing roughness down below **Ra 0.8 µm**).
- **Internal/complex finishing**: **Electropolishing**, **chemical etching**, or **abrasive flow machining (AFM)** — where abrasive paste is pumped through internal channels—to smooth areas tools cannot reach.

Would you like to look at **support structures and overhangs** next, or explore **how surface finishing methods compare** for internal versus external surfaces?
