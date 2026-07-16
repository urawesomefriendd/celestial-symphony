import numpy as np
from scipy.io.wavfile import write

# Real data from the Crab Pulsar (J0534+2200)
frequency_hz = 29.9469230  # spins per second, from real ATNF catalog data
duration = 5  # seconds of sound to generate

sample_rate = 44100
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# Create a series of sharp "clicks" at the pulsar's real spin rate,
# instead of a smooth sine wave, to sound more like a pulse than a tone
click_wave = (np.sin(2 * np.pi * frequency_hz * t) > 0.99).astype(np.float32)

write("crab_pulsar.wav", sample_rate, click_wave)
print("Done! Check your folder for crab_pulsar.wav")