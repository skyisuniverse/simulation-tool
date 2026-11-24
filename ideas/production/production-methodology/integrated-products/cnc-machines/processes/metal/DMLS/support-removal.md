# Support removal

From [DMLS-Direct-Metal-Laser-Sintering.md](ideas/production/production-methodology/integrated-products/cnc-machines/processes/metal/DMLS/DMLS-Direct-Metal-Laser-Sintering.md)

> - **Build and post-processing**: The platform lowers, another layer is applied, and the cycle repeats. Finished parts usually undergo stress-relief heat treatment, **support removal**, powder cleanup, and optional CNC machining or surface finishing.

What is support in DMLS?

What is support removal?

From conversation with Gemini on [support removal](https://share.google/aimode/cdRBWEcgCHHM9hAyI)

**Support removal in DMLS** is the mechanical or machining process of cutting, snapping, or grinding away the temporary metal scaffolding structures that anchored the part to the build plate and held up overhanging features during printing.

## Why Metal Supports Are Harder to Remove

Unlike plastic 3D printing where supports snap off easily by hand, DMLS supports are **solid metal welded directly into both the part and the build plate**. Because they conduct heat and resist warping during printing, they must be strong enough to hold down tons of thermal stress—making them tough to remove afterward.


## The Two-Stage Removal Process

### 1. Separating the Part from the Build Plate

Before individual supports are removed, the entire part (and its base supports) must be detached from the thick metal build platform—always **after** stress-relief heat treatment so the part does not warp:

- **Wire EDM (Electrical Discharge Machining)**: The gold standard for accuracy. An electrically charged thin brass wire slices cleanly through the bottom of the supports with zero mechanical force, leaving a flat cut without bending delicate parts.
- **Bandsaw**: A faster, cheaper option for robust parts with thick base supports, though less precise and prone to vibration on thin features.


### 2. Removing Supports from the Part Itself

Once off the plate, technicians remove the remaining support material from overhangs, bridges, and downward-facing surfaces:

- **Manual hand tools**: Pliers, chisels, pneumatic hammers, and rotary Dremel/die grinders are used to break away thin, perforated "breakaway" supports on accessible outer surfaces.
- **CNC milling or turning**: Thick, heavy-duty block or tree supports—often used on high-stress alloys like titanium or Inconel—are machined off cleanly using a CNC mill.
- **Bead blasting and grinding**: After the bulk support is gone, technicians grind or sand down the tiny remaining bumps (*witness marks*) so the surface is smooth.

## Key Design Challenges

- **Line-of-sight access**: If supports are placed inside a closed internal cavity or deep, winding channel where a saw, wire, pliers, or mill cannot reach, they can **never be removed**.
- **Overhang rules**: Designers orient parts at angles (typically keeping downward faces steeper than **45°** from horizontal) to minimize where supports are needed in the first place.

Would you like to dive into 
- **DMLS design rules for overhangs and supports**, 
- or explore **how support structures are generated** (such as block, tree, and cone supports)?
