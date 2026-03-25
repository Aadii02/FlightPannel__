import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

def open_pressure_test():
    # Create new window for pressure test
    pressure_window = tk.Toplevel()
    pressure_window.title("Pressure Test Control")
    pressure_window.geometry("1000x500+300+300")
    pressure_window.configure(bg='#0a0a1a')
    pressure_window.deiconify()
    pressure_window.update()

    # Title
    title_label = tk.Label(pressure_window, text="Pressure Tests", 
                          font=('Arial', 14, 'bold'), fg='white', bg='#0a0a1a')
    title_label.pack(pady=20)

    # Main frame
    main_frame = tk.Frame(pressure_window, bg='#0a0a1a')
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Test controls
    test_frame = tk.LabelFrame(main_frame, text="Test Controls", fg='white', bg='#0a0a1a', 
                              font=('Arial', 12, 'bold'))
    test_frame.pack(fill=tk.X, pady=10)

    # Test buttons
    test_buttons = tk.Frame(test_frame, bg='#0a0a1a')
    test_buttons.pack(pady=10)
    tk.Button(test_buttons, text="Start Pressure Test", bg='green', fg='white', width=18).pack(side=tk.LEFT, padx=10)
    tk.Button(test_buttons, text="Stop Test", bg='red', fg='white', width=12).pack(side=tk.LEFT, padx=10)

    # Results display
    results_frame = tk.LabelFrame(main_frame, text="Test Results", fg='white', bg='#0a0a1a', 
                                 font=('Arial', 12, 'bold'))
    results_frame.pack(fill=tk.BOTH, expand=True, pady=10)

    results_text = tk.Text(results_frame, height=6, bg='#1a1a2a', fg='white', font=('Arial', 10))
    results_text.pack(fill=tk.X, padx=10, pady=10)
    results_text.insert(tk.END, "Pressure Test Results:\n\n- Current Pressure: 1.2 bar\n- Test Status: Ready\n- Last Test: Passed\n- Safety Check: OK\n")

    # Pressure Graphs
    graphs_frame = tk.Frame(main_frame, bg='#0a0a1a')
    graphs_frame.pack(fill=tk.BOTH, expand=True, pady=10)

    # Oxygen Tank Pressure Graph
    oxygen_graph_frame = tk.LabelFrame(graphs_frame, text="Oxygen Tank Pressure", fg='cyan', bg='#0a0a1a', 
                                       font=('Arial', 12, 'bold'))
    oxygen_graph_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

    # Create matplotlib figure for oxygen pressure graph
    fig_oxygen = Figure(figsize=(4, 3), dpi=100)
    fig_oxygen.patch.set_alpha(0)
    ax_oxygen = fig_oxygen.add_subplot(111)

    # Sample oxygen pressure data
    time_data_oxygen = np.linspace(0, 10, 50)
    pressure_data_oxygen = list(1.0 + 0.2 * np.sin(time_data_oxygen) + 0.1 * np.random.randn(50))

    line_oxygen, = ax_oxygen.plot(time_data_oxygen, pressure_data_oxygen, 'c-', linewidth=2)
    ax_oxygen.set_title('Oxygen Tank Pressure Over Time', fontsize=10, color='white')
    ax_oxygen.set_xlabel('Time (seconds)', fontsize=8, color='white')
    ax_oxygen.set_ylabel('Pressure (bar)', fontsize=8, color='white')
    ax_oxygen.set_ylim(0.5, 1.8)
    ax_oxygen.grid(True, alpha=0.3)

    ax_oxygen.patch.set_alpha(0)
    ax_oxygen.tick_params(colors='white')
    ax_oxygen.xaxis.label.set_color('white')
    ax_oxygen.yaxis.label.set_color('white')
    ax_oxygen.title.set_color('white')
    for spine in ax_oxygen.spines.values():
        spine.set_edgecolor('#444466')

    canvas_oxygen = FigureCanvasTkAgg(fig_oxygen, master=oxygen_graph_frame)
    canvas_oxygen.draw()
    canvas_oxygen.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    canvas_oxygen.get_tk_widget().configure(bg='#0a0a1a')

    # Fuel Tank Pressure Graph
    fuel_graph_frame = tk.LabelFrame(graphs_frame, text="Fuel Tank Pressure", fg='yellow', bg='#0a0a1a', 
                                     font=('Arial', 12, 'bold'))
    fuel_graph_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))

    # Create matplotlib figure for fuel pressure graph
    fig_fuel = Figure(figsize=(4, 3), dpi=100)
    fig_fuel.patch.set_alpha(0)
    ax_fuel = fig_fuel.add_subplot(111)

    # Sample fuel pressure data
    time_data_fuel = np.linspace(0, 10, 50)
    pressure_data_fuel = list(1.0 + 0.2 * np.sin(time_data_fuel) + 0.1 * np.random.randn(50))

    line_fuel, = ax_fuel.plot(time_data_fuel, pressure_data_fuel, 'y-', linewidth=2)
    ax_fuel.set_title('Fuel Tank Pressure Over Time', fontsize=10, color='white')
    ax_fuel.set_xlabel('Time (seconds)', fontsize=8, color='white')
    ax_fuel.set_ylabel('Pressure (bar)', fontsize=8, color='white')
    ax_fuel.set_ylim(0.5, 1.8)
    ax_fuel.grid(True, alpha=0.3)

    ax_fuel.patch.set_alpha(0)
    ax_fuel.tick_params(colors='white')
    ax_fuel.xaxis.label.set_color('white')
    ax_fuel.yaxis.label.set_color('white')
    ax_fuel.title.set_color('white')
    for spine in ax_fuel.spines.values():
        spine.set_edgecolor('#444466')

    canvas_fuel = FigureCanvasTkAgg(fig_fuel, master=fuel_graph_frame)
    canvas_fuel.draw()
    canvas_fuel.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    canvas_fuel.get_tk_widget().configure(bg='#0a0a1a')

    # Function to update pressure graphs
    def update_pressure_graph():
        # Update oxygen pressure
        new_pressure_oxygen = pressure_data_oxygen[-1] + 0.05 * (np.random.randn() - 0.5)
        new_pressure_oxygen = max(0.8, min(1.5, new_pressure_oxygen))
        
        pressure_data_oxygen[:-1] = pressure_data_oxygen[1:]
        pressure_data_oxygen[-1] = new_pressure_oxygen
        
        line_oxygen.set_ydata(pressure_data_oxygen)
        ax_oxygen.set_ylim(min(pressure_data_oxygen)-0.1, max(pressure_data_oxygen)+0.1)
        canvas_oxygen.draw()
        
        # Update fuel pressure
        new_pressure_fuel = pressure_data_fuel[-1] + 0.05 * (np.random.randn() - 0.5)
        new_pressure_fuel = max(0.8, min(1.5, new_pressure_fuel))
        
        pressure_data_fuel[:-1] = pressure_data_fuel[1:]
        pressure_data_fuel[-1] = new_pressure_fuel
        
        line_fuel.set_ydata(pressure_data_fuel)
        ax_fuel.set_ylim(min(pressure_data_fuel)-0.1, max(pressure_data_fuel)+0.1)
        canvas_fuel.draw()
        
        # Update every 2 seconds
        pressure_window.after(2000, update_pressure_graph)

    # Start updating the graphs
    update_pressure_graph()

    # Close button
    close_btn = tk.Button(pressure_window, text="Close", command=pressure_window.destroy, 
                         bg='gray', fg='white', width=10)
    close_btn.pack(pady=10)

    pressure_window.lift()
    pressure_window.focus_force()

def open_fuel_level():
    # Create new window for fuel level monitoring
    level_window = tk.Toplevel()
    level_window.title("Fuel Level Monitoring")
    level_window.geometry("700x500+400+300")
    level_window.configure(bg='#0a0a1a')
    level_window.deiconify()
    level_window.update()

    # Title
    title_label = tk.Label(level_window, text="Fuel & Oxygen Tank Level Monitoring", 
                          font=('Arial', 14, 'bold'), fg='white', bg='#0a0a1a')
    title_label.pack(pady=20)

    # Main frame
    main_frame = tk.Frame(level_window, bg='#0a0a1a')
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Left side - Oxygen Tank
    oxygen_frame = tk.LabelFrame(main_frame, text="Oxygen Tank", fg='cyan', bg='#0a0a1a', 
                                font=('Arial', 12, 'bold'))
    oxygen_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

    oxygen_display = tk.Frame(oxygen_frame, bg='#1a1a2a')
    oxygen_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    oxygen_level_label = tk.Label(oxygen_display, text="OXYGEN LEVEL\n92%", font=('Arial', 20, 'bold'), 
                                 fg='cyan', bg='#1a1a2a')
    oxygen_level_label.pack(expand=True)

    oxygen_info = tk.Label(oxygen_frame, text="Tank Capacity: 500L\nCurrent: 460L\nPressure: 200 bar\nTemperature: 20°C", 
                          fg='white', bg='#0a0a1a', font=('Arial', 10))
    oxygen_info.pack(pady=10)

    # Control buttons for Oxygen
    oxygen_buttons = tk.Frame(oxygen_frame, bg='#0a0a1a')
    oxygen_buttons.pack(pady=5)
    tk.Button(oxygen_buttons, text="Refill", bg='cyan', fg='black', width=10,
             command=lambda: oxygen_level_label.config(text="OXYGEN LEVEL\n100%")).pack(side=tk.LEFT, padx=5)
    tk.Button(oxygen_buttons, text="Drain", bg='blue', fg='white', width=10).pack(side=tk.LEFT, padx=5)

    # Right side - Fuel Tank
    fuel_frame = tk.LabelFrame(main_frame, text="Fuel Tank", fg='yellow', bg='#0a0a1a', 
                              font=('Arial', 12, 'bold'))
    fuel_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))

    fuel_display = tk.Frame(fuel_frame, bg='#1a1a2a')
    fuel_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    fuel_level_label = tk.Label(fuel_display, text="FUEL LEVEL\n85%", font=('Arial', 20, 'bold'), 
                               fg='yellow', bg='#1a1a2a')
    fuel_level_label.pack(expand=True)

    fuel_info = tk.Label(fuel_frame, text="Tank Capacity: 1000L\nCurrent: 850L\nTemperature: -183°C\nFuel Type: RP-1", 
                        fg='white', bg='#0a0a1a', font=('Arial', 10))
    fuel_info.pack(pady=10)

    # Control buttons for Fuel
    fuel_buttons = tk.Frame(fuel_frame, bg='#0a0a1a')
    fuel_buttons.pack(pady=5)
    tk.Button(fuel_buttons, text="Refill", bg='yellow', fg='black', width=10,
             command=lambda: fuel_level_label.config(text="FUEL LEVEL\n100%")).pack(side=tk.LEFT, padx=5)
    tk.Button(fuel_buttons, text="Drain", bg='orange', fg='white', width=10).pack(side=tk.LEFT, padx=5)

    # Close button
    close_btn = tk.Button(level_window, text="Close", command=level_window.destroy, 
                         bg='gray', fg='white', width=10)
    close_btn.pack(pady=10)

    level_window.lift()
    level_window.focus_force()

def open_tank_operations():
    # Create new window for fuel tank operations
    tank_window = tk.Toplevel()
    tank_window.title("Fuel Tank Operations Control")
    tank_window.geometry("800x600+200+200")
    tank_window.configure(bg='#0a0a1a')
    tank_window.deiconify()
    tank_window.update()

    # Title label
    title_label = tk.Label(tank_window, text="Fuel Tank Operations Control Panel", 
                          font=('Arial', 16, 'bold'), fg='white', bg='#0a0a1a')
    title_label.pack(pady=20)

    # Main frame with left and right sections
    main_frame = tk.Frame(tank_window, bg='#0a0a1a')
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    main_frame.grid_columnconfigure(0, weight=1)  # Left side
    main_frame.grid_columnconfigure(1, weight=0)  # Right side for buttons

    # Left side - Status and Monitoring
    left_frame = tk.Frame(main_frame, bg='#0a0a1a')
    left_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 10))

    # Status display at top
    status_var = tk.StringVar()
    status_var.set("Fuel Tank System Online")
    status_label = tk.Label(left_frame, textvariable=status_var, fg='yellow', bg='#0a0a1a', 
                           font=('Arial', 12, 'bold'))
    status_label.pack(pady=10)

    # Fuel Monitoring
    monitor_frame = tk.LabelFrame(left_frame, text="Fuel Monitoring", fg='white', bg='#0a0a1a', 
                                 font=('Arial', 12, 'bold'))
    monitor_frame.pack(fill=tk.X, pady=10)

    # Monitoring buttons
    monitor_buttons = tk.Frame(monitor_frame, bg='#0a0a1a')
    monitor_buttons.pack(pady=5)
    tk.Button(monitor_buttons, text="Check Level", bg='purple', fg='white', width=12,
             command=open_fuel_level).pack(side=tk.LEFT, padx=5)
    tk.Button(monitor_buttons, text="Pressure Test", bg='Purple', fg='white', width=12,
             command=open_pressure_test).pack(side=tk.LEFT, padx=5)
    tk.Button(monitor_buttons, text="Quality Check", bg='green', fg='white', width=12,
             command=lambda: status_var.set("Running Fuel Quality Check")).pack(side=tk.LEFT, padx=5)

    # System Status
    status_frame = tk.LabelFrame(left_frame, text="System Status", fg='white', bg='#0a0a1a', 
                                font=('Arial', 12, 'bold'))
    status_frame.pack(fill=tk.X, pady=10)

    # Status labels
    status_labels = [
        "Fuel Level: 85%",
        "Pressure: Normal",
        "Temperature: 25°C",
        "Pump Status: Ready",
        "Valve Status: Closed",
        "System Health: Good"
    ]

    for status in status_labels:
        tk.Label(status_frame, text=status, fg='white', bg='#0a0a1a', 
                font=('Arial', 10)).pack(anchor=tk.W, padx=10, pady=2)

    # Right side - Fuel System Controls (Vertical)
    right_frame = tk.Frame(main_frame, bg='#0a0a1a')
    right_frame.grid(row=0, column=1, sticky='ns')

    # Fuel System Controls title
    controls_title = tk.Label(right_frame, text="Fuel System Controls", fg='white', bg='#0a0a1a', 
                             font=('Arial', 12, 'bold'))
    controls_title.pack(pady=(0, 10))

    # Pump controls
    tk.Button(right_frame, text="Start Pump\n(Oxygen)", bg='green', fg='white', width=15, height=2,
             command=lambda: status_var.set("Oxygen Pump Started")).pack(pady=5)

    tk.Button(right_frame, text="Stop Pump\n(Oxygen)", bg='darkgreen', fg='white', width=15, height=2,
             command=lambda: status_var.set("Oxygen Pump Stopped")).pack(pady=5)

    tk.Button(right_frame, text="Start Pump\n(Fuel)", bg='red', fg='white', width=15, height=2,
             command=lambda: status_var.set("Fuel Pump Started")).pack(pady=5)

    tk.Button(right_frame, text="Stop Pump\n(Fuel)", bg='darkred', fg='white', width=15, height=2,
             command=lambda: status_var.set("Fuel Pump Stopped")).pack(pady=5)

    # Valve controls
    tk.Button(right_frame, text="Open Valve", bg='blue', fg='white', width=15, height=2,
             command=lambda: status_var.set("Fuel Valve Opened")).pack(pady=5)

    tk.Button(right_frame, text="Close Valve", bg='orange', fg='white', width=15, height=2,
             command=lambda: status_var.set("Fuel Valve Closed")).pack(pady=5)

    # Emergency controls
    tk.Button(right_frame, text="EMERGENCY\nSHUTOFF", bg='red', fg='white', font=('Arial', 10, 'bold'), 
             width=15, height=3, command=lambda: status_var.set("EMERGENCY SHUTOFF ACTIVATED")).pack(pady=10)

    # Close button
    close_btn = tk.Button(tank_window, text="Close", command=tank_window.destroy, 
                         bg='gray', fg='white', width=10)
    close_btn.pack(pady=10)

    # Bring window to front
    tank_window.lift()
    tank_window.focus_force()

if __name__ == "__main__":
    # For testing the window independently
    root = tk.Tk()
    root.withdraw()  # Hide main window
    open_tank_operations()
    root.mainloop()