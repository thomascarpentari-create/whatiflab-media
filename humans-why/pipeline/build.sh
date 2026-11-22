#!/bin/sh
# Aufruf im Ordner humans-why/bilder:  sh ../pipeline/build.sh ../folgen/<folge>.json
# Voraussetzungen: pip install --break-system-packages sherpa-onnx==1.12.40 pillow numpy scipy ; ffmpeg
# Stimme: kokoro-en-v0_19 von https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/kokoro-en-v0_19.tar.bz2 entpacken, Pfad in KOKORO setzen.
# Schrift: Anton-Regular.ttf nach /usr/share/fonts/truetype/google-fonts/ofl/anton/ legen.
set -e
C="$1"; D=$(dirname "$0")
python3 "$D/tts.py" "$C"
python3 "$D/render.py" "$C" --stills
python3 "$D/render.py" "$C"
