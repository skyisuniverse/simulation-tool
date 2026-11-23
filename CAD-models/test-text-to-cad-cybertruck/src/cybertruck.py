"""Complete production Tesla Cybertruck (AWD / Cyberbeast, Medium Air Suspension) root CAD assembly.

Composes all modular sub-assemblies (chassis, 30X stainless exoskeleton, powered frunk with DRL
lightbar, tailgate with crimson LED bar, panoramic glazing & cabin interior, exterior cladding &
hardware, and four 20-inch Cyber wheels with 7-spoke aero covers and Goodyear Wrangler Territory RT
285/65R20 all-terrain tires), plus articulated frunk & tailgate closures with named mechanism states.

Coordinate convention:
  -Y forward (nose), +Y rearward (tailgate), +X driver side (left), +Z up, Z = 0 ground plane.
"""

from __future__ import annotations

import build123d as bd
from cad import model
from cad.build123d import configuration_sequence, mechanism_state

from ct_body import cybertruck_body
from ct_chassis import cybertruck_chassis
from ct_frunk import cybertruck_frunk
from ct_glazing import cybertruck_glazing
from ct_tailgate import cybertruck_tailgate
from ct_trim import cybertruck_trim
from ct_wheel import cyber_wheel
from lib import spec


@model
def tesla_cybertruck():
    """Complete production Tesla Cybertruck assembly with articulated powered frunk and tailgate."""
    chassis = cybertruck_chassis().shape
    body = cybertruck_body().shape
    glazing = cybertruck_glazing().shape
    trim = cybertruck_trim().shape
    frunk = cybertruck_frunk().shape
    tailgate = cybertruck_tailgate().shape

    wheel_proto = cyber_wheel().shape
    wheel_fl = bd.Pos(spec.TRACK_HALF, spec.Y_FRONT_AXLE, spec.AXLE_Z) * wheel_proto
    wheel_fr = bd.Pos(-spec.TRACK_HALF, spec.Y_FRONT_AXLE, spec.AXLE_Z) * bd.Rot(0, 0, 180) * wheel_proto
    wheel_rl = bd.Pos(spec.TRACK_HALF, spec.Y_REAR_AXLE, spec.AXLE_Z) * wheel_proto
    wheel_rr = bd.Pos(-spec.TRACK_HALF, spec.Y_REAR_AXLE, spec.AXLE_Z) * bd.Rot(0, 0, 180) * wheel_proto

    wheel_fl.label = "wheel_front_left"
    wheel_fr.label = "wheel_front_right"
    wheel_rl.label = "wheel_rear_left"
    wheel_rr.label = "wheel_rear_right"
    wheels = bd.Compound(children=[wheel_fl, wheel_fr, wheel_rl, wheel_rr], label="wheels")

    # Hinged powered frunk closure: +angle lifts front nose upward around cowl hinge axis (-X)
    frunk_axis = bd.Axis(
        (0.0, spec.s_to_y(spec.S_COWL_CENTER - 20.0), spec.Z_COWL - 6.0),
        (-1.0, 0.0, 0.0),
    )
    frunk_hinge = bd.RevoluteJoint("frunk_open", chassis, axis=frunk_axis, angular_range=(0.0, 50.0))
    bd.RigidJoint("frunk_open", frunk, frunk_hinge.location)
    frunk_hinge.connect_to(frunk.joints["frunk_open"], angle=0.0)

    # Hinged tailgate closure: +angle folds tailgate rearward/flat (90 deg) around lower rear hinge (-X)
    tg_axis = bd.Axis(
        (0.0, spec.s_to_y(spec.S_TAILGATE_TOP + 8.0), spec.Z_TAILGATE_BOT + 16.0),
        (-1.0, 0.0, 0.0),
    )
    tg_hinge = bd.RevoluteJoint("tailgate_open", chassis, axis=tg_axis, angular_range=(0.0, 90.0))
    bd.RigidJoint("tailgate_open", tailgate, tg_hinge.location)
    tg_hinge.connect_to(tailgate.joints["tailgate_open"], angle=0.0)

    assy = bd.Compound(
        children=[chassis, body, glazing, trim, frunk, tailgate, wheels],
        label="tesla_cybertruck",
    )

    # Official production dimensional assertions (Medium air suspension)
    bb = assy.bounding_box()
    assert abs(bb.size.Y - spec.LENGTH) < 2.0, f"Length mismatch: {bb.size.Y}"
    assert abs(bb.size.X - spec.WIDTH_INCL_MIRRORS) < 2.0, f"Width incl mirrors mismatch: {bb.size.X}"
    assert abs(bb.size.Z - spec.HEIGHT_MEDIUM) < 3.0, f"Height mismatch: {bb.size.Z}"
    assert abs(bb.min.Z) < 0.5, f"Tires not seated on Z=0 ground plane: min.Z={bb.min.Z}"

    # Named mechanism poses & showcase motion sequence
    mechanism_state(assy, "closed", frunk_open=0.0, tailgate_open=0.0)
    mechanism_state(assy, "tailgate_open", frunk_open=0.0, tailgate_open=90.0)
    mechanism_state(assy, "frunk_open", frunk_open=45.0, tailgate_open=0.0)
    mechanism_state(assy, "utility_open", frunk_open=45.0, tailgate_open=90.0)
    configuration_sequence(
        assy,
        "showcase_closures",
        [
            (0.0, "closed"),
            (1.8, "frunk_open"),
            (3.6, "utility_open"),
            (5.4, "tailgate_open"),
            (7.2, "closed"),
        ],
    )
    return assy


if __name__ == "__main__":
    tesla_cybertruck()
