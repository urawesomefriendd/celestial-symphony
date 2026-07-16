import numpy as np
from scipy.io.wavfile import write

# Pretend this is "data" -- like brightness readings from a star over time
data = [1, 1, 1, 8, 8, 8, 1, 1, 1]

sample_rate = 44100
note_duration = 0.3  # each number becomes a 0.3 second note

full_wave = np.array([])  # this will hold our whole song, built piece by piece

for value in data:
    frequency = 200 + (value * 50)  # turn the number into a pitch
    t = np.linspace(0, note_duration, int(sample_rate * note_duration), endpoint=False)
    note = np.sin(2 * np.pi * frequency * t)
    full_wave = np.concatenate([full_wave, note])  # stick this note onto the end

write("data_melody.wav", sample_rate, full_wave.astype(np.float32))
print("Done! Check your folder for data_melody.wav")