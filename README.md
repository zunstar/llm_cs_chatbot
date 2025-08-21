# LLM 기반 고객 서비스 챗봇 파인튜닝 프로젝트

## 📝 프로젝트 개요

이 프로젝트는 고객 서비스(CS) 문의 데이터셋을 활용하여 대규모 언어 모델(LLM)을 파인튜닝하고, CS 챗봇을 구축하는 것을 목표로 합니다. 원본 데이터베이스에서 Q&A 데이터를 추출, 정제, 가공하여 모델 학습에 적합한 형태로 만들고, 이를 기반으로 모델을 학습시키는 전체 파이프라인을 포함합니다.

## ✨ 주요 기능

- **데이터 추출**: MySQL 데이터베이스에 저장된 고객 문의 및 답변 데이터를 추출합니다.
- **데이터 전처리**: 개인정보(전화번호, 이메일 등)를 마스킹하고, 불필요한 인사말이나 정형화된 문구를 제거하여 학습 데이터의 품질을 높입니다.
- **프롬프트 엔지니어링**: 문의 유형, 세부 분류 등의 메타데이터를 활용하여 모델이 문맥을 더 잘 이해할 수 있는 형태의 프롬프트(Prompt)를 생성합니다.
- **학습 데이터 생성**: 전처리된 데이터를 LLM 파인튜닝에 일반적으로 사용되는 `prompt`/`response` 형식의 JSONL 파일로 변환합니다.

## ⚙️ 전체 워크플로우

이 프로젝트는 `run_full_workflow.sh` 스크립트를 통해 전체 과정을 자동화합니다.

1.  **[1단계] 원본 Q&A 데이터 추출 (`main.py`)**
    - `config/config.py` 설정을 통해 DB에 연결하고 Q&A 데이터를 조회합니다.
    - 추출된 데이터를 `data/qna_dataset_sample.csv` 파일로 저장합니다.

2.  **[2단계] 학습 데이터 가공 (`scripts/generate_prompt_response.py`)**
    - `data/qna_dataset_sample.csv` 파일을 입력으로 받습니다.
    - 개인정보 마스킹, 텍스트 정제, 부적합 샘플 필터링 등의 전처리 작업을 수행합니다.
    - 최종적으로 `data/qna_prompt_response.jsonl` 형식의 학습용 데이터셋을 생성합니다.

3.  **[3단계] 모델 학습 (`model/train.py`)**
    - `data/qna_prompt_response.jsonl` 파일을 사용하여 Hugging Face Transformers 라이브러리 기반으로 LLM을 파인튜닝합니다.
    - *(참고: `model/train.py` 스크립트는 현재 저장소에 포함되어 있지 않습니다.)*

## 🚀 설치 및 실행 방법

### 1. 환경 설정

먼저, 프로젝트 실행에 필요한 파이썬 라이브러리를 설치합니다.

```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정

데이터베이스 연결을 위해 프로젝트 루트 디렉터리에 `.env` 파일을 생성하고 아래와 같이 DB 접속 정보를 입력합니다.

```env
# .env 파일 예시
DB_USER="your_db_user"
DB_PASSWORD="your_db_password"
DB_HOST="localhost"
DB_PORT="3306"
DB_NAME="your_db_name"
```

### 3. 전체 워크플로우 실행

아래 셸 스크립트를 실행하여 데이터 추출부터 모델 학습까지의 전체 파이프라인을 한 번에 실행할 수 있습니다.

```bash
bash run_full_workflow.sh
```

### 4. (참고) 학습된 모델로 추론 실행

학습이 완료된 모델을 사용하여 추론을 실행하는 파이프라인도 제공됩니다.

```bash
bash run_full_pipeline.sh
```
*(참고: 이 스크립트가 실행하는 `model/inference.py` 파일은 현재 저장소에 포함되어 있지 않습니다.)*


## 📂 프로젝트 구조

```
.
├── .env                  # DB 접속 정보 등 환경 변수 설정 파일 (생성 필요)
├── .gitignore
├── README.md             # 프로젝트 안내 문서
├── config/
│   └── config.py         # DB 엔진 생성 등 설정 관련 코드
├── data/                 # 데이터 파일 저장 디렉터리 (스크립트 실행 시 자동 생성)
│   ├── qna_dataset_sample.csv
│   └── qna_prompt_response.jsonl
├── main.py               # 1단계: DB에서 Q&A 데이터를 추출하여 CSV로 저장
├── requirements.txt      # 프로젝트 의존성 라이브러리 목록
├── run_full_pipeline.sh  # 학습된 모델 추론 실행 스크립트
├── run_full_workflow.sh  # 데이터 추출부터 학습까지 전체 파이프라인 실행 스크립트
└── scripts/
    └── generate_prompt_response.py # 2단계: CSV 데이터를 학습용 JSONL 데이터로 가공
```

## ⚠️ 참고: 누락된 파일 안내

현재 프로젝트 저장소에는 모델 학습(`model/train.py`) 및 추론(`model/inference.py`)에 관련된 스크립트가 포함되어 있지 않습니다. `run_full_workflow.sh`와 `run_full_pipeline.sh`를 완전하게 실행하려면 해당 파일들이 `model/` 디렉터리 내에 존재해야 합니다.
