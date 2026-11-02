# List of solvers

From conversation with Gemini on [solvers](https://share.google/aimode/iLABYaR1XBs7bIhjB)

----

- [Part 1]()
  - CFD, FEA, EM
- [Part 2]()
  - Multiphysics & Coupled-Field
  - Acoustic & Wave Propagation
  - Advanced & Alternative CFD
  - Multiscale, Molecular & Materials 
  - Earth Science & Large-Scale Systems
- [Part 3 (nanomaterials and nanoelectronics)]()
  - Quantum Electronic Transport
  - Ballistic & Statistical Semiclassical
  - Advanced Molecular Dynamics (MD) & Force Field
  - Multiscale Bridging
- [Part 4 (nanoelectronic)]()
  - Advanced Band Structure & Empirical Transport
  - Semiclassical & Stochastic Semiclassical
  - Spintronics & Quantum Phase
  - AI & Accelerated Quantum
- [Part 5 (structural/chemical design of nanomaterials)]()
  - Mathematical Optimization & Inverse-Design
  - Specialized Force Field & Nanostructure Geometry Modeler Engines
  - Stochastic Assembly & Surface Area
  - Kinetic & Plasma Dynamics Synthesis

----

# Part 1

From conversation with Gemini on [solvers (part 1) (list all possible for 3d engineering sim)](https://share.google/aimode/VkotUFKdwNSOeQAi9)

In 3D engineering simulation, "solvers" refer directly to the **numerical methods and governing physics equations** hardcoded into software packages.

The extensive taxonomy of 3D simulation solvers spans across major physics domains, categorized by the exact equations they solve and the physical phenomena they calculate.

##  1. Fluid Dynamics & Thermal Solvers (CFD)

- **Navier-Stokes Solvers**: Solves the **Navier-Stokes equations** to calculate fluid velocity, pressure drops, and complex shear stresses in Newtonian fluids (e.g., airflow over an electric vehicle or water rushing through a pump).

- **Reynolds-Averaged Navier-Stokes (RANS) Solvers**: Solves time-averaged equations combined with a turbulence model (like \(k-\epsilon\) or \(k-\omega\)) to calculate macro-level turbulent behavior efficiently without tracking every tiny vortex (e.g., standard industrial HVAC duct flows).

- **Large Eddy Simulation (LES) / Detached Eddy Simulation (DES) Solvers**: Solves filtered equations that directly track massive, chaotic turbulent structures while modeling small-scale eddies mathematically (e.g., aerodynamic buffet and wind noise on side-view mirrors).

- **Euler Solvers**: Solves simplified, inviscid Navier-Stokes equations where fluid friction (viscosity) is ignored to calculate high-speed gas behavior rapidly (e.g., supersonic shockwave patterns around high-altitude aerospace hulls).

- **Lattice Boltzmann Method (LBM) Solvers**: Tracks the statistical probability distribution of discrete particle packets moving on a lattice grid instead of solving continuum mechanics (e.g., complex multiphase tracking like fuel sloshing in a tank or aeroacoustic simulations).

## 2. Structural Mechanics & Solid Solvers (FEA)

- **Linear Static (Hooke's Law) Solvers**: Solves matrix equations formatted as \(F = K \cdot u\) assuming displacements are minuscule and stress stays perfectly proportional to strain to calculate basic rigidity (e.g., checking if a steel bracket yields under a structural dead-weight load).

- **Nonlinear Implicit Solvers**: Steps through calculations incrementally, resolving changing contacts, large geometric distortions, or complex hyperelastic behaviors until global force equilibrium converges (e.g., measuring the sealing pressure of a rubber O-ring or a metal stamping process).

- **Explicit Dynamic Solvers**: Integrates equations forward through microsecond increments without calculating formal global matrix inversion, tracking structural waves directly (e.g., simulating vehicle crashworthiness (impact resistance?) impact tests or ballistic armor penetration).

- **Modal / Harmonic Eigenvalue Solvers**: Solves generalized eigenvalue equations (\(K - \omega^2 M = 0\)) to isolate an assembly's **natural resonant frequencies** and mode shapes (e.g., identifying vibration risk zones in an aircraft engine housing).

## 3. Electromagnetics (EM) & Wave Solvers

- **Method of Moments (MoM) / Boundary Element Method (BEM) Solvers**: Solves the integral form of **Maxwell's equations** by computing surface currents on metallic boundaries rather than meshing open space (e.g., calculating antenna radiation patterns or radar cross-sections).

- **Finite-Difference Time-Domain (FDTD) Solvers**: Marches through time using a staggered grid to solve the differential form of Maxwell’s equations, tracking the movement of electric and magnetic fields dynamically (e.g., high-frequency signal integrity checks on microprocessors or optic fiber wave propagation).

- **Eddy Current / Magnetostatic Solvers**: Solves Maxwell’s equations ignoring wave propagation delays, targeting induction and diffusion fields (e.g., optimizing magnetic flux paths and heat generation inside electric vehicle traction motors).

---

Are you studying one of these fields in particular, or are you **building/coding a custom solver framework** from scratch? If you have a specific physical problem in mind, I can help you choose the exact solver category required.

---

# Part 2

From conversation with Gemini on [solvers (part 2) (list all other possible)](https://share.google/aimode/07jyFplZYJ4MT6SEB)

The solvers listed previously represent the primary, mainstream workhorses found in standard commercial CAD/CAE tools (like Ansys, Abaqus, Simulia, and Altair). However, they are **not the only ones**.

The broader landscape of 3D engineering simulation contains specialized numerical formulations designed for complex materials, subatomic scales, astrophysical bodies, and coupled phenomena.

## 1. Multiphysics & Coupled-Field Solvers

- **Fluid-Structure Interaction (FSI) Solvers**: Couples a CFD solver with an FEA solver concurrently, exchanging data at boundary interfaces to calculate how fluid forces deform solids and how those deformed solids alter the fluid flow (e.g., calculating heart valve mechanics, wind turbine blade flexing, or aircraft wing flutter).

- **Smoothed Particle Hydrodynamics (SPH) Solvers**: A mesh-free, Lagrangian solver that tracks discrete moving particles interacting based on a smoothing kernel function rather than utilizing a geometric grid (e.g., modeling high-energy fragmentation, wave breaking against offshore oil rigs, or bird-strike damage on jet engines).

- **Discrete Element Method (DEM) Solvers**: Tracks the kinematics and forces of individual granular particles colliding with each other and with rigid walls over time (e.g., simulating bulk solids handling, agricultural grain silos, rock crushing machines, or pharmaceutical pill mixing).


## 2. Acoustic & Wave Propagation Solvers

- **Helmholtz Solvers**: Solves the frequency-domain wave equation to calculate steady-state acoustic pressures and sound radiation patterns within or around a structure (e.g., optimizing car cabin acoustics, concert hall sound projection, or speaker enclosure designs).

- **Ray Tracing / Geometrical Acoustic Solvers**: Traces high-frequency acoustic waves as rays that specularly or diffusely reflect off geometries, bypassing small-scale mesh calculations (e.g., mapping radar signatures across kilometers or analyzing long-range sonar propagation under water).


## 3. Advanced & Alternative CFD Solvers

- **Direct Simulation Monte Carlo (DSMC) Solvers**: Simulates low-density, rarefied gas dynamics by using a probabilistic approach to track thousands of model particles colliding with each other and surfaces (e.g., predicting aerodynamic drag on satellites in the upper atmosphere/thermosphere where continuum mechanics assumptions fail).

- **Potential Flow / Vortex Lattice Solvers**: Solves Laplace's equation for velocity potential, ignoring viscosity and rotation entirely, to rapidly determine lifting pressures across thin surfaces (e.g., early-stage conceptual aircraft wing design or high-speed hydrofoil profiles).

## 4. Multiscale, Molecular & Materials Solvers

- **Molecular Dynamics (MD) Solvers**: Solves Newton's classic equations of motion for individual atoms or molecules utilizing empirical interatomic potential forces (e.g., predicting the cracking and degradation of nano-composite polymers or thermal conductivity of graphene sheets).

- **Density Functional Theory (DFT) Solvers**: Solves the quantum mechanical Schrödinger equation using electron density approximations to predict materials properties from first principles (e.g., calculating the electrochemical energy storage limits of next-generation lithium-metal batteries).

- **Phase-Field Solvers**: Solves diffuse-interface equations (like the Allen-Cahn or Cahn-Hilliard equations) to predict microstructural evolution without explicitly tracking physical interfaces (e.g., calculating dendritic crystal growth during metal alloy solidification or micro-crack propagation patterns).

## 5. Earth Science & Large-Scale Systems Solvers

- **Magnetohydrodynamics (MHD) Solvers**: Couples Navier-Stokes equations with Maxwell’s equations to simulate the behavior of electrically conducting fluids like liquid metals or ionized gases (e.g., controlling magnetic confinement in nuclear fusion reactors or tracking solar flare paths).

- **Poromechanics Solvers**: Solves coupled equations governing fluid pressure and solid skeleton deformation in porous media (e.g., predicting oil reservoir compaction, land subsidence, or groundwater seepage through earthen dams).

Because nature is continuous, mathematicians are constantly creating hybrid combinations of these methods. Are you trying to solve a complex **multiphysics problem** (like an object heating up, melting, and then flowing), or are you focusing on **nano-scale materials**?


---

# Part 3

From conversation with Gemini on [solvers (part 3) (for nano-scale materials)](https://share.google/aimode/07jyFplZYJ4MT6SEB)

When simulation scales down to nanomaterials and nanoelectronics (1 to 100 nanometers), traditional continuum mechanics (which assume matter is a solid, continuous block) completely break down. At this boundary, engineering must account for quantum effects, discrete atomic structures, and ballistic particle transport.

---

# Part 4

...

---

# Part 5

...
