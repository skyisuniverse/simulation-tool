# Powder cleanup

From [DMLS-Direct-Metal-Laser-Sintering.md](ideas/production/production-methodology/integrated-products/cnc-machines/processes/metal/DMLS/DMLS-Direct-Metal-Laser-Sintering.md)

> - **Build and post-processing**: The platform lowers, another layer is applied, and the cycle repeats. Finished parts usually undergo stress-relief heat treatment, support removal, **powder cleanup**, and optional CNC machining or surface finishing.

From conversation with Gemini on [powder cleanup](https://share.google/aimode/ClLqCfzf9dISB2r3c)

> What is powder cleanup?

**Powder cleanup** (also called **depowdering** or **powder removal**) is the post-processing step where all loose, unmelted metal powder is removed from around and inside the finished parts after the laser finishes printing.

- **Initial chamber excavation**: Once the build cools down inside the inert chamber, an operator uses an **explosion-proof (ATEX/NFPA-rated) vacuum** and soft brushes to remove the surrounding cake of loose metal powder from the build plate so the printed parts are exposed.
- **Trapped-powder evacuation**: Because DMLS parts often feature narrow internal cooling channels, hollow cavities, or dense lattice structures, unmelted powder gets tightly packed inside. Operators clear these areas using:
	- **Compressed inert gas or air jets** (inside a sealed glovebox or extraction booth)
	- **Ultrasonic vibration tables** that shake trapped powder loose from winding internal passages
	- **Automated depowdering stations** that rotate and vibrate the entire build plate while blasting air through internal ports


## Why It Is Critical

- **Before heat treatment**: Any loose powder left inside narrow channels during stress-relief heat treatment can partially sinter into a solid plug, permanently blocking internal fluid paths.
- **Safety and contamination**: Metal dust is hazardous to breathe and combustible if dispersed in the air, so cleanup must happen inside enclosed, grounded ventilation hoods with operators wearing respirators and protective gear.
- **Powder recovery**: The vacuumed loose powder is collected, passed through a vibratory sieve to filter out melted spatter clumps, and blended back into fresh powder for future prints—keeping material waste low.

## Design Rule for Easy Cleanup

- **Escape holes (drain holes)**: Whenever a part contains a hollow cavity or enclosed lattice, designers must include at least **two escape holes** (typically **3–5 mm or wider**) so powder can flow out while air flows in—otherwise, trapped powder remains sealed inside the part forever.

Would you like to
- look at **support removal** next, 
- or explore **how designers plan escape holes and internal channels** to prevent trapped powder?

---

How is it performed?
