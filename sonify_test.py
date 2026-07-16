import numpy as np
from scipy.io.wavfile import write

# Settings for our sound
sample_rate = 44100  # how many "snapshots" of sound per second (CD quality)
duration = 2          # length of the sound, in seconds
frequency = 440       # pitch, in Hz (440 = the musical note A)

# Create a time array: a list of tiny time steps across our 2 seconds
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# Generate a sine wave at our chosen frequency
wave = np.sin(2 * np.pi * frequency * t)

# Save it as a .wav file
write("test_tone.wav", sample_rate, wave.astype(np.float32))

print("Done! Check your folder for test_tone.wav")