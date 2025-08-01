import pandas as pd
import re

# ✅ 개인정보 마스킹 함수
def mask_personal_info(text):
    if not isinstance(text, str): return ""
    text = re.sub(r'\b(0\d{1,2})[-\s]?(\d{3,4})[-\s]?(\d{4})\b', '[전화번호]', text)  # 전화번호
    text = re.sub(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', '[이메일]', text)                   # 이메일
    text = re.sub(r'(서울|부산|대구|광주|대전|울산|세종|경기|강원|충북|충남|전북|전남|경북|경남|제주)[^\s,]{0,20}(구|시|군)', '[주소]', text)
    text = re.sub(r'[0-9]{2,5}(동|호)', '[주소]', text)                              # 동/호
    text = re.sub(r'\b\d{5}\b', '[우편번호]', text)                                  # 우편번호
    return text

# ✅ 공통 텍스트 정제
def clean_prompt_response(text):
    if not isinstance(text, str): return ""
    text = text.strip()
    if text.startswith('"') and text.endswith('"'):
        text = text[1:-1]
    text = text.replace('\r\n', ' ').replace('\r', ' ').replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text)
    return mask_personal_info(text.strip())

# ✅ 답변용 정제 함수 (인사말 및 고정 멘트 제거 포함)
def clean_response_text(text):
    text = clean_prompt_response(text)
    # 인사말 제거
    intro_patterns = [
        r'^안녕하세요[.!, ]*(고객님)?[.! ,]*',
        r'^안녕하세요[.!, ]*[\w\s]+입니다[.! ,]*',
        r'^안녕하십니까[.! ,]*',
        r'^안녕하세[요유][.! ,]*'
    ]
    for pattern in intro_patterns:
        text = re.sub(pattern, '', text)

    # 과한 정중 표현 제거
    polite_phrases = [
        r'감사합니다', r'죄송합니다', r'불편을 드려 죄송합니다',
        r'도와드리겠습니다', r'도와드릴게요', r'안내드리겠습니다',
        r'빠르게 준비하겠습니다', r'확인하여 안내드리겠습니다',
        r'최대한 반영하겠습니다', r'언제든지 문의 부탁드립니다',
        r'문의 주시면 안내 드리겠습니다'
    ]
    for phrase in polite_phrases:
        text = re.sub(phrase, '', text)

    text = re.sub(r'\s+', ' ', text)
    return mask_personal_info(text.strip())

# ✅ 학습 부적합한 질문 필터링
def is_invalid_chat(text):
    if not isinstance(text, str): return True
    text = text.strip()
    if len(text) < 10: return True
    if any(kw in text for kw in ['이벤트 당첨', '소통왕', '감사합니다', '잘 쓰겠습니다', '선물 감사합니다']): return True
    if re.search(r'\d{3}-?\d{3,4}-?\d{4}', text): return True
    if re.search(r'(아파트|동|호|번지|도로명|주소|시|구|군)', text): return True
    return False

# ✅ 학습 데이터 생성 함수
def generate_llm_training_data(input_csv: str, output_path: str):
    df = pd.read_csv(input_csv)

    # 필수 컬럼 존재 여부 체크 및 필터링
    df = df[df['문의내용'].notnull() & df['답변내용'].notnull()].copy()

    # 📌 부적합 질문 제거
    before = len(df)
    df = df[~df['문의내용'].apply(is_invalid_chat)].copy()
    removed = before - len(df)
    print(f"🧹 부적합 샘플 {removed:,}건 필터링 완료")

    # NaN 컬럼 처리
    for col in ['분류', '유형', '세부유형']:
        if col in df.columns:
            df[col] = df[col].fillna("")
        else:
            df[col] = ""

    # 📌 유형 태그 구성 함수
    def build_type_tag(row):
        tags = []
        if row['분류']: tags.append(f"분류: {row['분류']}")
        if row['유형']: tags.append(f"유형: {row['유형']}")
        if row['세부유형']: tags.append(f"세부유형: {row['세부유형']}")
        return " / ".join(tags)

    # 프롬프트 생성
    df['prompt'] = df.apply(lambda row:
        clean_prompt_response(f"[{build_type_tag(row)}] [고객문의] {row['문의내용']}"),
        axis=1
    )

    # 응답 생성
    df['response'] = df['답변내용'].apply(clean_response_text)

    # 저장
    df[['prompt', 'response']].to_csv(output_path + '.csv', index=False)
    df[['prompt', 'response']].to_json(output_path + '.jsonl', lines=True, orient='records', force_ascii=False)

    print("✅ 전처리 및 저장 완료!")
    print(f"📄 CSV 파일: {output_path}.csv")
    print(f"📄 JSONL 파일: {output_path}.jsonl")

# ✅ 실행
if __name__ == "__main__":
    generate_llm_training_data(
        input_csv="data/qna_dataset_sample.csv",        # 👉 입력 CSV 경로
        output_path="data/qna_prompt_response"          # 👉 저장 파일명 prefix
    )
