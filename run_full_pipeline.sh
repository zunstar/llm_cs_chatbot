#!/bin/bash
# run_full_pipeline.sh

echo "🧹 기존 venv 세션이 열려 있다면 비활성화 중..."
deactivate 2>/dev/null || echo "참고: 현재 활성화된 가상환경 없음 (계속 진행)"

echo "🐍 Python 3.12 전용 가상환경(vnv-py312) 활성화 중..."
source venv-py312/bin/activate

python model/inference.py