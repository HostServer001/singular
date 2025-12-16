#!/bin/bash

# Create venv path
VENV_PATH="/home/$(whoami)/pro_py"

# Create venv if not exists
if [ ! -d "$VENV_PATH" ]; then
    python3 -m venv "$VENV_PATH"
fi

# Activate venv and install deps (if pip is allowed)
if [ -f "$VENV_PATH/bin/activate" ]; then
    source "$VENV_PATH/bin/activate"
    if command -v pip >/dev/null 2>&1; then
        pip install rustimport
    else
        echo "pip not available, skipping dependency install"
    fi
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SERVICE_TEMPLATE="$SCRIPT_DIR/singular.service"
SERVICE_FILE="/etc/systemd/system/singular.service"
CURRENT_USER="$(whoami)"

# Rewrite relevant lines: point ExecStart to venv python
sed -e "s|ExecStart=.*|ExecStart=$VENV_PATH/bin/python3 -m singular|g" \
    -e "s|WorkingDirectory=.*|WorkingDirectory=$SCRIPT_DIR|g" \
    -e "s|User=.*|User=$CURRENT_USER|g" \
    "$SERVICE_TEMPLATE" | sudo tee "$SERVICE_FILE" > /dev/null

# For database and log files
sudo mkdir -p /var/log/singular
sudo mkdir -p /var/lib/singular
sudo mkdir -p /etc/singular

sudo chown $CURRENT_USER:$CURRENT_USER /var/log/singular
sudo chown $CURRENT_USER:$CURRENT_USER /var/lib/singular

# Copy config if singular_config.json exists
if [ -f "$SCRIPT_DIR/singular_config.json" ]; then
    sudo cp "$SCRIPT_DIR/singular_config.json" /etc/singular/singular_config.json
    sudo chown $CURRENT_USER:$CURRENT_USER /etc/singular/singular_config.json
    sudo chmod 600 /etc/singular/singular_config.json
else
    echo "Warning: no singular_config.json file found in $SCRIPT_DIR"
fi

# Reload and start service
sudo systemctl daemon-reload
sudo systemctl unmask singular.service 2>/dev/null
sudo systemctl enable singular.service
sudo systemctl start singular.service

echo "Service file installed at $SERVICE_FILE, systemd reloaded, and singular.service started."
