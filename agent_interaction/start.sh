#!/bin/bash

# Start virtual display
Xvfb $DISPLAY -screen 0 $RESOLUTION &
sleep 2

# Start window manager
fluxbox &
sleep 1

# Start VNC server (no password for dev use)
x11vnc -display $DISPLAY -forever -nopw -shared -rfbport $VNC_PORT &
sleep 1

# Start noVNC (web-based VNC client)
websockify --web /usr/share/novnc/ $NOVNC_PORT localhost:$VNC_PORT &
sleep 1

# Launch 4diac IDE
/opt/4diac/4diac-ide -data /root/workspace &

echo "=== 4diac IDE is running ==="
echo "VNC:    localhost:$VNC_PORT"
echo "noVNC:  http://localhost:$NOVNC_PORT/vnc.html"

# Keep container alive
wait
