import streamlit as st
import pdfplumber
import re

def extract_answers_for_grader(pdf_file):
    question_pattern = re.compile(r'^\s*0*(\d{1,3})\s*')
    ans_map = {'①': 1, '②': 2, '③': 3, '④': 4, '⑤': 5}
    
    db_list = []
    current_item = None

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue
                
            for line in text.split('\n'):
                original_line = line.strip()
                compressed_line = original_line.replace(" ", "").replace("\t", "")
                
                clean_line = re.sub(r'^\d+\s+', '', original_line)
                clean_line = re.sub(r'\s+\d+$', '', clean_line)
                clean_line = clean_line.replace("정답 및 해설", "").strip()
                
                if clean_line.upper().startswith(("PART", "CHAPTER", "CHATPER", "SECTION")):
                    if len(clean_line) < 40 and "①" not in clean_line:
                        if current_item is None or current_item['title'] != clean_line:
                            current_item = {"title": clean_line, "ans": []}
                            db_list.append(current_item)
                        continue
                    
                if q_match := question_pattern.search(original_line):
                    current_question = q_match.group(1)
                    
                if "정답" in compressed_line:
                    ans_match = re.search(r'정답.*?([①②③④⑤])', compressed_line)
                    if ans_match and current_item is not None:
                        ans_char = ans_match.group(1)
                        current_item["ans"].append(ans_map[ans_char])
                        current_question = None 

    output_text = ""
    for item in db_list:
        title = item['title']
        ans_list = item['ans']
        output_text += f"'{title}': {ans_list},\n"
            
    return output_text

st.title("컴팩트 기출 정답 자동 추출기 (진짜 최종)")
st.write("PDF 원고를 업로드하면 채점기 코드에 삽입할 DB 배열을 만들어줍니다.")

uploaded_file = st.file_uploader("PDF 파일 업로드", type="pdf")

if uploaded_file is not None:
    if st.button("정답 추출 시작"):
        with st.spinner("순서 꼬임 없이 정답을 소팅하는 중입니다..."):
            result_text = extract_answers_for_grader(uploaded_file)
            st.success("추출 완료! 아래 텍스트를 복사해서 코드에 붙여넣으세요.")
            st.text_area("추출된 정답 DB", result_text, height=400)
