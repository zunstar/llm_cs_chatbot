
# LLM CS Chatbot

## 🎯 프로젝트 목적
CS(고객지원) QnA 챗봇을 위한 LLM 파인튜닝 파이프라인입니다. 
데이터베이스에서 QnA 데이터를 추출하여 KoGPT2 모델을 파인튜닝하고 추론하는 전체 워크플로우를 제공합니다.

## 🚀 핵심 기능
- **데이터 추출**: MySQL DB에서 CS QnA 데이터 추출 및 전처리 
- **모델 파인튜닝**: KoGPT2 기반 지도학습 파인튜닝
- **추론 시스템**: 학습된 모델로 질문 답변 생성
- **개인정보 보호**: 전화번호, 이메일, 주소 자동 마스킹

## 📁 프로젝트 구조

```
llm_cs_chatbot/
├── main.py                    # 메인 실행: DB에서 QnA 데이터 추출
├── requirements.txt           # Python 의존성 패키지 목록
├── run_full_workflow.sh       # 전체 파이프라인 자동 실행 스크립트
├── run_full_pipeline.sh       # 추론만 실행하는 스크립트
├── config/
│   └── config.py             # DB 연결 설정 및 환경변수 관리
├── preprocessing/
│   └── data_extractor.py     # MySQL에서 CS QnA 데이터 추출 클래스
├── scripts/
│   └── generate_prompt_response.py  # CSV를 JSONL 형식으로 변환 및 정제
├── model/
│   ├── train.py              # KoGPT2 파인튜닝 학습 코드
│   ├── inference.py          # 학습된 모델로 추론/질문 답변
│   └── output_*/             # 파인튜닝된 모델 저장 디렉토리들
└── data/
    ├── qna_dataset_sample.csv    # DB에서 추출한 원본 QnA 데이터
    ├── qna_prompt_response.csv   # 정제된 프롬프트-응답 쌍
    └── qna_prompt_response.jsonl # 학습용 JSONL 형식 데이터
```

## 🔧 주요 모듈 설명

### `main.py`
- DB에서 최대 20,000건의 QnA 데이터 추출
- `CSQnaExtractor` 클래스를 사용하여 MySQL 쿼리 실행
- 결과를 `data/qna_dataset_sample.csv`로 저장

### `preprocessing/data_extractor.py`
- MySQL DB 연결 및 복잡한 JOIN 쿼리 실행
- CS 분류별(배송, 반품/교환, 취소/환불 등) 데이터 추출
- 문의 내용과 답변 내용을 매칭하여 반환

### `scripts/generate_prompt_response.py`
- CSV 데이터를 학습용 프롬프트-응답 형식으로 변환
- 개인정보(전화번호, 이메일, 주소) 자동 마스킹
- 불필요한 인사말 및 고정 멘트 제거
- JSONL 형식으로 저장하여 모델 학습 준비

### `model/train.py`
- HuggingFace Transformers 사용
- 베이스 모델: `skt/kogpt2-base-v2`
- 지도학습 방식으로 파인튜닝
- 학습 결과를 `model/output_[timestamp]/`에 저장

### `model/inference.py`
- 가장 최근 학습된 모델 자동 로드
- 질문 입력 시 답변 생성
- GPU/MPS/CPU 환경 자동 감지

## ⚙️ 설치 및 실행

### 1. 환경 설정
```bash
# 의존성 설치
pip install -r requirements.txt

# .env 파일 생성 (프로젝트 루트)
echo "DB_USER=your_username" >> .env
echo "DB_PASSWORD=your_password" >> .env
echo "DB_HOST=localhost" >> .env
echo "DB_PORT=3306" >> .env
echo "DB_NAME=your_database" >> .env
```

### 2. 전체 파이프라인 실행
```bash
# 데이터 추출 → 전처리 → 학습 → 추론 전체 실행
bash run_full_workflow.sh
```

### 3. 추론만 실행
```bash
# 기존 학습된 모델로 추론만 실행
bash run_full_pipeline.sh
```

### 4. 개별 단계 실행
```bash
# 1단계: DB에서 데이터 추출
python main.py

# 2단계: 데이터 전처리 및 JSONL 변환
python scripts/generate_prompt_response.py

# 3단계: 모델 파인튜닝
python model/train.py

# 4단계: 추론/질문답변
python model/inference.py
```

## 🔍 데이터 파이프라인

1. **DB 추출** (`main.py`) → `qna_dataset_sample.csv`
2. **전처리** (`generate_prompt_response.py`) → `qna_prompt_response.jsonl`
3. **학습** (`model/train.py`) → `model/output_*/`
4. **추론** (`model/inference.py`) → 실시간 질문 답변

## 🎓 학습 목적
KoGPT2 기반 CS 챗봇 파인튜닝 실습 및 다양한 학습 방식 연구를 위한 프로젝트입니다.