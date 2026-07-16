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

# Sort by date -- now we keep JD and mag paired together
paired = sorted(zip(jd_values, mag_values))
jd_values = [j for j, _ in paired]
mag_values = [m for _, m in paired]
gaps = [jd_values[i] - jd_values[i-1] for i in range(1, len(jd_values))]
print(f"Smallest gap: {min(gaps):.4f} days")
print(f"Largest gap: {max(gaps):.4f} days")
print(f"Average gap: {sum(gaps)/len(gaps):.4f} days")

max_mag = max(mag_values)

sample_rate = 44100
full_wave = np.array([])

# Settings to control how "gaps" translate to sound length
min_note_len = 0.03   # shortest a note can ever be (seconds)
max_note_len = 0.3    # longest a note can ever be (seconds), so huge gaps don't create silence forever

for i in range(len(mag_values)):
    mag = mag_values[i]
    brightness = max_mag - mag
    frequency = 200 + (brightness * 100)

    if i == 0:
        gap_days = 0.1  # first note has no "previous" gap, so just use a small default
    else:
        gap_days = jd_values[i] - jd_values[i - 1]

    # Squeeze the real-world gap (which could be tiny or huge) into our note-length range
    note_duration = min_note_len + min(gap_days, 5) / 5 * (max_note_len - min_note_len)

    t = np.linspace(0, note_duration, int(sample_rate * note_duration), endpoint=False)
    note = np.sin(2 * np.pi * frequency * t)
    full_wave = np.concatenate([full_wave, note])

write("mira_symphony_timed.wav", sample_rate, full_wave.astype(np.float32))
print("Done! Check your folder for mira_symphony_timed.wav")