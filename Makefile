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

zenml-init:
	@echo "initializing zenml in root directory..."
	poetry run zenml init

zenml-up: zenml-init
	@echo "Spinning Zenml up..."
	poetry run zenml login --local

run-generate-instruct-datasets: install-dependancies
	poetry run python tools/run.py \
	--run-generate-instruct-datasets \
	--no-cache

# Run etl pipeline
run-digital-data-etl: build-docker
	@echo "Running Digital Data ETL..."
	docker run --rm \
		--network host \
		--shm-size=2g \
		--env-file .env \
		${IMAGE_NAME} \
		poetry run main \
		--run-etl \
		--etl-config-filename="digital_data_etl.yaml"

# clean up container and image
clean:
	docker rm -f ${IMAGE_NAME} || true
	docker rmi ${IMAGE_NAME}:${IMAGE_TAG} || true
