import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import defaultdict

# ---- Load Mira data (same as before) ----
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
brightness = [max(daily_avg_mag) - m for m in daily_avg_mag]

# ---- Set up a figure with 3 panels side by side ----
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5), facecolor='black')

for ax in (ax1, ax2, ax3):
    ax.set_facecolor('black')
    ax.tick_params(colors='white')

# --- Panel 1: Mira ---
ax1.set_xlim(0, len(brightness))
ax1.set_ylim(min(brightness) - 0.5, max(brightness) + 0.5)
ax1.set_title("Mira (Variable Star)", color='white')
mira_line, = ax1.plot([], [], color='cyan', linewidth=2)
mira_dot, = ax1.plot([], [], 'o', color='yellow', markersize=8)

# --- Panel 2: Pulsar ---
ax2.set_xlim(-1.5, 1.5)
ax2.set_ylim(-1.5, 1.5)
ax2.set_title("Crab Pulsar (30 spins/sec)", color='white')
ax2.set_xticks([])
ax2.set_yticks([])
pulsar_beam, = ax2.plot([], [], color='magenta', linewidth=3)
pulsar_star = ax2.scatter([0], [0], color='white', s=200)

# --- Panel 3: Exoplanet ---
ax3.set_xlim(-1.5, 1.5)
ax3.set_ylim(-1.5, 1.5)
ax3.set_title("Kepler-10 b (Transit)", color='white')
ax3.set_xticks([])
ax3.set_yticks([])
exo_star = ax3.scatter([0], [0], color='orange', s=400)
exo_planet, = ax3.plot([], [], 'o', color='blue', markersize=10)

pulsar_freq = 29.9469230  # real spin rate, spins/sec
exo_period_frames = 60    # how many frames = one fake "orbit" for visual purposes

def init():
    mira_line.set_data([], [])
    mira_dot.set_data([], [])
    pulsar_beam.set_data([], [])
    exo_planet.set_data([], [])
    return mira_line, mira_dot, pulsar_beam, exo_planet

def animate(frame):
    # Mira: reveal one more day each frame
    mira_frame = min(frame, len(brightness))
    x = list(range(mira_frame))
    y = brightness[:mira_frame]
    mira_line.set_data(x, y)
    if mira_frame > 0:
        mira_dot.set_data([mira_frame - 1], [brightness[mira_frame - 1]])

    # Pulsar: spinning beam, angle advances based on real spin frequency
    angle = 2 * np.pi * pulsar_freq * (frame / 20)  # frame/20 approximates seconds
    beam_x = [0, 1.3 * np.cos(angle)]
    beam_y = [0, 1.3 * np.sin(angle)]
    pulsar_beam.set_data(beam_x, beam_y)

    # Exoplanet: orbiting dot, dims the star briefly when crossing in front
    orbit_angle = 2 * np.pi * (frame % exo_period_frames) / exo_period_frames
    planet_x = 1.2 * np.cos(orbit_angle)
    planet_y = 0.3 * np.sin(orbit_angle)  # flattened ellipse for a "side view" feel
    exo_planet.set_data([planet_x], [planet_y])

    # Dim the star when planet crosses close in front (small x range near center, y near 0)
    if abs(planet_x) < 0.3 and planet_y > 0:
        exo_star.set_color('darkred')
    else:
        exo_star.set_color('orange')

    return mira_line, mira_dot, pulsar_beam, exo_planet

ani = animation.FuncAnimation(
    fig, animate, init_func=init,
    frames=len(brightness), interval=50, blit=False
)

plt.tight_layout()
plt.show()