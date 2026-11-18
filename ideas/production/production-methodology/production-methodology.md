# Production methodology

- [ ] Describe the production methodology of:
  - [ ] [rockets](./rockets/rockets.md)
  - [ ] [cars](./cars/cars.md)
  - [ ] [trucks](./trucks/trucks.md)
  - [ ] [robots](./robots/robots.md)
  - [ ] [satellites](./satellites/satellites.md)

With [text-to-cad](../../techstack/text-to-cad/text-to-cad.md) (from design to production).

---

We could theoretically design the entire product with AI:

1. **Design the product in text** (conversations with AI (?))
    1. Create a **list of all components** (in a series of conversations with AI)
    2. Describe the **functionality of each component**
    3. Describe functionality & characteristics of the **integrated product**.
2. **Create a** simulation-testing- and production- ready **3D CAD design of each component** with text-to-cad
    1. Run simulation tests for each component
3. **Create an integrated 3D CAD design of the entire product** (with text-to-cad?)
    1. Run simulation tests of the entire integrated product with (with text-to-cad?)


4. **Manufacture each component** of the product **from 3D CAD Design** (with 3D Printing? CNC-machining?)
5. **Test each component in real physical conditions** (engines, flaps, tanks, etc.)
6. **Assemble physical product from the components**
7. **Test integrated product** (until the entire blueprint & process are well-tested & standardized)
8. **Use the product** according to its operation goals

---

1. **Product specification** 

    ([AI agent skill](https://www.skills.sh/)? similar to text-to-cad's [CAD modeling and inspection](https://github.com/earthtojake/text-to-cad/blob/main/skills/cad/SKILL.md), [PCB design](https://github.com/earthtojake/text-to-cad/blob/main/skills/pcb/SKILL.md))

    - **list of components**
      - (each) component functionality description
      - (each) component **techspecs**
    - **integrated product**
      - integrated product functionality description
      - integrated product **techspecs**
2. **3D CAD Design**
    - simulation-testing- and production- ready 3D CAD design:
      - **of each component**
      - **of integrated product**

3. **Simulation tests**

    ([AI agent skill](https://www.skills.sh/)? e.g. text-to-cad's [Manufacturing checks](https://github.com/earthtojake/text-to-cad/blob/main/skills/cad/SKILL.md#can-it-be-made), [Stress checks](https://github.com/earthtojake/text-to-cad/blob/main/skills/fea/SKILL.md), etc.?)

    - **of each component**
    - **of integrated product**

4. **Manufacture each component** of the product **from 3D CAD Design**

5. **Test each component in real physical conditions**

6. **Assemble physical product from the components**

7. **Test integrated product**

8. **Use the product**

Important: [testing of components / integrated products](../testing-methodology/testing-methodology.md) assumes existence of the testing infra (devices / software) in real world. Which means we'd have to be able to generate and affordably produce it as well.
