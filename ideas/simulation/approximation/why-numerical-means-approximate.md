# Why "Numerical" Means "Approximate"

From conversation with Gemini on [Numerical Model Approximation](https://share.google/aimode/ZMwL0VzpCSw6twCQN)

>> From https://sdcverifier.com/structural-engineering-101/meshing-in-finite-element-analysis
>>
>> In Finite Element Analysis (FEA), mesh plays a crucial role in transforming real-world structures into a numerical model that can be analyzed.
>
> Does "numerical" mean approximate?

**Yes, in the context of Finite Element Analysis (FEA), a "numerical model" is inherently an approximate model**. While the word "numerical" literally means calculating with numbers rather than algebraic symbols, the underlying process relies on mathematical approximations to solve complex engineering problems.

## Why "Numerical" Means "Approximate" in FEA

- **Discretization**: Real-world structures are continuous with infinite points. A numerical model breaks the structure down into a finite number of small shapes (elements and nodes). This process of cutting infinity into finite pieces creates an approximation.
- **Simplified Calculus**: The software converts exact differential equations (which describe continuous physics) into a system of simpler algebraic equations that a computer can solve using arithmetic.
- **Mesh Dependency**: Because it is an approximation, the accuracy depends on the mesh size. A finer mesh yields an answer closer to the true physical reality, but it never becomes a mathematically perfect, exact solution.

## Analytical vs. Numerical Solutions


| Feature | Analytical Solution | Numerical Solution (FEA) |
| :--- | :--- | :--- |
| **Method** | Exact mathematical formulas | Computer-driven numerical algorithms |
| **Accuracy** | 100% exact | Approximate (converges toward exact) |
| **Geometry** | Limited to very simple shapes (e.g., a perfect cylinder) | Can analyze highly complex, irregular structures |

If you are working on a specific FEA problem, tell me:

- What **software** you are using?
- What **type of structure** you are analyzing?

I can share tips on how to perform a **mesh convergence** study to ensure your approximations are highly accurate.

----

## Algebraic symbols

From conversation with Gemini on [Algebraic symbols](https://share.google/aimode/en0IGTq6Wcp0ihIJV)

> While the word "numerical" literally means calculating with numbers rather than algebraic symbols, the underlying process relies on mathematical approximations to solve complex engineering problems.

What are algebraic symbols in this context?

In this context, **algebraic symbols are the variables and letters (like \(x, y, F, M, E,\) or \(I\)) used to write general mathematical formulas**.

When you solve an engineering problem analytically, you manipulate these letters using algebra and calculus to find an exact, universal equation before plugging in any final numbers.

## The Difference in Practice

- **Algebraic/Analytical Approach**: You work with symbolic equations. For example, to find the maximum deflection (\(\delta \)) of a simple cantilever beam with a force at the end, you use the exact symbolic formula:

  ![](../../../img/exact-symbolic-formula-example.png)

  Here, **\(F\)** is force, **\(L\)** is length, **\(E\)** is material stiffness, and **\(I\)** is geometry. The letters represent variables, and the relationship is mathematically perfect.

- **Numerical Approach (FEA)**: A computer cannot manipulate abstract symbols to "invent" a new formula for a complex shape. Instead, it bypasses the need for a general symbolic formula. You must feed it specific numbers from the start (e.g., \(F = 500\), \(L = 2.5\), \(E = 210,000,000\)). The computer then plugs these numbers into giant matrices and uses basic arithmetic (addition, subtraction, multiplication) to calculate a specific numerical answer for every single node.

In short, algebraic symbols allow humans to find a generalized, **exact formula**, while numerical methods allow computers to calculate a specific, **approximate number** for shapes too complex for formulas.

Would you like to see a quick example of how **FEA turns a differential equation into a matrix of numbers**, or are you focusing on a specific **structural engineering concept** right now?

---

## Examples: difference between Algebraic/Analytical Approach and Numerical Approach (FEA)

From conversation with Gemini on [Difference between Algebraic/Analytical Approach and Numerical Approach (FEA) (examples)](https://share.google/aimode/RRzsRai59XYxMJPTE)

Here are three distinct engineering examples comparing the **Algebraic/Analytical Approach** (exact formulas using symbols) with the **Numerical Approach** (approximate computer calculations using numbers).

### Example 1: Stress in a Thick-Walled Pressure Vessel

Imagine a high-pressure scuba tank or a hydraulic cylinder. Engineers need to know the internal stress to prevent the tank from bursting.

- **Algebraic/Analytical Approach**: You use Lamé's equations, which are exact formulas derived from theory. To find the stress (\(\sigma \)) at any radius (\(r\)) inside the cylinder wall, you manipulate symbols:

  ![](../../../img/exact-symbolic-formula-example-2.png)
  
  *You have a single, perfect symbolic equation that works for any cylinder radius, internal pressure (\(P_{i}\)), or external pressure (\(P_{o}\)).*

- **Numerical Approach (FEA)**: If the tank has irregular cooling fins, a nozzle welded to the side, or a changing wall thickness, Lamé's algebraic formula completely breaks down.

  The FEA software divides the tank wall into thousands of tiny 3D solid brick elements. It does not know Lamé’s formula. Instead, it takes explicit numbers (e.g., Pressure = \(15.5\) MPa, Radius = \(0.12\) m) and solves millions of basic arithmetic equations simultaneously to tell you the specific stress value at every single corner of those tiny bricks.


### Example 2: Heat Dissipation in a Microchip (Thermal Analysis)

Imagine a square computer processor generating heat, and you need to find the temperature distribution across its surface.

- **Algebraic/Analytical Approach**: You solve **Fourier's Law of Heat Conduction**, a partial differential equation. For a perfectly uniform, flat, 2D plate with constant heat applied to one edge, calculus yields a complex symbolic series solution involving sines and cosines:

  ![](../../../img/exact-symbolic-formula-example-3.png)

  This algebraic formula gives the mathematically exact temperature at any precise coordinate \((x,y)\).

- **Numerical Approach (FEA/Thermal)**: Real microchips are not uniform; they have copper circuits, silicon layers, and tiny transistors grouped in patches.
The FEA software blankets the chip layout with a 2D mesh of triangles. It looks at the individual numbers (e.g., Thermal Conductivity = \(149\) W/m·K) and calculates how much heat passes from Node A to Node B using basic algebraic grid approximations (like the Finite Difference or Finite Element method). The output is a color-coded temperature map made of fixed numerical data points.

### Example 3: Torsional Twist of a Structural Shaft

Imagine a steel drive shaft in a car being twisted by the engine's torque (\(T\)). You need to know how many degrees it will rotate.

- **Algebraic/Analytical Approach**: For a perfectly solid, round bar, you use the classic **torsion formula**:

  ![](../../../img/exact-symbolic-formula-example-4.png)

  By manipulating these symbols (\(\theta \) = twist angle, \(L\) = length, \(G\) = shear modulus, \(J\) = polar moment of inertia), you get a universal, exact relationship. If you double the length (\(L\)), the twist exactly doubles.

- **Numerical Approach (FEA)**: If the drive shaft is splined (has gear-like teeth cut into it to lock into a transmission), computing the geometric symbol "\(J\)" becomes practically impossible.

  The FEA software cuts the splined shaft into a mesh of thousands of 3D tetrahedral elements. It takes the concrete numbers (Torque = \(350\) N·m) and uses matrix algebra to calculate the microscopic displacement of every node, summing them up to give you the total twist angle as a final decimal number (e.g., \(1.42^{\circ }\)).

## Summary Checklist

| If the scenario involves... | The Algebraic Approach uses... | The Numerical Approach (FEA) uses... |
| :--- | :--- | :--- |
| **Geometry** | Perfect shapes (circles, rectangles, straight lines) | Irregular shapes (car bumpers, brackets, welds) |
| **The Math** | Calculus, derivatives, and symbol manipulation | Matrices, arithmetic, and discrete grids |
| **The Result** | A reusable formula | A specific set of numbers |

Are any of these specific physics domains— **stress/structural**, **thermal**, or **fluid dynamics** — related to the project or concept you are studying right now?

-----

## Continuity

From conversation with Gemini on [Continuum Hypothesis (simplification)](https://share.google/aimode/j7uobNXi7xlSwz8u8)

> Discretization: Real-world structures are continuous with infinite points.

Is this statement true? Or is it simplification of the underlying atomic/molecular structure of a real-world physical object to fit it into the simplified methods of FEA?

---

You hit on a profound distinction: **The statement is a macroscopic simplification known as the "continuum hypothesis," rather than a microscopic truth.**

In reality, physical objects are made of discrete atoms and molecules with empty space between them. However, engineering and Finite Element Analysis (FEA) do not model atoms; they model a mathematical abstraction called **continuum mechanics**.

Here is how these layers of simplification actually work:

### 1. The First Simplification: Real World -> Continuum Mechanics

At the atomic scale, matter is discrete. But tracking the position and forces of trillions of individual atoms in a simple steel bracket is computationally impossible and practically useless for an engineer.

To solve this, physics uses the **continuum hypothesis**:

- It **smooths out** the atomic gaps.
- It assumes matter is completely unbroken and continuous down to an infinitely small point.
- This allows us to use calculus (differential equations) to describe stress, fluid flow, and heat.

So, when we say "real-world structures are continuous with infinite points," we are talking about the *engineering model* of the world, not the **actual quantum reality**.

### 2. The Second Simplification: Continuum Mechanics -> FEA Mesh

This leads to an ironic loop of simplification:

1. **Nature**: Discrete (made of distinct atoms).
2. **Calculus/Theory**: Continuous (smoothed into infinite points so humans can write equations).
3. **FEA**: Discrete (chopped back down into finite elements so computers can calculate it).

```
[ Real Matter ]       [ Continuum Model ]       [ FEA Mesh ]
 Discrete Atoms  -->   Infinite Points    -->  Finite Elements
 (True Reality)       (Calculus Theory)        (Computer Solvable)
```

### Why FEA Doesn't Just Use the Atomic Structure

You might wonder why we don't just skip the middleman and model the atoms directly.

- **Scale**: A single drop of water contains about \(10^{21}\) atoms. A computer cannot solve a matrix of that size.

- **Relevance**: Individual atomic behaviors (like quantum vibrations) average out at the macroscopic level. **The continuous approximation introduces negligible error for everyday engineering scales** (anything larger than a micrometer).

In short, FEA chops up a *continuous mathematical fiction* because that fiction is the most accurate, efficient way to predict how a discrete physical reality will behave.

Are you exploring this for a **physics** perspective, or are you trying to understand the **limits of FEA accuracy** (like when analyzing nanomaterials or microscopic cracks)?


---

> Discretization: Real-world structures are continuous with infinite points.
>
> Is this statement true? Or is it simplification of the underlying atomic/molecular structure of a real-world physical object to fit it into the simplified methods of FEA?

If the second, then we might assume **atomic fidelity** as the desired flavor of app (**AFA - Atomic Fidelity Analysis**?) (without simplification) along with classical FEA.
