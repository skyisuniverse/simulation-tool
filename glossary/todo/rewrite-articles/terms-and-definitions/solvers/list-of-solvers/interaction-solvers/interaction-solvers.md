# Interaction solvers

Can we have:

1. All types of solvers integrated into a single (robust low-latency) system
2. Have interaction solvers that would calculate all effects combined? (assume full real-world simulation at once (low latency lol))

From [List of solvers (Part 2)](../list-of-solvers.md)

> # Part 2
>
> ## 1. Multiphysics & Coupled-Field Solvers
>
> - **Fluid-Structure Interaction (FSI) Solvers**: Couples a CFD solver with an FEA solver concurrently, exchanging data at boundary interfaces to calculate how fluid forces deform solids and how those deformed solids alter the fluid flow (e.g., calculating heart valve mechanics, wind turbine blade flexing, or aircraft wing flutter).

---

can this be useful in the context of atoms / molecules as a basis for simulation (rather than elements) ?

> - **Discrete Element Method (DEM) Solvers**: Tracks the kinematics and forces of individual granular particles colliding with each other and with rigid walls over time (e.g., simulating bulk solids handling, agricultural grain silos, rock crushing machines, or pharmaceutical pill mixing).

---

From [List of solvers (Part 3)](../list-of-solvers.md)

> ## 4. Multiscale Bridging Solvers
>
> - **Atomistic-to-Continuum (AtC) Solvers**: A hybrid method that couples an explicit molecular dynamics solver (for localized atomic cracks/defects) directly to a standard Finite Element Analysis (FEA) continuum solver at the boundary region (e.g., measuring how a microscopic grain-boundary defect causes a macro-scale failure in a turbine blade).


---

From [List of solvers (Part 5)](../list-of-solvers.md)

## 4. Kinetic & Plasma Dynamics Synthesis Solvers

- **Chemical Reduction Kinetic Solvers**: Solves coupled differential reaction equations that balance heating, reducing agents, and capping agents over a set time timeline. It bridges chemical engineering with physical geometry to map synthesis rates (e.g., tracking the bottom-up chemical reduction of a metal salt solution into a colloidal metallic nanoparticle).
