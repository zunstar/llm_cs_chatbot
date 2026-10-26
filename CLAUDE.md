# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 프로젝트 개요

CS(고객지원) QnA 챗봇을 위한 LLM 파인튜닝 파이프라인입니다. MySQL 데이터베이스에서 QnA 데이터를 추출하여 KoGPT2 모델을 파인튜닝하고 추론하는 전체 워크플로우를 제공합니다.

## 개발 환경 및 명령어

### 가상환경 활성화
```bash
source venv-py312/bin/activate
```

### 핵심 실행 명령어
- **전체 파이프라인**: `bash run_full_workflow.sh` - 데이터 추출부터 학습까지 전체 과정
- **추론만 실행**: `bash run_full_pipeline.sh` - 기존 학습된 모델로 추론만 실행
- **개별 단계**:
  - 데이터 추출: `python main.py`
  - 데이터 전처리: `python scripts/generate_prompt_response.py`
  - 모델 학습: `python model/train.py`
  - 추론: `python model/inference.py`

### 의존성 설치
```bash
pip install -r requirements.txt
```

## 아키텍처 구조

### 데이터 파이프라인
1. **DB 추출** (main.py) → `data/qna_dataset_sample.csv`
2. **전처리** (scripts/generate_prompt_response.py) → `data/qna_prompt_response.jsonl`
3. **학습** (model/train.py) → `model/output_[timestamp]/`
4. **추론** (model/inference.py) → 실시간 질문 답변

### 핵심 구성요소

#### 데이터 추출 (preprocessing/data_extractor.py)
- `CSQnaExtractor` 클래스가 MySQL DB 연결 및 복잡한 JOIN 쿼리 실행
- CS 분류별(배송, 반품/교환, 취소/환불 등) 데이터 추출
- 최대 20,000건의 QnA 데이터 처리

#### 데이터 전처리 (scripts/generate_prompt_response.py)
- CSV 데이터를 학습용 프롬프트-응답 형식으로 변환
- 개인정보(전화번호, 이메일, 주소) 자동 마스킹 기능
- 불필요한 인사말 및 고정 멘트 제거
- JSONL 형식으로 저장하여 모델 학습에 최적화

#### 모델 학습 (model/train.py)
- 베이스 모델: `skt/kogpt2-base-v2`
- HuggingFace Transformers 사용한 지도학습 방식
- 학습 결과는 `model/output_[timestamp]/` 디렉토리에 저장

#### 추론 시스템 (model/inference.py)
- 가장 최근 학습된 모델 자동 로드
- GPU/MPS/CPU 환경 자동 감지
- 실시간 질문 답변 생성

## 환경 설정

### 데이터베이스 연결 설정
프로젝트 루트에 `.env` 파일 생성 필요:
```
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=your_database
```

### 주요 의존성
- Python 3.12 환경 사용
- HuggingFace Transformers, PyTorch 기반
- MySQL 연결을 위한 PyMySQL
- 데이터 처리용 pandas, datasets

## 파일 구조 특이사항

- `model/output_*/`: 각 학습 세션별 타임스탬프 기반 디렉토리 생성
- `data/`: CSV 원본 데이터와 JSONL 학습 데이터 분리
- `config/`: 데이터베이스 연결 설정 관리
- `venv-py312/`: Python 3.12 전용 가상환경