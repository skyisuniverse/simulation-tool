# preCICE

([precice.org](https://precice.org/), [github.com/precice](https://github.com/precice)) 

preCICE is an **open-source coupling library and ecosystem** for general partitioned multi-physics and multi-scale simulations, including surface and volume coupling.

  Partitioned means that **preCICE couples existing programs/solvers** capable of simulating a subpart of the complete physics involved in a simulation. This allows for the high flexibility that is needed to keep a decent time-to-solution for complex coupled problems.

  The software offers convenient methods for transient equation coupling, communication, time interpolation, and data mapping.

  - **Minimally invasive integration**
    - Elegant library approach
    - High-level API in C++, C, Fortran, Python, Matlab
  - **Coupling of arbitrary many programs**
    - Arbitrary combinations of strong and weak interactions
    - Arbitrary many solvers
  - **State-of-the-art numerical methods**
    - Robust quasi-Newton acceleration
    - Radial-basis function data mapping
  - **Scalability up to complete supercomputers**
    - Pure peer-to-peer approach
    - Support of heterogenous hardware (CPU/GPU)
    - Efficient also on a laptop
