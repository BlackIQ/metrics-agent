#!/bin/bash

export PYTHONPATH=/opt/openhubble-agent

/usr/local/bin/uv run /opt/openhubble-agent/cli/cli.py "$@"
