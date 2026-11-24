# Optional CNC machining

From [DMLS-Direct-Metal-Laser-Sintering.md](ideas/production/production-methodology/integrated-products/cnc-machines/processes/metal/DMLS/DMLS-Direct-Metal-Laser-Sintering.md)

> - **Build and post-processing**: The platform lowers, another layer is applied, and the cycle repeats. Finished parts usually undergo stress-relief heat treatment, support removal, powder cleanup, and **optional CNC machining** or surface finishing.

From conversation with Gemini on [optional CNC machining](https://share.google/aimode/5UzY5yMw9lcNBld8r)

What is optional CNC machining in DMLS? 

**Optional CNC machining in DMLS** (often called **hybrid post-processing** or **finish machining**) is the subtractive machining of a 3D-printed metal part after printing to achieve tight dimensional tolerances, smooth mating surfaces, and precision features that laser powder bed fusion cannot produce on its own.

## Why DMLS Parts Need CNC Machining

- **Rough as-printed surfaces**: Freshly printed DMLS surfaces have a grainy, sand-cast-like texture (typically **Ra 6–15 µm**) caused by partially melted powder particles clinging to the outer edges.
- **Moderate dimensional tolerances**: Raw DMLS tolerances usually sit around **±0.1 mm to ±0.2 mm** (or ±0.2%), which is too loose for precision mechanical assemblies.
- **Support witness marks**: Where support structures are snapped or cut off, tiny bumps and scars remain that must be milled flat.


## What Gets Machined

Engineers rarely machine the entire part (which would defeat the purpose of 3D printing); instead, they selectively machine **critical functional interfaces**:

- **Flat mating faces and sealing flanges** (e.g., gasket surfaces or mounting pads)
- **Precision bores and bearing seats** (reamed or bored to tight concentricity and roundness)
- **Threaded holes and bosses** (drilled and tapped cleanly rather than printing fragile threads)
- **Datum reference surfaces** used to align the part in inspection fixtures or larger assemblies


## How Designers Prepare for It

- **Adding machining stock (allowance)**: In the 3D CAD model, designers add an extra **0.5 mm to 1.5 mm of sacrificial material** onto faces that will be CNC machined later, ensuring the cutting tool removes the rough outer skin down to clean, dense metal.
- **Designing fixturing features**: Because organic 3D-printed parts can have curved, hard-to-clamp shapes, designers often print temporary **sacrificial tabs, parallel clamping flats, or datum holes** onto the part so a CNC vise can grip it securely—and then mill those tabs off at the end.

Would you like to 
- look at **designing support structures and overhangs**, 
- or explore **how DMLS compares to full CNC machining** when deciding which process to use?

---

Why could there be a need for it, if it is possible to design the CAD model and print the physical object identical to it?
