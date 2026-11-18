# SMLib

Gemini on [SMLib](https://share.google/aimode/pKSXiOyMBIGS6bqYy)

SMLib is **a pure-NURBS and polygonal boundary representation (B-rep) solid modeling geometry kernel** originally developed by Solid Modeling Solutions (SMS) and acquired by Nvidia. ([SMlib is a purely NURBS based geometry kernel...](https://x.com/istvan_csanady/status/2110478253177905606), [nvidia omniverse](https://docs.nvidia.com/omniverse/), [Solid Modeling Solutions](https://en.wikipedia.org/wiki/Solid_Modeling_Solutions))

[awv-informatik/smlibpy](https://github.com/awv-informatik/smlibpy)

[smlibpy.classcad.ch](https://smlibpy.classcad.ch/)

## Key Details

- **Core Functions**: Creates and edits B-rep solids, managing operations like boolean geometry, fillets, sweeps, offsets, and surface healing. ([tangency-labs/smlib](https://github.com/tangency-labs/smlib), [NVIDIA-Omniverse/usd-brep](https://github.com/NVIDIA-Omniverse/usd-brep))

- **Nvidia & Open-Source Release**: Nvidia acquired SMS in May 2022 and open-sourced the underlying technology as part of its USD BRep initiative to expose CAD geometry directly to neural networks, LLMs, diffusion models, and the Nvidia Omniverse. ([Nvidia launches USD BRep geometry kernel for solid modelling](https://develop3d.com/cad/nvidia-launches-usd-brep-geometry-kernel-for-solid-modelling/))

- **Ecosystem & Bindings**:
  - [smlibpy](https://github.com/awv-informatik/smlibpy): A Python wrapper and API (styled after **build123d**) that interfaces with SMLib, supporting STEP, IGES, USD, BREP, DXF, and other file formats.
  - **WebAssembly/JS**: Compiles locally into the browser via WebAssembly (`smlibwasm` / `smlibpy-three`).
  - **Integrations**: Powers tools like AWV Informatik's ClassCAD and connects with openUSD pipelines.

Would you like to explore how to set up **smlibpy** in Python or look into its integration with **Nvidia Omniverse**?
