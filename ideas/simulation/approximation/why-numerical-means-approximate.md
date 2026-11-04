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


----

## Algebraic symbols

> what are algebraic symbols?

> how is calculating with algebraic symbols different from calculating with numbers?

-----

## Continuity

> Discretization: Real-world structures are continuous with infinite points.

Is this statement true? Or is it simplification of the underlying atomic/molecular layer to fit it into the simplified metods of FEA?

If the second, then we might assume **atomic fidelity** as the desired flavor of app (**AFA - Atomic Fidelity Analysis**?) (without simplification) along with classical FEA.
