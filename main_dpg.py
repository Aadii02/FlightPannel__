import dearpygui.dearpygui as dpg
import numpy as np
import time
from datetime import datetime, timezone, timedelta
from PIL import Image
import os

# Import operation modules
from tank_operations_dpg import open_tank_operations
from vehicle_operations_dpg import open_vehicle_operations
from engine_operations_dpg import open_engine_operations

# Mission start time (resets each launch)
mission_start_time = time.time()

# Track whether system is stopped
system_stopped = False

# Sample data length and arrays
length = 100
x = np.linspace(0, 10, length)

#max limit of the data 
MAX_POINTS = 100
#last update 
last_update = 0 

# Initialize with random values
y1 = np.random.randn(length).tolist()
y2 = np.random.randn(length).tolist()
y3 = np.random.randn(length).tolist()
vel = np.random.randn(length).tolist()
acc = np.random.randn(length).tolist()
alt = np.random.randn(length).tolist()

# Electrical signals
bat = (12 + np.sin(x)).tolist()
temp_in = (20 + np.sin(x)).tolist()
temp_out = (15 + np.cos(x)).tolist()
press_in = (101 + np.sin(x)).tolist()
press_out = (100 + np.cos(x)).tolist()

# Convert numpy array to list for DearPyGui
x_list = x.tolist()

# Colors
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
GREY = (170, 170, 170)

# Graph colors matching main.py (tkinter version)
COL_X_AXIS        = (0, 191, 255)      # deepskyblue
COL_Y_AXIS        = (0, 250, 154)      # mediumspringgreen
COL_Z_AXIS        = (255, 105, 180)    # hotpink
COL_VELOCITY      = (0, 255, 255)      # cyan
COL_ACCELERATION  = (0, 255, 0)        # lime
COL_ALTITUDE      = (255, 69, 0)       # orangered
COL_BATTERY       = (255, 255, 0)      # yellow
COL_TEMP_IN       = (255, 99, 71)      # tomato
COL_TEMP_OUT      = (135, 206, 235)    # skyblue
COL_PRESS_IN      = (238, 130, 238)    # violet
COL_PRESS_OUT     = (221, 160, 221)    # plum

# Create DearPyGui context
dpg.create_context()

# ── Fonts ──
with dpg.font_registry():
    _font_body_path = r"C:\Windows\Fonts\seguisb.ttf"   # Segoe UI Semibold
    _font_title_path = r"C:\Windows\Fonts\arialbd.ttf"  # Arial Bold
    _font_clock_path = r"C:\Windows\Fonts\consolab.ttf" # Consolas Bold
    font_body = dpg.add_font(_font_body_path, 16)
    font_title = dpg.add_font(_font_title_path, 28)
    font_status = dpg.add_font(_font_title_path, 18)
    font_button = dpg.add_font(_font_title_path, 16)
    font_clocks = dpg.add_font(_font_clock_path, 18)

# ── Load Logo Image ──
logo_texture_id = None
logo_width = 0
try:
    logo_path = r"C:\Users\AADITYA\OneDrive\Desktop\panel\images\logo.png"
    if os.path.exists(logo_path):
        img = Image.open(logo_path).convert("RGBA")
        img.thumbnail((220, 220), Image.Resampling.LANCZOS)
        logo_width = img.width
        img_data = np.array(img, dtype=np.float32) / 255.0
        with dpg.texture_registry(show=False):
            logo_texture_id = dpg.add_raw_texture(
                width=img.width,
                height=img.height,
                default_value=img_data,
                format=dpg.mvFormat_Float_rgba
            )
except Exception as e:
    print(f"Error loading logo: {e}")

# ── Global widget IDs ──
utc_label_id = None
ist_label_id = None
timer_label_id = None
status_indicator_id = None
gps_sat_label_id = None
telemetry_rate_label_id = None
delay_label_id = None
line_x_series_id = None
line_y_series_id = None
line_z_series_id = None
line_vel_series_id = None
line_acc_series_id = None
line_alt_series_id = None
line_batt_series_id = None
line_temp_in_series_id = None
line_temp_out_series_id = None
line_press_in_series_id = None
line_press_out_series_id = None

# Header telemetry status (simulated incoming link data)
gps_sat_available = 11
telemetry_rate_hz = 50.0
link_delay_ms = 180

# ── Button callbacks ──
def tank_command():
    print("Tank Operations button clicked!")
    try:
        open_tank_operations()
        print("Tank window opened successfully")
    except Exception as e:
        print(f"Error opening tank window: {e}")

def vehicle_command():
    print("Vehicle Operations button clicked!")
    try:
        open_vehicle_operations()
        print("Vehicle window opened successfully")
    except Exception as e:
        print(f"Error opening vehicle window: {e}")

def engine_command():
    print("Engine Control button clicked!")
    try:
        open_engine_operations()
        print("Engine window opened successfully")
    except Exception as e:
        print(f"Error opening engine window: {e}")

def stop_command():
    global system_stopped
    system_stopped = not system_stopped
    if system_stopped:
        dpg.set_value(status_indicator_id, "EMERGENCY STOP")
        dpg.bind_item_theme(status_indicator_id, red_text_theme)
    else:
        dpg.set_value(status_indicator_id, "SYSTEMS ONLINE")
        dpg.bind_item_theme(status_indicator_id, green_text_theme)

def roll_append(arr, center=0, scale=1):
    arr = np.roll(arr, -1)
    arr[-1] = center + np.random.randn() * scale
    return arr 

# ── Layout resize function ──
_HEADER_H = 320
_VPAD     = 20


# UI HEREEEE
def resize_layout():
    vp_h = dpg.get_viewport_client_height()
    avail = max(200, vp_h - _HEADER_H - _VPAD)

    # Left column: 3 equal stacked plots 
    #acc velocity and altitude graph space 
    lh = max(50, avail // 3)
    for _t in ("plot_vel", "plot_acc", "plot_alt"):
        dpg.configure_item(_t, height=lh)

    # Center column: XYZ row 28%, battery 20%, temp/pressure 26% each
    h_xyz  = max(50, int(avail * 0.28))
    h_batt = max(40, int(avail * 0.20))
    h_tp   = max(40, int(avail * 0.26))
    for _t in ("plot_x", "plot_y", "plot_z"):
        dpg.configure_item(_t, height=h_xyz)
    dpg.configure_item("plot_batt", height=h_batt)
    for _t in ("plot_temp_in", "plot_temp_out", "plot_press_in", "plot_press_out"):
        dpg.configure_item(_t, height=h_tp)

    # Right buttons: 4 equal
    btn_h = max(40, avail // 4)
    for _t in ("btn_tank", "btn_vehicle", "btn_engine", "btn_stop"):
        dpg.configure_item(_t, height=btn_h)

# ── Frame-based update ──
frame_counter = 0


#FRAME UPDATE
def update_callback():
    global last_update 
    global system_stopped, y1, y2, y3, vel, acc, alt, bat, temp_in, temp_out, press_in, press_out
    global frame_counter
    global gps_sat_available, telemetry_rate_hz, link_delay_ms
    frame_counter += 1

    # Clocks every frame is fine (cheap)
    utc_now = datetime.now(timezone.utc)
    ist_now = utc_now + timedelta(hours=5, minutes=30)
    dpg.set_value(utc_label_id, utc_now.strftime("UTC  %H:%M:%S"))
    dpg.set_value(ist_label_id, ist_now.strftime("IST  %H:%M:%S"))

    elapsed = int(time.time() - mission_start_time)
    h, rem = divmod(elapsed, 3600)
    m, s = divmod(rem, 60)
    dpg.set_value(timer_label_id, f"T+ {h:02d}:{m:02d}:{s:02d}")

    # Simulated incoming comms/status values
    if frame_counter % 30 == 0:
        gps_sat_available = int(np.clip(gps_sat_available + np.random.randint(-1, 2), 8, 16))
        telemetry_rate_hz = float(np.clip(telemetry_rate_hz + np.random.randn() * 1.4, 42.0, 58.0))
        link_delay_ms = int(np.clip(link_delay_ms + np.random.randint(-20, 21), 90, 320))

    dpg.set_value(gps_sat_label_id, f"GPS SAT AVAILABLE - {gps_sat_available}")
    dpg.set_value(telemetry_rate_label_id, f"TELEMETRY RATE - {telemetry_rate_hz:05.1f} Hz")
    dpg.set_value(delay_label_id, f"DELAY - {link_delay_ms} ms")

    # ── Dynamic centering + layout resize (every 5 frames) ──
    if frame_counter % 5 == 0:
        try:
            vp_w = dpg.get_viewport_client_width()
            mc_w = dpg.get_text_size("MISSION CONTROL", font=font_title)[0]
            clk_w = dpg.get_text_size("UTC  00:00:00", font=font_clocks)[0]
            istw = dpg.get_text_size("IST  00:00:00", font=font_clocks)[0]
            center_w = max(mc_w, clk_w + 30 + istw)
            lw = logo_width + 16 if logo_texture_id else 0
            sw = max(
                dpg.get_text_size("SYSTEMS ONLINE", font=font_clocks)[0],
                dpg.get_text_size("GPS SAT AVAILABLE - 16", font=font_clocks)[0],
                dpg.get_text_size("TELEMETRY RATE - 058.0 Hz", font=font_clocks)[0],
                dpg.get_text_size("DELAY - 320 ms", font=font_clocks)[0],
            ) + 16
            right_gap = 24
            left_spacer = max(8, int((vp_w - lw - center_w - sw - right_gap - 24) / 2))
            dpg.configure_item("hdr_spacer_l", width=left_spacer)
            dpg.configure_item("hdr_spacer_r", width=right_gap)
        except Exception:
            pass
        resize_layout()

    # Update graphs ~every 30 frames (~0.5 s at 60 fps)
    if frame_counter % 2 != 0:
        return
    if system_stopped:
        return

    y1 = roll_append(y1)
    y2 = roll_append(y2)
    y3 = roll_append(y3)
    vel = roll_append(vel)
    acc = roll_append(acc)
    alt = roll_append(alt)
    bat = roll_append(bat, center=12, scale=0.1)
    temp_in = roll_append(temp_in, center=20, scale=0.5)
    temp_out = roll_append(temp_out, center=15, scale=0.5)
    press_in = roll_append(press_in, center=101, scale=0.5)
    press_out = roll_append(press_out, center=100, scale=0.5)
    
    # y1 = y1[-MAX_POINTS:]
    # y2 = y2[-MAX_POINTS:]
    # y3 = y3[-MAX_POINTS:]
    # vel = vel[-MAX_POINTS:]
    # acc = acc[-MAX_POINTS:]
    # alt = alt[-MAX_POINTS:]
    # bat = bat[-MAX_POINTS:]
    # temp_in = temp_in[-MAX_POINTS:]
    # temp_out = temp_out[-MAX_POINTS:]
    # press_in = press_in[-MAX_POINTS:]
    # press_out = press_out[-MAX_POINTS:]
    # x_list = x_list[-MAX_POINTS:]

    

    dpg.set_value(line_x_series_id, [x_list, y1])
    dpg.set_value(line_y_series_id, [x_list, y2])
    dpg.set_value(line_z_series_id, [x_list, y3])
    dpg.set_value(line_vel_series_id, [x_list, vel])
    dpg.set_value(line_acc_series_id, [x_list, acc])
    dpg.set_value(line_alt_series_id, [x_list, alt])
    dpg.set_value(line_batt_series_id, [x_list, bat])
    dpg.set_value(line_temp_in_series_id, [x_list, temp_in])
    dpg.set_value(line_temp_out_series_id, [x_list, temp_out])
    dpg.set_value(line_press_in_series_id, [x_list, press_in])
    dpg.set_value(line_press_out_series_id, [x_list, press_out])

    # last_update = time.time()

# ── Themes ──
# Dark window theme
with dpg.theme() as dark_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (10, 10, 26))
        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (10, 10, 26))
        dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (15, 15, 40))
        dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (20, 20, 55))
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (26, 26, 42))
        dpg.add_theme_color(dpg.mvThemeCol_TableHeaderBg, (10, 10, 26))
        dpg.add_theme_color(dpg.mvThemeCol_TableBorderStrong, (10, 10, 26))
        dpg.add_theme_color(dpg.mvThemeCol_TableBorderLight, (10, 10, 26))
        dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 8, 8)
        dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 6, 4)
        # White-ish text for plot labels, titles, tick marks
        dpg.add_theme_color(dpg.mvThemeCol_Text, (220, 220, 220))

# Button themes
def _make_btn_theme(bg, hover, text_col=(255, 255, 255)):
    with dpg.theme() as t:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, bg)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, hover)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, bg)
            dpg.add_theme_color(dpg.mvThemeCol_Text, text_col)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 6)
    return t

blue_btn     = _make_btn_theme((0, 80, 220),   (60, 140, 255))
yellow_btn   = _make_btn_theme((200, 180, 0),   (255, 230, 80), (0, 0, 0))
green_btn    = _make_btn_theme((0, 140, 0),     (40, 200, 40))
red_btn      = _make_btn_theme((200, 0, 0),     (255, 80, 80))

with dpg.theme() as green_text_theme:
    with dpg.theme_component(dpg.mvText):
        dpg.add_theme_color(dpg.mvThemeCol_Text, GREEN)

with dpg.theme() as red_text_theme:
    with dpg.theme_component(dpg.mvText):
        dpg.add_theme_color(dpg.mvThemeCol_Text, RED)

# ── Main Window ──
with dpg.window(tag="main_window", no_scrollbar=True, no_scroll_with_mouse=True):
    # Top padding
    dpg.add_spacer(height=15)
    
    # ── Header row ──
    with dpg.group(horizontal=True):
        # Logo (left)
        if logo_texture_id:
            dpg.add_image(logo_texture_id)

        # Spacer that grows to push title to center
        dpg.add_spacer(tag="hdr_spacer_l", width=300)

        # Center block: title + clocks + timer
        with dpg.group():
            _mc = dpg.add_text("MISSION CONTROL", color=CYAN)
            dpg.bind_item_font(_mc, font_title)
            with dpg.group(horizontal=True):
                utc_label_id = dpg.add_text("UTC  00:00:00", color=GREY)
                dpg.bind_item_font(utc_label_id, font_clocks)
                dpg.add_spacer(width=30)
                ist_label_id = dpg.add_text("IST  00:00:00", color=GREY)
                dpg.bind_item_font(ist_label_id, font_clocks)
            timer_label_id = dpg.add_text("T+ 00:00:00", color=ORANGE)
            dpg.bind_item_font(timer_label_id, font_clocks)

        # Spacer between center and status
        dpg.add_spacer(tag="hdr_spacer_r", width=24)

        # Status (right)
        with dpg.group():
            status_indicator_id = dpg.add_text("SYSTEMS ONLINE", color=GREEN)
            dpg.bind_item_theme(status_indicator_id, green_text_theme)
            dpg.bind_item_font(status_indicator_id, font_status)
            gps_sat_label_id = dpg.add_text("GPS SAT AVAILABLE - 11", color=GREY)
            telemetry_rate_label_id = dpg.add_text("TELEMETRY RATE - 050.0 Hz", color=GREY)
            delay_label_id = dpg.add_text("DELAY - 180 ms", color=GREY)

    dpg.add_separator()

    # ── 3-column layout via table ──
    with dpg.table(header_row=False, resizable=True, borders_innerV=False,
                   borders_outerV=False, borders_outerH=False, borders_innerH=False):

        dpg.add_table_column(init_width_or_weight=0.18, width_fixed=False)   # left
        dpg.add_table_column(init_width_or_weight=0.70, width_fixed=False)   # center
        dpg.add_table_column(init_width_or_weight=0.12, width_fixed=False)   # right buttons

        with dpg.table_row():
            # ══════ LEFT COLUMN ══════
            with dpg.group():
                with dpg.plot(label="Velocity", tag="plot_vel", width=-1, height=170, no_mouse_pos=True):
                    dpg.add_plot_axis(dpg.mvXAxis, no_tick_labels=True)
                    with dpg.plot_axis(dpg.mvYAxis, tag="vel_axis"):
                        dpg.set_axis_limits("vel_axis", -3, 3)
                        line_vel_series_id = dpg.add_line_series(x_list, vel)

                with dpg.plot(label="Acceleration", tag="plot_acc", width=-1, height=170, no_mouse_pos=True):
                    dpg.add_plot_axis(dpg.mvXAxis, no_tick_labels=True)
                    with dpg.plot_axis(dpg.mvYAxis, tag="acc_axis"):
                        dpg.set_axis_limits("acc_axis", -4, 4)
                        line_acc_series_id = dpg.add_line_series(x_list, acc)

                with dpg.plot(label="Altitude", tag="plot_alt", width=-1, height=170, no_mouse_pos=True):
                    dpg.add_plot_axis(dpg.mvXAxis, no_tick_labels=True)
                    with dpg.plot_axis(dpg.mvYAxis, tag="alt_axis"):
                        dpg.set_axis_limits("alt_axis", -6, 6)
                        line_alt_series_id = dpg.add_line_series(x_list, alt)

            # ══════ CENTER COLUMN ══════
            with dpg.group():
                # X / Y / Z row
                with dpg.table(header_row=False, borders_innerV=False, borders_outerV=False,
                               borders_outerH=False, borders_innerH=False):
                    dpg.add_table_column(init_width_or_weight=1.0, width_fixed=False)
                    dpg.add_table_column(init_width_or_weight=1.0, width_fixed=False)
                    dpg.add_table_column(init_width_or_weight=1.0, width_fixed=False)
                    with dpg.table_row():
                        with dpg.plot(label="X Axis", tag="plot_x", width=-1, height=150, no_mouse_pos=True):
                            dpg.add_plot_axis(dpg.mvXAxis, no_tick_labels=True)
                            with dpg.plot_axis(dpg.mvYAxis, tag="x_axis"):
                                dpg.set_axis_limits("x_axis", -2, 2)
                                line_x_series_id = dpg.add_line_series(x_list, y1)
                        with dpg.plot(label="Y Axis", tag="plot_y", width=-1, height=150, no_mouse_pos=True):
                            dpg.add_plot_axis(dpg.mvXAxis, no_tick_labels=True)
                            with dpg.plot_axis(dpg.mvYAxis, tag="y_axis"):
                                dpg.set_axis_limits("y_axis", -2, 2)
                                line_y_series_id = dpg.add_line_series(x_list, y2)
                        with dpg.plot(label="Z Axis", tag="plot_z", width=-1, height=150, no_mouse_pos=True):
                            dpg.add_plot_axis(dpg.mvXAxis, no_tick_labels=True)
                            with dpg.plot_axis(dpg.mvYAxis, tag="z_axis"):
                                dpg.set_axis_limits("z_axis", -2, 2)
                                line_z_series_id = dpg.add_line_series(x_list, y3)
                with dpg.plot(label="Battery Voltage", tag="plot_batt", width=-1, height=120, no_mouse_pos=True):
                    dpg.add_plot_axis(dpg.mvXAxis, no_tick_labels=True)
                    with dpg.plot_axis(dpg.mvYAxis, tag="batt_axis"):
                        dpg.set_axis_limits("batt_axis", 0, 15)
                        line_batt_series_id = dpg.add_line_series(x_list, bat)

                # Temp row (2 cols)
                with dpg.table(header_row=False, borders_innerV=False, borders_outerV=False,
                               borders_outerH=False, borders_innerH=False):
                    dpg.add_table_column(init_width_or_weight=1.0, width_fixed=False)
                    dpg.add_table_column(init_width_or_weight=1.0, width_fixed=False)
                    with dpg.table_row():
                        with dpg.plot(label="Temp Inside", tag="plot_temp_in", width=-1, height=120, no_mouse_pos=True):
                            dpg.add_plot_axis(dpg.mvXAxis, no_tick_labels=True)
                            with dpg.plot_axis(dpg.mvYAxis, tag="temp_in_axis"):
                                line_temp_in_series_id = dpg.add_line_series(x_list, temp_in)
                        with dpg.plot(label="Temp Outside", tag="plot_temp_out", width=-1, height=120, no_mouse_pos=True):
                            dpg.add_plot_axis(dpg.mvXAxis, no_tick_labels=True)
                            with dpg.plot_axis(dpg.mvYAxis, tag="temp_out_axis"):
                                line_temp_out_series_id = dpg.add_line_series(x_list, temp_out)

                # Pressure row (2 cols)
                with dpg.table(header_row=False, borders_innerV=False, borders_outerV=False,
                               borders_outerH=False, borders_innerH=False):
                    dpg.add_table_column(init_width_or_weight=1.0, width_fixed=False)
                    dpg.add_table_column(init_width_or_weight=1.0, width_fixed=False)
                    with dpg.table_row():
                        with dpg.plot(label="Pressure Inside", tag="plot_press_in", width=-1, height=120, no_mouse_pos=True):
                            dpg.add_plot_axis(dpg.mvXAxis, no_tick_labels=True)
                            with dpg.plot_axis(dpg.mvYAxis, tag="press_in_axis"):
                                line_press_in_series_id = dpg.add_line_series(x_list, press_in)
                        with dpg.plot(label="Pressure Outside", tag="plot_press_out", width=-1, height=120, no_mouse_pos=True):
                            dpg.add_plot_axis(dpg.mvXAxis, no_tick_labels=True)
                            with dpg.plot_axis(dpg.mvYAxis, tag="press_out_axis"):
                                line_press_out_series_id = dpg.add_line_series(x_list, press_out)

            # ══════ RIGHT COLUMN (buttons) ══════
            with dpg.group():
                dpg.add_button(tag="btn_tank", label="Fuel Tank\nOperations", width=-1, height=120, callback=tank_command)
                dpg.bind_item_theme("btn_tank", blue_btn)
                dpg.bind_item_font("btn_tank", font_button)

                dpg.add_button(tag="btn_vehicle", label="Rocket\nOperations", width=-1, height=120, callback=vehicle_command)
                dpg.bind_item_theme("btn_vehicle", yellow_btn)
                dpg.bind_item_font("btn_vehicle", font_button)

                dpg.add_button(tag="btn_engine", label="Engine\nControl", width=-1, height=120, callback=engine_command)
                dpg.bind_item_theme("btn_engine", green_btn)
                dpg.bind_item_font("btn_engine", font_button)

                dpg.add_button(tag="btn_stop", label="STOP", width=-1, height=120, callback=stop_command)
                dpg.bind_item_theme("btn_stop", red_btn)
                dpg.bind_item_font("btn_stop", font_button)

# ── Apply global dark theme ──
dpg.bind_theme(dark_theme)
dpg.bind_font(font_body)

# ── Viewport setup ──
dpg.create_viewport(title="Mission Control", width=1200, height=800)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main_window", True)

# Main loop
if __name__ == "__main__":
    while dpg.is_dearpygui_running():
        update_callback()
        dpg.render_dearpygui_frame()
    dpg.destroy_context()
    