"""Master dimensional specification and parametric surface cage for the production Tesla Cybertruck.

Coordinate convention (units: mm, +Z up, Z = 0 is the ground plane):
  -Y : forward (front bumper tip at Y_NOSE = -2841.5 mm)
  +Y : rearward (rear bumper tip at Y_REAR = +2841.5 mm)
  +X : vehicle left (US driver side, where the Gigawiper parks vertically)
  -X : vehicle right (passenger side)
  +Z : up (Medium / standard air suspension height = 1794.0 mm, ground clearance = 257.0 mm)

All dimensions follow Tesla's official production AWD / Cyberbeast Owner's Manual specs:
  Overall length            : 5683.0 mm (official 5682.9 mm / 223.74 in)
  Overall width excl mirrors: 2032.0 mm (official 2031.6 mm / 79.98 in)
  Overall width incl mirrors: 2413.0 mm (official 2413.3 mm / 95.01 in)
  Overall height (Medium)   : 1794.0 mm (official 1793.8 mm / 70.62 in)
  Wheelbase                 : 3635.0 mm (official 3635.0 mm / 143.11 in)
  Front overhang            :  878.3 mm (official  878.3 mm /  34.58 in)
  Rear overhang             : 1169.6 mm (official 1169.6 mm /  46.05 in)
  Ground clearance (Medium) :  257.0 mm (official  257.0 mm /  10.12 in)
  Tire size (285/65R20)     :  879.0 mm OD, 508.0 mm (20 in) rim, 276 mm mounted width
  Cargo bed (Vault)         : 1825.0 mm length x 1295.0 mm floor width, 728 mm front / 504 mm rear height
"""

from __future__ import annotations

import math

# ---------------------------------------------------------------------------
# Core official vehicle dimensions (mm)
# ---------------------------------------------------------------------------
LENGTH = 5683.0
WIDTH_EXCL_MIRRORS = 2032.0   # outer edge of trapezoidal fender flares (+/-1016 mm)
WIDTH_INCL_MIRRORS = 2413.0   # outer tip of triangular side mirrors (+/-1206.5 mm)
HEIGHT_MEDIUM = 1794.0        # roof apex height at Medium air suspension
GROUND_CLEARANCE = 257.0      # flat battery belly pan clearance at Medium setting

WHEELBASE = 3635.0
FRONT_OVERHANG = 878.3
REAR_OVERHANG = 1169.7        # 878.3 + 3635.0 + 1169.7 = 5683.0

# Longitudinal world-Y origin (centered longitudinally)
Y_NOSE = -LENGTH / 2.0        # -2841.5
Y_REAR = LENGTH / 2.0         # +2841.5


def s_to_y(s: float) -> float:
    """Convert distance from absolute front bumper tip s in [0, 5683] to world Y."""
    return Y_NOSE + s


# ---------------------------------------------------------------------------
# Wheels, tires, and suspension geometry
# ---------------------------------------------------------------------------
TIRE_OD = 879.0               # 285/65R20 nominal OD (34.6 in)
TIRE_RADIUS = TIRE_OD / 2.0   # 439.5 mm -> axle Z = 439.5 mm so tires rest on Z = 0
TIRE_WIDTH = 276.0            # mounted section width on 20x9J wheel
RIM_OD = 508.0                # 20 inches
RIM_RADIUS = RIM_OD / 2.0     # 254.0 mm

# Half-track placed so tire outer sidewall sits cleanly tucked 4 mm inside the +/-1016 mm flare lip
TRACK_HALF = 874.0            # track = 1748 mm (official 1772 mm; outer tire face at +/-1012 mm)
AXLE_Z = TIRE_RADIUS          # 439.5 mm

S_FRONT_AXLE = FRONT_OVERHANG                # 878.3
S_REAR_AXLE = FRONT_OVERHANG + WHEELBASE     # 4513.3
Y_FRONT_AXLE = s_to_y(S_FRONT_AXLE)          # -1963.2
Y_REAR_AXLE = s_to_y(S_REAR_AXLE)            # +1671.8

# ---------------------------------------------------------------------------
# Key longitudinal stations along s (mm from front bumper tip)
# ---------------------------------------------------------------------------
S_BUMPER_TIP = 0.0            # matte-black front bumper leading edge at X = 0
S_NOSE_CENTER = 85.0          # front stainless nose / DRL lightbar center (X = 0)
S_NOSE_CORNER = 200.0         # front stainless nose / DRL lightbar outer corner (X = +/-905)
S_COWL_CENTER = 850.0         # windshield base at X = 0 (sits right over front axle)
S_COWL_CORNER = 910.0         # windshield base at A-pillar outer corner
S_QUARTER_GLASS_FWD = 1070.0  # front apex of side triangular quarter window
S_FRONT_DOOR_SEAM = 1485.0    # front fender / front door vertical seam & mirror stalk
S_ROOF_APEX = 2470.0          # peak of the single-wedge roofline (Z = 1794.0)
S_B_PILLAR = 2630.0           # front door / rear door vertical seam
S_REAR_DOOR_SEAM = 3730.0     # rear door / rear quarter panel seam
S_CAB_REAR = 3765.0           # rear cab bulkhead / front of Vault bed
S_TAILGATE_TOP = 5635.0       # rear face of tailgate & sail pillar tips
S_REAR_BUMPER_END = 5683.0    # protruding rear bumper step trailing edge

# ---------------------------------------------------------------------------
# Key heights Z (mm above ground plane Z = 0)
# ---------------------------------------------------------------------------
Z_BELLY = GROUND_CLEARANCE    # 257.0 mm flat underbody skid plate
Z_ROCKER_BOT = 295.0          # bottom edge of side rocker cladding
Z_ROCKER_TOP = 365.0          # top edge of black rocker cladding / bottom of stainless doors
Z_FRONT_BUMPER_BOT = 465.0    # front bumper lower chin edge
Z_FRONT_BUMPER_TOP = 670.0    # top shelf of matte-black front bumper
Z_HEADLIGHT_SLOT_TOP = 735.0  # top of recessed dark headlight slot / bottom of stainless nose
Z_DRL_BOT = 1008.0            # bottom edge of front full-width DRL lightbar
Z_DRL_TOP = 1045.0            # top edge of front DRL lightbar / hood leading lip
Z_COWL = 1278.0               # windshield base height at cowl
Z_ROOF_APEX = HEIGHT_MEDIUM   # 1794.0 mm exact official Medium height
Z_TAILGATE_TOP = 1380.0       # rear top edge of tailgate / Vault roof slope termination
Z_TAILGATE_BOT = 650.0        # bottom edge of tailgate / top of rear bumper shelf
Z_REAR_BUMPER_BOT = 475.0     # bottom edge of rear bumper / diffuser

# Beltline crease endpoints (single razor-straight line from front corner to rear tailgate corner)
Z_BELT_FRONT = 1045.0         # at S_NOSE_CORNER = 200.0
Z_BELT_REAR = 1368.0          # at S_TAILGATE_TOP = 5635.0

# Cargo bed ("The Vault") internal specs
Z_BED_FLOOR = 865.0           # bed floor height in Medium mode (~34.1 in)
BED_INNER_HALF_W = 647.5      # 1295.0 mm official floor width
BED_S_FRONT = 3780.0          # front bulkhead inside bed
BED_S_REAR = 5605.0           # inner tailgate face (1825.0 mm bed floor length)
TONNEAU_HALF_W = 735.0        # 1470 mm (~57.9 in) retractable tonneau slat span

# ---------------------------------------------------------------------------
# Trapezoidal wheel arch geometry (identical silhouette profile fore & aft)
# ---------------------------------------------------------------------------
ARCH_TOP_Z = 965.0            # inner opening top (85.5 mm clearance above 879 mm tire)
ARCH_BOT_Z = 310.0            # opening meets lower rocker plane
ARCH_TOP_HALF_W = 345.0       # 690 mm wide flat top of trapezoid
ARCH_BOT_HALF_W = 595.0       # 1190 mm wide base at rocker height
FLARE_BAND_W = 64.0           # black plastic flare flange width around arch opening
FLARE_OUTER_X = WIDTH_EXCL_MIRRORS / 2.0  # 1016.0 mm exact outer flare face

# ---------------------------------------------------------------------------
# Panel gap & material thickness constants
# ---------------------------------------------------------------------------
PANEL_GAP = 4.5               # crisp dark shadow reveal between stainless panels
SKIN_THICK = 4.0              # rendered solid thickness for stainless outer panels
GLASS_THICK = 8.0             # glazing thickness
CANT_RAIL_W = 48.0            # width of stainless roof/A-pillar cant rail beside glass


# ---------------------------------------------------------------------------
# Master parametric surface functions (shared across ALL sub-assemblies)
# ---------------------------------------------------------------------------
def front_bow_ds(x: float) -> float:
    """Gentle curved plan-view sweepback of the front nose from X=0 to outer corners."""
    u = min(abs(x) / 905.0, 1.15)
    return (S_NOSE_CORNER - S_NOSE_CENTER) * (u ** 1.85)


def cowl_bow_ds(x: float) -> float:
    """Subtle plan-view sweepback of the hood trailing edge / windshield cowl."""
    u = min(abs(x) / 890.0, 1.15)
    return (S_COWL_CORNER - S_COWL_CENTER) * (u ** 1.85)


def z_belt(s: float) -> float:
    """Height Z of the iconic straight side beltline crease at station s."""
    t = (s - S_NOSE_CORNER) / (S_TAILGATE_TOP - S_NOSE_CORNER)
    return Z_BELT_FRONT + t * (Z_BELT_REAR - Z_BELT_FRONT)


def z_roof(s: float) -> float:
    """Height Z of the outer roof / windshield / hood / vault centerline profile at station s.

    Uses a crisp aerospace piecewise linear profile matching real measurements:
      - Hood:       (S_NOSE_CENTER=85, 1045) -> (S_COWL_CENTER=850, 1278)  [~16.9 deg]
      - Windshield: (S_COWL_CENTER=850, 1278) -> (S_ROOF_APEX=2470, 1794)  [~17.7 deg]
      - Vault/Roof: (S_ROOF_APEX=2470, 1794) -> (S_TAILGATE_TOP=5635, 1380) [-7.45 deg]
    """
    if s <= S_COWL_CENTER:
        t = (s - S_NOSE_CENTER) / (S_COWL_CENTER - S_NOSE_CENTER)
        return Z_DRL_TOP + t * (Z_COWL - Z_DRL_TOP)
    if s <= S_ROOF_APEX:
        t = (s - S_COWL_CENTER) / (S_ROOF_APEX - S_COWL_CENTER)
        return Z_COWL + t * (Z_ROOF_APEX - Z_COWL)
    t = (s - S_ROOF_APEX) / (S_TAILGATE_TOP - S_ROOF_APEX)
    return Z_ROOF_APEX + t * (Z_TAILGATE_TOP - Z_ROOF_APEX)


def z_roof_side(s: float) -> float:
    """Height Z of the outer cant-rail edge along the A-pillar, roof, and sail pillar.

    Slightly lower at the front cowl corner (1262 mm) and seamlessly merges to the
    tailgate upper corner (1368 mm) at the rear.
    """
    if s <= S_COWL_CORNER:
        t = (s - S_NOSE_CORNER) / (S_COWL_CORNER - S_NOSE_CORNER)
        return Z_BELT_FRONT + t * (1262.0 - Z_BELT_FRONT)
    if s <= S_ROOF_APEX:
        t = (s - S_COWL_CORNER) / (S_ROOF_APEX - S_COWL_CORNER)
        return 1262.0 + t * (Z_ROOF_APEX - 6.0 - 1262.0)
    if s <= S_CAB_REAR:
        t = (s - S_ROOF_APEX) / (S_CAB_REAR - S_ROOF_APEX)
        return (Z_ROOF_APEX - 6.0) + t * (z_roof(S_CAB_REAR) - 4.0 - (Z_ROOF_APEX - 6.0))
    # Rear sail pillar outer edge descends straight from C-pillar roof corner to rear corner
    t = (s - S_CAB_REAR) / (S_TAILGATE_TOP - S_CAB_REAR)
    z_c = z_roof(S_CAB_REAR) - 4.0
    return z_c + t * (Z_BELT_REAR - z_c)


def x_belt(s: float) -> float:
    """Half-width X of the stainless steel outer body along the beltline crease at station s.

    Planar slab sides across the cabin doors (985 mm), tapering linearly forward across the
    front fender (905 mm) and linearly rearward across the entire single-plane rear quarter
    from S_REAR_DOOR_SEAM (985 mm) to S_TAILGATE_TOP (920 mm) with zero mid-panel crease!
    """
    if s <= S_NOSE_CORNER:
        return 905.0
    if s <= S_FRONT_DOOR_SEAM:
        t = (s - S_NOSE_CORNER) / (S_FRONT_DOOR_SEAM - S_NOSE_CORNER)
        return 905.0 + t * (985.0 - 905.0)
    if s <= S_REAR_DOOR_SEAM:
        return 985.0
    if s <= S_TAILGATE_TOP:
        t = (s - S_REAR_DOOR_SEAM) / (S_TAILGATE_TOP - S_REAR_DOOR_SEAM)
        return 985.0 + t * (920.0 - 985.0)
    return 920.0


def x_rocker(s: float) -> float:
    """Half-width X of the lower stainless steel body at rocker height (Z_ROCKER_TOP = 365)."""
    # Slight 28 mm inward tuck relative to the beltline crease (~2 deg clean vertical stance)
    return x_belt(s) - 28.0


def x_roof(s: float) -> float:
    """Half-width X of the outer edge of the cant rail / sail pillar top crest at station s.

    Note: behind S_CAB_REAR (3765), the outer stainless sail-pillar spine sweeps linearly from
    X=735 mm (at the C-pillar roof edge) outward to X=920 mm (meeting the rear corner of the
    tailgate), while the inner Vault tonneau track stays parallel at X=735 mm!
    """
    if s <= S_NOSE_CORNER:
        return 905.0
    if s <= S_COWL_CORNER:
        t = (s - S_NOSE_CORNER) / (S_COWL_CORNER - S_NOSE_CORNER)
        return 905.0 + t * (875.0 - 905.0)
    if s <= S_ROOF_APEX:
        t = (s - S_COWL_CORNER) / (S_ROOF_APEX - S_COWL_CORNER)
        return 875.0 + t * (725.0 - 875.0)
    if s <= S_CAB_REAR:
        t = (s - S_ROOF_APEX) / (S_CAB_REAR - S_ROOF_APEX)
        return 725.0 + t * (TONNEAU_HALF_W - 725.0)
    if s <= S_TAILGATE_TOP:
        t = (s - S_CAB_REAR) / (S_TAILGATE_TOP - S_CAB_REAR)
        return TONNEAU_HALF_W + t * (920.0 - TONNEAU_HALF_W)
    return 920.0


def x_tonneau_inner(s: float) -> float:
    """Half-width X of the inner glass / tonneau opening edge (inside cant rail)."""
    if s <= S_COWL_CORNER:
        return x_roof(s) - 40.0
    if s <= S_ROOF_APEX:
        return x_roof(s) - CANT_RAIL_W
    if s <= S_CAB_REAR:
        return x_roof(s) - CANT_RAIL_W
    return TONNEAU_HALF_W - 15.0  # 720 mm clear slatted tonneau half-width (1440 mm)


def x_body_lower(s: float, z: float) -> float:
    """Half-width X on the lower planar body side (below beltline) at (s, z)."""
    zb = z_belt(s)
    t = (z - Z_ROCKER_TOP) / max(zb - Z_ROCKER_TOP, 1.0)
    t = max(-0.2, min(1.0, t))
    return x_rocker(s) + t * (x_belt(s) - x_rocker(s))


def x_body_upper(s: float, z: float) -> float:
    """Half-width X on the upper tumblehome side plane (between beltline and cant rail)."""
    zb = z_belt(s)
    zr = z_roof_side(s)
    if abs(zr - zb) < 1e-3:
        return x_belt(s)
    t = (z - zb) / (zr - zb)
    t = max(0.0, min(1.0, t))
    return x_belt(s) + t * (x_roof(s) - x_belt(s))


def arch_polygon_2d(s_axle: float, expand: float = 0.0) -> list[tuple[float, float]]:
    """Return 2D (Y, Z) vertices of the iconic Cybertruck trapezoidal wheel arch opening.

    When expand > 0, offsets the top and angled legs outward by `expand` mm to generate
    the matching trapezoidal matte-black fender flare outer profile.
    """
    yc = s_to_y(s_axle)
    # Leg slope vector from top corner to bottom corner
    dy = ARCH_BOT_HALF_W - ARCH_TOP_HALF_W  # 250 mm
    dz = ARCH_TOP_Z - ARCH_BOT_Z            # 655 mm
    hyp = math.hypot(dy, dz)
    # Horizontal expansion at a given Z for perpendicular offset `expand` on angled leg
    # and horizontal offset at top corner where horizontal & angled offsets meet:
    sec_alpha = hyp / dz                    # horizontal shift per unit perpendicular offset
    tan_alpha = dy / dz                     # slope dY/dZ of angled leg
    # For top edge shifted up by `expand` and angled leg shifted outward by `expand`:
    top_z = ARCH_TOP_Z + expand
    bot_z = ARCH_BOT_Z - (20.0 if expand == 0.0 else 0.0)
    # Where shifted leg intersects top_z:
    # Original leg: y_off(z) = ARCH_TOP_HALF_W + (ARCH_TOP_Z - z) * tan_alpha
    # Shifted leg:  y_off(z) = ARCH_TOP_HALF_W + expand * sec_alpha + (ARCH_TOP_Z - z) * tan_alpha
    top_half = ARCH_TOP_HALF_W + expand * (sec_alpha - tan_alpha)
    bot_half = ARCH_TOP_HALF_W + expand * sec_alpha + (ARCH_TOP_Z - bot_z) * tan_alpha
    return [
        (yc - bot_half, bot_z),
        (yc - top_half, top_z),
        (yc + top_half, top_z),
        (yc + bot_half, bot_z),
    ]
