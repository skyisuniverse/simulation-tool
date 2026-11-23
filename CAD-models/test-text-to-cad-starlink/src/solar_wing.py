"""Articulated accordion-folded solar array wing components for SpaceX Starlink V2 Mini.

Exports four shared B-rep part models that compose both the Port (-X) and Starboard (+X)
10-panel solar array wings (~26.8 m deployed wingspan, flat-stowing inside the 2.7 x 4.1 m
bus footprint for Falcon 9 fairing stacking):

- sada_yoke: Solar Array Drive Assembly rotary shaft, A-frame truss, and 4 root hinge forks
- solar_panel_odd: Inboard TOP tang, outboard BOTTOM fork+pin (Panels 1, 3, 5, 7, 9)
- solar_panel_even: Inboard BOTTOM tang, outboard TOP fork+pin (Panels 2, 4, 6, 8)
- solar_panel_tip: Inboard BOTTOM tang, closed outboard tip bumper rail (Panel 10)
"""

import build123d as bd
from bd_materials import metals
from cad import model
from cad.build123d import materials

from spec import (
    BUS_X,
    HINGE_EAR_W,
    HINGE_FORK_GAP,
    HINGE_GAP_X,
    HINGE_TANG_W,
    HINGE_Y_POSITIONS,
    HINGE_Z_OFFSET,
    PANEL_CHORD,
    PANEL_LEN,
    PANEL_THICK,
    ROOT_HINGE_X,
    SADA_Z,
    Z_HINGE_TOP,
)

BOSS_R = 7.5
PIN_R = 4.0
BORE_R = 4.5


def _hinge_lug_solid(end_sign: float, z_sign: float, y_center: float, width: float) -> bd.Solid:
    """Build one gooseneck clevis ear or tang connecting a panel end to its offset hinge pin.

    Geometry guarantees >= 2.5 mm radial clearance against the mating panel across the full
    0..180 degree accordion fold sweep.
    """
    hx = PANEL_LEN / 2.0
    hz = PANEL_THICK / 2.0
    x_pin = end_sign * (hx + HINGE_GAP_X)
    z_pin = z_sign * HINGE_Z_OFFSET
    x_edge = end_sign * hx
    x_in = end_sign * (hx - 4.0)

    # Gooseneck profile in XZ plane at y = y_center
    # Outer edge slopes cleanly from pin boss top/bottom down to panel face corner (z = z_sign * hz)
    # so it stays strictly outside the mating panel's 180-deg folded volume.
    pts_xz = [
        (x_pin, y_center, z_pin + z_sign * BOSS_R),
        (x_edge, y_center, z_sign * hz),
        (x_in, y_center, z_sign * hz),
        (x_in, y_center, -z_sign * (hz - 3.0)),
        (x_edge, y_center, -z_sign * (hz - 3.0)),
        (x_pin, y_center, z_pin - z_sign * BOSS_R),
    ]
    face = bd.Face(bd.Wire.make_polygon(pts_xz + [pts_xz[0]]))
    strap = bd.extrude(face, amount=width / 2.0, dir=(0, 1, 0), both=True)
    boss = (
        bd.Pos(x_pin, y_center, z_pin)
        * bd.Rot(90, 0, 0)
        * bd.Cylinder(radius=BOSS_R, height=width)
    )
    return strap + boss


def _make_panel_assembly(label: str, in_z_sign: float, out_z_sign: float | None) -> bd.Compound:
    """Build one complete solar array panel (frame + hinges + photovoltaic cell blanket).

    Local frame:
      X in [-PANEL_LEN/2, +PANEL_LEN/2]  (-X inboard, +X outboard)
      Y in [-PANEL_CHORD/2, +PANEL_CHORD/2]
      Z in [-PANEL_THICK/2, +PANEL_THICK/2] (+Z sun-facing PV cells)
    """
    frame_mat = materials.anodized("#2E3540")
    pv_mat = materials.anodized("#0E2244")
    pv_mat.pbr = pv_mat.pbr.override(roughness=0.16, metalness=0.55, clearcoat=0.65, clearcoat_roughness=0.10)
    ti = metals.titanium()
    ti.pbr = ti.pbr.override(roughness=0.25)

    hx = PANEL_LEN / 2.0
    hz = PANEL_THICK / 2.0

    # 1. Structural CFRP/aluminum perimeter frame with +Z PV pocket and -Z rear stiffening ribs
    outer_box = bd.Box(PANEL_LEN, PANEL_CHORD, PANEL_THICK)

    frame_cuts = []
    # Front (+Z) photovoltaic cell blanket recess: Z in [+2.4, +7.5], rim = 26 mm
    frame_cuts.append(
        bd.Pos(0.0, 0.0, 2.4)
        * bd.Box(
            PANEL_LEN - 52.0,
            PANEL_CHORD - 52.0,
            hz - 2.4 + 2.0,
            align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
        )
    )

    # Rear (-Z) lightweighting structural truss bays (2 spanwise x 6 chordwise pockets)
    # Leaves central spanwise spine & 5 transverse chordwise ribs on the -Z rear face
    rear_w = (PANEL_LEN - 110.0) / 2.0
    rear_l = (PANEL_CHORD - 210.0) / 6.0
    for rx in (-PANEL_LEN / 4.0 + 4.0, PANEL_LEN / 4.0 - 4.0):
        for j in range(6):
            ry = -PANEL_CHORD / 2.0 + 35.0 + rear_l / 2.0 + j * (rear_l + 28.0)
            frame_cuts.append(
                bd.Pos(rx, ry, -hz - 1.0)
                * bd.Box(
                    rear_w,
                    rear_l,
                    5.2,
                    align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
                )
            )

    frame = outer_box - frame_cuts

    # Add inboard (-X) single hinge tangs at all 4 hinge stations
    in_pin_x = -(hx + HINGE_GAP_X)
    in_pin_z = in_z_sign * HINGE_Z_OFFSET
    lug_adds = []
    lug_bores = []
    for yh in HINGE_Y_POSITIONS:
        lug_adds.append(_hinge_lug_solid(-1.0, in_z_sign, yh, HINGE_TANG_W))
        lug_bores.append(
            bd.Pos(in_pin_x, yh, in_pin_z)
            * bd.Rot(90, 0, 0)
            * bd.Cylinder(radius=BORE_R, height=HINGE_TANG_W + 6.0)
        )

    # Add outboard (+X) double-ear clevis forks + pins, or tip bumper pads if outboard tip panel
    pins_solids = []
    if out_z_sign is not None:
        out_pin_x = hx + HINGE_GAP_X
        out_pin_z = out_z_sign * HINGE_Z_OFFSET
        ear_offset = (HINGE_FORK_GAP + HINGE_EAR_W) / 2.0
        pin_len = HINGE_FORK_GAP + 2.0 * HINGE_EAR_W + 2.0
        for yh in HINGE_Y_POSITIONS:
            lug_adds.append(_hinge_lug_solid(1.0, out_z_sign, yh - ear_offset, HINGE_EAR_W))
            lug_adds.append(_hinge_lug_solid(1.0, out_z_sign, yh + ear_offset, HINGE_EAR_W))
            # Bore outer fork ears for the pin
            lug_bores.append(
                bd.Pos(out_pin_x, yh, out_pin_z)
                * bd.Rot(90, 0, 0)
                * bd.Cylinder(radius=PIN_R + 0.25, height=pin_len + 4.0)
            )
            pins_solids.append(
                bd.Pos(out_pin_x, yh, out_pin_z)
                * bd.Rot(90, 0, 0)
                * bd.Cylinder(radius=PIN_R, height=pin_len)
            )
    else:
        # Outboard tip bumper rail accent pads (compact, non-protruding past end)
        for yh in (-1460.0, 0.0, 1460.0):
            lug_adds.append(
                bd.Pos(hx + 3.0, yh, 0.0)
                * bd.Box(8.0, 140.0, PANEL_THICK - 2.0)
            )

    for add in lug_adds:
        frame = frame + add
    frame = frame - lug_bores
    frame.label = f"{label}_frame"
    frame.material = frame_mat

    # 2. Photovoltaic solar cell blanket (+Z face, Z in [2.8, 6.6], inset 2 mm inside frame pocket)
    pv_w = PANEL_LEN - 56.0
    pv_l = PANEL_CHORD - 56.0
    pv_blanket = bd.Pos(0.0, 0.0, 2.8) * bd.Box(
        pv_w, pv_l, 3.8, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    # Score crisp 4 x 12 solar cell sub-module grid grooves on +Z face (depth 1.8 mm)
    grooves = []
    for ix in range(1, 4):
        gx = -pv_w / 2.0 + ix * (pv_w / 4.0)
        grooves.append(
            bd.Pos(gx, 0.0, 4.8)
            * bd.Box(4.0, pv_l + 4.0, 3.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        )
    for iy in range(1, 12):
        gy = -pv_l / 2.0 + iy * (pv_l / 12.0)
        grooves.append(
            bd.Pos(0.0, gy, 4.8)
            * bd.Box(pv_w + 4.0, 4.0, 3.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        )
    pv_cells = pv_blanket - grooves
    pv_cells.label = f"{label}_pv_cells"
    pv_cells.material = pv_mat

    children = [frame, pv_cells]
    if pins_solids:
        pin_group = pins_solids[0]
        for p in pins_solids[1:]:
            pin_group = pin_group + p
        pin_group.label = f"{label}_hinge_pins"
        pin_group.material = ti
        children.append(pin_group)

    return bd.Compound(children=children, label=label)


@model
def sada_yoke():
    """Starboard SADA rotary drive shaft, A-frame composite truss yoke, and 4 root hinge forks.

    Built in world coordinates for the Starboard (+X) wing at SADA = 0 deg.
    Port (-X) wing uses a 180-deg Z-rotated placement of this exact same model.
    """
    ti = metals.titanium()
    ti.pbr = ti.pbr.override(roughness=0.25)
    yoke_mat = materials.anodized("#3A424D")

    x_bus = BUS_X / 2.0  # 1350.0
    x_bar = ROOT_HINGE_X  # 1356.0 (yoke plane X in [1351.5, 1363.5], 1.5 mm outboard of bus edge)

    # 1. Rotary drive shaft (r = 19.5 mm, clears R=21 housing bore by 1.5 mm) & hub collar
    shaft = (
        bd.Pos(x_bus - 20.0, 0.0, SADA_Z)
        * bd.Rot(0, 90, 0)
        * bd.Cylinder(radius=19.5, height=64.0)
    )
    hub = (
        bd.Pos(x_bar + 1.5, 0.0, SADA_Z)
        * bd.Rot(0, 90, 0)
        * bd.Cylinder(radius=34.0, height=12.0)
    )

    # 2. A-frame diagonal truss arms rising from SADA hub (Y=0, Z=136) to transverse beam (Z=196)
    arm_pts_pos = [
        (x_bar + 1.5, -18.0, SADA_Z + 12.0),
        (x_bar + 1.5, 18.0, SADA_Z + 12.0),
        (x_bar + 1.5, 515.0, 192.0),
        (x_bar + 1.5, 465.0, 192.0),
    ]
    arm_pts_neg = [
        (x_bar + 1.5, -18.0, SADA_Z + 12.0),
        (x_bar + 1.5, 18.0, SADA_Z + 12.0),
        (x_bar + 1.5, -465.0, 192.0),
        (x_bar + 1.5, -515.0, 192.0),
    ]
    arm_p = bd.extrude(bd.Face(bd.Wire.make_polygon(arm_pts_pos + [arm_pts_pos[0]])), amount=6.0, dir=(1, 0, 0), both=True)
    arm_n = bd.extrude(bd.Face(bd.Wire.make_polygon(arm_pts_neg + [arm_pts_neg[0]])), amount=6.0, dir=(1, 0, 0), both=True)

    # Secondary diagonal outer braces from (Y=+-140, Z=150) out to (Y=+-1460, Z=192)
    brace_p_pts = [
        (x_bar + 1.5, 220.0, 162.0),
        (x_bar + 1.5, 280.0, 162.0),
        (x_bar + 1.5, 1480.0, 192.0),
        (x_bar + 1.5, 1430.0, 192.0),
    ]
    brace_n_pts = [
        (x_bar + 1.5, -220.0, 162.0),
        (x_bar + 1.5, -280.0, 162.0),
        (x_bar + 1.5, -1480.0, 192.0),
        (x_bar + 1.5, -1430.0, 192.0),
    ]
    brace_p = bd.extrude(bd.Face(bd.Wire.make_polygon(brace_p_pts + [brace_p_pts[0]])), amount=5.5, dir=(1, 0, 0), both=True)
    brace_n = bd.extrude(bd.Face(bd.Wire.make_polygon(brace_n_pts + [brace_n_pts[0]])), amount=5.5, dir=(1, 0, 0), both=True)

    # 3. Horizontal transverse hinge carrier bar (X in [1351.5, 1363.5], Z in [188, 203])
    # Strictly below deployed P1 (Z >= 207) and stowed P1 (Z >= 225) and outboard of bus (X <= 1350)
    beam = (
        bd.Pos(x_bar + 1.5, 0.0, 188.0)
        * bd.Box(12.0, 3000.0, 15.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    )

    yoke_body = shaft + hub + arm_p + arm_n + brace_p + brace_n + beam

    # 4. Four double-ear root clevis forks centered at (X = ROOT_HINGE_X, Z = Z_HINGE_TOP = 223.0)
    ear_offset = (HINGE_FORK_GAP + HINGE_EAR_W) / 2.0
    pin_len = HINGE_FORK_GAP + 2.0 * HINGE_EAR_W + 2.0
    ear_bores = []
    pins = []
    for yh in HINGE_Y_POSITIONS:
        for ey in (yh - ear_offset, yh + ear_offset):
            stem = (
                bd.Pos(x_bar, ey, 201.0)
                * bd.Box(14.0, HINGE_EAR_W, Z_HINGE_TOP - 201.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
            )
            boss = (
                bd.Pos(x_bar, ey, Z_HINGE_TOP)
                * bd.Rot(90, 0, 0)
                * bd.Cylinder(radius=BOSS_R, height=HINGE_EAR_W)
            )
            yoke_body = yoke_body + stem + boss

        ear_bores.append(
            bd.Pos(x_bar, yh, Z_HINGE_TOP)
            * bd.Rot(90, 0, 0)
            * bd.Cylinder(radius=PIN_R + 0.25, height=pin_len + 4.0)
        )
        pins.append(
            bd.Pos(x_bar, yh, Z_HINGE_TOP)
            * bd.Rot(90, 0, 0)
            * bd.Cylinder(radius=PIN_R, height=pin_len)
        )

    yoke_body = yoke_body - ear_bores
    yoke_body.label = "sada_yoke_structure"
    yoke_body.material = yoke_mat

    pin_group = pins[0]
    for p in pins[1:]:
        pin_group = pin_group + p
    pin_group.label = "sada_root_pins"
    pin_group.material = ti

    return bd.Compound(children=[yoke_body, pin_group], label="sada_yoke")


@model
def solar_panel_odd():
    """Odd-numbered accordion solar panel (Panels 1, 3, 5, 7, 9): inboard TOP tang, outboard BOTTOM fork."""
    return _make_panel_assembly("solar_panel_odd", in_z_sign=1.0, out_z_sign=-1.0)


@model
def solar_panel_even():
    """Even-numbered accordion solar panel (Panels 2, 4, 6, 8): inboard BOTTOM tang, outboard TOP fork."""
    return _make_panel_assembly("solar_panel_even", in_z_sign=-1.0, out_z_sign=1.0)


@model
def solar_panel_tip():
    """Outboard tip solar panel (Panel 10): inboard BOTTOM tang, closed outboard tip bumper rail."""
    return _make_panel_assembly("solar_panel_tip", in_z_sign=-1.0, out_z_sign=None)


if __name__ == "__main__":
    sada_yoke()
    solar_panel_odd()
    solar_panel_even()
    solar_panel_tip()
