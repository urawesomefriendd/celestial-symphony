import numpy as np
from scipy.io.wavfile import read, write

sr1, mira = read("mira_scaled.wav")
sr2, pulsar = read("crab_pulsar.wav")
sr3, exoplanet = read("exoplanet_transit.wav")
sr4, halley = read("halley_journey_melodic.wav")

mira = mira.astype(np.float32)
pulsar = pulsar.astype(np.float32)
exoplanet = exoplanet.astype(np.float32)
halley = halley.astype(np.float32)

sample_rate = sr1
pause_length = int(sample_rate * 1.5)  # 1.5 second breath before Halley begins

buildup_length = len(mira)
target_length = buildup_length + pause_length + len(halley)

def loop_to_length(sound, length):
    if len(sound) < length:
        repeats = int(np.ceil(length / len(sound)))
        sound = np.tile(sound, repeats)
    return sound[:length]

mira = loop_to_length(mira, buildup_length)
pulsar = loop_to_length(pulsar, buildup_length)
exoplanet = loop_to_length(exoplanet, buildup_length)

# Pad buildup layers with silence through the pause AND the Halley section
silence_tail = np.zeros(pause_length + len(halley))
mira = np.concatenate([mira, silence_tail])
pulsar = np.concatenate([pulsar, silence_tail])
exoplanet = np.concatenate([exoplanet, silence_tail])

# Halley: silent through buildup + pause, then plays, with its own gentle fade-in
halley_fade_in_len = int(sample_rate * 2)  # 2-second fade-in on top of its existing note fades
halley_with_fade = halley.copy()
fade_curve = np.linspace(0, 1, halley_fade_in_len)
halley_with_fade[:halley_fade_in_len] *= fade_curve

halley_full = np.concatenate([np.zeros(buildup_length + pause_length), halley_with_fade])

def fade_out_envelope(length, end_sample, fade_length):
    envelope = np.ones(length)
    fade_start = max(end_sample - fade_length, 0)
    if fade_start < length:
        envelope[fade_start:end_sample] = np.linspace(1, 0, end_sample - fade_start)
        envelope[end_sample:] = 0.0
    return envelope

def fade_in_envelope(length, start_sample, fade_length):
    envelope = np.zeros(length)
    fade_end = min(start_sample + fade_length, length)
    if start_sample < length:
        envelope[start_sample:fade_end] = np.linspace(0, 1, fade_end - start_sample)
        envelope[fade_end:] = 1.0
    return envelope

quarter = buildup_length // 3
fade_length = sample_rate * 3

mira_envelope = np.ones(target_length)
pulsar_envelope = fade_in_envelope(target_length, quarter, fade_length)
exoplanet_envelope = fade_in_envelope(target_length, quarter * 2, fade_length)

# Fade the buildup out a bit EARLIER, so it finishes fading right as the pause begins
# -- this creates a soft overlap feeling rather than a hard cutoff
fade_others_out = fade_out_envelope(target_length, buildup_length, fade_length)

mira_volume = 0.7
pulsar_volume = 0.2
exoplanet_volume = 0.4
halley_volume = 0.9  # slightly louder since it plays alone -- deserves to feel like the climax

mixed = (mira * mira_volume * mira_envelope * fade_others_out) + \
        (pulsar * pulsar_volume * pulsar_envelope * fade_others_out) + \
        (exoplanet * exoplanet_volume * exoplanet_envelope * fade_others_out) + \
        (halley_full * halley_volume)

max_val = np.max(np.abs(mixed))
if max_val > 1.0:
    mixed = mixed / max_val

write("celestial_symphony_v4_polished.wav", sample_rate, mixed.astype(np.float32))
print("Done! Check your folder for celestial_symphony_v4_polished.wav")