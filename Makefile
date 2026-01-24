# --- Configuration Variables ---
# Change these if your project name or ports change
IMAGE_BACKEND = tardis-lights-backend
IMAGE_FRONTEND = tardis-lights-frontend
VERSION = latest
APP_PORT_BACKEND = 8000
APP_PORT_FRONTEND = 3000
BUILD_ID = $(shell git rev-parse --short HEAD 2>/dev/null || echo "unknown")
BUILD_DATE = $(shell date -u +"%Y-%m-%dT%H:%M:%SZ")
ENABLE_DEBUGGER = False


# --- Raspberry Pi Details ---
PI_USER = pi
PI_HOST = tardis.local
REGISTRY_PORT = 5001
# NOTE: This command is for macOS. For Linux, use: $(shell hostname -I | awk '{print $$1}')
MAC_IP = $(shell ipconfig getifaddr en0)
#MAC_IP = 192.168.1.209

# --- Derived Variables (Do not edit) ---
REGISTRY_URL = localhost:$(REGISTRY_PORT)
FULL_IMAGE_BACKEND = $(REGISTRY_URL)/$(IMAGE_BACKEND):$(VERSION)
FULL_IMAGE_FRONTEND = $(REGISTRY_URL)/$(IMAGE_FRONTEND):$(VERSION)

# .PHONY tells Make that these are commands, not files
.PHONY: all build push deploy logs start-registry test-local stop-local get-schema build-api push-api deploy-api

# Default target: Run everything in order
all: deploy

# Optional: Start registry on Mac if not running
start-registry:
	@echo "--- 🏁 Starting Registry on Mac ---"
	docker start registry 2>/dev/null || docker run -d -p $(REGISTRY_PORT):5000 --name registry --restart unless-stopped registry:2

# Step 1: Build the images on your Mac
build:
	@echo "--- 🏗️   Building Images ---"
	DOCKER_DEFAULT_PLATFORM=linux/arm64 docker-compose build --build-arg BUILD_ID=$(BUILD_ID) --build-arg BUILD_DATE=$(BUILD_DATE)
	@echo "--- 🏷️   Tagging Images for Registry ---"
	docker tag $(IMAGE_BACKEND):$(VERSION) $(FULL_IMAGE_BACKEND)
	docker tag $(IMAGE_FRONTEND):$(VERSION) $(FULL_IMAGE_FRONTEND)

# Step 1.5: Build only the backend
build-api:
	@echo "--- 🏗️   Building Backend Image ---"
	DOCKER_DEFAULT_PLATFORM=linux/arm64 docker-compose build --build-arg BUILD_ID=$(BUILD_ID) --build-arg BUILD_DATE=$(BUILD_DATE) backend
	@echo "--- 🏷️   Tagging Backend Image for Registry ---"
	docker tag $(IMAGE_BACKEND):$(VERSION) $(FULL_IMAGE_BACKEND)

# Step 2: Push the images to the Pi's Registry
push: build
	@echo "--- 🚀 Pushing to Registry at $(REGISTRY_URL) ---"
	docker push $(FULL_IMAGE_BACKEND)
	docker push $(FULL_IMAGE_FRONTEND)

# Step 2.5: Push only the backend
push-api: build-api
	@echo "--- 🚀 Pushing Backend to Registry at $(REGISTRY_URL) ---"
	docker push $(FULL_IMAGE_BACKEND)

# Step 3: Tell the Pi to pull, tag, and run with docker-compose
deploy: push start-registry
	@echo "--- 📡 Deploying to Raspberry Pi at $(PI_HOST) ---"
	ssh $(PI_USER)@$(PI_HOST) "mkdir -p ~/nginx"
	scp docker-compose.yml $(PI_USER)@$(PI_HOST):~/docker-compose.yml
	scp nginx/default.conf $(PI_USER)@$(PI_HOST):~/nginx/default.conf
	ssh $(PI_USER)@$(PI_HOST) "docker pull $(MAC_IP):$(REGISTRY_PORT)/$(IMAGE_BACKEND):$(VERSION) && \
	docker pull $(MAC_IP):$(REGISTRY_PORT)/$(IMAGE_FRONTEND):$(VERSION) && \
	docker tag $(MAC_IP):$(REGISTRY_PORT)/$(IMAGE_BACKEND):$(VERSION) $(IMAGE_BACKEND):$(VERSION) && \
	docker tag $(MAC_IP):$(REGISTRY_PORT)/$(IMAGE_FRONTEND):$(VERSION) $(IMAGE_FRONTEND):$(VERSION) && \
	docker compose down && ENABLE_DEBUGGER=$(ENABLE_DEBUGGER) docker compose up -d"
	@echo "--- ✅ Deployment Complete! ---"
	@echo "View App:      http://$(PI_HOST) (frontend)"
	@echo "View Backend:  http://$(PI_HOST) (backend)"

# Step 3.5: Deploy only the backend
deploy-api: push-api start-registry
	@echo "--- 📡 Deploying Backend to Raspberry Pi at $(PI_HOST) ---"
	scp docker-compose.yml $(PI_USER)@$(PI_HOST):~/docker-compose.yml
	ssh $(PI_USER)@$(PI_HOST) "docker pull $(MAC_IP):$(REGISTRY_PORT)/$(IMAGE_BACKEND):$(VERSION) && \
	docker tag $(MAC_IP):$(REGISTRY_PORT)/$(IMAGE_BACKEND):$(VERSION) $(IMAGE_BACKEND):$(VERSION) && \
	ENABLE_DEBUGGER=$(ENABLE_DEBUGGER) docker compose up -d --no-deps backend"
	@echo "--- ✅ Backend Deployment Complete! ---"

# Helper: View logs of the running services on the Pi
logs:
	ssh $(PI_USER)@$(PI_HOST) "docker compose logs -f"

# Fetch the OpenAPI schema from the running Raspberry Pi instance
get-schema:
	@echo "--- 📥 Fetching OpenAPI Schema from $(PI_HOST) ---"
	curl -o openapi.json http://$(PI_HOST)/openapi.json
	@echo "✅ Schema saved to openapi.json"

# Local test: Run containers on Mac for testing
test-local: build
	@echo "--- 🧪 Testing Locally on Mac ---"
	docker compose up -d
	@echo "Frontend: http://localhost"
	@echo "Backend: http://localhost"
	@echo "Run 'make stop-local' to stop"

# Stop local test
stop-local:
	docker compose down