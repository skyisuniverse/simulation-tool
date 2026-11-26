# CNC-machine

What type of CNC-machine (s?) do we want to produce? Ideally, such that would be capable of producing parts for anything - from desktop tools / devices to rockets / rocket components.

Consider a **multi-tool CNC** with [tools](./tools.md):

- [plasma cutting (for metal)](./tools/plasma.md)
- [laser (3D-printing metal)](laser.md)
- stapler
- saw
- painter
- welder (with [photonic welding](./processes/metal/welding/photonic-welding.md) / [electrical welding](./processes/metal/welding/electrical-arc-welding.md) ?)
  - how does it affect requirements for [power source (component)](./components/power-source.md) for powering multiple tools, including photonic welder (?) 
- etc. 

that would allows to work with variety (any) materials - including **wood** and **metal**.

---

## CNC. Considerations for (automated assembly of a) [Wooden Shop](ideas/production/production-methodology/integrated-products/buildings/wooden-shop/wooden-shop.md)

From [wooden-shop (CNC considerations)](ideas/production/production-methodology/integrated-products/buildings/wooden-shop/wooden-shop.md)):

> following considerations were made for automated assembly of a wooden shop, we move those here in order to define tech-specs for a CNC-machine

- Could a CNC have a list of necessary tools to perform operations on the wood +
- A **single energy source** to power all of the tools +
- A **programmatically controlled energy distribution** to **control how much energy is distributed** for handling **each particular tool and operation** within a tool ?

### Generic operations

- Measuring (e.g. measurements of sizes of building materials, like lengths / widths / thickness of wooden boards)

### Operations with wood

- Cutting
- Stapling
- Drilling
- Polishing
- Painting
-

Could the tool to build a wooden shop be something like a big open-source [CNC-machine](ideas/production/production-methodology/integrated-products/cnc-machines/cnc-machine.md), that would perform all operations to build the wooden shop entirely autonomously?

- Wooden feedstock
  - either pre-defined and prepared for assembly
  - or standardized for construction purposes (cutting, etc.)
- Shop (building) blueprints
- Automated operations for preparing feedstock for assembly
- Assembly operations
  - Foundation
  - Walls
  - Windows
  - Roof

Frames, Sheets, ...

### Tools

Which tools are typically used and for what type of operations during:

- feedstock preparation
- assembly ?

Which tools could perform such operations within a CNC-machine?


### Gantry

- What size of gantry would be fine? 
  - Can we make the gantry **modular** and easily **disassemblable**? Such that a user can assemble it for a certain task, and later disassemble / assemble it again would there be such a need (e.g. **for a different task (s)**, or in a different place with **different space dimensions**)
  - Such tool could be useful for long-term use (one machine to do it all - from building a shop to later building components / products)
- What components could gantry be made of? ((cut & bolted) steel profiles? hand-cut & finished / pre-fabricated components?)
- What are requirements for gantry and gantry components?
- What are requirements for tool handlers / manipulators? What could those be? (assembled steel spacers sliding along steel tubes?)

### Frame (?)

Is there a need for a frame?

- [ ] [slot-extrusion](glossary/structural-framing/slot-extrusion.md) ?

### Motion system

- [ ] [linear-slide](glossary/structural-framing/linear-slide.md) ?

- [ ] [linear-stage](glossary/structural-framing/linear-stage.md) ?

### Energy distribution

How can we implement tool- and operation- specific energy distribution in a CNC?

### Tool box (tool storage)

Multiple Tools (24? based on [tools](ideas/production/production-methodology/integrated-products/buildings/wooden-shop/tools.md)) could probably be stored in a compact way (e.g. a **tool box**) and taken out of the box and put into work depending on a current needed assembly operation.

([Bambu Lab launches P3C multi-material 3D printer](https://www.voxelmatters.com/bambu-lab-launches-p3c-multi-material-3d-printer/) ? (simpler reference of a compact placement of tools / (unified) materials))

### Tool parallel work

How many parallel tool manipulators would be ok? In order to achieve max assembly speed, we might need multiple tool manipulators to work in parallel.

How do we implement parallel tool work within a single gantry?

- [ ] [T-slot-structural-framing](T-slot-structural-framing.md) ?

### (Optional) (Machine?) Enclosure

Is there a need for an (optional) enclosure? (e.g. in case of bad weather conditions?)

## LLM

Could such CNC-machine be powered by an LLM with computer vision for object recognition?

## Computer vision

- object recognition? e.g.: 
  - differentiation of different types of objects (doors, windows, frames, sheets, etc.
  - differentiation of different types of materials (wood, stone, metal, etc.?)

## LLM costs 

(e.g. for a [wooden shop](ideas/production/production-methodology/integrated-products/buildings/wooden-shop/wooden-shop.md) or any other type of product)

- When assuming assembly of a [wooden shop](ideas/production/production-methodology/integrated-products/buildings/wooden-shop/wooden-shop.md) with LLM (with computer vision, etc.), take into account the cost of usage of LLM
- What does it imply? **Type of access** to LLM, **paid usage**.
- Account for such things as possible **rate limits**, etc. (?). What does a user do in case of such? e.g. just wait and try later? (Shouldn’t be the case for paid versions?)

Ideally, it would be nice to have a performant enough LLM hosted locally to use it without limitations and have **predictable AI costs**.

...

## Requirements for Tools

What are requirements for the tools for CNC for building a wooden shed

In order for them to be easily pickable, usable and disposable by the linear stage ?

Should all those tools have a standard similar connector, that connects the tool to the moving stage?

Should the handle be durable enough in order to withstand the load during operation?

---

### Considerations for Tools

We’ll probably look for cheap but quality tools to assemble CNC from. Expectations are that initially the CNC might be bulky and spacious - because components will be bought and assembled together (probably in a tool box), not designed from scratch to fit the least space possible. Initially we’ll be optimizing for cost / POC, to prove the design is possible at all. 

Later, it is obvious the tool box with each tool will have to be designed from scratch. This design will also have to be evolved over time, with new releases of tools and accompanying software to ensure better performance and cheaper cost.

- It means the necessity to **manufacture tools themselves**. Things like **motion systems**, **connectors**, etc. in order to produce **compact and quality system**.

- Another option - is to focus on integration. There are a lot of good examples of companies that focus on **vertical integration**. However, does it mean they get all components from aside? They produce it themselves. It is a question though, what components they produce and what they use as ready ones.

We assume the following logic:

1. We first search for existing tools / components to implement the idea
2. If existing tools / components are absent, we produce our own.

In general, the course is to be able to **produce as much own stuff as possible**. 

---

## Simple assembly

In order to work in practice (as an idea and a concept) the CNC-machine must be:

- dead **simple to assemble** (e.g. consider **4 parts** in total) (?)
- and dead **simple to operate** (ideally - press **1 button, and let AI do the work**).
- With a possibility to **control step-by-step by verifying AI actions**. 
- With possibility to **manually tap into any AI / CNC op** be there such a need.

The justification is simple - user of the CNC-machine (e.g. homeowners) already have enough headache to take care of, which means that any suggested tool and automation process should be dead simple. Ideally also cheap.

Which means - it has to practically **make sense**. Like, obviously. Without guesses. The gains have to be evident. (e.g. - plasma CNC). The qualitative difference is obvious - no metal any close even in imagination for nerds, due to lack of knowledge / stereotypes. And whole new world with metal and possible incomes - with improved imagination from [practical evidence](https://www.youtube.com/@jdsgarage701/videos).
