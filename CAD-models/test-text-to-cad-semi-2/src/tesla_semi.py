"""Master root assembly of the original Tesla Semi (6x4 Long Range Day Cab).

Composes:
  - chassis           (ladder frame, ~900 kWh battery pack, tri-motor e-axles, catwalk, fifth wheel)
  - cab               (sculpted aerodynamic silver bullet cab, bumper, swept LED headlights, mirrors)
  - glazing           (panoramic wraparound curved windshield, helmet-visor side windows & frit)
  - interior          (central driver cockpit, 3-spoke steering wheel, twin 15-in displays, jump seat)
  - 2x steer_wheel    (295/75R22.5 front steer tires + Tesla satin-black aero wheel covers)
  - 4x drive_wheel_pair (8x 295/75R22.5 tandem dual drive tires + Tesla rear aero wheel covers)
"""

import build123d as bd
from cad import model

import dims as D
from cab import cab
from chassis import chassis
from glazing import glazing
from interior import interior
from wheels import drive_wheel_pair, steer_wheel


@model
def tesla_semi():
    """Full 1:1 original Tesla Semi Class 8 electric tractor assembly."""
    ch = chassis().shape
    cb = cab().shape
    gl = glazing().shape
    it = interior().shape

    sw = steer_wheel().shape
    dw = drive_wheel_pair().shape

    # Front steer wheels (left +X outboard, right -X outboard rotated 180 about Z)
    sw_l = bd.Pos(D.X_STEER_CENTER, D.Y_FRONT_AXLE, D.TIRE_R) * sw
    sw_l.label = "steer_wheel_left"
    sw_r = bd.Pos(-D.X_STEER_CENTER, D.Y_FRONT_AXLE, D.TIRE_R) * bd.Rot(0, 0, 180) * sw
    sw_r.label = "steer_wheel_right"

    # Tandem rear dual drive wheel pairs (forward cruise e-axle & rearward dual-motor e-axle)
    x_drive_mid = (D.X_DRIVE_INNER + D.X_DRIVE_OUTER) / 2.0
    dw_fl = bd.Pos(x_drive_mid, D.Y_REAR_AXLE_1, D.TIRE_R) * dw
    dw_fl.label = "drive_wheels_fwd_left"
    dw_fr = bd.Pos(-x_drive_mid, D.Y_REAR_AXLE_1, D.TIRE_R) * bd.Rot(0, 0, 180) * dw
    dw_fr.label = "drive_wheels_fwd_right"

    dw_al = bd.Pos(x_drive_mid, D.Y_REAR_AXLE_2, D.TIRE_R) * dw
    dw_al.label = "drive_wheels_aft_left"
    dw_ar = bd.Pos(-x_drive_mid, D.Y_REAR_AXLE_2, D.TIRE_R) * bd.Rot(0, 0, 180) * dw
    dw_ar.label = "drive_wheels_aft_right"

    wheels_group = bd.Compound(
        children=[sw_l, sw_r, dw_fl, dw_fr, dw_al, dw_ar],
        label="wheels",
    )

    truck = bd.Compound(
        children=[ch, cb, gl, it, wheels_group],
        label="tesla_semi",
    )

    bb = truck.bounding_box()
    assert abs(bb.min.Z) < 2.0, f"Tires should rest on Z=0 ground plane, got min.Z={bb.min.Z}"
    assert abs(bb.max.Z - D.TOTAL_HEIGHT) < 35.0, f"Overall height mismatch: {bb.max.Z}"
    assert 6500.0 <= bb.size.Y <= 6700.0, f"Overall length out of Class 8 Semi range: {bb.size.Y}"
    return truck


if __name__ == "__main__":
    tesla_semi()
