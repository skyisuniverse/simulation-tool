# Approximate vs exact model

From conversation with Gemini on [Numerical Model Approximation](https://share.google/aimode/ZMwL0VzpCSw6twCQN)

> is exact model possible? how? what could help achieve it?

...

---

Based on the data in the current folder "**approximation**" we could (possibly) be able to reason better about how to achieve an exact model (if it's possible). Current FEA solutions make a tradeoff between several limiting conditions to achieve results, among which are limitations of simulation capabilities (e.g. finite element objects instead of continuous with infinite points), compute.

- What could be the best implementation of continuous objects in simulation? 
- Could it possibly help to achieve an exact model?
- What could the effect be if exact model is achieved?
- What kind of resources could be required for it? (compute, other?)

At some point, we can assume constructing physical objects from digital blueprints, what means that the simulated object could be a pre-requisute for a physical one. Its design and properties to be reproduced in the physical one.

We should probably not limit our imagination for the possible features with the currently existing compute, but rather assume feature-requests as pre-requisites for it. Given the desired precision and quality of the sim, and availability and cost of compute, we can possibly assume designing and producing it. (& scaling it to the extent, until it satisfies the level necessary for desired features). In an entirely automated (AI-fied ?), preferably commoditized way.
