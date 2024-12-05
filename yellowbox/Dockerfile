# Set base image
FROM python:3.12-alpine

# Install required system dependencies
RUN apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    mariadb-connector-c-dev \
    mariadb-dev

# By default, listen on port 5000
EXPOSE 5000/tcp

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the application source files
COPY app /app/app
COPY config.py . 
COPY flasky.py . 

# Specify the command to run on container start
CMD ["python", "./flasky.py"]
