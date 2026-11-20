# Wooden Shop. Conversations

## Part 1

From conversation with Gemini on a [CNC-machine for wooden shop assembly](https://share.google/aimode/AOzOD1i57vf7z3h7j)

> Consider a CNC-machine that would be capable of assembling a 1-story wooden shop building for 1 person, comfortable for working with wood, metal, etc. inside. Including all necessary operations with wood like cutting (boards, sheets, etc), stapling, painting, assembling (frames, floor, walls, roof). Could it be possible?

**Yes, it is technically possible**, and industrial versions of these systems already build full-scale wooden buildings today. However, doing every single step inside one single machine—rather than a modular factory line—comes with major engineering and economic trade-offs.

### How It Already Exists in Industry

In modern prefabricated timber construction, your exact workflow is handled by **CNC multifunction bridges** (such as [WEINMANN WALLTEQ](https://www.homag.com/en/machines/house-construction/multifunction-bridge) or [Randek AutoWall](https://www.randek.com/systems/autowall)) and **gantry-mounted robotic cells** (like those developed at [ETH Zurich](https://parametrichouse.com/robotic-prefabrication/)):

- **Cutting and milling**. A CNC joinery saw or router cuts dimensional lumber to length, mills mortise-and-tenon joints, and cuts window and door openings out of sheet goods like OSB or plywood.

- **Fastening and stapling**. Automated tool heads shoot nails, staples, or screws to join studs to top/bottom plates and fasten sheathing onto the frame.

- **Assembling 3D structures**. Multi-axis robotic arms with vacuum grippers and pneumatic clamps pick up individual boards, hold them in 3D space while fastening, and flip completed wall, floor, and roof panels.

- **Surface finishing**. Industrial spray-painting robots or gantry-mounted paint heads can prime and paint exterior siding or interior panels before assembly.

### Why One All-in-One Machine Is Difficult

Combining every step into a single, compact machine rather than separate stations creates four practical bottlenecks:

- **Workspace scale**. A comfortable 1-person wood and metal shop needs roughly 4 × 6 meters (about 13 × 20 feet) of floor space with high ceilings. A single gantry machine capable of enclosing and assembling the entire structure in place would have to be larger than the building itself, making it far more practical to build flat wall, floor, and roof panels and join them afterward.
- **Paint contamination**. Spraying paint or primer inside the same machine that cuts and routes wood creates a severe fire and quality hazard. Fine sawdust ruins wet paint finishes, and overspray gums up linear rails, ball screws, and optical sensors.
- **Wood imperfection**. Unlike metal, framing lumber warps, bows, and twists. Automated framing systems require heavy servo-controlled clamping tables and machine-vision sensors to straighten boards before nailing—adding massive mechanical complexity to an all-in-one unit.
- **Cost vs. output**. A multi-axis robotic cell with automatic tool changers (saw, router, nailer, stapler, vacuum gripper, paint sprayer) costs hundreds of thousands of dollars—economical for a factory producing dozens of buildings a year, but vastly more expensive than building a single workshop manually or buying flat-packed CNC-cut kits.

### The Most Realistic Approach Today

If you want to build a 1-person workshop using CNC automation without owning a massive factory:

- **CNC-cut interlocking kits (WikiHouse style)**. A standard 4×8-foot (1.2 × 2.4 m) CNC router cuts interlocking plywood ribs, floor cassettes, and roof beams from sheet material. You assemble the numbered pieces by hand with a mallet and screws in a few days.

- **Two-station microfactory**. Keep cutting/fastening on a gantry table and separate painting/finishing into a ventilated booth or outdoor step, then bolt the finished wall, floor, and roof cassettes together on your foundation.

Are you exploring this as a **theoretical engineering concept**, or are you looking to **design/build a real workshop** using CNC tools? If you share your **target building dimensions** or **available budget**, I can outline the most practical setup.

---

## Part 2

From conversation with Gemini on a [CNC-machine for wooden shop assembly (part 2)](https://share.google/aimode/AOzOD1i57vf7z3h7j)

> CNC-machines can be assembled with cheap tools that are affordable (for example - CNC-machines with plasma cutters for 250$, that are assembled with component like those from mcmaster, that cut metal. Wood is much cheaper to operate then metal - if metal was possible, then wood should be also. 
>
> Describe (within the initial idea), how could the CNC-machine, that could assemble the entire wooden shop entirely automatically be possible? (consider open-source libraries and affordable tooling)

**Yes—a DIY, open-source CNC builder is possible if you solve the problem modularly**, using a large-format cable or track gantry (like Maslow CNC or LowRider CNC) equipped with a quick-change tool head to build and stack interlocking wall, floor, and roof cassettes on-site.

While a $250 plasma cutter only needs to move a lightweight torch over a flat sheet of metal, building a 3D wooden shop requires picking, clamping, fastening, and lifting heavy timber—which means the real engineering challenge is mechanical handling and lumber warping rather than cutting power.


### 1. The Low-Cost Frame & Motion Architecture

Instead of a massive, rigid steel bridge, you can scale up proven open-source DIY CNC mechanics using off-the-shelf hardware (extruded aluminum, EMT conduit, stepper motors, and belts/cables):

- **Track-mounted gantry (LowRider / MPCNC style)**: Mount Y-axis rails directly onto a temporary, level plywood worktable (e.g., 1.5 × 3.5 meters) built on-site. The gantry rolls along the table to process full 4×8-foot (1.22 × 2.44 m) plywood sheets and standard 3-meter framing studs.
- **Cable-suspended vertical frame (Maslow CNC style)**: Lean a near-vertical frame against a wall and suspend the tool sled from two top corner motors. This slashes footprint and cost, though it is limited to flat sheet cutting rather than 3D stud framing.
- **Control electronics**: Run open-source **GRBL / FluidNC** or **LinuxCNC** on a $30 microcontroller or Raspberry Pi. With custom G-code macros (`M6` tool changes and `M3/M5` relay triggers), the controller can fire pneumatic tools, steppers, and pumps in sequence.


### 2. Modular Quick-Change Tool Heads

To keep the gantry light and affordable, use a kinematic magnetic or pneumatic coupling so the carriage swaps between four cheap, off-the-shelf tools:

1. **Cutting & Milling**: A standard trim router ($80–$150) with a compression spiral bit cuts interlocking puzzle joints, mortises, and window openings out of plywood/OSB.
2. **Fastening (Stapling / Nailing)**: A $50 pneumatic framing nailer or narrow-crown stapler mounted to a solenoid valve and a short Z-axis pneumatic cylinder. When triggered via G-code, the cylinder presses the safety nose down and fires a fastener.
3. **Pick-and-Place Gripper**: A $40 DIY vacuum suction cup (powered by a salvaged shop-vac or venturi generator) paired with a simple servo-actuated parallel jaw gripper to lift cut plywood sheets and place precut studs into position.
4. **Painting / Sealing**: An airless paint sprayer gun ($100) triggered by a linear servo. To prevent sawdust from ruining the paint or gumming up rails, the machine must run **dry cutting/assembly batches first**, blow off the worktable with compressed air, and run a **dedicated painting pass last** (or use pre-primed sheets).

### 3. Designing the Building for the Machine

Because a cheap DIY gantry lacks the brute force to straighten twisted 2×4 lumber, **the building design must do the heavy lifting**:

- **All-sheet construction (WikiHouse / CNC box-beam approach)**: Avoid dimensional lumber entirely. Cut everything—studs, joists, rafters, and sheathing—from CNC-routed plywood or OSB sheets with interlocking tab-and-slot joints. Sheet goods are flat, predictable, and easy for a vacuum gripper to handle.

- **On-table cassette assembly**: The machine builds one hollow wall, floor, or roof cassette at a time flat on the worktable:
	1. Cuts the interior skin and internal ribs from stacked sheets.
	2. Uses the vacuum gripper to place the ribs into the slots of the bottom skin.
	3. Fires staples/nails along the joints.
	4. Places and staples the top skin, then sprays exterior primer/paint.

- **Final erection (the hard part)**: Once the machine finishes all cassettes, a simple **A-frame hoist with a cheap electric winch** (or manual tilt-up with a helper) lifts the lightweight panels upright onto the foundation, where they bolt together.


## Key Bottlenecks You Still Have to Solve

- **Material feeding**: Someone—or a secondary roller feeder—still has to load raw 4×8 sheets onto the worktable and clear finished panels off.
- **Z-axis height**: Framing a 15–20 cm thick wall cassette requires at least 25–30 cm of Z-axis clearance, which introduces flex in cheap conduit/extrusion gantries unless you use dual-side drive motors and rigid linear rails (like HGR20).

Would you like to dive deeper into any specific part of this setup, such as:

- **Open-source firmware & G-code automation** (configuring FluidNC/LinuxCNC to fire pneumatic nailers and paint sprayers)
- **Mechanical BOM & gantry design** (scaling a LowRider-style gantry for thick wall cassettes)
- **Parametric WikiHouse-style CAD libraries** for generating interlocking shop panels?
