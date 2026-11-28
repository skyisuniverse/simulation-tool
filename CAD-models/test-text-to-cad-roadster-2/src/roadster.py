"""Root articulated CAD assembly of the 2nd-generation Tesla Roadster
(production-intent aerospace design per https://www.tesla.com/roadster).

Composes:
  - chassis  : Carbon monocoque, front splitter & intake, rising carbon rockers,
               4 rear cold-gas thrusters, 4 circular ducted suction fans, and
               4 underside perimeter thruster nozzles
  - body     : Ano White sculpted bodywork, hidden diagonal headlights, front
               full-width DRL, side aero camera/amber marker pods, edge-to-edge
               red rear light bar, and recessed 'RDSTR' license plate
  - canopy   : Continuous Gold Glazed wrap-around windshield, arched roof,
               tapered fastback rear glass, titanium A-pillar rails & mirror
  - doors    : Articulated left & right dihedral butterfly doors with frameless
               Gold Glazed glass, Alcantara door cards & glowing red LED accents
  - wing     : Articulated active rear wing (Ano White top, anodized bronze
               underside, downturned red-lit endplates, dark swan-neck struts)
  - wheels   : 20" front (295/30R20) & 21" rear (335/30R21) dual-tone 5-spoke
               aero wheels, Pirelli Trofeo tires & carbon-ceramic brakes
  - interior : Minimalist 'Supersonic' two-seat cockpit (Ultrawhite & Alcantara
               bucket seats, center spine, floating touchscreen, twin forward
               displays, and steer-by-wire Ultrawhite yoke)

Named mechanism states:
  - cruise   : Doors closed, active rear wing stowed low-drag (as built)
  - track    : Doors closed, active rear wing deployed +18 deg high-downforce
  - showroom : Both butterfly doors swung open +58 deg & active wing deployed
"""

import build123d as bd
from cad import model
from cad.build123d import configuration_sequence, mechanism_state

from body import body
from canopy import canopy
from chassis import chassis
from doors import door_left, door_right
from interior import interior
from spec import (
    DOOR_HINGE_DIR_L,
    DOOR_HINGE_POS_L,
    DOOR_OPEN_ANGLE,
    HEIGHT,
    LENGTH,
    TIRE_F_RADIUS,
    TIRE_R_RADIUS,
    WHEEL_F_CENTER_X,
    WHEEL_R_CENTER_X,
    WIDTH,
    WING_DEPLOY_ANGLE,
    WING_PIVOT_Y,
    WING_PIVOT_Z,
    Y_FRONT_AXLE,
    Y_REAR_AXLE,
    unit_vec,
)
from wheels import wheel_front, wheel_front_right, wheel_rear, wheel_rear_right
from wing import active_wing


@model
def tesla_roadster():
    """Complete articulated 2nd-generation Tesla Roadster assembly."""
    # Fixed structural & exterior subsystems
    ch = chassis().shape
    bd_shell = body().shape
    cn = canopy().shape
    cab = interior().shape

    # 4 Wheels (proper right-handed models on both sides so all normals face outward!)
    wf_l = wheel_front().shape
    wf_r = wheel_front_right().shape
    wr_l = wheel_rear().shape
    wr_r = wheel_rear_right().shape

    wheel_fl = bd.Pos(WHEEL_F_CENTER_X, Y_FRONT_AXLE, TIRE_F_RADIUS) * wf_l
    wheel_fl.label = "wheel_front_left"

    wheel_fr = bd.Pos(-WHEEL_F_CENTER_X, Y_FRONT_AXLE, TIRE_F_RADIUS) * wf_r
    wheel_fr.label = "wheel_front_right"

    wheel_rl = bd.Pos(WHEEL_R_CENTER_X, Y_REAR_AXLE, TIRE_R_RADIUS) * wr_l
    wheel_rl.label = "wheel_rear_left"

    wheel_rr = bd.Pos(-WHEEL_R_CENTER_X, Y_REAR_AXLE, TIRE_R_RADIUS) * wr_r
    wheel_rr.label = "wheel_rear_right"

    wheels_group = bd.Compound(
        children=[wheel_fl, wheel_fr, wheel_rl, wheel_rr],
        label="wheels",
    )

    # Articulated moving assemblies (built in exact closed/stowed as-built positions)
    dl = door_left().shape
    dr = door_right().shape
    wg = active_wing().shape

    # 1. Left (+X) dihedral butterfly door joint
    hx, hy, hz = DOOR_HINGE_POS_L
    dx, dy, dz = unit_vec(DOOR_HINGE_DIR_L)
    j_door_l = bd.RevoluteJoint(
        "door_left_hinge",
        bd_shell,
        axis=bd.Axis((hx, hy, hz), (dx, dy, dz)),
        angular_range=(0.0, 62.0),
    )
    bd.RigidJoint("door_left_hinge", dl, j_door_l.location)
    j_door_l.connect_to(dl.joints["door_left_hinge"], angle=0.0)

    # 2. Right (-X) dihedral butterfly door joint (exact YZ-mirror symmetry)
    j_door_r = bd.RevoluteJoint(
        "door_right_hinge",
        bd_shell,
        axis=bd.Axis((-hx, hy, hz), (dx, -dy, -dz)),
        angular_range=(0.0, 62.0),
    )
    bd.RigidJoint("door_right_hinge", dr, j_door_r.location)
    j_door_r.connect_to(dr.joints["door_right_hinge"], angle=0.0)

    # 3. Active rear aero wing deployment joint (+angle lifts wing & pitches nose-down)
    j_wing = bd.RevoluteJoint(
        "wing_deploy",
        bd_shell,
        axis=bd.Axis((0.0, WING_PIVOT_Y, WING_PIVOT_Z), (1.0, 0.0, 0.0)),
        angular_range=(0.0, 23.0),
    )
    bd.RigidJoint("wing_deploy", wg, j_wing.location)
    j_wing.connect_to(wg.joints["wing_deploy"], angle=0.0)

    car = bd.Compound(
        children=[ch, bd_shell, cn, cab, wheels_group, dl, dr, wg],
        label="tesla_roadster",
    )

    # Dimensional sanity assertions on the assembled vehicle envelope
    bb = car.bounding_box()
    bb_body = bd_shell.bounding_box()
    assert abs(bb.min.Z) < 2.0, f"Tires should rest on Z=0, got Z_min={bb.min.Z:.2f}"
    assert abs(bb.size.X - WIDTH) < 35.0, f"Width {bb.size.X:.1f} outside target {WIDTH}"
    assert abs(bb_body.size.Y - LENGTH) < 10.0, f"Body length {bb_body.size.Y:.1f} outside {LENGTH}"
    assert abs(bb.size.Z - HEIGHT) < 35.0, f"Height {bb.size.Z:.1f} outside target {HEIGHT}"

    # Named mechanism poses & smooth showcase motion sequence
    mechanism_state(
        car,
        "cruise",
        door_left_hinge=0.0,
        door_right_hinge=0.0,
        wing_deploy=0.0,
    )
    mechanism_state(
        car,
        "track",
        door_left_hinge=0.0,
        door_right_hinge=0.0,
        wing_deploy=WING_DEPLOY_ANGLE,
    )
    mechanism_state(
        car,
        "showroom",
        door_left_hinge=DOOR_OPEN_ANGLE,
        door_right_hinge=DOOR_OPEN_ANGLE,
        wing_deploy=WING_DEPLOY_ANGLE,
    )
    return configuration_sequence(
        car,
        "showcase",
        [
            (0.0, "cruise"),
            (2.0, "track"),
            (4.5, "showroom"),
            (6.5, "showroom"),
            (8.5, "cruise"),
        ],
    )


if __name__ == "__main__":
    tesla_roadster()
