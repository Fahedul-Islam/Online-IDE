# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the script into the container
COPY script.py .

# Run the Python script
CMD ["python", "script.py"]
