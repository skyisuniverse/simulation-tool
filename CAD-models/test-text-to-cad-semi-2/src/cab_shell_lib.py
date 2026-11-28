"""Shared @memo Class-A B-rep loft builders for the Tesla Semi cab & glazing.

Uses a single G2-smooth continuous symmetric spline wrapping seamlessly from left
sill over the roof crown to right sill (eliminating any shoulder/crown crease lines!),
intersected with a smooth aerodynamic front bow & bullet nose-rounding profile.
"""

import build123d as bd
from cad.build123d import memo

import cab_surface as CS


def _make_section_face(y, inset=0.0):
    """Build a seamless 2-edge symmetric closed Face on XZ shifted to Y.

    Edge 1: Flat bottom belly line from (+ws, zb) to (-ws, zb)
    Edge 2: ONE continuous G2-smooth Spline wrapping from (-ws, zb) up the left flank,
            smoothly across the crowned roof arch (0, zt), and down the right flank to (+ws, zb).
    Eliminates shoulder/roof tangent creases for true Class-A automotive reflections!
    """
    z_bot, z_top, w_sill, w_low, w_belt, w_mid, w_crown = CS.station_params(y)
    zb = z_bot + inset
    zt = z_top - inset
    h = max(zt - zb, 60.0)
    f = CS.PROFILE_FRACS

    ws = max(w_sill - inset, 25.0)
    wl = max(w_low - inset, 25.0)
    wb = max(w_belt - inset, 25.0)
    wm = max(w_mid - inset, 25.0)
    wc = max(w_crown - inset, 25.0)
    w_arch = wc * 0.56  # Smooth intermediate crown-shoulder control point for flat-topped arch

    r_pts = [
        (ws, zb),
        (wl, zb + f[1] * h),
        (wb, zb + f[2] * h),
        (wm, zb + f[3] * h),
        (wc, zb + f[4] * h),
        (w_arch, zb + 0.982 * h),
    ]
    # Continuous symmetric loop from left sill -> crown -> right sill
    skin_pts = [(-x, z) for x, z in r_pts] + [(0.0, zt)] + list(reversed(r_pts))

    plane = bd.Plane(origin=(0.0, y, 0.0), x_dir=(1.0, 0.0, 0.0), z_dir=(0.0, -1.0, 0.0))
    with bd.BuildSketch(plane) as sk:
        with bd.BuildLine():
            bd.Spline(*skin_pts)
            bd.Line((ws, zb), (-ws, zb))
        bd.make_face()
    return sk.sketch.face()


def _make_front_bow_prism(inset=0.0):
    """Analytical circular-arc plan-view bow + smooth chin rounding (zero spline ripples!)."""
    y_shift = inset
    x_max = 1400.0
    # Single analytical ThreePointArc gives a mirror-smooth cylindrical nose curvature!
    p_left = (-x_max, 345.0 + y_shift)
    p_mid = (0.0, y_shift)
    p_right = (x_max, 345.0 + y_shift)

    with bd.BuildSketch(bd.Plane.XY) as sk:
        with bd.BuildLine():
            bd.ThreePointArc(p_left, p_mid, p_right)
            bd.Line(p_right, (x_max, 5200.0))
            bd.Line((x_max, 5200.0), (-x_max, 5200.0))
            bd.Line((-x_max, 5200.0), p_left)
        bd.make_face()
    # Tall extrusion (6200 mm) so tilting 11 deg rearward never clips the 3960 mm rear roof crown!
    bow_xy = bd.Pos(0, 0, -200.0) * bd.extrude(sk.sketch.face(), amount=6200.0, dir=(0, 0, 1))
    bow_xy = bd.Pos(0, 0, 420.0) * bd.Rot(-11.0, 0, 0) * bd.Pos(0, 0, -420.0) * bow_xy

    # Smooth vertical chin rounding strictly below bumper split (Z <= 805) so silver nose stays pure NURBS!
    with bd.BuildSketch(bd.Plane.YZ) as sk_yz:
        with bd.BuildLine():
            pts_nose = [
                (44.0 + y_shift, 220.0),
                (4.0 + y_shift, 440.0),
                (2.0 + y_shift, 660.0),
                (18.0 + y_shift, 805.0),
            ]
            bd.Spline(*pts_nose)
            bd.Line(pts_nose[-1], (-220.0 + y_shift, 1120.0))
            bd.Line((-220.0 + y_shift, 1120.0), (-220.0 + y_shift, 4300.0))
            bd.Line((-220.0 + y_shift, 4300.0), (4300.0, 4300.0))
            bd.Line((4300.0, 4300.0), (4300.0, 220.0))
            bd.Line((4300.0, 220.0), pts_nose[0])
        bd.make_face()
    bow_yz = bd.Pos(-1450.0, 0.0, 0.0) * bd.extrude(sk_yz.sketch.face(), amount=2900.0, dir=(1, 0, 0))

    return bow_xy & bow_yz


@memo
def build_cab_envelope(inset=0.0):
    """Return the smooth Class-A outer (or inset inner) monocoque solid of the Tesla Semi cab."""
    faces = [_make_section_face(st[0], inset=inset) for st in CS.CAB_STATIONS]
    raw_loft = bd.loft(faces, ruled=False)
    bow = _make_front_bow_prism(inset=inset)
    result = raw_loft & bow
    return result


@memo
def build_windshield_aperture(margin=0.0):
    """Return the 3D cutting solid defining the expansive wraparound panoramic windshield opening."""
    y0 = 760.0 + margin
    y1 = 1810.0 - margin
    z0 = 1510.0 + margin * 0.8
    z1 = 2710.0 - margin * 0.8

    with bd.BuildSketch(bd.Plane.YZ) as sk_yz:
        with bd.BuildLine():
            bd.Polyline(
                (y0 - 40.0, z0),
                (y0 + 540.0, z0 - 20.0),
                (y1 + 310.0, z1 - 35.0),
                (y1 - 30.0, z1 + 40.0),
                close=True,
            )
        bd.make_face()
    prism_yz = bd.Pos(-1400.0, 0.0, 0.0) * bd.extrude(sk_yz.sketch.face(), amount=2800.0, dir=(1, 0, 0))

    # Wide wraparound planform leaving crisp structural A-pillars flanking the glass
    hw_front = 1090.0 - margin
    hw_back = 1020.0 - margin
    with bd.BuildSketch(bd.Plane.XY) as sk_xy:
        with bd.BuildLine():
            bd.Polyline(
                (-hw_front, 500.0),
                (hw_front, 500.0),
                (hw_back, 1980.0),
                (-hw_back, 1980.0),
                close=True,
            )
        bd.make_face()
    prism_xy = bd.Pos(0.0, 0.0, 1200.0) * bd.extrude(sk_xy.sketch.face(), amount=1900.0, dir=(0, 0, 1))

    aperture = prism_yz & prism_xy
    return aperture


@memo
def build_side_window_aperture(margin=0.0):
    """Return the 3D cutting solid for the iconic sleek Tesla Semi helmet-visor side windows.

    Features a crisp raked front A-pillar edge, sleek door drop-glass header, flat
    door beltline, and sharp stealth-fighter tapered rear quarter triangle behind the door!
    """
    m = margin
    with bd.BuildSketch(bd.Plane.YZ) as sk:
        with bd.BuildLine():
            p_fl = (1415.0 + m, 1510.0 + m)
            p_ft = (2025.0 + m, 2555.0 - m)
            p_rt = (2830.0 - m * 0.5, 2545.0 - m)
            # Sleek tapered stealth-fighter rear quarter corner!
            p_tip = (3315.0 - m * 1.4, 1900.0)
            p_rb = (2960.0 - m * 0.5, 1515.0 + m)

            bd.Line(p_fl, p_ft)
            bd.Spline(p_ft, (2425.0, 2575.0 - m), p_rt)
            bd.Line(p_rt, p_tip)
            bd.Line(p_tip, p_rb)
            bd.Line(p_rb, p_fl)
        bd.make_face()
    left_cut = bd.Pos(650.0, 0.0, 0.0) * bd.extrude(sk.sketch.face(), amount=750.0, dir=(1, 0, 0))
    right_cut = bd.Pos(-1400.0, 0.0, 0.0) * bd.extrude(sk.sketch.face(), amount=750.0, dir=(1, 0, 0))
    aperture = left_cut + right_cut
    return aperture
