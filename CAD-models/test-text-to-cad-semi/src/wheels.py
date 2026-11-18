"""Wheel models for the Tesla Semi-style truck."""

import build123d as bd
from cad import model

from constants import (
    COLOR_TIRE_RUBBER,
    COLOR_WHEEL_AERO,
    COLOR_WHEEL_RIM,
    RIM_RADIUS,
    TIRE_RADIUS,
    TIRE_WIDTH,
)


def make_tire(width=TIRE_WIDTH, outer_r=TIRE_RADIUS, inner_r=RIM_RADIUS):
    """Constructs a commercial truck tire with profiled shoulders."""
    # Main tire cylinder along Y axis (width)
    tire = bd.Cylinder(outer_r, width)
    # Fillet outer shoulders for realistic rounded tire profile
    shoulder_edges = tire.edges().filter_by(bd.GeomType.CIRCLE)
    if shoulder_edges:
        tire = bd.fillet(shoulder_edges, 35.0)

    # Bore out rim center
    bore = bd.Cylinder(inner_r, width + 2.0)
    tire = tire - bore

    # Add 4 circumferential tread grooves for visual realism
    for offset_y in [-80.0, -28.0, 28.0, 80.0]:
        groove = bd.Cylinder(outer_r + 1.0, 8.0) - bd.Cylinder(outer_r - 6.0, 8.0)
        groove = bd.Pos(0, 0, offset_y) * groove
        tire = tire - groove

    tire.color = COLOR_TIRE_RUBBER
    tire.label = "tire"
    return tire


def make_steer_wheel():
    """Single front steer wheel with aerodynamic Tesla Semi style aero cover."""
    tire = make_tire()

    # Wheel rim barrel
    rim = bd.Cylinder(RIM_RADIUS, TIRE_WIDTH - 20.0)
    rim_bore = bd.Cylinder(RIM_RADIUS - 35.0, TIRE_WIDTH)
    rim = rim - rim_bore
    rim.color = COLOR_WHEEL_RIM
    rim.label = "rim"

    # Aerodynamic aero cover disc on the outboard face (Z = +TIRE_WIDTH/2 in local frame)
    cover_z = TIRE_WIDTH / 2.0 - 5.0
    aero_disc = bd.Cylinder(RIM_RADIUS - 5.0, 15.0)
    aero_center = bd.Cylinder(90.0, 24.0)
    aero_rim_ring = bd.Cylinder(RIM_RADIUS - 10.0, 18.0) - bd.Cylinder(RIM_RADIUS - 35.0, 20.0)

    cover = aero_disc + aero_center + aero_rim_ring
    # Aero cooling slots (small circular recess patterns)
    for i in range(8):
        angle = i * 45.0
        slot = bd.Pos(0, 0, 0) * bd.Rot(0, 0, angle) * bd.Pos(RIM_RADIUS - 65.0, 0, 0) * bd.Cylinder(16.0, 25.0)
        cover = cover - slot

    cover = bd.Pos(0, 0, cover_z - 7.5) * cover
    cover.color = COLOR_WHEEL_AERO
    cover.label = "aero_cover"

    # In local frame, cylinder is along Z. Rotate so tire axis is along Y (+Y is outboard)
    # bd.Rot(90, 0, 0) maps Z -> Y
    wheel = bd.Compound(children=[tire, rim, cover], label="steer_wheel")
    wheel = bd.Rot(90, 0, 0) * wheel
    return wheel


def make_drive_wheel_dual(spacing=310.0):
    """Dual rear drive wheels with heavy-duty hub and aero rim inserts."""
    inner_tire = make_tire()
    outer_tire = make_tire()

    # Rims
    inner_rim = bd.Cylinder(RIM_RADIUS, TIRE_WIDTH - 20.0) - bd.Cylinder(RIM_RADIUS - 40.0, TIRE_WIDTH)
    outer_rim = bd.Cylinder(RIM_RADIUS, TIRE_WIDTH - 20.0) - bd.Cylinder(RIM_RADIUS - 40.0, TIRE_WIDTH)
    inner_rim.color = COLOR_WHEEL_RIM
    outer_rim.color = COLOR_WHEEL_RIM

    # Heavy-duty central axle hub between both wheels
    hub = bd.Cylinder(140.0, spacing + TIRE_WIDTH - 10.0)
    hub_cap = bd.Pos(0, 0, spacing / 2.0 + TIRE_WIDTH / 2.0) * bd.Cylinder(90.0, 30.0)
    hub = hub + hub_cap
    hub.color = COLOR_WHEEL_AERO
    hub.label = "axle_hub"

    # Outer wheel aero dish
    outer_cover = bd.Cylinder(RIM_RADIUS - 10.0, 12.0)
    for i in range(10):
        slot = bd.Rot(0, 0, i * 36.0) * bd.Pos(RIM_RADIUS - 70.0, 0, 0) * bd.Cylinder(14.0, 20.0)
        outer_cover = outer_cover - slot
    outer_cover = bd.Pos(0, 0, spacing / 2.0 + TIRE_WIDTH / 2.0 - 15.0) * outer_cover
    outer_cover.color = COLOR_WHEEL_AERO
    outer_cover.label = "outer_cover"

    # Position inner and outer along local Z (which will become Y)
    inner_assembly = bd.Pos(0, 0, -spacing / 2.0) * bd.Compound(children=[inner_tire, inner_rim], label="inner_wheel")
    outer_assembly = bd.Pos(0, 0, spacing / 2.0) * bd.Compound(children=[outer_tire, outer_rim], label="outer_wheel")

    dual = bd.Compound(children=[inner_assembly, outer_assembly, hub, outer_cover], label="drive_wheel_dual")
    dual = bd.Rot(90, 0, 0) * dual
    return dual


@model
def steer_wheel():
    return make_steer_wheel()


@model
def drive_wheel_pair():
    return make_drive_wheel_dual()


if __name__ == "__main__":
    steer_wheel()
    drive_wheel_pair()
