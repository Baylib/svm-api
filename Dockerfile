# Use the Python image from quay.io
FROM python:latest

# Set the working directory inside the container
WORKDIR /app

# Copy the Python script and any required files into the container
COPY main.py .

# Install dependencies (if any)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080
EXPOSE 8080

# Specify the command to run the Python script
ENTRYPOINT ["python", "/app/main.py"]
