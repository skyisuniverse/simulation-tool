"""Master engineering dimensions, coordinates, and material looks for Mechazilla (Starbase OLIT).

Scale: 1:100 (10.0 mm = 1.0 m, 1.0 mm = 0.1 m).
Coordinate system:
  - Origin (0, 0, 0): Center of tower footprint on the launch pad ground plane (Z = 0).
  - +X: Launch / catch direction toward Orbital Launch Mount & Starship centerline (X = +300 mm = 30 m).
  - -X: Rear / drawworks winch house & cryogenic propellant riser face.
  - +Y / -Y: Port (+Y) and Starboard (-Y) sides of the tower.
  - +Z: Vertical up.
"""

import math

SCALE_MM_PER_M = 10.0  # 1:100 scale

# ---------------------------------------------------------------------------
# Concrete Foundation & Drawworks Winch House
# ---------------------------------------------------------------------------
APRON_X_MIN = -205.0
APRON_X_MAX = 95.0
APRON_Y_HALF = 105.0
APRON_H = 10.0  # Z: 0 -> 10

PLINTH_LOW_HALF = 82.0
PLINTH_LOW_TOP_Z = 32.0  # Z: 10 -> 32

PLINTH_HIGH_HALF = 74.0
PLINTH_HIGH_TOP_Z = 47.0  # Z: 32 -> 47

BASE_PLATE_SIZE = 22.0
BASE_PLATE_H = 3.0  # Z: 47 -> 50 (steel anchor sole plates under 4 columns)

WINCH_X_MIN = -190.0
WINCH_X_MAX = -102.0
WINCH_Y_HALF = 52.0
WINCH_H = 46.0  # Z: 10 -> 56

REAR_SHEAVE_X = -88.0  # Lower deflector sheave center X (outer edge -74.8 clears plinth -74.0)
SHEAVE_PITCH_R = 12.0  # Cable pitch radius: -88 + 12 = -76.0 exact rear cable X!
SHEAVE_OUTER_R = 13.4  # Outer flange radius
REAR_SHEAVE_Z = 51.2   # Bottom rim at 37.8 clears lower plinth Z=32.0; bottom cable CL at Z=39.2
WINCH_DRUM_X = -132.0
WINCH_DRUM_Z = 28.0    # Barrel R=10.0, flange R=13.5 (bottom 14.5 > 12.5 floor); cable CL at 39.2
WINCH_DRUM_R = 10.0
CABLE_Y = 18.0         # Symmetric pair at Y = +/-18 mm
CABLE_R = 1.1          # Haul wire rope bundle radius
REAR_CABLE_X = REAR_SHEAVE_X + SHEAVE_PITCH_R  # -76.0 mm exact vertical rear haul cable X

# ---------------------------------------------------------------------------
# 9-Section Structural Steel Tower
# ---------------------------------------------------------------------------
TOWER_BASE_Z = 50.0
N_MODULES = 9
MODULE_H = 145.0  # 14.5 m per prefabricated section
TOWER_TOP_Z = TOWER_BASE_Z + N_MODULES * MODULE_H  # 1355.0 mm (135.5 m)

COL_HALF = 60.0   # 12.0 m x 12.0 m column center-to-center square
COL_R = 6.0       # 1.2 m OD steel corner columns
FLANGE_R = 8.2    # Bolted section splice flange outer radius
FLANGE_HALF_H = 1.5

BAY_H = MODULE_H / 2.0  # 2 sub-bays per module (72.5 mm each)
BEAM_SIZE = 5.6         # Horizontal perimeter box girders
BRACE_SIZE = 3.8        # Diagonal X-bracing struts
FRONT_BRACE_X = 56.0    # Recessed front K-bracing plane (clear of rails)

# Internal cladded elevator & utility core
CORE_X_CENTER = -14.0
CORE_DX = 38.0
CORE_DY = 36.0

# Front (+X) Twin Vertical Guide Rails (mounted flush on column boss at X = 68.5, proud of R=8.2 flange)
RAIL_BOSS_X = 68.5
RAIL_BACK_X = 68.5
RAIL_WEB_X0 = 71.5
RAIL_WEB_X1 = 76.5
RAIL_FRONT_X = 80.5
RAIL_FLANGE_W = 14.0  # Y_rel in [-7, +7]
RAIL_WEB_W = 6.0      # Y_rel in [-3, +3]

# Cryogenic propellant risers (running up rear-starboard side to SQD level)
CRYO_PIPES = (
    (-71.5, -34.0, 2.2),  # Main LOX insulated riser
    (-71.5, -42.5, 2.0),  # Main CH4 insulated riser
    (-71.5, -50.0, 1.3),  # High-pressure GN2 / purge line
)

# ---------------------------------------------------------------------------
# Top Crown, Pulley Sheave Headframe & Lightning Mast
# ---------------------------------------------------------------------------
CROWN_DECK_HALF = 70.0
CROWN_DECK_H = 8.0      # Z: 1355 -> 1363
CROWN_PARAPET_H = 11.0  # Z: 1363 -> 1374

CROWN_SHEAVE_Z = 1392.0
CROWN_SHEAVE_R = SHEAVE_OUTER_R
CROWN_REAR_AXLE_X = REAR_CABLE_X + SHEAVE_PITCH_R   # -64.0 (rear pitch tangent at -76.0)
CROWN_FRONT_AXLE_X = 78.0                           # front pitch tangent at +90.0
FRONT_CABLE_X = CROWN_FRONT_AXLE_X + SHEAVE_PITCH_R  # +90.0

LIGHTNING_MAST_BASE_Z = TOWER_TOP_Z + CROWN_DECK_H  # 1363.0
LIGHTNING_MAST_TOP_Z = 1500.0                       # 150.0 m total tower height

# ---------------------------------------------------------------------------
# Vertical-Travel Catch Carriage
# ---------------------------------------------------------------------------
CARRIAGE_H = 140.0       # 14.0 m tall structural gantry
CARRIAGE_Z_BUILT = 520.0 # As-built base Z (52.0 m); spans Z = 520..660
CARRIAGE_Z_MIN = 180.0   # Lower park / OLM lift height (18.0 m)
CARRIAGE_Z_MAX = 1090.0  # Upper Starship stacking height (109.0 m)
CARRIAGE_TRAVEL_MIN = CARRIAGE_Z_MIN - CARRIAGE_Z_BUILT  # -340.0 mm
CARRIAGE_TRAVEL_MAX = CARRIAGE_Z_MAX - CARRIAGE_Z_BUILT  # +570.0 mm

CARRIAGE_SPINE_X0 = 86.5
CARRIAGE_SPINE_X1 = 106.5
CARRIAGE_Y_HALF = 76.0

# Chopstick vertical hinge pins (mounted on carriage front clevises)
HINGE_X = 119.5
HINGE_Y = 74.0          # Port: +74.0, Starboard: -74.0
HINGE_PIN_R = 4.5
HINGE_BORE_R = 5.0      # 0.5 mm radial running clearance
CLEVIS_Z_LUGS = (
    (46.0, 56.0),       # Bottom clevis ear (carriage-local Z)
    (76.0, 86.0),       # Middle clevis ear
    (106.0, 116.0),     # Top clevis ear
)
KNUCKLE_CLEAR_Z = 0.8   # Axial clearance inside each clevis slot
ARM_ROOT_Z0_LOCAL = CLEVIS_Z_LUGS[0][1] + KNUCKLE_CLEAR_Z  # 56.8
ARM_ROOT_Z1_LOCAL = CLEVIS_Z_LUGS[2][0] - KNUCKLE_CLEAR_Z  # 105.2
ARM_ROOT_H = ARM_ROOT_Z1_LOCAL - ARM_ROOT_Z0_LOCAL         # 48.4 mm
ARM_TIP_H = 22.0                                           # 2.2 m at tip

# ---------------------------------------------------------------------------
# Chopsticks (Catch & Lift Arms) & Sliding Catch Trolleys
# ---------------------------------------------------------------------------
ARM_LEN = 345.0          # 34.5 m from hinge pin to tip (tips at X = 463 mm)
ARM_BOOM_W = 12.0        # Structural boom wall/chord thickness
ARM_KNUCKLE_R = 9.5      # Clears carriage spine (118 - 9.5 = 108.5 > 105.0)

# Inward gooseneck offset: positions sliding catch trolleys at Y_inner = +/-46.1 mm
# (exact 92.2 mm = 9.22 m clear inner span so a 9.0 m Starship / Super Heavy fuselage fits cleanly
# between the trolleys while its protruding catch pins land squarely on the orange shock pads!)
CATCH_RAIL_INNER_Y = 49.5
CATCH_RAIL_W = 3.5       # Rail bar width (Y: 49.5 -> 53.0)
ARM_BOOM_INNER_Y = CATCH_RAIL_INNER_Y + CATCH_RAIL_W + 1.5  # 54.5 (1.5 mm damper stanchion gap)
ARM_BOOM_CENTER_Y = ARM_BOOM_INNER_Y + ARM_BOOM_W / 2.0     # 60.5
ARM_GOOSENECK_X = 82.0   # Length of inward root transition from hinge

CATCH_RAIL_X0 = 86.0     # Arm-local X start of catch rail (world X = 205.5)
CATCH_RAIL_X1 = 326.0    # Arm-local X end of catch rail (world X = 445.5)

TROLLEY_LEN = 36.0
TROLLEY_X_BUILT = 180.5  # Arm-local X center as built (world X = 119.5 + 180.5 = 300.0 = Rocket CL!)
TROLLEY_MIN_X = 110.5    # Arm-local X center min
TROLLEY_MAX_X = 280.5    # Arm-local X center max
TROLLEY_TRAVEL_MIN = TROLLEY_MIN_X - TROLLEY_X_BUILT  # -70.0 mm
TROLLEY_TRAVEL_MAX = TROLLEY_MAX_X - TROLLEY_X_BUILT  # +100.0 mm

# Arm opening angles (degrees; positive opens outward for Port via coupling)
ARM_ANGLE_MIN = -4.0
ARM_ANGLE_MAX = 36.0

# ---------------------------------------------------------------------------
# Ship Quick Disconnect (SQD) Arm
# ---------------------------------------------------------------------------
SQD_Z = 825.0            # 82.5 m elevation (Starship 2nd stage aft cryo QD port)
SQD_HINGE_X = 46.0       # On cantilevered outrigger behind front rail (X=67)
SQD_HINGE_Y = -98.0      # Starboard (-Y) outrigger, clearing tower & carriage
SQD_PIN_R = 3.5

ROCKET_CENTER_X = 300.0  # 30.0 m from tower center to OLM / Starship centerline
ROCKET_RADIUS = 45.0     # 9.0 m diameter Starship / Super Heavy
SQD_TARGET_X = ROCKET_CENTER_X - ROCKET_RADIUS  # 255.0 (-X fuselage skin)
SQD_TARGET_Y = 0.0

_sqd_dx = SQD_TARGET_X - SQD_HINGE_X  # 209.0
_sqd_dy = SQD_TARGET_Y - SQD_HINGE_Y  # +98.0
SQD_DEPLOY_LEN = math.hypot(_sqd_dx, _sqd_dy)                 # ~230.83 mm
SQD_DEPLOY_ANGLE_DEG = math.degrees(math.atan2(_sqd_dy, _sqd_dx))  # +25.12 deg
SQD_STOWED_ANGLE_DELTA = -(180.0 + SQD_DEPLOY_ANGLE_DEG)      # -205.12 deg (points straight -X)
SQD_SWING_MIN = -208.0
SQD_SWING_MAX = 10.0


# ---------------------------------------------------------------------------
# Material Factories (called inside model bodies so kernel/material loads stay lazy)
# ---------------------------------------------------------------------------
def mat_concrete(color="#9A9892"):
    from bd_materials import resins
    m = resins.ceramic()
    m.pbr = m.pbr.override(roughness=0.92, metalness=0.0)
    return m, color


def mat_concrete_dark():
    return mat_concrete("#807E79")


def mat_tower_steel():
    from bd_materials import metals
    from cad.build123d import materials
    return materials.powder_coat("#3A4048", finish="satin", substrate=metals.mild_steel())


def mat_carriage_steel():
    from bd_materials import metals
    from cad.build123d import materials
    return materials.powder_coat("#2E343C", finish="satin", substrate=metals.alloy_steel())


def mat_cladding():
    from bd_materials import metals
    from cad.build123d import materials
    return materials.powder_coat("#B4BCC4", finish="satin", substrate=metals.mild_steel())


def mat_deck_grating():
    from bd_materials import metals
    from cad.build123d import materials
    return materials.powder_coat("#525962", finish="matte", substrate=metals.mild_steel())


def mat_guide_rail():
    from bd_materials import metals
    from cad.build123d import materials
    return materials.brushed(substrate=metals.alloy_steel())


def mat_stainless():
    from bd_materials import metals
    m = metals.stainless()
    m.pbr = m.pbr.override(roughness=0.28)
    return m


def mat_catch_rail():
    from bd_materials import metals
    from cad.build123d import materials
    return materials.powder_coat("#E2E6EA", finish="satin", substrate=metals.alloy_steel())


def mat_trolley_body():
    from bd_materials import metals
    from cad.build123d import materials
    return materials.powder_coat("#BCC4CC", finish="satin", substrate=metals.alloy_steel())


def mat_bumper_pad():
    from bd_materials import plastics
    m = plastics.tpu()
    m.pbr = m.pbr.override(roughness=0.65, metalness=0.0)
    return m, "#D96B27"


def mat_sqd_steel():
    from bd_materials import metals
    from cad.build123d import materials
    return materials.powder_coat("#9AA3AC", finish="satin", substrate=metals.mild_steel())


def mat_cable():
    from bd_materials import metals
    from cad.build123d import materials
    return materials.powder_coat("#646B73", finish="matte", substrate=metals.alloy_steel())


def mat_sheave():
    from bd_materials import metals
    from cad.build123d import materials
    return materials.powder_coat("#76808B", finish="satin", substrate=metals.alloy_steel())


def mat_beacon_red():
    from bd_materials import plastics
    m = plastics.pc()
    m.pbr = m.pbr.override(
        roughness=0.18,
        metalness=0.0,
        emissive=(0.95, 0.08, 0.05),
        emissive_intensity=1.6,
    )
    return m, "#E02424"


def apply_material(part, mat_spec):
    """Apply either a FinishedMaterial or a (FinishedMaterial, hex_color) pair."""
    if isinstance(mat_spec, tuple):
        mat, col = mat_spec
        part.material = mat
        part.color = col
    else:
        part.material = mat_spec
    return part
