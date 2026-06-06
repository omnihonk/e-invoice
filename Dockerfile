# Use standard Python 3.12 slim image
FROM python:3.12-slim

# Prevent python from writing pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies for WeasyPrint, Java download, and fonts
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    tar \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libharfbuzz0b \
    libjpeg62-turbo \
    libopenjp2-7 \
    libffi-dev \
    shared-mime-info \
    fontconfig \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# Download and install OpenJDK JRE 21 via Adoptium API
RUN mkdir -p /opt/openjdk && \
    curl -L "https://api.adoptium.net/v3/binary/latest/21/ga/linux/x64/jre/hotspot/normal/eclipse" | \
    tar -xzf - --strip-components=1 -C /opt/openjdk

# Add OpenJDK to PATH
ENV JAVA_HOME=/opt/openjdk
ENV PATH="${JAVA_HOME}/bin:${PATH}"


# Pre-download Mustang-CLI-2.23.0.jar (saved outside /app/data to avoid volume shadowing)
RUN mkdir -p /app && \
    curl -L -o /app/Mustang-CLI-2.23.0.jar https://repo1.maven.org/maven2/org/mustangproject/Mustang-CLI/2.23.0/Mustang-CLI-2.23.0.jar

# Set working directory
WORKDIR /app

# Install python dependencies
COPY pyproject.toml /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir .

# Copy application source files
COPY . /app/

# Create data directory for volume mount
RUN mkdir -p /app/data

# Run the FastAPI server
EXPOSE 8765
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8765}"]
