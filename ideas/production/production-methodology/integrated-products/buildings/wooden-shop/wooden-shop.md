# Wooden Shop

[Wooden Shop - CAD Model](../../../../../../CAD-models/test-text-to-cad-wooden-shop) (generated with [text-to-cad](ideas/techstack/text-to-cad/text-to-cad.md))

[Wooden Shop - CAD Model - Screenshots](../../../../../../CAD-models/test-text-to-cad-wooden-shop-img)

![](../../../../../../CAD-models/test-text-to-cad-wooden-shop-img/1.png)

![](../../../../../../CAD-models/test-text-to-cad-wooden-shop-img/2.png)

![](../../../../../../CAD-models/test-text-to-cad-wooden-shop-img/3.png)

![](../../../../../../CAD-models/test-text-to-cad-wooden-shop-img/4.png)

![](../../../../../../CAD-models/test-text-to-cad-wooden-shop-img/5.png)

![](../../../../../../CAD-models/test-text-to-cad-wooden-shop-img/6.png)

![](../../../../../../CAD-models/test-text-to-cad-wooden-shop-img/7.png)

![](../../../../../../CAD-models/test-text-to-cad-wooden-shop-img/8.png)

![](../../../../../../CAD-models/test-text-to-cad-wooden-shop-img/9.png)

![](../../../../../../CAD-models/test-text-to-cad-wooden-shop-img/10.png)

![](../../../../../../CAD-models/test-text-to-cad-wooden-shop-img/11.png)

![](../../../../../../CAD-models/test-text-to-cad-wooden-shop-img/12.png)

![](../../../../../../CAD-models/test-text-to-cad-wooden-shop-img/13.png)

![](../../../../../../CAD-models/test-text-to-cad-wooden-shop-img/14.png)

![](../../../../../../CAD-models/test-text-to-cad-wooden-shop-img/15.png)

![](../../../../../../CAD-models/test-text-to-cad-wooden-shop-img/16.png)

---

[Conversations with Gemini on a CNC-machine for wooden shop assembly](./conversations.md)

How do we automate production / assembly of wooden shops?

Let's assume wood as a building material to begin with, since it will make it easier to start - wood as a material is easy to operate, manipulate, transform compared to other materials like metal. It is also cheap enough and affordable and widely used in construction.

Let's assume medium-size 1-story (floor) 1-room shop for 1 person, comfortable for production, working with wood, metal, etc.

## Considerations

Could the tool to build a wooden shop be something like a big open-source [CNC-machine](ideas/production/production-methodology/integrated-products/cnc-machines/cnc-machine.md), that would perform all operations to build the wooden shop entirely autonomously?

All considerations were moved to [CNC-machine (cnc-machine.md)](ideas/production/production-methodology/integrated-products/cnc-machines/cnc-machine.md) in order to be converted into the CNC-machine techspecs. (deduplicate later)

### Generic operations

- Measuring (e.g. measurements of sizes of building materials, like lengths / widths / thickness of wooden boards)

### Operations with wood

- Cutting
- Stapling
- Drilling
- Polishing
- Painting
-

Could the tool to build a wooden shop be something like a big open-source CNC-machine, that would perform all operations to build the wooden shop entirely autonomously?

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

## LLM

Could such CNC-machine be powered by an LLM with computer vision for object recognition?

## Computer vision

- object recognition? e.g.: 
  - differentiation of different types of objects (doors, windows, frames, sheets, etc.
  - differentiation of different types of materials (wood, stone, metal, etc.?)

...

---

## CNC

- Could a CNC have a list of necessary tools to perform operations on the wood +
- A **single energy source** to power all of the tools +
- A **programmatically controlled energy distribution** to **control how much energy is distributed** for handling **each particular tool and operation** within a tool ?


### Gantry

- What size of gantry would be fine?
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
