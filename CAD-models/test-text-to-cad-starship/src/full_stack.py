"""SpaceX Starship & Super Heavy Booster — Fully Stacked 121.3 m Launch Vehicle.

Root assembly model (`starship_full_stack`) combining:
- Super Heavy Booster (71.0 m tall with 1.8 m vented Hot-Stage Ring, 33 Raptor 2 SL engines,
  4 articulated waffle grid fins, 2 COPV chines, +Y raceway/BQD, and 2 Mechazilla catch pins)
- Starship Upper Stage (50.3 m tall, 9.0 m diameter 304L stainless hull + G1 tangent ogive nosecone,
  matte-black ceramic TPS windward heat shield + 360° stagnation nose cap, 3 Raptor SL + 3 Raptor Vacuum
  engines, 4 articulated aerodynamic flaps with windward aero-covers, Starlink payload door & RCS pods)

Kinematics:
- As-built state is `launch_stacked` (121.3 m tall, Starship seated flush atop Hot-Stage Ring at Z = 71,000 mm).
- `stage_separation`: LinearJoint (0 .. 14,000 mm along +Z) to inspect hot-staging & Ship's 6 Raptor engines.
- `grid_fin_1..4`: RevoluteJoints (-30° .. +30°) on Super Heavy's 4 asymmetric waffle grid fins.
- `aft_flap_stbd`, `aft_flap_port`, `fwd_flap_stbd`, `fwd_flap_port`: RevoluteJoints (0° .. 65° leeward)
  on Starship's 4 aerodynamic flaps.
"""

import build123d as bd
from cad import model
from cad.build123d import configuration_sequence, mechanism_state

from grid_fin import grid_fin
from lib import dims
from starship import (
    aft_flap_port,
    aft_flap_stbd,
    attach_starship_flaps,
    fwd_flap_port,
    fwd_flap_stbd,
    starship_core,
)
from super_heavy import attach_grid_fins, super_heavy_core


@model
def starship_full_stack():
    """SpaceX Starship fully stacked atop Super Heavy Booster (121.3 m tall, 9.0 m diameter)."""
    booster_core = super_heavy_core().shape
    fins = attach_grid_fins(booster_core, grid_fin().shape)

    ship_core = starship_core().shape

    # Connect Starship Upper Stage to Super Heavy Booster via axial hot-stage separation LinearJoint
    sep_axis = bd.Axis((0.0, 0.0, dims.Z_HSR_TOP), (0.0, 0.0, 1.0))
    sep_joint = bd.LinearJoint(
        "stage_separation",
        booster_core,
        axis=sep_axis,
        linear_range=(0.0, 14000.0),
    )
    bd.RigidJoint("stage_separation", ship_core, bd.Location(sep_axis.position))
    sep_joint.connect_to(ship_core.joints["stage_separation"], position=0.0)

    # Attach all 4 Starship aero flaps to ship_core (move upward with Starship during stage separation!)
    flaps = attach_starship_flaps(
        ship_core,
        aft_flap_stbd().shape,
        aft_flap_port().shape,
        fwd_flap_stbd().shape,
        fwd_flap_port().shape,
    )

    stack = bd.Compound(
        children=[
            booster_core,
            *fins,
            ship_core,
            *flaps,
        ],
        label="starship_full_stack",
    )

    bb = stack.bounding_box()
    assert abs(bb.min.Z - dims.Z_NOZZLE_EXIT) < 1.0, bb
    assert abs(bb.max.Z - dims.Z_SHIP_TOP) < 1.0, bb

    # Named mechanism states (presets in the viewer's Position panel)
    mechanism_state(
        stack,
        "launch_stacked",
        stage_separation=0.0,
        grid_fin_1=0.0,
        grid_fin_2=0.0,
        grid_fin_3=0.0,
        grid_fin_4=0.0,
        aft_flap_stbd=0.0,
        aft_flap_port=0.0,
        fwd_flap_stbd=0.0,
        fwd_flap_port=0.0,
    )
    mechanism_state(
        stack,
        "hot_stage_separation",
        stage_separation=7500.0,
        grid_fin_1=0.0,
        grid_fin_2=0.0,
        grid_fin_3=0.0,
        grid_fin_4=0.0,
        aft_flap_stbd=0.0,
        aft_flap_port=0.0,
        fwd_flap_stbd=0.0,
        fwd_flap_port=0.0,
    )
    mechanism_state(
        stack,
        "reentry_flight",
        stage_separation=12000.0,
        grid_fin_1=22.0,
        grid_fin_2=-22.0,
        grid_fin_3=-22.0,
        grid_fin_4=22.0,
        aft_flap_stbd=55.0,
        aft_flap_port=55.0,
        fwd_flap_stbd=55.0,
        fwd_flap_port=55.0,
    )

    # Eased mission-sequence showcase motion
    return configuration_sequence(
        stack,
        "mission_preview",
        [
            (0.0, "launch_stacked"),
            (3.0, "hot_stage_separation"),
            (6.5, "reentry_flight"),
            (10.0, "launch_stacked"),
        ],
    )


if __name__ == "__main__":
    starship_full_stack()
