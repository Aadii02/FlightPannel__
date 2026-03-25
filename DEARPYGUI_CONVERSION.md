# Mission Control Dashboard - DearPyGui Conversion

This directory contains both the original **Tkinter** version and a fully converted **DearPyGui** version of the Mission Control Dashboard.

## File Structure

### Tkinter Version (Original)
- `main.py` - Main dashboard with live graphs and operation buttons
- `tank_operations.py` - Fuel tank operations control panel
- `vehicle_operations.py` - Rocket operations control panel
- `engine_operations.py` - Engine control panel
- `requirements.txt` - Tkinter dependencies
- `.venv/` - Python virtual environment

### DearPyGui Version (Converted)
- `main_dpg.py` - Main dashboard (DearPyGui)
- `tank_operations_dpg.py` - Fuel tank operations (DearPyGui)
- `vehicle_operations_dpg.py` - Rocket operations (DearPyGui)
- `engine_operations_dpg.py` - Engine control (DearPyGui)
- `requirements_dpg.txt` - DearPyGui dependencies

## Conversion Summary

### ✅ Preserved Features
- ✔ All button functionality and callbacks
- ✔ Live graph updates with data streaming
- ✔ Mission timer and dual clocks (UTC/IST)
- ✔ Emergency STOP button with system freeze/resume
- ✔ All operation windows (Tank, Rocket, Engine)
- ✔ Color scheme and visual hierarchy
- ✔ Dynamic data generation (velocity, acceleration, battery, temperature, pressure)
- ✔ All variable names and function names

### ⚠️ Framework Differences (DearPyGui vs Tkinter)
DearPyGui has a fundamentally different architecture than Tkinter:

1. **Single Context Model**: DearPyGui uses a single context for all UI elements. All windows must be created before the main render loop.
   - Tkinter: Creates separate Toplevel() windows independently
   - DearPyGui: All windows in one context, shown/hidden via dpg.show/hide_item()

2. **Rendering Loop**: DearPyGui requires a continuous render loop with callbacks.
   - Tkinter: Uses event-driven `after()` polling
   - DearPyGui: Uses `set_frame_callback()` for continuous updates

3. **Plotting**: DearPyGui uses native `add_plot()` with `add_line_series()`
   - Tkinter: Embedded matplotlib figures
   - DearPyGui: Native plotting (different visual style, no matplotlib)

4. **Value Management**: 
   - Tkinter: StringVar, IntVar, etc.
   - DearPyGui: Value registry (dpg.set_value/get_value)

5. **Layout System**:
   - Tkinter: Grid, pack, place geometry managers
   - DearPyGui: Groups, drawlayers, hierarchical containers

## Running the Application

### Tkinter Version (Original)
```bash
python main.py
```

### DearPyGui Version
First, install dependencies:
```bash
pip install -r requirements_dpg.txt
```

Then run:
```bash
python main_dpg.py
```

## Key Conversion Details

### Matplotlib → DearPyGui Plotting
- **Original**: FigureCanvasTkAgg embedding matplotlib figures
- **Converted**: Native DearPyGui `add_plot()` with `add_line_series()`
- Multiple plots arranged in groups/layouts matching original 3-column design

### Canvas Text Rotation
- **Original**: tk.Canvas.create_text() with angle=90 for vertical text
- **Converted**: DearPyGui buttons with multi-line labels (limitations: angle rotation not supported)

### Tkinter Toplevel Windows
- **Original**: Independent Toplevel() windows for Tank, Rocket, Engine operations
- **Converted**: Windows created in same context and managed via dpg.window()
- All operation windows are initialized at startup within main render loop

### Continuous Updates
- **Original**: `root.after(500, update)` polling loop
- **Converted**: `dpg.set_frame_callback(0, update_callback)` in main render loop

## Functionality Mapping

| Feature | Tkinter | DearPyGui |
|---------|---------|-----------|
| Main Dashboard | main.py | main_dpg.py |
| Live Graphs | matplotlib embedded | Native plots |
| Operation Buttons | Canvas text + callbacks | Buttons with callbacks |
| Sub-windows | Toplevel() popup | dpg.window() in context |
| Clocks/Timer | tk.Label with after() | dpg.text with frame callback |
| Graph Updates | Line.set_ydata() | dpg.set_value() + series |
| Color Scheme | Tkinter colors | RGB tuples (0-255) |

## Test Commands

**Tkinter:**
```bash
python main.py
```

**DearPyGui:**
```bash
python main_dpg.py
```

Click operation buttons to open:
- **Fuel Tank Operations** - Monitoring and pump controls
- **Rocket Operations** - Systems and emergency controls
- **Engine Control** - Ignition and throttle controls
- **STOP** - Emergency freeze/resume graphs

## Notes

1. DearPyGui requires a specific PyPI version (check latest)
2. All business logic and callbacks are preserved exactly
3. Visual layout is as close as possible to original (DearPyGui has different sizing constraints)
4. Graph rendering style differs due to native plotting vs matplotlib
5. Window positioning uses absolute coordinates (convertible to relative if needed)

## Debugging

If windows don't appear:
- Ensure all UI creation happens before `dpg.show_viewport()`
- Check that operation window functions are called before main render loop
- Verify dpg context is created before any UI elements

