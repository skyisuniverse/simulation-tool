"""Reusable build123d faceted / planar loft and solid construction helpers.

All build123d attributes are accessed inside functions so importing this module
does not load the OCCT kernel at module import time.
"""

from __future__ import annotations

import build123d as bd

from lib import spec


def section_face_yz_at_y(y_val: float, xz_pts: list[tuple[float, float]]) -> bd.Face:
    """Create a planar polygonal Face on the XZ plane at constant Y = y_val."""
    pts3d = [(x, y_val, z) for x, z in xz_pts]
    wire = bd.Wire.make_polygon(pts3d)
    return bd.Face(wire)


def ruled_loft_sections(sections_3d: list[list[tuple[float, float, float]]]) -> bd.Solid:
    """Build a crisp faceted solid via ruled loft through matching 3D polygonal loops."""
    faces = [bd.Face(bd.Wire.make_polygon(pts)) for pts in sections_3d]
    solid = bd.loft(faces, ruled=True)
    return solid


def quad_slab(
    p0: tuple[float, float, float],
    p1: tuple[float, float, float],
    p2: tuple[float, float, float],
    p3: tuple[float, float, float],
    thickness: float,
    inward_normal_hint: tuple[float, float, float],
) -> bd.Solid:
    """Build a crisp thin solid plate from 4 corners (even slightly non-planar quads via ruled loft).

    Offsets all 4 points along `inward_normal_hint` (normalized) by `thickness` and creates a
    watertight ruled hexahedron (exact solid, zero thin-shell sewing issues).
    """
    nx, ny, nz = inward_normal_hint
    mag = (nx * nx + ny * ny + nz * nz) ** 0.5
    ux, uy, uz = nx / mag * thickness, ny / mag * thickness, nz / mag * thickness

    outer = [p0, p1, p2, p3]
    inner = [(x + ux, y + uy, z + uz) for x, y, z in outer]
    # Use two planar triangles if quad is non-planar, or ruled loft between 2-segment / 4-vertex pairs
    # A hexahedron built from ruled loft between edge-pair faces [p0,p1,i1,i0] and [p3,p2,i2,i3]
    # handles slight bilinear twist cleanly AND guarantees valid positive solid!
    f_a = bd.Face(bd.Wire.make_polygon([outer[0], outer[1], inner[1], inner[0]]))
    f_b = bd.Face(bd.Wire.make_polygon([outer[3], outer[2], inner[2], inner[3]]))
    return bd.loft([f_a, f_b], ruled=True)


def tri_slab(
    p0: tuple[float, float, float],
    p1: tuple[float, float, float],
    p2: tuple[float, float, float],
    thickness: float,
    inward_normal_hint: tuple[float, float, float],
) -> bd.Solid:
    """Build a crisp exact flat triangular prism plate of given thickness."""
    face = bd.Face(bd.Wire.make_polygon([p0, p1, p2]))
    v_n = face.normal_at()
    hx, hy, hz = inward_normal_hint
    if v_n.X * hx + v_n.Y * hy + v_n.Z * hz < 0:
        v_n = -v_n
    return bd.extrude(face, amount=thickness, dir=v_n)


def extrude_yz_polygon(
    yz_pts: list[tuple[float, float]],
    x_min: float,
    x_max: float,
) -> bd.Solid:
    """Extrude a 2D (Y, Z) polygon along +X from x_min to x_max."""
    pts3d = [(x_min, y, z) for y, z in yz_pts]
    face = bd.Face(bd.Wire.make_polygon(pts3d))
    return bd.extrude(face, amount=(x_max - x_min), dir=(1, 0, 0))


def extrude_xy_polygon(
    xy_pts: list[tuple[float, float]],
    z_min: float,
    z_max: float,
) -> bd.Solid:
    """Extrude a 2D (X, Y) polygon along +Z from z_min to z_max."""
    pts3d = [(x, y, z_min) for x, y in xy_pts]
    face = bd.Face(bd.Wire.make_polygon(pts3d))
    return bd.extrude(face, amount=(z_max - z_min), dir=(0, 0, 1))


def wheel_arch_cutter(s_axle: float, x_in: float = 550.0, x_out: float = 1150.0) -> bd.Solid:
    """Build a trapezoidal wheel-arch cutout tool on both left (+X) and right (-X) sides."""
    pts = spec.arch_polygon_2d(s_axle, expand=0.0)
    left = extrude_yz_polygon(pts, x_in, x_out)
    right = extrude_yz_polygon(pts, -x_out, -x_in)
    return left + right


def body_cross_section_full(
    s: float,
    z_bot: float | None = None,
    inset: float = 0.0,
) -> list[tuple[float, float, float]]:
    """Return an 8-point symmetric closed outer hull loop (X, Y, Z) at longitudinal station s.

    Points run around the cross-section in consistent order for crisp ruled lofting:
      0: (+x_bot, y, z_bot)
      1: (+x_b,   y, z_b)
      2: (+x_r,   y, z_rs)
      3: (+x_c,   y, z_rc)   (center-crown left)
      4: (-x_c,   y, z_rc)   (center-crown right)
      5: (-x_r,   y, z_rs)
      6: (-x_b,   y, z_b)
      7: (-x_bot, y, z_bot)
    """
    y = spec.s_to_y(s)
    zb_low = spec.Z_ROCKER_TOP if z_bot is None else z_bot
    xb_low = max(100.0, spec.x_rocker(s) - inset)
    xb = max(100.0, spec.x_belt(s) - inset)
    zb = spec.z_belt(s)
    xr = max(100.0, spec.x_roof(s) - inset)
    zrs = spec.z_roof_side(s) - inset * 0.35
    zrc = spec.z_roof(s) - inset * 0.35
    xc = max(50.0, min(xr - 15.0, spec.x_tonneau_inner(s) - inset))
    return [
        (xb_low, y, zb_low),
        (xb, y, zb),
        (xr, y, zrs),
        (xc, y, zrc),
        (-xc, y, zrc),
        (-xr, y, zrs),
        (-xb, y, zb),
        (-xb_low, y, zb_low),
    ]
