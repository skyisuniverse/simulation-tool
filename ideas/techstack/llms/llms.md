# LLMs

## LLM considerations

The LLM landscape is going to be constantly changing, meaning that new models and new versions of them are going to appear continuously as teams ship them. For us at least it means:

- the **necessity of continuously checking / iterating on LLMs** (and **tooling**) and their suitability / quality for the agentic design / manufacturing domain
- timely selection of the best model / tooling for the task

Two conversations with Gemini below show it.

## Part 1

From talk with Gemini on **gemini neon argon hydrogen (Gemini LLMs)**

Gemini 4 [Neon](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-neon/), Argon, and Hydrogen (alongside Carbon) are Google's element-named AI models in the Gemini 4 lineup, each tuned for different speed, reasoning, and cost trade-offs.

[Introducing Gemini 4 Neon](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-neon/)

[Google's Gemini 4 Lineup Explained: Argon, Carbon, Hydrogen, Neon](https://www.mindstudio.ai/blog/google-gemini-4-model-lineup)

[Google Gemini 4 Neon vs Carbon vs Hydrogen vs Argon](https://www.youtube.com/watch?v=pBWi89wd188)

According to the Google Blog, **Neon** balances depth and efficiency for complex coding, analytical reasoning, and production workflows. As noted in a [Medium](https://medium.com/data-science-in-your-pocket/gemini-4-neon-vs-carbon-vs-hydrogen-vs-argon-cd5377c1f812) breakdown of the lineup, Neon has become the primary middle-ground choice while Hydrogen handles high-volume speed and Argon is phasing out of the Gemini app.


### Model Roles & Pricing

- **Gemini 4 Neon** (`gemini-4-neon`): Sits between Hydrogen and Carbon for complex software engineering, tool-heavy tasks, and analytical workflows. Adapted from Carbon with a 1M unified context window and default high thinking (supports xhigh). Priced at $3 / 1M input tokens and $15 / 1M output tokens (paid tier).

- **Gemini 4 Argon**: An earlier generalist/frontier model for complex engineering, science, legal, and multimodal tasks. Removed from the Gemini app picker when Neon launched, though still accessible via the API. Priced at $2 / 1M input tokens and $10 / 1M output tokens, scheduled to rise to $4 / 1M input and $20 / 1M output on December 1, 2026

- **Gemini 4 Carbon**: Kept for the hardest, longest-horizon architecture, deep debugging, and high-stakes security/research problems.

Are you choosing a model for a **specific workload** (such as coding, agents, or analysis) or **migrating an existing setup** from Argon or Carbon?

## Part 2

> which of those models is the best choice for generating a CAD model of a rocket (SpaceX Starship) with text-to-cad ( https://www.texttocad.dev/ ) ?

Gemini 4 Neon (`gemini-4-neon`) is the best choice here.

Because `text-to-cad` generates models by writing **Python scripts using** `build123d` **and OpenCASCADE** and running iterative tool workflows (compiling geometry, viewing renders, and fixing build errors), your model needs strong spatial reasoning, multi-step 3D math, and reliable tool calling without burning excessive tokens on every minor revision.


### Why Gemini 4 Neon Wins for Starship CAD

- **Complex 3D Geometry & Spatial Math**: A SpaceX Starship model isn't a simple primitive—it requires lofted ogive nosecones, angled forward/aft flaps with hinges, grid fins (if including Super Heavy), Raptor engine bells, and a multi-part assembly. Neon is adapted from Carbon specifically for complex software engineering and analytical reasoning, giving it the spatial and algebraic accuracy needed to write valid `build123d` booleans, lofts, and fillets without failing OpenCASCADE kernel checks.
- **Agentic Tool-Loop Efficiency**: `text-to-cad` works inside an agent loop (writing code, running checks, inspecting live viewer output, and tweaking parameters). Neon's balance of speed and `high/xhigh` thinking lets your agent iterate through geometric bugs much faster and at a lower cost than Carbon, while avoiding the frequent syntax or topology errors Hydrogen can make on complex assemblies.

### How the Other Models Compare for This Task

| Model | Suitability for Starship CAD | Why |
| :--- | :--- | :--- |
| **Gemini 4 Neon** | **Best Overall** | Ideal balance of deep spatial/Python reasoning and fast, cost-effective agentic iteration. |
| **Gemini 4 Carbon** | **Runner-Up (For Extreme Detail)** | Worth switching to only if you are modeling intricate internal plumbing, a full 33-engine Raptor cluster, or articulated flap joints that trip up Neon. |
| **Gemini 4 Hydrogen** | **Good for Fast Tweaks** | Great for quick dimension changes, simple brackets, or early rough block-outs, but more prone to OpenCASCADE boolean/fillet failures on complex curved surfaces. |
| **Gemini 4 Argon** | **Skip** | Being phased out of the Gemini app, outperformed by Neon on coding/tool workflows, and its API price doubles on Dec 1, 2026. |


### Recommended Workflow

1. **Start with Gemini 4 Neon** (with default `high` thinking, or `xhigh` for the initial nosecone/flap lofting) to generate the core `build123d` assembly (hull, nosecone, flaps, engine skirt).
2. **Switch to Hydrogen** if you want cheap, rapid iterations on simple adjustments like wall thickness, 3D-print tolerances, or exporting STL/3MF slices.
Are you aiming for a **single-piece display model** (e.g., for 3D printing) or a **multi-part mechanical assembly** (with separate Starship upper stage, Super Heavy booster, and articulated flaps)?
