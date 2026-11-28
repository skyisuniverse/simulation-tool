"""Master dimensional specification, surface stations, and materials for the
2nd-generation Tesla Roadster (production-intent design per tesla.com/roadster).

Coordinate system (mm, +Z up):
    X : Lateral  (+X = driver's left / LHD, -X = passenger's right)
    Y : Longitudinal (-Y = forward toward nose, +Y = rearward toward tail)
        So CAD Viewer `--camera front` looks straight at the car's front nose,
        `--camera back` looks straight at the rear diffuser & light bar,
        `--camera right` shows the driver-side profile with nose pointing left.
    Z : Vertical (Z = 0.0 is ground / tire contact plane)
"""

import math

# ---------------------------------------------------------------------------
# Master exterior envelope (mm)
# ---------------------------------------------------------------------------
WHEELBASE = 2825.0          # 111.2 in (published spec)
WIDTH = 2000.0              # ~79 in (published spec)
HALF_W = WIDTH / 2.0
LENGTH = 4560.0             # Derived from wheelbase + tight hypercar overhangs
HEIGHT = 1180.0             # Low-slung hypercar stance (W/H = 1.695)
Z_FLOOR = 105.0             # Flat ground-effect carbon floor clearance

Y_NOSE = -2280.0
Y_TAIL = 2280.0
FRONT_OVERHANG = 890.0
REAR_OVERHANG = LENGTH - WHEELBASE - FRONT_OVERHANG  # 845.0 mm

Y_FRONT_AXLE = Y_NOSE + FRONT_OVERHANG               # -1390.0 mm
Y_REAR_AXLE = Y_FRONT_AXLE + WHEELBASE               # +1435.0 mm

# ---------------------------------------------------------------------------
# Wheels, tires & brakes (20" front 295/30R20, 21" rear 335/30R21)
# ---------------------------------------------------------------------------
TIRE_F_RADIUS = 342.5       # Ø 685 mm
TIRE_F_RIM_R = 254.0        # 20 in rim (Ø 508 mm)
TIRE_F_WIDTH = 295.0
WHEEL_F_OUTER_X = 968.0     # Flush inside front fender arch
WHEEL_F_CENTER_X = WHEEL_F_OUTER_X - TIRE_F_WIDTH / 2.0  # 820.5 mm
ARCH_F_RADIUS = 374.0       # Tight ~31.5 mm radial fender clearance

TIRE_R_RADIUS = 364.0       # Ø 728 mm
TIRE_R_RIM_R = 266.5        # 21 in rim (Ø 533 mm)
TIRE_R_WIDTH = 335.0
WHEEL_R_OUTER_X = 982.0     # Flush inside muscular rear haunch
WHEEL_R_CENTER_X = WHEEL_R_OUTER_X - TIRE_R_WIDTH / 2.0  # 814.5 mm
ARCH_R_RADIUS = 396.0       # Tight ~32 mm radial fender clearance

ROTOR_F_RADIUS = 205.0      # Ø 410 mm carbon-ceramic disc
ROTOR_R_RADIUS = 195.0      # Ø 390 mm carbon-ceramic disc

# ---------------------------------------------------------------------------
# Door & canopy boundaries
# ---------------------------------------------------------------------------
# Door shutline runs cleanly behind the front wheel arch & side marker pod,
# up to the rear of the cockpit ahead of the fixed triangular rear quarter glass.
DOOR_Y_FRONT_BOT = -965.0
DOOR_Y_FRONT_TOP = -875.0
DOOR_Y_REAR_BOT = 445.0
DOOR_Y_REAR_TOP = 570.0
DOOR_GAP = 4.5              # Crisp exterior panel shutline gap (mm)
BODY_SKIN_THICKNESS = 46.0  # Structural exterior shell thickness

# Dihedral butterfly door hinge (driver's left +X; passenger -X mirrors X)
# Positioned at the outer-front door shutline corner so EVERY point on the door
# skin and frameless glass swings strictly outward, rearward, and upward away
# from the front fender, sill, and A-pillar throughout 0..60 deg travel.
DOOR_HINGE_POS_L = (972.0, -918.0, 725.0)
DOOR_HINGE_DIR_L = (0.68, -0.42, -0.60)
DOOR_OPEN_ANGLE = 58.0      # deg

# Active rear wing kinematics
WING_PIVOT_Y = 1610.0
WING_PIVOT_Z = 710.0
WING_DEPLOY_ANGLE = 21.0    # deg upward swing (~215 mm lift + downforce pitch)
WING_SPAN = 1740.0
WING_CHORD = 305.0
WING_STOWED_Y_LE = 1945.0
WING_STOWED_Y_TE = WING_STOWED_Y_LE + WING_CHORD  # 2250.0 mm

# ---------------------------------------------------------------------------
# Master outer body cross-section schedule (uniformly spaced in Y!)
# ---------------------------------------------------------------------------
# Each station defines a 10-edge symmetric XZ cross-section:
#   (y, x_floor, z_floor, x_rocker, z_rocker, x_shldr, z_shldr,
#    x_ridge, z_ridge, x_deck, z_deck, z_center, flank_bow, top_bow)
#
# Calibrated directly against official tesla.com/roadster front, rear, side,
# overhead, and 3/4 views:
#   - Razor-sharp low wedge nose at Z ~ 415 mm (DRL leading edge)
#   - Front fender crests arch cleanly over the 685 mm front tires (Z ~ 758 mm)
#   - Beltline dips to Z ~ 710 mm at A-pillar base, then rises in a dead-straight
#     wedge crease to Z ~ 835 mm at the Kamm tail
#   - Rear haunches flare to full 2,000 mm width over the 728 mm rear tires,
#     carrying two crisp triangular flying-buttress ridges flanking the tapered
#     dark fastback glass down to the low Kamm-tail deck (Z ~ 820 mm)

BODY_STATIONS = [
    #   y       x_flr  z_flr  x_rck  z_rck  x_shd  z_shd  x_rdg  z_rdg  x_dck  z_dck  z_ctr  f_bow  t_bow
    (-2360.0,   685.0, 128.0, 785.0, 195.0, 785.0, 396.0, 620.0, 416.0, 560.0, 405.0, 412.0,   6.0,   5.0),
    (-2040.0,   775.0, 112.0, 880.0, 198.0, 912.0, 535.0, 705.0, 568.0, 576.0, 518.0, 528.0,  10.0,  12.0),
    (-1720.0,   838.0, 106.0, 932.0, 200.0, 974.0, 668.0, 765.0, 708.0, 594.0, 622.0, 634.0,  14.0,  18.0),
    (-1400.0,   862.0, 105.0, 948.0, 202.0, 988.0, 742.0, 785.0, 772.0, 616.0, 702.0, 712.0,  15.0,  18.0),
    (-1080.0,   865.0, 105.0, 938.0, 204.0, 974.0, 724.0, 810.0, 742.0, 675.0, 714.0, 720.0,  12.0,  10.0),
    ( -760.0,   865.0, 105.0, 926.0, 208.0, 962.0, 726.0, 835.0, 742.0, 740.0, 726.0, 728.0,  10.0,   6.0),
    ( -440.0,   865.0, 105.0, 920.0, 214.0, 958.0, 740.0, 840.0, 756.0, 762.0, 742.0, 744.0,  10.0,   5.0),
    ( -120.0,   865.0, 105.0, 920.0, 222.0, 960.0, 756.0, 840.0, 772.0, 765.0, 758.0, 760.0,  10.0,   5.0),
    (  200.0,   865.0, 105.0, 924.0, 232.0, 968.0, 772.0, 830.0, 790.0, 745.0, 776.0, 778.0,  10.0,   6.0),
    (  520.0,   868.0, 105.0, 932.0, 248.0, 980.0, 788.0, 795.0, 816.0, 685.0, 798.0, 800.0,  12.0,   8.0),
    (  840.0,   868.0, 105.0, 946.0, 290.0, 994.0, 804.0, 695.0, 872.0, 565.0, 832.0, 834.0,  14.0,  12.0),
    ( 1160.0,   865.0, 106.0, 958.0, 325.0,1000.0, 820.0, 575.0, 918.0, 445.0, 862.0, 864.0,  16.0,  14.0),
    ( 1480.0,   848.0, 112.0, 952.0, 338.0, 994.0, 830.0, 470.0, 912.0, 355.0, 854.0, 855.0,  14.0,  12.0),
    ( 1800.0,   815.0, 125.0, 922.0, 345.0, 968.0, 836.0, 440.0, 862.0, 315.0, 838.0, 840.0,  10.0,   8.0),
    ( 2120.0,   765.0, 145.0, 882.0, 352.0, 935.0, 838.0, 485.0, 832.0, 320.0, 822.0, 824.0,   8.0,   5.0),
    ( 2360.0,   720.0, 162.0, 848.0, 358.0, 908.0, 838.0, 515.0, 822.0, 325.0, 814.0, 816.0,   6.0,   4.0),
]

# ---------------------------------------------------------------------------
# Gold Glazed teardrop glass canopy stations (uniformly spaced in Y!)
# ---------------------------------------------------------------------------
# Starts far forward over the rear of the front wheels (Y = -1240), rakes
# aggressively like a fighter jet up to Z = 1180 mm, and tapers smoothly
# into the iconic narrow fastback rear glass between the flying buttresses.
# Each entry: (y, half_w_base, z_base, half_w_roof, z_roof_edge, z_crown)
CANOPY_STATIONS = [
    (-1240.0, 608.0,  690.0, 565.0,  708.0,  718.0),
    ( -946.0, 710.0,  714.0, 595.0,  850.0,  876.0),
    ( -652.0, 762.0,  732.0, 590.0,  986.0, 1020.0),
    ( -358.0, 776.0,  748.0, 570.0, 1094.0, 1134.0),
    (  -64.0, 770.0,  764.0, 548.0, 1142.0, 1180.0),
    (  230.0, 742.0,  782.0, 522.0, 1132.0, 1166.0),
    (  524.0, 682.0,  804.0, 488.0, 1086.0, 1114.0),
    (  818.0, 575.0,  832.0, 442.0, 1022.0, 1044.0),
    ( 1112.0, 465.0,  858.0, 385.0,  956.0,  972.0),
    ( 1406.0, 378.0,  864.0, 332.0,  896.0,  906.0),
    ( 1700.0, 315.0,  846.0, 295.0,  852.0,  856.0),
]


def interp_station(stations, y):
    """Linearly interpolate a tuple of station numbers at longitudinal coord y."""
    if y <= stations[0][0]:
        return stations[0][1:]
    if y >= stations[-1][0]:
        return stations[-1][1:]
    for i in range(len(stations) - 1):
        y0, y1 = stations[i][0], stations[i + 1][0]
        if y0 <= y <= y1:
            t = (y - y0) / (y1 - y0)
            return tuple(
                stations[i][j] + t * (stations[i + 1][j] - stations[i][j])
                for j in range(1, len(stations[i]))
            )
    return stations[-1][1:]


def unit_vec(v):
    """Normalize a 3-tuple vector."""
    n = math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2])
    return (v[0] / n, v[1] / n, v[2] / n)


# ---------------------------------------------------------------------------
# Color & PBR Material Factories (called inside model bodies, never at import)
# ---------------------------------------------------------------------------
def apply_ano_white(shape):
    """Signature satin-matte aerospace 'Ano White' exterior finish."""
    from bd_materials import plastics

    m = plastics.abs_()
    m.pbr = m.pbr.override(
        roughness=0.26,
        metalness=0.06,
        clearcoat=0.38,
        clearcoat_roughness=0.16,
    )
    shape.material = m
    shape.color = "#e6e9ed"
    return shape


def apply_carbon_black(shape):
    """Satin-matte structural carbon fiber & lower aero trim."""
    from bd_materials import plastics

    m = plastics.cfrp()
    m.pbr = m.pbr.override(
        roughness=0.40,
        metalness=0.10,
        clearcoat=0.15,
        clearcoat_roughness=0.30,
    )
    shape.material = m
    shape.color = "#1b1d22"
    return shape


def apply_dark_gloss(shape):
    """Opaque gloss dark obsidian trim (front intake, wheel spokes, screens, housings)."""
    from bd_materials import plastics

    m = plastics.abs_()
    m.pbr = m.pbr.override(
        roughness=0.18,
        metalness=0.14,
        transmission=0.0,
        clearcoat=0.45,
        clearcoat_roughness=0.12,
    )
    shape.material = m
    shape.color = "#13151a"
    return shape


def apply_gold_glass(shape):
    """Copper/gold-glazed astronaut-visor canopy glass (clear transmissive look)."""
    from bd_materials import glass

    m = glass.soda_lime()
    m.pbr = m.pbr.override(
        roughness=0.04,
        metalness=0.12,
        ior=1.52,
        transmission=0.86,
        clearcoat=0.90,
        clearcoat_roughness=0.04,
    )
    shape.material = m
    shape.color = "#6b4f32"
    return shape


def apply_titanium(shape):
    """Bright machined aerospace titanium (thruster rims, A-pillar trim, center caps)."""
    from bd_materials import metals

    m = metals.titanium()
    m.pbr = m.pbr.override(roughness=0.16, metalness=0.90)
    shape.material = m
    shape.color = "#cfd4dc"
    return shape


def apply_dark_titanium(shape):
    """Dark anodized titanium / billet linkage & wing struts."""
    from bd_materials import metals

    m = metals.titanium()
    m.pbr = m.pbr.override(roughness=0.28, metalness=0.82)
    shape.material = m
    shape.color = "#32363c"
    return shape


def apply_bronze_titanium(shape):
    """Warm bronze-anodized titanium (wing underside & thruster nozzles)."""
    from bd_materials import metals

    m = metals.titanium()
    m.pbr = m.pbr.override(roughness=0.26, metalness=0.82)
    shape.material = m
    shape.color = "#8c7254"
    return shape


def apply_aero_blade(shape):
    """Satin bright silver-white aero wheel inserts."""
    from bd_materials import metals

    m = metals.aluminum()
    m.pbr = m.pbr.override(roughness=0.24, metalness=0.45)
    shape.material = m
    shape.color = "#d2d6dc"
    return shape


def apply_tire_rubber(shape):
    """Pirelli P Zero Trofeo semi-slick rubber."""
    from bd_materials import plastics

    m = plastics.rubber()
    m.pbr = m.pbr.override(roughness=0.80, metalness=0.0)
    shape.material = m
    shape.color = "#17181b"
    return shape


def apply_brake_rotor(shape):
    """Carbon-ceramic brake rotor disc."""
    from bd_materials import metals

    m = metals.mild_steel()
    m.pbr = m.pbr.override(roughness=0.42, metalness=0.55)
    shape.material = m
    shape.color = "#545860"
    return shape


def apply_red_led(shape):
    """Illuminated crimson LED rear light bar, wing endplates, and interior accents."""
    from bd_materials import plastics

    m = plastics.abs_()
    m.pbr = m.pbr.override(
        roughness=0.08,
        metalness=0.0,
        transmission=0.0,
        emissive="#ff1414",
        emissive_intensity=3.2,
    )
    shape.material = m
    shape.color = "#e61919"
    return shape


def apply_white_led(shape):
    """Illuminated crisp cool-white front DRL strip and hidden headlights."""
    from bd_materials import plastics

    m = plastics.abs_()
    m.pbr = m.pbr.override(
        roughness=0.08,
        metalness=0.0,
        transmission=0.0,
        emissive="#f4f8ff",
        emissive_intensity=3.0,
    )
    shape.material = m
    shape.color = "#f6f9ff"
    return shape


def apply_amber_led(shape):
    """Amber side-marker LED integrated into the side aero camera pod."""
    from bd_materials import plastics

    m = plastics.abs_()
    m.pbr = m.pbr.override(
        roughness=0.10,
        metalness=0.0,
        transmission=0.0,
        emissive="#ff7b00",
        emissive_intensity=2.8,
    )
    shape.material = m
    shape.color = "#ff8a1a"
    return shape


def apply_ultrawhite_interior(shape):
    """Ultrawhite interior seats, sculpted center console, and yoke rim."""
    from bd_materials import textile

    m = textile.leather()
    m.pbr = m.pbr.override(roughness=0.52, metalness=0.0)
    shape.material = m
    shape.color = "#edf0f3"
    return shape


def apply_alcantara(shape):
    """Dark graphite microsuede / Alcantara interior bolsters & dash shelf."""
    from bd_materials import textile

    m = textile.felt()
    m.pbr = m.pbr.override(roughness=0.88, metalness=0.0)
    shape.material = m
    shape.color = "#2e3136"
    return shape
