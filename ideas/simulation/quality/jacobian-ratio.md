# Jacobian Ratio

From conversation with Gemini on [Jacobian Ratio](https://share.google/aimode/JBuwduLoJBRauM0Yt)

The **Jacobian ratio** is **a quality metric in Finite Element Analysis (FEA) that measures how much a real-world distorted element deviates from an ideal, undistorted reference shape**.

## How It Is Calculated

- **Jacobian Determinant** (\(R_{J}\)): At sampling locations (such as corner nodes or Gauss quadrature points), the determinant of the Jacobian matrix is computed. It represents the scaling factor or volume/area mapping between the element's local (parametric) coordinate space and global (real) space.
- **Ratio Formula**: The Jacobian ratio is generally calculated as the **minimum \(R_{J}\) divided by the maximum \(R_{J}\)** sampled across the element, or compared against an ideal reference element value.

## Interpretation and Quality Thresholds


| Jacobian Ratio Value | Element Condition | Description & Action |
| :--- | :--- | :--- |
| **1.0** | **Ideal** | A perfect, undistorted element (e.g., a square or regular hexahedron with 90-degree angles). |
| **> 0.5 to < 1.0** | **Acceptable / Good** | Minor distortion; safe for analysis in most critical and non-critical regions. |
| **≤ 0.5 (Warning)** | **Poor Quality** | Significant distortion; can introduce numerical errors or warning flags in FEA solvers. |
| **≤ 0 (Negative or Zero)** | **Invalid / Tangled** | The element has inverted, collapsed, or folded inside out. The simulation will typically fail or produce garbage results; **remeshing is required**. |

*(Note: Depending on the specific FEA software—such as Ansys, Abaqus, or SolidWorks—scaling conventions can vary, with some bounded between -1 and 1 and others using higher positive multiplier scales.)*

## Key Methods

- **Corner Nodes vs. Gauss Points**: Calculating the Jacobian ratio using corner nodes is generally more restrictive, whereas evaluating Gauss points tests internal integration points and may yield different threshold behaviors.
- **Why It Matters**: If the Jacobian determinant drops to zero or turns negative, the geometric transformation breaks down, leading to solver crashes or negative stiffness matrix errors.

... mesh diagnostics ...
