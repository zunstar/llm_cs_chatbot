from preprocessing.data_extractor import CSQnaExtractor

def main():
    print("== LLM CS 챗봇용 QNA 데이터 추출 ==")
    
    extractor = CSQnaExtractor()
    df = extractor.extract_qna_joined(limit=20000)
    
    print(f"문의 데이터 {len(df):,}건 로딩 완료 ✅")
    print(df.head(3))

    # 저장
    output_path = "data/qna_dataset_sample.csv"
    df.to_csv(output_path, index=False)
    print(f"CSV 저장 완료 👉 {output_path}")

if __name__ == "__main__":
    main()
