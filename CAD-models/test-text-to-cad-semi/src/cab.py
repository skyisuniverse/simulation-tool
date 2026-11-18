"""Aerodynamic Cab Body, Panoramic Glasshouse, Side Skirts, and Fairings for Tesla Semi."""

import math
import build123d as bd
from cad import model

from constants import (
    COLOR_AERO_SKIRTS,
    COLOR_CAB_ACCENT,
    COLOR_CAB_BODY,
    COLOR_GLASS,
    COLOR_HEADLIGHT,
    COLOR_HEADLIGHT_ACCENT,
    COLOR_SKIRT_TRIM,
    TIRE_RADIUS,
    X_CAB_BACK,
    X_DRIVE_AXLE_1,
    X_DRIVE_AXLE_2,
    X_FRONT_AXLE,
    Y_AERO_SKIRT_HALF,
    Y_CAB_BASE_HALF,
    Y_ROOF_HALF,
    Z_BUMPER_BOTTOM,
    Z_CAB_FLOOR,
    Z_ROOF_TOP,
)


def make_cab_body():
    """Generates the aerodynamic Tesla Semi cab shell using a continuous aerodynamic profile."""
    # Side profile polygon in X-Z plane (at Y = 0, extruded across cab width)
    # Recreates Tesla Semi's signature aerodynamic bullet-train profile:
    profile_pts = [
        (40.0, 240.0),      # Front splitter tip
        (75.0, 500.0),      # Lower bumper
        (130.0, 850.0),     # Mid nose
        (250.0, 1150.0),    # Upper nose / hood crease
        (450.0, 1460.0),    # Windshield base
        (1920.0, 2740.0),   # Windshield crown / roof fairing base
        (2800.0, 3920.0),   # Roof fairing apex
        (3450.0, 3900.0),   # Roof fairing rear
        (3450.0, 1020.0),   # Cab back wall base at catwalk
        (1400.0, 1020.0),   # Cab floor above chassis
        (1400.0, 520.0),    # Wheel well inner vertical wall
        (600.0, 520.0),     # Floor front
        (600.0, 240.0),     # Bumper bottom back
    ]

    with bd.BuildSketch(bd.Plane.XZ) as profile_sketch:
        with bd.BuildLine():
            poly = bd.Polyline(profile_pts, close=True)
        bd.make_face()

    cab_w = 2.0 * Y_CAB_BASE_HALF  # 2320 mm
    cab_solid = bd.extrude(profile_sketch.sketch, amount=cab_w / 2.0, both=True)

    # Aerodynamic front corner tapers (in plan view)
    taper_l = (
        bd.Pos(180.0, Y_CAB_BASE_HALF + 320.0, 1000.0)
        * bd.Rot(0, 0, 19.0)
        * bd.Box(1300.0, 800.0, 2600.0)
    )
    taper_r = (
        bd.Pos(180.0, -Y_CAB_BASE_HALF - 320.0, 1000.0)
        * bd.Rot(0, 0, -19.0)
        * bd.Box(1300.0, 800.0, 2600.0)
    )
    cab_solid = cab_solid - taper_l - taper_r

    # Taper roof fairing width from 2320 mm down to 2100 mm (Y_ROOF_HALF = 1050)
    roof_taper_l = bd.Pos(2600.0, Y_CAB_BASE_HALF + 200.0, 3350.0) * bd.Box(1800.0, 400.0, 1300.0)
    roof_taper_r = bd.Pos(2600.0, -Y_CAB_BASE_HALF - 200.0, 3350.0) * bd.Box(1800.0, 400.0, 1300.0)
    cab_solid = cab_solid - roof_taper_l - roof_taper_r

    # Front wheel well cutouts
    arch_r = TIRE_RADIUS + 85.0
    arch_l = bd.Pos(X_FRONT_AXLE, Y_CAB_BASE_HALF, 520.0) * bd.Rot(90, 0, 0) * bd.Cylinder(arch_r, 450.0)
    arch_r_solid = bd.Pos(X_FRONT_AXLE, -Y_CAB_BASE_HALF, 520.0) * bd.Rot(90, 0, 0) * bd.Cylinder(arch_r, 450.0)
    cab_solid = cab_solid - arch_l - arch_r_solid

    # Trailer side extender wings extending behind cab back wall (X=3450 to 3780)
    wing_len = 330.0
    wing_t = 38.0
    wing_h = Z_ROOF_TOP - 1100.0
    wing_z = 1100.0 + wing_h / 2.0
    wing_l = bd.Pos(X_CAB_BACK + wing_len / 2.0, Y_CAB_BASE_HALF - 20.0, wing_z) * bd.Box(wing_len, wing_t, wing_h)
    wing_r = bd.Pos(X_CAB_BACK + wing_len / 2.0, -Y_CAB_BASE_HALF + 20.0, wing_z) * bd.Box(wing_len, wing_t, wing_h)
    cab_solid = cab_solid + wing_l + wing_r

    cab_solid.color = COLOR_CAB_BODY
    cab_solid.label = "cab_body"
    return cab_solid


def make_greenhouse_and_glass():
    """Wraparound panoramic windshield, side windows, and dark cockpit greenhouse canopy."""
    cab_w = 2.0 * Y_CAB_BASE_HALF  # 2320 mm

    # Windshield geometry: spans from (450, 1460) to (1920, 2740)
    ws_dx = 1920.0 - 450.0  # 1470 mm
    ws_dz = 2740.0 - 1460.0  # 1280 mm
    ws_len = math.sqrt(ws_dx**2 + ws_dz**2)  # ~1949 mm
    ws_angle = math.degrees(math.atan2(ws_dz, ws_dx))  # ~41.05 deg
    ws_cx = (450.0 + 1920.0) / 2.0  # 1185 mm
    ws_cz = (1460.0 + 2740.0) / 2.0  # 2100 mm
    ws_w = cab_w - 60.0
    ws_t = 26.0

    windshield = bd.Pos(ws_cx, 0, ws_cz + 4.0) * bd.Rot(0, -ws_angle, 0) * bd.Box(ws_len - 35.0, ws_w, ws_t)
    windshield.color = COLOR_GLASS
    windshield.label = "windshield_glass"

    # Gloss black A-pillars / ceramic border
    pillar_l = bd.Pos(ws_cx, Y_CAB_BASE_HALF - 20.0, ws_cz + 6.0) * bd.Rot(0, -ws_angle, 0) * bd.Box(ws_len - 15.0, 42.0, ws_t + 4.0)
    pillar_r = bd.Pos(ws_cx, -Y_CAB_BASE_HALF + 20.0, ws_cz + 6.0) * bd.Rot(0, -ws_angle, 0) * bd.Box(ws_len - 15.0, 42.0, ws_t + 4.0)
    pillar_l.color = COLOR_CAB_ACCENT
    pillar_r.color = COLOR_CAB_ACCENT
    pillar_l.label = "a_pillar_left"
    pillar_r.label = "a_pillar_right"

    # Side cockpit windows (flush dark tinted glass)
    side_w_len = 1080.0
    side_w_h = 590.0
    side_w_t = 24.0
    side_win_l = bd.Pos(2000.0, Y_CAB_BASE_HALF - 6.0, 2150.0) * bd.Box(side_w_len, side_w_t, side_w_h)
    side_win_r = bd.Pos(2000.0, -Y_CAB_BASE_HALF + 6.0, 2150.0) * bd.Box(side_w_len, side_w_t, side_w_h)
    side_win_l.color = COLOR_GLASS
    side_win_r.color = COLOR_GLASS
    side_win_l.label = "side_window_left"
    side_win_r.label = "side_window_right"

    # Black B-pillar window trim surrounding side windows
    b_pillar_l = bd.Pos(2580.0, Y_CAB_BASE_HALF - 4.0, 2150.0) * bd.Box(90.0, side_w_t + 4.0, side_w_h + 30.0)
    b_pillar_r = bd.Pos(2580.0, -Y_CAB_BASE_HALF + 4.0, 2150.0) * bd.Box(90.0, side_w_t + 4.0, side_w_h + 30.0)
    b_pillar_l.color = COLOR_CAB_ACCENT
    b_pillar_r.color = COLOR_CAB_ACCENT

    greenhouse = bd.Compound(
        children=[windshield, pillar_l, pillar_r, side_win_l, side_win_r, b_pillar_l, b_pillar_r],
        label="cockpit_greenhouse",
    )
    return greenhouse


def make_fascia_and_lighting():
    """Front bumper lower intake, aerodynamic splitter, LED headlights, and badging."""
    cab_w = 2.0 * Y_CAB_BASE_HALF

    # Lower front cooling intake slot
    intake = bd.Pos(65.0, 0, 390.0) * bd.Box(90.0, 1260.0, 92.0)
    intake.color = COLOR_CAB_ACCENT
    intake.label = "intake_slot"

    # Front splitter bottom lip (extends forward for aerodynamic downforce)
    splitter = bd.Pos(340.0, 0, Z_BUMPER_BOTTOM + 15.0) * bd.Box(680.0, cab_w + 30.0, 30.0)
    splitter.color = COLOR_SKIRT_TRIM
    splitter.label = "front_splitter"

    # Sleek angled LED headlight units
    hl_l = bd.Pos(120.0, 880.0, 720.0) * bd.Rot(0, -10.0, -18.0) * bd.Box(90.0, 270.0, 52.0)
    hl_l.color = COLOR_HEADLIGHT
    hl_l.label = "headlight_left"

    hl_drl_l = bd.Pos(100.0, 880.0, 742.0) * bd.Rot(0, -10.0, -18.0) * bd.Box(20.0, 260.0, 12.0)
    hl_drl_l.color = COLOR_HEADLIGHT_ACCENT
    hl_drl_l.label = "drl_strip_left"

    hl_r = bd.Pos(120.0, -880.0, 720.0) * bd.Rot(0, -10.0, 18.0) * bd.Box(90.0, 270.0, 52.0)
    hl_r.color = COLOR_HEADLIGHT
    hl_r.label = "headlight_right"

    hl_drl_r = bd.Pos(100.0, -880.0, 742.0) * bd.Rot(0, -10.0, 18.0) * bd.Box(20.0, 260.0, 12.0)
    hl_drl_r.color = COLOR_HEADLIGHT_ACCENT
    hl_drl_r.label = "drl_strip_right"

    # Front Tesla hood emblem badge
    badge = bd.Pos(180.0, 0, 1100.0) * bd.Rot(0, -22.0, 0) * bd.Box(15.0, 80.0, 35.0)
    badge.color = "#FFFFFF"
    badge.label = "tesla_badge"

    # 5 amber roof marker / clearance pods
    roof_pods = []
    for i, y in enumerate([-700.0, -350.0, 0.0, 350.0, 700.0]):
        pod = bd.Pos(2820.0, y, 3925.0) * bd.Box(50.0, 70.0, 18.0)
        pod.color = "#F59E0B"
        pod.label = f"roof_pod_{i+1}"
        roof_pods.append(pod)

    fascia = bd.Compound(
        children=[intake, splitter, hl_l, hl_drl_l, hl_r, hl_drl_r, badge] + roof_pods,
        label="fascia_lighting",
    )
    return fascia


def make_side_skirts_and_fenders():
    """Full-length aerodynamic side skirts with boarding steps and rear tandem fenders."""
    skirt_len = 3150.0
    skirt_w = 110.0
    skirt_h = Z_CAB_FLOOR - Z_BUMPER_BOTTOM + 80.0
    skirt_cx = 2050.0 + skirt_len / 2.0
    skirt_cz = Z_BUMPER_BOTTOM + skirt_h / 2.0

    skirt_l = bd.Pos(skirt_cx, Y_AERO_SKIRT_HALF - skirt_w / 2.0, skirt_cz) * bd.Box(skirt_len, skirt_w, skirt_h)
    skirt_r = bd.Pos(skirt_cx, -Y_AERO_SKIRT_HALF + skirt_w / 2.0, skirt_cz) * bd.Box(skirt_len, skirt_w, skirt_h)

    # Recessed driver boarding steps
    step1_l = bd.Pos(2400.0, Y_AERO_SKIRT_HALF, 450.0) * bd.Box(480.0, skirt_w + 20.0, 85.0)
    step2_l = bd.Pos(2400.0, Y_AERO_SKIRT_HALF, 680.0) * bd.Box(480.0, skirt_w + 20.0, 85.0)
    skirt_l = skirt_l - step1_l - step2_l

    step1_r = bd.Pos(2400.0, -Y_AERO_SKIRT_HALF, 450.0) * bd.Box(480.0, skirt_w + 20.0, 85.0)
    step2_r = bd.Pos(2400.0, -Y_AERO_SKIRT_HALF, 680.0) * bd.Box(480.0, skirt_w + 20.0, 85.0)
    skirt_r = skirt_r - step1_r - step2_r

    # Grip tread pads inside steps
    pad1_l = bd.Pos(2400.0, Y_AERO_SKIRT_HALF - 40.0, 420.0) * bd.Box(440.0, 70.0, 18.0)
    pad2_l = bd.Pos(2400.0, Y_AERO_SKIRT_HALF - 40.0, 650.0) * bd.Box(440.0, 70.0, 18.0)
    pad1_l.color = COLOR_SKIRT_TRIM
    pad2_l.color = COLOR_SKIRT_TRIM

    pad1_r = bd.Pos(2400.0, -Y_AERO_SKIRT_HALF + 40.0, 420.0) * bd.Box(440.0, 70.0, 18.0)
    pad2_r = bd.Pos(2400.0, -Y_AERO_SKIRT_HALF + 40.0, 650.0) * bd.Box(440.0, 70.0, 18.0)
    pad1_r.color = COLOR_SKIRT_TRIM
    pad2_r.color = COLOR_SKIRT_TRIM

    skirt_l.color = COLOR_AERO_SKIRTS
    skirt_r.color = COLOR_AERO_SKIRTS
    skirt_l.label = "aero_skirt_left"
    skirt_r.label = "aero_skirt_right"

    # Rear tandem wheel aero quarter fairings (fenders over tandem drive wheels)
    rear_arch_len = 2050.0
    rear_arch_h = 320.0
    rear_arch_z = 520.0 + TIRE_RADIUS + rear_arch_h / 2.0 - 120.0
    rear_arch_x = (X_DRIVE_AXLE_1 + X_DRIVE_AXLE_2) / 2.0

    rear_fender_l = bd.Pos(rear_arch_x, Y_AERO_SKIRT_HALF - 60.0, rear_arch_z) * bd.Box(rear_arch_len, 120.0, rear_arch_h)
    rear_fender_r = bd.Pos(rear_arch_x, -Y_AERO_SKIRT_HALF + 60.0, rear_arch_z) * bd.Box(rear_arch_len, 120.0, rear_arch_h)

    cut_w1_l = bd.Pos(X_DRIVE_AXLE_1, Y_AERO_SKIRT_HALF, 520.0) * bd.Rot(90, 0, 0) * bd.Cylinder(TIRE_RADIUS + 70.0, 300.0)
    cut_w2_l = bd.Pos(X_DRIVE_AXLE_2, Y_AERO_SKIRT_HALF, 520.0) * bd.Rot(90, 0, 0) * bd.Cylinder(TIRE_RADIUS + 70.0, 300.0)
    rear_fender_l = rear_fender_l - cut_w1_l - cut_w2_l

    cut_w1_r = bd.Pos(X_DRIVE_AXLE_1, -Y_AERO_SKIRT_HALF, 520.0) * bd.Rot(90, 0, 0) * bd.Cylinder(TIRE_RADIUS + 70.0, 300.0)
    cut_w2_r = bd.Pos(X_DRIVE_AXLE_2, -Y_AERO_SKIRT_HALF, 520.0) * bd.Rot(90, 0, 0) * bd.Cylinder(TIRE_RADIUS + 70.0, 300.0)
    rear_fender_r = rear_fender_r - cut_w1_r - cut_w2_r

    rear_fender_l.color = COLOR_AERO_SKIRTS
    rear_fender_r.color = COLOR_AERO_SKIRTS
    rear_fender_l.label = "rear_fender_left"
    rear_fender_r.label = "rear_fender_right"

    # Skirt bottom lip trim (satin dark edge)
    lip_h = 30.0
    lip_l = bd.Pos(skirt_cx, Y_AERO_SKIRT_HALF - skirt_w / 2.0, Z_BUMPER_BOTTOM + lip_h / 2.0) * bd.Box(skirt_len, skirt_w + 10.0, lip_h)
    lip_r = bd.Pos(skirt_cx, -Y_AERO_SKIRT_HALF + skirt_w / 2.0, Z_BUMPER_BOTTOM + lip_h / 2.0) * bd.Box(skirt_len, skirt_w + 10.0, lip_h)
    lip_l.color = COLOR_SKIRT_TRIM
    lip_r.color = COLOR_SKIRT_TRIM

    skirts = bd.Compound(
        children=[
            skirt_l,
            skirt_r,
            pad1_l,
            pad2_l,
            pad1_r,
            pad2_r,
            rear_fender_l,
            rear_fender_r,
            lip_l,
            lip_r,
        ],
        label="side_skirting",
    )
    return skirts


def make_aero_mirrors():
    """Tesla Semi digital camera mirror wings."""
    wing_w = 240.0
    wing_l = bd.Pos(1950.0, Y_CAB_BASE_HALF + wing_w / 2.0 - 15.0, 1950.0) * bd.Box(180.0, wing_w, 24.0)
    wing_r = bd.Pos(1950.0, -Y_CAB_BASE_HALF - wing_w / 2.0 + 15.0, 1950.0) * bd.Box(180.0, wing_w, 24.0)
    cam_l = bd.Pos(1980.0, Y_CAB_BASE_HALF + wing_w - 20.0, 1950.0) * bd.Box(70.0, 40.0, 50.0)
    cam_r = bd.Pos(1980.0, -Y_CAB_BASE_HALF - wing_w + 20.0, 1950.0) * bd.Box(70.0, 40.0, 50.0)
    lens_l = bd.Pos(2015.0, Y_CAB_BASE_HALF + wing_w - 20.0, 1950.0) * bd.Rot(0, 90, 0) * bd.Cylinder(12.0, 10.0)
    lens_r = bd.Pos(2015.0, -Y_CAB_BASE_HALF - wing_w + 20.0, 1950.0) * bd.Rot(0, 90, 0) * bd.Cylinder(12.0, 10.0)

    lens_l.color = "#0F172A"
    lens_r.color = "#0F172A"

    mirrors_body = bd.Compound(children=[wing_l, wing_r, cam_l, cam_r])
    mirrors_body.color = COLOR_CAB_ACCENT

    mirrors = bd.Compound(children=[mirrors_body, lens_l, lens_r], label="aero_mirrors")
    return mirrors


@model
def cab():
    body = make_cab_body()
    glass = make_greenhouse_and_glass()
    fascia = make_fascia_and_lighting()
    skirts = make_side_skirts_and_fenders()
    mirrors = make_aero_mirrors()

    cab_complete = bd.Compound(
        children=[body, glass, fascia, skirts, mirrors],
        label="tesla_semi_cab",
    )
    return cab_complete


if __name__ == "__main__":
    cab()
