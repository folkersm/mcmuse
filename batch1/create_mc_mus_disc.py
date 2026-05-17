import os
import urllib.parse
import sys

# Get directory from command line or use current directory
directory = sys.argv[1] if len(sys.argv) > 1 else "."

for filename in os.listdir(directory):
    path = os.path.join(directory, filename)

    if os.path.isfile(path):
        encoded = urllib.parse.quote(filename)
        print(f"{filename} -> {encoded}")