import numpy as np
from scipy.io.wavfile import write

# Real data: Kepler-10 b (Bonomo et al. 2025 / Holczer et al. 2016)
period_days = 0.837491       # one orbit = 20 hours
transit_duration_hours = 1.81
transit_depth_percent = 0.0191

sample_rate = 44100
seconds_per_orbit = 2.0  # we'll compress each 20-hour orbit into 2 seconds of audio
num_orbits = 8            # how many repeats to generate
duration = seconds_per_orbit * num_orbits

t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# Base tone representing the star's steady brightness
base_frequency = 300
wave = np.sin(2 * np.pi * base_frequency * t)

# Figure out what fraction of each orbit is spent "in transit" (the dip)
transit_duration_days = transit_duration_hours / 24
transit_fraction = transit_duration_days / period_days  # fraction of orbit spent dipping

# Build a repeating volume dip at the right point in every orbit cycle
orbit_phase = (t % seconds_per_orbit) / seconds_per_orbit  # where we are in the current orbit (0 to 1)
in_transit = orbit_phase < transit_fraction

volume = np.ones_like(t)
volume[in_transit] -= 0.7  # exaggerated so it's audible -- represents the real dip, just amplified to be heard

wave = wave * volume

write("exoplanet_transit.wav", sample_rate, wave.astype(np.float32))
print("Done! Check your folder for exoplanet_transit.wav")