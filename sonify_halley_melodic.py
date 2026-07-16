import numpy as np
from scipy.io.wavfile import write

# Real orbital elements for Halley's Comet, from JPL Small-Body Database
e = 0.9679359956953211
a = 17.92863504856923

num_notes = 120  # number of distinct notes across the full orbit
# Instead of even time-spacing, cluster more notes near perihelion (the sun)
# and fewer out in deep space -- for musical pacing, not raw uniform sampling
x = np.linspace(0, np.pi, num_notes)
mean_anomaly = np.pi * (1 - np.cos(x))

def solve_kepler(M, e, tolerance=1e-8):
    E = M.copy()
    for _ in range(100):
        delta = (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
        E = E - delta
        if np.max(np.abs(delta)) < tolerance:
            break
    return E

E = solve_kepler(mean_anomaly, e)
r = a * (1 - e * np.cos(E))  # real distance from sun, AU, at each of our 120 moments

# Real orbital speed (from vis-viva equation) -- genuinely how fast the comet moves at each point
# Using simplified units where GM_sun = 4*pi^2 (AU/year units)
GM = 4 * np.pi**2
speed = np.sqrt(GM * (2 / r - 1 / a))  # AU per year, real physics

# Use a logarithmic scale, since raw brightness varies too extremely (matches how
# astronomers measure real brightness/magnitude -- compressing huge ranges into something usable)
raw_brightness = 1 / (r ** 3)
log_brightness = np.log(raw_brightness)
relative_brightness = (log_brightness - log_brightness.min()) / (log_brightness.max() - log_brightness.min())
# Normalize speed to 0-1 for mapping to note duration
speed_norm = (speed - speed.min()) / (speed.max() - speed.min())
print("Brightness values (sample):", np.round(relative_brightness[::10], 3))
print("Speed values (sample):", np.round(speed_norm[::10], 3))

# ---- Lydian scale (bright, dreamy, "magical" sound) across 3 octaves ----
# Built on C: C D E F# G A B
lydian_scale = [
    261.63, 293.66, 329.63, 369.99, 392.00, 440.00, 493.88,   # C4 to B4
    523.25, 587.33, 659.25, 739.99, 783.99, 880.00, 987.77,   # C5 to B5
    1046.50                                                     # C6
]

sample_rate = 44100
min_note_len = 0.08   # fastest notes, near perihelion
max_note_len = 0.6    # slowest notes, far from the sun

full_wave = np.array([])

for i in range(num_notes):
    brightness = relative_brightness[i]
    fast = speed_norm[i]

    # pitch: brighter = higher note on our magical scale
    scale_index = int(brightness * (len(lydian_scale) - 1))
    frequency = lydian_scale[scale_index]

    # duration: faster real speed = shorter note (real Kepler physics driving rhythm)
    note_duration = max_note_len - (fast * (max_note_len - min_note_len))

    t = np.linspace(0, note_duration, int(sample_rate * note_duration), endpoint=False)
    note = np.sin(2 * np.pi * frequency * t)

    # smooth fade in/out so notes don't click
    fade_len = min(len(t) // 4, 2000)
    fade_in = np.linspace(0, 1, fade_len)
    fade_out = np.linspace(1, 0, fade_len)
    envelope = np.ones(len(t))
    envelope[:fade_len] = fade_in
    envelope[-fade_len:] = fade_out

    note = note * envelope * (0.3 + brightness * 0.7)  # volume also swells with brightness

    full_wave = np.concatenate([full_wave, note])

# ---- Add a simple echo/reverb for a magical, spacious feel ----
delay_samples = int(0.25 * sample_rate)  # quarter-second delay
echo = np.zeros(len(full_wave) + delay_samples * 2)
echo[:len(full_wave)] += full_wave
echo[delay_samples:delay_samples + len(full_wave)] += full_wave * 0.4  # faint delayed copy
echo[delay_samples*2:delay_samples*2 + len(full_wave)] += full_wave * 0.2  # even fainter second echo

# Normalize so it doesn't distort
echo = echo / np.max(np.abs(echo))

write("halley_journey_melodic.wav", sample_rate, echo.astype(np.float32))
print("Done! Check your folder for halley_journey_melodic.wav")