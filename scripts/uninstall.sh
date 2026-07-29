#!/usr/bin/env bash

################################################################################
# OpenHubble Metrics Agent                                                     #
################################################################################
# Welcome to OpenHubble Agent uninstaller                                      #
#                                                                              #
# GitHub: https://github.com/OpenHubble/metrics-agent                          #
#                                                                              #
# Created by: OpenHubble Team, Amirhossein Mohammadi 2025                      #
#                                                                              #
# Happy Monitoring!                                                            #
################################################################################

set -euo pipefail

################################################################################
# Uninstaller                                                                  #
################################################################################

if [[ "$EUID" -ne 0 ]]; then
    echo "Please run this script as root (sudo)."
    exit 1
fi

################################################################################
# Path                                                                         #
################################################################################

INSTALL_DIR="/opt/openhubble-agent"                      # Application
CONFIG_DIR="/etc/openhubble-agent"                       # Settings
DATA_DIR="/var/lib/openhubble-agent"                     # Database
LOG_DIR="/var/log/openhubble-agent"                      # Log

################################################################################
# Stop Service                                                                 #
################################################################################

echo "Stopping service..."

systemctl stop openhubble-agent 2>/dev/null || true
systemctl disable openhubble-agent 2>/dev/null || true

################################################################################
# Remove Service                                                               #
################################################################################

echo "Removing systemd service..."

rm -f /etc/systemd/system/openhubble-agent.service

systemctl daemon-reload

################################################################################
# Remove CLI                                                                   #
################################################################################

echo "Removing CLI..."

rm -f /usr/local/bin/openhubble-agent

################################################################################
# Remove Application                                                           #
################################################################################

echo "Removing application..."

rm -rf "$INSTALL_DIR"

################################################################################
# User Data                                                                    #
################################################################################

echo
echo "The following user data can also be removed:"
echo
echo "  Configuration : $CONFIG_DIR"
echo "  Database      : $DATA_DIR"
echo "  Logs          : $LOG_DIR"
echo

read -rp "Remove user data? [y/N]: " CONFIRM

if [[ "$CONFIRM" =~ ^[Yy]$ ]]; then
    rm -rf "$CONFIG_DIR"
    rm -rf "$DATA_DIR"
    rm -rf "$LOG_DIR"

    echo
    echo "User data removed."
else
    echo
    echo "Configuration, database and logs were preserved."
fi

################################################################################
# Finished                                                                     #
################################################################################

echo
echo "OpenHubble Metrics Agent has been uninstalled successfully."
