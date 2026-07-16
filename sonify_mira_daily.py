import csv
import numpy as np
from scipy.io.wavfile import write

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

print(f"Loaded {len(mag_values)} real observations of Mira!")

# Group observations by whole day (round JD down to nearest whole number)
from collections import defaultdict
daily_mags = defaultdict(list)

for jd, mag in zip(jd_values, mag_values):
    day = int(jd)  # rounds down -- groups all observations from the same day together
    daily_mags[day].append(mag)

# Average all magnitudes for each day, then sort by day
sorted_days = sorted(daily_mags.keys())
daily_avg_mag = [sum(daily_mags[day]) / len(daily_mags[day]) for day in sorted_days]

print(f"Reduced to {len(daily_avg_mag)} daily averaged points")

max_mag = max(daily_avg_mag)

sample_rate = 44100
note_duration = 0.15  # now uniform, since each note = one real day, evenly spaced
full_wave = np.array([])

for mag in daily_avg_mag:
    brightness = max_mag - mag
    frequency = 200 + (brightness * 100)
    t = np.linspace(0, note_duration, int(sample_rate * note_duration), endpoint=False)
    note = np.sin(2 * np.pi * frequency * t)
    full_wave = np.concatenate([full_wave, note])

write("mira_symphony_daily.wav", sample_rate, full_wave.astype(np.float32))
print("Done! Check your folder for mira_symphony_daily.wav")