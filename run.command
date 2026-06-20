#!/bin/bash

# 마인드케이 대시보드 실행 스크립트
# 더블클릭으로 실행 가능

set -e

# 스크립트 경로
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 포트 8080이 이미 사용 중인지 확인
if lsof -i:8080 >/dev/null 2>&1; then
    echo "포트 8080이 이미 사용 중입니다."
    echo "기존 서버를 종료하고 새로 시작합니다..."
    lsof -ti:8080 | xargs kill -9 2>/dev/null || true
    sleep 2
fi

# Flask 앱 실행
cd "$SCRIPT_DIR"
python3 app.py
