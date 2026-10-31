# Requirements for articles

Consider creating (introductory and deeper) articles for a knowledge base for the Simulation domain (including physics, chemistry, engineering simulation, etc.) in context of (3D) engineering simulation tool. 

Articles should:

- be easily understandable
- first provide high-level general understanding that makes it easy to understand the essence of the phenomenon
- preferably have a low entry barrier for people who don't posses domain-specific knowledge
- not be overloaded with terms that conceal the essence of the phenomenon with complex terms that are non-self-evident (e.g. fluid motion / Navier-Stokes)
- domain-specific terms can be present if they don't make articles less readable and more difficult for reasoning
- could be nice if clarifications and domain-specific scientific terms are provided alongside generic surface-level (easily digestible) knowledge (high-level general understanding) (in expandable way - could be in parentheses, tooltips or somehow else)
- be neutral in tone (not have any intimidating content)

----

## Current inefficient flow  

Based on example of [finite-element-method](./todo/rewrite-articles/terms-and-definitions/finite-element-method.md), currently the experience of reading a knowledge base article and understanding the topic is very error-prone.

For any user without significant knowledge in the given domain, the steps for understanding the topic include:

- initial attempt to read an article
- formulation of the topic context and (continuously) storing it in memory
- seeing a lot of new unknown domain-specific terms
- inability to understand the meaning of the terms at once
- opening of the terms' articles in new tabs, reading new definitions and trying to understand those
- (partial) alleviation of confusion if the new term's definition in the opened articled was easy to digest and understand, clarifying the understanding of the initial article **OR** magnification of confusion if it wasn't 
- attempt to optimize the flow by: 
  - labeling undigested terms for later TBD (to-be-done) & writing down
  - storing them (continuously) in memory
- continuation of an attempt to read an article
- confusion for not being able to understand the topic despite of having consumed a certain amount of information
- Repetition of attempt (s) to read article again (usually after visiting new terms' articles and forming basic understanding of those)
- Building up the (usually partial) knowledge-tree of an article including its context & related terms
  - Partial because a lot of terms aren't easy to understand and require opening new terms and understand those first, contributing to a chain of confusion
- Confusion related to
  - chaotic unsystematic presentation of information, which includes:
    - Jumping from one logical domain to another
    - Overloading with low-level details that don't contribute to overall understanding but slow down by re-directing brain processing power (vertical cognitive overload)
  - width of covered topics (one paragraph can include 16 topics, e.g. [finite-element-method#2nd-paragraph](./todo/rewrite-articles/terms-and-definitions/finite-element-method.md#2nd-paragraph)) (horizontal cognitive overload)
- Processing of unknown terms
- Understanding of unknown terms
- Repetition of the entire cycle
- Clarification of understanding of the article
- Re-writing the article for optimized clarity, consistency, understandability and systematic style of presentation

**15 steps from initial attempt to read an article to actually understanding it**.

(Not even to mention building tools on top of / with such understanding)

## Preferable desired flow

- initial attempt to read an article
- instant clear understanding of it

**2 steps from reading an article to understanding it**.

- optional expendables to dive deeper into the subject matter, details, terms and any kind of domain specificity if the user wants to
