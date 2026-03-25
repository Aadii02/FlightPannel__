import dearpygui.dearpygui as dpg
from ui_assets_dpg import bind_button_theme, bind_font, ensure_ui_fonts, ensure_window_theme

LIGHT_TEXT = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

_engine_win_id = None


def _set_status_lines(status_items, updates):
    for key, value in updates.items():
        if key in status_items:
            dpg.set_value(status_items[key], f"{key}: {value}")

def open_engine_operations():
    global _engine_win_id
    if _engine_win_id and dpg.does_item_exist(_engine_win_id):
        dpg.focus_item(_engine_win_id)
        return

    ensure_ui_fonts()
    window_theme = ensure_window_theme()

    def _on_close():
        global _engine_win_id
        if _engine_win_id and dpg.does_item_exist(_engine_win_id):
            dpg.delete_item(_engine_win_id)
        _engine_win_id = None

    with dpg.window(label="Engine Control Panel", width=900, height=600,
                    no_scrollbar=True, no_scroll_with_mouse=True,
                    on_close=_on_close) as win:
        _engine_win_id = win
        dpg.bind_item_theme(win, window_theme)
        title = dpg.add_text("Engine Control Panel", color=LIGHT_TEXT)
        bind_font(title, "title")
        status_id = dpg.add_text("Engine System Standby", color=YELLOW)
        bind_font(status_id, "status")
        status_items = {}

        def set_headline(value):
            dpg.set_value(status_id, value)

        def pre_ignition_check():
            set_headline("Pre-Ignition Check Running")
            _set_status_lines(status_items, {
                "Engine State": "Pre-Ignition Check",
                "System Health": "Diagnostics Running",
            })

        def ignition_on():
            set_headline("Ignition ON")
            _set_status_lines(status_items, {
                "Engine State": "Ignited",
                "RPM": "1200",
                "Pressure": "Nominal",
            })

        def ignition_off():
            set_headline("Ignition OFF")
            _set_status_lines(status_items, {
                "Engine State": "Standby",
                "RPM": "0",
                "Throttle": "0%",
            })

        def increase_throttle():
            set_headline("Throttle Increased")
            _set_status_lines(status_items, {
                "Throttle": "68%",
                "RPM": "4200",
                "Temperature": "41°C",
            })

        def decrease_throttle():
            set_headline("Throttle Decreased")
            _set_status_lines(status_items, {
                "Throttle": "32%",
                "RPM": "2100",
                "Temperature": "33°C",
            })

        def shutdown_engine():
            set_headline("ENGINE SHUTDOWN")
            _set_status_lines(status_items, {
                "Engine State": "Shutdown",
                "RPM": "0",
                "Throttle": "0%",
                "Pressure": "Safe",
                "System Health": "Offline",
            })

        with dpg.table(header_row=False, borders_innerV=False, borders_outerV=False,
                       borders_outerH=False, borders_innerH=False):
            dpg.add_table_column(init_width_or_weight=0.6, width_fixed=False)
            dpg.add_table_column(init_width_or_weight=0.4, width_fixed=False)
            with dpg.table_row():
                # Left - monitoring
                with dpg.group():
                    header = dpg.add_text("Engine Monitoring", color=LIGHT_TEXT)
                    bind_font(header, "status")
                    with dpg.table(header_row=False, borders_innerV=False, borders_outerV=False,
                                   borders_outerH=False, borders_innerH=False):
                        dpg.add_table_column(init_width_or_weight=1.0, width_fixed=False)
                        dpg.add_table_column(init_width_or_weight=1.0, width_fixed=False)
                        dpg.add_table_column(init_width_or_weight=1.0, width_fixed=False)
                        with dpg.table_row():
                            btn = dpg.add_button(label="Diagnostics", width=-1)
                            bind_button_theme(btn, "primary")
                            bind_font(btn, "button")
                            btn = dpg.add_button(label="Performance", width=-1)
                            bind_button_theme(btn, "accent")
                            bind_font(btn, "button")
                            btn = dpg.add_button(label="Temperature", width=-1)
                            bind_button_theme(btn, "warning")
                            bind_font(btn, "button")
                    dpg.add_separator()
                    with dpg.child_window(border=True, width=-1, height=220):
                        header = dpg.add_text("Engine Status", color=LIGHT_TEXT)
                        bind_font(header, "status")
                        dpg.add_separator()
                        for key, value in [
                            ("Engine State", "Standby"),
                            ("RPM", "0"),
                            ("Throttle", "0%"),
                            ("Temperature", "25°C"),
                            ("Pressure", "Normal"),
                            ("System Health", "Excellent"),
                        ]:
                            item = dpg.add_text(f"{key}: {value}", color=LIGHT_TEXT)
                            status_items[key] = item
                            bind_font(item, "body")
                # Right - controls
                with dpg.group():
                    header = dpg.add_text("Engine Controls", color=LIGHT_TEXT)
                    bind_font(header, "status")
                    btn = dpg.add_button(label="Pre-Ignition Check", width=-1, height=36,
                                         callback=pre_ignition_check)
                    bind_button_theme(btn, "warning")
                    bind_font(btn, "button")
                    btn = dpg.add_button(label="Ignition ON", width=-1, height=36,
                                         callback=ignition_on)
                    bind_button_theme(btn, "success")
                    bind_font(btn, "button")
                    btn = dpg.add_button(label="Ignition OFF", width=-1, height=36,
                                         callback=ignition_off)
                    bind_button_theme(btn, "danger")
                    bind_font(btn, "button")
                    btn = dpg.add_button(label="Increase Throttle", width=-1, height=36,
                                         callback=increase_throttle)
                    bind_button_theme(btn, "primary")
                    bind_font(btn, "button")
                    btn = dpg.add_button(label="Decrease Throttle", width=-1, height=36,
                                         callback=decrease_throttle)
                    bind_button_theme(btn, "muted")
                    bind_font(btn, "button")
                    btn = dpg.add_button(label="SHUTDOWN", width=-1, height=50,
                                         callback=shutdown_engine)
                    bind_button_theme(btn, "danger")
                    bind_font(btn, "button")

if __name__ == "__main__":
    dpg.create_context()
    dpg.create_viewport(title="Engine Operations", width=800, height=600)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    open_engine_operations()
    while dpg.is_dearpygui_running():
        dpg.render_dearpygui_frame()
    dpg.destroy_context()
