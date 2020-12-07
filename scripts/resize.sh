#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"/..
python3 src/resize.py --width 320 --height 240 --output /mnt/e/320x240
python3 src/resize.py --width 640 --height 480 --output /mnt/e/640x480
