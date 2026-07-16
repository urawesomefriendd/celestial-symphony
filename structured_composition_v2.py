import numpy as np
from scipy.io.wavfile import read, write

sr1, mira = read("mira_scaled.wav")           # <-- using the new scaled version
sr2, pulsar = read("crab_pulsar.wav")
sr3, exoplanet = read("exoplanet_transit.wav")

mira = mira.astype(np.float32)
pulsar = pulsar.astype(np.float32)
exoplanet = exoplanet.astype(np.float32)

target_length = len(mira)

def loop_to_length(sound, length):
    if len(sound) < length:
        repeats = int(np.ceil(length / len(sound)))
        sound = np.tile(sound, repeats)
    return sound[:length]

pulsar = loop_to_length(pulsar, target_length)
exoplanet = loop_to_length(exoplanet, target_length)

sample_rate = sr1

def fade_in_envelope(length, start_sample, fade_length):
    envelope = np.zeros(length)
    fade_end = min(start_sample + fade_length, length)
    if start_sample < length:
        envelope[start_sample:fade_end] = np.linspace(0, 1, fade_end - start_sample)
        envelope[fade_end:] = 1.0
    return envelope

third = target_length // 3
fade_length = sample_rate * 3

mira_envelope = np.ones(target_length)
pulsar_envelope = fade_in_envelope(target_length, third, fade_length)
exoplanet_envelope = fade_in_envelope(target_length, third * 2, fade_length)

mira_volume = 0.7
pulsar_volume = 0.2
exoplanet_volume = 0.4

mixed = (mira * mira_volume * mira_envelope) + \
        (pulsar * pulsar_volume * pulsar_envelope) + \
        (exoplanet * exoplanet_volume * exoplanet_envelope)

max_val = np.max(np.abs(mixed))
if max_val > 1.0:
    mixed = mixed / max_val

write("celestial_symphony_v2.wav", sample_rate, mixed.astype(np.float32))
print("Done! Check your folder for celestial_symphony_v2.wav")