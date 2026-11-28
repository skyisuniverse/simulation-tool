"""Parametric mathematical Class-A surface definition for the original Tesla Semi cab.

Pure Python math only (no build123d imports at module level) so both `cab.py`
and `glazing.py` query the exact same loft stations, outer skin coordinates,
bow curve, and surface normals for flush fit with controlled clearances.
"""

import math


# 12 evenly spaced longitudinal Y stations (360 mm uniform pitch => zero loft oscillation!)
# Tuned specifically to the authentic original 2017/2022 Tesla Semi proportions:
#   - Smooth rounded bullet nose rising gracefully into steeply raked panoramic windshield
#   - Graceful convex parabolic roof fairing arching seamlessly to full 3,960 mm (13 ft) height
#   - Muscular front wheel fenders (2,520 mm wide) with sleek tumblehome cabin greenhouse
#   - Full 2,540 mm trailer-matching rear cab extenders
PROFILE_FRACS = (0.04, 0.24, 0.48, 0.72, 0.91)

CAB_STATIONS = (
    #   y       z_bot  z_top   w_sill  w_low   w_belt  w_mid   w_crown
    (   0.0,    272.0,  785.0,  925.0, 1055.0, 1035.0,  895.0,  615.0),
    ( 360.0,    280.0, 1185.0, 1095.0, 1208.0, 1200.0, 1050.0,  760.0),
    ( 720.0,    290.0, 1475.0, 1160.0, 1235.0, 1238.0, 1125.0,  845.0),
    (1080.0,    296.0, 1895.0, 1178.0, 1240.0, 1240.0, 1122.0,  870.0),
    (1440.0,    300.0, 2320.0, 1184.0, 1240.0, 1234.0, 1120.0,  905.0),
    (1800.0,    300.0, 2730.0, 1186.0, 1242.0, 1234.0, 1138.0,  950.0),
    (2160.0,    300.0, 3110.0, 1188.0, 1244.0, 1240.0, 1170.0, 1012.0),
    (2520.0,    300.0, 3440.0, 1192.0, 1246.0, 1244.0, 1200.0, 1075.0),
    (2880.0,    300.0, 3705.0, 1196.0, 1248.0, 1248.0, 1225.0, 1135.0),
    (3240.0,    300.0, 3878.0, 1198.0, 1250.0, 1250.0, 1240.0, 1176.0),
    (3600.0,    300.0, 3950.0, 1200.0, 1250.0, 1252.0, 1246.0, 1196.0),
    (3960.0,    300.0, 3960.0, 1200.0, 1250.0, 1252.0, 1248.0, 1204.0),
)


def _catmull_interp(xs, ys, x):
    """Smooth piecewise Catmull-Rom Hermite interpolation along station Y values."""
    if x <= xs[0]:
        return ys[0]
    if x >= xs[-1]:
        return ys[-1]
    for i in range(len(xs) - 1):
        if xs[i] <= x <= xs[i + 1]:
            t = (x - xs[i]) / (xs[i + 1] - xs[i])
            y0 = ys[max(0, i - 1)]
            y1 = ys[i]
            y2 = ys[i + 1]
            y3 = ys[min(len(ys) - 1, i + 2)]
            m1 = 0.5 * (y2 - y0) if i > 0 else (y2 - y1)
            m2 = 0.5 * (y3 - y1) if i < len(xs) - 2 else (y2 - y1)
            t2 = t * t
            t3 = t2 * t
            return (
                (2 * t3 - 3 * t2 + 1) * y1
                + (t3 - 2 * t2 + t) * m1
                + (-2 * t3 + 3 * t2) * y2
                + (t3 - t2) * m2
            )
    return ys[-1]


_YS = tuple(s[0] for s in CAB_STATIONS)


def station_params(y):
    """Return smoothly interpolated (z_bot, z_top, w_sill, w_low, w_belt, w_mid, w_crown) at Y."""
    return tuple(
        _catmull_interp(_YS, tuple(s[col] for s in CAB_STATIONS), y)
        for col in range(1, 8)
    )


def z_top_at(y):
    """Centerline top height Z(Y) along the nose, windshield, and aero roof fairing."""
    return _catmull_interp(_YS, tuple(s[2] for s in CAB_STATIONS), y)


def z_bot_at(y):
    """Bottom sill height Z(Y)."""
    return _catmull_interp(_YS, tuple(s[1] for s in CAB_STATIONS), y)


def half_width_at(y, z, inset=0.0):
    """Evaluate approximate outer half-width |X| of the cab skin at (Y, Z)."""
    z_bot, z_top, w_sill, w_low, w_belt, w_mid, w_crown = station_params(y)
    zb = z_bot + inset
    zt = z_top - inset
    h = max(zt - zb, 50.0)
    if z <= zb or z >= zt:
        return 0.0
    f = (z - zb) / h
    fs = (0.0, *PROFILE_FRACS, 1.0)
    ws = (
        max(w_sill - inset, 0.0),
        max(w_sill - inset, 0.0),
        max(w_low - inset, 0.0),
        max(w_belt - inset, 0.0),
        max(w_mid - inset, 0.0),
        max(w_crown - inset, 0.0),
        0.0,
    )
    return max(_catmull_interp(fs, ws, f), 0.0)


def nose_slope_deg(y):
    """Slope angle (degrees from horizontal) of the centerline surface Z_top(Y) at Y."""
    dy = 10.0
    dz = z_top_at(y + dy) - z_top_at(y - dy)
    return math.degrees(math.atan2(dz, 2.0 * dy))
