# Project Overview
**Project Name:** [TARDIS Lights]
**Core Value Proposition:** [An intercatiove LED controller applictaion to manage the lights in my TARDIS]

# Technology Stack
**Web Frontend:** [React]
**Backend:** [Python]
**API:** [FastAPI]
**Database:** [N/A at this point, I don't think I will need to save state info]
**Infrastructure/Deployment:** [Docker]
**CI/CD:** [manual deployment with shell scripts on Mac deploy to Docker ibn rPi]
**Clients:** [web UI from server] 
**hosts:** [Raspberry Pi]
**Other** [LED control framework for the Raspberry Pi]
**LEDs:** a long string of NeoPixels/ WS2812B LEDs connected to rPi5

# MVP Requirements (Skeleton)
**Goal:** [A simoply web UI that interacts with basic APIs to ensure proper connectiovity, etc. ]
**Must-Haves for v0.1:**
1. Basic web UI to ensure LEDs work and the APIs are running
2. Integration of Adafruit CircuitPython NeoPixel for LED control
3. A data structure that can manage a long string of NeoPixels/ WS2812B LEDs
4. Basic features to turn on/off string, set colors, pulse colors

**Future**
1. ios Swift UI app that integrates with APIs to control lights
2. More adcanced capabilities like splitting up the large LED string into multiple "logical" groupings to be able to control them seperately.
3. Ability to play sounds/music from the rPI