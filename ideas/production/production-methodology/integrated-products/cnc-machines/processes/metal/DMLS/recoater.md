# Recoater

From [DMLS-Direct-Metal-Laser-Sintering.md](ideas/production/production-methodology/integrated-products/cnc-machines/processes/metal/DMLS/DMLS-Direct-Metal-Laser-Sintering.md)

> - **Powder layering**: A **recoater** spreads a thin layer of metal powder (typically tens of micrometers thick) across a build platform.

---

From conversation with Gemini on [What is a recoater?](https://share.google/aimode/BALL2NDEzOCU013T7)

What is a recoater?

A **recoater** (also called a recoater blade or wiper) is the moving mechanical assembly in a powder bed fusion 3D printer that sweeps across the build area to spread a fresh, uniform, ultra-thin layer of metal powder before each laser scan.


## How It Works

- **Powder supply**: After a layer is fused, the build platform lowers by one layer thickness (usually 20–60 micrometers), while a powder feed piston rises—or a hopper drops a measured dose of fresh powder onto the bed.
- **Spreading and leveling**: The recoater travels horizontally across the build plate, pushing the mound of powder ahead of it to fill the lowered build area and scraping off any excess into an overflow bin.
- **Precision gap**: The bottom edge of the recoater sits at an exact, fixed height above the build plate so the deposited powder bed is flat and consistent in density.


## Common Types of Recoaters

- **Hard/rigid blades (tool steel or ceramic)**: Provide very high dimensional accuracy and flat layers, though they can jam or get damaged if a warped part sticks up above the powder bed.
- **Soft/flexible blades (silicone or rubber)**: Bend slightly if they hit a raised edge or spatter bump, reducing the risk of a print crash while sacrificing a tiny amount of surface flatness.
- **Brush recoaters (carbon fiber or metal bristles)**: Gently sweep powder across delicate or thin-walled parts without snagging on slightly curled edges.
- **Counter-rotating rollers**: Roll powder forward while compacting it slightly, improving powder bed density for certain powders and alloys.


## Why It Is Critical

- **Prevents voids**: Any streak, gap, or uneven spot left by a nicked or worn recoater blade translates directly into porosity or weak spots in the finished metal part.
- **Detects collisions**: Many DMLS machines monitor motor torque or optical sensors on the recoater to detect if a warped part collides with the blade, pausing the build before damage occurs.

Would you like to know more about
- **what causes a recoater crash** (such as thermal warping) and how to prevent it, 
- or **how the metal powder itself is produced and reused**?
