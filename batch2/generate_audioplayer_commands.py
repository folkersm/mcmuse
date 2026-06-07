#!/usr/bin/env python3
"""Generate Minecraft /audioplayer commands for each MP3 in the current folder."""

import os
import urllib.parse

BASE_URL = "https://raw.githubusercontent.com/folkersm/mcmuse/main/batch1"
OUTPUT_FILE = "audioplayer_commands.txt"


def url_friendly_filename(filename: str) -> str:
    # Match GitHub raw URLs: encode spaces/brackets, leave parentheses literal.
    return urllib.parse.quote(filename, safe="()")


def song_name_from_filename(filename: str) -> str:
    name = os.path.splitext(filename)[0]
    for sep in ("(", "["):
        if sep in name:
            name = name.split(sep, 1)[0]
    return name.strip()


def main() -> None:
    folder = os.path.dirname(os.path.abspath(__file__)) or "."
    mp3_files = sorted(
        f for f in os.listdir(folder) if f.lower().endswith(".mp3")
    )

    if not mp3_files:
        print(f"No MP3 files found in {folder}")
        return

    lines: list[str] = []
    for filename in mp3_files:
        encoded = url_friendly_filename(filename)
        url = f"{BASE_URL}/{encoded}"
        song = song_name_from_filename(filename)
        lines.append(f'/audioplayer url "{url}"')
        lines.append(f'/audioplayer apply ID "{song}"')
        lines.append("")

    out_path = os.path.join(folder, OUTPUT_FILE)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines).rstrip() + "\n")

    print(f"Wrote {len(mp3_files)} track(s) to {out_path}")


if __name__ == "__main__":
    main()
