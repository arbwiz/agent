FROM python:3.11-slim

# Install necessary packages for Firefox and geckodriver
RUN apt-get update && \
    apt-get install -y firefox-esr wget && \
    rm -rf /var/lib/apt/lists/*

# Download and install geckodriver
RUN GECKODRIVER_VERSION=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest | grep 'tag_name' | cut -d\" -f4) && \
    wget https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz && \
    tar -xvzf geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz && \
    mv geckodriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/geckodriver && \
    rm geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz

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
