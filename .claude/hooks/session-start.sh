#!/bin/bash
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

echo "Session start hook running..."

cd "$CLAUDE_PROJECT_DIR"

if [ -f requirements.txt ]; then
  echo "Python 의존성 설치 중..."
  pip install -q -r requirements.txt
  echo "의존성 설치 완료"
fi
