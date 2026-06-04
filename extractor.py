import streamlit as st
import re

def extract_answers_from_txt(text):
    question_pattern = re.compile(r'^\s*0*(\d{1,3})\s*')
    ans_map = {'①': 1, '②': 2, '③': 3, '④': 4, '⑤': 5}
    
    hierarchy_pattern = re.compile(r'^(PART\s*[ⅠⅡⅢⅣⅤⅥ]+|CHAPTER\s*\d+|CHATPER\s*\d+|SECTION\s*\d+|\d+-\d+)', re.IGNORECASE)
    
    db_list = []
    current_item = None
    current_question = None

    for line in text.split('\n'):
        original_line = line.strip()
        compressed_line = original_line.replace(" ", "").replace("\t", "")
        
        clean_line = re.sub(r'^\d+\s+', '', original_line)
        clean_line = re.sub(r'\s+\d+$', '', clean_line)
        clean_line = clean_line.replace("정답 및 해설", "").strip()
        
        if hierarchy_pattern.match(clean_line):
            if len(clean_line) < 40 and "①" not in clean_line:
                clean_title = re.sub(r'\s+', ' ', clean_line).strip()
                if current_item is None or current_item['title'] != clean_title:
                    current_item = {"title": clean_title, "ans": []}
                    db_list.append(current_item)
                continue
            
        if q_match := question_pattern.search(original_line):
            current_question = q_match.group(1)
            
        if "정답" in compressed_line:
            ans_match = re.search(r'정답.*?([①②③④⑤])', compressed_line)
            if ans_match and current_question:
                if current_item is None:
                    current_item = {"title": "기본_분류안됨", "ans": []}
                    db_list.append(current_item)
                    
                ans_char = ans_match.group(1)
                current_item["ans"].append(ans_map[ans_char])
                current_question = None 

    output_text = ""
    for item in db_list:
        title = item['title']
        ans_list = item['ans']
        output_text += f"'{title}': {ans_list},\n"
        
    return output_text

st.title("텍스트 파일 정답 자동 추출기")
st.write("원고 텍스트를 메모장에 붙여넣고 txt 파일로 저장한 뒤 업로드하세요.")

uploaded_file = st.file_uploader("TXT 파일 업로드", type="txt")

if uploaded_file is not None:
    if st.button("정답 추출 시작"):
        with st.spinner("텍스트에서 정답을 소팅하는 중입니다..."):
            string_data = uploaded_file.getvalue().decode("utf-8")
            result_text = extract_answers_from_txt(string_data)
            
            st.success("추출 완료! 아래 텍스트를 복사해서 코드에 붙여넣으세요.")
            st.text_area("추출된 정답 DB", result_text, height=400)
