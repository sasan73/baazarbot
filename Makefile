# Define the image name
IMAGE_NAME=baazarbot
IMAGE_TAG=latest

# Declare phony targets
.PHONY: install-dependancies build-docker clean

# Install dependencies
install-dependancies:
	@echo "Installing dependencies using Poetry..."
	poetry install

# Build the Docker image
build-docker:
	@echo "Building Docker image..."
	docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .

# clean up container and image
clean:
	docker rm -f ${IMAGE_NAME} || true
	docker rmi ${IMAGE_NAME}:${IMAGE_TAG} || true
