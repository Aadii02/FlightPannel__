import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from PIL import Image, ImageTk
from tank_operations import open_tank_operations
from vehicle_operations import open_vehicle_operations
from engine_operations import open_engine_operations

import time
from datetime import datetime, timezone, timedelta

# Mission start time (resets each launch)
mission_start_time = time.time()

# Create main window
root = tk.Tk()
root.title("Mission Control Window")
root.geometry("1200x800")
root.configure(bg='#0a0a1a')  # dark navy background

# Track whether system is stopped
system_stopped = False

# Sample data length and arrays
length = 100
x = np.linspace(0, 10, length)
# initialize with random values
y1 = np.random.randn(length)
y2 = np.random.randn(length)
y3 = np.random.randn(length)
vel = np.random.randn(length)
acc = np.random.randn(length)
alt = np.random.randn(length)
# electrical signals
bat = 12 + np.random.randn(length) * 0.1
temp_in = 20 + np.random.randn(length) * 0.5
temp_out = 15 + np.random.randn(length) * 0.5
press_in = 101 + np.random.randn(length) * 0.5
press_out = 100 + np.random.randn(length) * 0.5

# Configure grid
root.grid_rowconfigure(0, weight=2)  # top row for logo + axis graphs
root.grid_rowconfigure(1, weight=1)  # middle row for side panels
root.grid_rowconfigure(2, weight=0)  # bottom row for buttons (fixed height)
root.grid_columnconfigure(0, weight=1)  # left column for logo/velocity/acc/alt
root.grid_columnconfigure(1, weight=2)  # middle column for graphs/electrical
root.grid_columnconfigure(2, weight=0)  # right column for buttons (fixed width)

# Global line objects (will be assigned after creation)
line1 = None
line2 = None
line3 = None
line_vel = None
line_acc = None
line_alt = None
line_batt = None
line_temp_in = None
line_temp_out = None
line_press_in = None
line_press_out = None

# Logo frame (top left)
logo_frame = tk.Frame(root, bg='#0a0a1a')
logo_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)

# Load and display logo
try:
    logo_img = Image.open('images/WhatsApp_Image_2026-03-03_at_8.23.29_PM-removebg-preview.png')
    logo_img.thumbnail((200, 200), Image.Resampling.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(logo_frame, image=logo_photo, bg='#0a0a1a')
    logo_label.image = logo_photo
    logo_label.pack(side=tk.LEFT, padx=5)
except Exception as e:
    print(f"Could not load logo: {e}")

# Mission title and clock
title_frame = tk.Frame(logo_frame, bg='#0a0a1a')
title_frame.pack(side=tk.LEFT, padx=20)
tk.Label(title_frame, text="MISSION CONTROL", font=('Arial', 18, 'bold'), fg='cyan', bg='#0a0a1a').pack(anchor='w')

clock_frame = tk.Frame(title_frame, bg='#0a0a1a')
clock_frame.pack(anchor='w')
utc_label = tk.Label(clock_frame, text="", font=('Consolas', 10), fg='#aaaaaa', bg='#0a0a1a')
utc_label.pack(side=tk.LEFT)
ist_label = tk.Label(clock_frame, text="", font=('Consolas', 10), fg='#aaaaaa', bg='#0a0a1a')
ist_label.pack(side=tk.LEFT, padx=(15, 0))

timer_label = tk.Label(title_frame, text="T+ 00:00:00", font=('Consolas', 12, 'bold'), fg='orange', bg='#0a0a1a')
timer_label.pack(anchor='w')
status_indicator = tk.Label(title_frame, text="\u25CF SYSTEMS ONLINE", font=('Arial', 10, 'bold'), fg='lime', bg='#0a0a1a')
status_indicator.pack(anchor='w')

def update_clock():
    utc_now = datetime.now(timezone.utc)
    ist_now = utc_now + timedelta(hours=5, minutes=30)
    utc_label.config(text=utc_now.strftime("UTC  %H:%M:%S"))
    ist_label.config(text=ist_now.strftime("IST  %H:%M:%S"))
    # Mission elapsed timer
    elapsed = int(time.time() - mission_start_time)
    h, rem = divmod(elapsed, 3600)
    m, s = divmod(rem, 60)
    timer_label.config(text=f"T+ {h:02d}:{m:02d}:{s:02d}")
    root.after(1000, update_clock)

update_clock()

# Side frame for velocity, acceleration, altitude
side_frame = tk.Frame(root, bg='#0a0a1a')
side_frame.grid(row=1, column=0, sticky='nsew')

fig_side = Figure(figsize=(2, 6))
fig_side.patch.set_alpha(0)  # transparent figure background
ax4 = fig_side.add_subplot(311)
ax5 = fig_side.add_subplot(312)
ax6 = fig_side.add_subplot(313)

line_vel, = ax4.plot(x, vel, label='Velocity', color='cyan')
ax4.set_title('Velocity', fontsize=8)
ax4.legend(fontsize=6)
ax4.set_ylim(-3, 3)
ax4.tick_params(labelsize=6)
ax4.grid(True)

line_acc, = ax5.plot(x, acc, label='Acceleration', color='lime')
ax5.set_title('Acceleration', fontsize=8)
ax5.legend(fontsize=6)
ax5.set_ylim(-4, 4)
ax5.tick_params(labelsize=6)
ax5.grid(True)

line_alt, = ax6.plot(x, alt, label='Altitude', color='orangered')
ax6.set_title('Altitude', fontsize=8)
ax6.legend(fontsize=6)
ax6.set_ylim(-6, 6)
ax6.tick_params(labelsize=6)
ax6.grid(True)

canvas_side = FigureCanvasTkAgg(fig_side, master=side_frame)
canvas_side.draw()
canvas_side.get_tk_widget().pack(fill=tk.BOTH, expand=True)
canvas_side.get_tk_widget().configure(bg='#0a0a1a')

# Right frame for electrical information
right_frame = tk.Frame(root, bg='#0a0a1a')
right_frame.grid(row=1, column=1, sticky='nsew')

bat = 12 + np.sin(x)
temp_in = 20 + np.sin(x)
temp_out = 15 + np.cos(x)
press_in = 101 + np.sin(x)
press_out = 100 + np.cos(x)

fig_elec = Figure(figsize=(2, 4))
fig_elec.patch.set_alpha(0)  # transparent figure background
gs = fig_elec.add_gridspec(3, 2)

ax_batt = fig_elec.add_subplot(gs[0, :])
line_batt, = ax_batt.plot(x, bat, label='Battery Voltage', color='yellow')
ax_batt.set_title('Battery Voltage', fontsize=8)
ax_batt.set_ylim(0, 15)
ax_batt.legend(fontsize=6)
ax_batt.tick_params(labelsize=6)
ax_batt.grid(True)

ax_temp_in = fig_elec.add_subplot(gs[1, 0])
ax_temp_out = fig_elec.add_subplot(gs[1, 1])
line_temp_in, = ax_temp_in.plot(x, temp_in, label='Temp Inside', color='tomato')
ax_temp_in.set_title('Temp Inside', fontsize=8)
ax_temp_in.legend(fontsize=6)
ax_temp_in.tick_params(labelsize=6)
ax_temp_in.grid(True)
line_temp_out, = ax_temp_out.plot(x, temp_out, label='Temp Outside', color='skyblue')
ax_temp_out.set_title('Temp Outside', fontsize=8)
ax_temp_out.legend(fontsize=6)
ax_temp_out.tick_params(labelsize=6)
ax_temp_out.grid(True)

ax_press_in = fig_elec.add_subplot(gs[2, 0])
ax_press_out = fig_elec.add_subplot(gs[2, 1])
line_press_in, = ax_press_in.plot(x, press_in, label='Pressure Inside', color='violet')
ax_press_in.set_title('Pressure Inside', fontsize=8)
ax_press_in.legend(fontsize=6)
ax_press_in.tick_params(labelsize=6)
ax_press_in.grid(True)
line_press_out, = ax_press_out.plot(x, press_out, label='Pressure Outside', color='plum')
ax_press_out.set_title('Pressure Outside', fontsize=8)
ax_press_out.legend(fontsize=6)
ax_press_out.tick_params(labelsize=6)
ax_press_out.grid(True)

canvas_elec = FigureCanvasTkAgg(fig_elec, master=right_frame)
canvas_elec.draw()
canvas_elec.get_tk_widget().pack(fill=tk.BOTH, expand=True)
canvas_elec.get_tk_widget().configure(bg='#0a0a1a')

# Button frame for operations
button_frame = tk.Frame(root, bg='#0a0a1a')
button_frame.grid(row=0, column=2, rowspan=3, sticky='ns', padx=10, pady=10)

def tank_command():
    print("Tank Operations button clicked!")
    try:
        open_tank_operations()  # Open tank operations window
        print("Tank window opened successfully")
    except Exception as e:
        print(f"Error opening tank window: {e}")

def vehicle_command():
    print("Vehicle Operations button clicked!")
    try:
        open_vehicle_operations()  # Open vehicle operations window
        print("Vehicle window opened successfully")
    except Exception as e:
        print(f"Error opening vehicle window: {e}")

def engine_command():
    print("Engine Control button clicked!")
    try:
        open_engine_operations()  # Open engine operations window
        print("Engine window opened successfully")
    except Exception as e:
        print(f"Error opening engine window: {e}")

def stop_command():
    global system_stopped
    system_stopped = not system_stopped
    if system_stopped:
        status_indicator.config(text="\u25CF EMERGENCY STOP", fg='red')
        stop_canvas.itemconfig('all', fill='white')
        stop_canvas.config(bg='darkred')
        print("EMERGENCY STOP ACTIVATED")
    else:
        status_indicator.config(text="\u25CF SYSTEMS ONLINE", fg='lime')
        stop_canvas.itemconfig('all', fill='white')
        stop_canvas.config(bg='red')
        print("Systems resumed")

# Tank Operations button - blue with vertical text
tank_canvas = tk.Canvas(button_frame, bg='blue', height=150, width=60, highlightthickness=0, relief='raised', borderwidth=3)
tank_canvas.create_text(30, 75, text="Fuel Tank\nOperations", angle=90, fill='white', font=('Arial', 10, 'bold'))
tank_canvas.bind("<Button-1>", lambda e: tank_command())
tank_canvas.bind("<Enter>", lambda e: tank_canvas.config(bg='lightblue'))
tank_canvas.bind("<Leave>", lambda e: tank_canvas.config(bg='blue'))
tank_canvas.pack(side=tk.TOP, expand=True, fill=tk.X, padx=5, pady=5)

# Vehicle Operations button - yellow with vertical text
vehicle_canvas = tk.Canvas(button_frame, bg='yellow', height=150, width=60, highlightthickness=0, relief='raised', borderwidth=3)
vehicle_canvas.create_text(30, 75, text="Rocket\nOperations", angle=90, fill='black', font=('Arial', 10, 'bold'))
vehicle_canvas.bind("<Button-1>", lambda e: vehicle_command())
vehicle_canvas.bind("<Enter>", lambda e: vehicle_canvas.config(bg='lightyellow'))
vehicle_canvas.bind("<Leave>", lambda e: vehicle_canvas.config(bg='yellow'))
vehicle_canvas.pack(side=tk.TOP, expand=True, fill=tk.X, padx=5, pady=5)

# Engine Control button - green with vertical text
engine_canvas = tk.Canvas(button_frame, bg='green', height=150, width=60, highlightthickness=0, relief='raised', borderwidth=3)
engine_canvas.create_text(30, 75, text="Engine\nControl", angle=90, fill='white', font=('Arial', 10, 'bold'))
engine_canvas.bind("<Button-1>", lambda e: engine_command())
engine_canvas.bind("<Enter>", lambda e: engine_canvas.config(bg='lightgreen'))
engine_canvas.bind("<Leave>", lambda e: engine_canvas.config(bg='green'))
engine_canvas.pack(side=tk.TOP, expand=True, fill=tk.X, padx=5, pady=5)

# STOP button - red with vertical text
stop_canvas = tk.Canvas(button_frame, bg='red', height=150, width=60, highlightthickness=0, relief='raised', borderwidth=3)
stop_canvas.create_text(30, 75, text="STOP", angle=90, fill='white', font=('Arial', 12, 'bold'))
stop_canvas.bind("<Button-1>", lambda e: stop_command())
stop_canvas.bind("<Enter>", lambda e: stop_canvas.config(bg='lightcoral'))
stop_canvas.bind("<Leave>", lambda e: stop_canvas.config(bg='red'))
stop_canvas.pack(side=tk.TOP, expand=True, fill=tk.X, padx=5, pady=5)

# Top frame for X, Y, Z graphs
top_frame = tk.Frame(root, bg='#0a0a1a')
top_frame.grid(row=0, column=1, sticky='nsew')

fig_top = Figure(figsize=(2, 2))
fig_top.patch.set_alpha(0)  # transparent figure background
ax1 = fig_top.add_subplot(131)
ax2 = fig_top.add_subplot(132)
ax3 = fig_top.add_subplot(133)

line1, = ax1.plot(x, y1, label='X Axis', color='deepskyblue')
ax1.set_title('X Axis', fontsize=8)
ax1.legend(fontsize=6)
ax1.set_ylim(-2, 2)
ax1.tick_params(labelsize=6)

line2, = ax2.plot(x, y2, label='Y Axis', color='mediumspringgreen')
ax2.set_title('Y Axis', fontsize=8)
ax2.legend(fontsize=6)
ax2.set_ylim(-2, 2)
ax2.tick_params(labelsize=6)

line3, = ax3.plot(x, y3, label='Z Axis', color='hotpink')
ax3.set_title('Z Axis', fontsize=8)
ax3.legend(fontsize=6)
ax3.set_ylim(-2, 2)
ax3.tick_params(labelsize=6)

canvas_top = FigureCanvasTkAgg(fig_top, master=top_frame)
canvas_top.draw()
canvas_top.get_tk_widget().pack(fill=tk.BOTH, expand=True)
canvas_top.get_tk_widget().configure(bg='#0a0a1a')

# Apply dark styling to ALL axes
all_axes = [ax1, ax2, ax3, ax4, ax5, ax6,
            ax_batt, ax_temp_in, ax_temp_out, ax_press_in, ax_press_out]

for ax in all_axes:
    ax.patch.set_alpha(0)           # transparent axes background
    ax.tick_params(colors='white')
    ax.title.set_color('white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    for spine in ax.spines.values():
        spine.set_edgecolor('#444466')
    ax.grid(True, color='#222244', linestyle='--', alpha=0.7)
    legend = ax.get_legend()
    if legend:
        legend.get_frame().set_alpha(0)
        for text in legend.get_texts():
            text.set_color('white')

# Redraw all canvases after styling
canvas_top.draw()
canvas_side.draw()
canvas_elec.draw()

# Live update function
def update():
    global y1, y2, y3, vel, acc, alt, bat, temp_in, temp_out, press_in, press_out
    global line1, line2, line3, line_vel, line_acc, line_alt, line_batt, line_temp_in, line_temp_out, line_press_in, line_press_out

    if system_stopped:
        root.after(500, update)
        return

    def roll_append(arr, center=0, scale=1):
        arr = np.roll(arr, -1)
        arr[-1] = center + np.random.randn() * scale
        return arr

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

    line1.set_ydata(y1)
    line2.set_ydata(y2)
    line3.set_ydata(y3)
    line_vel.set_ydata(vel)
    line_acc.set_ydata(acc)
    line_alt.set_ydata(alt)
    line_batt.set_ydata(bat)
    line_temp_in.set_ydata(temp_in)
    line_temp_out.set_ydata(temp_out)
    line_press_in.set_ydata(press_in)
    line_press_out.set_ydata(press_out)

    canvas_top.draw()
    canvas_side.draw()
    canvas_elec.draw()
    root.after(500, update)

update()
root.mainloop()