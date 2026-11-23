"""9-section structural steel tower, elevator core, vertical guide rails, cryo risers, and haul cables."""

import build123d as bd
from cad import model

import spec as S


def _strut_between(p0, p1, width_normal, width_inplane, face_normal, extend=1.5):
    """Build a crisp rectangular structural strut from p0 to p1 aligned with face_normal."""
    v0 = bd.Vector(*p0)
    v1 = bd.Vector(*p1)
    d = v1 - v0
    length = d.length
    z_dir = d.normalized()
    origin = v0 - z_dir * extend
    total_len = length + 2.0 * extend
    plane = bd.Plane(origin=origin, x_dir=bd.Vector(*face_normal), z_dir=z_dir)
    return plane * bd.Box(
        width_normal,
        width_inplane,
        total_len,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )


def _build_truss_frame():
    """Build one 14.5 m (145 mm) prefabricated structural steel truss module as a single fused Solid."""
    h = S.MODULE_H
    c = S.COL_HALF
    bw = S.BEAM_SIZE
    dw = S.BRACE_SIZE

    parts = []

    # 1. Four main cylindrical corner columns + top/bottom bolted splice flanges
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx, cy = sx * c, sy * c
            parts.append(
                bd.Pos(cx, cy, 0)
                * bd.Cylinder(
                    S.COL_R, h, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
                )
            )
            # Bottom and top half-flange collars (stacked modules form crisp 3.0 mm splice rings)
            parts.append(
                bd.Pos(cx, cy, 0)
                * bd.Cylinder(
                    S.FLANGE_R,
                    S.FLANGE_HALF_H,
                    align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
                )
            )
            parts.append(
                bd.Pos(cx, cy, h - S.FLANGE_HALF_H)
                * bd.Cylinder(
                    S.FLANGE_R,
                    S.FLANGE_HALF_H,
                    align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
                )
            )

    # 2. Flat-faced rail mounting bosses on the +X face of the two front columns (flush at X = 67.0)
    for sy in (-1, 1):
        for zb in (18.0, 54.0, 90.0, 126.0):
            parts.append(
                bd.Pos(c, sy * c, zb)
                * bd.Box(
                    S.RAIL_BOSS_X - c,  # 7.0 mm: X from 60.0 to 67.0
                    11.0,
                    12.0,
                    align=(bd.Align.MIN, bd.Align.CENTER, bd.Align.CENTER),
                )
            )

    # 3. Horizontal perimeter box girders at bottom, mid, and top of module
    z_levels = (4.5, S.BAY_H, h - 4.5)
    span = 2.0 * c  # 120.0 mm center-to-center
    for zl in z_levels:
        # Rear (-X) and recessed Front (+X) girders along Y
        parts.append(bd.Pos(-c, 0, zl) * bd.Box(bw, span, bw))
        parts.append(bd.Pos(S.FRONT_BRACE_X, 0, zl) * bd.Box(bw, span, bw))
        # Short front tie stubs into front columns so recessed beam connects solidly
        for sy in (-1, 1):
            parts.append(
                bd.Pos(S.FRONT_BRACE_X, sy * c, zl)
                * bd.Box(c - S.FRONT_BRACE_X + 2.0, bw, bw, align=(bd.Align.MIN, bd.Align.CENTER, bd.Align.CENTER))
            )
        # Port (+Y) and Starboard (-Y) girders along X
        for sy in (-1, 1):
            parts.append(bd.Pos(0, sy * c, zl) * bd.Box(span, bw, bw))

    # 4. Diagonal X-bracing across both sub-bays on Rear (-X), Port (+Y), and Starboard (-Y) faces
    bays = ((z_levels[0], z_levels[1]), (z_levels[1], z_levels[2]))
    for zb0, zb1 in bays:
        zm = (zb0 + zb1) / 2.0
        # Rear (-X) X-brace + central gusset hub
        parts.append(_strut_between((-c, -c, zb0), (-c, c, zb1), dw, dw, (-1, 0, 0)))
        parts.append(_strut_between((-c, c, zb0), (-c, -c, zb1), dw, dw, (-1, 0, 0)))
        parts.append(bd.Pos(-c, 0, zm) * bd.Box(dw + 1.4, 9.5, 9.5))

        # Port (+Y) and Starboard (-Y) X-braces + central gusset hubs
        for sy in (-1, 1):
            y_face = sy * c
            parts.append(_strut_between((-c, y_face, zb0), (c, y_face, zb1), dw, dw, (0, sy, 0)))
            parts.append(_strut_between((c, y_face, zb0), (-c, y_face, zb1), dw, dw, (0, sy, 0)))
            parts.append(bd.Pos(0, y_face, zm) * bd.Box(9.5, dw + 1.4, 9.5))

        # Front (+X) recessed chevron K-bracing (strictly at X = FRONT_BRACE_X = 56.0, clear of rails)
        fx = S.FRONT_BRACE_X
        parts.append(_strut_between((fx, -c, zb0), (fx, 0, zb1), dw, dw, (1, 0, 0)))
        parts.append(_strut_between((fx, c, zb0), (fx, 0, zb1), dw, dw, (1, 0, 0)))
        parts.append(bd.Pos(fx, 0, zb1) * bd.Box(bw + 0.8, 10.0, bw + 1.4))

    # 5. Internal tie-beams anchoring the central elevator core at bottom and mid levels
    # Stop cleanly outside the core exterior cladding ribs (0.6 mm proud of core faces)
    core_x0 = S.CORE_X_CENTER - S.CORE_DX / 2.0 - 0.6  # -33.6
    core_yh = S.CORE_DY / 2.0 + 0.6                    # 18.6
    for zl in (z_levels[0], z_levels[1]):
        # Rear tie from X=-c (-60) to core_x0 (-33.6)
        for sy in (-1, 1):
            parts.append(
                bd.Pos(-c, sy * 14.0, zl)
                * bd.Box(
                    core_x0 - (-c),
                    3.2,
                    3.6,
                    align=(bd.Align.MIN, bd.Align.CENTER, bd.Align.CENTER),
                )
            )
        # Side ties from Y=+/-core_yh to Y=+/-c
        for sy in (-1, 1):
            tie_len = c - core_yh
            y_start = core_yh if sy > 0 else -c
            parts.append(
                bd.Pos(S.CORE_X_CENTER, y_start, zl)
                * bd.Box(
                    3.2,
                    tie_len,
                    3.6,
                    align=(bd.Align.CENTER, bd.Align.MIN, bd.Align.CENTER),
                )
            )

    frame = parts[0] + parts[1:]
    frame.label = "truss_frame"
    S.apply_material(frame, S.mat_tower_steel())
    return frame


def _build_elevator_core():
    """Central cladded elevator & utility shaft segment (Z: 0..145) with vertical blast ribs."""
    h = S.MODULE_H
    xc = S.CORE_X_CENTER
    dx, dy = S.CORE_DX, S.CORE_DY

    core = bd.Pos(xc, 0, 0) * bd.Box(
        dx, dy, h, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    # Subtle exterior vertical steel cladding ribs on Port/Starboard/Rear faces
    ribs = []
    for rx in (xc - 11.0, xc, xc + 11.0):
        for sy in (-1, 1):
            ribs.append(
                bd.Pos(rx, sy * (dy / 2.0), 0)
                * bd.Box(
                    1.6,
                    1.2,
                    h,
                    align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
                )
            )
    for ry in (-10.0, 0.0, 10.0):
        ribs.append(
            bd.Pos(xc - dx / 2.0, ry, 0)
            * bd.Box(1.2, 1.6, h, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        )
    # Recessed elevator access door frame on +X landing face
    door_cut = bd.Pos(xc + dx / 2.0 - 0.6, 0, 9.5) * bd.Box(
        2.0, 12.0, 22.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    core = (core + ribs) - door_cut
    core.label = "elevator_core"
    S.apply_material(core, S.mat_cladding())
    return core


def _build_service_deck():
    """Interior steel maintenance platform landing on the +X side of the elevator core."""
    # Spans between elevator core +X face (X = +5.0) and recessed front beam (X = 56.0 - 2.8 = 53.2)
    # Leaves 0.6 mm clearance on all sides so zero interference with core or truss beams!
    x0 = S.CORE_X_CENTER + S.CORE_DX / 2.0 + 0.6  # +5.6
    x1 = S.FRONT_BRACE_X - S.BEAM_SIZE / 2.0 - 0.8  # +52.4
    y_half = S.COL_HALF - S.BEAM_SIZE / 2.0 - 4.0   # 53.2
    z0 = 7.4  # Sits cleanly right on top of the bottom horizontal girder top (4.5 + 2.8 = 7.3 -> 7.4)

    deck = bd.Pos((x0 + x1) / 2.0, 0, z0) * bd.Box(
        x1 - x0,
        2.0 * y_half,
        2.0,
        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN),
    )
    # Ladder hatch cutout on Starboard-front corner of deck
    hatch = bd.Pos(x1 - 12.0, -y_half + 12.0, z0 - 0.5) * bd.Box(
        11.0, 11.0, 3.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
    )
    deck = deck - hatch
    deck.label = "service_deck"
    S.apply_material(deck, S.mat_deck_grating())
    return deck


@model
def tower_module():
    """One 14.5 m (145 mm) prefabricated SpaceX Starship launch tower truss module."""
    frame = _build_truss_frame()
    core = _build_elevator_core()
    deck = _build_service_deck()
    mod = bd.Compound(children=[frame, core, deck], label="tower_module")
    bb = mod.bounding_box()
    assert abs(bb.size.Z - S.MODULE_H) < 1e-4, bb
    return mod


def _build_guide_rail():
    """Continuous heavy I-beam vertical carriage guide rail (Z: 50..1355), back flush at X=67.0."""
    h = S.TOWER_TOP_Z - S.TOWER_BASE_Z  # 1305.0 mm
    fw = S.RAIL_FLANGE_W / 2.0          # 7.0
    ww = S.RAIL_WEB_W / 2.0             # 3.0
    pts = [
        (S.RAIL_BACK_X, -fw),
        (S.RAIL_WEB_X0, -fw),
        (S.RAIL_WEB_X0, -ww),
        (S.RAIL_WEB_X1, -ww),
        (S.RAIL_WEB_X1, -fw),
        (S.RAIL_FRONT_X, -fw),
        (S.RAIL_FRONT_X, fw),
        (S.RAIL_WEB_X1, fw),
        (S.RAIL_WEB_X1, ww),
        (S.RAIL_WEB_X0, ww),
        (S.RAIL_WEB_X0, fw),
        (S.RAIL_BACK_X, fw),
    ]
    prof = bd.Polygon(pts, align=None)
    rail = bd.Pos(0, 0, S.TOWER_BASE_Z) * bd.extrude(prof, h, dir=(0, 0, 1))
    return rail


def _build_cryo_risers():
    """Three insulated stainless steel cryogenic propellant/purge risers running up the -X face to SQD."""
    z0 = S.TOWER_BASE_Z
    z1 = S.SQD_Z + 12.0  # Rises cleanly up to SQD manifold level (837 mm)
    riser_h = z1 - z0
    names = ("cryo_lox_riser", "cryo_ch4_riser", "cryo_gn2_riser")
    pipes = []
    for name, (px, py, pr) in zip(names, S.CRYO_PIPES):
        pipe = (
            bd.Pos(px, py, z0)
            * bd.Cylinder(pr, riser_h, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        )
        pipe.label = name
        S.apply_material(pipe, S.mat_stainless())
        pipes.append(pipe)

    # Periodic horizontal steel pipe-clamp standoff rails anchored to rear girders
    # Spans cleanly from rear girder back face (X = -62.8) to pipe back (X = -68.8) -> zero pipe overlap!
    clamps = []
    for i in range(6):
        zc = S.TOWER_BASE_Z + i * S.MODULE_H + S.BAY_H
        bar = bd.Pos(-66.0, -42.0, zc) * bd.Box(
            5.8, 22.0, 2.4, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.CENTER)
        )
        clamps.append(bar)
    clamp_solid = bd.Compound(children=clamps, label="cryo_pipe_supports")
    for idx, cpart in enumerate(clamps):
        cpart.label = f"cryo_clamp_{idx + 1}"
        S.apply_material(cpart, S.mat_tower_steel())

    return [*pipes, clamp_solid]


def _build_rear_haul_cables():
    """Twin vertical drawworks haul cables rising along the -X face from lower sheaves to crown."""
    z0 = S.REAR_SHEAVE_Z
    z1 = S.CROWN_SHEAVE_Z
    h = z1 - z0
    cables = []
    for sy, side in ((1, "port"), (-1, "stbd")):
        cable = (
            bd.Pos(S.REAR_CABLE_X, sy * S.CABLE_Y, z0)
            * bd.Cylinder(
                S.CABLE_R, h, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)
            )
        )
        cable.label = f"rear_haul_cable_{side}"
        S.apply_material(cable, S.mat_cable())
        cables.append(cable)
    return cables


@model
def tower():
    """Complete 9-section structural steel Starship launch tower (Z: 50..1355 mm = 5..135.5 m)."""
    mod_proto = tower_module().shape
    modules = []
    for i in range(S.N_MODULES):
        zm = S.TOWER_BASE_Z + i * S.MODULE_H
        m = bd.Pos(0, 0, zm) * mod_proto
        m.label = f"module_{i + 1}"
        modules.append(m)

    # Twin continuous front vertical guide rails (shared geometry!)
    rail_proto = _build_guide_rail()
    S.apply_material(rail_proto, S.mat_guide_rail())
    rail_port = bd.Pos(0, S.COL_HALF, 0) * rail_proto
    rail_stbd = bd.Pos(0, -S.COL_HALF, 0) * rail_proto
    rail_port.label = "guide_rail_port"
    rail_stbd.label = "guide_rail_stbd"

    cryo_parts = _build_cryo_risers()
    cables = _build_rear_haul_cables()

    assy = bd.Compound(
        children=[*modules, rail_port, rail_stbd, *cryo_parts, *cables],
        label="tower",
    )
    return assy


if __name__ == "__main__":
    tower_module()
    tower()
