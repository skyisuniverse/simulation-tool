# Build platform

From [DMLS-Direct-Metal-Laser-Sintering.md](ideas/production/production-methodology/integrated-products/cnc-machines/processes/metal/DMLS/DMLS-Direct-Metal-Laser-Sintering.md)

> - **Powder layering**: A recoater spreads a thin layer of metal powder (typically tens of micrometers thick) across a **build platform**.

From conversation with Gemini on [What is a build platform?](https://share.google/aimode/7wU7sQGsBw8bFRhU7)

A **build platform** (also called a **build plate** or **substrate**) is the heavy, flat metal slab inside the printer onto which the part is printed, welded, and supported throughout the entire DMLS process.


## How It Works

- **Vertical movement**: Mounted on a precision Z-axis piston, the platform drops down by one exact layer thickness (e.g., 30 micrometers) after every laser scan so the recoater can spread the next layer of powder on top.
- **Metallurgical anchoring**: The laser melts the very first layer of powder directly into the build platform itself, welding the part (or its support structures) to the plate so it cannot shift or curl upward during printing.
- **Heat sink**: Because the platform is a thick block of solid metal—often heated from underneath to reduce thermal shock—it conducts intense heat away from the laser melt pool during the build.


## Key Characteristics

- **Material compatibility**: The build plate is usually made from the **same or a metallurgically compatible metal** as the powder being printed (e.g., a steel plate for stainless steel, a titanium plate for titanium) so the first layer bonds cleanly without forming brittle intermetallic cracks.
- **Precision flatness**: It is surface-ground to be dead flat and parallel to the recoater blade, ensuring the initial layer of powder is uniform across the entire print area.
- **Reusable lifecycle**: After the build finishes and undergoes stress-relief heat treatment, parts are cut off the plate—usually via **Wire EDM (Electrical Discharge Machining)** or a bandsaw—and the plate is resurfaced (ground flat again) so it can be reused for future jobs.

Would you like to learn more about 

- **support structures** (how parts are anchored to the build platform) 
- or **post-processing** (how parts are removed and finished after printing)?
