# This is the content for the 'Dockerfile' in your root folder.
# It packages your Python script and its dependencies into a Docker image.

# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install the dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Google Cloud credentials file and the ETL script
COPY cultiveconnect-fc0aa870574b.json .
COPY etl-cafeteros.py .

# Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
# This variable tells the google-cloud-storage library where to find the key
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/cultiveconnect-fc0aa870574b.json

# The command to run the script when the container starts
CMD ["python", "etl-cafeteros.py"]