I built a python-based pipeline that takes astronomical data from celestial objects and turns each one into sound. Each object’s data is different in shape and meaning so a different mapping method for each was used.

1. Mira  
- Using real brightness measurements from the AAVSO database, spanning about 500 days, I converted each day’s average brightness into a musical tone.   
- Brighter days were higher notes, using an A minor scale so the melody would sound more intentional. This was the main melody of the piece.

2. The Crab Pulsar   
- Its real measured spin frequency was about 30 rotations per second (from ATNF Pulsar Catalogue). Using that, I generated a fast buzzing rhythmic layer in the piece. The pulsar really is a rapidly spinning neutron star sweeping a radio beam past Earth like a lighthouse.

3. Kepler-10 b (exoplanet)   
- Using its real orbital period and transit depth from NASA’s Exoplanet Archive,  generated a steady tone that briefly dims in volume every time the planet would cross in front of its stars. It repeated on the planet’s actual orbital rhythm (compressed from about 20 real hours into a 2-second loop). 

4. Halley’s Comet   
- I did this with a different approach entirely since there was no continuous observational data converting the full 76-year orbit. It’s invisible for most of that time. Instead, I used its real orbital elements such as eccentricity and semi major axis from JPL’s small-body database and applied it to Kepler’s Equation along with the vis-viva equation to calculate its distance and speed from the sun at any point in its orbit. Then I sonified that calculated journey using a Lydian scale and mapped its real orbital speed to the tempo of the notes.

All four layers are mixed and structured into one piece that builds up over time. It starts with Mira alone, adding the pulsar and exoplanet, then transitioning into Halley’s solo journey as a finale. The piece is also synced with visual animations of all three closer objects, combined into one final video. 

**Key Decisions and Why I Made Them**

Brightness to Pitch (Mira) 

- I mapped a star’s brightness to musical pitch because it felt like the most intuitive or natural connection and furthermore it’s what NASA also did with some of their sonifications. A brighter moment or feeling as a higher note is how most people would think about light and sound intensity. It’s a simplification since real astronomers wouldn’t say brightness and pitch are physically related, but it’s an honest, clearly stated artistic choice rather than something I claimed was scientifically necessary.   
- 

Daily Averaging instead of Raw Observations (Mira) 

- My first version used every single observation but with around 960 data points from many different observers. Most of them clustered within hours of each other and the result was noisy and didn’t clearly reflect Mira’s actual around 332 day brightness cycle. Averaging to one value per day cut this down to 263 clean points and made the real cycle audible. This taught me that raw data usually needs to be cleaned or processed before it reveals a genuine pattern. 

Calculating Halley’s Orbit instead of downloading data 

- Unlike mira, there was no continuous observational record covering Halley’s Comet across its full 76-year orbit. It was simply too faint to observe for most of the time. Instead of downloading a dataset, I used its real orbital elements from JPL’s Small-Body Database. This is a different and arguably more advanced approach than the rest of the project. It’s closer to what real astronomers do when direct observation isn’t possible.

Logarithmic Brightness Scaling (Halley) 

- When I first sonified Halley’s calculated brightness, almost the entire piece sounded flat. It was one sharp spike near the sun and then a near-total silence everywhere else. This turned out to be an honest reflection of real physics. Halley’s brightness changes so extremely across its orbit that a direct and linear mapping made everything except the very peak indiscernible. I fixed this by applying a logarithmic scale. Compressing extreme ranges logarithmically is standard scientific practice, not something I invented for convenience.

Different musical scales for different objects

- I used an A minor scale for Mira that’s more of a familiar and moody sound for a star that has a well-documented and repeated cycle. For Halley’s journey, I used the lydian scale to make it sound brighter and dreamier just to try it out. This was a deliberate creative choice to give each object its own musical identity, rather than using one identical mapping for everything. 


Structuring the piece to build over time

- Rather than playing all four layers at once from the very beginning, I structured the composition to start sparsely with Mira alone, and gradually add the pulsar and exoplanet, then transition into Halley’s journey as a solo finale. This mirrors how real life musical compositions are structured and it also happens to mirror the real difference between the three closer, more “constant” objects and Halley’s rare, dramatic appearance. 

**Problems I Ran Into (and How I Solved Them)**

- The Mira noise problem. My first working version of Mira's sonification used every single observation in the dataset with about 960 data points. It technically worked, but it sounded busy and chaotic, without any clear sense of Mira's actual \~332 day brightness cycle coming through. At first I assumed the timing itself was the problem, so I tried adjusting note lengths based on the real gaps between observations but that barely changed anything. When I actually printed out the gap statistics, I found the real issue: most observations were happening within hours of each other while only a few gaps were large. This meant almost all my "notes" were nearly identical in timing, drowning out any real variation.  
    
- The fix was to average all observations from the same day into a single value, cutting \~960 noisy points down to 263 clean daily averages. The difference was dramatic and Mira's actual rise and fall cycle became clearly audible for the first time. This was the moment I really understood that raw real world data is often too noisy to reveal its own pattern, and that cleaning and processing is a necessary and honest part of working with real data.

The Halley Overlap Bug

- When I first combined Halley’s finale with the rest of the piece, I built the timeline so all four layers shared the same exact time instead of playing one another. Because Halley’s track happened to be longer than the build-up section it caused Halley to start playing from the very beginning which caused it to be buried underneath everything else. My planned finale wasn’t actually landing as one. The fix was restructuring the code to explicitly place Halley’s audio after the buildup section ends, rather than just assuming everything automatically fit each other. 

The Halley flatness problem

- My first calculated version of Halley’s journey sounded like a constant and single quiet hum rather than something dynamic. By printing out the actual brightness value, it revealed that Halley’s real orbital brightness is so extreme \- nearly all darkness with a brief and sharp peak \-  that a direct and linear mapping made almost every note nearly identical. Applying a logarithmic scale fixed this problem and let the journey’s shape finally come through. 

**What Surprised Me**

The thing that surprised me most was just how dramatic and extreme a comet’s brightness change actually is. Before this project, I knew that comets got brighter near the sun but I didn’t appreciate how extreme that swing really is. Halley’s calculated brightness was so overwhelmingly concentrated in one brief peak that my first sonification attempt was essentially silent except for a single spike. 

**What I’d Still Like to Improve**

- The most important thing left to improve is making Halley’s layer sound genuinely polished and finished. Right now it’s a solid proof of concept with real orbital mechanics driving real musical choices but it still has some rough edges in how it’s mixed into the full piece. My next step is to keep refining it by testing different scales, tempos, and mixing balances until it feels as intentional and complete as the rest of the piece. It’s still improving with the way it sounds and it definitely could be a better musical piece but I believe it is good for what it is. 

