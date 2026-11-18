"""Constants and design parameters for the Tesla Semi-style truck."""

# Dimensions (in mm)
# Overall vehicle envelope
TRUCK_TOTAL_LENGTH = 7300.0
TRUCK_TOTAL_WIDTH = 2500.0
TRUCK_TOTAL_HEIGHT = 3950.0

# Ground clearance & Wheels
TIRE_RADIUS = 520.0  # 1040 mm diameter commercial truck tire
TIRE_WIDTH = 295.0
RIM_RADIUS = 285.0  # 22.5 inch rim (~570 mm)
GROUND_CLEARANCE = 260.0

# Longitudinal positions (X-axis, 0 at front bumper, +X rearward)
X_FRONT_BUMPER = 0.0
X_FRONT_AXLE = 1450.0
X_CAB_NOSE = 100.0
X_WINDSHIELD_BASE = 520.0
X_CAB_PILLAR_B = 2100.0
X_CAB_BACK = 3450.0

X_BATTERY_FRONT = 1750.0
X_BATTERY_REAR = 4800.0

X_DRIVE_AXLE_1 = 5350.0
X_DRIVE_AXLE_2 = 6700.0
X_FIFTH_WHEEL = 6025.0
X_REAR_BUMPER = 7280.0

# Vertical positions (Z-axis, 0 at ground plane, +Z upward)
Z_GROUND = 0.0
Z_AXLE = TIRE_RADIUS  # 520 mm
Z_CHASSIS_BOTTOM = 400.0
Z_CHASSIS_TOP = 950.0
Z_DECK_TOP = 1020.0
Z_FIFTH_WHEEL = 1180.0

Z_BUMPER_BOTTOM = 220.0
Z_CAB_FLOOR = 900.0
Z_HOOD_LINE = 1450.0
Z_ROOF_LOWER = 2750.0
Z_ROOF_TOP = 3920.0

# Lateral positions (Y-axis, 0 is truck centerline, +Y left, -Y right)
Y_CHASSIS_RAIL_HALF = 480.0  # standard 960 mm wide chassis frame
Y_FRONT_TRACK_HALF = 1020.0
Y_REAR_INNER_HALF = 820.0
Y_REAR_OUTER_HALF = 1130.0
Y_CAB_BASE_HALF = 1160.0
Y_AERO_SKIRT_HALF = 1240.0
Y_ROOF_HALF = 1050.0

# Colors (Hex codes for styling)
COLOR_CAB_BODY = "#E5E7EB"        # Sleek Tesla pearl silver / white
COLOR_CAB_ACCENT = "#1F2937"      # Dark carbon / satin black lower trim
COLOR_AERO_SKIRTS = "#E5E7EB"     # Matching body skirts
COLOR_SKIRT_TRIM = "#111827"      # Dark bottom lip / step trim
COLOR_GLASS = "#1E293B"           # Deep dark tinted panoramic glass
COLOR_CHASSIS = "#262626"         # Heavy duty chassis dark graphite
COLOR_FIFTH_WHEEL = "#374151"     # Cast steel fifth wheel
COLOR_TIRE_RUBBER = "#171717"     # Dark rubber
COLOR_WHEEL_AERO = "#1F2937"      # Satin dark aero wheel covers
COLOR_WHEEL_RIM = "#4B5563"       # Alloy wheel rim
COLOR_HEADLIGHT = "#F8FAFC"       # Cool crisp LED white
COLOR_HEADLIGHT_ACCENT = "#38BDF8"# Subtle electric cyan DRL accent
COLOR_TAILLIGHT = "#EF4444"       # Vibrant LED red
COLOR_CATWALK = "#64748B"         # Aluminum checker plate deck
COLOR_INTERIOR = "#0F172A"        # Interior cockpit silhouette
