#!/bin/bash

# Variables
IMAGE_NAME="arpansahu_dot_me_mac"
HARBOR_URL="harbor.arpansahu.me/library"
LOCAL_IMAGE="arpansahu_dot_me"
TAG="latest"
KUBE_DEPLOYMENT="arpansahu-dot-me-app-mac"
NAMESPACE="default"
SECRET_NAME="arpansahu-dot-me-secret"
ENV_FILE=".env"
SERVICE_FILE="service.yaml"
DEPLOYMENT_FILE="deployment-mac.yaml"
HARBOR_USERNAME="admin"
HARBOR_PASSWORD="harborKesar302@"

# Function to print error message and exit
function error_exit {
    echo "$1" 1>&2
    exit 1
}

# Step 1: Build the Docker image locally
echo "Building Docker image..."
sudo docker build -t ${LOCAL_IMAGE}:${TAG} . || error_exit "Failed to build Docker image."

# Step 2: Tag the Docker image for Harbor
echo "Tagging Docker image..."
sudo docker tag ${LOCAL_IMAGE}:${TAG} ${HARBOR_URL}/${IMAGE_NAME}:${TAG} || error_exit "Failed to tag Docker image."

# Step 3: Log in to Harbor
echo "Logging in to Harbor..."
echo ${HARBOR_PASSWORD} | docker login ${HARBOR_URL} --username ${HARBOR_USERNAME} --password-stdin || error_exit "Failed to log in to Harbor."

# Step 4: Push the Docker image to Harbor
echo "Pushing Docker image to Harbor..."
sudo docker push ${HARBOR_URL}/${IMAGE_NAME}:${TAG} || error_exit "Failed to push Docker image to Harbor."

# Step 5: Delete the existing Kubernetes secret (if it exists) and create a new one
echo "Deleting existing Kubernetes secret (if it exists)..."
kubectl delete secret ${SECRET_NAME} -n ${NAMESPACE} --ignore-not-found

echo "Creating Kubernetes secret..."
kubectl create secret generic ${SECRET_NAME} --from-env-file=${ENV_FILE} -n ${NAMESPACE} || error_exit "Failed to create Kubernetes secret."

# Step 6: Apply the service configuration
echo "Applying service configuration..."
kubectl apply -f ${SERVICE_FILE} -n ${NAMESPACE} || error_exit "Failed to apply service configuration."

# Step 7: Apply the new deployment configuration
echo "Applying deployment configuration..."
kubectl apply -f ${DEPLOYMENT_FILE} -n ${NAMESPACE} || error_exit "Failed to apply deployment configuration."

echo "Deployment updated successfully!"

# Verify the updated deployment
kubectl rollout status deployment/${KUBE_DEPLOYMENT} -n ${NAMESPACE} || error_exit "Failed to rollout Kubernetes deployment."

echo "Deployment rolled out successfully!"