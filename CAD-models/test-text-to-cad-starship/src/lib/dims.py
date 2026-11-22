"""Master 1:1 scale engineering dimensions (mm, +Z up) for SpaceX Starship & Super Heavy Booster.

Configuration: Block 1 / Flight 5 full-stack architecture (Booster 12 + Ship 30).
- Coordinate convention:
  +Z: vehicle longitudinal axis (up), Z = 0 at Super Heavy Raptor 2 nozzle exit plane.
  -Y: Starship windward (belly / TPS ceramic heat shield) side.
  +Y: Starship leeward (dorsal / bare stainless steel / tower raceway) side.
  +X / -X: Starboard and Port lateral flap & Mechazilla catch-pin axes.
"""

import math

# =============================================================================
# Primary Stack Envelope
# =============================================================================
HULL_D = 9000.0
HULL_R = HULL_D / 2.0  # 4500.0 mm

# Z-stations along the full 121.3 m stack
Z_NOZZLE_EXIT = 0.0
Z_SH_SKIRT_BOT = 400.0        # Super Heavy aft engine protective skirt rim
Z_SH_THRUST_DECK = 3100.0     # Super Heavy engine mounting deck / thrust dome base
Z_SH_BODY_TOP = 69200.0       # Top of Super Heavy main 9 m propellant barrel
HSR_HEIGHT = 1800.0           # Hot-Stage Ring height
Z_HSR_BOT = Z_SH_BODY_TOP     # 69200.0 mm
Z_HSR_TOP = Z_HSR_BOT + HSR_HEIGHT  # 71000.0 mm (Stage separation interface)

SHIP_HEIGHT = 50300.0         # Starship upper stage total height (including 55 mm nose TPS cap)
Z_SHIP_BOT = Z_HSR_TOP        # 71000.0 mm
Z_SHIP_TOP = Z_SHIP_BOT + SHIP_HEIGHT  # 121300.0 mm (Total stack height = 121.3 m)

# =============================================================================
# Raptor 2 Sea-Level (SL) & Raptor Vacuum (RVac) Engines
# =============================================================================
RAPTOR_SL_HEIGHT = 3100.0
RAPTOR_SL_EXIT_D = 1160.0     # Compact Raptor 2 exit bell fitting 20-engine outer ring cleanly
RAPTOR_SL_EXIT_R = RAPTOR_SL_EXIT_D / 2.0  # 580.0 mm
RAPTOR_SL_THROAT_R = 165.0
RAPTOR_SL_WALL = 32.0
RAPTOR_SL_BELL_H = 1800.0     # Throat to exit rim

RAPTOR_VAC_HEIGHT = 3900.0
RAPTOR_VAC_EXIT_D = 2300.0    # Large vacuum expansion nozzle
RAPTOR_VAC_EXIT_R = RAPTOR_VAC_EXIT_D / 2.0  # 1150.0 mm
RAPTOR_VAC_THROAT_R = 175.0
RAPTOR_VAC_WALL = 38.0
RAPTOR_VAC_BELL_H = 2650.0

# =============================================================================
# Super Heavy Booster Details
# =============================================================================
SH_SKIRT_WALL = 80.0
SH_SKIRT_IN_R = HULL_R - SH_SKIRT_WALL  # 4420.0 mm

# 33-engine cluster layout (20 outer + 10 middle + 3 center)
SH_OUTER_COUNT = 20
SH_OUTER_RING_R = 3820.0      # outer tip 4400 < 4420; chord 1195.2 > 1160 (35.2 mm gap)
SH_MID_COUNT = 10
SH_MID_RING_R = 2320.0        # chord 1433.8 mm; radial gap to outer = 340 mm
SH_INNER_COUNT = 3
SH_INNER_RING_R = 850.0       # chord 1472.2 mm; radial gap to mid = 310 mm
SH_DIVIDER_RING_R = 3070.0    # Circular heat-shield baffle between outer 20 & inner 13

# Barrel weld rings (3.6 m dual-ring segments for crisp CAD appearance)
RING_STEP = 3600.0
WELD_GROOVE_DEPTH = 10.0
WELD_GROOVE_HALF_H = 18.0

# Super Heavy Aerodynamic Chines (2 opposite COPV/manifold fairings on ±X)
CHINE_Z_BOT = 1200.0
CHINE_Z_TOP = 37500.0
CHINE_WIDTH = 1350.0          # Tangential width at base
CHINE_PROTRUSION = 580.0      # Radial protrusion past HULL_R

# Super Heavy Catch / Lifting Pins (±X, centered in 120° grid-fin corridors)
SH_CATCH_PIN_Z = 62600.0
SH_CATCH_PIN_R = 240.0
SH_CATCH_PIN_LEN = 980.0

# Super Heavy Grid Fins (4 waffle fins, asymmetric 60°/120° Booster 12 layout)
GRID_FIN_Z = 65600.0
GRID_FIN_ANGLES_DEG = (60.0, 120.0, 240.0, 300.0)
GRID_FIN_ROOT_OFFSET = 460.0  # Pivot shoulder beyond HULL_R (at R = 4960 mm)
GRID_FIN_SPAN = 3850.0        # Radial extent of waffle blade
GRID_FIN_WIDTH = 3100.0       # Tangential width at outer tip
GRID_FIN_ROOT_WIDTH = 2450.0  # Slightly tapered at root
GRID_FIN_DEPTH = 540.0        # Axial height (Z thickness of waffle cells)
GRID_FIN_FRAME_T = 110.0      # Perimeter structural frame thickness
GRID_FIN_RIB_T = 36.0         # Internal diagonal waffle blade thickness

# =============================================================================
# Hot-Stage Ring (HSR)
# =============================================================================
HSR_WALL = 120.0
HSR_IN_R = HULL_R - HSR_WALL  # 4380.0 mm
HSR_BOT_FLANGE_H = 280.0
HSR_TOP_FLANGE_H = 280.0
HSR_PILLAR_COUNT = 24
HSR_PILLAR_W = 240.0          # Tangential width of each structural vent pillar
HSR_DOME_BASE_Z = Z_HSR_BOT + 120.0
HSR_DOME_PEAK_Z = Z_HSR_BOT + 1220.0  # Safely below Ship RVac exits (71,500 mm)

# =============================================================================
# Starship Upper Stage (50.3 m)
# =============================================================================
SHIP_SKIRT_H = 4500.0         # Aft skirt Z = 71,000..75,500
SHIP_SKIRT_WALL = 100.0
SHIP_SKIRT_IN_R = HULL_R - SHIP_SKIRT_WALL  # 4400.0 mm
Z_SHIP_THRUST_DECK = Z_SHIP_BOT + 4400.0    # 75400.0 mm
Z_SHIP_RVAC_EXIT = Z_SHIP_THRUST_DECK - RAPTOR_VAC_HEIGHT  # 71500.0 mm
Z_SHIP_SL_EXIT = Z_SHIP_BOT + 800.0         # 71800.0 mm (mounted via 500 mm thrust puck)
SHIP_SL_RING_R = 860.0
SHIP_VAC_RING_R = 2950.0

# TPS Ceramic Heat Shield Thickness
TPS_THICKNESS = 55.0

# Nosecone Tangent Ogive + Spherical Tip (Exact G1 Tangency)
# Outer TPS tip reaches exactly Z_SHIP_TOP = 121,300.0 mm.
# Steel hull beneath TPS terminates at Z_SHIP_TOP - TPS_THICKNESS = 121,245.0 mm.
NOSE_H_OUTER = 14000.0
Z_NOSE_BASE = Z_SHIP_TOP - NOSE_H_OUTER     # 107300.0 mm
NOSE_STEEL_H = NOSE_H_OUTER - TPS_THICKNESS  # 13945.0 mm
NOSE_CAP_R_STEEL = 550.0
NOSE_CAP_R_OUTER = NOSE_CAP_R_STEEL + TPS_THICKNESS  # 605.0 mm

# Solve exact ogive circle radius for steel hull:
# (rho - R)^2 + (H - r_cap)^2 = (rho - r_cap)^2
NOSE_OGIVE_RHO_STEEL = (
    (HULL_R**2 - NOSE_CAP_R_STEEL**2 + (NOSE_STEEL_H - NOSE_CAP_R_STEEL) ** 2)
    / (2.0 * (HULL_R - NOSE_CAP_R_STEEL))
)
NOSE_OGIVE_RHO_OUTER = NOSE_OGIVE_RHO_STEEL + TPS_THICKNESS
NOSE_OGIVE_CX = HULL_R - NOSE_OGIVE_RHO_STEEL  # Negative radial center coordinate
NOSE_CAP_CZ = Z_NOSE_BASE + NOSE_STEEL_H - NOSE_CAP_R_STEEL

# Exact tangency point (r, z) between steel ogive arc and spherical nose cap
_T_RATIO_STEEL = NOSE_OGIVE_RHO_STEEL / (NOSE_OGIVE_RHO_STEEL - NOSE_CAP_R_STEEL)
NOSE_TAN_R_STEEL = NOSE_CAP_R_STEEL * (NOSE_OGIVE_RHO_STEEL - HULL_R) / (NOSE_OGIVE_RHO_STEEL - NOSE_CAP_R_STEEL)
NOSE_TAN_Z_STEEL = Z_NOSE_BASE + _T_RATIO_STEEL * (NOSE_STEEL_H - NOSE_CAP_R_STEEL)

# Exact tangency point for outer TPS surface (same ray from ogive center!)
_T_RATIO_OUTER = NOSE_OGIVE_RHO_OUTER / (NOSE_OGIVE_RHO_STEEL - NOSE_CAP_R_STEEL)
NOSE_TAN_R_OUTER = NOSE_OGIVE_CX + _T_RATIO_OUTER * (NOSE_OGIVE_RHO_STEEL - HULL_R)
NOSE_TAN_Z_OUTER = Z_NOSE_BASE + _T_RATIO_OUTER * (NOSE_STEEL_H - NOSE_CAP_R_STEEL)

# Full 360-degree black ceramic stagnation cap starts at this Z
Z_TPS_FULL_CAP = 119500.0


def nose_radius_at_z(z: float, outer_tps: bool = False) -> float:
    """Exact hull (or TPS outer) radius at elevation z along Starship."""
    r_cyl = HULL_R + (TPS_THICKNESS if outer_tps else 0.0)
    if z <= Z_NOSE_BASE:
        return r_cyl
    rho = NOSE_OGIVE_RHO_OUTER if outer_tps else NOSE_OGIVE_RHO_STEEL
    r_cap = NOSE_CAP_R_OUTER if outer_tps else NOSE_CAP_R_STEEL
    z_tan = NOSE_TAN_Z_OUTER if outer_tps else NOSE_TAN_Z_STEEL
    if z <= z_tan:
        dz = z - Z_NOSE_BASE
        return NOSE_OGIVE_CX + math.sqrt(max(0.0, rho**2 - dz**2))
    dz = z - NOSE_CAP_CZ
    return math.sqrt(max(0.0, r_cap**2 - dz**2))


# =============================================================================
# Starship Aerodynamic Flaps (2 Aft + 2 Forward)
# =============================================================================
# Aft Flaps: mounted along vertical hinge axes at (±AFT_FLAP_HINGE_X, AFT_FLAP_HINGE_Y)
AFT_FLAP_Z_BOT = Z_SHIP_BOT + 350.0          # 71350.0 mm
AFT_FLAP_Z_TOP = Z_SHIP_BOT + 16350.0        # 87350.0 mm (16.0 m root height)
AFT_FLAP_HINGE_X = HULL_R + 180.0            # 4680.0 mm (clean clearance outside 4555 TPS)
AFT_FLAP_HINGE_Y = 580.0                     # Slightly leeward (+Y) for clean 65° folding
AFT_FLAP_SPAN = 3900.0                       # Outward from hinge -> tip at |X| = 8580 mm (17.16 m total span)
AFT_FLAP_ROOT_THICK = 640.0
AFT_FLAP_TIP_THICK = 170.0

# Forward Flaps: mounted on nosecone along inclined hinge axes matching local ogive slope
FWD_FLAP_Z_BOT = 108600.0
FWD_FLAP_Z_TOP = 117000.0
FWD_FLAP_HINGE_Y = 480.0                     # Slightly leeward (+Y) for clean leeward swing
FWD_FLAP_RADIAL_CLEARANCE = 230.0            # Clearance outside steel ogive (clears 55 mm TPS too)
FWD_FLAP_SPAN = 3250.0                       # Outward span perpendicular to hinge line
FWD_FLAP_ROOT_THICK = 440.0
FWD_FLAP_TIP_THICK = 130.0

# Compute exact forward flap hinge anchor points (starboard +X side; port mirrors X)
_R_FWD_BOT = nose_radius_at_z(FWD_FLAP_Z_BOT, outer_tps=False)
_R_FWD_TOP = nose_radius_at_z(FWD_FLAP_Z_TOP, outer_tps=False)
# Place hinge tangent line safely outside the convex ogive curve at midpoint too!
_R_FWD_MID = nose_radius_at_z(0.5 * (FWD_FLAP_Z_BOT + FWD_FLAP_Z_TOP), outer_tps=False)
_MID_CHORD_R = 0.5 * (_R_FWD_BOT + _R_FWD_TOP)
_OGIVE_BULGE = max(0.0, _R_FWD_MID - _MID_CHORD_R)
# Compute X on hull at Y = FWD_FLAP_HINGE_Y -> x_surface = sqrt(r^2 - y^2)
FWD_HINGE_P0 = (
    math.sqrt(max(0.0, _R_FWD_BOT**2 - FWD_FLAP_HINGE_Y**2)) + _OGIVE_BULGE + FWD_FLAP_RADIAL_CLEARANCE,
    FWD_FLAP_HINGE_Y,
    FWD_FLAP_Z_BOT,
)
FWD_HINGE_P1 = (
    math.sqrt(max(0.0, _R_FWD_TOP**2 - FWD_FLAP_HINGE_Y**2)) + _OGIVE_BULGE + FWD_FLAP_RADIAL_CLEARANCE,
    FWD_FLAP_HINGE_Y,
    FWD_FLAP_Z_TOP,
)
_FWD_DX = FWD_HINGE_P1[0] - FWD_HINGE_P0[0]
_FWD_DZ = FWD_HINGE_P1[2] - FWD_HINGE_P0[2]
FWD_HINGE_LEN = math.hypot(_FWD_DX, _FWD_DZ)
FWD_HINGE_DIR = (_FWD_DX / FWD_HINGE_LEN, 0.0, _FWD_DZ / FWD_HINGE_LEN)
# Inward tilt angle from +Z toward -X (degrees, positive)
FWD_HINGE_TILT_DEG = math.degrees(math.atan2(-_FWD_DX, _FWD_DZ))

# Ship forward lifting/catch pins
SHIP_CATCH_PIN_Z = 104400.0
SHIP_CATCH_PIN_R = 165.0
SHIP_CATCH_PIN_LEN = 620.0
