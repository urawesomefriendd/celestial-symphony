"""
Quick, lighter sonifications for the "Explore More Sounds" bonus page.
Each one is grounded in a single real fact, but isn't as deeply processed
or musically refined as the core four objects -- these are sketches.
"""

import numpy as np
from scipy.io.wavfile import write

sample_rate = 44100

def save_tone(filename, frequency, duration, volume=0.5, fade=0.05):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = np.sin(2 * np.pi * frequency * t) * volume
    fade_len = int(sample_rate * fade)
    wave[:fade_len] *= np.linspace(0, 1, fade_len)
    wave[-fade_len:] *= np.linspace(1, 0, fade_len)
    write(filename, sample_rate, wave.astype(np.float32))
    print(f"Saved {filename}")

# ---- Jupiter: real rotation period = 9.9 hours (fastest planet) ----
# Compressed: 9.9 hours -> mapped to a fast, low oscillation
jupiter_freq = 55  # low, fast-feeling tone
save_tone("audio/explore_jupiter.wav", jupiter_freq, duration=4)

# ---- Saturn: real day = 10.7 hours, real orbit = 29.5 years ----
# Two layered tones: fast "spin" tone + slow "orbit" tone
t = np.linspace(0, 5, int(sample_rate * 5), endpoint=False)
spin = np.sin(2 * np.pi * 60 * t)
orbit = np.sin(2 * np.pi * 2 * t)  # slow modulation representing its long orbit
saturn_wave = (spin * 0.4) * (0.6 + 0.4 * orbit)
fade_len = int(sample_rate * 0.05)
saturn_wave[:fade_len] *= np.linspace(0, 1, fade_len)
saturn_wave[-fade_len:] *= np.linspace(1, 0, fade_len)
write("audio/explore_saturn.wav", sample_rate, saturn_wave.astype(np.float32))
print("Saved audio/explore_saturn.wav")

# ---- Mars: real day = 24.6 hours, almost Earth-length ----
save_tone("audio/explore_mars.wav", 110, duration=4)  # steady, "familiar" pitch

# ---- Andromeda: real recession velocity = -110 km/s (moving TOWARD us) ----
# Sonified as a slow downward glide (a naive stand-in for blueshift)
duration = 6
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
start_freq, end_freq = 300, 180  # descending, representing approach
freq_sweep = np.linspace(start_freq, end_freq, len(t))
andromeda_wave = np.sin(2 * np.pi * np.cumsum(freq_sweep) / sample_rate) * 0.4
fade_len = int(sample_rate * 0.1)
andromeda_wave[:fade_len] *= np.linspace(0, 1, fade_len)
andromeda_wave[-fade_len:] *= np.linspace(1, 0, fade_len)
write("audio/explore_andromeda.wav", sample_rate, andromeda_wave.astype(np.float32))
print("Saved audio/explore_andromeda.wav")

# ---- Comet NEOWISE: quick brightness-style sketch (simplified, not full Kepler solve) ----
num_notes = 40
brightness_curve = np.concatenate([
    np.linspace(0.05, 1.0, num_notes // 2) ** 2,   # approach: brightening
    np.linspace(1.0, 0.05, num_notes // 2) ** 2,   # retreat: fading
])
notes_wave = np.array([])
for b in brightness_curve:
    freq = 220 + b * 400
    note_len = 0.12
    t = np.linspace(0, note_len, int(sample_rate * note_len), endpoint=False)
    note = np.sin(2 * np.pi * freq * t) * (0.2 + b * 0.5)
    notes_wave = np.concatenate([notes_wave, note])
write("audio/explore_neowise.wav", sample_rate, notes_wave.astype(np.float32))
print("Saved audio/explore_neowise.wav")

# ---- Black hole merger chirp (GW150914-style): rising frequency + amplitude, then cutoff ----
# Simplified recreation of the real, famous "chirp" shape -- not the actual waveform data.
duration = 2.5
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
f_start, f_end = 35, 250  # Hz, rising -- mirrors the real GW150914 chirp's rough shape
freq_sweep = np.linspace(f_start, f_end, len(t)) ** 1.5
freq_sweep = f_start + (freq_sweep - freq_sweep.min()) / (freq_sweep.max() - freq_sweep.min()) * (f_end - f_start)
amplitude = np.linspace(0.1, 1.0, len(t)) ** 2  # grows louder as it spirals in
chirp = np.sin(2 * np.pi * np.cumsum(freq_sweep) / sample_rate) * amplitude
# sharp cutoff right after peak, like the real merger's ringdown
cutoff = int(sample_rate * 0.15)
chirp[-cutoff:] *= np.linspace(1, 0, cutoff)
write("audio/explore_blackhole_chirp.wav", sample_rate, (chirp * 0.6).astype(np.float32))
print("Saved audio/explore_blackhole_chirp.wav")

print("\nAll bonus sounds generated!")
