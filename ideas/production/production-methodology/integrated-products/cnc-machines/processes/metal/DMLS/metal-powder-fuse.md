# Metal powder fuse

From [DMLS-Direct-Metal-Laser-Sintering.md](ideas/production/production-methodology/integrated-products/cnc-machines/processes/metal/DMLS/DMLS-Direct-Metal-Laser-Sintering.md)

> **Direct Metal Laser Sintering (DMLS)** is a metal 3D printing (powder bed fusion) process that uses a high-powered laser to **fuse fine metal powder** layer by layer from a 3D CAD model inside an inert gas chamber.

From conversation with Gemini on [How is metal powder fused](https://share.google/aimode/0Utbm99e9RkbMcmnr)

> How is metal powder fused?

In DMLS, the metal powder is fused by **intense localized thermal energy from a focused laser beam**, which rapidly heats the particles until they melt or bond together into a solid mass, then quickly cools as the laser moves on.


## Step-by-Step Fusion Mechanism

- **Energy absorption**: A focused fiber laser (typically 200 W to 1,000+ W) strikes the top layer of metal powder, and the particles absorb that light energy as heat.
- **Melt pool formation**: In modern DMLS systems, the localized heat is high enough to fully melt the metal particles into a tiny, moving melt pool (around 100 micrometers wide) that wets and merges with the solid metal layer directly beneath it.
- **Solid-state sintering (historical/secondary effect)**: In earlier systems or multi-component alloys with different melting points, lower-melting constituents liquefied first and bound higher-melting particles together without fully melting everything—which is where the word "sintering" in DMLS comes from.
- **Rapid solidification**: As the laser scans away at high speed, surrounding metal and inert gas conduct heat out of the melt pool within milliseconds, freezing the molten metal into a dense, continuous solid track (called a scan track or bead).
- **Layer-to-layer bonding**: Each scan track overlaps adjacent tracks and penetrates slightly into the previously solidified layer underneath, creating a metallurgical bond across the entire part.


## Why the Inert Gas Matters

- **Prevents oxidation**: Molten metal reacts instantly with oxygen and nitrogen in air, forming brittle oxide films that prevent neighboring melt pools from wetting and fusing cleanly.
- **Clears fumes and spatter**: A steady flow of argon or nitrogen sweeps away vaporized metal plumes and tiny molten droplets (*spatter*) so they do not scatter the laser beam or create defects in the part.

Would you like to dive deeper into:

- **how laser parameters** (power, scan speed, hatch spacing) affect part density, 
- or **how DMLS compares to SLM and EBM**?



---

- What is the melting temperature of different materials (e.g. Stainless steel and tool steel, Aluminum alloys (such as AlSi10Mg), Titanium alloys (such as Ti6Al4V), Nickel superalloys (such as Inconel), cobalt-chrome, copper, and tungsten)?
- What are operating temperature ranges in DMLS printers?
- Does DMLS require specific safety measures like thermal (& other?) screening?
