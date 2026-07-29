#!/usr/bin/env bash

################################################################################
# OpenHubble Metrics Agent                                                     #
################################################################################
# Welcome to OpenHubble Agent installer                                        #
#                                                                              #
# GitHub: https://github.com/OpenHubble/metrics-agent                          #
#                                                                              #
# Created by: OpemHubble Team, Amirhossein Mohammadi 2025                      #
#                                                                              #
# Install:                                                                     #
# curl -s https://get.openhubble.com/agent | sudo bash                         #
#                                                                              #
# Happy Monitoring!                                                            #
################################################################################

set -euo pipefail

################################################################################
# Installer                                                                    #
################################################################################

# Run this script as root
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

TMP_FILE="/tmp/openhubble-agent.tar.gz"

GITHUB_REPO="OpenHubble/metrics-agent"

################################################################################
# Dependencies                                                                 #
################################################################################

echo "Installing dependencies..."

apt update -y
apt install -y \
    python3 \
    python3-venv \
    python3-pip \
    curl \
    tar \
    jq

################################################################################
# Install uv                                                                   #
################################################################################

if ! command -v uv >/dev/null 2>&1; then
    echo "Installing uv..."

    export UV_INSTALL_DIR="/usr/local/bin"

    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

################################################################################
# Get latest release                                                           #
################################################################################

echo "Fetching latest release..."

LATEST_VERSION=$(
    curl -fsSL "https://api.github.com/repos/${GITHUB_REPO}/releases/latest" \
    | jq -r ".tag_name"
)

if [[ -z "$LATEST_VERSION" || "$LATEST_VERSION" == "null" ]]; then
    echo "Unable to determine latest release."
    exit 1
fi

TARBALL_URL="https://api.github.com/repos/${GITHUB_REPO}/tarball/${LATEST_VERSION}"

echo "Installing OpenHubble Metrics Agent ${LATEST_VERSION}"

################################################################################
# Directories                                                                  #
################################################################################

mkdir -p "$INSTALL_DIR"
mkdir -p "$CONFIG_DIR"
mkdir -p "$DATA_DIR"
mkdir -p "$LOG_DIR"

################################################################################
# Download                                                                     #
################################################################################

echo "Downloading release..."

curl -fL "$TARBALL_URL" -o "$TMP_FILE"

echo "Extracting..."

rm -rf "${INSTALL_DIR:?}"/*

tar \
    -xzf "$TMP_FILE" \
    --strip-components=1 \
    -C "$INSTALL_DIR"

rm -f "$TMP_FILE"

################################################################################
# Configuration                                                                #
################################################################################

echo "Setting up configuration..."

if [[ ! -f "$CONFIG_DIR/.env" ]]; then
    cp "$INSTALL_DIR/.env.example" "$CONFIG_DIR/.env"
    echo "Created default configuration:"
    echo "  $CONFIG_DIR/.env"
else
    echo "Existing configuration found. Keeping it."
fi

################################################################################
# Python dependencies                                                          #
################################################################################

echo "Installing Python dependencies..."

cd "$INSTALL_DIR"

uv sync

################################################################################
# Database                                                                     #
################################################################################

echo "Initializing database..."

uv run alembic upgrade head

################################################################################
# Permissions                                                                  #
################################################################################

chmod +x "$INSTALL_DIR/cli/wrapper.sh"

################################################################################
# CLI                                                                          #
################################################################################

ln -sf \
    "$INSTALL_DIR/cli/wrapper.sh" \
    /usr/local/bin/openhubble-agent

################################################################################
# Systemd                                                                      #
################################################################################

echo "Installing systemd service..."

if [[ ! -f "$INSTALL_DIR/openhubble-agent.service" ]]; then
    echo "Service file not found."
    exit 1
fi

cp "$INSTALL_DIR/openhubble-agent.service" /etc/systemd/system/

systemctl daemon-reload
systemctl enable openhubble-agent

################################################################################
# Finished                                                                     #
################################################################################

echo
echo "OpenHubble Metrics Agent ${LATEST_VERSION} installed successfully."
echo
echo "Directories:"
echo "  Application : $INSTALL_DIR"
echo "  Config      : $CONFIG_DIR"
echo "  Database    : $DATA_DIR"
echo "  Logs        : $LOG_DIR"
echo
echo "Configuration:"
echo "  $CONFIG_DIR/.env"
echo
echo "Edit the configuration before starting the service."
