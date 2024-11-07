#!/bin/bash

# Stop services
echo "Stopping services..."
sudo systemctl stop bloko-data
sudo systemctl stop bloko

# Disable services
echo "Disabling services..."
sudo systemctl disable bloko-data
sudo systemctl disable bloko

# Remove service files
echo "Removing service files..."
sudo rm /lib/systemd/system/bloko-data.service
sudo rm /lib/systemd/system/bloko.service

# Reload systemd
echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

echo "Done! Services have been uninstalled."