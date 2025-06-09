FROM python:3.10-slim

# System dependencies for PySide6 and X11
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libegl1-mesa \
    libegl1-mesa-dev \
    libgles2-mesa-dev \
    libx11-6 \
    libxext6 \
    libxrender1 \
    libxkbcommon0 \
    libxkbcommon-x11-0 \
    libxcomposite1 \
    libxrandr2 \
    libxfixes3 \
    libxi6 \
    libxtst6 \
    libxcursor1 \
    libxdamage1 \
    libnss3 \
    libasound2 \
    libdbus-1-3 \
    libxss1 \
    libfontconfig1 \
    libfreetype6 \
    libglib2.0-0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    x11-utils \
    libxcb-cursor0 \
    libfontconfig1 \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app code
COPY  . .

# Create a startup script for debugging
RUN echo '#!/bin/bash\n\
echo "Container started..."\n\
echo "DISPLAY: $DISPLAY"\n\
echo "Testing X11 connection..."\n\
xdpyinfo -display $DISPLAY || echo "X11 connection failed"\n\
echo "Starting Python application..."\n\
python main.py' > start.sh && chmod +x start.sh

CMD ["bash", "start.sh"]