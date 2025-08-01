
# llm_cs_chatbot

## 프로젝트 개요
`llm_cs_chatbot`은 LLM(대형 언어 모델)을 활용한 고객 지원 챗봇 개발을 위한 프로젝트입니다. 데이터 전처리, 모델 학습 및 추론, API, 자동화 스크립트 등 전체 파이프라인을 포함합니다.

## 디렉토리 구조

```
llm_cs_chatbot/
├── api/                # 인퍼런스 API(FastAPI 등)
├── config/             # 설정 파일 (.env, 환경 변수)
├── data/               # 데이터셋(원본/가공 CSV 등)
├── model/              # 모델링, 학습, 파인튜닝 코드
├── preprocessing/      # 데이터 추출, 정제, EDA
├── notebooks/          # Jupyter 실험, 분석
├── scripts/            # 자동화 스크립트(스케줄러, 배치 등)
├── tests/              # 테스트 코드
├── requirements.txt    # pip 패키지 목록
├── .env                # DB 등 환경변수(민감정보 별도)
└── README.md           # 프로젝트 설명
```

## 주요 폴더 및 파일 설명

- **api/**: 챗봇 인퍼런스 API 서버 코드 (예: FastAPI)
- **config/**: 환경설정 파일 및 환경 변수 관리
- **data/**: 원본 및 가공된 데이터셋 저장 (CSV, JSONL 등)
- **model/**: 모델 학습, 파인튜닝, 추론 관련 코드 및 결과물
- **preprocessing/**: 데이터 추출, 정제, EDA(탐색적 데이터 분석) 코드
- **notebooks/**: Jupyter Notebook을 활용한 실험 및 분석
- **scripts/**: 파이프라인 자동화, 스케줄링, 배치 처리 스크립트
- **tests/**: 유닛 테스트 등 테스트 코드
- **requirements.txt**: 프로젝트 의존성 패키지 목록
- **.env**: 환경 변수 및 민감 정보 관리 파일
- **README.md**: 프로젝트 설명서

## 설치 및 실행 방법

1. 의존성 설치
    ```bash
    pip install -r requirements.txt
    ```

2. 환경 변수 설정
    - 프로젝트 루트에 `.env` 파일을 생성하고 필요한 환경변수를 입력합니다.

3. 전체 파이프라인 실행
    ```bash
    bash run_full_pipeline.sh
    ```

4. 워크플로우 실행
    ```bash
    bash run_full_workflow.sh
    ```


본 프로젝트는 QnA 챗봇 구축 및 LLM 파인튜닝(지도학습 기반) 실습/스터디를 목적으로 합니다. 다양한 버전의 파인튜닝 실험과 학습 방식을 연구합니다.