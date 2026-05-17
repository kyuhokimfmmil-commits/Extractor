import streamlit as st
import pdfplumber
import re

def extract_answers_for_grader(pdf_file):
    part_pattern = re.compile(r'PART\s+[ⅠⅡⅢⅣⅤⅥ]+[\s\.]+(.*)')
    chapter_pattern = re.compile(r'(?:CHAPTER|CHATPER)\s+\d+[\s\.]+(.*)')
    section_pattern = re.compile(r'SECTION\s+\d+(?:-\d+)?[\s\.]+(.*)')
    
    question_pattern = re.compile(r'^(\d{3})')
    answer_pattern = re.compile(r'정답\s*([①②③④⑤])')
    
    ans_map = {'①': 1, '②': 2, '③': 3, '④': 4, '⑤': 5}
    
    current_hierarchy = "기본_분류안됨"
    db_answers = {}
    current_question = None

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue
                
            for line in text.split('\n'):
                line = line.strip()
                
                if part_pattern.search(line) or chapter_pattern.search(line) or section_pattern.search(line):
                    current_hierarchy = line
                    if current_hierarchy not in db_answers:
                        db_answers[current_hierarchy] = []
                    
                if q_match := question_pattern.search(line):
                    current_question = q_match.group(1)
                    
                if a_match := answer_pattern.search(line):
                    if current_question:
                        ans_char = a_match.group(1)
                        db_answers[current_hierarchy].append(ans_map[ans_char])
                        current_question = None 
                        
    return db_answers

st.title("컴팩트 기출 정답 자동 추출기")
st.write("PDF 원고를 업로드하면 채점기 코드에 삽입할 DB 배열을 만들어줍니다.")

uploaded_file = st.file_uploader("PDF 파일 업로드", type="pdf")

if uploaded_file is not None:
    if st.button("정답 추출 시작"):
        with st.spinner("PDF를 분석하고 정답을 소팅하는 중입니다..."):
            result = extract_answers_for_grader(uploaded_file)
            
            st.success("추출 완료! 아래 텍스트를 복사해서 코드에 붙여넣으세요.")
            
            output_text = ""
            for title, ans_list in result.items():
                if ans_list:
                    output_text += f"'{title}': {ans_list},\n"
                    
            st.text_area("추출된 정답 DB", output_text, height=400)