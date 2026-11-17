#  text-to-cad

[texttocad.dev](https://www.texttocad.dev)

[earthtojake/text-to-cad](https://github.com/earthtojake/text-to-cad)

## Conversation with Gemini

Conversation with Gemini on [how text-to-cad works](https://share.google/aimode/AHV2X8cPeQO3sEoeL)

earthtojake/text-to-cad is an open-source plugin and MCP (Model Context Protocol) server that **lets AI coding agents design, analyze, and prepare physical products for manufacturing using Python code**. Instead of generating rough 3D meshes directly, it equips AI agents with specialized CAD workflows to write parametric Python scripts that compile into industry-standard engineering files.

## Core Workflow

- **Code-as-CAD Generation**: When you ask an AI agent (such as Claude, Cursor, Codex, or Gemini) for a part, it writes a Python script using [build123d](https://github.com/gumyr/build123d) and [OpenCASCADE](https://occt3d.com/open-cascade-technology/index.html).

- **Local Execution & Live Preview**: The agent runs the script locally through the `cad` **CLI** and **MCP server**, exporting standard **CAD formats** (STEP, STL, 3MF, GLB, or DXF) and displaying the 3D geometry live inside a built-in **CAD viewer**.

- **Agent Integration**: A single installer script sets up [uv](https://docs.astral.sh/uv) (a Python package manager) and automatically configures the necessary [skills](https://www.skills.sh) and **MCP server** across whatever AI agent apps are installed on your computer.

## Built-In Engineering Capabilities

Beyond basic 3D modeling, the repository bundles modular "skills" that connect your AI agent to open-source engineering tools:

- **Electronics & PCBs**: Generates and routes **KiCad** schematics and circuit boards, running electrical and design rule checks (**ERC**/**DRC**) before exporting fabrication files.
- **Simulation & Stress Testing**: Uses **CalculiX** to run finite element analysis (FEA) on parts or assemblies, calculating peak stress, safety factors, and deflection under load.
- **Manufacturing & Slicing**: Evaluates parts against rules for CNC machining, sheet metal bending, injection molding, or 3D printing. It can validate files for services like [SendCutSend](https://sendcutsend.com/) or slice models with [OrcaSlicer](https://www.orcaslicer.com/) to send directly to [Bambu Studio](https://bambulab.com/en/download/studio) ([github](https://github.com/bambulab/BambuStudio)).
- **Documentation & Rendering**: Projects 3D geometry into dimensioned 2D engineering drawings (PDFs with hidden lines and hole callouts) and uses **Blender** to produce GPU-rendered photorealistic stills or turntables.
- **Robotics**: Exports robot and environment descriptions in **URDF** (ROS), **SRDF** (MoveIt), and **MJCF** (MuJoCo) formats for motion planning and physics simulation.

If you'd like to explore further, I can help you with:

- **Setting it up** with a specific AI agent (like Claude Code, Cursor, or Gemini)
- **Walking through a sample workflow** (such as generating a 3D-printable part or running a stress check)

Which would be most helpful?

---

## Features

The text-to-cad plugin gives your agent local workflows to generate 3D models as STEP, GLB, STL or 3MF files, check them for manufacturing, draw them, and connect to 3D printing, sheet metal and CNC services. It works with any agent that supports plugins or skills.

### [Parts and assemblies](https://github.com/earthtojake/text-to-cad/blob/main/skills/cad/SKILL.md)

Models written as Python scripts with build123d and OpenCASCADE, exported as STEP, STL, 3MF or GLB, and as DXF profiles and flat patterns for laser and waterjet cutting, with joints and animations for mechanisms, and shown live in the CAD viewer.

### [Circuit boards](https://github.com/earthtojake/text-to-cad/blob/main/skills/pcb/SKILL.md)

KiCad schematics and boards, placed and routed, checked with ERC and DRC, reviewed before you order, and exported as fabrication files.

### [Manufacturing checks](https://github.com/earthtojake/text-to-cad/blob/main/skills/cad/SKILL.md#can-it-be-made)

Whether a part can be machined, cut and bent, molded or 3D printed, measured against the process's rules, and what to change where it cannot.

### [Stress checks](https://github.com/earthtojake/text-to-cad/blob/main/skills/fea/SKILL.md)

Whether a part or an assembly of bonded parts holds under its loads, solved with CalculiX: each part's peak stress, safety factor and how far it moves, drawn on the model.

### [Engineering drawings](https://github.com/earthtojake/text-to-cad/blob/main/skills/engineering-drawing/SKILL.md)

Dimensioned PDF sheets projected from the part's geometry: views, hidden lines, centre marks, hole callouts and a title block.

### [Renders](https://github.com/earthtojake/text-to-cad/blob/main/skills/render/SKILL.md)

Photoreal stills, turntables and films of a model with Blender, lit and framed in a Python script and run on the GPU, with a quick draft before each final.

### [Fabrication services](https://github.com/earthtojake/text-to-cad/blob/main/skills/sendcutsend/SKILL.md)

Checks DXF and STEP files against SendCutSend's guide before you upload them, and slices 3D prints with OrcaSlicer and sends them to Bambu Connect or Bambu Studio.

### [Robotics and simulation](https://github.com/earthtojake/text-to-cad/blob/main/skills/robot-simulation/SKILL.md)

Robot and world descriptions for simulation and motion planning: URDF for ROS, SRDF for MoveIt and MJCF for MuJoCo.
