import numpy as np
from scipy.io.wavfile import read, write

# Load both existing sound files
sample_rate1, mira = read("mira_symphony_daily.wav")
sample_rate2, pulsar = read("crab_pulsar.wav")

# Make sure both are float32 and in the same "loudness" range (-1 to 1)
mira = mira.astype(np.float32)
pulsar = pulsar.astype(np.float32)

# Since Mira's track is probably longer, we'll loop the pulsar
# clicks over and over until it matches Mira's length
target_length = len(mira)

if len(pulsar) < target_length:
    repeats = int(np.ceil(target_length / len(pulsar)))
    pulsar = np.tile(pulsar, repeats)  # repeat the pulsar clip end-to-end

pulsar = pulsar[:target_length]  # trim to exactly match Mira's length

# Adjust volumes -- pulsar clicks are naturally sharp/loud, so we turn it down
# relative to the melody so it sits underneath, not on top
mira_volume = 0.8
pulsar_volume = 0.3

mixed = (mira * mira_volume) + (pulsar * pulsar_volume)

# Prevent "clipping" (distortion from the combined volume being too loud)
max_val = np.max(np.abs(mixed))
if max_val > 1.0:
    mixed = mixed / max_val

write("celestial_symphony_v1.wav", sample_rate1, mixed.astype(np.float32))
print("Done! Check your folder for celestial_symphony_v1.wav")