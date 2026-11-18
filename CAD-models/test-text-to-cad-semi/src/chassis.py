"""Chassis, battery pack, fifth wheel, and rear gear for the Tesla Semi-style truck."""

import build123d as bd
from cad import model

from constants import (
    COLOR_CATWALK,
    COLOR_CHASSIS,
    COLOR_FIFTH_WHEEL,
    COLOR_TAILLIGHT,
    COLOR_TIRE_RUBBER,
    X_BATTERY_FRONT,
    X_BATTERY_REAR,
    X_DRIVE_AXLE_1,
    X_DRIVE_AXLE_2,
    X_FIFTH_WHEEL,
    X_FRONT_AXLE,
    X_REAR_BUMPER,
    Y_CHASSIS_RAIL_HALF,
    Z_CHASSIS_BOTTOM,
    Z_CHASSIS_TOP,
    Z_DECK_TOP,
    Z_FIFTH_WHEEL,
    Z_GROUND,
)


def make_c_channel(length, height=280.0, flange=90.0, web_t=14.0, flange_t=16.0):
    """Creates a structural C-channel frame rail along X axis."""
    outer = bd.Box(length, flange, height)
    inner = bd.Box(length + 2.0, flange - web_t, height - 2.0 * flange_t)
    # Cut out one side to make a C-channel
    inner = bd.Pos(0, -web_t / 2.0 - 1.0, 0) * inner
    channel = outer - inner
    return channel


def make_chassis_frame():
    """Heavy-duty ladder frame rails and structural crossmembers."""
    rail_len = X_REAR_BUMPER - 700.0  # from X=700 to 7280
    rail_center_x = 700.0 + rail_len / 2.0
    rail_center_z = (Z_CHASSIS_BOTTOM + 250.0 + Z_CHASSIS_TOP) / 2.0  # ~825 mm

    # Left rail (+Y)
    left_c = make_c_channel(rail_len)
    left_rail = bd.Pos(rail_center_x, Y_CHASSIS_RAIL_HALF, rail_center_z) * left_c
    left_rail.color = COLOR_CHASSIS
    left_rail.label = "chassis_rail_left"

    # Right rail (-Y)
    right_c = make_c_channel(rail_len)
    # Mirror along Y
    right_c = bd.Rot(0, 0, 180) * right_c
    right_rail = bd.Pos(rail_center_x, -Y_CHASSIS_RAIL_HALF, rail_center_z) * right_c
    right_rail.color = COLOR_CHASSIS
    right_rail.label = "chassis_rail_right"

    # Crossmembers at key structural locations
    cross_xs = [
        X_FRONT_AXLE,
        2800.0,
        4200.0,
        X_DRIVE_AXLE_1,
        X_FIFTH_WHEEL,
        X_DRIVE_AXLE_2,
        X_REAR_BUMPER - 40.0,
    ]
    crossmembers = []
    span = 2.0 * Y_CHASSIS_RAIL_HALF - 40.0
    for i, cx in enumerate(cross_xs):
        cross = bd.Box(140.0, span, 180.0)
        # Bore lightening hole in the middle
        bore = bd.Rot(0, 90, 0) * bd.Cylinder(45.0, 150.0)
        cross = cross - bore
        cross = bd.Pos(cx, 0, rail_center_z) * cross
        cross.color = COLOR_CHASSIS
        cross.label = f"crossmember_{i+1}"
        crossmembers.append(cross)

    frame = bd.Compound(children=[left_rail, right_rail] + crossmembers, label="ladder_frame")
    return frame


def make_battery_pack():
    """Tesla Semi low-slung high-voltage traction battery pack."""
    bat_len = X_BATTERY_REAR - X_BATTERY_FRONT  # 3050 mm
    bat_center_x = (X_BATTERY_FRONT + X_BATTERY_REAR) / 2.0
    bat_width = 2200.0  # spans under chassis between outer aero skirts
    bat_h = 360.0
    bat_center_z = 280.0 + bat_h / 2.0  # 460 mm

    main_casing = bd.Box(bat_len, bat_width, bat_h)
    # Chamfer lower perimeter edges for ground clearance & skid deflection
    lower_edges = main_casing.edges().filter_by(bd.Axis.Z).sort_by(bd.Axis.Z)
    bot_edges = main_casing.faces().sort_by(bd.Axis.Z)[0].edges()
    if bot_edges:
        main_casing = bd.chamfer(bot_edges, 35.0)

    # Skid protective ribs along the bottom
    ribs = []
    for y_offset in [-800.0, -400.0, 0.0, 400.0, 800.0]:
        rib = bd.Box(bat_len - 100.0, 30.0, 20.0)
        rib = bd.Pos(0, y_offset, -bat_h / 2.0 - 10.0) * rib
        ribs.append(rib)

    # Top high-voltage junction box
    junction = bd.Box(500.0, 600.0, 90.0)
    junction = bd.Pos(bat_len / 2.0 - 400.0, 0, bat_h / 2.0 + 45.0) * junction

    battery = main_casing
    for r in ribs:
        battery = battery + r
    battery = battery + junction

    battery = bd.Pos(bat_center_x, 0, bat_center_z) * battery
    battery.color = "#1E293B"  # Dark ballistic armor finish
    battery.label = "traction_battery_pack"
    return battery


def make_fifth_wheel():
    """Heavy-duty semi trailer fifth wheel hitch coupling."""
    # Base pedestal plates mounting to chassis rails
    pedestal_left = bd.Pos(X_FIFTH_WHEEL, Y_CHASSIS_RAIL_HALF, Z_CHASSIS_TOP + 40.0) * bd.Box(550.0, 160.0, 80.0)
    pedestal_right = bd.Pos(X_FIFTH_WHEEL, -Y_CHASSIS_RAIL_HALF, Z_CHASSIS_TOP + 40.0) * bd.Box(550.0, 160.0, 80.0)

    # Top hitch plate (horseshoe shape with kingpin entry throat)
    plate_len = 780.0
    plate_w = 860.0
    plate_t = 55.0

    plate = bd.Box(plate_len, plate_w, plate_t)
    # Fillet front outer corners
    front_edges = plate.edges().filter_by(bd.Axis.Z).sort_by(bd.Axis.X)[:2]
    if front_edges:
        plate = bd.fillet(front_edges, 120.0)

    # Kingpin center throat and rear V-shaped entry ramps
    # V-notch from rear (positive X in truck frame)
    v_cutter = bd.Pos(plate_len / 2.0, 0, 0) * bd.Rot(0, 0, 45) * bd.Box(360.0, 360.0, plate_t + 10.0)
    center_hole = bd.Pos(20.0, 0, 0) * bd.Cylinder(55.0, plate_t + 10.0)
    throat_slot = bd.Pos(plate_len / 4.0, 0, 0) * bd.Box(plate_len / 2.0, 80.0, plate_t + 10.0)

    plate = plate - v_cutter - center_hole - throat_slot

    # Bevel / ramp down rear edges
    rear_faces = plate.faces().sort_by(bd.Axis.X)[-1:]

    # Tilt fifth wheel plate slightly rearward (~4 degrees) like real highway tractors
    plate = bd.Rot(0, 4.0, 0) * plate
    plate = bd.Pos(X_FIFTH_WHEEL, 0, Z_FIFTH_WHEEL) * plate

    # Release handle extending out to left side (+Y)
    handle_rod = bd.Pos(X_FIFTH_WHEEL, Y_CHASSIS_RAIL_HALF + 200.0, Z_FIFTH_WHEEL - 10.0) * bd.Box(25.0, 320.0, 25.0)
    handle_grip = bd.Pos(X_FIFTH_WHEEL - 40.0, Y_CHASSIS_RAIL_HALF + 360.0, Z_FIFTH_WHEEL - 10.0) * bd.Box(100.0, 25.0, 35.0)

    fifth_wheel_unit = bd.Compound(
        children=[pedestal_left, pedestal_right, plate, handle_rod, handle_grip],
        label="fifth_wheel_assembly",
    )
    fifth_wheel_unit.color = COLOR_FIFTH_WHEEL
    return fifth_wheel_unit


def make_catwalk_deck():
    """Aluminum catwalk behind cab with trailer hookup umbilical connections."""
    deck_len = 1500.0
    deck_w = 920.0
    deck_t = 18.0
    deck_x = 3500.0 + deck_len / 2.0
    deck_z = Z_CHASSIS_TOP + deck_t / 2.0 + 8.0

    deck = bd.Box(deck_len, deck_w, deck_t)
    # Perforations / textured grid pattern
    for ix in range(-5, 6):
        for iy in range(-3, 4):
            hole = bd.Pos(ix * 120.0, iy * 120.0, 0) * bd.Box(60.0, 50.0, deck_t + 2.0)
            deck = deck - hole

    deck = bd.Pos(deck_x, 0, deck_z) * deck
    deck.color = COLOR_CATWALK
    deck.label = "catwalk_plate"

    # Cab back trailer connection pogo stick / umbilical hoses stand
    pogo_base = bd.Pos(3600.0, 0, deck_z + 300.0) * bd.Cylinder(22.0, 600.0)
    pogo_base.color = "#475569"
    pogo_base.label = "umbilical_post"

    # Air lines (Red = Emergency, Blue = Service) & Green electrical cable
    air_red = bd.Pos(3600.0, 45.0, deck_z + 450.0) * bd.Cylinder(16.0, 300.0)
    air_red.color = "#DC2626"
    air_red.label = "air_hose_red"

    air_blue = bd.Pos(3600.0, -45.0, deck_z + 450.0) * bd.Cylinder(16.0, 300.0)
    air_blue.color = "#2563EB"
    air_blue.label = "air_hose_blue"

    catwalk = bd.Compound(children=[deck, pogo_base, air_red, air_blue], label="catwalk_assembly")
    return catwalk


def make_rear_bumper_and_mudflaps():
    """Rear bumper bar, LED tail lights, license plate, and heavy mudflaps."""
    bumper_len = 120.0
    bumper_w = 2440.0
    bumper_h = 160.0
    bumper_z = 520.0

    # Transverse bumper beam
    beam = bd.Pos(X_REAR_BUMPER, 0, bumper_z) * bd.Box(bumper_len, bumper_w, bumper_h)
    beam.color = COLOR_CHASSIS
    beam.label = "rear_bumper_beam"

    # Recessed horizontal LED taillight bars on left and right
    taillight_l = bd.Pos(X_REAR_BUMPER + 45.0, 850.0, bumper_z) * bd.Box(35.0, 380.0, 65.0)
    taillight_l.color = COLOR_TAILLIGHT
    taillight_l.label = "taillight_left"

    taillight_r = bd.Pos(X_REAR_BUMPER + 45.0, -850.0, bumper_z) * bd.Box(35.0, 380.0, 65.0)
    taillight_r.color = COLOR_TAILLIGHT
    taillight_r.label = "taillight_right"

    # License plate holder in center
    plate_frame = bd.Pos(X_REAR_BUMPER + 42.0, 0, bumper_z) * bd.Box(25.0, 320.0, 150.0)
    plate_frame.color = "#FFFFFF"
    plate_frame.label = "license_plate"

    # Heavy-duty mudflaps behind the rear tandem wheels
    flap_w = 600.0
    flap_h = 680.0
    flap_t = 24.0
    flap_z = 180.0 + flap_h / 2.0  # 520 mm
    flap_x = X_REAR_BUMPER - 30.0

    flap_left = bd.Pos(flap_x, 950.0, flap_z) * bd.Box(flap_t, flap_w, flap_h)
    flap_left.color = COLOR_TIRE_RUBBER
    flap_left.label = "mudflap_left"

    flap_right = bd.Pos(flap_x, -950.0, flap_z) * bd.Box(flap_t, flap_w, flap_h)
    flap_right.color = COLOR_TIRE_RUBBER
    flap_right.label = "mudflap_right"

    rear_gear = bd.Compound(
        children=[beam, taillight_l, taillight_r, plate_frame, flap_left, flap_right],
        label="rear_bumper_mudflaps",
    )
    return rear_gear


@model
def chassis():
    frame = make_chassis_frame()
    battery = make_battery_pack()
    fifth_wheel = make_fifth_wheel()
    catwalk = make_catwalk_deck()
    rear_gear = make_rear_bumper_and_mudflaps()

    chassis_assembly = bd.Compound(
        children=[frame, battery, fifth_wheel, catwalk, rear_gear],
        label="chassis_complete",
    )
    return chassis_assembly


if __name__ == "__main__":
    chassis()
