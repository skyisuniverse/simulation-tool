# Mechanical properties

From [DMLS-Direct-Metal-Laser-Sintering.md](ideas/production/production-methodology/integrated-products/cnc-machines/processes/metal/DMLS/DMLS-Direct-Metal-Laser-Sintering.md)

> - **Advantages**: Handles complex internal channels, lattices, and part consolidation; requires no molds; creates strong parts with near-wrought mechanical properties.

Conversation with Gemini on [near-wrought mechanical properties](https://share.google/aimode/6JUMkMfCWBRp3EwiF)

> What are near-wrought mechanical properties?

**Near-wrought mechanical properties** mean that a 3D-printed metal part achieves **strength, hardness, and density nearly equal to (and sometimes exceeding) traditionally forged, rolled, or machined bar stock ("wrought" metal)** — making it far stronger and denser than cast or conventionally sintered metal parts.


## What "Wrought" Means as a Benchmark

- **Wrought metal** (such as rolled plate, extruded bars, or forged billets used in CNC machining) has been mechanically worked under intense heat and pressure. This eliminates internal voids and refines the metal's crystal grain structure, setting the gold standard for **yield strength, ultimate tensile strength, and toughness**.
- **Cast metal**, by contrast, is poured molten into a mold and cools slowly, often leaving larger grain structures, shrinkage pores, and lower strength.
- **Near-wrought** means DMLS parts typically reach **99.5% to 99.9%+ relative density**, matching or slightly beating wrought static strength (tensile and yield strength), while coming close to wrought **ductility and fatigue life** after heat treatment.


## Why DMLS Achieves Near-Wrought Strength

- **Full localized melting**: Unlike older powder metallurgy that merely pressed and baked powder together (leaving 5–15% porosity), DMLS fully melts each overlapping laser track into the layer below, leaving virtually no gaps.
- **Ultra-fine microstructure**: Because the tiny laser melt pool cools within milliseconds, the metal freezes so fast that its crystal grains remain extremely fine. In metallurgy, finer grains directly increase yield strength and hardness (known as the **Hall–Petch effect**).


## The Catch: Where "Near" Differs from True Wrought

While static strength matches or exceeds wrought stock, raw DMLS parts differ in three ways unless properly post-processed:

- **Anisotropy (directional strength)**: Because parts are built layer by layer, strength and ductility along the vertical build direction (Z-axis) can be slightly lower than in the horizontal plane (X-Y), though heat treatment helps equalize this.
- **Lower as-printed ductility**: Rapid cooling makes raw DMLS parts harder and slightly more brittle than wrought metal until stress relief or annealing restores elongation.
- **Fatigue sensitivity**: Tiny microscopic pores (< 0.5%) or rough as-printed surfaces can act as crack starters under millions of cyclic loads—which is why critical aerospace parts undergo **Hot Isostatic Pressing (HIP)** and surface machining to match true wrought fatigue performance.

Would you like to 
- compare **DMLS mechanical properties against metal casting and CNC machining** side by side, 
- or look at **design rules for complex features** like internal channels and overhangs?

---

- How and why are those obtained (in non-DMLS)?
- How and why are those obtained (in DMLS)?
