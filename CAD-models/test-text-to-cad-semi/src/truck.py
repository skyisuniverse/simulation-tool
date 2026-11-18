"""Complete assembly of the Tesla Semi-style electric Class 8 truck tractor."""

import build123d as bd
from cad import model

from cab import cab
from chassis import chassis
from constants import (
    COLOR_CHASSIS,
    X_DRIVE_AXLE_1,
    X_DRIVE_AXLE_2,
    X_FRONT_AXLE,
    Y_FRONT_TRACK_HALF,
    Z_AXLE,
)
from wheels import drive_wheel_pair, steer_wheel


def make_powertrain_axles():
    """Front steer axle and rear independent electric drive units (e-axles)."""
    # Front steer axle beam
    front_axle_beam = bd.Pos(X_FRONT_AXLE, 0, Z_AXLE) * bd.Box(120.0, 1850.0, 90.0)
    front_kingpin_l = bd.Pos(X_FRONT_AXLE, 880.0, Z_AXLE) * bd.Cylinder(45.0, 180.0)
    front_kingpin_r = bd.Pos(X_FRONT_AXLE, -880.0, Z_AXLE) * bd.Cylinder(45.0, 180.0)
    front_steer_unit = front_axle_beam + front_kingpin_l + front_kingpin_r
    front_steer_unit.color = COLOR_CHASSIS
    front_steer_unit.label = "front_steer_axle"

    # Tandem Drive Axle 1: Integrated Electric Drive Unit (motor + gearbox + axle tubes)
    e_motor_1 = bd.Pos(X_DRIVE_AXLE_1 - 100.0, 0, Z_AXLE) * bd.Cylinder(160.0, 520.0)  # motor casing
    diff_casing_1 = bd.Pos(X_DRIVE_AXLE_1, 0, Z_AXLE) * bd.Cylinder(190.0, 380.0)
    axle_tubes_1 = bd.Pos(X_DRIVE_AXLE_1, 0, Z_AXLE) * bd.Rot(90, 0, 0) * bd.Cylinder(65.0, 1750.0)
    drive_unit_1 = e_motor_1 + diff_casing_1 + axle_tubes_1
    drive_unit_1.color = COLOR_CHASSIS
    drive_unit_1.label = "electric_drive_unit_1"

    # Tandem Drive Axle 2: Integrated Electric Drive Unit
    e_motor_2 = bd.Pos(X_DRIVE_AXLE_2 - 100.0, 0, Z_AXLE) * bd.Cylinder(160.0, 520.0)
    diff_casing_2 = bd.Pos(X_DRIVE_AXLE_2, 0, Z_AXLE) * bd.Cylinder(190.0, 380.0)
    axle_tubes_2 = bd.Pos(X_DRIVE_AXLE_2, 0, Z_AXLE) * bd.Rot(90, 0, 0) * bd.Cylinder(65.0, 1750.0)
    drive_unit_2 = e_motor_2 + diff_casing_2 + axle_tubes_2
    drive_unit_2.color = COLOR_CHASSIS
    drive_unit_2.label = "electric_drive_unit_2"

    powertrain = bd.Compound(
        children=[front_steer_unit, drive_unit_1, drive_unit_2],
        label="powertrain_suspension",
    )
    return powertrain


def make_wheel_assembly():
    """All 10 commercial truck wheels (2 front steer + 8 tandem dual drive)."""
    # Wheel templates from models
    steer_geom = steer_wheel().shape
    dual_geom = drive_wheel_pair().shape

    # Front Steer Wheels
    w_steer_l = bd.Pos(X_FRONT_AXLE, Y_FRONT_TRACK_HALF, Z_AXLE) * steer_geom
    w_steer_l.label = "front_wheel_left"

    w_steer_r = bd.Pos(X_FRONT_AXLE, -Y_FRONT_TRACK_HALF, Z_AXLE) * bd.Rot(0, 0, 180) * steer_geom
    w_steer_r.label = "front_wheel_right"

    # Mid Tandem Axle Wheels (Tandem 1)
    y_dual = 975.0
    w_drive1_l = bd.Pos(X_DRIVE_AXLE_1, y_dual, Z_AXLE) * dual_geom
    w_drive1_l.label = "drive_wheels_mid_left"

    w_drive1_r = bd.Pos(X_DRIVE_AXLE_1, -y_dual, Z_AXLE) * bd.Rot(0, 0, 180) * dual_geom
    w_drive1_r.label = "drive_wheels_mid_right"

    # Rear Tandem Axle Wheels (Tandem 2)
    w_drive2_l = bd.Pos(X_DRIVE_AXLE_2, y_dual, Z_AXLE) * dual_geom
    w_drive2_l.label = "drive_wheels_rear_left"

    w_drive2_r = bd.Pos(X_DRIVE_AXLE_2, -y_dual, Z_AXLE) * bd.Rot(0, 0, 180) * dual_geom
    w_drive2_r.label = "drive_wheels_rear_right"

    wheels_compound = bd.Compound(
        children=[
            w_steer_l,
            w_steer_r,
            w_drive1_l,
            w_drive1_r,
            w_drive2_l,
            w_drive2_r,
        ],
        label="wheels_running_gear",
    )
    return wheels_compound


@model
def tesla_semi_truck():
    """Complete Tesla Semi Class 8 Electric Truck Tractor Assembly."""
    # 1. Heavy-duty chassis ladder frame, battery pack, fifth wheel, catwalk, and rear bumper
    chassis_sub = chassis().shape
    chassis_sub.label = "chassis"

    # 2. Powertrain axles and electric drive units
    powertrain_sub = make_powertrain_axles()

    # 3. Running gear wheels (steer and tandem dual drive wheels)
    wheels_sub = make_wheel_assembly()

    # 4. Aerodynamic cab body, panoramic glasshouse, aero skirts, lights, and camera mirrors
    cab_sub = cab().shape
    cab_sub.label = "cab_assembly"

    truck = bd.Compound(
        children=[chassis_sub, powertrain_sub, wheels_sub, cab_sub],
        label="tesla_semi_truck",
    )
    return truck


if __name__ == "__main__":
    tesla_semi_truck()
