# LLM CS 챗봇 파인튜닝 프로젝트

이 프로젝트는 고객 서비스(CS) 문의 데이터베이스에서 Q&A 데이터를 추출하고, 이를 가공하여 대규모 언어 모델(LLM)을 파인튜닝하기 위한 학습 데이터를 생성하는 파이프라인을 제공합니다.

## 🚀 프로젝트 목표

고객 문의 및 답변 데이터를 활용하여, CS 업무에 특화된 LLM 챗봇을 만들기 위한 학습 데이터를 구축하고 모델을 훈련시키는 것을 목표로 합니다.

## 📁 프로젝트 구조

```
.
├── .gitignore
├── README.md
├── config
│   └── config.py           # 데이터베이스 연결 설정
├── main.py                 # DB에서 QnA 데이터 추출 및 CSV 저장
├── requirements.txt        # Python 패키지 의존성 목록
├── run_full_pipeline.sh    # (추정) 모델 추론 파이프라인 실행 스크립트
├── run_full_workflow.sh    # 전체 데이터 처리 및 학습 파이프라인 실행 스크립트
└── scripts
    └── generate_prompt_response.py # QnA 데이터를 프롬프트-응답 쌍으로 가공
```

**참고:** `run_full_pipeline.sh`와 `run_full_workflow.sh` 스크립트에서 `preprocessing`, `model` 디렉토리를 참조하고 있으나, 현재 레포지토리에는 해당 디렉토리들이 포함되어 있지 않습니다. 프로젝트의 완전한 실행을 위해서는 아래 "실행 방법" 섹션에 설명된 파일들을 추가로 구현해야 합니다.

## ⚙️ 주요 기능 및 워크플로우

본 프로젝트의 전체 워크플로우는 `run_full_workflow.sh` 스크립트에 정의되어 있으며, 다음 3단계로 구성됩니다.

**1️⃣ 1단계: 원본 QnA 데이터 추출 (`main.py`)**

-   MySQL 데이터베이스에 연결하여 고객 문의 및 답변 데이터를 추출합니다.
-   추출된 데이터를 `data/qna_dataset_sample.csv` 파일로 저장합니다.
-   **필요 사항:** `preprocessing.data_extractor.CSQnaExtractor` 클래스가 필요합니다. 이 클래스는 DB에서 데이터를 읽어오는 로직을 포함해야 합니다.

**2️⃣ 2단계: 학습용 데이터 가공 (`scripts/generate_prompt_response.py`)**

-   1단계에서 생성된 CSV 파일을 입력으로 받습니다.
-   개인정보(전화번호, 이메일, 주소 등)를 마스킹 처리합니다.
-   불필요한 인사말, 과한 정중 표현 등을 제거하여 텍스트를 정제합니다.
-   학습에 부적합한 샘플(짧은 문장, 광고성 문의 등)을 필터링합니다.
-   최종적으로 `[유형] [고객문의] {문의내용}` 형식의 `prompt`와 정제된 `response` 쌍을 생성합니다.
-   결과를 `data/qna_prompt_response.csv`와 `data/qna_prompt_response.jsonl` 두 가지 포맷으로 저장합니다.

**3️⃣ 3단계: 모델 학습 (`model/train.py`)**

-   2단계에서 가공된 `jsonl` 파일을 사용하여 Hugging Face의 `transformers` 라이브러리를 통해 LLM을 파인튜닝합니다.
-   **필요 사항:** `model/train.py` 스크립트가 필요합니다. 이 스크립트는 `datasets` 라이브러리로 `jsonl` 파일을 로드하고, `Trainer` 또는 유사한 클래스를 사용하여 모델 학습을 수행하는 코드를 포함해야 합니다.

## 🛠️ 실행 방법

### 1. 환경 설정

**가상환경 생성 및 활성화**

```bash
python -m venv venv
source venv/bin/activate
```

**의존성 패키지 설치**

```bash
pip install -r requirements.txt
```

**환경 변수 설정**

프로젝트 루트 디렉토리에 `.env` 파일을 생성하고, 데이터베이스 연결 정보를 입력합니다.

```
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=3306
DB_NAME=your_db_name
```

### 2. 누락된 스크립트 구현

프로젝트를 완전히 실행하려면 다음 파일들을 직접 구현해야 합니다.

-   **`preprocessing/data_extractor.py`**:
    -   `CSQnaExtractor` 클래스를 정의합니다.
    -   `config.py`의 `get_db_engine`을 사용하여 DB에 연결하고, QnA 데이터를 `pandas.DataFrame`으로 반환하는 `extract_qna_joined` 메소드를 구현해야 합니다.

-   **`model/train.py`**:
    -   `transformers` 라이브러리의 `Trainer` 또는 `SFTTrainer` 등을 사용하여 `data/qna_prompt_response.jsonl` 파일을 학습 데이터로 사용하는 파인튜닝 코드를 작성합니다.

-   **`model/inference.py`**:
    -   `run_full_pipeline.sh`에서 사용되는 스크립트로, 파인튜닝된 모델을 로드하여 새로운 질문에 대한 답변을 생성하는 추론 코드를 작성합니다.

### 3. 전체 워크플로우 실행

모든 파일이 준비되면, 아래 스크립트를 실행하여 전체 파이프라인을 실행할 수 있습니다.

```bash
bash run_full_workflow.sh
```

## 📦 주요 의존성

-   `pandas`: 데이터 처리 및 CSV/JSON 파일 입출력
-   `SQLAlchemy`, `PyMySQL`: MySQL 데이터베이스 연동
-   `python-dotenv`: 환경 변수 관리
-   `transformers`, `torch`, `datasets`: Hugging Face 기반 모델 학습 및 데이터셋 처리
-   `accelerate`: 모델 학습 가속화

이 README가 프로젝트를 이해하고 사용하는 데 도움이 되기를 바랍니다.
