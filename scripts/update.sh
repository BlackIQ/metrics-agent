#!/usr/bin/env bash

################################################################################
# OpenHubble Metrics Agent                                                     #
################################################################################
# Welcome to OpenHubble Agent updater                                          #
#                                                                              #
# GitHub: https://github.com/OpenHubble/metrics-agent                          #
#                                                                              #
# Created by: OpenHubble Team, Amirhossein Mohammadi 2025                      #
#                                                                              #
# Happy Monitoring!                                                            #
################################################################################

set -euo pipefail

################################################################################
# Updater                                                                      #
################################################################################

if [[ "$EUID" -ne 0 ]]; then
    echo "Please run this script as root (sudo)."
    exit 1
fi

################################################################################
# Path                                                                         #
################################################################################

INSTALL_DIR="/opt/openhubble-agent"

TMP_FILE="/tmp/openhubble-agent.tar.gz"

GITHUB_REPO="OpenHubble/metrics-agent"

################################################################################
# Check Installation                                                           #
################################################################################

if [[ ! -d "$INSTALL_DIR" ]]; then
    echo "OpenHubble Metrics Agent is not installed."
    exit 1
fi

################################################################################
# Get Latest Release                                                           #
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

echo "Updating to ${LATEST_VERSION}"

TARBALL_URL="https://api.github.com/repos/${GITHUB_REPO}/tarball/${LATEST_VERSION}"

################################################################################
# Stop Service                                                                 #
################################################################################

echo "Stopping service..."

systemctl stop openhubble-agent || true

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
# Python Dependencies                                                          #
################################################################################

echo "Installing Python dependencies..."

cd "$INSTALL_DIR"

uv sync

################################################################################
# Database                                                                     #
################################################################################

echo "Running database migrations..."

uv run alembic upgrade head

################################################################################
# Permissions                                                                  #
################################################################################

chmod +x "$INSTALL_DIR/cli/wrapper.sh"

################################################################################
# CLI                                                                          #
################################################################################

ln -sf "$INSTALL_DIR/cli/wrapper.sh" /usr/local/bin/openhubble-agent

################################################################################
# Systemd                                                                      #
################################################################################

echo "Updating systemd service..."

cp "$INSTALL_DIR/openhubble-agent.service" /etc/systemd/system/

systemctl daemon-reload

################################################################################
# Restart                                                                      #
################################################################################

echo "Starting service..."

systemctl restart openhubble-agent

################################################################################
# Finished                                                                     #
################################################################################

echo
echo "OpenHubble Metrics Agent has been updated successfully."
echo
echo "Current Version : ${LATEST_VERSION}"
