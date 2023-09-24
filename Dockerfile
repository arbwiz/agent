FROM python:3.11-slim

# Install any dependencies your app needs
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy your app code into the container
COPY . /app

# Set the working directory
WORKDIR /app

# Expose the port your app runs on
EXPOSE 8000

# Start the app
CMD ["python", "-u" , "main.py"]