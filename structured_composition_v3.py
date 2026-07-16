import numpy as np
from scipy.io.wavfile import read, write

sr1, mira = read("mira_scaled.wav")
sr2, pulsar = read("crab_pulsar.wav")
sr3, exoplanet = read("exoplanet_transit.wav")
sr4, halley = read("halley_journey_melodic.wav")

print(f"Mira length: {len(mira)/sr1:.1f} seconds")
print(f"Halley length: {len(halley)/sr4:.1f} seconds")

mira = mira.astype(np.float32)
pulsar = pulsar.astype(np.float32)
exoplanet = exoplanet.astype(np.float32)
halley = halley.astype(np.float32)

# Since Halley's piece is a full "journey" that likely runs longer than Mira,
# let's make Halley's length the new target -- everything else loops to fit it
buildup_length = len(mira)  # the first section length, based on Mira's natural length
target_length = buildup_length + len(halley)  # total = buildup, THEN Halley's finale

def loop_to_length(sound, length):
    if len(sound) < length:
        repeats = int(np.ceil(length / len(sound)))
        sound = np.tile(sound, repeats)
    return sound[:length]

mira = loop_to_length(mira, buildup_length)
pulsar = loop_to_length(pulsar, buildup_length)
exoplanet = loop_to_length(exoplanet, buildup_length)

# Pad all three buildup layers with silence for the Halley section that follows
mira = np.concatenate([mira, np.zeros(len(halley))])
pulsar = np.concatenate([pulsar, np.zeros(len(halley))])
exoplanet = np.concatenate([exoplanet, np.zeros(len(halley))])

# Halley plays ONLY during the finale section, silent during the buildup
halley_full = np.concatenate([np.zeros(buildup_length), halley])
sample_rate = sr1

def fade_in_envelope(length, start_sample, fade_length):
    envelope = np.zeros(length)
    fade_end = min(start_sample + fade_length, length)
    if start_sample < length:
        envelope[start_sample:fade_end] = np.linspace(0, 1, fade_end - start_sample)
        envelope[fade_end:] = 1.0
    return envelope

def fade_out_envelope(length, end_sample, fade_length):
    """Fades volume DOWN to zero, ending at end_sample."""
    envelope = np.ones(length)
    fade_start = max(end_sample - fade_length, 0)
    if fade_start < length:
        envelope[fade_start:end_sample] = np.linspace(1, 0, end_sample - fade_start)
        envelope[end_sample:] = 0.0
    return envelope

quarter = target_length // 4
fade_length = sample_rate * 3

mira_envelope = np.ones(target_length)
pulsar_envelope = fade_in_envelope(target_length, quarter, fade_length)
exoplanet_envelope = fade_in_envelope(target_length, quarter * 2, fade_length)

# As Halley's finale begins, gently fade the other three layers OUT,
# so Halley's journey gets to stand alone for its climax
fade_others_out = fade_out_envelope(target_length, buildup_length + int(sample_rate * 2), fade_length)

mira_volume = 0.7
pulsar_volume = 0.2
exoplanet_volume = 0.4
halley_volume = 0.8

mixed = (mira * mira_volume * mira_envelope * fade_others_out) + \
        (pulsar * pulsar_volume * pulsar_envelope * fade_others_out) + \
        (exoplanet * exoplanet_volume * exoplanet_envelope * fade_others_out) + \
        (halley_full * halley_volume)

max_val = np.max(np.abs(mixed))
if max_val > 1.0:
    mixed = mixed / max_val

write("celestial_symphony_v3_FINAL.wav", sample_rate, mixed.astype(np.float32))
print("Done! Check your folder for celestial_symphony_v3_FINAL.wav")