import tkinter as tk
from tkinter import ttk

def open_vehicle_operations():
    # Create new window for vehicle operations
    vehicle_window = tk.Toplevel()
    vehicle_window.title("Rocket Operations Control")
    vehicle_window.geometry("800x600+100+100")
    vehicle_window.configure(bg='#0a0a1a')
    vehicle_window.deiconify()
    vehicle_window.update()

    # Title label
    title_label = tk.Label(vehicle_window, text="Rocket Operations Control Panel", 
                          font=('Arial', 16, 'bold'), fg='white', bg='#0a0a1a')
    title_label.pack(pady=20)

    # Main frame
    main_frame = tk.Frame(vehicle_window, bg='#0a0a1a')
    main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Vehicle systems
    systems_frame = tk.LabelFrame(main_frame, text="Rocket Systems", fg='white', bg='#0a0a1a', 
                                 font=('Arial', 12, 'bold'))
    systems_frame.pack(fill=tk.X, pady=10)

    # Lights and signals
    lights_frame = tk.Frame(systems_frame, bg='#0a0a1a')
    lights_frame.pack(pady=5)
    tk.Button(lights_frame, text="Navigation Lights", bg='yellow', fg='black', width=12).pack(side=tk.LEFT, padx=5)
    tk.Button(lights_frame, text="Warning Lights", bg='orange', fg='black', width=12).pack(side=tk.LEFT, padx=5)
    tk.Button(lights_frame, text="Beacon", bg='red', fg='white', width=12).pack(side=tk.LEFT, padx=5)

    # Emergency controls
    emergency_frame = tk.Frame(systems_frame, bg='#0a0a1a')
    emergency_frame.pack(pady=5)
    tk.Button(emergency_frame, text="EMERGENCY SHUTDOWN", bg='red', fg='white', font=('Arial', 12, 'bold'), 
             width=15, height=2).pack()

    # Status display
    status_frame = tk.LabelFrame(main_frame, text="Rocket Status", fg='white', bg='#0a0a1a', 
                                font=('Arial', 12, 'bold'))
    status_frame.pack(fill=tk.X, pady=10)

    # Status labels
    status_labels = [
        "Engine Status: Ready",
        "Fuel Level: 95%",
        "Oxidizer Level: 92%",
        "Avionics: Online",
        "Navigation: Locked",
        "Launch Sequence: Standby"
    ]

    for status in status_labels:
        tk.Label(status_frame, text=status, fg='white', bg='#0a0a1a', 
                font=('Arial', 10)).pack(anchor=tk.W, padx=10, pady=2)

    # Close button
    close_btn = tk.Button(vehicle_window, text="Close", command=vehicle_window.destroy, 
                         bg='gray', fg='white', width=10)
    close_btn.pack(pady=10)

    # Bring window to front
    vehicle_window.lift()
    vehicle_window.focus_force()

if __name__ == "__main__":
    # For testing the window independently
    root = tk.Tk()
    root.withdraw()  # Hide main window
    open_vehicle_operations()
    root.mainloop()