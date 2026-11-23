"""Single-source-of-truth architectural dimensions for the 1-story 1-person wooden shop.

Coordinate convention (millimetres, +Z up):
- X: left (-X) to right (+X), symmetric about X = 0
- Y: front storefront (-Y) to rear (+Y), so CAD Viewer `front` camera faces the shop entrance
- Z = 0: bottom of the monolithic concrete foundation footing (sits flat on ground plane)
"""

import math

# ---------------------------------------------------------------------------
# Concrete Foundation (Monolithic Thickened-Edge Slab + Entry Step)
# ---------------------------------------------------------------------------
FOOTING_H = 140.0           # Lower footing plinth height (Z: 0 -> 140)
SLAB_UPPER_H = 160.0        # Main exposed concrete slab height (Z: 140 -> 300)
SLAB_TOP_Z = FOOTING_H + SLAB_UPPER_H  # 300.0 mm finished concrete floor level

SLAB_W = 4000.0             # X: -2000 .. +2000 (200 mm drip apron each side of 3600 mm shop)
SLAB_Y_MIN = -2900.0        # Front edge of covered concrete porch
SLAB_Y_MAX = 2700.0         # Rear edge of concrete drip apron (200 mm behind rear wall)
SLAB_D = SLAB_Y_MAX - SLAB_Y_MIN  # 5600.0 mm

FOOTING_MARGIN = 80.0       # Stepped concrete footing toe all around
FOOTING_W = SLAB_W + 2 * FOOTING_MARGIN           # 4160.0 mm
FOOTING_Y_MIN = SLAB_Y_MIN - FOOTING_MARGIN       # -2980.0 mm
FOOTING_Y_MAX = SLAB_Y_MAX + FOOTING_MARGIN       # +2780.0 mm
FOOTING_D = FOOTING_Y_MAX - FOOTING_Y_MIN         # 5760.0 mm

# Front concrete entry step (aligned with left porch entrance bay)
STEP_X_MIN = -1720.0
STEP_X_MAX = -370.0         # 1350 mm wide
STEP_Y_MIN = -3320.0        # 420 mm deep tread forward of upper slab nose (-2900)
STEP_H = 150.0              # Two equal 150 mm risers: 0 -> 150 -> 300 mm

# Damp-proof course / EPDM sill gasket under perimeter wooden walls
MEMBRANE_T = 4.0            # Z: 300 -> 304

# ---------------------------------------------------------------------------
# Enclosed Shop Footprint & Wall Framing (45 x 140 mm timber studs)
# ---------------------------------------------------------------------------
SHOP_W = 3600.0             # Outer framing width: X = -1800 .. +1800
SHOP_X_MIN = -SHOP_W / 2    # -1800.0
SHOP_X_MAX = SHOP_W / 2     # +1800.0

SHOP_Y_MIN = -1700.0        # Front wall outer framing face
SHOP_Y_MAX = 2500.0         # Rear wall outer framing face
SHOP_D = SHOP_Y_MAX - SHOP_Y_MIN  # 4200.0 mm

WALL_DEPTH = 140.0          # Framing lumber depth (2x6 / 45x140)
STUD_W = 45.0               # Framing lumber width
PLATE_H = 45.0              # Bottom / top plate thickness
HEADER_H = 180.0            # Double lintel header height above openings

INNER_X_MIN = SHOP_X_MIN + WALL_DEPTH   # -1660.0
INNER_X_MAX = SHOP_X_MAX - WALL_DEPTH   # +1660.0
INNER_Y_MIN = SHOP_Y_MIN + WALL_DEPTH   # -1560.0
INNER_Y_MAX = SHOP_Y_MAX - WALL_DEPTH   # +2360.0

WALL_BASE_Z = SLAB_TOP_Z + MEMBRANE_T   # 304.0
WALL_H = 2600.0                         # Clear wall framing height (plates + studs)
WALL_TOP_Z = WALL_BASE_Z + WALL_H       # 2904.0
STUD_BASE_Z = WALL_BASE_Z + PLATE_H     # 349.0
STUD_TOP_Z = WALL_TOP_Z - 2 * PLATE_H   # 2814.0

# ---------------------------------------------------------------------------
# Covered Front Porch (Timber Posts, Beams, Knee Braces, Steel Base Shoes)
# ---------------------------------------------------------------------------
POST_SIZE = 120.0           # 120 x 120 mm heavy timber porch columns
PORCH_POST_Y = -2740.0      # Center Y of porch posts (Y: -2800 .. -2680)
PORCH_Y_MIN = PORCH_POST_Y - POST_SIZE / 2  # -2800.0
PORCH_Y_MAX = PORCH_POST_Y + POST_SIZE / 2  # -2680.0
PORCH_POST_XS = (-1740.0, -350.0, 1740.0)   # Left, middle (between door & window), right

POST_SHOE_BASE_H = 8.0      # Steel base plate thickness on concrete (Z: 300 -> 308)
POST_SHOE_STANDOFF_H = 16.0 # Moisture standoff seat height (Z: 308 -> 324)
POST_BASE_Z = SLAB_TOP_Z + POST_SHOE_BASE_H + POST_SHOE_STANDOFF_H  # 324.0
POST_SHOE_EAR_T = 6.0
POST_SHOE_EAR_H = 140.0

PORCH_BEAM_H = 180.0        # Heavy header beam height (Z: 2724 -> 2904)
PORCH_BEAM_BOT_Z = WALL_TOP_Z - PORCH_BEAM_H  # 2724.0
KNEE_BRACE_SIZE = 90.0
KNEE_BRACE_SPAN = 320.0

# ---------------------------------------------------------------------------
# Gable Roof Framing (6:12 Pitch, Slope = 0.5)
# ---------------------------------------------------------------------------
ROOF_SLOPE = 0.5            # 6:12 pitch (rise / run)
ROOF_ANGLE_RAD = math.atan(ROOF_SLOPE)
ROOF_COS = math.cos(ROOF_ANGLE_RAD)
ROOF_SIN = math.sin(ROOF_ANGLE_RAD)

RAFTER_W = 45.0             # Standard rafter thickness along Y
RAFTER_D = 140.0            # Rafter depth perpendicular to roof slope
RAFTER_VERT_H = RAFTER_D / ROOF_COS  # 156.524758 mm vertical plumb depth

RIDGE_W = 60.0              # Central ridge beam width (X: -30 .. +30)
RIDGE_HALF_W = RIDGE_W / 2  # 30.0

EAVE_X = 2150.0             # Plumb cut outer X of rafters (350 mm eave overhang past 1800)
ROOF_Y_MIN = -3020.0        # Front fly-rafter outer Y (220 mm past porch beam)
ROOF_Y_MAX = 2720.0         # Rear fly-rafter outer Y (220 mm past rear wall)

# Exact roof height lines (with birdsmouth flat seat on WALL_TOP_Z across |x| in [1660, 1800])
def rafter_bot_z(abs_x: float) -> float:
    """Bottom slope line of rafters (intersects WALL_TOP_Z at inner wall edge |x|=1660)."""
    return WALL_TOP_Z + ROOF_SLOPE * (INNER_X_MAX - abs_x)


def rafter_top_z(abs_x: float) -> float:
    """Top slope line of rafters (bearing plane for roof deck)."""
    return rafter_bot_z(abs_x) + RAFTER_VERT_H


RIDGE_BOT_Z = rafter_bot_z(RIDGE_HALF_W)   # 3719.0 mm
RIDGE_PEAK_Z = rafter_top_z(0.0)           # 3890.525 mm

# Roof envelope layer vertical thicknesses
ROOF_DECK_T = 18.0
ROOF_DECK_VERT_H = ROOF_DECK_T / ROOF_COS
ROOF_DECK_Y_MIN = ROOF_Y_MIN - 20.0        # -3040.0
ROOF_DECK_Y_MAX = ROOF_Y_MAX + 20.0        # +2740.0
FASCIA_T = 25.0
ROOF_DECK_X = EAVE_X + FASCIA_T            # 2175.0

METAL_PAN_VERT_H = 6.0
METAL_ROOF_X = ROOF_DECK_X + 30.0          # 2205.0 (drip lip into gutter)
METAL_ROOF_Y_MIN = ROOF_DECK_Y_MIN - 15.0  # -3055.0
METAL_ROOF_Y_MAX = ROOF_DECK_Y_MAX + 15.0  # +2755.0
SEAM_RIB_W = 18.0
SEAM_RIB_VERT_H = 34.0 / ROOF_COS          # 38.013 mm vertical height

# Interior collar ties
COLLAR_BOT_Z = 3260.0
COLLAR_TOP_Z = 3350.0
INTERIOR_RAFTER_YS = (-1050.0, -450.0, 150.0, 750.0, 1350.0, 1950.0)

# ---------------------------------------------------------------------------
# Wall Envelope Layers (Sheathing, Exterior Siding, Interior Wood Lining)
# ---------------------------------------------------------------------------
SHEATH_T = 15.0             # OSB/plywood sheathing outside framing
SIDING_T = 22.0             # Horizontal shiplap cedar cladding outside sheathing
LINING_T = 15.0             # Interior birch/pine wall paneling inside framing
BASEBOARD_T = 16.0          # Interior skirting board thickness
BASEBOARD_H = 85.0          # Interior skirting board height (Z: 300 -> 385)

EXT_X_MIN = SHOP_X_MIN - SHEATH_T - SIDING_T   # -1837.0
EXT_X_MAX = SHOP_X_MAX + SHEATH_T + SIDING_T   # +1837.0
EXT_Y_MIN = SHOP_Y_MIN - SHEATH_T - SIDING_T   # -1737.0
EXT_Y_MAX = SHOP_Y_MAX + SHEATH_T + SIDING_T   # +2537.0

ROOM_X_MIN = INNER_X_MIN + LINING_T            # -1645.0
ROOM_X_MAX = INNER_X_MAX - LINING_T            # +1645.0
ROOM_Y_MIN = INNER_Y_MIN + LINING_T            # -1545.0
ROOM_Y_MAX = INNER_Y_MAX - LINING_T            # +2345.0

CORNER_TRIM_W = 105.0
CORNER_TRIM_T = 22.0

# ---------------------------------------------------------------------------
# Rough Openings (Door & Windows)
# ---------------------------------------------------------------------------
# Front wall entrance door (left side)
DOOR_X_MIN = -1450.0
DOOR_X_MAX = -500.0         # 950 mm wide rough opening
DOOR_Z_MIN = SLAB_TOP_Z     # 300.0 (threshold rests on concrete slab)
DOOR_Z_MAX = 2454.0         # 2154 mm rough height

# Front wall showcase display window (right side)
FRONT_WIN_X_MIN = -200.0
FRONT_WIN_X_MAX = 1500.0    # 1700 mm wide
FRONT_WIN_Z_MIN = 1054.0    # 754 mm above concrete slab
FRONT_WIN_Z_MAX = 2454.0    # 1400 mm tall

# Right side wall window
RIGHT_WIN_Y_MIN = -800.0
RIGHT_WIN_Y_MAX = 600.0     # 1400 mm wide
RIGHT_WIN_Z_MIN = 1254.0
RIGHT_WIN_Z_MAX = 2454.0    # 1200 mm tall

# Left side wall clerestory transom window (above shelving)
LEFT_WIN_Y_MIN = 700.0
LEFT_WIN_Y_MAX = 1900.0     # 1200 mm wide
LEFT_WIN_Z_MIN = 2054.0
LEFT_WIN_Z_MAX = 2454.0     # 400 mm tall

# Rear wall clerestory transom window (above rear shelving)
REAR_WIN_X_MIN = -900.0
REAR_WIN_X_MAX = 900.0      # 1800 mm wide
REAR_WIN_Z_MIN = 2054.0
REAR_WIN_Z_MAX = 2454.0     # 400 mm tall
