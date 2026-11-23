"""Geometry helper primitives using exact world-coordinate bounds (lazy build123d)."""

import build123d as bd


def box_bounds(
    x0: float,
    x1: float,
    y0: float,
    y1: float,
    z0: float,
    z1: float,
):
    """Create a solid axis-aligned box spanning [x0, x1] x [y0, y1] x [z0, z1]."""
    dx = x1 - x0
    dy = y1 - y0
    dz = z1 - z0
    if dx <= 0 or dy <= 0 or dz <= 0:
        raise ValueError(
            f"Non-positive box extents: x=[{x0}, {x1}], y=[{y0}, {y1}], z=[{z0}, {z1}]"
        )
    return bd.Pos(x0, y0, z0) * bd.Box(
        dx, dy, dz, align=(bd.Align.MIN, bd.Align.MIN, bd.Align.MIN)
    )


def extrude_xz_polygon(points_xz: list[tuple[float, float]], y0: float, y1: float):
    """Extrude a 2D polygon in the XZ plane along +Y from y0 to y1."""
    dy = y1 - y0
    if dy <= 0:
        raise ValueError(f"Non-positive Y extrusion: y=[{y0}, {y1}]")
    pts = [(x, y0, z) for x, z in points_xz]
    wire = bd.Wire.make_polygon(pts)
    face = bd.Face(wire)
    return bd.extrude(face, amount=dy, dir=(0, 1, 0))


def extrude_yz_polygon(points_yz: list[tuple[float, float]], x0: float, x1: float):
    """Extrude a 2D polygon in the YZ plane along +X from x0 to x1."""
    dx = x1 - x0
    if dx <= 0:
        raise ValueError(f"Non-positive X extrusion: x=[{x0}, {x1}]")
    pts = [(x0, y, z) for y, z in points_yz]
    wire = bd.Wire.make_polygon(pts)
    face = bd.Face(wire)
    return bd.extrude(face, amount=dx, dir=(1, 0, 0))
