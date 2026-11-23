"""Tesla Roadster (2nd Generation) — full parametric CAD assembly with kinematics.

Mechanisms & poses
------------------
  - ``door_left`` / ``door_right``: angled butterfly doors (0 to 56 deg)
    carrying frameless door glass and aerodynamic wing mirrors.
  - ``active_spoiler``: deployable rear aero wing on twin titanium actuators (0 to 85 mm).
  - ``targa_roof``: removable panoramic glass Targa roof panel lift (0 to 320 mm).

Named states: ``cruise`` (as built), ``track`` (active rear wing deployed),
``open_top`` (Targa roof lifted), ``showroom`` (butterfly doors open + wing deployed).
Configuration sequence: ``showcase`` (smooth 6 s showroom presentation).
"""

from __future__ import annotations

import build123d as bd
from cad import model
from cad.build123d import configuration_sequence, mechanism_state, memo

from lib import aero as aero_lib
from lib import body as body_lib
from lib import chassis as chassis_lib
from lib import glazing as glazing_lib
from lib import interior as interior_lib
from lib import lighting as lighting_lib
from lib import wheels_brakes as wheels_lib
from lib.palette import group
from lib.surfaces import DOOR_FRONT_X, SPOILER_FRONT_X, SPOILER_REAR_X


@memo
def stage_body_and_glazing():
    body_fixed, door_l, door_r, spoiler = body_lib.build()
    glazing_fixed, targa_roof, glass_l, glass_r = glazing_lib.build()
    mirror_l = aero_lib.build_wing_mirror(1)
    mirror_r = aero_lib.build_wing_mirror(-1)
    spoiler_struts = aero_lib.build_spoiler_struts()

    door_left_assy = group("door_left", [door_l, glass_l, mirror_l])
    door_right_assy = group("door_right", [door_r, glass_r, mirror_r])
    spoiler_assy = group("active_spoiler", [spoiler, *spoiler_struts])
    return (
        body_fixed,
        glazing_fixed,
        door_left_assy,
        door_right_assy,
        spoiler_assy,
        targa_roof,
    )


@memo
def stage_lighting_and_aero():
    return group("lighting_and_aero", [lighting_lib.build(), aero_lib.build()])


@memo
def stage_wheels_and_brakes():
    return wheels_lib.build()


@memo
def stage_chassis():
    return chassis_lib.build()


@memo
def stage_interior():
    return interior_lib.build()


def _attach_kinematics(body_fixed, door_l, door_r, spoiler_assy, targa_roof):
    """Attach butterfly door hinges, deployable rear spoiler slide, and removable Targa lift."""
    # Butterfly door hinges positioned at the upper A-pillar beltline so the entire door swings cleanly outward & upward
    left_axis = bd.Axis((DOOR_FRONT_X + 6.0, 918.0, 770.0), (0.0, 0.36, -0.933))
    right_axis = bd.Axis((DOOR_FRONT_X + 6.0, -918.0, 770.0), (0.0, 0.36, 0.933))

    jl = bd.RevoluteJoint("door_left", body_fixed, axis=left_axis, angular_range=(0.0, 56.0))
    bd.RigidJoint("door_left", door_l, jl.location)
    jl.connect_to(door_l.joints["door_left"], angle=0.0)

    jr = bd.RevoluteJoint("door_right", body_fixed, axis=right_axis, angular_range=(0.0, 56.0))
    bd.RigidJoint("door_right", door_r, jr.location)
    jr.connect_to(door_r.joints["door_right"], angle=0.0)

    # Deployable active rear spoiler linear slide (+Z up to 85 mm)
    sp_x = 0.5 * (SPOILER_FRONT_X + SPOILER_REAR_X)
    sp_axis = bd.Axis((sp_x, 0.0, 835.0), (0.0, 0.0, 1.0))
    js = bd.LinearJoint("active_spoiler", body_fixed, axis=sp_axis, linear_range=(0.0, 85.0))
    bd.RigidJoint("active_spoiler", spoiler_assy, bd.Location(sp_axis.position))
    js.connect_to(spoiler_assy.joints["active_spoiler"], position=0.0)

    # Removable panoramic Targa roof glass lift (+Z up to 320 mm)
    if targa_roof is not None:
        tr_axis = bd.Axis((-140.0, 0.0, 1170.0), (0.0, 0.0, 1.0))
        jt = bd.LinearJoint("targa_roof", body_fixed, axis=tr_axis, linear_range=(0.0, 320.0))
        bd.RigidJoint("targa_roof", targa_roof, bd.Location(tr_axis.position))
        jt.connect_to(targa_roof.joints["targa_roof"], position=0.0)


@model
def tesla_roadster():
    body_fixed, glazing_fixed, door_l, door_r, spoiler_assy, targa_roof = (
        stage_body_and_glazing()
    )
    trim = stage_lighting_and_aero()
    wheels = stage_wheels_and_brakes()
    chassis = stage_chassis()
    cabin = stage_interior()

    _attach_kinematics(body_fixed, door_l, door_r, spoiler_assy, targa_roof)

    children = [
        body_fixed,
        glazing_fixed,
        door_l,
        door_r,
        spoiler_assy,
    ]
    if targa_roof is not None:
        children.append(targa_roof)
    children.extend([trim, wheels, chassis, cabin])

    car = bd.Compound(children=children, label="tesla_roadster")

    # Verify target dimensions directly on built geometry
    bb = car.bounding_box()
    assert 4480.0 <= bb.size.X <= 4560.0, f"Unexpected length: {bb.size.X}"
    assert 1150.0 <= bb.size.Z <= 1210.0, f"Unexpected height: {bb.size.Z}"

    # Named mechanism poses
    mechanism_state(car, "cruise", door_left=0.0, door_right=0.0, active_spoiler=0.0, targa_roof=0.0)
    mechanism_state(car, "track", door_left=0.0, door_right=0.0, active_spoiler=80.0, targa_roof=0.0)
    mechanism_state(car, "open_top", door_left=0.0, door_right=0.0, active_spoiler=0.0, targa_roof=280.0)
    mechanism_state(car, "showroom", door_left=52.0, door_right=52.0, active_spoiler=80.0, targa_roof=0.0)

    # Smooth showroom configuration sequence
    configuration_sequence(
        car,
        "showcase",
        [
            (0.0, "cruise"),
            (1.8, "track"),
            (3.6, "showroom"),
            (5.4, "cruise"),
        ],
    )
    return car


if __name__ == "__main__":
    tesla_roadster()
