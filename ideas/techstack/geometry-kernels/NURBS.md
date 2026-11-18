# NURBS kernel

Gemini on [nurbs kernel](https://share.google/aimode/SNCqnNAPFVoeZMwcy)

A **NURBS kernel** (or geometric modeling kernel) is **the core software engine behind 3D CAD, CAM, and CAE applications that mathematically creates, manipulates, and analyzes 3D shapes**.

[Non-uniform rational B-spline](https://en.wikipedia.org/wiki/Non-uniform_rational_B-spline)

It combines **NURBS** (Non-Uniform Rational B-Splines) to represent exact curves and smooth surfaces with **B-Rep** (Boundary Representation) to track how those surfaces connect into watertight 3D solids.

[NVIDIA Open-Sources CAD Kernel! The Expanding Possibilities of CAD with SMLib and AI](https://note.com/teruemon/n/n95ccc9062d25?hl=en)

## Core Functions of a NURBS Kernel

- **Exact Geometry Representation**. Unlike polygon meshes that approximate shapes with flat triangles, NURBS uses polynomial equations, weighted control points, and knot vectors to define curves and surfaces with infinite mathematical precision. This allows exact representation of both freeform organic shapes and analytical primitives like true circles and cylinders.

- **Boolean and Topological Operations**. The kernel calculates complex 3D intersections to perform solid modeling actions like union, subtraction, and intersection. [OpenGeometry](https://github.com/openGeometry-io/OpenGeometry)

- **Surface Modification**. It executes low-level algorithms such as knot insertion, degree elevation, lofting, sweeping, filleting, and offsetting. [OpenGeometry](https://github.com/openGeometry-io/OpenGeometry)

- **Data Exchange and Tessellation**. It translates models into standard industry formats (like STEP and IGES) and tessellates smooth NURBS surfaces into polygon meshes for screen rendering or 3D printing. [OpenGeometry](https://github.com/openGeometry-io/OpenGeometry)

## Notable NURBS & B-Rep Kernels

- [Open CASCADE Technology (OCCT)](https://occt3d.com/open-cascade-technology/index.html). The most established open-source B-Rep and NURBS kernel, widely used in free and commercial engineering tools like FreeCAD and Analysis Situs. (????) 

> Does Open CASCADE support Nurbs? ([see Prompt 5 of text-to-cad-evolution-path-for-integrated-product-design.md](ideas/production/production-methodology/integrated-products/text-to-cad-evolution-path-for-integrated-product-design.md))

- [NVIDIA USD BRep (incorporating SMLib)](https://develop3d.com/cad/nvidia-launches-usd-brep-geometry-kernel-for-solid-modelling/). An open-source C++ and Python geometry library based on the pure-NURBS SMLib kernel. It integrates exact CAD solids directly into [OpenUSD](https://openusd.org/release/index.html) pipelines, AI workflows, and browser environments.

- [OpenGeometry](https://github.com/openGeometry-io/OpenGeometry). A modern open-source B-Rep CAD kernel written in Rust and compiled to WebAssembly for browser-based modeling and STEP export.

- **Commercial Industry Kernels**. Proprietary engines like [Parasolid](plm.sw.siemens.com/en-US/plm-components/parasolid/) (Siemens), [ACIS](https://www.spatial.com/solutions/3d-modeling/3d-acis-modeler) (Dassault Systèmes), C3D, and the proprietary kernel powering [Rhino 3D](https://www.rhino3d.com/) dominate commercial mechanical CAD and industrial design.

---

How would you like to explore this further? Let me know if you are looking to:

- **Integrate a kernel** into a software project (e.g., C++, Python, Rust, or web/WASM)
- **Compare specific kernels** by licensing, features, or performance
- **Understand the math** behind NURBS evaluation, knot vectors, and B-Rep topology
