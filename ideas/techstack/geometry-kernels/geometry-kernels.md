# Geometry kernels

## OpenGeometry

Geometry Infrastructure
for Humans & AI Agents

[opengeometry.io](https://opengeometry.io/)

### Kernel

A Rust and WebAssembly geometry kernel with a TypeScript API for browser applications.

[openGeometry-io/OpenGeometry](https://github.com/openGeometry-io/OpenGeometry)

Geometry CAD Kernel for Humans and AI Agents

**Open-source CAD kernel for the web: exact B-rep solids, booleans, extrude, sweep and revolve, and STEP export, in Rust and WebAssembly with a TypeScript SDK for Three.js. For product configurators, mechanical parts, buildings, robotics and AI agents that model.**

#### **What is OpenGeometry?**

OpenGeometry is an **open-source CAD kernel for the web**. It models **B-rep solids** with exact planes, cylinders, spheres, cones and tori, runs **boolean operations** (union, subtract, intersect), builds solids by **extrude, sweep and revolve**, hollows them with **shell**, and writes **STEP** files that other CAD and CAM tools open. The kernel is written in **Rust** and compiled to **WebAssembly**. A **TypeScript SDK for Three.js** puts every body straight into your scene, and the same calls run in **Node.js** with no browser.

It is the geometry engine, not a CAD application: you build the product, OpenGeometry does the solid modelling. The same calls give the same shape every time, so an app, a script or an AI agent can drive it and check the result with exact queries: volume, area, bounds, validity, and whether a point is inside.

## Use cases

| Field | What you build | What OpenGeometry gives you |
| --- | --- | --- |
| **Product configurators and e-commerce** | A shopper picks sizes and options and sees the exact part, then orders it | Parametric primitives that `rebuild` in place, booleans for cut-outs, STEP for the factory |
| **Mechanical parts and enclosures** | Plates, brackets, housings, flanges, pipe parts | Rounded boxes, slots, cylinders, pipe segments, through-holes in one call, shell for walls, STEP in millimetres |
| **Manufacturing and fabrication** | Web tools that turn an order into a production file | Exact B-rep, valid and closed solids, STEP export with an export report |
| **Architecture, construction and interiors** | Walls, openings, slabs, furniture, MEP parts | Polysolid walls along a path, extrude with holes, sweeps along arcs, the IFC exchange body for an IFC writer |
| **Robotics and automation** | Fixtures, grippers, end-of-arm tools, work-cell layouts | Assemblies with placements, point-inside tests, measured volume, picking down to face and edge |
| **AI agents and prompt-to-CAD** | An agent that turns a request into a part, then checks it | Plain JSON parameters, deterministic results, `validity()` and `measure()` to verify, typed errors with a `code` |
| **Education and geometry tools** | Teaching solids, booleans and B-rep in a browser tab | Open source, runs client-side, the B-rep of every body is readable |
| **Server-side generation** | A Node.js service that makes STEP files from parameters | The same API in Node, with inline tessellation and no browser |
