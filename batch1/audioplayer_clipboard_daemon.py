#!/usr/bin/env python3
"""Copy the next audioplayer command to the clipboard on Ctrl+Shift+O."""

import argparse
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
COMMANDS_FILE = SCRIPT_DIR / "audioplayer_commands.txt"
STATE_FILE = SCRIPT_DIR / ".audioplayer_clipboard_index"


def load_commands() -> list[str]:
    if not COMMANDS_FILE.is_file():
        return []
    commands: list[str] = []
    with COMMANDS_FILE.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                commands.append(line)
    return commands


def read_index() -> int:
    if not STATE_FILE.is_file():
        return 0
    try:
        return max(0, int(STATE_FILE.read_text(encoding="utf-8").strip()))
    except ValueError:
        return 0


def write_index(index: int) -> None:
    STATE_FILE.write_text(str(index), encoding="utf-8")


def copy_to_clipboard(text: str) -> None:
    for tool in (
        ["xclip", "-selection", "clipboard"],
        ["wl-copy"],
    ):
        try:
            subprocess.run(
                tool,
                input=text.encode("utf-8"),
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return
        except FileNotFoundError:
            continue
    raise RuntimeError("No clipboard tool found (install xclip or wl-copy)")


def notify(title: str, body: str) -> None:
    try:
        subprocess.run(
            ["notify-send", "-a", "audioplayer-clipboard", title, body],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except FileNotFoundError:
        pass


def copy_next_command() -> None:
    commands = load_commands()
    if not commands:
        notify("Audioplayer clipboard", f"No commands in {COMMANDS_FILE.name}")
        return

    index = read_index()
    if index >= len(commands):
        index = 0
        notify("Audioplayer clipboard", "Wrapped to first command")

    command = commands[index]
    copy_to_clipboard(command)
    write_index(index + 1)

    preview = command if len(command) <= 72 else command[:69] + "..."
    notify(
        "Audioplayer clipboard",
        f"Copied {index + 1}/{len(commands)}\n{preview}",
    )


def run_daemon() -> None:
    try:
        from pynput import keyboard
    except ImportError:
        print(
            "pynput is required. Run: ./start_audioplayer_clipboard.sh",
            file=sys.stderr,
        )
        sys.exit(1)

    if not COMMANDS_FILE.is_file():
        print(f"Missing {COMMANDS_FILE}", file=sys.stderr)
        sys.exit(1)

    write_index(0)

    notify("Audioplayer clipboard", "Listening for Ctrl+Shift+O")

    hotkeys = keyboard.GlobalHotKeys({"<ctrl>+<shift>+o": copy_next_command})
    with hotkeys:
        hotkeys.join()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Reset to the first command and exit",
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Copy the next command once and exit (no hotkey listener)",
    )
    args = parser.parse_args()

    if args.reset:
        write_index(0)
        print("Reset to first command.")
        return

    if args.once:
        copy_next_command()
        return

    run_daemon()


if __name__ == "__main__":
    main()
