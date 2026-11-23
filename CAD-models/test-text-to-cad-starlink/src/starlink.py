"""SpaceX Starlink V2 Mini satellite root assembly with full solar deployment kinematics.

Composes:
- bus_chassis: 2.7 m x 4.1 m chamfered flat-panel spacecraft bus with OSR thermal radiators,
  central dorsal avionics spine, 4 reaction wheel housings, snubbers, SADA housings, and
  Falcon 9 stack retention lugs
- payload_antennas: Earth-facing (-Z) 4-sector Ku-band phased arrays, dual Ka-band parabolic
  gateway dishes, central E-band backhaul array, and S-band TT&C patches
- propulsion_module: Aft (-Y) dual Argon Hall-effect ion thrusters with BN ceramic channels,
  cathode neutralizers, and dual carbon-fiber Argon COPV tanks
- avionics_optics: 3 gimbaled Optical ISL ("Space Laser") terminals, dual baffled star
  trackers, zenith GNSS receiver, and coarse sun sensors
- Port & Starboard 10-panel articulated accordion solar array wings (~26.8 m deployed span,
  stowing flat within the 2.7 m x 4.1 m x 0.40 m Falcon 9 launch envelope)

Mechanism controls:
- port_sada / stbd_sada: Solar Array Drive Assembly pitch rotation (-180..+180 deg)
- port_root / stbd_root: Root deployment hinge lifting folded stack off bus (0..180 deg)
- port_accordion / stbd_accordion: Coupled 9-hinge Z-fold accordion deployment (0..1)
- Mechanism states: deployed, sun_tracking, unfolding, unlatched, stowed
- Configuration sequence: deploy_orbit (stowed -> unlatched -> deployed -> sun_tracking)
"""

import build123d as bd
from cad import model
from cad.build123d import configuration_sequence, gear_pair, mechanism_state

from avionics_optics import avionics_optics
from bus import bus_chassis
from payload_antennas import payload_antennas
from propulsion import propulsion_module
from solar_wing import sada_yoke, solar_panel_even, solar_panel_odd, solar_panel_tip
from spec import (
    BUS_X,
    HINGE_GAP_X,
    PANEL_DEPLOY_Z,
    PANEL_LEN,
    PANEL_PITCH_X,
    ROOT_HINGE_X,
    SADA_Z,
    WING_PANEL_COUNT,
    Z_HINGE_BOT,
    Z_HINGE_TOP,
)


def _build_wing_chain(
    side_name: str,
    side_sign: float,
    bus_ground: bd.Compound,
    yoke_shape: bd.Compound,
    odd_shape: bd.Compound,
    even_shape: bd.Compound,
    tip_shape: bd.Compound,
) -> tuple[list[bd.Compound], dict[str, float]]:
    """Place a SADA yoke and 10 accordion solar panels in deployed world pose and connect joints.

    Returns (parts_list, accordion_coupling_ratios).
    """
    # Starboard (+1): hinge axis (0, -1, 0) folds +X upward (+Z) and back over bus (-X)
    # Port (-1):      hinge axis (0, +1, 0) folds -X upward (+Z) and back over bus (+X)
    hinge_dir = (0.0, -side_sign, 0.0)
    rot_z = bd.Location() if side_sign > 0 else bd.Rot(0.0, 0.0, 180.0)

    # 1. SADA rotary yoke
    yoke = rot_z * yoke_shape
    yoke.label = f"{side_name}_sada_yoke"

    sada_name = f"{side_name}_sada"
    sada_axis = bd.Axis((side_sign * BUS_X / 2.0, 0.0, SADA_Z), (1.0, 0.0, 0.0))
    sada_joint = bd.RevoluteJoint(sada_name, bus_ground, axis=sada_axis, angular_range=(-180.0, 180.0))
    bd.RigidJoint(sada_name, yoke, sada_joint.location)
    sada_joint.connect_to(yoke.joints[sada_name], angle=0.0)

    parts = [yoke]
    coupling_ratios: dict[str, float] = {}

    # 2. Chain of 10 accordion solar panels (P1..P10)
    prev_body = yoke
    for k in range(WING_PANEL_COUNT):
        panel_num = k + 1
        if panel_num == WING_PANEL_COUNT:
            template = tip_shape
        elif panel_num % 2 == 1:
            template = odd_shape
        else:
            template = even_shape

        cx = side_sign * (ROOT_HINGE_X + HINGE_GAP_X + PANEL_LEN / 2.0 + k * PANEL_PITCH_X)
        panel = bd.Pos(cx, 0.0, PANEL_DEPLOY_Z) * rot_z * template
        panel.label = f"{side_name}_panel_{panel_num:02d}"

        hinge_x = side_sign * (ROOT_HINGE_X + k * PANEL_PITCH_X)
        if k == 0:
            # Root deployment hinge H0 (top hinge): 0 deg deployed, 90 deg upright, 180 deg stowed
            jname = f"{side_name}_root"
            hinge_z = Z_HINGE_TOP
            ang_range = (0.0, 180.0)
        elif k % 2 == 1:
            # Odd inter-panel hinge H1, H3, H5, H7, H9 (bottom hinge): 0 deg deployed, -180 deg folded
            jname = f"{side_name}_h{k}"
            hinge_z = Z_HINGE_BOT
            ang_range = (-180.0, 0.0)
            coupling_ratios[jname] = -180.0
        else:
            # Even inter-panel hinge H2, H4, H6, H8 (top hinge): 0 deg deployed, +180 deg folded
            jname = f"{side_name}_h{k}"
            hinge_z = Z_HINGE_TOP
            ang_range = (0.0, 180.0)
            coupling_ratios[jname] = 180.0

        h_axis = bd.Axis((hinge_x, 0.0, hinge_z), hinge_dir)
        h_joint = bd.RevoluteJoint(jname, prev_body, axis=h_axis, angular_range=ang_range)
        bd.RigidJoint(jname, panel, h_joint.location)
        h_joint.connect_to(panel.joints[jname], angle=0.0)

        parts.append(panel)
        prev_body = panel

    return parts, coupling_ratios


@model
def starlink_v2_mini():
    """Complete articulated SpaceX Starlink V2 Mini satellite assembly."""
    bus = bus_chassis().shape
    antennas = payload_antennas().shape
    propulsion = propulsion_module().shape
    optics = avionics_optics().shape

    # Group fixed spacecraft bus & payload subsystems into the ground link
    spacecraft_bus = bd.Compound(
        children=[bus, antennas, propulsion, optics],
        label="spacecraft_bus",
    )

    # Fetch shared solar wing B-rep prototypes (built once, placed across all 20 panels)
    yoke_proto = sada_yoke().shape
    odd_proto = solar_panel_odd().shape
    even_proto = solar_panel_even().shape
    tip_proto = solar_panel_tip().shape

    # Build Starboard (+X) and Port (-X) articulated 10-panel solar wings
    stbd_parts, stbd_ratios = _build_wing_chain(
        "stbd", 1.0, spacecraft_bus, yoke_proto, odd_proto, even_proto, tip_proto
    )
    port_parts, port_ratios = _build_wing_chain(
        "port", -1.0, spacecraft_bus, yoke_proto, odd_proto, even_proto, tip_proto
    )

    sat = bd.Compound(
        children=[spacecraft_bus, *stbd_parts, *port_parts],
        label="starlink_v2_mini",
    )

    # Couple all 9 inter-panel accordion hinges per wing into clean 0..1 fold controls
    gear_pair(sat, "stbd_accordion", **stbd_ratios)
    gear_pair(sat, "port_accordion", **port_ratios)

    # Named orbital & launch mechanism states
    mechanism_state(
        sat,
        "deployed",
        stbd_sada=0.0,
        port_sada=0.0,
        stbd_root=0.0,
        port_root=0.0,
        stbd_accordion=0.0,
        port_accordion=0.0,
    )
    mechanism_state(
        sat,
        "sun_tracking",
        stbd_sada=35.0,
        port_sada=35.0,
        stbd_root=0.0,
        port_root=0.0,
        stbd_accordion=0.0,
        port_accordion=0.0,
    )
    mechanism_state(
        sat,
        "unfolding",
        stbd_sada=0.0,
        port_sada=0.0,
        stbd_root=45.0,
        port_root=45.0,
        stbd_accordion=0.5,
        port_accordion=0.5,
    )
    mechanism_state(
        sat,
        "unlatched",
        stbd_sada=0.0,
        port_sada=0.0,
        stbd_root=90.0,
        port_root=90.0,
        stbd_accordion=1.0,
        port_accordion=1.0,
    )
    mechanism_state(
        sat,
        "stowed",
        stbd_sada=0.0,
        port_sada=0.0,
        stbd_root=180.0,
        port_root=180.0,
        stbd_accordion=1.0,
        port_accordion=1.0,
    )

    # Full orbital deployment motion sequence: Falcon 9 flat-pack -> unlatch -> accordion unfold -> sun track
    configuration_sequence(
        sat,
        "deploy_orbit",
        [
            (0.0, "stowed"),
            (0.8, "stowed"),
            (2.8, "unlatched"),
            (6.0, "deployed"),
            (8.0, "sun_tracking"),
            (9.5, "sun_tracking"),
            (11.0, "deployed"),
        ],
    )

    # Geometry sanity assertions on deployed full-scale envelope
    bb = sat.bounding_box()
    expected_span = 2.0 * (ROOT_HINGE_X + HINGE_GAP_X + (WING_PANEL_COUNT - 1) * PANEL_PITCH_X + PANEL_LEN + 7.0)
    assert abs(bb.size.X - expected_span) < 5.0, f"Unexpected deployed wingspan: {bb.size.X} vs {expected_span}"
    assert abs(bb.size.Y - 4189.0) < 30.0, f"Unexpected length along Y: {bb.size.Y}"
    return sat


if __name__ == "__main__":
    starlink_v2_mini()
