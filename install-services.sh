#!/bin/bash

# Copy service files
echo "Copying service files..."
sudo cp samples/bloko-data.service /lib/systemd/system/
sudo cp samples/bloko.service /lib/systemd/system/

# Reload systemd
echo "Reloading systemd daemon..."
sudo systemctl daemon-reload

# Enable and start services
echo "Enabling and starting services..."
sudo systemctl enable bloko-data
sudo systemctl enable bloko
sudo systemctl start bloko-data
sudo systemctl start bloko

echo "Done! Services should be running."