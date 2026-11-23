"""Master surface geometry and single source of truth for the Tesla Roadster (2nd gen).

Coordinate frame
----------------
    +X  forward (nose)          X = 0 at wheelbase centre
    +Y  car left (driver side)  Y = 0 at vehicle centreline
    +Z  up                      Z = 0 at ground contact plane
Units: millimetres (mm).

Overall target proportions (2nd-generation Tesla Roadster)
----------------------------------------------------------
    Length:       4,520 mm  (NOSE_X = +2270, TAIL_X = -2250)
    Wheelbase:    2,825 mm  (FRONT_AXLE_X = +1412.5, REAR_AXLE_X = -1412.5)
    Width:        1,996 mm  (HALF_WIDTH_MAX = 998 across muscular rear haunches)
    Height:       1,180 mm  (ROOF_Z = 1180 at Targa canopy peak)
    Wheels:       285/35ZR20 front (OD 707.5 mm), 325/30ZR21 rear (OD 728.4 mm)
"""

from __future__ import annotations

import math
from bisect import bisect_left

import build123d as bd

# ---------------------------------------------------------------------------
# Package & hard points
# ---------------------------------------------------------------------------

WHEELBASE = 2825.0
FRONT_AXLE_X = WHEELBASE / 2.0          # +1412.5
REAR_AXLE_X = -WHEELBASE / 2.0          # -1412.5

NOSE_X = 2270.0
TAIL_X = -2250.0
LENGTH = NOSE_X - TAIL_X                # 4520.0

# Staggered hypercar tires: 285/35ZR20 front, 325/30ZR21 rear
FRONT_RIM_D = 20.0 * 25.4               # 508.0
REAR_RIM_D = 21.0 * 25.4                # 533.4
FRONT_TYRE_W = 285.0
REAR_TYRE_W = 325.0
FRONT_TYRE_OD = FRONT_RIM_D + 2.0 * 0.35 * FRONT_TYRE_W   # 707.5
REAR_TYRE_OD = REAR_RIM_D + 2.0 * 0.30 * REAR_TYRE_W      # 728.4
FRONT_TYRE_R = FRONT_TYRE_OD / 2.0      # 353.75
REAR_TYRE_R = REAR_TYRE_OD / 2.0        # 364.20

# Tracks tucked flush inside front (988) and rear (998) fenders
FRONT_TRACK = 1612.0
REAR_TRACK = 1608.0
FRONT_HUB_Y = FRONT_TRACK / 2.0         # 806.0 (outer tire face = 948.5 < 988 fender!)
REAR_HUB_Y = REAR_TRACK / 2.0           # 804.0 (outer tire face = 966.5 < 998 fender!)

FRONT_HUB_Z = FRONT_TYRE_R              # 353.75
REAR_HUB_Z = REAR_TYRE_R                # 364.20

HALF_WIDTH_MAX = 998.0                  # 1996 mm overall width
ROOF_Z = 1180.0                         # 1180 mm overall height

# Wheel-arch cutouts
FRONT_ARCH_R = FRONT_TYRE_R + 24.0      # 377.75 (arch crest Z = 731.5)
REAR_ARCH_R = REAR_TYRE_R + 26.0        # 390.20 (arch crest Z = 754.4)
ARCH_INNER_Y = 530.0
ARCH_OUTER_Y = 1350.0

# Key panel split X coordinates (single source of truth across all modules)
HOOD_FRONT_X = 2005.0                   # Front bumper / hood leading shutline
HOOD_REAR_X = 865.0                     # Windshield cowl base (matches DOOR_FRONT_X cleanly)
BUMPER_FENDER_X = 1795.0                # Front bumper to front fender seam (meets arch!)
DOOR_FRONT_X = 865.0                    # Front fender / door shutline
DOOR_REAR_X = -515.0                    # Door / rear quarter shutline
TARGA_FRONT_X = 175.0                   # Windshield header / removable Targa glass front
TARGA_REAR_X = -455.0                   # Removable Targa glass rear / Targa roll hoop front
HOOP_REAR_X = -635.0                    # Targa roll hoop rear / fastback glass start
REAR_GLASS_END_X = -1880.0              # Fastback teardrop rear glass tip
SPOILER_FRONT_X = -1975.0               # Active deployable rear spoiler leading edge
SPOILER_REAR_X = -2215.0                # Active deployable rear spoiler trailing edge
SPOILER_HALF_W = 670.0                  # Active spoiler half-width

SHUTLINE_GAP = 4.5                      # Crisp automotive panel gap (mm)
BODY_SKIN_T = 14.0                      # Master outer-to-inner shell thickness
GLASS_T = 8.0                           # Canopy glazing thickness


# ---------------------------------------------------------------------------
# Smooth non-overshooting 1-D control curves (Catmull-Rom + Laplacian relax)
# ---------------------------------------------------------------------------


def _catmull(xs, vs, x):
    if x <= xs[0]:
        return vs[0]
    if x >= xs[-1]:
        return vs[-1]
    i = max(0, min(bisect_left(xs, x) - 1, len(xs) - 2))
    x0, x1 = xs[i], xs[i + 1]
    t = (x - x0) / (x1 - x0)
    p0 = vs[i - 1] if i > 0 else vs[i]
    p1, p2 = vs[i], vs[i + 1]
    p3 = vs[i + 2] if i + 2 < len(vs) else vs[i + 1]
    m1, m2 = 0.5 * (p2 - p0), 0.5 * (p3 - p1)
    t2, t3 = t * t, t * t * t
    return (
        (2 * t3 - 3 * t2 + 1) * p1
        + (t3 - 2 * t2 + t) * m1
        + (-2 * t3 + 3 * t2) * p2
        + (t3 - t2) * m2
    )


_DENSE_N = 601
_SMOOTH_PASSES = 20


class C1:
    """Smooth, non-overshooting C1 longitudinal profile curve over X."""

    def __init__(self, name, table, smooth_passes=_SMOOTH_PASSES):
        self.name = name
        xs = [p[0] for p in table]
        vs = [p[1] for p in table]
        if xs[0] > xs[-1]:
            xs, vs = xs[::-1], vs[::-1]
        self.x0, self.x1 = xs[0], xs[-1]
        span = self.x1 - self.x0
        self.step = span / (_DENSE_N - 1)
        dense = [
            _catmull(xs, vs, self.x0 + i * self.step) for i in range(_DENSE_N)
        ]
        for _ in range(smooth_passes):
            prev = dense[:]
            for i in range(1, _DENSE_N - 1):
                dense[i] = 0.25 * prev[i - 1] + 0.5 * prev[i] + 0.25 * prev[i + 1]
        self.dense = dense

    def __call__(self, x):
        if x <= self.x0:
            return self.dense[0]
        if x >= self.x1:
            return self.dense[-1]
        f = (x - self.x0) / self.step
        i = int(f)
        if i >= _DENSE_N - 1:
            return self.dense[-1]
        t = f - i
        return self.dense[i] * (1.0 - t) + self.dense[i + 1] * t


# ---------------------------------------------------------------------------
# Lower body longitudinal control curves (authentic 2nd-gen Tesla Roadster!)
# ---------------------------------------------------------------------------

# Centreline top: razor-low shark-nose sweeping CONTINUOUSLY upward into the
# windshield cowl (zero retro hump!), smooth deck, taut ducktail Kammback.
DECK_Z = C1("deck_z", [
    (2270, 345), (2210, 396), (2110, 476), (1950, 560), (1750, 626),
    (1550, 668), (1412, 692), (1180, 738), (920, 774), (620, 796),
    (260, 808), (-160, 824), (-580, 852), (-980, 876), (-1412, 886),
    (-1760, 872), (-2020, 854), (-2160, 854), (-2250, 864),
])

# Shoulder crest: taut low front-wheel brow (clears arch 731.5 cleanly at ~778),
# dipping gently into beltline and sweeping up into dramatic rear haunches!
CREST_Z = C1("crest_z", [
    (2270, 348), (2210, 412), (2110, 508), (1950, 616), (1750, 702),
    (1550, 762), (1412, 782), (1180, 786), (920, 792), (620, 802),
    (260, 814), (-160, 834), (-580, 866), (-980, 898), (-1412, 912),
    (-1760, 898), (-2020, 876), (-2160, 868), (-2250, 868),
])

# Subtle sculpted twin shoulder crown flanking the rear fastback teardrop
RIDGE_H = C1("ridge_h", [
    (2270, 0), (1412, 0), (920, 0), (200, 0), (-200, 0),
    (-600, 10), (-1020, 22), (-1412, 26), (-1780, 18), (-2060, 8), (-2250, 2),
])

# Planform half-width: smoothly curved aerodynamic shark-nose tip (no flat wall!),
# flush front fenders, sculpted hourglass waist at doors, wide rear haunches,
# smoothly tucked Kammback rear corners!
HALF_WIDTH = C1("half_width", [
    (2270, 165), (2235, 365), (2165, 585), (2045, 780), (1870, 908),
    (1650, 968), (1412, 988), (1160, 956), (880, 910), (560, 896),
    (200, 892), (-200, 904), (-600, 946), (-1000, 988), (-1412, 998),
    (-1740, 974), (-1980, 926), (-2140, 862), (-2215, 808), (-2250, 758),
], smooth_passes=14)

# Height of maximum width: taut shoulder highlight rising toward rear haunch
MAXW_Z = C1("maxw_z", [
    (2270, 314), (2210, 356), (2110, 422), (1950, 498), (1750, 558),
    (1550, 594), (1412, 608), (1180, 586), (920, 566), (620, 562),
    (260, 572), (-160, 596), (-580, 636), (-980, 684), (-1412, 718),
    (-1760, 722), (-2020, 708), (-2160, 694), (-2250, 678),
])

# Iconic Tesla Roadster lower-door sculpted scallop undercut
SCALLOP_IN = C1("scallop_in", [
    (2270, 0), (1412, 0), (1080, 10), (850, 56), (540, 68),
    (180, 64), (-180, 54), (-560, 34), (-920, 12), (-1260, 0), (-2250, 0),
])

# Rocker sill half-width (sleek lower aero crease)
SILL_Y = C1("sill_y", [
    (2270, 130), (2235, 310), (2165, 510), (2045, 695), (1870, 815),
    (1650, 868), (1412, 886), (1160, 858), (880, 838), (560, 834),
    (200, 834), (-200, 840), (-600, 866), (-1000, 896), (-1412, 908),
    (-1740, 886), (-1980, 842), (-2140, 782), (-2215, 732), (-2250, 686),
], smooth_passes=14)

# Rocker sill height (low knife-edge nose undercut -> flat wheelbase -> high diffuser sweep!)
SILL_Z = C1("sill_z", [
    (2270, 260), (2210, 224), (2110, 186), (1950, 162), (1750, 152),
    (1550, 148), (1412, 146), (1180, 144), (920, 142), (620, 142),
    (260, 142), (-160, 144), (-580, 150), (-980, 168), (-1412, 200),
    (-1760, 268), (-2020, 354), (-2160, 412), (-2250, 452),
])

# Underbody floor height (flat EV battery skateboard between axles, aggressive rear diffuser ramp)
FLOOR_Z = C1("floor_z", [
    (2270, 240), (2210, 192), (2110, 146), (1950, 122), (1750, 116),
    (1550, 114), (1412, 114), (1180, 112), (920, 112), (620, 112),
    (260, 112), (-160, 112), (-580, 114), (-980, 122), (-1412, 152),
    (-1760, 224), (-2020, 316), (-2160, 376), (-2250, 414),
])

FLOOR_Y = C1("floor_y", [
    (2270, 95), (2235, 245), (2165, 415), (2045, 560), (1870, 668),
    (1650, 715), (1412, 730), (1160, 712), (880, 700), (560, 696),
    (200, 696), (-200, 700), (-600, 720), (-1000, 744), (-1412, 756),
    (-1740, 738), (-1980, 698), (-2140, 646), (-2215, 602), (-2250, 564),
], smooth_passes=14)


# ---------------------------------------------------------------------------
# Sweeping teardrop glass canopy curves (windshield -> Targa -> fastback glass)
# ---------------------------------------------------------------------------

CANOPY_X0 = 960.0
CANOPY_X1 = -1940.0

CANOPY_TOP_Z = C1("canopy_top_z", [
    (960, 766), (780, 886), (560, 1018), (320, 1126), (90, 1172),
    (-100, 1180), (-300, 1176), (-500, 1158), (-740, 1118),
    (-1000, 1062), (-1280, 998), (-1540, 938), (-1760, 892), (-1940, 862),
], smooth_passes=16)

CANOPY_HW = C1("canopy_hw", [
    (960, 575), (780, 640), (560, 690), (320, 718), (90, 728),
    (-100, 728), (-300, 716), (-500, 690), (-740, 642),
    (-1000, 570), (-1280, 480), (-1540, 380), (-1760, 276), (-1940, 175),
], smooth_passes=14)

# Subtle double-bubble aerodynamic contour over the removable Targa roof
CANOPY_BUBBLE = C1("canopy_bubble", [
    (960, 0), (340, 0), (140, 6), (-100, 9), (-340, 8), (-560, 3), (-880, 0), (-1940, 0),
], smooth_passes=16)

CANOPY_MAXW_Z = C1("canopy_maxw_z", [
    (960, 704), (780, 742), (560, 782), (320, 818), (90, 842),
    (-100, 856), (-300, 868), (-500, 878), (-740, 882),
    (-1000, 876), (-1280, 862), (-1540, 840), (-1760, 822), (-1940, 804),
], smooth_passes=16)

CANOPY_BASE_Z = C1("canopy_base_z", [
    (960, 638), (780, 668), (560, 702), (320, 732), (90, 752),
    (-100, 766), (-300, 778), (-500, 788), (-740, 794),
    (-1000, 792), (-1280, 782), (-1540, 766), (-1760, 752), (-1940, 738),
], smooth_passes=16)


# ---------------------------------------------------------------------------
# Cross-section generators
# ---------------------------------------------------------------------------

_TOP_SAMPLES = 7


def _top_blend(t):
    return (t * t * (3.0 - 2.0 * t)) * 0.45 + (t ** 1.55) * 0.55


def body_section_bands(x):
    """Half-section at station X as (top_band, flank_band, under_band)."""
    deck = DECK_Z(x)
    crest = CREST_Z(x)
    hw = HALF_WIDTH(x)
    mz = MAXW_Z(x)
    sy, sz = SILL_Y(x), SILL_Z(x)
    fy, fz = FLOOR_Y(x), FLOOR_Z(x)
    ridge = RIDGE_H(x)
    scallop = SCALLOP_IN(x)

    crest_y = 0.905 * hw
    top = []
    for i in range(_TOP_SAMPLES + 1):
        t = i / _TOP_SAMPLES
        z = deck + (crest - deck) * _top_blend(t)
        if ridge > 0.05:
            z += ridge * math.exp(-(((t - 0.72) / 0.28) ** 2))
        top.append((crest_y * t, z))

    mid_flank_y = 0.56 * hw + 0.44 * sy - scallop
    mid_flank_z = 0.50 * mz + 0.50 * sz
    flank = [
        top[-1],
        (hw, mz),
        (mid_flank_y, mid_flank_z),
        (sy, sz),
    ]

    under = [
        (sy, sz),
        (0.55 * sy + 0.45 * fy, fz + 0.46 * (sz - fz)),
        (fy, fz),
        (0.55 * fy, fz - 1.5),
        (0.0, fz - 2.0),
    ]
    return top, flank, under


def canopy_section_points(x):
    top = CANOPY_TOP_Z(x)
    hw = CANOPY_HW(x)
    mz = CANOPY_MAXW_Z(x)
    bz = CANOPY_BASE_Z(x)
    bub = CANOPY_BUBBLE(x)

    z0 = top - bub
    z1 = top + 0.15 * bub - 0.06 * (top - mz)
    return [
        (0.0, z0),
        (0.36 * hw, z1),
        (0.68 * hw, top - 0.28 * (top - mz)),
        (0.89 * hw, top - 0.62 * (top - mz)),
        (hw, mz),
        (0.985 * hw, bz + 0.45 * (mz - bz)),
        (0.94 * hw, bz),
        (0.54 * hw, bz - 28.0),
        (0.0, bz - 36.0),
    ]


def _dir(a, b):
    dy, dz = b[0] - a[0], b[1] - a[1]
    n = math.hypot(dy, dz) or 1.0
    return (dy / n, dz / n)


def _mirrored_face(bands, x):
    edges = []
    last = len(bands) - 1
    for i, pts in enumerate(bands):
        t0 = (1, 0) if i == 0 else None
        t1 = (-1, 0) if i == last else None
        if t0 and t1:
            edges.append(bd.Spline(*pts, tangents=(t0, t1)))
        elif t0:
            edges.append(bd.Spline(*pts, tangents=(t0, _dir(pts[-2], pts[-1]))))
        elif t1:
            edges.append(bd.Spline(*pts, tangents=(_dir(pts[0], pts[1]), t1)))
        else:
            edges.append(bd.Spline(*pts))
    half = edges[0]
    for e in edges[1:]:
        half = half + e
    return bd.Plane.YZ.offset(x) * bd.make_face(half + bd.mirror(half, bd.Plane.YZ))


def body_section_face(x):
    return _mirrored_face(body_section_bands(x), x)


def canopy_section_face(x):
    return _mirrored_face([canopy_section_points(x)], x)


def _inset_band(points, d):
    n = len(points)
    out = []
    for i, (y, z) in enumerate(points):
        a = points[max(i - 1, 0)]
        b = points[min(i + 1, n - 1)]
        dy, dz = b[0] - a[0], b[1] - a[1]
        m = math.hypot(dy, dz) or 1.0
        ny, nz = dz / m, -dy / m
        out.append((y + ny * d, z + nz * d))
    out[0] = (0.0, out[0][1])
    out[-1] = (0.0, out[-1][1])
    return out


def body_section_face_inset(x, d=BODY_SKIN_T):
    top, flank, under = body_section_bands(x)
    whole = top + flank[1:] + under[1:]
    inner = _inset_band(whole, d)
    nt, nf = len(top), len(flank) - 1
    return _mirrored_face(
        [inner[:nt], inner[nt - 1:nt + nf], inner[nt + nf - 1:]], x
    )


def canopy_section_face_inset(x, d=GLASS_T):
    return _mirrored_face([_inset_band(canopy_section_points(x), d)], x)


BODY_STATIONS = [
    2270, 2245, 2200, 2130, 2030, 1890, 1730, 1570, 1412, 1240,
    1050, 880, 680, 460, 230, 0, -230, -460, -700, -940,
    -1180, -1412, -1640, -1860, -2040, -2160, -2220, -2250,
]

CANOPY_STATIONS = [
    960, 850, 720, 580, 430, 280, 130, -20, -170, -320,
    -470, -630, -800, -980, -1160, -1340, -1520, -1690, -1830, -1940,
]


def body_master():
    return bd.loft([body_section_face(x) for x in BODY_STATIONS])


def body_master_inner(d=BODY_SKIN_T):
    raw = bd.loft([body_section_face_inset(x, d) for x in BODY_STATIONS])
    # Trim the nose tip cleanly so the shark-nose leading cap stays closed & watertight
    return raw - box_between(NOSE_X - d - 4.0, NOSE_X + 25.0, -1200.0, 1200.0, -100.0, 1200.0)


def canopy_master():
    return bd.loft([canopy_section_face(x) for x in CANOPY_STATIONS])


def canopy_master_inner(d=GLASS_T):
    return bd.loft([canopy_section_face_inset(x, d) for x in CANOPY_STATIONS])


def arch_cutter(x, z, radius, side):
    length = ARCH_OUTER_Y - ARCH_INNER_Y
    y_mid = side * (ARCH_INNER_Y + length / 2.0)
    cyl = bd.Rot(-90, 0, 0) * bd.Cylinder(radius=radius, height=length)
    return bd.Pos(x, y_mid, z) * cyl


def arch_cutters():
    out = []
    for side in (1, -1):
        out.append(arch_cutter(FRONT_AXLE_X, FRONT_HUB_Z, FRONT_ARCH_R, side))
        out.append(arch_cutter(REAR_AXLE_X, REAR_HUB_Z, REAR_ARCH_R, side))
    return out


def rear_transom_cap(thickness=16.0):
    """Exact rear transom closing wall flush with the Kammback tail (zero Booleans)."""
    return bd.loft([body_section_face(TAIL_X), body_section_face(TAIL_X + thickness)], ruled=True)


def body_skin():
    """True 14 mm thin-walled single-shell body skin with closed shark-nose cap."""
    # Combine inner cavity with underfloor opening FIRST so OCCT builds a 1-shell manifold solid!
    open_void = body_master_inner(BODY_SKIN_T) + box_between(
        -1680.0, 1780.0, -740.0, 740.0, 40.0, 260.0
    )
    shell = body_master() - open_void
    shell = shell - arch_cutters()
    assert shell.volume < 360e6, f"body_skin unexpectedly solid: {shell.volume / 1e6:.1f} L"
    return shell


def canopy_glass_shell():
    return (canopy_master() - canopy_master_inner()) - body_master()


def wheel_specs():
    """Return (name, x, y, z, side, tyre_r, tyre_w, rim_d) for all four corners."""
    return [
        ("front_left",  FRONT_AXLE_X,  FRONT_HUB_Y, FRONT_HUB_Z,  1, FRONT_TYRE_R, FRONT_TYRE_W, FRONT_RIM_D),
        ("front_right", FRONT_AXLE_X, -FRONT_HUB_Y, FRONT_HUB_Z, -1, FRONT_TYRE_R, FRONT_TYRE_W, FRONT_RIM_D),
        ("rear_left",   REAR_AXLE_X,   REAR_HUB_Y,  REAR_HUB_Z,   1, REAR_TYRE_R,  REAR_TYRE_W,  REAR_RIM_D),
        ("rear_right",  REAR_AXLE_X,  -REAR_HUB_Y,  REAR_HUB_Z,  -1, REAR_TYRE_R,  REAR_TYRE_W,  REAR_RIM_D),
    ]


def box_between(x0, x1, y0, y1, z0, z1):
    return bd.Pos((x0 + x1) / 2.0, (y0 + y1) / 2.0, (z0 + z1) / 2.0) * bd.Box(
        abs(x1 - x0), abs(y1 - y0), abs(z1 - z0)
    )
