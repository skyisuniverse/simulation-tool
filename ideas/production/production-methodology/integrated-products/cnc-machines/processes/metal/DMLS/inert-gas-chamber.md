# Inert gas chamber

From [DMLS-Direct-Metal-Laser-Sintering.md](ideas/production/production-methodology/integrated-products/cnc-machines/processes/metal/DMLS/DMLS-Direct-Metal-Laser-Sintering.md)

> **Direct Metal Laser Sintering (DMLS)** is a metal 3D printing (powder bed fusion) process that uses a high-powered laser to fuse fine metal powder layer by layer from a 3D CAD model inside an **inert gas chamber**.

Conversation with Gemini on [What is an inert gas chamber?](https://share.google/aimode/37DGJPhrsd4aR91rI)

> What is an inert gas chamber?

An **inert gas chamber** is the sealed, airtight enclosure inside a DMLS printer where the build takes place, filled with a non-reactive gas—typically **argon** or **nitrogen** — instead of regular air.


## Why Regular Air Cannot Be Used

- **Instant oxidation**: At the extreme temperatures of the laser melt pool, molten metal reacts immediately with oxygen in the air, forming brittle oxide layers that prevent neighboring metal tracks from bonding properly.
- **Porosity and weakness**: Trapped oxygen, nitrogen, and moisture from ambient air create gas bubbles (pores) and brittle compounds inside the metal, severely weakening the part.
- **Fire and explosion hazard**: Fine, airborne metal powders (especially titanium and aluminum) are highly combustible when suspended in oxygen-rich air and exposed to an ignition source like a high-powered laser.

## How the Chamber Works

- **Purging before printing**: Once the build plate is loaded and the chamber door is sealed, the machine pumps out ambient air and floods the chamber with inert gas until oxygen sensors confirm levels have dropped below a strict threshold (often **under 100 to 1,000 parts per million**, or `< 0.1%` oxygen).

- **Choosing the right gas**:
	- **Argon**: Completely non-reactive even at extreme temperatures; required for reactive metals like **titanium (Ti6Al4V)** and **aluminum**.
	- **Nitrogen**: More economical and commonly used for **stainless steels**, **tool steels**, and **cobalt-chrome** (though unsuitable for titanium, which reacts with nitrogen at high heat to form brittle titanium nitride).

- **Continuous gas circulation (laminar flow)**: During printing, a steady stream of filtered inert gas sweeps horizontally across the powder bed. This blows away vaporized metal fumes (*plume*) and molten droplets (*spatter*) so they do not block the laser or contaminate the powder bed, while a closed-loop filter traps the soot and recirculates the clean gas.

Would you like to know more about 

- **powder handling and safety** outside the chamber, 
- or how **laser parameters and scan strategies** control the melt pool inside it?
