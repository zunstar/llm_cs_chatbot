#!/bin/bash
# run_full_workflow.sh
set -e

echo "==== 1️⃣ [DB→CSV] 원본 QnA 데이터 추출 및 저장 ===="
python main.py

echo "==== 2️⃣ [CSV→Prompt/Response JSONL] 데이터 가공 ===="
python scripts/generate_prompt_response.py

echo "==== 3️⃣ [모델 학습(파인튜닝)] ===="
python model/train.py

echo "==== ✅ 전체 파이프라인 자동화 완료 ===="
