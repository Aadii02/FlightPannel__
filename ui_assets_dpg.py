import dearpygui.dearpygui as dpg

LIGHT_TEXT = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (170, 170, 170)

_font_body = None
_font_title = None
_font_status = None
_font_button = None
_font_clocks = None
_window_theme = None
_button_themes = {}


def ensure_ui_fonts():
    global _font_body, _font_title, _font_status, _font_button, _font_clocks

    if _font_body and dpg.does_item_exist(_font_body):
        return {
            "body": _font_body,
            "title": _font_title,
            "status": _font_status,
            "button": _font_button,
            "clocks": _font_clocks,
        }

    with dpg.font_registry():
        _font_body = dpg.add_font(r"C:\Windows\Fonts\seguisb.ttf", 16)
        _font_title = dpg.add_font(r"C:\Windows\Fonts\arialbd.ttf", 28)
        _font_status = dpg.add_font(r"C:\Windows\Fonts\arialbd.ttf", 18)
        _font_button = dpg.add_font(r"C:\Windows\Fonts\arialbd.ttf", 16)
        _font_clocks = dpg.add_font(r"C:\Windows\Fonts\consolab.ttf", 18)

    return {
        "body": _font_body,
        "title": _font_title,
        "status": _font_status,
        "button": _font_button,
        "clocks": _font_clocks,
    }


def ensure_window_theme():
    global _window_theme

    if _window_theme and dpg.does_item_exist(_window_theme):
        return _window_theme

    with dpg.theme() as _window_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (10, 10, 26))
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (10, 10, 26))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (15, 15, 40))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (20, 20, 55))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (26, 26, 42))
            dpg.add_theme_color(dpg.mvThemeCol_TableHeaderBg, (10, 10, 26))
            dpg.add_theme_color(dpg.mvThemeCol_TableBorderStrong, (10, 10, 26))
            dpg.add_theme_color(dpg.mvThemeCol_TableBorderLight, (10, 10, 26))
            dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 12, 12)
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 8, 6)
    return _window_theme


def ensure_button_theme(name, button_color, hover_color, active_color=None, text_color=LIGHT_TEXT):
    global _button_themes

    existing = _button_themes.get(name)
    if existing and dpg.does_item_exist(existing):
        return existing

    if active_color is None:
        active_color = hover_color

    with dpg.theme() as theme:
        with dpg.theme_component(dpg.mvButton):
            dpg.add_theme_color(dpg.mvThemeCol_Button, button_color)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, hover_color)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, active_color)
            dpg.add_theme_color(dpg.mvThemeCol_Text, text_color)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 6)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 10, 8)

    _button_themes[name] = theme
    return theme


def bind_button_theme(item, theme_name):
    theme_map = {
        "primary": ensure_button_theme("primary", (40, 90, 210), (70, 140, 255), (25, 70, 170)),
        "warning": ensure_button_theme("warning", (214, 170, 20), (255, 210, 70), (184, 138, 10), (20, 20, 20)),
        "success": ensure_button_theme("success", (25, 145, 70), (45, 190, 95), (18, 120, 58)),
        "danger": ensure_button_theme("danger", (180, 40, 40), (225, 70, 70), (145, 28, 28)),
        "accent": ensure_button_theme("accent", (120, 60, 185), (155, 95, 225), (96, 45, 152)),
        "muted": ensure_button_theme("muted", (70, 80, 110), (95, 108, 146), (58, 66, 92)),
    }
    dpg.bind_item_theme(item, theme_map[theme_name])


def bind_font(item, font_key):
    fonts = ensure_ui_fonts()
    dpg.bind_item_font(item, fonts[font_key])
