# Heat treatment

From [DMLS-Direct-Metal-Laser-Sintering.md](ideas/production/production-methodology/integrated-products/cnc-machines/processes/metal/DMLS/DMLS-Direct-Metal-Laser-Sintering.md)

> - **Build and post-processing**: The platform lowers, another layer is applied, and the cycle repeats. Finished parts usually undergo **stress-relief heat treatment**, support removal, powder cleanup, and optional CNC machining or surface finishing.

From conversation with Gemini on [What is stress-relief heat treatment?](https://share.google/aimode/yZ1zebkMQ5zFkNozh)

- What is stress-relief heat treatment? 

**Stress-relief heat treatment** is a thermal post-processing step in which the printed metal parts—still welded to the build platform—are heated in a furnace to a controlled temperature below their melting point, held there, and slowly cooled to relax locked-in internal stresses created during laser printing.


## Why DMLS Parts Need It

- **Extreme thermal gradients**: During printing, the laser heats tiny spots of metal above 1,000 °C–3,000 °C in milliseconds while the surrounding metal stays much cooler.
- **Shrinkage tension**: As each newly melted layer cools and shrinks against the rigid solid metal underneath, massive **residual tensile and compressive stresses** get locked inside the part.
- **Preventing spring-back**: If you cut a part off the build plate *before* relieving those stresses, the part can immediately warp, twist, or crack as the trapped tension suddenly releases.

## How the Process Works

1. **Before plate removal**: The entire build plate (with parts and supports still attached) is placed inside a vacuum or inert-gas furnace (argon/nitrogen) to prevent oxidation.
2. **Controlled heating**: The furnace ramps up to an alloy-specific temperature (for example, roughly **600–650 °C for titanium Ti6Al4V**, **550–650 °C for stainless steel 316L**, or **300 °C for aluminum AlSi10Mg)**.
3. **Soaking**: The parts are held at that temperature for **1 to 4 hours**, allowing atoms in the metal crystal lattice to shift slightly and relieve microscopic strain without changing the part's overall shape.
4. **Slow cooling**: The parts are cooled gradually inside the furnace so new thermal stresses are not introduced.


## Additional Heat Treatments (Optional)

- **Solution annealing and aging**: Used on precipitation-hardening alloys (like Inconel 718, 17-4PH stainless steel, or aluminum) to maximize strength and hardness.
- **Hot Isostatic Pressing (HIP)**: Combines high heat with extreme inert-gas pressure to close tiny internal microscopic pores and maximize fatigue life for aerospace or medical implants.

Would you like to look at the next post-processing steps — 
- **support removal and Wire EDM**
- or explore **how designers reduce thermal stress during the CAD and slicing stage**?
