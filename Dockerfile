# Use the official Python base image
FROM python:3.11-slim

# Set the current working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files securely into the container
COPY . .

# Expose port 80 (Azure Web App for Containers maps external traffic to port 80 by default)
EXPOSE 80

# Startup command specifying Uvicorn to run the FastAPI app natively on port 80
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "80"]
