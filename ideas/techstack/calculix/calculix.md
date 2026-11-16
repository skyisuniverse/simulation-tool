# Calculix

[Calculix (Wikipedia)](https://en.wikipedia.org/wiki/Calculix)

- [dhondt.de](https://www.dhondt.de/) A Free Software Three-Dimensional Structural Finite Element Program
- [calculix.de](https://www.calculix.de/)
  - [jet-engine-model and documentation](https://www.calculix.de/fw05.html)
  - [example of the turbo-charger compressor](https://www.calculix.de/fw05lav.html)
  - [example of the turbo-charger turbine](https://www.calculix.de/fw05lat.html)
  - [further examples](https://github.com/calculix/CalculiX-Examples)


- [CALCULIX](https://github.com/calculix) (Developers area of CalculiX Finite Element Software)
  - [32 repositories](https://github.com/orgs/calculix/repositories?type=all)
  - [calculix/CalculiX-Windows](https://github.com/calculix/CalculiX-Windows) 
    - CalculiX is an **OSS package** designed **to solve field problems**. The method used is the **finite element method**. This package is a native Microsoft Windows 64-bit build of CalculiX.
  - [calculix/beso](https://github.com/calculix/beso) (Python code for **topology optimization** using CalculiX FEM solver.)
  - [calculix/CalculiX-Examples](https://github.com/calculix/CalculiX-Examples) CalculiX examples. Excellent starting point to master **parametric modelling** with CGX and CCX.
  - [calculix/examples](https://github.com/calculix/examples) 
    - Official and user examples for CCX and CGX. All in one place. Do not hesitate to add yours.
  - [calculix/cae](https://github.com/calculix/cae) (CalculiX Advanced Environment, **correct input file with no mistakes**)
  - [calculix/ccx2paraview](https://github.com/calculix/ccx2paraview)
    - **CalculiX to Paraview converter (frd to vtk/vtu)**. Makes possible to view and postprocess CalculiX analysis results in Paraview. Generates Mises and Principal components for stress and strain tensors.
  - [calculix/pygccx](https://github.com/calculix/pygccx)
    - A python framework to build, solve and postprocess finite element models made out of 3D solid elements using Gmsh and CalculiX.
  - [calculix/Cubit-CalculiX](https://github.com/calculix/Cubit-CalculiX)
    - **Pre- and Postprocessing** for CalculiX can be done with this component in coreform cubit. The results will be converted to Paraview (.frd and .dat: nodal, element and integration points results).
  - [calculix/docker-calculix](https://github.com/calculix/docker-calculix)
    - Docker Compose configuration to run CalculiX in a containerized environment
  - [calculix/ccx_runner](https://github.com/calculix/ccx_runner)
    - Lightweight tool to **call and monitor a** running CalculiX **process**. Most useful **for long running simulations**.
  - [calculix/CyclicAMIChannel](https://github.com/calculix/CyclicAMIChannel) example implementation of an [OpenFOAM](https://www.openfoam.com) model
  - [calculix/inp2unv](https://github.com/calculix/inp2unv)
    - CalculiX to Salome universal converter. Converts CalculiX INP mesh to the UNV format.


---

# Calculix

Gemini on [Calculix](https://share.google/aimode/hgv45tmIb06pdSrGw)

CalculiX is a **free and open-source Finite Element Analysis (FEA) software package used to solve 3D structural, thermal, fluid, and coupled multi-physics problems**.

## Key Components & Architecture

- **CalculiX CrunchiX (`ccx`)**: The core implicit and explicit finite element solver developed by Guido Dhondt. It uses input file formats and naming conventions compatible with Abaqus. [Calculix (wikipedia)](https://en.wikipedia.org/wiki/Calculix)

- **CalculiX GraphiX (`cgx`)**: The interactive 3D pre- and post-processor developed by Klaus Wittig for model building, meshing, and viewing results.

- **Alternative GUIs & Interfaces**: Many users pair CalculiX with user-friendly graphical interfaces like [PrePoMax](https://prepomax.fs.um.si) ([github](https://github.com/PrePoMax/PrePoMax)) or CAD tools like [FreeCAD](https://www.freecad.org) (via its FEM workbench).

## Core Capabilities

- **Analysis Types**: Linear and non-linear static, dynamic/explicit, eigenfrequency (modal), buckling, heat transfer, and coupled thermo-mechanical simulations.

- **Material Models**: Linear elastic, plastic, and hyperelastic material definitions.

- **Interoperability**: Can import/export or generate mesh data for tools like Abaqus, Ansys, Nastran, Code-Aster, and OpenFOAM, or couple with fluid solvers via [preCICE](https://precice.org/) ([github](https://github.com/precice)).

- **Platforms**: Available for Linux and Windows (maintained via official archives and repositories like the [CalculiX GitHub Repository](https://github.com/Dhondtguido/CalculiX)).

Are you looking for help with:

- Setting up a **specific FEA model or input file** **(`.inp`)**?
- Installing **CalculiX or a GUI like PrePoMax** on Windows or Linux?
- Running a particular kind of analysis (like **thermal**, **contact**, or **non-linear static**)?

---

Geminin on [CalculiX (2)](https://share.google/aimode/UdcA3K6fZgHNO44hp)

CalculiX is a free and open-source finite element analysis (FEA) suite used to solve 3D linear and non-linear structural, dynamic, thermal, and coupled field problems.

## Key Components

- **CalculiX CrunchiX (`ccx`)**: The core implicit and explicit solver written by Guido Dhondt.

- **CalculiX GraphiX (`cgx`)**: The interactive 3D pre- and post-processor written by Klaus Wittig.

- **Solvers & Add-ons**: Integrates sparse direct solvers like SPOOLES and PaStiX (with optional CUDA acceleration), ARPACK for eigenvalue/frequency problems, CAD converters, and preCICE for fluid-structure interaction.

## Common Ecosystem & Interfaces

- **PrePoMax**: A popular, user-friendly open-source Windows GUI frontend for CalculiX.
- **FreeCAD**: Features a built-in FEM workbench that automates CalculiX model creation.
- **PyCalculix**: A Python library designed to build, mesh, and run 2D CalculiX models programmatically.
- **Operating Systems**: Native support for Linux and Windows (via direct ports and launchers).

Would you like to know more about:

- **Setting up a model** in CalculiX or PrePoMax?
- **Installing** CalculiX on Windows or Linux?
- Running a specific type of **analysis** (static, thermal, or modal)?
