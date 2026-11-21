# CNC-machine

What type of CNC-machine (s?) do we want to produce? Ideally, such that would be capable of producing parts for anything - from desktop tools / devices to rockets / rocket components.

Consider a **multi-tool CNC** with [tools](./tools.md):

- [plasma cutting (for metal)](./tools/plasma.md)
- [laser (3D-printing metal)](laser.md)
- stapler
- saw
- painter
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

...

## Requirements for Tools

What are requirements for the tools for CNC for building a wooden shed

In order for them to be easily pickable, usable and disposable by the linear stage ?

Should all those tools have a standard similar connector, that connects the tool to the moving stage?

Should the handle be durable enough in order to withstand the load during operation?

---
