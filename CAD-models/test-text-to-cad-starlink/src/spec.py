"""Shared dimensional specifications and datums for the SpaceX Starlink V2 Mini satellite.

Coordinate system (1:1 full scale, millimetres, +Z up):
  X: solar wing span axis (+X starboard, -X port)
  Y: spacecraft body axis (+Y forward/velocity vector, -Y aft/Hall thrusters)
  Z: orbital vertical (+Z zenith/space-facing deck, -Z nadir/Earth-facing antenna deck)

All solar wing accordion fold geometry is derived parametrically from these constants
so that stowed, unlatched, mid-accordion, deployed, and sun-tracking poses remain
free of solid interference.
"""

# ---------------------------------------------------------------------------
# Main flat-panel bus envelope (SpaceX Starlink V2 Mini: ~4.1 m x 2.7 m)
# ---------------------------------------------------------------------------
BUS_X = 2700.0          # Width along wing span axis (X in [-1350, +1350])
BUS_Y = 4100.0          # Length along chord / flight axis (Y in [-2050, +2050])
BUS_Z = 240.0           # Nominal structural chassis height (Z in [0, 240])
BUS_CORNER_CHAMFER = 180.0  # Corner bevels to nest inside Falcon 9 4.6 m fairing

# Zenith (+Z) deck zones
SPINE_HALF_X = 136.0    # Central dorsal avionics/propulsion spine X in [-136, +136]
STOW_FLOOR_Z = 196.0    # Recessed floor of Port/Starboard solar stowage trays
RIM_HALF_Y = 1865.0     # Fore/aft raised perimeter decks live beyond |Y| >= 1865 mm

# Nadir (-Z) Earth-facing payload recess
NADIR_DECK_Z = 0.0      # Reference nadir mounting plane
NADIR_RECESS_DEPTH = 14.0

# ---------------------------------------------------------------------------
# Dual accordion-folded solar array wings (10 panels per wing, ~26.8 m span)
# ---------------------------------------------------------------------------
WING_PANEL_COUNT = 10   # 10 panels per wing -> ~12.0 m per wing, ~26.8 m wingspan
PANEL_LEN = 1176.0      # Panel spanwise length along X (fits inside [168, 1344] stowed)
PANEL_CHORD = 3680.0    # Panel chordwise width along Y (fits inside |Y| <= 1840)
PANEL_THICK = 14.0      # Structural panel frame thickness along Z
PANEL_FOLD_GAP = 4.0    # Z air gap between adjacent folded panels when stowed
HINGE_GAP_X = 10.0      # Half-gap from panel end face to hinge pin axis along X
PANEL_PITCH_X = PANEL_LEN + 2.0 * HINGE_GAP_X  # Center-to-center hinge pitch (1196 mm)

# Vertical datums for exact Z-fold geometry:
#   Deployed panel occupies Z in [PANEL_DEPLOY_Z - T/2, PANEL_DEPLOY_Z + T/2] = [207, 221]
#   Top hinge pin axis (H0, H2, H4, ...) at Z_HINGE_TOP = 223.0
#   Bottom hinge pin axis (H1, H3, H5, ...) at Z_HINGE_BOT = 205.0
#   Stowed panel P1 occupies Z in [225, 239] -> 29 mm above STOW_FLOOR_Z (196 mm)
#   Stowed 10-panel stack top = 225 + 9 * 18 + 14 = 401 mm (matches Falcon 9 stack pitch!)
PANEL_DEPLOY_Z = 214.0
HINGE_Z_OFFSET = (PANEL_THICK + PANEL_FOLD_GAP) / 2.0  # 9.0 mm from panel midplane
Z_HINGE_TOP = PANEL_DEPLOY_Z + HINGE_Z_OFFSET          # 223.0 mm
Z_HINGE_BOT = PANEL_DEPLOY_Z - HINGE_Z_OFFSET          # 205.0 mm

# SADA (Solar Array Drive Assembly) & Root Hinge Datums
SADA_Z = 136.0          # SADA rotary shaft axis Z (fully enclosed inside bus side rail below STOW_FLOOR_Z)
ROOT_HINGE_X = 1356.0   # Starboard root hinge X0 (Port is -1356.0)
# Check stowed X span of all panels:
#   [ROOT_HINGE_X - HINGE_GAP_X - PANEL_LEN, ROOT_HINGE_X - HINGE_GAP_X]
#   = [1356 - 10 - 1176, 1356 - 10] = [170.0, 1346.0] mm
#   Clear of central spine (|X| <= 152) by 18 mm, and inside bus edge (1350) by 4 mm!

# 4 hinge stations symmetrically spaced along the 3680 mm panel chord
HINGE_Y_POSITIONS = (-1460.0, -490.0, 490.0, 1460.0)
HINGE_PIN_R = 4.5
HINGE_BOSS_R = 8.0
HINGE_TANG_W = 22.0     # Center tang width along Y
HINGE_FORK_GAP = 25.0   # Clear inner width of fork clevis along Y (1.5 mm clearance/side)
HINGE_EAR_W = 12.0      # Each outer fork ear thickness along Y

# ---------------------------------------------------------------------------
# Propulsion (Aft -Y Argon Hall-effect thrusters & COPV Argon tanks)
# ---------------------------------------------------------------------------
THRUSTER_X_OFFSET = 270.0    # Dual Hall thrusters at X = +-270 mm on aft bulkhead
THRUSTER_Y_MOUNT = -BUS_Y / 2.0  # -2050.0 mm
THRUSTER_Z_CENTER = 120.0

# ---------------------------------------------------------------------------
# Optical ISL ("Space Lasers") & Attitude Sensors
# ---------------------------------------------------------------------------
# 3 Optical ISL terminals positioned outside |Y| <= 1865 so stowed arrays never clash
ISL_FWD_POS = (0.0, 1955.0, BUS_Z)
ISL_AFT_PORT_POS = (-640.0, -1955.0, BUS_Z)
ISL_AFT_STBD_POS = (640.0, -1955.0, BUS_Z)

# Falcon 9 stack retention corner hardpoints (outside stowed array footprint)
STACK_LUG_POSITIONS = (
    (-1120.0, -1955.0),
    (1120.0, -1955.0),
    (-1120.0, 1955.0),
    (1120.0, 1955.0),
)
