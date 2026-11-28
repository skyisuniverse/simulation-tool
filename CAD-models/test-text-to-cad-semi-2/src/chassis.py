"""Tesla Semi 6x4 heavy-duty chassis, battery pack, tri-motor e-axles, and fifth wheel.

Builds:
  - chassis: Ladder frame rails & crossmembers, structural ~900 kWh under-floor
    battery pack with HV conduits, front steer axle & disc brakes, forward cruise
    e-axle & rearward dual-motor acceleration e-axle, air-ride suspension bellows,
    aluminum catwalk deck, gladhand air/electric utility mast, heavy-duty sliding
    36-inch fifth wheel coupling, rear quarter fenders, LED tail light crossmember,
    and rear mudflaps.
"""

import math
import build123d as bd
from bd_materials import metals, plastics
from cad import model

import dims as D


def _steel(part, color=D.COLOR_FRAME_STEEL, roughness=0.52, metalness=0.72):
    part.material = metals.mild_steel()
    part.material.pbr = part.material.pbr.override(roughness=roughness, metalness=metalness)
    part.color = color
    return part


def _aluminum(part, color=D.COLOR_ALUMINUM, roughness=0.36, metalness=0.85):
    part.material = metals.aluminum()
    part.material.pbr = part.material.pbr.override(roughness=roughness, metalness=metalness)
    part.color = color
    return part


def _plastic(part, color=D.COLOR_SKIRT_DARK, roughness=0.55, metalness=0.05):
    part.material = plastics.abs_()
    part.material.pbr = part.material.pbr.override(roughness=roughness, metalness=metalness)
    part.color = color
    return part


def _rubber(part, color=D.COLOR_TIRE_RUBBER, roughness=0.85):
    part.material = plastics.rubber()
    part.material.pbr = part.material.pbr.override(roughness=roughness)
    part.color = color
    return part


def _make_ladder_frame():
    """Twin heavy-duty C-channel steel frame rails with bolted crossmembers."""
    parts = []
    rail_len = D.FRAME_Y_END - D.FRAME_Y_START
    w = D.FRAME_RAIL_W
    h = D.FRAME_RAIL_H
    t = D.FRAME_WEB_T
    x_out = D.FRAME_OUTER_HALF_W
    x_in = x_out - w
    z0 = D.FRAME_Z_BOT
    z1 = D.FRAME_Z_TOP

    # Right (-X) and Left (+X) C-channel rails facing inward toward centerline
    for side, sgn in (("left", 1.0), ("right", -1.0)):
        pts = [
            (sgn * x_out, z0),
            (sgn * x_in, z0),
            (sgn * x_in, z0 + t),
            (sgn * (x_out - t), z0 + t),
            (sgn * (x_out - t), z1 - t),
            (sgn * x_in, z1 - t),
            (sgn * x_in, z1),
            (sgn * x_out, z1),
        ]
        if sgn < 0:
            pts = list(reversed(pts))
        with bd.BuildSketch(bd.Plane.XZ) as sk:
            with bd.BuildLine():
                bd.Polyline(*pts, close=True)
            bd.make_face()
        rail = bd.extrude(sk.sketch.face(), amount=rail_len, dir=(0, 1, 0))
        rail = bd.Pos(0, D.FRAME_Y_START, 0) * rail
        # Bevel rear bottom corner of frame rail like real Class 8 tractor
        bevel = (
            bd.Pos(sgn * (x_out - w / 2.0), D.FRAME_Y_END + 20.0, z0 - 20.0)
            * bd.Rot(-35, 0, 0)
            * bd.Box(w + 20.0, 160.0, 140.0)
        )
        rail = rail - bevel
        rail.label = f"frame_rail_{side}"
        parts.append(_steel(rail))

    # Structural tubular/boxed crossmembers between the inner rail webs (clear of flanges)
    xm_ys = [520.0, 1200.0, 1820.0, 2600.0, 3440.0, 4120.0, 4560.0, 5220.0, 5880.0, 6430.0]
    xm_span = (x_in - 1.0) * 2.0
    for idx, y in enumerate(xm_ys):
        xm = (
            bd.Pos(0.0, y, (z0 + z1) / 2.0)
            * bd.Box(xm_span, 76.0, h - 2.0 * t - 16.0)
        )
        xm.label = f"crossmember_{idx + 1}"
        parts.append(_steel(xm, color="#2D323A"))

    return bd.Compound(children=parts, label="ladder_frame")


def _make_battery_pack():
    """Structural under-floor ~900 kWh battery enclosure with cooling ribs & HV conduits."""
    parts = []
    length = D.BATT_Y_END - D.BATT_Y_START
    y_mid = (D.BATT_Y_START + D.BATT_Y_END) / 2.0
    hw = 880.0
    z0 = D.BATT_Z_BOT + 14.0
    z1 = D.BATT_Z_TOP
    h = z1 - z0

    # Main chamfered aluminum battery tray (tapered bottom edges for aero & ground clearance)
    with bd.BuildSketch(bd.Plane.XZ) as sk:
        with bd.BuildLine():
            bd.Polyline(
                (-hw + 85.0, z0),
                (hw - 85.0, z0),
                (hw, z0 + 75.0),
                (hw, z1),
                (-hw, z1),
                (-hw, z0 + 75.0),
                close=True,
            )
        bd.make_face()
    pack = bd.Pos(0, D.BATT_Y_START, 0) * bd.extrude(sk.sketch.face(), amount=length, dir=(0, 1, 0))
    pack.label = "battery_enclosure"
    parts.append(_aluminum(pack, color="#4B525C", roughness=0.48, metalness=0.72))

    # Brushed aluminum underbody protective skid ribs (7 longitudinal ribs)
    for i, rx in enumerate((-640.0, -420.0, -210.0, 0.0, 210.0, 420.0, 640.0)):
        rib = (
            bd.Pos(rx, y_mid, z0 - 7.0)
            * bd.Box(26.0, length - 120.0, 12.0)
        )
        rib.label = f"battery_skid_rib_{i + 1}"
        parts.append(_aluminum(rib, color=D.COLOR_ALUMINUM))

    # High-voltage orange armored power conduits running from battery aft to the rear e-axles
    for side, sx in (("left", 65.0), ("right", -65.0)):
        hv = (
            bd.Pos(sx, 4800.0, D.FRAME_Z_BOT - 38.0)
            * bd.Rot(90, 0, 0)
            * bd.Cylinder(17.0, 1740.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.CENTER))
        )
        hv.label = f"hv_conduit_{side}"
        parts.append(_plastic(hv, color=D.COLOR_HV_ORANGE, roughness=0.4))

    return bd.Compound(children=parts, label="battery_pack")


def _make_front_steer_axle():
    """Forged dropped front steer axle beam, ventilated disc brakes, and air/leaf springs."""
    parts = []
    y0 = D.Y_FRONT_AXLE
    z_axle = D.TIRE_R  # 516.0 mm

    # Forged dropped steel beam (spans X = -915 .. +915, drops in center for clearance)
    with bd.BuildSketch(bd.Plane.XZ) as sk:
        with bd.BuildLine():
            bd.Polyline(
                (-910.0, z_axle - 32.0),
                (-660.0, z_axle - 32.0),
                (-540.0, z_axle - 92.0),
                (540.0, z_axle - 92.0),
                (660.0, z_axle - 32.0),
                (910.0, z_axle - 32.0),
                (910.0, z_axle + 32.0),
                (640.0, z_axle + 32.0),
                (520.0, z_axle - 26.0),
                (-520.0, z_axle - 26.0),
                (-640.0, z_axle + 32.0),
                (-910.0, z_axle + 32.0),
                close=True,
            )
        bd.make_face()
    beam = bd.Pos(0, y0 - 38.0, 0) * bd.extrude(sk.sketch.face(), amount=76.0, dir=(0, 1, 0))
    beam.label = "steer_axle_beam"
    parts.append(_steel(beam, color=D.COLOR_CAST_STEEL))

    # Steering knuckles, brake discs & longitudinal leaf-spring perches (left & right)
    for side, sgn in (("left", 1.0), ("right", -1.0)):
        # Ventilated brake rotor inside wheel hub clearance (X = +/-924 mm, R = 210 mm)
        rotor = (
            bd.Pos(sgn * 930.0, y0, z_axle)
            * bd.Rot(0, 90, 0)
            * bd.Cylinder(208.0, 32.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.CENTER))
        )
        rotor.label = f"front_brake_rotor_{side}"
        parts.append(_steel(rotor, color="#7D8590", roughness=0.28, metalness=0.9))

        # Caliper housing straddling aft edge of rotor with clean rotor clearance slot
        caliper = (
            bd.Pos(sgn * 930.0, y0 + 175.0, z_axle + 15.0)
            * bd.Box(78.0, 120.0, 145.0)
            - bd.Pos(sgn * 930.0, y0, z_axle)
            * bd.Rot(0, 90, 0)
            * bd.Cylinder(212.0, 38.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.CENTER))
        )
        caliper.label = f"front_brake_caliper_{side}"
        parts.append(_steel(caliper, color="#3E444D"))

        # Parabolic front suspension spring pack under frame rail (X = +/-392)
        spring = (
            bd.Pos(sgn * 392.0, y0, (D.FRAME_Z_BOT + z_axle + 32.0) / 2.0 + 18.0)
            * bd.Box(78.0, 1080.0, 56.0)
        )
        spring.label = f"front_leaf_spring_{side}"
        parts.append(_steel(spring, color="#2A2E35"))

        # Spring hanger pedestals connecting axle beam up to spring
        pedestal = (
            bd.Pos(sgn * 392.0, y0, (z_axle - 24.0 + 622.0) / 2.0)
            * bd.Box(74.0, 110.0, 130.0)
        )
        pedestal.label = f"front_axle_pad_{side}"
        parts.append(_steel(pedestal, color=D.COLOR_CAST_STEEL))

    return bd.Compound(children=parts, label="front_steer_axle")


def _make_rear_drive_axles():
    """Tesla Semi tri-motor tandem drive e-axles + air-ride trailing suspension."""
    parts = []
    z_axle = D.TIRE_R  # 516.0 mm

    # --- Forward drive axle (Y = 4560): Permanent-magnet highway cruise motor ---
    y1 = D.Y_REAR_AXLE_1
    cruise_motor = (
        bd.Pos(0.0, y1 - 35.0, z_axle + 10.0)
        * bd.Rot(0, 90, 0)
        * bd.Cylinder(155.0, 410.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.CENTER))
    )
    cruise_motor.label = "cruise_drive_motor"
    parts.append(_aluminum(cruise_motor, color="#9BA3AD", roughness=0.35))

    for side, sgn in (("left", 1.0), ("right", -1.0)):
        tube1 = (
            bd.Pos(sgn * 440.0, y1, z_axle)
            * bd.Rot(0, 90, 0)
            * bd.Cylinder(62.0, 466.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.CENTER))
        )
        tube1.label = f"forward_axle_tube_{side}"
        parts.append(_steel(tube1, color=D.COLOR_CAST_STEEL))

    # --- Rearward drive axle (Y = 5880): Twin independent induction acceleration motors ---
    y2 = D.Y_REAR_AXLE_2
    # Center bridge between twin motors (-40..+40) and outer half-tubes (+/-312..+/-673)
    center_diff = (
        bd.Pos(0.0, y2, z_axle)
        * bd.Rot(0, 90, 0)
        * bd.Cylinder(62.0, 82.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.CENTER))
    )
    center_diff.label = "rearward_center_housing"
    parts.append(_steel(center_diff, color=D.COLOR_CAST_STEEL))

    for side, sgn in (("left", 1.0), ("right", -1.0)):
        accel_motor = (
            bd.Pos(sgn * 175.0, y2 - 40.0, z_axle + 10.0)
            * bd.Rot(0, 90, 0)
            * bd.Cylinder(142.0, 265.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.CENTER))
        )
        accel_motor.label = f"accel_drive_motor_{side}"
        parts.append(_aluminum(accel_motor, color="#9BA3AD", roughness=0.35))

        tube2 = (
            bd.Pos(sgn * 492.0, y2, z_axle)
            * bd.Rot(0, 90, 0)
            * bd.Cylinder(62.0, 362.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.CENTER))
        )
        tube2.label = f"rearward_axle_tube_{side}"
        parts.append(_steel(tube2, color=D.COLOR_CAST_STEEL))

    # --- Air-ride trailing suspension beams, air spring bellows & disc brakes ---
    for ax_name, y_ax in (("fwd", y1), ("aft", y2)):
        for side, sgn in (("left", 1.0), ("right", -1.0)):
            # Air-ride trailing arm cleanly above axle tube (Z=582..652) & outboard of frame rail (435)
            arm = (
                bd.Pos(sgn * 516.0, y_ax + 65.0, 618.0)
                * bd.Box(68.0, 620.0, 70.0)
            )
            arm.label = f"susp_arm_{ax_name}_{side}"
            parts.append(_steel(arm, color="#2D323A"))

            # Ribbed rubber air-suspension bellows (X=516, R=72 => 444..588: clear of rail 435 & tire 597.5)
            bellows = (
                bd.Pos(sgn * 516.0, y_ax + 280.0, 718.0)
                * bd.Cylinder(72.0, 124.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.CENTER))
            )
            bellows.label = f"air_spring_{ax_name}_{side}"
            parts.append(_rubber(bellows, color="#1D1F24"))

            # Upper air-spring outrigger bracket welded outboard of frame rail (X = 437..575, Z = 784..848)
            bracket = (
                bd.Pos(sgn * 506.0, y_ax + 280.0, 816.0)
                * bd.Box(136.0, 165.0, 64.0)
            )
            bracket.label = f"air_spring_bracket_{ax_name}_{side}"
            parts.append(_steel(bracket))

            # Heavy-duty ventilated brake disc with axle bore (R_in = 65 > R_tube 62)
            rotor = (
                bd.Pos(sgn * 572.0, y_ax, z_axle)
                * bd.Rot(0, 90, 0)
                * (
                    bd.Cylinder(210.0, 28.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.CENTER))
                    - bd.Cylinder(65.0, 34.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.CENTER))
                )
            )
            rotor.label = f"rear_brake_rotor_{ax_name}_{side}"
            parts.append(_steel(rotor, color="#7D8590", roughness=0.28, metalness=0.9))

    return bd.Compound(children=parts, label="rear_drive_axles")


def _make_fifth_wheel():
    """Authentic heavy-duty sliding 36-inch cast-steel fifth wheel coupling at Z = 1220 mm."""
    parts = []
    yc = D.FIFTH_WHEEL_Y  # 5180.0 mm
    z_frame = D.FRAME_Z_TOP  # 1020.0 mm
    z_top = D.FIFTH_WHEEL_Z_TOP  # 1220.0 mm

    # Twin toothed slide tracks bolted atop the frame rails
    for side, sgn in (("left", 1.0), ("right", -1.0)):
        track = (
            bd.Pos(sgn * (D.FRAME_OUTER_HALF_W - D.FRAME_RAIL_W / 2.0), yc, z_frame + 22.0)
            * bd.Box(D.FRAME_RAIL_W - 4.0, 1080.0, 40.0)
        )
        track.label = f"fifth_wheel_slide_rail_{side}"
        parts.append(_steel(track, color="#2D323A"))

    # Sliding sub-frame base plate spanning the tracks (Z = 1064 .. 1094)
    base_plate = (
        bd.Pos(0.0, yc, z_frame + 60.0)
        * bd.Box(D.FRAME_OUTER_HALF_W * 2.0 + 10.0, 640.0, 30.0)
    )
    base_plate.label = "fifth_wheel_base"
    parts.append(_steel(base_plate, color="#2A2F36"))

    # Twin heavy cast-steel trunnion pivot brackets supporting the fifth-wheel plate
    for side, sgn in (("left", 1.0), ("right", -1.0)):
        trunnion = (
            bd.Pos(sgn * 265.0, yc - 20.0, 1126.0)
            * bd.Box(84.0, 250.0, 62.0)
        )
        trunnion.label = f"fifth_wheel_trunnion_{side}"
        parts.append(_steel(trunnion, color=D.COLOR_CAST_STEEL))

    # Sculpted horseshoe cast-steel fifth-wheel top plate (D = 920 mm, Z = 1160 .. 1220)
    r_plate = D.FIFTH_WHEEL_DIA / 2.0  # 460.0 mm
    plate_h = 58.0
    z_plate_bot = z_top - plate_h  # 1162.0 mm

    plate = (
        bd.Pos(0.0, yc, z_plate_bot)
        * bd.Cylinder(r_plate, plate_h, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    )

    # Cut authentic rear V-shaped kingpin throat opening (+Y faces rearward)
    with bd.BuildSketch(bd.Plane.XY) as throat_sk:
        with bd.BuildLine():
            bd.Polyline(
                (-38.0, yc - 35.0),
                (38.0, yc - 35.0),
                (38.0, yc + 95.0),
                (235.0, yc + r_plate + 40.0),
                (-235.0, yc + r_plate + 40.0),
                (-38.0, yc + 95.0),
                close=True,
            )
        bd.make_face()
    throat_cut = bd.Pos(0, 0, z_plate_bot - 10.0) * bd.extrude(
        throat_sk.sketch.face(), amount=plate_h + 20.0, dir=(0, 0, 1)
    )

    # Cut gentle rear lead-in ramp bevels on the two rear horns (+Y side)
    ramp_cut = (
        bd.Pos(0.0, yc + r_plate - 30.0, z_top + 10.0)
        * bd.Rot(14, 0, 0)
        * bd.Box(D.FIFTH_WHEEL_DIA + 40.0, 260.0, 60.0)
    )

    # Cut concentric grease grooves on the top bearing face
    grease_groove = (
        bd.Pos(0.0, yc, z_top - 4.0)
        * (
            bd.Cylinder(315.0, 10.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
            - bd.Cylinder(295.0, 12.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        )
    )

    plate = plate - [throat_cut, ramp_cut, grease_groove]
    plate.label = "fifth_wheel_plate"
    parts.append(_steel(plate, color=D.COLOR_CAST_STEEL, roughness=0.45, metalness=0.78))

    # Driver-side (+X) fifth wheel jaw release pull handle (clear of 460 mm radius plate)
    handle = (
        bd.Pos(565.0, yc + 35.0, z_plate_bot + 26.0)
        * bd.Rot(0, 90, 0)
        * bd.Cylinder(11.0, 200.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.CENTER))
    )
    handle.label = "fifth_wheel_release_handle"
    parts.append(_steel(handle, color=D.COLOR_CHROME, roughness=0.25, metalness=0.9))

    return bd.Compound(children=parts, label="fifth_wheel")


def _make_catwalk_and_utility_mast():
    """Brushed aluminum catwalk behind the cab + gladhand air/electrical hose tender."""
    parts = []
    # Slotted aluminum catwalk sitting cleanly above frame rails (Y = 3600 .. 4220)
    cw_len = 600.0
    cw_w = 910.0
    cw_h = 24.0
    cw_y = 3910.0
    cw_z = D.FRAME_Z_TOP + 2.0

    catwalk = (
        bd.Pos(0.0, cw_y, cw_z)
        * bd.Box(cw_w, cw_len, cw_h, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    )
    # Cut anti-slip traction slots across deck
    slots = []
    for i in range(6):
        sy = cw_y - 210.0 + i * 84.0
        for sx in (-250.0, 0.0, 250.0):
            slots.append(
                bd.Pos(sx, sy, cw_z - 2.0)
                * bd.Box(160.0, 26.0, cw_h + 6.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
            )
    catwalk = catwalk - slots
    catwalk.label = "catwalk_deck"
    parts.append(_aluminum(catwalk, color=D.COLOR_ALUMINUM, roughness=0.32))

    # Welded T-shaped utility mast / pogo stick mounted on catwalk (Y = 3685)
    mast_post = (
        bd.Pos(0.0, 3685.0, cw_z + cw_h + 2.0)
        * bd.Cylinder(22.0, 1080.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    )
    mast_bar = (
        bd.Pos(0.0, 3685.0, cw_z + cw_h + 1050.0)
        * bd.Rot(0, 90, 0)
        * bd.Cylinder(14.0, 440.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.CENTER))
    )
    mast = mast_post + mast_bar
    mast.label = "utility_mast"
    parts.append(_steel(mast, color=D.COLOR_TRIM_BLACK, roughness=0.45))

    # Stylized hanging trailer umbilical lines (clear aft of mast at Y >= 3745)
    for name, hx, col in (
        ("air_line_emergency", 150.0, D.COLOR_AIR_RED),
        ("electrical_cord_7way", 0.0, D.COLOR_TRIM_BLACK),
        ("air_line_service", -150.0, D.COLOR_AIR_BLUE),
    ):
        path = bd.Spline(
            (hx, 3748.0, cw_z + cw_h + 1020.0),
            (hx + 16.0, 3805.0, cw_z + cw_h + 620.0),
            (hx, 3855.0, cw_z + cw_h + 360.0),
            (hx - 16.0, 3805.0, cw_z + cw_h + 520.0),
            (hx, 3748.0, cw_z + cw_h + 740.0),
        )
        profile = bd.Plane(origin=path @ 0, z_dir=path % 0) * bd.Circle(13.0)
        hose = bd.sweep(profile, path=path)
        hose.label = name
        parts.append(_plastic(hose, color=col, roughness=0.42))

    return bd.Compound(children=parts, label="catwalk_and_lines")


def _make_rear_quarter_fenders_and_tail():
    """Sculpted aerodynamic black rear quarter fenders, rear LED tail crossmember & mudflaps."""
    parts = []

    # --- Sculpted aerodynamic rear quarter fenders ahead of forward tandem wheels ---
    # Concentric arc centered at (Y_REAR_AXLE_1, TIRE_R) with 48 mm clearance over 516 mm tire
    # and clean air gap behind rear cab aero seal (Y <= 3988)
    r_in = D.TIRE_R + 48.0   # 564.0 mm
    r_out = r_in + 14.0      # 578.0 mm (frontmost point at 4560 - 578*cos(12 deg) = 3994 > 3988!)
    pts_out = []
    pts_in = []
    n_seg = 16
    a_start = math.radians(92.0)
    a_end = math.radians(168.0)
    for i in range(n_seg + 1):
        ang = a_start + (a_end - a_start) * (i / n_seg)
        pts_out.append((D.Y_REAR_AXLE_1 + r_out * math.cos(ang), D.TIRE_R + r_out * math.sin(ang)))
        pts_in.append((D.Y_REAR_AXLE_1 + r_in * math.cos(ang), D.TIRE_R + r_in * math.sin(ang)))

    with bd.BuildSketch(bd.Plane.YZ) as fsk:
        with bd.BuildLine():
            s_out = bd.Spline(*pts_out)
            l_bot = bd.Line(pts_out[-1], pts_in[-1])
            s_in = bd.Spline(*list(reversed(pts_in)))
            l_top = bd.Line(pts_in[0], pts_out[0])
        bd.make_face()
    qf_face = fsk.sketch.face()

    for side, sgn in (("left", 1.0), ("right", -1.0)):
        # Spans width of dual tandem tires: |X| = 585 .. 1252 mm (667 mm wide)
        x_start = 585.0 if sgn > 0 else -1252.0
        qf = bd.Pos(x_start, 0.0, 0.0) * bd.extrude(qf_face, amount=667.0, dir=(1, 0, 0))
        qf.label = f"quarter_fender_{side}"
        parts.append(_plastic(qf, color=D.COLOR_BUMPER_DARK, roughness=0.42))

        # Horizontal mounting tube from outer frame rail (437) into quarter fender inner face (584)
        mount = (
            bd.Pos(sgn * 511.0, 4050.0, 815.0)
            * bd.Rot(0, 90, 0)
            * bd.Cylinder(20.0, 146.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.CENTER))
        )
        mount.label = f"quarter_fender_post_{side}"
        parts.append(_steel(mount, color=D.COLOR_TRIM_BLACK))

    # --- Rear bumper closing crossmember & sleek LED tail lights (Y = 6512 .. 6560) ---
    rear_bar = (
        bd.Pos(0.0, 6536.0, 888.0)
        * bd.Box(1060.0, 48.0, 260.0)
    )
    rear_bar.label = "rear_crossmember"
    parts.append(_steel(rear_bar, color=D.COLOR_BUMPER_DARK, roughness=0.45))

    # Sleek Tesla-style horizontal LED tail light clusters (left & right)
    for side, sgn in (("left", 1.0), ("right", -1.0)):
        # Black recessed bezel on +Y face (Y = 6560 .. 6566)
        bezel = (
            bd.Pos(sgn * 340.0, 6563.0, 898.0)
            * bd.Box(260.0, 6.0, 96.0)
        )
        bezel.label = f"taillight_bezel_{side}"
        parts.append(_plastic(bezel, color=D.COLOR_TRIM_BLACK, roughness=0.25))

        # Crimson LED brake / tail light bar
        red_led = (
            bd.Pos(sgn * 340.0, 6568.0, 916.0)
            * bd.Box(235.0, 4.0, 34.0)
        )
        red_led.label = f"taillight_red_{side}"
        red_led.material = plastics.pmma()
        red_led.material.pbr = red_led.material.pbr.override(
            roughness=0.15, emissive=(0.85, 0.05, 0.05), emissive_intensity=2.0
        )
        red_led.color = D.COLOR_LED_RED
        parts.append(red_led)

        # Amber turn indicator & white reverse bar below
        amb_led = (
            bd.Pos(sgn * 388.0, 6568.0, 874.0)
            * bd.Box(135.0, 4.0, 24.0)
        )
        amb_led.label = f"taillight_amber_{side}"
        amb_led.material = plastics.pmma()
        amb_led.material.pbr = amb_led.material.pbr.override(
            roughness=0.15, emissive=(0.95, 0.5, 0.0), emissive_intensity=1.5
        )
        amb_led.color = D.COLOR_LED_AMBER
        parts.append(amb_led)

        rev_led = (
            bd.Pos(sgn * 265.0, 6568.0, 874.0)
            * bd.Box(85.0, 4.0, 24.0)
        )
        rev_led.label = f"taillight_reverse_{side}"
        rev_led.material = plastics.pmma()
        rev_led.material.pbr = rev_led.material.pbr.override(
            roughness=0.12, emissive=(0.9, 0.94, 1.0), emissive_intensity=1.2
        )
        rev_led.color = D.COLOR_LED_WHITE
        parts.append(rev_led)

    # Rear license plate panel in center of rear crossmember
    plate = bd.Pos(0.0, 6563.0, 888.0) * bd.Box(305.0, 4.0, 155.0)
    plate.label = "rear_license_plate"
    parts.append(_aluminum(plate, color="#E6E9EE", roughness=0.35))

    # --- Heavy-duty rear mudflaps & stainless anti-sail hangers (Y = 6462 mm) ---
    for side, sgn in (("left", 1.0), ("right", -1.0)):
        # Mudflap hanger bar anchored at outer frame rail (X = +/-437 .. +/-1240)
        hanger = (
            bd.Pos(sgn * 842.0, 6462.0, 865.0)
            * bd.Box(805.0, 32.0, 44.0)
        )
        hanger.label = f"mudflap_hanger_{side}"
        parts.append(_aluminum(hanger, color=D.COLOR_CHROME, roughness=0.22, metalness=0.92))

        # Wide heavy rubber mudflap behind dual tires (62 mm clear of tire at Y = 6396)
        flap = (
            bd.Pos(sgn * 920.0, 6462.0, 502.0)
            * bd.Box(640.0, 14.0, 675.0)
        )
        flap.label = f"rear_mudflap_{side}"
        parts.append(_rubber(flap, color=D.COLOR_SKIRT_DARK, roughness=0.82))

    return bd.Compound(children=parts, label="rear_fenders_and_tail")


@model
def chassis():
    """Complete Tesla Semi 6x4 structural chassis, battery pack, e-axles & fifth wheel."""
    children = [
        _make_ladder_frame(),
        _make_battery_pack(),
        _make_front_steer_axle(),
        _make_rear_drive_axles(),
        _make_fifth_wheel(),
        _make_catwalk_and_utility_mast(),
        _make_rear_quarter_fenders_and_tail(),
    ]
    asm = bd.Compound(children=children, label="chassis")
    bb = asm.bounding_box()
    assert abs(bb.max.Y - D.TOTAL_LENGTH) < 15.0, f"Chassis rear Y mismatch: {bb.max.Y}"
    return asm


if __name__ == "__main__":
    chassis()
