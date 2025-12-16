#!/bin/bash

VENV_PATH="/home/$(whoami)/pro_py"

#create venv
if [ ! -d "$VENV_PATH" ]; then
 python3 -m venv "$VENV_PATH"
fi

#activate venv and install deps (if pip is allowed)
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

#wrapper script
cat <<EOF | sudo tee /usr/local/bin/singular > /dev/null
#!/bin/bash
exec $VENV_PATH/bin/python3 -m singular "\$@"
EOF
sudo chmod +x /usr/local/bin/singular

#rewrite service file
sed -e "s|ExecStart=.*|ExecStart=/usr/local/bin/singular daemon|g" \
 -e "s|WorkingDirectory=.*|WorkingDirectory=$SCRIPT_DIR|g" \
 -e "s|User=.*|User=$CURRENT_USER|g" \
 "$SERVICE_TEMPLATE" | sudo tee "$SERVICE_FILE" > /dev/null

#create directories
sudo mkdir -p /var/log/singular /var/lib/singular /etc/singular
sudo chown $CURRENT_USER:$CURRENT_USER /var/log/singular /var/lib/singular

#copy config
if [ -f "$SCRIPT_DIR/singular_config.json" ]; then
 sudo cp "$SCRIPT_DIR/singular_config.json" /etc/singular/singular_config.json
 sudo chown $CURRENT_USER:$CURRENT_USER /etc/singular/singular_config.json
 sudo chmod 600 /etc/singular/singular_config.json
else
 echo "Warning: no singular_config.json file found in $SCRIPT_DIR"
fi

#reload and start service
sudo systemctl daemon-reload
sudo systemctl unmask singular.service 2>/dev/null
sudo systemctl enable singular.service
sudo systemctl start singular.service

echo "Service file installed at $SERVICE_FILE, systemd reloaded, and singular.service started."