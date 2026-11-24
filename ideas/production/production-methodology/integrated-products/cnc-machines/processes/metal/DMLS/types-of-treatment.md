# Types of treatment

From [DMLS-Direct-Metal-Laser-Sintering.md](ideas/production/production-methodology/integrated-products/cnc-machines/processes/metal/DMLS/DMLS-Direct-Metal-Laser-Sintering.md)

From conversation with Gemini on [other types of treatment in DMLS](https://share.google/aimode/IaBttI1GMye89Kbxq)

> - **Build and post-processing**: The platform lowers, another layer is applied, and the cycle repeats. Finished parts usually undergo **stress-relief heat treatment**, support removal, powder cleanup, and optional CNC machining or surface finishing.

- Are there other types of treatment in DMLS?

Yes—beyond stress relief, DMLS parts routinely undergo several **thermal**, **mechanical**, and **chemical treatments** depending on the alloy and the performance or surface quality required.


## 1. Thermal Treatments (Microstructure & Density)

- **Hot Isostatic Pressing (HIP)**: Parts are placed in a high-pressure vessel filled with inert gas (usually argon) at high heat and intense pressure (often 100–200 MPa). This collapses microscopic internal pores and gas voids, boosting **fatigue strength and density** close to 100%—standard for aerospace and medical implants.
- **Solution Annealing**: Heating the part to a high temperature to dissolve alloying elements evenly into a uniform crystal structure, followed by rapid cooling (quenching). This erases the directional grain boundaries left by layer-by-layer printing and restores ductility.
- **Precipitation Hardening (Aging)**: A lower-temperature secondary heat cycle (often done after solution annealing) that forms microscopic strengthening precipitates inside alloys like Inconel 718, 17-4PH stainless steel, maraging steel, and AlSi10Mg to maximize hardness and yield strength.

## 2. Mechanical Surface Treatments

- **Media Blasting / Shot Peening**: Bombarding the part with glass beads, ceramic media, or metal shot to smooth the grainy as-printed texture and induce beneficial compressive surface stress, which helps prevent fatigue cracks.
- **Tumbling / Vibratory Finishing**: Placing parts in a vibrating tub with abrasive ceramic or plastic media to deburr edges and polish accessible external surfaces.
- **CNC Machining**: Precision milling, turning, or drilling of critical mating faces, bearing bores, and threads where as-printed tolerances are not tight enough.

## 3. Chemical & Electrochemical Treatments

- **Chemical Polishing / Etching**: Submerging parts in acid or alkaline baths to selectively dissolve surface roughness—especially useful for complex internal channels and lattice structures that mechanical tools cannot reach.
- **Electropolishing**: An electrochemical bath process that removes a thin microscopic outer layer of metal, leaving a bright, ultra-smooth, corrosion-resistant finish (common for medical devices and food/pharma hardware).


## 4. Protective & Functional Coatings

- **Anodizing (for Aluminum/Titanium)**: Electrochemically thickening the natural oxide layer to improve wear resistance, corrosion protection, or biocompatibility.
- **PVD / CVD / Plating**: Applying thin hard coatings (such as titanium nitride, chrome, or nickel) for extreme wear, low friction, or specific electrical/thermal properties.

Are you aiming for 

- a specific **material property** (like maximum fatigue life or hardness) 
- or a **surface finish requirement** (such as mirror-smooth external faces or clean internal fluid channels)?
