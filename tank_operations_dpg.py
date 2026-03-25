import dearpygui.dearpygui as dpg
import numpy as np
from ui_assets_dpg import bind_button_theme, bind_font, ensure_ui_fonts, ensure_window_theme, GREY

# Colors
LIGHT_TEXT = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

_pressure_win_id = None
_fuel_level_win_id = None
_tank_ops_win_id = None


def _set_status_lines(status_items, updates):
    for key, value in updates.items():
        if key in status_items:
            dpg.set_value(status_items[key], f"{key}: {value}")

def open_pressure_test():
    
    global _pressure_win_id
    if _pressure_win_id and dpg.does_item_exist(_pressure_win_id):
        dpg.focus_item(_pressure_win_id)
        return

    ensure_ui_fonts()
    window_theme = ensure_window_theme()

    time_data = np.linspace(0, 10, 50).tolist()
    p_oxygen = (1.0 + 0.2 * np.sin(np.array(time_data)) + 0.1 * np.random.randn(50)).tolist()
    p_fuel   = (1.0 + 0.2 * np.sin(np.array(time_data)) + 0.1 * np.random.randn(50)).tolist()

    def _on_close():
        global _pressure_win_id
        if _pressure_win_id and dpg.does_item_exist(_pressure_win_id):
            dpg.delete_item(_pressure_win_id)
        _pressure_win_id = None

    with dpg.window(label="Pressure Test Control", width=900, height=460,
                    no_scrollbar=True, no_scroll_with_mouse=True,
                    on_close=_on_close) as win:
        _pressure_win_id = win
        dpg.bind_item_theme(win, window_theme)
        title = dpg.add_text("Pressure Tests", color=LIGHT_TEXT)
        bind_font(title, "title")
        with dpg.table(header_row=False, borders_innerV=False, borders_outerV=False,
                       borders_outerH=False, borders_innerH=False):
            dpg.add_table_column(init_width_or_weight=1.0, width_fixed=False)
            dpg.add_table_column(init_width_or_weight=1.0, width_fixed=False)
            with dpg.table_row():
                start_btn = dpg.add_button(label="Start Pressure Test", width=-1, height=36)
                stop_btn = dpg.add_button(label="Stop Test", width=-1, height=36)
                bind_button_theme(start_btn, "success")
                bind_button_theme(stop_btn, "danger")
                bind_font(start_btn, "button")
                bind_font(stop_btn, "button")
        label = dpg.add_text("Test Results:", color=LIGHT_TEXT)
        bind_font(label, "status")
        results = dpg.add_text(
            "- Current Pressure: 1.2 bar\n- Test Status: Ready\n- Last Test: Passed\n- Safety Check: OK",
            color=GREY,
        )
        bind_font(results, "body")
        with dpg.table(header_row=False, borders_innerV=False, borders_outerV=False,
                       borders_outerH=False, borders_innerH=False):
            dpg.add_table_column(init_width_or_weight=1.0, width_fixed=False)
            dpg.add_table_column(init_width_or_weight=1.0, width_fixed=False)
            with dpg.table_row():
                with dpg.plot(label="Oxygen Tank Pressure", width=-1, height=250):
                    dpg.add_plot_axis(dpg.mvXAxis)
                    with dpg.plot_axis(dpg.mvYAxis):
                        dpg.add_line_series(time_data, p_oxygen)
                with dpg.plot(label="Fuel Tank Pressure", width=-1, height=250):
                    dpg.add_plot_axis(dpg.mvXAxis)
                    with dpg.plot_axis(dpg.mvYAxis):
                        dpg.add_line_series(time_data, p_fuel)

def open_fuel_level():
    global _fuel_level_win_id
    if _fuel_level_win_id and dpg.does_item_exist(_fuel_level_win_id):
        dpg.focus_item(_fuel_level_win_id)
        return

    ensure_ui_fonts()
    window_theme = ensure_window_theme()

    oxygen_state = {
        "percent": 92,
        "current": 460,
        "pressure": 200,
        "temp": 20,
        "draining": False,
    }
    fuel_state = {
        "percent": 85,
        "current": 850,
        "temp": -183,
        "draining": False,
    }

    def _on_close():
        global _fuel_level_win_id
        oxygen_state["draining"] = False
        fuel_state["draining"] = False
        if _fuel_level_win_id and dpg.does_item_exist(_fuel_level_win_id):
            dpg.delete_item(_fuel_level_win_id)
        _fuel_level_win_id = None

    with dpg.window(label="Fuel Level Monitoring", width=760, height=430,
                    no_scrollbar=True, no_scroll_with_mouse=True,
                    on_close=_on_close) as win:
        _fuel_level_win_id = win
        dpg.bind_item_theme(win, window_theme)
        title = dpg.add_text("Fuel & Oxygen Tank Level Monitoring", color=LIGHT_TEXT)
        bind_font(title, "title")
        with dpg.table(header_row=False, borders_innerV=False, borders_outerV=False,
                       borders_outerH=False, borders_innerH=False):
            dpg.add_table_column(init_width_or_weight=1.0, width_fixed=False)
            dpg.add_table_column(init_width_or_weight=1.0, width_fixed=False)
            with dpg.table_row():
                with dpg.group():
                    hdr = dpg.add_text("OXYGEN TANK", color=CYAN)
                    oxygen_level = dpg.add_text("OXYGEN LEVEL\n92%", color=CYAN)
                    oxygen_desc = dpg.add_text(
                        "Tank Capacity: 500L\nCurrent: 460L\nPressure: 200 bar\nTemperature: 20°C",
                        color=LIGHT_TEXT,
                    )
                    bind_font(hdr, "status")
                    bind_font(oxygen_level, "status")
                    bind_font(oxygen_desc, "body")

                    def refresh_oxygen_ui():
                        dpg.set_value(oxygen_level, f"OXYGEN LEVEL\n{oxygen_state['percent']}%")
                        dpg.set_value(
                            oxygen_desc,
                            "Tank Capacity: 500L\n"
                            f"Current: {oxygen_state['current']}L\n"
                            f"Pressure: {oxygen_state['pressure']} bar\n"
                            f"Temperature: {oxygen_state['temp']}°C",
                        )

                    def oxygen_drain_tick():
                        if _fuel_level_win_id is None or not oxygen_state["draining"]:
                            return
                        oxygen_state["percent"] = max(0, oxygen_state["percent"] - 1)
                        oxygen_state["current"] = max(0, oxygen_state["current"] - 5)
                        oxygen_state["pressure"] = max(120, oxygen_state["pressure"] - 1)
                        oxygen_state["temp"] = max(15, oxygen_state["temp"] - 1)
                        refresh_oxygen_ui()
                        if oxygen_state["percent"] > 0 and oxygen_state["draining"]:
                            dpg.set_frame_callback(dpg.get_frame_count() + 15, oxygen_drain_tick)
                        else:
                            oxygen_state["draining"] = False

                    def refill_oxygen():
                        oxygen_state["percent"] = 100
                        oxygen_state["current"] = 500
                        oxygen_state["pressure"] = 205
                        oxygen_state["temp"] = 20
                        refresh_oxygen_ui()

                    def start_drain_oxygen():
                        if oxygen_state["draining"]:
                            return
                        oxygen_state["draining"] = True
                        oxygen_drain_tick()

                    def stop_drain_oxygen():
                        oxygen_state["draining"] = False

                    with dpg.group(horizontal=True):
                        refill_o2 = dpg.add_button(label="Refill", width=115, callback=refill_oxygen)
                        drain_start_o2 = dpg.add_button(label="Drain Start", width=115, callback=start_drain_oxygen)
                        drain_stop_o2 = dpg.add_button(label="Drain Stop", width=115, callback=stop_drain_oxygen)
                        bind_button_theme(refill_o2, "primary")
                        bind_button_theme(drain_start_o2, "danger")
                        bind_button_theme(drain_stop_o2, "muted")
                        bind_font(refill_o2, "button")
                        bind_font(drain_start_o2, "button")
                        bind_font(drain_stop_o2, "button")
                with dpg.group():
                    hdr = dpg.add_text("FUEL TANK", color=YELLOW)
                    fuel_level = dpg.add_text("FUEL LEVEL\n85%", color=YELLOW)
                    fuel_desc = dpg.add_text(
                        "Tank Capacity: 1000L\nCurrent: 850L\nTemperature: -183°C\nFuel Type: RP-1",
                        color=LIGHT_TEXT,
                    )
                    bind_font(hdr, "status")
                    bind_font(fuel_level, "status")
                    bind_font(fuel_desc, "body")

                    def refresh_fuel_ui():
                        dpg.set_value(fuel_level, f"FUEL LEVEL\n{fuel_state['percent']}%")
                        dpg.set_value(
                            fuel_desc,
                            "Tank Capacity: 1000L\n"
                            f"Current: {fuel_state['current']}L\n"
                            f"Temperature: {fuel_state['temp']}°C\n"
                            "Fuel Type: RP-1",
                        )

                    def fuel_drain_tick():
                        if _fuel_level_win_id is None or not fuel_state["draining"]:
                            return
                        fuel_state["percent"] = max(0, fuel_state["percent"] - 1)
                        fuel_state["current"] = max(0, fuel_state["current"] - 10)
                        fuel_state["temp"] = min(-176, fuel_state["temp"] + 1)
                        refresh_fuel_ui()
                        if fuel_state["percent"] > 0 and fuel_state["draining"]:
                            dpg.set_frame_callback(dpg.get_frame_count() + 15, fuel_drain_tick)
                        else:
                            fuel_state["draining"] = False

                    def refill_fuel_tank():
                        fuel_state["percent"] = 100
                        fuel_state["current"] = 1000
                        fuel_state["temp"] = -183
                        refresh_fuel_ui()

                    def start_drain_fuel_tank():
                        if fuel_state["draining"]:
                            return
                        fuel_state["draining"] = True
                        fuel_drain_tick()

                    def stop_drain_fuel_tank():
                        fuel_state["draining"] = False

                    with dpg.group(horizontal=True):
                        refill_fuel = dpg.add_button(label="Refill", width=115, callback=refill_fuel_tank)
                        drain_start_fuel = dpg.add_button(label="Drain Start", width=115, callback=start_drain_fuel_tank)
                        drain_stop_fuel = dpg.add_button(label="Drain Stop", width=115, callback=stop_drain_fuel_tank)
                        bind_button_theme(refill_fuel, "warning")
                        bind_button_theme(drain_start_fuel, "danger")
                        bind_button_theme(drain_stop_fuel, "muted")
                        bind_font(refill_fuel, "button")
                        bind_font(drain_start_fuel, "button")
                        bind_font(drain_stop_fuel, "button")

def open_tank_operations():
    global _tank_ops_win_id
    if _tank_ops_win_id and dpg.does_item_exist(_tank_ops_win_id):
        dpg.focus_item(_tank_ops_win_id)
        return

    ensure_ui_fonts()
    window_theme = ensure_window_theme()

    def _on_close():
        global _tank_ops_win_id
        if _tank_ops_win_id and dpg.does_item_exist(_tank_ops_win_id):
            dpg.delete_item(_tank_ops_win_id)
        _tank_ops_win_id = None

    with dpg.window(label="Fuel Tank Operations Control", width=900, height=600,
                    no_scrollbar=True, no_scroll_with_mouse=True,
                    on_close=_on_close) as win:
        _tank_ops_win_id = win
        dpg.bind_item_theme(win, window_theme)
        title = dpg.add_text("Fuel Tank Operations Control Panel", color=LIGHT_TEXT)
        bind_font(title, "title")
        status_id = dpg.add_text("Fuel Tank System Online", color=YELLOW)
        bind_font(status_id, "status")
        status_items = {}

        def set_headline(value):
            dpg.set_value(status_id, value)

        def check_level_action():
            open_fuel_level()
            set_headline("Fuel Levels Verified")
            _set_status_lines(status_items, {
                "Fuel Level": "85% Verified",
                "System Health": "Nominal",
            })

        def pressure_test_action():
            open_pressure_test()
            set_headline("Pressure Test Window Opened")
            _set_status_lines(status_items, {
                "Pressure": "Pressure Test Armed",
                "System Health": "Monitoring",
            })

        def quality_check_action():
            set_headline("Fuel Quality Check Complete")
            _set_status_lines(status_items, {
                "Temperature": "25°C Stable",
                "System Health": "Quality Check Passed",
            })

        def oxygen_pump_start():
            set_headline("Oxygen Pump Started")
            _set_status_lines(status_items, {
                "Pump Status": "Oxygen Pump Running",
                "Pressure": "Rising",
            })

        def oxygen_pump_stop():
            set_headline("Oxygen Pump Stopped")
            _set_status_lines(status_items, {
                "Pump Status": "Oxygen Pump Idle",
                "Pressure": "Stabilized",
            })

        def fuel_pump_start():
            set_headline("Fuel Pump Started")
            _set_status_lines(status_items, {
                "Pump Status": "Fuel Pump Running",
                "Fuel Level": "Transfer Active",
            })

        def fuel_pump_stop():
            set_headline("Fuel Pump Stopped")
            _set_status_lines(status_items, {
                "Pump Status": "Fuel Pump Idle",
                "Fuel Level": "85% Stable",
            })

        def open_valve_action():
            set_headline("Fuel Valve Opened")
            _set_status_lines(status_items, {
                "Valve Status": "Open",
                "Pressure": "Flow Enabled",
            })

        def close_valve_action():
            set_headline("Fuel Valve Closed")
            _set_status_lines(status_items, {
                "Valve Status": "Closed",
                "Pressure": "Sealed",
            })

        def emergency_action():
            set_headline("EMERGENCY SHUTOFF ACTIVATED")
            _set_status_lines(status_items, {
                "Pump Status": "Offline",
                "Valve Status": "Emergency Lock",
                "Pressure": "Dumped to Safe Limit",
                "System Health": "Critical Stop",
            })

        with dpg.table(header_row=False, borders_innerV=False, borders_outerV=False,
                       borders_outerH=False, borders_innerH=False):
            dpg.add_table_column(init_width_or_weight=0.6, width_fixed=False)
            dpg.add_table_column(init_width_or_weight=0.4, width_fixed=False)
            with dpg.table_row():
                # Left - monitoring
                with dpg.group():
                    header = dpg.add_text("Fuel Monitoring", color=LIGHT_TEXT)
                    bind_font(header, "status")
                    with dpg.table(header_row=False, borders_innerV=False, borders_outerV=False,
                                   borders_outerH=False, borders_innerH=False):
                        dpg.add_table_column(init_width_or_weight=1.0, width_fixed=False)
                        dpg.add_table_column(init_width_or_weight=1.0, width_fixed=False)
                        dpg.add_table_column(init_width_or_weight=1.0, width_fixed=False)
                        with dpg.table_row():
                            btn = dpg.add_button(label="Check Level", width=-1, callback=check_level_action)
                            bind_button_theme(btn, "primary")
                            bind_font(btn, "button")
                            btn = dpg.add_button(label="Pressure Test", width=-1, callback=pressure_test_action)
                            bind_button_theme(btn, "accent")
                            bind_font(btn, "button")
                            btn = dpg.add_button(label="Quality Check", width=-1, callback=quality_check_action)
                            bind_button_theme(btn, "success")
                            bind_font(btn, "button")
                # Right - controls
                with dpg.group():
                    header = dpg.add_text("Fuel System Controls", color=LIGHT_TEXT)
                    bind_font(header, "status")
                    btn = dpg.add_button(label="Start Pump (Oxygen)", width=-1,
                                         callback=oxygen_pump_start)
                    bind_button_theme(btn, "success")
                    bind_font(btn, "button")
                    btn = dpg.add_button(label="Stop Pump (Oxygen)", width=-1,
                                         callback=oxygen_pump_stop)
                    bind_button_theme(btn, "muted")
                    bind_font(btn, "button")
                    btn = dpg.add_button(label="Start Pump (Fuel)", width=-1,
                                         callback=fuel_pump_start)
                    bind_button_theme(btn, "warning")
                    bind_font(btn, "button")
                    btn = dpg.add_button(label="Stop Pump (Fuel)", width=-1,
                                         callback=fuel_pump_stop)
                    bind_button_theme(btn, "danger")
                    bind_font(btn, "button")
                    btn = dpg.add_button(label="Open Valve", width=-1,
                                         callback=open_valve_action)
                    bind_button_theme(btn, "primary")
                    bind_font(btn, "button")
                    btn = dpg.add_button(label="Close Valve", width=-1,
                                         callback=close_valve_action)
                    bind_button_theme(btn, "accent")
                    bind_font(btn, "button")
                    btn = dpg.add_button(label="EMERGENCY SHUTOFF", width=-1, height=44,
                                         callback=emergency_action)
                    bind_button_theme(btn, "danger")
                    bind_font(btn, "button")

        dpg.add_separator()
        with dpg.child_window(border=True, width=-1, autosize_y=True):
            status_header = dpg.add_text("System Status", color=LIGHT_TEXT)
            bind_font(status_header, "status")
            dpg.add_separator()
            for key, value in [
                ("Fuel Level", "85%"),
                ("Pressure", "Normal"),
                ("Temperature", "25°C"),
                ("Pump Status", "Ready"),
                ("Valve Status", "Closed"),
                ("System Health", "Good"),
            ]:
                item = dpg.add_text(f"{key}: {value}", color=LIGHT_TEXT)
                status_items[key] = item
                bind_font(item, "body")

if __name__ == "__main__":
    dpg.create_context()
    dpg.create_viewport(title="Tank Operations", width=800, height=600)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    open_tank_operations()
    while dpg.is_dearpygui_running():
        dpg.render_dearpygui_frame()
    dpg.destroy_context()
