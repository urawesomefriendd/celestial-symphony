import csv
import numpy as np
from scipy.io.wavfile import write
from collections import defaultdict

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

max_mag = max(daily_avg_mag)
min_mag = min(daily_avg_mag)

# A minor scale, built across 3 octaves for a wide singable range (frequencies in Hz)
# These are real, standard musical note frequencies
a_minor_scale = [
    220.00, 246.94, 261.63, 293.66, 329.63, 349.23, 392.00,   # A3 to G4
    440.00, 493.88, 523.25, 587.33, 659.25, 698.46, 783.99,   # A4 to G5
    880.00                                                     # A5
]

sample_rate = 44100
note_duration = 0.15
full_wave = np.array([])

for mag in daily_avg_mag:
    # Normalize brightness to a 0-1 range
    brightness = (max_mag - mag) / (max_mag - min_mag)
    
    # Map that 0-1 range onto an INDEX in our scale list, instead of a raw frequency
    scale_index = int(brightness * (len(a_minor_scale) - 1))
    frequency = a_minor_scale[scale_index]
    
    t = np.linspace(0, note_duration, int(sample_rate * note_duration), endpoint=False)
    
    # Add a simple fade-out to each note so they don't click/pop against each other
    note = np.sin(2 * np.pi * frequency * t)
    fade = np.linspace(1, 0, len(t)) ** 2
    note = note * fade
    
    full_wave = np.concatenate([full_wave, note])

write("mira_scaled.wav", sample_rate, full_wave.astype(np.float32))
print("Done! Check your folder for mira_scaled.wav")