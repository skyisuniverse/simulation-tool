# Agentic Manufacturing. Justification

Based on [texttocad](https://www.texttocad.dev/) ('s prototypical yet efficiently and autonomosly working capabilities) and my thoughts from [production-methodology.md](./production-methodology.md) it now becomes obvious that the next standard manufacturing approach will be based on [AI agents](https://github.com/mastra-ai/mastra) + [skills](https://www.skills.sh/).

It is now probably time to introduce the concept of manufacturing agents.

## Manufacturing agents

Manufacturing agents could be:

- [AI agents](https://github.com/mastra-ai/mastra) + 
- manufacturing tools +
  - 3D-Printers
  - CNC-Machines
  - DNA-Synthesizers (?)
- [skills](https://www.skills.sh/)

It imples that AI agents could be capable of controlling manufacturing tools in an automated way and perform automated process of manufacturing with AI agent skills. In the same way the AI agents [became an improvement over direct usage of LLMs](ideas/ai-agents/ai-agents.md) (e.g. by getting access to software tools), the **manufacturing agents** could become an improvement over AI agents (by getting access to hardware manufacturing tools). 

- access to manufacturing tools

## Evolution path towards Agentic Manufacturing

[text-to-cad's evolution-path-for-integrated-product-design](ideas/production/production-methodology/integrated-products/text-to-cad-evolution-path-for-integrated-product-design.md)

## Scope

Given the (possible?) scope (amount of parts) in a typical product, e.g.:

- [Tesla Model Y: 3,000 to 5,000 total individual parts](https://share.google/aimode/dEQgjMwtuEKeReAcV) (???)
- [Starship: tens of thousands of individual components](https://share.google/aimode/SLqFxpmCbBofAaHUV) (???)
- [Figure Robot: a couple hundred unique parts and a couple thousand parts in total](https://share.google/aimode/zUWwAzFdNrf80Uu5A) (???)

it makes sense that the entire stack will have to be evolved and fine-tuned / polished in connection with manufacturing tools, LLMs, AI agents, etc., in order to produce high-quality optimized components (e.g. similar to Tesla's bespoke metal die casting).

Most probably, solving a certain type of task for a particular domain (e.g. subdivision surfaces, dependency (component) graphs) will enable certain functionality for the entire domain.

## Machinery

What about [machinery](https://share.google/aimode/qAehf1qyhJxcfB689)? e.g.:

- [Injection Molding Machines](https://share.google/aimode/yTHrmYCnUn0YztPwW)
- [Die Casting Machines](https://share.google/aimode/4ogfe3hWhtTMp99Az)
- [Green Sand and Flaskless Molding Machines](https://share.google/aimode/b9K3WHh0GntnIksFP)
- [Foundry Handling and Special Systems](https://share.google/aimode/eBMmmKRb0yLh2zkG5)

Manufacturing systems like machinery seem to be too big and bulky. For now we focus on compact manufacturing methods and [miniaturization](ideas/production/production-methodology/miniaturization.md) as a path towards making **agentic manufacturing** compact and affordable on individual level.

## Stabilization. Phases

Based on [considerations-based-on-semi-truck-cad-design.md](ideas/production/production-methodology/considerations-based-on-semi-truck-cad-design.md) and [text-to-cad's evolution-path-for-integrated-product-design](ideas/production/production-methodology/integrated-products/text-to-cad-evolution-path-for-integrated-product-design.md) it seems that it will take some time until (open-source) industry grows and matures from currently existing text-to-cad experiments to full-fledged integrated product design flow. Similar to how JS ecosystem grew from vanilla JS, jQuery to frameworks, build systems, monorepos, etc. It makes sense that in order to enable **manufacturability** the first phase will require as much effort as possible in manufacturing automation. 

1. Enabling domain-specific features (frameworks (?)) from [evolution-path](ideas/production/production-methodology/integrated-products/text-to-cad-evolution-path-for-integrated-product-design.md)
2. Industry-wide standard blueprints for typical integrated products
    - Starship (?)
    - Falcon 9 (?) / Heavy (?)
    - Optimus / Figure (?)
    - Cybercab (?)
    - etc. (with time it could be any and all products), with Manufacturing Agents becoming standard manufacturing way for anything (with just the manufacturing tools differing, until we stabilize DNA-assemblers (?))

    Due to scope of undertaking, it seems that leading product blueprints will take as much time/effort for development as current leading js frameworks like next.js (4k contributors), turborepo (1k contributors), etc.

    Each product (and complex component) can be thought of as a framework. 


## Variability

Once the stabilization phase is done, when we get stable full-fledged frameworks for Agentic Manufacturing, we might move into a new era of abundance, with cheap production of anything. It makes sense that after stabilizing the core tech some attention could be driven towards perfecting the aesthetics, taste and fashion part of products. Enabling vast variability of products, designable in seconds by AI.

As an intermediate step there could be manual part of assembly of autonomously manufactured parts - until we perfect the process and automate entirely.
