FROM python:3.11-slim

ARG GECKODRIVER_VERSION=v0.34.0

# Install necessary packages for Firefox and geckodriver
RUN apt-get update && \
    apt-get install -y firefox-esr wget curl && \
    rm -rf /var/lib/apt/lists/*

# Download and install geckodriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VERSION}/geckodriver-${GECKODRIVER_VERSION}-linux-aarch64.tar.gz && \
    tar -xvzf geckodriver-${GECKODRIVER_VERSION}-linux-aarch64.tar.gz && \
    mv geckodriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/geckodriver && \
    rm geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy your app code into the container
COPY . /app

# Set the working directory
WORKDIR /app

# Expose the port your app runs on
EXPOSE 8000

# Define the health check using the custom script
HEALTHCHECK --interval=150s --timeout=10s --start-period=60s CMD /app/agent_healthcheck.sh || kill -9 1

# Start the app
CMD ["python", "-u", "main.py"]
