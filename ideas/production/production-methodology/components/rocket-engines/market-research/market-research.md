# Rocket engines manufacturing. Market Research

## Part 1. SpaceX

From conversation with Gemini on [how does SpaceX produce Raptor 3 engines](https://share.google/aimode/MOVDnsNELv2BO1muO)

> how does SpaceX produce Raptor 3 engines? is it DMLS (Direct Metal Laser Sintering) ?

**Yes, SpaceX relies heavily on DMLS (Direct Metal Laser Sintering)—more broadly referred to in aerospace as Laser Powder Bed Fusion (PBF-LB)—as the core technology for producing Raptor 3 engines**. However, the engine is not printed as one single solid block; rather, **it is produced through a hybrid pipeline that combines additive manufacturing, specialized metallurgy, precision machining, and robotic welding**.

### 1. Metal 3D Printing (DMLS / PBF-LB)

SpaceX uses industrial-scale laser powder bed fusion systems (including licensed technology from [Velo3D](https://www.velo3d.com/)) to build complex, monolithic engine parts layer by layer from powdered metal.

- **Part consolidation**. Instead of casting, machining, and bolting together hundreds of separate pipes, valves, and manifolds, SpaceX prints entire sub-assemblies as single continuous pieces.

- **Internalized routing**. For Raptor 3, engineers moved external secondary flow paths and plumbing inside the solid metal walls of the engine. This eliminated bolted flanges and external piping, which reduced leak points and allowed SpaceX to completely remove the engine's external heat shield and fire-suppression system.

- **Regenerative cooling channels**. DMLS allows SpaceX to print intricate, microscopic cooling channels directly into the combustion chamber walls and exposed components. Cold liquid methane flows through these internal channels to keep the engine from melting under extreme temperatures.


### 2. Specialized Superalloys

Because Raptor 3 operates at extreme chamber pressures (~300+ bar) in an oxygen-rich, high-temperature environment, standard metals would quickly degrade or ignite. SpaceX prints different sections of the engine using specialized alloys:

- **SX500**. A proprietary nickel-based superalloy developed by SpaceX to withstand hot, oxygen-rich gas without oxidizing or cracking.
- **GRCop-42**. A high-conductivity copper-chromium-niobium alloy printed for the main combustion chamber liner to rapidly transfer heat into the regenerative cooling channels.

### 3. Post-Processing, Machining, and Welding

Once components come out of the 3D printers, they go through a traditional industrial finishing line (which SpaceX calls "The Bakery" due to the massive heat-treating ovens):

- **Hot Isostatic Pressing (HIP) & heat treatment**. Printed parts are subjected to extreme heat and inert gas pressure to eliminate microscopic internal voids, ensuring near-100% density and high structural integrity.
- **CNC machining**. High-precision computer-controlled milling machines refine mating surfaces, injector holes, and tolerances to exact dimensions.
- **Robotic welding**. While bolted flanges were largely eliminated on Raptor 3, major printed sub-assemblies (such as the turbopumps, main combustion chamber, and nozzle) are permanently joined together using automated robotic welding.
- **Testing**. Every completed engine is shipped to SpaceX's facility in McGregor, Texas, for a full-duration static fire test before being cleared for flight.

If you'd like to dive deeper, I can explain:

- The **specific design upgrades** that separate Raptor 3 from Raptor 2 (such as thrust, mass, and hydrostatic bearings)
- How **Velo3D's support-free printing** works for complex internal rocket geometry
- The **full-flow staged combustion cycle** that Raptor 3 uses to generate power

Let me know which area you'd like to explore!

---

## Part 2. RocketLab

From conversation with Gemini on [how does RocketLab produce their rocket engines](https://share.google/aimode/P4LJs0wYWOGYSJxud)

> how does RocketLab produce their rocket engines? is it DMLS (Direct Metal Laser Sintering) ?

**No, Rocket Lab primarily uses Electron Beam Melting (EBM) and Laser Powder Bed Fusion (LPBF/SLM) rather than DMLS**, though all of these belong to the same broader powder-bed fusion family of metal 3D printing.

At their Engine Development Complex in Long Beach, California, Rocket Lab 3D prints the vast majority of its engine hardware in-house—including

- thrust chambers, 
- injectors, 
- turbopump housings, 
- and propellant valves—using proprietary metal alloys and powders.

### 3D Printing Technologies Used

- **Electron Beam Melting (EBM)**. Rocket Lab famously pioneered orbital-class 3D-printed engines using EBM (specifically Arcam systems) for the **Rutherford** engine (which powers the Electron rocket) and the **Curie** kick-stage engine. Instead of a laser, EBM uses a high-powered electron beam inside a vacuum chamber to fully melt titanium and Inconel powders layer by layer. Printing in a vacuum prevents oxidation and reduces residual thermal stress in the metal.

- **Laser Powder Bed Fusion (LPBF / SLM)**. Alongside EBM, Rocket Lab uses laser-based powder bed fusion (often referred to as Selective Laser Melting, or SLM) for intricate components and newer engines like **Archimedes** (which powers the larger Neutron rocket). While technically very similar to DMLS—both use lasers to fuse metal powder—LPBF/SLM **fully melts** the metal powder into a solid, homogeneous part, whereas DMLS traditionally **sinters** (fuses without fully liquefying) the particles.

### How Rocket Lab Manufactures an Engine

- **Design for Additive Manufacturing**. Engineers combine dozens of traditionally separate parts into single, complex geometries. For example, regenerative cooling channels are printed directly inside the walls of the combustion chamber, eliminating the need for manual welding or brazing.

- **Multi-Material Construction**. For high-stress engines like the reusable Archimedes, Rocket Lab prints the inner thrust chamber out of a copper alloy for superior heat transfer, then clads it in a high-strength superalloy.

- **Rapid Production Speed**. Traditional rocket engines can take months to machine and assemble. By printing components from CAD files, Rocket Lab can print primary Rutherford components in about 24 hours and build a complete, much larger Archimedes engine in roughly 8 to 11 days.

- **Post-Processing and Assembly**. Once printed, excess powder is vacuumed out, temporary support structures are removed, and parts undergo precision CNC machining on mating surfaces, heat treatment, and inspection before being assembled with non-printed parts (like electric motors, batteries, and standard fasteners).

- **Testing and Qualification**. Completed Rutherford engines are hot-fired in dedicated test cells, while the larger Archimedes engines are shipped to Rocket Lab's test stand at [NASA's Stennis Space Center](https://rocketlabcorp.com/updates/rocket-lab-completes-archimedes-engine-build-begins-engine-test-campaign/) in Mississippi for full-duration acceptance testing.

Would you like to dive deeper into a specific aspect, such as:

- The **electric turbopump design** on the Rutherford engine
- How the **Archimedes staged-combustion cycle** differs from Rutherford
- The **post-processing steps** (like Hot Isostatic Pressing and CNC finishing) used on 3D-printed aerospace parts

---

## Part 3. Artemis

From conversation with Gemini on [how does Artemis produce their rocket engines](https://share.google/aimode/QfwElOJcHOnXeFqaz)

> how does Artemis produce their rocket engines? is it Laser Powder Bed Fusion (PBF-LB)?

**Yes, Laser Powder Bed Fusion (PBF-LB) is heavily used to produce components for NASA's Artemis rocket engines, though it is combined with traditional manufacturing and other 3D-printing methods**.

The core stage of the Space Launch System (SLS) is powered by four **RS-25 engines** built by [L3Harris (Aerojet Rocketdyne)](https://www.l3harris.com/all-capabilities/rs-25-engine). Because PBF-LB build chambers have size limits, the entire engine isn't printed in one piece; instead, manufacturing splits into distinct processes based on component size and function:

### 1. Laser Powder Bed Fusion (PBF-LB)

PBF-LB is the primary additive manufacturing method used for complex, high-precision internal engine parts.

- **Key components**. Engineers use PBF-LB to fabricate intricate parts like the **pogo accumulator** (which acts as a shock absorber to prevent fuel pressure oscillations), injector assemblies, valves, and ducts.
- **Specialized alloys**. NASA developed custom superalloys specifically for PBF-LB in liquid-hydrogen engines, such as **GRCop-42** (a high-conductivity copper alloy for combustion chambers) and **NASA HR-2** (an iron-nickel superalloy resistant to hydrogen embrittlement).
- **Impact**. Switching these sub-assemblies to PBF-LB allowed engineers to consolidate multi-piece designs into single printed parts, eliminating over 700 welds and reducing per-engine production costs by roughly 30% for flights starting with Artemis V.

### 2. Blown Powder Directed Energy Deposition (DED)

For massive parts that exceed the bed size of PBF-LB printers, NASA’s Rapid Analysis and Manufacturing Propulsion Technology (RAMPT) project utilizes **Blown Powder DED**.

- **How it works**. Instead of a stationary powder bed, a robotic arm feeds metal powder directly into a laser-heated molten pool.
- **Key components**. This process builds large-scale structures like **regeneratively cooled engine nozzles** with complex internal cooling channels—cutting fabrication times from nearly a year down to about 30 days.

### 3. Traditional Manufacturing & Mission Phasing

- **Artemis I through IV**. These flights rely on 16 heritage RS-25 engines refurbished from the Space Shuttle program. While these legacy engines were originally built using traditional forging, CNC machining, and hand-welding, they have been upgraded with PBF-LB components (like the 3D-printed pogo accumulators) and modern digital controllers.

- **Artemis V and beyond**. L3Harris restarted RS-25 production with a re-engineered design that integrates PBF-LB, Hot Isostatic Pressing (HIP) for bonding, and automated welding to build brand-new engines from scratch.

*(Note: Other propulsion systems on the Artemis stack—such as the upper-stage *RL10 engine* and Northrop Grumman’s **Solid Rocket Boosters**—also incorporate PBF-LB parts for injectors and valves alongside traditional composite winding and casting.)*

Would you like to dive deeper into:

- The **post-processing steps** required for aerospace PBF-LB parts (like Hot Isostatic Pressing and heat treatment)
- The **material science** behind NASA's custom printing alloys (GRCop-42 and HR-2)
- How **commercial Artemis landers** (like SpaceX's Raptor or Blue Origin's BE-7) compare in their additive manufacturing approaches?

---

## Part 3. FireFly

From conversation with Gemini on [how does FireFly produce their rocket engines](https://share.google/aimode/oGwBhRgglFrXXlyWu)

> how does FireFly produce their rocket engines? is it Laser Powder Bed Fusion (PBF-LB)?

**Yes, Firefly Aerospace relies heavily on metal additive manufacturing (3D printing)—specifically Laser Powder Bed Fusion (PBF-LB)—combined with precision post-processing and conventional machining to produce its rocket engines**.

Rather than relying on a single method, Firefly uses a hybrid, vertically integrated approach at its "Rocket Ranch" facility in Briggs, Texas, tailored to each engine's architecture.

### 1. Metal Additive Manufacturing (PBF-LB)

- **Complex Engine Components**. Firefly uses metal 3D printing to produce intricate internal engine hardware—such as injectors, combustion chambers, and turbopump manifolds—that would be impossible or too expensive to cast or machine traditionally. PBF-LB (also referred to as Selective Laser Melting) is the aerospace industry standard for these high-precision propulsion parts, fusing fine metal superalloy or copper powders layer-by-layer to build regenerative cooling channels directly into the hardware.
- **Part Count Reduction**. By printing consolidated components for its **Reaver**, **Lightning**, and newer **Miranda** and **Vira** engines, Firefly drastically reduces welds, brazes, and potential leak points. Firefly originally partnered with Aerojet Rocketdyne to accelerate its additive manufacturing capabilities for the Reaver engine and has since scaled those processes in-house.

### 2. Specialized Post-Processing

- **Abrasive Flow Machining (AFM)**. Because PBF-LB leaves a rough, granular surface finish inside small internal cooling channels and propellant passages, Firefly works with finishing partners (such as Extrude Hone) to run abrasive media through the printed parts, smoothing internal walls to ensure predictable fluid dynamics.

- **CNC Machining & Heat Treatment**. Printed engine components undergo thermal stress relief, Hot Isostatic Pressing (HIP) to remove internal porosity, and traditional multi-axis CNC machining for mating flanges and tight-tolerance interfaces.

### 3. Simplified Engine Architecture

- **Tap-Off Cycle Design**. Manufacturing speed is also baked into Firefly's engine design. Unlike complex staged-combustion engines, Firefly’s engines use a **combustion tap-off cycle**, which bleeds hot gas directly from the main combustion chamber to drive the turbopumps. Eliminating a separate gas generator or preburner significantly cuts the total number of parts that need to be printed or machined.

*(Note: While you will often see Firefly's manufacturing mentioned alongside **Automated Fiber Placement (AFP)**, that robotic layup process is used for its carbon-composite rocket airframes and propellant tanks, not its metallic engines.)*

If you're looking into a specific aspect of their propulsion, let me know if you want to explore:

- **Specific engine specs** (comparing Reaver, Lightning, Miranda, or Vira)
- **Materials used** (such as copper alloys or nickel superalloys in PBF-LB)
- **How Firefly's approach compares** to other 3D-printed rocket makers like Relativity Space or Rocket Lab

---

## Part 4. Stoke Space

From conversation with Gemini on [how does Stoke Space produce their rocket engines](https://share.google/aimode/4dnaFSLb2yFLZkW8Y)

> how does Stoke Space produce their rocket engines? is it Laser Powder Bed Fusion (PBF-LB)?

**Yes, Stoke Space heavily relies on Laser Powder Bed Fusion (PBF-LB) to produce its rocket engines**, alongside post-print CNC machining and specialized laser welding.

Because Stoke Space is vertically integrated, the company designs, prints, and machines its propulsion hardware in-house at its Kent, Washington headquarters to enable rapid iteration.

### 1. Laser Powder Bed Fusion (PBF-LB)

Stoke Space uses industrial PBF-LB systems—specifically [Additive Industries' MetalFab G2 and MetalFab 420K](https://www.voxelmatters.com/at-stoke-space-metalfab-rules/) multi-laser metal 3D printers—to fabricate complex engine components that would be nearly impossible to make with traditional manufacturing:

- **Thrust Chambers & Cooling Channels**. Stoke 3D-prints the thrust chambers for both its first-stage **Zenith** engines and its second-stage **Andromeda** engine (which features a ring of 24 individual thrusters). Printing allows them to embed intricate internal manifolds and regenerative cooling channels directly into the chamber walls.
- **Exotic & Custom Alloys**. To handle extreme thermal loads and allow rapid reuse without refurbishment, Stoke prints its chambers out of a **high-conductivity copper alloy**. They also partnered with [QuesTek Innovations](https://questek.com/questek-innovations-featured-as-additive-manufacturing-leader-in-space-industry/) to develop a custom, printable nickel superalloy engineered to balance high strength with oxygen burn resistance for extreme engine environments.
- **High-Throughput Production**. Following a beta program, Stoke expanded its additive fleet with five MetalFab 420K systems. Each machine uses four 1-kilowatt lasers with variable beam spot sizes (100–500 µm) to speed up build rates while maintaining fine structural resolution.

### 2. Post-Processing & Depowdering

Printing intricate copper cooling channels creates a major manufacturing hurdle: unfused copper powder tends to clump and stick inside tight internal cavities. To solve this, Stoke uses specialized post-processing workflows:

- **Automated Depowdering**. Stoke uses [Solukon SFM-AT800-S](https://3dprint.com/308305/stoke-space-deploys-solukons-automated-depowdering-solution-for-reusable-rockets/) depowdering systems equipped with two-axis rotation, ultrasonic vibration, and high-frequency knockers to shake loose trapped copper powder from internal regenerative channels.
- **Precision CNC Machining**. Once a thrust chamber or engine component is printed and depowdered, it moves to Stoke’s in-house machine shop. Using 4-axis and 5-axis CNC mills, lathes, and electrical discharge machining (EDM), technicians finish critical sealing surfaces and mating interfaces.

### 3. Laser Welding

To assemble engine components and attach them to the vehicle's structure without warping thin-walled metal parts, Stoke has largely replaced traditional TIG welding with **handheld and robotic laser welding** (using [IPG Photonics LightWELD systems](https://www.lightweld.com/the-weld-shop/success-story-stoke-space/)). Laser welding delivers significantly lower heat input than arc welding, preventing part distortion when joining delicate, thin-walled engine hardware and regenerative heat shield structures.

Would you like to explore a specific part of Stoke Space's propulsion manufacturing, such as:

- The **Zenith** booster engine's full-flow staged-combustion hardware
- The **Andromeda** upper stage's 24-thruster ring and actively cooled heat shield
- Specific **materials and alloys** used in their 3D printing process

---

## Part 5. Relativity Space

From conversation with Gemini on [how does Relativity Space produce their rocket engines](https://share.google/aimode/39pR1kwuc0gssgit0)

> how does Relativity Space produce their rocket engines? is it Laser Powder Bed Fusion (PBF-LB)?

Yes—Relativity Space uses **Laser Powder Bed Fusion (PBF-LB)** for detailed engine components like 
- combustion chambers, 
- nozzles, 
- and cooling channels, 

alongside **Wire Arc Additive Manufacturing (WAAM)** and traditional manufacturing methods.

### How Relativity Space Makes Its Engines

- **Laser Powder Bed Fusion (PBF-LB)**: Lasers selectively fuse thin layers of metal powder (often only tens of microns thick) one layer at a time. This works well for fine internal features like cooling channels, injectors, and detailed combustion chamber or nozzle parts. NASA's **GRCop** copper alloys (such as GRCop-84 or GRCop-42) are well suited for high-heat thrust chamber parts made with PBF-LB.

- **Wire Arc Additive Manufacturing (WAAM) & Stargate**: Relativity's Stargate 3D-printing platform uses robotic arms and additive processes—including PBF and WAAM—to build large or complex engine hardware (like Aeon R components) faster and iterate quickly on designs.

- **Hybrid Manufacturing**: For the Terran R rocket and Aeon R engines, Relativity pairs additive manufacturing with traditional methods—such as friction stir welding and machining—to balance speed, cost, and performance.

On Reddit's [r/AdditiveManufacturing](https://www.reddit.com/r/AdditiveManufacturing/comments/l5cnvw/whats_the_deal_with_relativity_space_wtf/), opinions are mixed on exact materials and processes, with users noting that while exact recipes can be confidential, commercial suppliers and rocket hardware clues let people infer general alloy and printing approaches.

Are you looking into a specific engine—like **Aeon 1** or **Aeon R**—or curious about how **GRCop copper alloys** handle engine heat?
