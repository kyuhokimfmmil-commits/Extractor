import streamlit as st
import re

TOC_BOOK1 = [
    "CHAPTER 01 형법의 기본개념", "CHAPTER 02 죄형법정주의", "SECTION 01 시간적 적용범위", "SECTION 02 장소적 적용범위",
    "SECTION 03 인적 적용범위", "CHAPTER 01 범죄론의 기초이론", "SECTION 01 구성요건 일반이론", "SECTION 02 행위의 주체",
    "SECTION 03 인과관계와 객관적 귀속", "SECTION 04 구성요건적 고의", "SECTION 05 구성요건적 착오", "SECTION 01 위법성 일반이론",
    "SECTION 02 정당방위", "SECTION 03 긴급피난", "SECTION 04 자구행위", "SECTION 05 피해자의 승낙", "SECTION 06 정당행위",
    "SECTION 01 책임이론", "SECTION 02 책임능력", "SECTION 03 원인에 있어서 자유로운 행위", "SECTION 04 위법성의 인식",
    "SECTION 05 금지착오", "SECTION 06 기대가능성", "SECTION 01-1 실행의 착수", "SECTION 01-2 미수범 일반",
    "SECTION 02 예비‧음모죄", "SECTION 03 장애미수", "SECTION 04 중지미수", "SECTION 05 불능미수",
    "SECTION 01 다수범죄가담형태론 일반이론", "SECTION 02 공동정범", "SECTION 03 간접정범", "SECTION 04 교사범",
    "SECTION 05 방조범", "SECTION 06 공범과 신분", "CHAPTER 03 부작위범", "SECTION 01 과실범", "SECTION 02 결과적 가중범",
    "CHAPTER 01 죄수의 일반이론", "SECTION 01 법조경합", "SECTION 02 포괄일죄", "SECTION 01 상상적 경합",
    "SECTION 02 실체적 경합", "CHAPTER 01 형벌의 의의와 종류", "CHAPTER 02 형의 양정", "CHAPTER 03 누범",
    "CHAPTER 04 선고유예‧집행유예‧가석방", "CHAPTER 05 형의 시효‧소멸‧기간", "CHAPTER 06 보안처분", "CHAPTER 01 형법 사례형 문제"
]

TOC_BOOK2 = [
    "SECTION 01 살인의 죄", "SECTION 02 상해와 폭행의 죄", "SECTION 03 과실치사상의 죄", "SECTION 04 낙태의 죄",
    "SECTION 05 유기와 학대의 죄", "SECTION 01 협박의 죄", "SECTION 02 체포와 감금의 죄", "SECTION 03 약취와 유인의 죄",
    "SECTION 04 강요의 죄", "SECTION 07 강간과 추행의 죄", "SECTION 01 명예에 대한 죄", "SECTION 02 신용‧업무와 경매에 대한 죄",
    "SECTION 01 비밀침해의 죄", "SECTION 02 주거침입의 죄", "SECTION 01 재산죄 총설", "SECTION 02-1 절도의 죄",
    "SECTION 02-2 친족상도례", "SECTION 03 강도의 죄", "SECTION 04-1 사기의 죄", "SECTION 04-2 신용카드 등 관련 범죄",
    "SECTION 05 공갈죄", "SECTION 06 횡령의 죄", "SECTION 07 배임의 죄", "SECTION 08 장물의 죄", "SECTION 09 손괴의 죄",
    "SECTION 10 권리행사방해죄", "SECTION 11 강제집행면탈죄", "SECTION 01 공안을 해하는 죄", "SECTION 02 폭발물에 관한 죄",
    "SECTION 03 방화와 실화의 죄", "SECTION 04 일수와 수리에 관한 죄", "SECTION 05 교통방해의 죄", "CHAPTER 02 공중의 건강에 대한 죄",
    "SECTION 01 통화에 관한 죄", "SECTION 02 유가증권‧우표‧인지에 관한 죄", "SECTION 03-1 공문서등의 위조, 변조죄",
    "SECTION 03-2 자격모용에 의한 공문서작성죄", "SECTION 03-3 허위공문서작성등 죄", "SECTION 03-4 공정증서원본등 불(부)실기재죄",
    "SECTION 03-5 허위진단서등 작성죄", "SECTION 03-6 사문서 등의 위조, 변조죄", "SECTION 03-7 자격모용에 의한 사문서작성죄",
    "SECTION 03-8 위조 등 문서행사죄", "SECTION 03-9 공(사)문서부정행사죄", "SECTION 03-10 공(사)전자기록 위작등 죄",
    "SECTION 04 인장에 관한 죄", "SECTION 01 성풍속에 관한 죄", "SECTION 02 도박과 복표에 대한 죄", "SECTION 03 신앙에 관한 죄",
    "SECTION 01 내란의 죄", "SECTION 02 외환의 죄", "SECTION 03 국기에 관한 죄", "SECTION 04 국교에 관한 죄",
    "SECTION 01-1 직무유기죄", "SECTION 01-2 직권남용죄", "SECTION 01-3 기타 직무수행상의 범죄", "SECTION 01-4 뇌물죄",
    "SECTION 02 공무방해에 관한 죄", "SECTION 03 도주와 범인은닉의 죄", "SECTION 04 위증과 증거인멸의 죄", "SECTION 05 무고의 죄"
]

TOC_BOOK3 = [
    "SECTION 01-1 총설", "SECTION 01-2 함정수사", "SECTION 02-1 불심검문", "SECTION 02-2 변사자의 검시",
    "SECTION 02-3 고소‧고발", "SECTION 02-4 자수", "SECTION 03-1 임의수사", "SECTION 03-2 피의자신문",
    "SECTION 01-1 체포", "SECTION 01-2 구속", "SECTION 01-3 접견교통권", "SECTION 01-4 체포‧구속적부심",
    "SECTION 01-5 보석", "SECTION 01-6 구속집행정지, 구속실효", "SECTION 02-1 압수‧수색‧검증", "SECTION 02-2 통신제한조치 등",
    "SECTION 03 판사에 대한 강제처분의 청구", "SECTION 01 수사의 종결", "SECTION 02 재정신청", "SECTION 03 공소제기 후의 수사",
    "SECTION 01 공소제기의 효과", "SECTION 01 증거의 의의와 종류", "SECTION 02 증거법의 기본원칙", "SECTION 03 위법수집증거배제법칙",
    "SECTION 04 자백배제법칙", "SECTION 05 전문법칙", "SECTION 06 당사자의 증거동의와 증거능력", "SECTION 07 탄핵증거",
    "SECTION 08 자백의 보강법칙", "SECTION 09 공판조서의 증명력", "CHAPTER 01 수사‧증거 사례형 문제", "CHAPTER 02 형사법 종합 사례형 문제"
]

TOC_BOOK4 = [
    "SECTION 01 형사소송법의 의의와 성격", "SECTION 02 형사소송법의 법원(法源)", "SECTION 03 형사소송법의 적용범위",
    "SECTION 01 형사소송의 이념과 기본원칙", "SECTION 02 형사소송의 기본구조", "CHAPTER 03 소송절차의 본질과 절차이분론",
    "SECTION 01-1 법원의 의의와 구성", "SECTION 01-2 제척‧기피‧회피", "SECTION 01-3 법원의 관할", "SECTION 02 검사",
    "SECTION 03 피고인", "SECTION 04 변호인", "SECTION 01 소송행위의 일반적 요소", "SECTION 02 소송조건",
    "CHAPTER 01 공소와 공소권", "CHAPTER 02 공소제기의 기본원리", "CHAPTER 03 공소제기의 절차",
    "SECTION 01 공판절차의 기본원칙", "SECTION 02 공판심리의 범위", "SECTION 03 공판준비절차", "SECTION 04 공판정의 심리",
    "SECTION 05 공판기일의 절차", "SECTION 06 증인신문‧감정‧검증", "SECTION 07-1 간이공판절차", "SECTION 07-2 공판절차의 정지와 갱신",
    "SECTION 07-3 국민참여재판", "CHAPTER 02 재판", "CHAPTER 03 종국재판", "CHAPTER 04 재판의 효력", "CHAPTER 05 소송비용",
    "SECTION 01-1 상소일반", "SECTION 01-2 불이익변경금지의 원칙", "SECTION 02 항소", "SECTION 03 상고", "SECTION 04 항고(재항고)",
    "CHAPTER 02 비상구제절차", "SECTION 01 약식절차", "SECTION 02 즉결심판절차", "SECTION 03 소년에 대한 형사절차",
    "SECTION 04 범죄피해자의 법적지위", "SECTION 01 재판의 집행", "SECTION 02 형사보상"
]

def clean_text(text):
    return re.sub(r'[^가-힣a-zA-Z0-9①②③④⑤]', '', text)

def extract_answers_by_book(text, toc_list):
    compressed_text = clean_text(text)
    ans_map = {'①': 1, '②': 2, '③': 3, '④': 4, '⑤': 5}
    
    toc_indices = []
    for title in toc_list:
        clean_title = clean_text(title)
        idx = compressed_text.find(clean_title)
        if idx != -1:
            toc_indices.append({"idx": idx, "title": title})
            
    toc_indices.sort(key=lambda x: x["idx"])
    
    if not toc_indices:
        return "오류: 업로드한 텍스트에서 선택한 교재의 목차를 하나도 찾지 못했습니다."
        
    results = []
    for i in range(len(toc_indices)):
        start_idx = toc_indices[i]["idx"]
        title = toc_indices[i]["title"]
        
        if i < len(toc_indices) - 1:
            end_idx = toc_indices[i+1]["idx"]
        else:
            end_idx = len(compressed_text)
            
        chunk = compressed_text[start_idx:end_idx]
        
        answers = []
        matches = re.finditer(r'정답([①②③④⑤])', chunk)
        for m in matches:
            answers.append(ans_map[m.group(1)])
            
        results.append(f"'{title}': {answers},")
        
    return "\n".join(results)

st.title("컴팩트기출 정답 자동 추출기 (교재 전체 통합본)")

book_choice = st.selectbox(
    "교재를 선택하세요", 
    ["1권 형법 총론", "2권 형법 각론", "3권 수사증거", "4권 형사절차"]
)

toc_map = {
    "1권 형법 총론": TOC_BOOK1,
    "2권 형법 각론": TOC_BOOK2,
    "3권 수사증거": TOC_BOOK3,
    "4권 형사절차": TOC_BOOK4
}

uploaded_file = st.file_uploader("TXT 파일 업로드", type="txt")

if uploaded_file is not None:
    if st.button("정답 추출 시작"):
        with st.spinner(f"{book_choice} 목차에 맞춰 정답을 소팅하는 중입니다..."):
            string_data = uploaded_file.getvalue().decode("utf-8")
            selected_toc = toc_map[book_choice]
            result_text = extract_answers_by_book(string_data, selected_toc)
            
            st.success("추출 완료! 아래 텍스트를 복사해서 코드에 붙여넣으세요.")
            st.text_area("추출된 정답 DB", result_text, height=400)
