#!/usr/bin/env bash
set -euo pipefail

pip install -e ".[api]"
agentdesk skill load
agentdesk serve --host 0.0.0.0 --port 8500
