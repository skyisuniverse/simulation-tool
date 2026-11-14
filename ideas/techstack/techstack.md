# TechStack

## Considerations

We might aim to develop/support two app tracks in parallel:

- **Engineering sim for nano-assembly** / quantum as a manufacturing method
  - nano-assembly
    - with DNA
    - quantum (?)
- **Engineering sim for** already existing **traditional manufacturing**
  - CNC-machining
  - 3D-printing
  - injection molding
  - casting

We assume that the tech-stack for the first method might not be existing yet and/or not available in open-source, thus we'd have to conceptualize and develop it ourselves.

For the second method things are easier, as there are some (supposedly related) open-source packages (subject to further hypothesis verification in practice).

## Devices

- What about adaptivity? (computers / mobiles (?)))

---

## OpenSource tools

- [ ] From [features-part-5.md](../features/features-part-5.md) :
  - Are you planning to build **proprietary solvers** from scratch, or wrap around **open-source solvers** like:
    - [OpenFOAM](https://www.openfoam.com) 
    - or [CalculiX](https://github.com/calculix)?

---

- [ ] Process
  - [ ] [qd-cae/awesome-CAE](https://github.com/qd-cae/awesome-CAE) (awesome CAE frameworks, libraries and software)
    - [ ] [CAD](https://github.com/qd-cae/awesome-CAE#cad)
    - [ ] [Preprocessors](https://github.com/qd-cae/awesome-CAE#preprocessors)
    - [ ] [Materials](https://github.com/qd-cae/awesome-CAE#materials)
    - [ ] [Solver related](https://github.com/qd-cae/awesome-CAE#solver-related)
    - [ ] [Postprocessing](https://github.com/qd-cae/awesome-CAE#postprocessing)
    - [ ] [Optimization](https://github.com/qd-cae/awesome-CAE#optimization)
    - [ ] [Tools](https://github.com/qd-cae/awesome-CAE#tools)
    - [ ] [Editors](https://github.com/qd-cae/awesome-CAE#editors)
    - [ ] [Documentation](https://github.com/qd-cae/awesome-CAE#documentation)
  - [ ] [010zx00x1/Awesome-Physical-Engineering-AI](https://github.com/010zx00x1/Awesome-Physical-Engineering-AI)  (from [features-part-3.md](../features/features-part-3.md)) (list of AI tools for hardware engineering — CAD, simulation, manufacturing, and beyond)
    * [🎨 AI CAD & Engineering Design](https://github.com/010zx00x1/Awesome-Physical-Engineering-AI#ai-cad-engineering-design)
    * [🔍 Engineering Review, Drawings & Knowledge](https://github.com/010zx00x1/Awesome-Physical-Engineering-AI#engineering-review-drawings-knowledge)
    * [🧪 AI for CAE & Simulation](https://github.com/010zx00x1/Awesome-Physical-Engineering-AI#ai-cae-simulation)
    * [⚙️ AI CAM & Manufacturing](https://github.com/010zx00x1/Awesome-Physical-Engineering-AI#ai-cam-manufacturing)
    * [👁️ Inspection & Machine Vision](https://github.com/010zx00x1/Awesome-Physical-Engineering-AI#inspection-machine-vision)
    * [🔮 Predictive Maintenance & Industrial AI](https://github.com/010zx00x1/Awesome-Physical-Engineering-AI#predictive-maintenance-industrial-ai)
    * [🧱 Materials AI](https://github.com/010zx00x1/Awesome-Physical-Engineering-AI#materials-ai)
    * [🤖 Robotics & Physical AI](https://github.com/010zx00x1/Awesome-Physical-Engineering-AI#robotics-physical-ai)
    * [⚡ Electronics, PCB & EDA AI](https://github.com/010zx00x1/Awesome-Physical-Engineering-AI#electronics-pcb-eda-ai)
    * [🔌 MCP Servers, Connectors & Agent Skills](https://github.com/010zx00x1/Awesome-Physical-Engineering-AI#mcp-connectors-agent-skills)
    * [📄 Research Models & Methods](https://github.com/010zx00x1/Awesome-Physical-Engineering-AI#research-models-methods)
    * [📊 Benchmarks & Reality Checks](https://github.com/010zx00x1/Awesome-Physical-Engineering-AI#benchmarks-reality-checks)
    * [🧰 Engineering Foundations](https://github.com/010zx00x1/Awesome-Physical-Engineering-AI#-engineering-foundations) 
      * CAD kernels, modelers, and programmatic CAD
      * CAE solvers, meshing, and visualization
      * Robotics, dynamics, and controls
      * Scientific and engineering Python
      * Computer vision infrastructure
      * Additive manufacturing infrastructure
      * Digital twin and engineering-data infrastructure
      * Materials data and analysis
    * [🧪 Experimental / Early Projects](https://github.com/010zx00x1/Awesome-Physical-Engineering-AI#experimental-early-projects)
    * [🪦 Removed / Reclassified](https://github.com/010zx00x1/Awesome-Physical-Engineering-AI#removed--reclassified)
    * [📚 Learning Resources](https://github.com/010zx00x1/Awesome-Physical-Engineering-AI#learning-resources)
  - [ ] [joreilly86/Python-Libraries-for-Engineers](https://github.com/joreilly86/Python-Libraries-for-Engineers) (relevant Python libraries for Professional Engineers)
  - [ ] [m2n037/awesome-mecheng](https://github.com/m2n037/awesome-mecheng) (General mechanical-engineering awesome list)
  - [ ] [edt-community/awesome-digital-twins](https://github.com/edt-community/awesome-digital-twins) (Curated repository of awesome Digital Twin resources)
  - [ ] [Roboflow Universe](https://universe.roboflow.com/) (Computer-vision datasets)
  - [ ] [Awesome Internet of things and sensor data](https://github.com/oxnr/awesome-bigdata#internet-of-things-and-sensor-data)

---

- [dhondt.de](https://www.dhondt.de/) A Free Software Three-Dimensional Structural Finite Element Program
- [calculix.de](https://www.calculix.de/)
  - [jet-engine-model and documentation](https://www.calculix.de/fw05.html)
  - [example of the turbo-charger compressor](https://www.calculix.de/fw05lav.html)
  - [example of the turbo-charger turbine](https://www.calculix.de/fw05lat.html)
  - [further examples](https://github.com/calculix/CalculiX-Examples)


- [CALCULIX](https://github.com/calculix) (Developers area of CalculiX Finite Element Software)
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
  - [](https://www.salome-platform.org/)

---

## Concerns

We have several domains of concerns that we have to make work together in one single product performantly:

- Programming language (s) for best performance (C / Assembly?)
- Device support, Adaptivity (computers, mobiles, etc.)
- OpenSource tools
  - Some tools are written in Python (like solvers(?))
  - Some tools are written in JS/TS (like (web / mobile) frontend)
  - etc.

How do we make it all work together?

- Conceptualize the product
  - finalize features, stories
  - make a list of scenarios for simulations 
- Inspect possible dependencies (open-source tools)
- Create a table for techstack, list all 
  - programming languages
  - tools (libs, apps, frameworks, etc.)
- Analyze the applicability of each tech for the overall requirements
  - Performance
  - Scalability
- Choose techstack wisely with future-proof vision (as much as possible, given the scope of task, lol)
