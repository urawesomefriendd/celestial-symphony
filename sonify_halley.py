import numpy as np
from scipy.io.wavfile import write

# Real orbital elements for Halley's Comet, from JPL Small-Body Database
e = 0.9679359956953211      # eccentricity
a = 17.92863504856923       # semi-major axis, AU
period_years = 75.91525280740373

# We'll sample the comet's position at many points across one full orbit
num_points = 2000
mean_anomaly = np.linspace(0, 2 * np.pi, num_points)  # represents "time" evenly spaced across the orbit

# Solving Kepler's Equation: M = E - e*sin(E)
# We know M (mean anomaly, basically "time"), we need E (eccentric anomaly, the real angular position)
# There's no simple formula for this -- we solve it numerically using Newton's method
def solve_kepler(M, e, tolerance=1e-8):
    E = M.copy()  # start with a guess
    for _ in range(100):  # refine the guess up to 100 times
        delta = (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
        E = E - delta
        if np.max(np.abs(delta)) < tolerance:
            break
    return E

E = solve_kepler(mean_anomaly, e)

# Once we have E, we can calculate the real distance from the sun at that moment
r = a * (1 - e * np.cos(E))  # distance from the sun, in AU

print(f"Closest approach in this simulation: {r.min():.3f} AU")
print(f"Farthest point in this simulation: {r.max():.3f} AU")

# Comet brightness roughly follows an inverse power law with distance from the sun
# (comets brighten dramatically as they near the sun -- much more dramatically than planets do,
# because heat causes the comet to release gas/dust, which is what we actually see glowing)
relative_brightness = 1 / (r ** 3)  # simplified but physically-motivated approximation
relative_brightness = relative_brightness / relative_brightness.max()  # normalize 0 to 1

# ---- Sonify: map brightness to both pitch AND volume for a "surreal" swelling effect ----
sample_rate = 44100
total_duration = 60  # compress the full 76-year orbit into 60 seconds
samples_per_point = int(sample_rate * total_duration / num_points)

full_wave = np.array([])

base_freq = 100  # low, distant hum when far from the sun
max_freq_boost = 400  # how much higher pitch gets at peak brightness

for b in relative_brightness:
    frequency = base_freq + (b * max_freq_boost)
    t = np.linspace(0, samples_per_point / sample_rate, samples_per_point, endpoint=False)
    tone = np.sin(2 * np.pi * frequency * t)
    tone = tone * b  # volume swells with brightness too -- silence-ish when far, full volume near the sun
    full_wave = np.concatenate([full_wave, tone])

write("halley_journey.wav", sample_rate, full_wave.astype(np.float32))
print("Done! Check your folder for halley_journey.wav")