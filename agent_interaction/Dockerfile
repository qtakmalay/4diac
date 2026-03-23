FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV DISPLAY=:1
ENV VNC_PORT=5900
ENV NOVNC_PORT=6080
ENV RESOLUTION=1920x1080x24

# Install dependencies
RUN apt-get update && apt-get install -y \
    openjdk-17-jre \
    wget \
    xvfb \
    x11vnc \
    fluxbox \
    novnc \
    websockify \
    dbus-x11 \
    libgtk-3-0 \
    libswt-gtk-4-jni \
    libwebkit2gtk-4.0-37 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Download and install 4diac IDE 3.0.2
RUN wget -q "https://www.eclipse.org/downloads/download.php?file=/4diac/releases/3.0/4diac-ide/4diac-ide_3.0.2-linux.gtk.x86_64.tar.gz&r=1" \
    -O /tmp/4diac-ide.tar.gz \
    && mkdir -p /opt/4diac \
    && tar -xzf /tmp/4diac-ide.tar.gz -C /opt/4diac --strip-components=1 \
    && rm /tmp/4diac-ide.tar.gz \
    && chmod +x /opt/4diac/4diac-ide

# Create workspace with sample project
RUN mkdir -p /root/workspace

# Create startup script
COPY start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 5900 6080

CMD ["/start.sh"]
