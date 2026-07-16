import numpy as np
from scipy.io.wavfile import read, write

# Load all three tracks
sr1, mira = read("mira_symphony_daily.wav")
sr2, pulsar = read("crab_pulsar.wav")
sr3, exoplanet = read("exoplanet_transit.wav")

mira = mira.astype(np.float32)
pulsar = pulsar.astype(np.float32)
exoplanet = exoplanet.astype(np.float32)

# Mira is likely the longest track -- use it as our target length
target_length = len(mira)

def loop_to_length(sound, length):
    if len(sound) < length:
        repeats = int(np.ceil(length / len(sound)))
        sound = np.tile(sound, repeats)
    return sound[:length]

pulsar = loop_to_length(pulsar, target_length)
exoplanet = loop_to_length(exoplanet, target_length)

# Volume balance for each layer -- tweak these numbers to taste
mira_volume = 0.7       # the melody -- should be prominent
pulsar_volume = 0.2     # rhythmic texture -- sits underneath
exoplanet_volume = 0.4  # steady tone with dips -- adds atmosphere

mixed = (mira * mira_volume) + (pulsar * pulsar_volume) + (exoplanet * exoplanet_volume)

# Prevent distortion from combined volume being too loud
max_val = np.max(np.abs(mixed))
if max_val > 1.0:
    mixed = mixed / max_val

write("celestial_symphony_full.wav", sr1, mixed.astype(np.float32))
print("Done! Check your folder for celestial_symphony_full.wav")