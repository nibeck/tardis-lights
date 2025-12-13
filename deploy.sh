#!/bin/bash

# Build and deploy to Raspberry Pi using local Docker registry
# Assumes rPi IP is set, SSH key is configured, and RPi can reach Mac's IP

RPI_IP="192.168.1.161"  # Replace with actual IP
REGISTRY_PORT=5000
MAC_IP="192.168.1.214"

# Start local registry if not running
if ! docker ps | grep -q registry; then
    docker run -d -p $REGISTRY_PORT:5000 --name registry registry:2
fi

# Build images locally
docker-compose build

# Tag and push images to local registry
docker tag tardis-lights-backend localhost:$REGISTRY_PORT/tardis-lights-backend
docker tag tardis-lights-frontend localhost:$REGISTRY_PORT/tardis-lights-frontend
docker push localhost:$REGISTRY_PORT/tardis-lights-backend
docker push localhost:$REGISTRY_PORT/tardis-lights-frontend

# Copy docker-compose.yml to rPi
scp docker-compose.yml pi@$RPI_IP:~/

# On rPi, pull images and run
ssh pi@$RPI_IP << EOF
docker pull $MAC_IP:$REGISTRY_PORT/tardis-lights-backend
docker pull $MAC_IP:$REGISTRY_PORT/tardis-lights-frontend
docker tag $MAC_IP:$REGISTRY_PORT/tardis-lights-backend tardis-lights-backend
docker tag $MAC_IP:$REGISTRY_PORT/tardis-lights-frontend tardis-lights-frontend
docker-compose up -d
EOF

echo "--- ✅ Deployment Complete! ---"
echo "View App:      http://$RPI_IP:3000 (frontend) and http://$RPI_IP:8000 (backend)"