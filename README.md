# 🌌 Celestial Symphony: Mapping the Sounds of the Universe

Sonifying real astronomical data — turning a variable star, a pulsar, an exoplanet, and a comet into music, using real measurements from NASA, AAVSO, and JPL.

## About

This project explores **sonification**: converting real scientific data into sound. Rather than using fictional or simulated data, every layer of the final composition is generated from actual astronomical measurements or real orbital physics.

The full story of how this project was built — including the decisions, mistakes, and debugging along the way — is documented in [`celestial_symphony_journal.md`](./celestial_symphony_journal.md).

## The Four Celestial Objects

| Object | What it is | Data source | How it's sonified |
|---|---|---|---|
| **Mira (omi Cet)** | A variable star that cycles between bright and dim over ~332 days | [AAVSO](https://www.aavso.org/) — 962 real observations, averaged into 263 daily values | Brightness → pitch, on an A minor scale |
| **Crab Pulsar (PSR J0534+2200)** | A rapidly spinning neutron star from a supernova recorded in 1054 CE | [ATNF Pulsar Catalogue](https://www.atnf.csiro.au/research/pulsar/psrcat/) — real spin frequency (~30 Hz) | Real spin rate → rhythmic clicking texture |
| **Kepler-10 b** | A rocky exoplanet orbiting its star every ~20 hours | [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/) — real orbital period & transit depth | Orbital transit → periodic volume dip on a steady tone |
| **Halley's Comet (1P/Halley)** | A comet on a ~76-year elliptical orbit | [JPL Small-Body Database](https://ssd.jpl.nasa.gov/) — real orbital elements, position/speed calculated via Kepler's Equation & the vis-viva equation | Calculated brightness (log-scaled) → pitch on a Lydian scale; orbital speed → tempo |

## How It Works

1. **Data collection** — real data pulled from public astronomy archives (AAVSO, ATNF, NASA Exoplanet Archive, JPL)
2. **Cleaning/processing** — e.g. averaging noisy daily observations for Mira; solving Kepler's Equation numerically for Halley
3. **Sonification** — each dataset mapped to sound using Python (`numpy`, `scipy`), with a deliberate, explained mapping choice per object
4. **Composition** — layers mixed and structured to build over time, ending in Halley's solo "finale"
5. **Visualization** — synced animations (`matplotlib`) for the three closer objects
6. **Final output** — audio + visuals combined into one video (`ffmpeg`)

## Files

- `sonify_mira_daily.py`, `sonify_pulsar.py`, `sonify_exoplanet.py`, `sonify_halley_melodic.py` — individual sonification scripts
- `structured_composition_v4.py` — combines and structures all four layers into the final piece
- `visualize_all_three.py` — animated visuals for Mira, the pulsar, and the exoplanet
- `celestial_symphony_v4_polished.wav` — final audio
- `celestial_symphony_FINAL.mp4` — final audio + visuals combined
- `celestial_symphony_journal.md` — full project reflection: decisions, problems solved, and what I'd still improve

## Data Sources & Credit

- Star brightness data: [AAVSO International Database](https://www.aavso.org/)
- Pulsar data: [ATNF Pulsar Catalogue](https://www.atnf.csiro.au/research/pulsar/psrcat/), CSIRO
- Exoplanet data: [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/), operated by Caltech/JPL under contract with NASA
- Comet orbital data: [JPL Small-Body Database](https://ssd.jpl.nasa.gov/), NASA/JPL-Caltech

## Inspiration

This project was inspired by NASA's own data sonification work, including their exoplanet discovery sonification. My goal was to apply the same honest and data-driven approach across several very different kinds of astronomical data with each requiring its own scientifically grounded mapping method.
