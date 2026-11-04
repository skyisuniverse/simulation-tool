# Mesh dependency in the context of atomic fidelity in 3D engineering sim

From conversation with Gemini on [Numerical Model Approximation](https://share.google/aimode/ZMwL0VzpCSw6twCQN) (in classical FEA)

> - **Mesh Dependency**: Because it is an approximation, the accuracy depends on the mesh size. A finer mesh yields an answer closer to the true physical reality, but it never becomes a mathematically perfect, exact solution.

----

> How a mathematically perfect, exact solution can be achieved?

----

> Would a mesh be required with implemented atomic fidelity? 

> If in real physical world objects are made of atoms and molecules, could we possibly create meshes consisting of those? And operate / perform calculations on them?

If a mesh is a digital representation of a physical object, we can assume different types of it dependent on the context or extent of refinement:

- polygon-mesh
- fea-mesh (classical FEA)
- afa-mesh (atomic fidelity mesh - consisting of atoms and molecules)

We can assume the possibility of doing the sim on afa-meshes.

We can assume having a perfect 1-to-1 afa-mesh of a physical object in sim, with a possibility to zoom-in/out with precision up to an atom / molecule.
