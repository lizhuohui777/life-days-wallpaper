#!/bin/zsh
set -euo pipefail
cd "$(dirname "$0")/.."
TEST_ROOT="$(mktemp -d "${TMPDIR:-/private/tmp/}daywallpaper-tests.XXXXXX")"
trap 'rm -rf "$TEST_ROOT"' EXIT
/usr/bin/swiftc -module-cache-path "$TEST_ROOT/modules" Shared.swift Tests/main.swift -o "$TEST_ROOT/tests"
"$TEST_ROOT/tests" "$TEST_ROOT"
python3 -B Tests/test_metadata.py
