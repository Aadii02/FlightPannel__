import dearpygui.dearpygui as dpg
from ui_assets_dpg import bind_button_theme, bind_font, ensure_ui_fonts, ensure_window_theme

LIGHT_TEXT = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

_vehicle_win_id = None


def _set_status_lines(status_items, updates):
    for key, value in updates.items():
        if key in status_items:
            dpg.set_value(status_items[key], f"{key}: {value}")

def open_vehicle_operations():
    global _vehicle_win_id
    if _vehicle_win_id and dpg.does_item_exist(_vehicle_win_id):
        dpg.focus_item(_vehicle_win_id)
        return

    ensure_ui_fonts()
    window_theme = ensure_window_theme()

    def _on_close():
        global _vehicle_win_id
        if _vehicle_win_id and dpg.does_item_exist(_vehicle_win_id):
            dpg.delete_item(_vehicle_win_id)
        _vehicle_win_id = None

    with dpg.window(label="Rocket Operations Control", width=820, height=520,
                    no_scrollbar=True, no_scroll_with_mouse=True,
                    on_close=_on_close) as win:
        _vehicle_win_id = win
        dpg.bind_item_theme(win, window_theme)
        title = dpg.add_text("Rocket Operations Control Panel", color=LIGHT_TEXT)
        bind_font(title, "title")
        status_items = {}

        def navigation_lights_action():
            _set_status_lines(status_items, {
                "Avionics": "Online",
                "Navigation": "Guidance Lights Active",
            })

        def warning_lights_action():
            _set_status_lines(status_items, {
                "Launch Sequence": "Warning Broadcast Active",
                "Navigation": "Caution Mode",
            })

        def beacon_action():
            _set_status_lines(status_items, {
                "Navigation": "Beacon Locked",
                "Avionics": "Tracking Enabled",
            })

        def emergency_shutdown_action():
            _set_status_lines(status_items, {
                "Engine Status": "Shutdown",
                "Fuel Level": "Feed Closed",
                "Oxidizer Level": "Feed Closed",
                "Launch Sequence": "Aborted",
            })

        with dpg.table(header_row=False, borders_innerV=False, borders_outerV=False,
                       borders_outerH=False, borders_innerH=False):
            dpg.add_table_column(init_width_or_weight=0.52, width_fixed=False)
            dpg.add_table_column(init_width_or_weight=0.48, width_fixed=False)
            with dpg.table_row():
                with dpg.group():
                    header = dpg.add_text("Rocket Systems", color=LIGHT_TEXT)
                    bind_font(header, "status")
                    with dpg.table(header_row=False, borders_innerV=False, borders_outerV=False,
                                   borders_outerH=False, borders_innerH=False):
                        dpg.add_table_column(init_width_or_weight=1.0, width_fixed=False)
                        dpg.add_table_column(init_width_or_weight=1.0, width_fixed=False)
                        dpg.add_table_column(init_width_or_weight=1.0, width_fixed=False)
                        with dpg.table_row():
                            btn = dpg.add_button(label="Navigation Lights", width=-1, callback=navigation_lights_action)
                            bind_button_theme(btn, "warning")
                            bind_font(btn, "button")
                            btn = dpg.add_button(label="Warning Lights", width=-1, callback=warning_lights_action)
                            bind_button_theme(btn, "accent")
                            bind_font(btn, "button")
                            btn = dpg.add_button(label="Beacon", width=-1, callback=beacon_action)
                            bind_button_theme(btn, "danger")
                            bind_font(btn, "button")
                    dpg.add_separator()
                    with dpg.child_window(border=True, width=-1, height=220):
                        header = dpg.add_text("Rocket Status", color=LIGHT_TEXT)
                        bind_font(header, "status")
                        dpg.add_separator()
                        for key, value in [
                            ("Engine Status", "Ready"),
                            ("Fuel Level", "95%"),
                            ("Oxidizer Level", "92%"),
                            ("Avionics", "Online"),
                            ("Navigation", "Locked"),
                            ("Launch Sequence", "Standby"),
                        ]:
                            item = dpg.add_text(f"{key}: {value}", color=LIGHT_TEXT)
                            status_items[key] = item
                            bind_font(item, "body")
                with dpg.group():
                    header = dpg.add_text("Emergency Controls", color=LIGHT_TEXT)
                    bind_font(header, "status")
                    btn = dpg.add_button(label="EMERGENCY SHUTDOWN", width=-1, height=60, callback=emergency_shutdown_action)
                    bind_button_theme(btn, "danger")
                    bind_font(btn, "button")

if __name__ == "__main__":
    dpg.create_context()
    dpg.create_viewport(title="Rocket Operations", width=800, height=600)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    open_vehicle_operations()
    while dpg.is_dearpygui_running():
        dpg.render_dearpygui_frame()
    dpg.destroy_context()
