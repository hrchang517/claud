#!/bin/bash
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$APP_DIR"

# 포트 체크 및 정리
if lsof -i:8080 >/dev/null 2>&1; then
    lsof -ti:8080 | xargs kill -9 2>/dev/null || true
    sleep 2
fi

# Flask 실행
python3 app.py
