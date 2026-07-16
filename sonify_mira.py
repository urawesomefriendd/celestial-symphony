import csv
import numpy as np
from scipy.io.wavfile import write

jd_values = []
mag_values = []

with open("mira_data.csv", "r") as f:
    reader = csv.reader(f)
    next(reader)  # skip the header row (column names)
    for row in reader:
        try:
            jd = float(row[0])
            mag = float(row[1])
            jd_values.append(jd)
            mag_values.append(mag)
        except (ValueError, IndexError):
            continue  # skip any messy/broken rows

print(f"Loaded {len(mag_values)} real observations of Mira!")

# Sort by date, since real data isn't always in order
paired = sorted(zip(jd_values, mag_values))
mag_values = [m for _, m in paired]

# Turn brightness into pitch: brighter (LOWER mag number) = higher pitch
# So we flip it: subtract mag from a max value
max_mag = max(mag_values)
min_mag = min(mag_values)

sample_rate = 44100
note_duration = 0.05  # short notes since we have MANY data points
full_wave = np.array([])

for mag in mag_values:
    brightness = max_mag - mag  # flip so brighter = bigger number
    frequency = 200 + (brightness * 100)  # map brightness to pitch
    t = np.linspace(0, note_duration, int(sample_rate * note_duration), endpoint=False)
    note = np.sin(2 * np.pi * frequency * t)
    full_wave = np.concatenate([full_wave, note])

write("mira_symphony.wav", sample_rate, full_wave.astype(np.float32))
print("Done! Check your folder for mira_symphony.wav")