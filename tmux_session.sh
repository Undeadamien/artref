#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")" || exit 0

NAME_SESSION="artref"

if tmux has-session -t "$NAME_SESSION"; then
    tmux kill-session -t "$NAME_SESSION"
fi

if [ ! -f .venv/bin/activate ]; then python -m venv .venv; fi
source ".venv/bin/activate"
if [ -f requirements.txt ]; then python -m pip install -r requirements.txt; fi

tmux new-session -d -s "$NAME_SESSION"

tmux set-option -t "$NAME_SESSION" base-index 1
tmux set-option -t "$NAME_SESSION" pane-base-index 1

tmux set-hook -t "$NAME_SESSION" after-new-window "send-keys \"source $(pwd)/.venv/bin/activate\" Enter \"clear\" Enter"
tmux set-hook -t "$NAME_SESSION" after-split-window "send-keys \"source $(pwd)/.venv/bin/activate\" Enter \"clear\" Enter"
tmux send-keys -t "$NAME_SESSION:1.1" "source $(pwd)/.venv/bin/activate" Enter "clear" Enter

tmux attach -t "$NAME_SESSION:1.1"
