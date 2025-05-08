#!/usr/bin/env bash

set -eu

echo; echo "Building 'scrape'"; echo
pyinstaller -y -n scrape --onefile src/scrape.py
