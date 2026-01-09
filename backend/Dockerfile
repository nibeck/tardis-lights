FROM python:3.11-slim

# Install SoX for audio playback and packages to connect to the host's PulseAudio server
RUN apt-get update && apt-get install -y gcc python3-dev git sox libsox-fmt-mp3 libsox-fmt-pulse libsox-fmt-alsa pulseaudio-utils && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY test_leds_rpi.py .
COPY sounds ./sounds

CMD ["python", "-Xfrozen_modules=off", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]