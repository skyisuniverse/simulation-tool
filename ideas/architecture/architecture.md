# Architecture

- [ ] Extract & unify architecture ideas from:
  - [ ] [README.md](../../README.md)
  - [ ] [Architectural Configuration Matrix](../features/features-part-5.md)  from ../features/features-part-5.md


## Architectural Configuration Matrix

| Feature Tier | Primary Target Use Case | Key Technical Dependencies |
| :--- | :--- | :--- |
| **Pre-Processing** | Geometry cleanup & automeshing | Direct modeling engine, CAD translation libraries |
| **Solver Core** | Multiphysics execution | Linear algebra libraries, MPI parallelization, GPU SDKs |
| **Optimization** | Topology & Parametric exploration | DoE frameworks, optimization heuristics, surrogate ML |
| **Surrogate AI** | Real-time predictive 3D fields | Geometric Deep Learning, historical dataset training pipelines |


## adr cli & sdk

- adr cli
- adr sdk
