"""Articulated SpaceX Mechazilla Tower (Starbase Orbital Launch Integration Tower - OLIT).

Scale: 1:100 (10.0 mm = 1.0 m; total height 1,500 mm = 150.0 m).
Coordinate system: Origin at center of tower footprint on launch pad ground plane (Z = 0),
+X pointing toward the Orbital Launch Mount & Starship centerline (X = 300 mm = 30.0 m),
-X toward the drawworks winch house, +Z vertical up.

Articulated mechanism:
  - carriage_lift (LinearJoint): Vertical travel along front twin I-beam guide rails (18 m -> 109 m).
  - chopsticks_open (gear_pair of arm_port & arm_stbd): Symmetric chopstick opening (-4 deg -> +36 deg).
  - trolley_slide (rack_and_pinion_pair of trolley_port & trolley_stbd): Synchronized booster-alignment
    trolleys sliding along each chopstick's damped catch rail (-70 mm -> +100 mm = 17 m stroke).
  - sqd_swing (RevoluteJoint): Ship Quick Disconnect arm swing from Starship aft port (0 deg) to
    stowed clear of carriage (-205 deg).
"""

import build123d as bd
from cad import model
from cad.build123d import (
    configuration_sequence,
    gear_pair,
    mechanism_state,
    rack_and_pinion_pair,
)

import spec as S
from carriage import carriage
from chopsticks import (
    catch_trolley_port,
    catch_trolley_stbd,
    chopstick_port,
    chopstick_stbd,
)
from crown import crown
from foundation import foundation
from sqd_arm import sqd_arm, sqd_outrigger
from tower import tower


@model
def mechazilla():
    """Master articulated Mechazilla Tower assembly with joints, states, and motion sequences."""
    # Fixed tower structure (ground link)
    found_s = foundation().shape
    tower_s = tower().shape
    crown_s = crown().shape
    outrigger_s = sqd_outrigger().shape
    fixed_tower = bd.Compound(
        children=[found_s, tower_s, crown_s, outrigger_s],
        label="tower_structure",
    )

    # Moving links (all built in their exact world as-built coordinates)
    carr_s = carriage().shape
    arm_p = chopstick_port().shape
    arm_s = chopstick_stbd().shape
    trol_p = catch_trolley_port().shape
    trol_s = catch_trolley_stbd().shape
    sqd_s = sqd_arm().shape

    # 1. Vertical carriage lift along front twin guide rails (+Z slide)
    lift_axis = bd.Axis((S.RAIL_FRONT_X, 0.0, S.CARRIAGE_Z_BUILT), (0, 0, 1))
    j_lift = bd.LinearJoint(
        "carriage_lift",
        fixed_tower,
        axis=lift_axis,
        linear_range=(S.CARRIAGE_TRAVEL_MIN, S.CARRIAGE_TRAVEL_MAX),
    )
    bd.RigidJoint("carriage_lift", carr_s, bd.Location(lift_axis.position))
    j_lift.connect_to(carr_s.joints["carriage_lift"], position=0.0)

    # 2. Port & Starboard chopstick vertical hinge pivots on carriage clevises
    hinge_z = S.CARRIAGE_Z_BUILT + S.ARM_ROOT_Z0_LOCAL
    j_port = bd.RevoluteJoint(
        "arm_port",
        carr_s,
        axis=bd.Axis((S.HINGE_X, S.HINGE_Y, hinge_z), (0, 0, 1)),
        angular_range=(S.ARM_ANGLE_MIN, S.ARM_ANGLE_MAX),
    )
    bd.RigidJoint("arm_port", arm_p, j_port.location)
    j_port.connect_to(arm_p.joints["arm_port"], angle=0.0)

    j_stbd = bd.RevoluteJoint(
        "arm_stbd",
        carr_s,
        axis=bd.Axis((S.HINGE_X, -S.HINGE_Y, hinge_z), (0, 0, 1)),
        angular_range=(-S.ARM_ANGLE_MAX, -S.ARM_ANGLE_MIN),
    )
    bd.RigidJoint("arm_stbd", arm_s, j_stbd.location)
    j_stbd.connect_to(arm_s.joints["arm_stbd"], angle=0.0)

    # 3. Synchronized sliding booster catch trolleys on each chopstick catch rail (+X slide)
    rail_z = hinge_z + 14.25
    trol_x = S.HINGE_X + S.TROLLEY_X_BUILT
    tp_axis = bd.Axis((trol_x, S.CATCH_RAIL_INNER_Y, rail_z), (1, 0, 0))
    j_tp = bd.LinearJoint(
        "trolley_port",
        arm_p,
        axis=tp_axis,
        linear_range=(S.TROLLEY_TRAVEL_MIN, S.TROLLEY_TRAVEL_MAX),
    )
    bd.RigidJoint("trolley_port", trol_p, bd.Location(tp_axis.position))
    j_tp.connect_to(trol_p.joints["trolley_port"], position=0.0)

    ts_axis = bd.Axis((trol_x, -S.CATCH_RAIL_INNER_Y, rail_z), (1, 0, 0))
    j_ts = bd.LinearJoint(
        "trolley_stbd",
        arm_s,
        axis=ts_axis,
        linear_range=(S.TROLLEY_TRAVEL_MIN, S.TROLLEY_TRAVEL_MAX),
    )
    bd.RigidJoint("trolley_stbd", trol_s, bd.Location(ts_axis.position))
    j_ts.connect_to(trol_s.joints["trolley_stbd"], position=0.0)

    # Virtual reference pinion on carriage to couple both sliding catch trolleys symmetrically
    bd.RevoluteJoint(
        "trolley_drive",
        carr_s,
        axis=bd.Axis((S.CARRIAGE_SPINE_X1, 0.0, rail_z), (0, 1, 0)),
        angular_range=(-180.0, 180.0),
    )

    # 4. Ship Quick Disconnect (SQD) arm swing hinge on Module 6 Starboard outrigger
    j_sqd = bd.RevoluteJoint(
        "sqd_swing",
        fixed_tower,
        axis=bd.Axis((S.SQD_HINGE_X, S.SQD_HINGE_Y, 826.0), (0, 0, 1)),
        angular_range=(S.SQD_SWING_MIN, S.SQD_SWING_MAX),
    )
    bd.RigidJoint("sqd_swing", sqd_s, j_sqd.location)
    j_sqd.connect_to(sqd_s.joints["sqd_swing"], angle=0.0)

    # Compose top-level articulated assembly
    assy = bd.Compound(
        children=[fixed_tower, carr_s, arm_p, arm_s, trol_p, trol_s, sqd_s],
        label="mechazilla",
    )

    # Couplings: symmetric chopsticks opening (deg) & synchronized catch trolley translation (mm)
    gear_pair(assy, "chopsticks_open", arm_port=1.0, arm_stbd=-1.0)
    rack_and_pinion_pair(
        assy,
        "trolley_slide",
        trolley_drive=1.0,
        trolley_port=1.0,
        trolley_stbd=1.0,
    )

    # Named Mechanism States
    mechanism_state(
        assy,
        "prelaunch_fueling",
        carriage_lift=-300.0,
        chopsticks_open=0.0,
        trolley_slide=0.0,
        sqd_swing=0.0,
    )
    mechanism_state(
        assy,
        "launch_clearance",
        carriage_lift=-300.0,
        chopsticks_open=34.0,
        trolley_slide=-55.0,
        sqd_swing=-205.0,
    )
    mechanism_state(
        assy,
        "catch_approach",
        carriage_lift=440.0,
        chopsticks_open=22.0,
        trolley_slide=0.0,
        sqd_swing=-205.0,
    )
    mechanism_state(
        assy,
        "booster_caught",
        carriage_lift=220.0,
        chopsticks_open=0.0,
        trolley_slide=0.0,
        sqd_swing=-205.0,
    )
    mechanism_state(
        assy,
        "ship_stacking_high",
        carriage_lift=550.0,
        chopsticks_open=0.0,
        trolley_slide=0.0,
        sqd_swing=-205.0,
    )
    mechanism_state(
        assy,
        "stowed",
        carriage_lift=-320.0,
        chopsticks_open=0.0,
        trolley_slide=-65.0,
        sqd_swing=-205.0,
    )

    # Playable Configuration Sequences (motions in the CAD Viewer)
    configuration_sequence(
        assy,
        "booster_catch",
        [
            (0.0, "catch_approach"),
            (
                2.5,
                {
                    "carriage_lift": 420.0,
                    "chopsticks_open": 0.0,
                    "trolley_slide": 0.0,
                    "sqd_swing": -205.0,
                },
            ),
            (
                5.5,
                {
                    "carriage_lift": -280.0,
                    "chopsticks_open": 0.0,
                    "trolley_slide": 0.0,
                    "sqd_swing": -205.0,
                },
            ),
            (
                7.5,
                {
                    "carriage_lift": -280.0,
                    "chopsticks_open": 0.0,
                    "trolley_slide": 65.0,
                    "sqd_swing": -205.0,
                },
            ),
            (10.0, "catch_approach"),
        ],
    )
    configuration_sequence(
        assy,
        "launch_sequence",
        [
            (0.0, "prelaunch_fueling"),
            (3.0, "launch_clearance"),
            (5.0, "launch_clearance"),
            (8.0, "prelaunch_fueling"),
        ],
    )
    configuration_sequence(
        assy,
        "starship_stacking",
        [
            (0.0, "stowed"),
            (
                2.0,
                {
                    "carriage_lift": -300.0,
                    "chopsticks_open": 18.0,
                    "trolley_slide": 70.0,
                    "sqd_swing": -205.0,
                },
            ),
            (
                3.5,
                {
                    "carriage_lift": -300.0,
                    "chopsticks_open": 0.0,
                    "trolley_slide": 0.0,
                    "sqd_swing": -205.0,
                },
            ),
            (6.5, "ship_stacking_high"),
            (
                8.0,
                {
                    "carriage_lift": 550.0,
                    "chopsticks_open": 20.0,
                    "trolley_slide": 0.0,
                    "sqd_swing": -205.0,
                },
            ),
            (10.5, "stowed"),
        ],
    )

    bb = assy.bounding_box()
    assert abs(bb.min.Z - 0.0) < 1e-4, bb
    assert abs(bb.max.Z - S.LIGHTNING_MAST_TOP_Z) < 1e-4, bb
    return assy


if __name__ == "__main__":
    mechazilla()
