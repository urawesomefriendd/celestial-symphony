import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import defaultdict

# Load and process the same Mira data as before
jd_values = []
mag_values = []

with open("mira_data.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        try:
            jd = float(row[0])
            mag = float(row[1])
            jd_values.append(jd)
            mag_values.append(mag)
        except (ValueError, IndexError):
            continue

daily_mags = defaultdict(list)
for jd, mag in zip(jd_values, mag_values):
    day = int(jd)
    daily_mags[day].append(mag)

sorted_days = sorted(daily_mags.keys())
daily_avg_mag = [sum(daily_mags[day]) / len(daily_mags[day]) for day in sorted_days]

# Flip magnitude so the graph shows "brightness" going UP when the star is brighter
# (remember: lower magnitude = brighter, so we flip it for intuitive viewing)
brightness = [max(daily_avg_mag) - m for m in daily_avg_mag]

# Set up the plot
fig, ax = plt.subplots(figsize=(10, 5), facecolor='black')
ax.set_facecolor('black')
ax.set_xlim(0, len(brightness))
ax.set_ylim(min(brightness) - 0.5, max(brightness) + 0.5)
ax.set_title("Mira: Real Brightness Over Time", color='white', fontsize=14)
ax.set_xlabel("Days", color='white')
ax.set_ylabel("Relative Brightness", color='white')
ax.tick_params(colors='white')

line, = ax.plot([], [], color='cyan', linewidth=2)
dot, = ax.plot([], [], 'o', color='yellow', markersize=10)

def init():
    line.set_data([], [])
    dot.set_data([], [])
    return line, dot

def animate(frame):
    x = list(range(frame))
    y = brightness[:frame]
    line.set_data(x, y)
    if frame > 0:
        dot.set_data([frame - 1], [brightness[frame - 1]])
    return line, dot

ani = animation.FuncAnimation(
    fig, animate, init_func=init,
    frames=len(brightness), interval=50, blit=True
)

plt.tight_layout()
plt.show()