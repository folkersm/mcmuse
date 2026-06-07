#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

VENV=".venv-clipboard"
PIDFILE="audioplayer_clipboard.pid"
LOG="audioplayer_clipboard.log"

if [[ -f "$PIDFILE" ]] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
  echo "Already running (PID $(cat "$PIDFILE"))."
  exit 0
fi

if [[ ! -d "$VENV" ]]; then
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install -q pynput
fi

echo 0 >.audioplayer_clipboard_index

nohup "$VENV/bin/python" audioplayer_clipboard_daemon.py >>"$LOG" 2>&1 &
echo $! >"$PIDFILE"
echo "Started audioplayer clipboard daemon (PID $(cat "$PIDFILE"))."
echo "Press Ctrl+Shift+O to copy the next command. Log: $LOG"
