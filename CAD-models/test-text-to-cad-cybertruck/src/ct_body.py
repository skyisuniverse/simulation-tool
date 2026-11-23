"""30X Cold-Rolled Stainless Steel Exoskeleton panels for the production Tesla Cybertruck.

Constructs every side body panel as crisp, flat-faceted solids with realistic 4.5 mm panel gaps:
  - Left & right front fenders (lower planar fender + upper triangular fender shoulder)
  - Left & right handle-less front doors
  - Left & right handle-less rear doors
  - Left & right rear quarter panels + iconic flat triangular sail pillars
  - Left & right continuous stainless steel roof / A-pillar cant rails
"""

from __future__ import annotations

import build123d as bd
from cad import model

from lib import geometry, materials, spec

T_SKIN = 5.0          # solid panel thickness (mm), extruded strictly inward from outer master cage
GAP = spec.PANEL_GAP  # 4.5 mm crisp shadow reveal between adjacent panels


def _lower_side_slab(s0: float, s1: float, z0_lo: float, z1_lo: float) -> bd.Solid:
    """Build a crisp flat-faceted lower body side stainless panel on the +X (left) side."""
    y0, y1 = spec.s_to_y(s0), spec.s_to_y(s1)
    zb0, zb1 = spec.z_belt(s0), spec.z_belt(s1)
    x0_lo = spec.x_body_lower(s0, z0_lo)
    x1_lo = spec.x_body_lower(s1, z1_lo)
    x0_hi = spec.x_belt(s0)
    x1_hi = spec.x_belt(s1)

    p0 = (x0_lo, y0, z0_lo)
    p1 = (x1_lo, y1, z1_lo)
    p2 = (x1_hi, y1, zb1)
    p3 = (x0_hi, y0, zb0)
    return geometry.quad_slab(p0, p1, p2, p3, thickness=T_SKIN, inward_normal_hint=(-1.0, 0.0, 0.0))


def _build_front_fenders() -> tuple[bd.Solid, bd.Solid]:
    """Build left & right stainless front fenders (lower planar panel + upper fender shoulder)."""
    s_f = spec.S_NOSE_CORNER + 2.0           # 202 mm (crisp gap behind front nose corner)
    s_r = spec.S_FRONT_DOOR_SEAM - GAP / 2.0  # 1482.75 mm
    z_lo = spec.Z_ROCKER_TOP + 1.0           # 366 mm

    lower = _lower_side_slab(s_f, s_r, z_lo, z_lo)

    # Trim lower front nose corner below Z = 672 mm all the way into front wheel arch (s <= 500)
    # so there is zero hanging fang ahead of the arch and the front bumper wraps cleanly underneath.
    y_bumper_cut = spec.s_to_y(500.0)
    bumper_cut = bd.Pos(880.0, y_bumper_cut, 672.0) * bd.Box(
        500.0,
        500.0,
        400.0,
        align=(bd.Align.CENTER, bd.Align.MAX, bd.Align.MAX),
    )
    lower = lower - bumper_cut

    # Upper triangular stainless fender shoulder (between hood crease, beltline, and A-pillar glass)
    p_front = (spec.x_belt(s_f), spec.s_to_y(s_f), spec.z_belt(s_f))
    p_cowl = (spec.x_roof(spec.S_COWL_CORNER), spec.s_to_y(spec.S_COWL_CORNER), spec.z_roof_side(spec.S_COWL_CORNER))
    p_qglass = (spec.x_belt(spec.S_QUARTER_GLASS_FWD), spec.s_to_y(spec.S_QUARTER_GLASS_FWD), spec.z_belt(spec.S_QUARTER_GLASS_FWD))
    upper_tri = geometry.tri_slab(
        p_front, p_cowl, p_qglass, thickness=T_SKIN, inward_normal_hint=(-0.92, 0.0, -0.38)
    )

    fender_l = lower + upper_tri

    # Cut exact trapezoidal front wheel arch opening
    arch_pts = spec.arch_polygon_2d(spec.S_FRONT_AXLE, expand=0.0)
    arch_cut = geometry.extrude_yz_polygon(arch_pts, 650.0, 1150.0)
    fender_l = fender_l - arch_cut

    fender_r = bd.mirror(fender_l, about=bd.Plane.YZ)
    return (
        materials.apply_mat(fender_l, materials.stainless_30x, "front_fender_l"),
        materials.apply_mat(fender_r, materials.stainless_30x, "front_fender_r"),
    )


def _build_doors() -> list[bd.Solid]:
    """Build left & right handle-less flat stainless front and rear doors."""
    z_lo = spec.Z_ROCKER_TOP + 2.0  # 367 mm (clean 2 mm shadow reveal above matte-black rocker)

    # Front door: s in [1487.25, 2627.75]
    fd_s0 = spec.S_FRONT_DOOR_SEAM + GAP / 2.0
    fd_s1 = spec.S_B_PILLAR - GAP / 2.0
    fd_l = _lower_side_slab(fd_s0, fd_s1, z_lo, z_lo)
    fd_r = bd.mirror(fd_l, about=bd.Plane.YZ)

    # Rear door: s in [2632.25, 3727.75]
    rd_s0 = spec.S_B_PILLAR + GAP / 2.0
    rd_s1 = spec.S_REAR_DOOR_SEAM - GAP / 2.0
    rd_l = _lower_side_slab(rd_s0, rd_s1, z_lo, z_lo)
    rd_r = bd.mirror(rd_l, about=bd.Plane.YZ)

    return [
        materials.apply_mat(fd_l, materials.stainless_30x, "front_door_l"),
        materials.apply_mat(fd_r, materials.stainless_30x, "front_door_r"),
        materials.apply_mat(rd_l, materials.stainless_30x, "rear_door_l"),
        materials.apply_mat(rd_r, materials.stainless_30x, "rear_door_r"),
    ]


def _build_rear_quarters_and_sails() -> tuple[bd.Solid, bd.Solid]:
    """Build left & right single-plane rear quarter panels integrated with flat triangular sail pillars."""
    s_0 = spec.S_REAR_DOOR_SEAM + GAP / 2.0   # 3732.25 mm
    s_end = spec.S_TAILGATE_TOP - 2.0         # 5633.0 mm
    z_lo = spec.Z_ROCKER_TOP + 1.0            # 366 mm

    # One single unbroken dead-flat stainless steel rear quarter panel from rear door seam to tailgate!
    lower = _lower_side_slab(s_0, s_end, z_lo, z_lo)

    # Trim lower rear corner behind rear wheel arch below Z = 652 mm (starting inside arch at s=4920)
    # so there is zero hanging fang behind the arch and the rear bumper wraps cleanly underneath.
    y_rb_cut = spec.s_to_y(4920.0)
    rb_cut = bd.Pos(880.0, y_rb_cut, 652.0) * bd.Box(
        500.0,
        850.0,
        400.0,
        align=(bd.Align.CENTER, bd.Align.MIN, bd.Align.MAX),
    )
    lower = lower - rb_cut

    # Iconic flat triangular stainless steel Sail Pillar (3 exact points -> true zero-twist plane!)
    # Starts cleanly 2 mm aft of cant_rail trailing edge (S_CAB_REAR) with a crisp shadow gap.
    s_c = spec.S_CAB_REAR + 2.0
    p_c_belt = (spec.x_belt(s_c), spec.s_to_y(s_c), spec.z_belt(s_c))
    p_c_roof = (spec.x_roof(s_c), spec.s_to_y(s_c), spec.z_roof_side(s_c))
    p_t_corner = (spec.x_belt(s_end), spec.s_to_y(s_end), spec.z_belt(s_end))
    sail_tri = geometry.tri_slab(
        p_c_belt, p_c_roof, p_t_corner, thickness=T_SKIN, inward_normal_hint=(-0.82, 0.0, -0.57)
    )

    quarter_l = lower + sail_tri

    # Cut exact trapezoidal rear wheel arch opening
    arch_pts = spec.arch_polygon_2d(spec.S_REAR_AXLE, expand=0.0)
    arch_cut = geometry.extrude_yz_polygon(arch_pts, 650.0, 1150.0)
    quarter_l = quarter_l - arch_cut

    quarter_r = bd.mirror(quarter_l, about=bd.Plane.YZ)
    return (
        materials.apply_mat(quarter_l, materials.stainless_30x, "rear_quarter_l"),
        materials.apply_mat(quarter_r, materials.stainless_30x, "rear_quarter_r"),
    )


def _build_cant_rails() -> tuple[bd.Solid, bd.Solid]:
    """Build left & right continuous stainless steel roof / A-pillar cant rails framing the glasshouse.

    Spans from the cowl corner (s=910) straight up the A-pillar to the roof apex (s=2470),
    then straight back over the panoramic roof to the C-pillar / sail transition (s=3765).
    """
    t_rail = 14.0
    w_rail = spec.CANT_RAIL_W  # 48 mm wide metallic structural arch

    def _rail_seg(s_a: float, s_b: float) -> bd.Solid:
        # Outer edge along x_roof(s), inner edge inward by w_rail along roof slope
        p0 = (spec.x_roof(s_a), spec.s_to_y(s_a), spec.z_roof_side(s_a))
        p1 = (spec.x_roof(s_b), spec.s_to_y(s_b), spec.z_roof_side(s_b))
        p2 = (spec.x_roof(s_b) - w_rail, spec.s_to_y(s_b), spec.z_roof(s_b))
        p3 = (spec.x_roof(s_a) - w_rail, spec.s_to_y(s_a), spec.z_roof(s_a))
        return geometry.quad_slab(p0, p1, p2, p3, thickness=t_rail, inward_normal_hint=(-0.22, 0.0, -0.97))

    front_leg = _rail_seg(spec.S_COWL_CORNER + 8.0, spec.S_ROOF_APEX)
    rear_leg = _rail_seg(spec.S_ROOF_APEX, spec.S_CAB_REAR - 2.0)
    rail_l = front_leg + rear_leg
    rail_r = bd.mirror(rail_l, about=bd.Plane.YZ)

    return (
        materials.apply_mat(rail_l, materials.stainless_cant_rail, "cant_rail_l"),
        materials.apply_mat(rail_r, materials.stainless_cant_rail, "cant_rail_r"),
    )


@model
def cybertruck_body():
    """Complete fixed 30X stainless steel Cybertruck exoskeleton panels (10 parts)."""
    ff_l, ff_r = _build_front_fenders()
    doors = _build_doors()
    rq_l, rq_r = _build_rear_quarters_and_sails()
    cr_l, cr_r = _build_cant_rails()

    assy = bd.Compound(
        children=[ff_l, ff_r, *doors, rq_l, rq_r, cr_l, cr_r],
        label="cybertruck_body",
    )
    bb = assy.bounding_box()
    assert abs(bb.max.Z - spec.Z_ROOF_APEX) < 3.0, f"Unexpected body apex Z: {bb.max.Z}"
    return assy


if __name__ == "__main__":
    cybertruck_body()
