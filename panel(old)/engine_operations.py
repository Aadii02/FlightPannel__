import tkinter as tk
from tkinter import ttk

def open_engine_operations():
    # Create new window for engine operations
    engine_window = tk.Toplevel()
    engine_window.title("Engine Control Panel")
    engine_window.geometry("800x600+150+150")
    engine_window.configure(bg='#0a0a1a')
    engine_window.deiconify()
    engine_window.update()

    # Title label
    title_label = tk.Label(engine_window, text="Engine Control Panel", 
                          font=('Arial', 16, 'bold'), fg='white', bg='#0a0a1a')
    title_label.pack(pady=20)

    # Main frame
    main_frame = tk.Frame(engine_window, bg='#0a0a1a')
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=0)

    # Left side - Engine Status and Monitoring
    left_frame = tk.Frame(main_frame, bg='#0a0a1a')
    left_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 10))

    # Status display at top
    status_var = tk.StringVar()
    status_var.set("Engine System Standby")
    status_label = tk.Label(left_frame, textvariable=status_var, fg='yellow', bg='#0a0a1a', 
                           font=('Arial', 12, 'bold'))
    status_label.pack(pady=10)

    # Engine Monitoring
    monitor_frame = tk.LabelFrame(left_frame, text="Engine Monitoring", fg='white', bg='#0a0a1a', 
                                 font=('Arial', 12, 'bold'))
    monitor_frame.pack(fill=tk.X, pady=10)

    # Monitoring buttons
    monitor_buttons = tk.Frame(monitor_frame, bg='#0a0a1a')
    monitor_buttons.pack(pady=5)
    tk.Button(monitor_buttons, text="Diagnostics", bg='purple', fg='white', width=12).pack(side=tk.LEFT, padx=5)
    tk.Button(monitor_buttons, text="Performance", bg='purple', fg='white', width=12).pack(side=tk.LEFT, padx=5)
    tk.Button(monitor_buttons, text="Temperature", bg='purple', fg='white', width=12).pack(side=tk.LEFT, padx=5)

    # Engine Status
    status_frame = tk.LabelFrame(left_frame, text="Engine Status", fg='white', bg='#0a0a1a', 
                                font=('Arial', 12, 'bold'))
    status_frame.pack(fill=tk.X, pady=10)

    # Status labels
    status_labels = [
        "Engine State: Standby",
        "RPM: 0",
        "Throttle: 0%",
        "Temperature: 25°C",
        "Pressure: Normal",
        "System Health: Excellent"
    ]

    for status in status_labels:
        tk.Label(status_frame, text=status, fg='white', bg='#0a0a1a', 
                font=('Arial', 10)).pack(anchor=tk.W, padx=10, pady=2)

    # Right side - Engine Control (Vertical)
    right_frame = tk.Frame(main_frame, bg='#0a0a1a')
    right_frame.grid(row=0, column=1, sticky='ns')

    # Engine Control title
    controls_title = tk.Label(right_frame, text="Engine Controls", fg='white', bg='#0a0a1a', 
                             font=('Arial', 12, 'bold'))
    controls_title.pack(pady=(0, 10))

    # Ignition controls
    tk.Button(right_frame, text="Pre-Ignition\nCheck", bg='orange', fg='black', width=15, height=2,
             command=lambda: status_var.set("Running Pre-Ignition Check...")).pack(pady=5)

    tk.Button(right_frame, text="Ignition\nON", bg='lime', fg='black', width=15, height=2,
             command=lambda: status_var.set("Engine Ignition ON")).pack(pady=5)

    tk.Button(right_frame, text="Ignition\nOFF", bg='red', fg='white', width=15, height=2,
             command=lambda: status_var.set("Engine Ignition OFF")).pack(pady=5)

    # Throttle controls
    tk.Button(right_frame, text="Increase\nThrottle", bg='cyan', fg='black', width=15, height=2,
             command=lambda: status_var.set("Throttle Increasing...")).pack(pady=5)

    tk.Button(right_frame, text="Decrease\nThrottle", bg='blue', fg='white', width=15, height=2,
             command=lambda: status_var.set("Throttle Decreasing...")).pack(pady=5)

    # Shutdown
    tk.Button(right_frame, text="SHUTDOWN", bg='darkred', fg='white', font=('Arial', 10, 'bold'), 
             width=15, height=2, command=lambda: status_var.set("Engine Shutdown Initiated")).pack(pady=10)

    # Close button
    close_btn = tk.Button(engine_window, text="Close", command=engine_window.destroy, 
                         bg='gray', fg='white', width=10)
    close_btn.pack(pady=10)

    # Bring window to front
    engine_window.lift()
    engine_window.focus_force()

if __name__ == "__main__":
    # For testing the window independently
    root = tk.Tk()
    root.withdraw()  # Hide main window
    open_engine_operations()
    root.mainloop()
