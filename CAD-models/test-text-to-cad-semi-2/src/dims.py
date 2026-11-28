"""Shared dimensions, coordinates, and visual styling constants for the original Tesla Semi.

Coordinate system (1:1 real-world scale in millimetres, +Z up):
  X = 0      : Vehicle longitudinal centerline (+X = driver's left / port, -X = right / starboard)
  Y = 0      : Front bumper leading tip (+Y runs rearward toward the fifth wheel and tail)
  Z = 0      : Ground contact plane (bottom of tires)

With this convention, standard CAD viewer cameras align naturally:
  front -> front face of the truck (looking from -Y toward +Y)
  back  -> rear face (fifth wheel, cab extenders, tail lights)
  right -> left-side profile (front pointing left)
  left  -> right-side profile (front pointing right)
  iso   -> classic front-left 3/4 hero angle
"""

# ---------------------------------------------------------------------------
# Master exterior envelope (Class 8 original Tesla Semi 6x4 Long Range Day Cab)
# ---------------------------------------------------------------------------
TOTAL_LENGTH = 6560.0       # Y = 0 (nose tip) .. 6560 (rear crossmember)
BODY_WIDTH = 2540.0         # Full aero width across rear skirts & extenders (100 in)
BODY_HALF_W = BODY_WIDTH / 2.0  # 1270.0 mm
TOTAL_HEIGHT = 3960.0       # Full aero roof fairing peak (~13 ft)

# ---------------------------------------------------------------------------
# Tires & wheels (standard 295/75R22.5 commercial Class 8)
# ---------------------------------------------------------------------------
TIRE_OD = 1032.0            # Outer diameter (~40.6 in)
TIRE_R = TIRE_OD / 2.0      # 516.0 mm (axle centerline Z height)
TIRE_W = 295.0              # Section width (295 mm)
RIM_OD = 572.0              # 22.5 inch wheel rim diameter
RIM_R = RIM_OD / 2.0        # 286.0 mm

# Axle Y coordinates (from nose tip Y = 0)
Y_FRONT_AXLE = 1200.0
Y_REAR_AXLE_1 = 4560.0
Y_REAR_AXLE_2 = 5880.0
TANDEM_SPREAD = Y_REAR_AXLE_2 - Y_REAR_AXLE_1  # 1320.0 mm (52 in)
WHEELBASE_MID = (Y_REAR_AXLE_1 + Y_REAR_AXLE_2) / 2.0 - Y_FRONT_AXLE  # 4020.0 mm (158.3 in)

# Wheel lateral track coordinates (X from centerline)
# Front steer tires (single): outer face at +/-1227.5 mm (tucked cleanly inside +/-1255 fender)
X_STEER_CENTER = 1080.0
# Rear dual drive tires (two per side):
# Inner tire: 745 +/- 147.5 => 597.5 .. 892.5 mm
# Outer tire: 1095 +/- 147.5 => 947.5 .. 1242.5 mm (55 mm dual tire air gap)
X_DRIVE_INNER = 745.0
X_DRIVE_OUTER = 1095.0
DRIVE_DUAL_GAP = (X_DRIVE_OUTER - X_DRIVE_INNER) - TIRE_W  # 55.0 mm

# ---------------------------------------------------------------------------
# Ladder frame & powertrain layout
# ---------------------------------------------------------------------------
FRAME_OUTER_HALF_W = 435.0  # 870 mm outer frame rail width (standard 34 in Class 8)
FRAME_RAIL_W = 86.0         # C-channel flange width
FRAME_RAIL_H = 260.0        # C-channel web height
FRAME_WEB_T = 12.0          # Rail wall thickness
FRAME_Z_BOT = 760.0         # Bottom of main frame rails
FRAME_Z_TOP = FRAME_Z_BOT + FRAME_RAIL_H  # 1020.0 mm (top of frame rails)
FRAME_Y_START = 485.0       # Forward bumper-mount end of rails (cleanly behind front bulkhead)
FRAME_Y_END = 6510.0        # Rear end of rails (rear crossmember sits 6510..6560)

# Under-floor structural battery pack (between steer axle and forward drive axle)
BATT_Y_START = 1860.0
BATT_Y_END = 3920.0
BATT_HALF_W = 920.0         # Wide structural pack sitting inside lower side skirts
BATT_Z_BOT = 360.0          # Ground clearance above road
BATT_Z_TOP = 748.0          # 12 mm clean clearance below frame rail bottom (760)

# Fifth wheel coupling (standard 48 in / 1220 mm top height)
FIFTH_WHEEL_Y = 5180.0      # Slightly forward of tandem midpoint (5220) for optimal load transfer
FIFTH_WHEEL_Z_TOP = 1220.0  # Standard North American kingpin plate height
FIFTH_WHEEL_DIA = 920.0     # 36 inch cast-steel plate

# ---------------------------------------------------------------------------
# Cab & aero body layout
# ---------------------------------------------------------------------------
GROUND_CLEARANCE_NOSE = 270.0   # Front chin air-dam bottom
GROUND_CLEARANCE_SKIRT = 300.0  # Side aero skirt bottom edge

CAB_BULKHEAD_Y = 3560.0     # Rear structural cab wall
CAB_EXTENDER_Y = 3960.0     # Trailing edge of tall curved side aero collars & roof fairing
CAB_FLOOR_Z = 1140.0        # Standing interior cabin floor (above frame top 1020 + subfloor)

# Front wheel arch cutout (centered at Y_FRONT_AXLE, Z = TIRE_R)
FRONT_ARCH_R = 615.0        # ~99 mm radial clearance around 516 mm steer tire

# Door & entry step recess (behind front wheel arch)
DOOR_Y_FRONT = 2020.0
DOOR_Y_REAR = 2960.0
DOOR_Z_BOT = 1090.0
STEP_Y_FRONT = 2120.0
STEP_Y_REAR = 2860.0

# ---------------------------------------------------------------------------
# Color & material palette (Original 2017/2022 Tesla Semi Metallic Silver)
# ---------------------------------------------------------------------------
COLOR_BODY_SILVER = "#B8C1CC"      # Iconic original unveil Metallic Silver
COLOR_BUMPER_DARK = "#24282E"      # Satin obsidian composite bumper & lower trim
COLOR_SKIRT_DARK = "#2B3038"       # Satin charcoal aerodynamic skirts / mudflaps
COLOR_TRIM_BLACK = "#1A1D21"       # Gloss/satin black moldings, window frit, wiper arms
COLOR_GLASS_TINT = "#4E5966"       # Smoked automotive glass (used with transmission)
COLOR_GLASS_MIRROR = "#C6D2DE"     # Reflective mirror glass
COLOR_FRAME_STEEL = "#343942"      # Industrial powder-coated dark grey chassis steel
COLOR_ALUMINUM = "#B8BFC7"         # Brushed aluminum catwalk, e-axles, battery skid
COLOR_CAST_STEEL = "#2B2F36"       # Cast fifth wheel & axle housings
COLOR_TIRE_RUBBER = "#232529"      # Matte vulcanized rubber
COLOR_RIM_DARK = "#3A4048"         # Dark metallic forged 22.5" rim
COLOR_WHEEL_COVER = "#262A30"      # Signature satin-black Tesla aero wheel cover
COLOR_CHROME = "#E4E8EE"           # Polished chrome Tesla T badge, lug nuts, handles
COLOR_HV_ORANGE = "#E8611A"        # High-voltage orange battery cable accents
COLOR_LED_WHITE = "#F5FAFF"        # Glowing white DRL / projector LEDs
COLOR_LED_AMBER = "#FF9900"        # DOT amber clearance & side marker lights
COLOR_LED_RED = "#E01B1B"          # Rear LED tail / brake light bars
COLOR_INTERIOR_DARK = "#282C33"    # Charcoal cabin upholstery / dash
COLOR_SEAT_LEATHER = "#1F2227"     # Matte black vegan leather driver seat
COLOR_SCREEN_UI = "#1B2A3D"        # Dark-mode Tesla UI display glass
COLOR_SCREEN_BEZEL = "#14161A"     # Display bezel
COLOR_AIR_RED = "#C92A2A"          # Emergency air brake coil hose
COLOR_AIR_BLUE = "#1E6FD9"         # Service air brake coil hose
