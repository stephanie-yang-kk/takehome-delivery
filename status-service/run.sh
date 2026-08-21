#!/usr/bin/env bash
# Auto-detect OS/arch and run the matching statussvc binary.
# Works on Linux, macOS, WSL, and Git Bash / MSYS on Windows.
set -euo pipefail
DIR="$(cd "$(dirname "$0")" && pwd)"
OS="$(uname -s | tr '[:upper:]' '[:lower:]')"
# Git Bash / MSYS / Cygwin on Windows report names like MINGW64_NT, MSYS_NT, CYGWIN_NT
case "$OS" in
  mingw*|msys*|cygwin*) OS=windows ;;
esac
ARCH="$(uname -m)"
case "$ARCH" in
  x86_64|amd64)  ARCH=amd64 ;;
  aarch64|arm64) ARCH=arm64 ;;
  *) echo "Unsupported arch: $ARCH"; exit 1 ;;
esac
EXT=""
if [ "$OS" = "windows" ]; then EXT=".exe"; fi
BIN="$DIR/bin/statussvc-$OS-$ARCH$EXT"
if [ ! -x "$BIN" ] && [ ! -f "$BIN" ]; then
  echo "No binary for $OS/$ARCH in $DIR/bin/ — available:"
  ls "$DIR/bin/"
  exit 1
fi
exec "$BIN" "$@"
