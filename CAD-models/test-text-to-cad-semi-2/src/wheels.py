"""Tesla Semi 22.5-inch commercial wheel & tire assemblies with signature aero covers.

Builds:
  - steer_wheel: Single 295/75R22.5 steer tire, forged 22.5" rim, 10-lug hub,
    and Tesla Semi flush satin-black aerodynamic wheel cover (+X faces outward).
  - drive_wheel_pair: Dual tandem 295/75R22.5 tires with 55 mm air gap, dual rims,
    deep hub, and Tesla Semi satin-black rear aero wheel cover (+X faces outward).

Local coordinate frame of both models:
  - Axis of rotation along X (wheel lies in YZ plane, centered at origin (0, 0, 0)).
  - +X is the outboard (street-facing) side of the wheel.
  - For left side (+X of truck): place at Pos(+X_center, Y_axle, TIRE_R).
  - For right side (-X of truck): rotate 180 deg about Z so outboard faces -X!
"""

import math
import build123d as bd
from bd_materials import metals, plastics
from cad import model

import dims as D


def _make_tire(width=D.TIRE_W, r_outer=D.TIRE_R, r_rim=D.RIM_R):
    """Build a realistic contoured commercial truck tire revolved about the X axis.

    Uses smooth arc/spline shoulders and circumferential highway tread grooves
    so the profile reads crisp and continuous (no faceted polygonal bands).
    """
    hw = width / 2.0
    r_bead = r_rim - 4.0       # Slight seat overlap onto rim flange? Keep exact contact r_rim!
    r_bead = r_rim + 0.5       # 0.5 mm radial clearance from rim outer lip -> zero interference
    r_bulge = r_rim + (r_outer - r_rim) * 0.45
    r_shoulder = r_outer - 22.0
    hw_tread = hw - 18.0
    hw_bulge = hw + 3.0        # Subtle realistic sidewall bulge

    # Revolve profile in XZ plane about the X axis (Wait: Z is radial, X is axial)
    # In BuildSketch(Plane.XZ), local X = world X (axial), local Y = world Z (radial >= 0)
    with bd.BuildSketch(bd.Plane.XZ) as sk:
        with bd.BuildLine():
            # Inner bead seat (parallel to X at Z = r_bead)
            l_inner = bd.Line((-hw + 22.0, r_bead), (hw - 22.0, r_bead))
            # Right (+X) sidewall: bead -> bulge -> shoulder
            s_right = bd.Spline(
                (hw - 22.0, r_bead),
                (hw - 6.0, r_rim + 32.0),
                (hw_bulge, r_bulge),
                (hw - 4.0, r_shoulder - 18.0),
                (hw_tread, r_outer - 4.0),
            )
            # Crown arc (gently crowned highway tread surface)
            a_crown = bd.ThreePointArc(
                (hw_tread, r_outer - 4.0),
                (0.0, r_outer),
                (-hw_tread, r_outer - 4.0),
            )
            # Left (-X) sidewall (mirror of right)
            s_left = bd.Spline(
                (-hw_tread, r_outer - 4.0),
                (-hw + 4.0, r_shoulder - 18.0),
                (-hw_bulge, r_bulge),
                (-hw + 6.0, r_rim + 32.0),
                (-hw + 22.0, r_bead),
            )
        bd.make_face()
    tire = bd.revolve(sk.sketch.face(), axis=bd.Axis.X, revolution_arc=360)

    # Cut 4 clean circumferential highway tread grooves around the crown
    groove_xs = [-78.0, -26.0, 26.0, 78.0]
    groove_w = 11.0
    groove_d = 12.0
    grooves = []
    for gx in groove_xs:
        with bd.BuildSketch(bd.Plane.XZ) as gsk:
            with bd.BuildLine():
                bd.Polyline(
                    (gx - groove_w / 2.0, r_outer + 5.0),
                    (gx + groove_w / 2.0, r_outer + 5.0),
                    (gx + groove_w * 0.35, r_outer - groove_d),
                    (gx - groove_w * 0.35, r_outer - groove_d),
                    close=True,
                )
            bd.make_face()
        grooves.append(bd.revolve(gsk.sketch.face(), axis=bd.Axis.X, revolution_arc=360))
    tire = tire - grooves

    tire.label = "tire"
    tire.material = plastics.rubber()
    tire.material.pbr = tire.material.pbr.override(roughness=0.86)
    tire.color = D.COLOR_TIRE_RUBBER
    return tire


def _make_rim(width=D.TIRE_W, r_rim=D.RIM_R, is_steer=True):
    """Build a 22.5-inch commercial truck wheel rim (barrel + dish + mounting flange)."""
    hw = width / 2.0 - 23.0  # Fits cleanly inside tire beads without interference
    r_inner = r_rim - 18.0
    r_lip = r_rim - 0.5      # 1.0 mm clear of tire inner bead (r_rim + 0.5)

    # Revolved rim barrel + mounting web in XZ plane about X axis
    # For steer wheel, center disc sits near +X side (outboard dish);
    # for drive wheels, deep dish mounts cleanly to axle flange.
    disc_x = 38.0 if is_steer else 0.0
    with bd.BuildSketch(bd.Plane.XZ) as sk:
        with bd.BuildLine():
            pts = [
                (-hw, r_inner),
                (-hw, r_lip),
                (-hw + 14.0, r_lip),
                (-hw + 18.0, r_rim - 10.0),
                (hw - 18.0, r_rim - 10.0),
                (hw - 14.0, r_lip),
                (hw, r_lip),
                (hw, r_inner),
                (disc_x + 12.0, r_inner),
                (disc_x + 12.0, 118.0),
                (disc_x - 12.0, 118.0),
                (disc_x - 12.0, r_inner),
            ]
            bd.Polyline(*pts, close=True)
        bd.make_face()
    rim = bd.revolve(sk.sketch.face(), axis=bd.Axis.X, revolution_arc=360)

    # Cut 10 rounded commercial vent hand-holes around the rim disc
    vent_holes = []
    for i in range(10):
        ang = math.radians(i * 36.0)
        vy = 205.0 * math.cos(ang)
        vz = 205.0 * math.sin(ang)
        cyl = (
            bd.Pos(disc_x, vy, vz)
            * bd.Rot(0, 90, 0)
            * bd.Cylinder(26.0, 44.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.CENTER))
        )
        vent_holes.append(cyl)
    rim = rim - vent_holes

    rim.label = "rim"
    rim.material = metals.aluminum()
    rim.material.pbr = rim.material.pbr.override(roughness=0.32, metalness=0.85)
    rim.color = D.COLOR_RIM_DARK
    return rim


def _make_aero_wheel_cover(x_outer, r_outer=D.RIM_R - 4.0, is_steer=True):
    """Build the iconic Tesla Semi flush satin-black aerodynamic wheel cover.

    Smooth gently-domed composite aero disc with recessed turbine spoke flutes
    and a central Tesla center cap — matching the original 2017/2022 Semi wheels.
    """
    r_cap = 96.0
    # Smooth revolved aerodynamic dish sitting cleanly outboard of the rim lip (124.5)
    # and flush inside the tire sidewall (147.5)
    x1 = x_outer + 6.0    # Outer flush lip (e.g. 137.5 on steer, 312.5 on drive)
    x_apex = x1 + (10.0 if is_steer else 6.0)

    with bd.BuildSketch(bd.Plane.XZ) as sk:
        with bd.BuildLine():
            # Flat center seat for medallion + smooth contoured aero face
            l_seat = bd.Line((x_apex, 0.0), (x_apex, 62.0))
            s_front = bd.Spline(
                (x_apex, 62.0),
                (x_apex - 1.5, r_cap),
                (x1 + 3.5, r_outer * 0.68),
                (x1, r_outer),
            )
            l_edge = bd.Line((x1, r_outer), (x1 - 9.0, r_outer))
            s_back = bd.Spline(
                (x1 - 9.0, r_outer),
                (x1 - 5.5, r_outer * 0.68),
                (x_apex - 11.0, r_cap),
                (x_apex - 10.0, 0.0),
            )
            l_axis = bd.Line((x_apex - 10.0, 0.0), (x_apex, 0.0))
        bd.make_face()
    cover = bd.revolve(sk.sketch.face(), axis=bd.Axis.X, revolution_arc=360)

    # Sculpt 5 crisp aerodynamic flush-spoke cooling flutes on the outboard face
    slots = []
    for i in range(5):
        ang_deg = i * 72.0
        slot_box = bd.Box(
            8.0, 125.0, 26.0,
            align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.CENTER),
        )
        slot_placed = (
            bd.Rot(ang_deg, 0, 0)
            * bd.Pos(x1 + 3.5, 185.0, 0.0)
            * bd.Rot(16.0, 0, 0)
            * slot_box
        )
        slots.append(slot_placed)
    cover = cover - slots

    cover.label = "aero_cover"
    cover.material = plastics.abs_()
    cover.material.pbr = cover.material.pbr.override(roughness=0.35, metalness=0.25)
    cover.color = "#323740"

    # Central metallic hub ring / Tesla cap medallion (0.2 mm clear of flat seat)
    cap_disc = (
        bd.Pos(x_apex + 0.2, 0.0, 0.0)
        * bd.Rot(0, 90, 0)
        * bd.Cylinder(58.0, 4.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    )
    cap_disc.label = "center_cap"
    cap_disc.material = metals.aluminum()
    cap_disc.material.pbr = cap_disc.material.pbr.override(roughness=0.22, metalness=0.9)
    cap_disc.color = D.COLOR_CHROME

    # Subtle outer chrome/silver trim ring around aero cover lip
    with bd.BuildSketch(bd.Plane.XZ) as rsk:
        with bd.BuildLine():
            bd.Polyline(
                (x1 + 1.5, r_outer - 10.0),
                (x1 + 4.0, r_outer - 10.0),
                (x1 + 4.0, r_outer - 2.0),
                (x1 + 1.5, r_outer - 2.0),
                close=True,
            )
        bd.make_face()
    trim_ring = bd.revolve(rsk.sketch.face(), axis=bd.Axis.X, revolution_arc=360)
    trim_ring.label = "trim_ring"
    trim_ring.material = metals.aluminum()
    trim_ring.material.pbr = trim_ring.material.pbr.override(roughness=0.25, metalness=0.88)
    trim_ring.color = D.COLOR_CHROME

    return [cover, cap_disc, trim_ring]


def _make_hub_and_lugs(x_hub_start, x_hub_end, x_flange):
    """Build central wheel hub barrel (fits inside rim bore, clear of aero cover)."""
    length = x_hub_end - x_hub_start
    hub = (
        bd.Pos((x_hub_start + x_hub_end) / 2.0, 0.0, 0.0)
        * bd.Rot(0, 90, 0)
        * bd.Cylinder(116.0, length, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.CENTER))
    )
    hub.label = "hub"
    hub.material = metals.mild_steel()
    hub.material.pbr = hub.material.pbr.override(roughness=0.45, metalness=0.8)
    hub.color = D.COLOR_CAST_STEEL
    return hub


@model
def steer_wheel():
    """Single 295/75R22.5 front steer wheel assembly with Tesla aero cover."""
    tire = _make_tire(D.TIRE_W, D.TIRE_R, D.RIM_R)
    rim = _make_rim(D.TIRE_W, D.RIM_R, is_steer=True)
    hub = _make_hub_and_lugs(-95.0, 95.0, 38.0)
    cover_parts = _make_aero_wheel_cover(x_outer=D.TIRE_W / 2.0 - 16.0, is_steer=True)

    asm = bd.Compound(children=[tire, rim, hub, *cover_parts], label="steer_wheel")
    bb = asm.bounding_box()
    assert abs(bb.size.Z - D.TIRE_OD) < 2.0, f"Steer tire OD mismatch: {bb.size.Z}"
    return asm


@model
def drive_wheel_pair():
    """Dual 295/75R22.5 rear tandem drive wheel pair with Tesla aero cover.

    Origin is placed at the midpoint between inner and outer tire centers:
      inner tire at X = -(TIRE_W + DRIVE_DUAL_GAP) / 2 = -175 mm
      outer tire at X = +(TIRE_W + DRIVE_DUAL_GAP) / 2 = +175 mm
    """
    half_pitch = (D.TIRE_W + D.DRIVE_DUAL_GAP) / 2.0  # 175.0 mm

    tire_proto = _make_tire(D.TIRE_W, D.TIRE_R, D.RIM_R)
    rim_proto = _make_rim(D.TIRE_W, D.RIM_R, is_steer=False)

    tire_in = bd.Pos(-half_pitch, 0.0, 0.0) * tire_proto
    tire_in.label = "tire_inner"
    tire_out = bd.Pos(half_pitch, 0.0, 0.0) * tire_proto
    tire_out.label = "tire_outer"

    rim_in = bd.Pos(-half_pitch, 0.0, 0.0) * rim_proto
    rim_in.label = "rim_inner"
    rim_out = bd.Pos(half_pitch, 0.0, 0.0) * rim_proto
    rim_out.label = "rim_outer"

    # Central dual-wheel hub spanning both rim bores
    hub = _make_hub_and_lugs(-half_pitch - 60.0, half_pitch + 75.0, 0.0)

    # Flush Tesla aero wheel cover on the outboard (+X) wheel
    cover_parts = _make_aero_wheel_cover(
        x_outer=half_pitch + D.TIRE_W / 2.0 - 16.0,
        is_steer=False,
    )

    asm = bd.Compound(
        children=[tire_in, tire_out, rim_in, rim_out, hub, *cover_parts],
        label="drive_wheel_pair",
    )
    bb = asm.bounding_box()
    assert abs(bb.size.Z - D.TIRE_OD) < 2.0, f"Drive tire OD mismatch: {bb.size.Z}"
    return asm


if __name__ == "__main__":
    steer_wheel()
    drive_wheel_pair()
