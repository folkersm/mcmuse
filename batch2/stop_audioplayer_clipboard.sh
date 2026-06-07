#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

PIDFILE="audioplayer_clipboard.pid"

if [[ ! -f "$PIDFILE" ]]; then
  echo "Not running (no pid file)."
  exit 0
fi

PID=$(cat "$PIDFILE")
if kill -0 "$PID" 2>/dev/null; then
  kill "$PID"
  echo "Stopped daemon (PID $PID)."
else
  echo "Daemon not running (stale pid file)."
fi
rm -f "$PIDFILE"
