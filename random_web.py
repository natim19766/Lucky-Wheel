import streamlit as st
import streamlit.components.v1 as components
import random

st.set_page_config(page_title="Wheel of Names", layout="wide")

# 1. จัดการ Session State สำหรับรายชื่อ
if 'names_input' not in st.session_state:
    st.session_state.names_input = "Ali\nBeatriz\nCharles\nDiya\nEric\nFatima\nGabriel\nHanna"

# ฟังก์ชันสำหรับปุ่มต่างๆ
def shuffle_names():
    names = st.session_state.names_input.split('\n')
    names = [n.strip() for n in names if n.strip()]
    random.shuffle(names)
    st.session_state.names_input = "\n".join(names)

def clear_names():
    st.session_state.names_input = ""

# 2. ส่วนของ Sidebar (ฝั่งซ้าย)
with st.sidebar:
    st.header("รายการชื่อ")
    
    # ช่องกรอกชื่อที่ผูกกับ Session State
    input_text = st.text_area("1 ชื่อต่อบรรทัด", 
                              value=st.session_state.names_input, 
                              height=400, 
                              key="names_area")
    
    # อัปเดตค่ากลับเข้า State เมื่อมีการพิมพ์
    st.session_state.names_input = input_text

    # วางปุ่มไว้ใต้รายการชื่อ
    col1, col2 = st.columns(2)
    with col1:
        st.button("🔀 สลับชื่อ", on_click=shuffle_names, use_container_width=True)
    with col2:
        st.button("🗑️ ล้างข้อมูล", on_click=clear_names, use_container_width=True)

    name_list = [n.strip() for n in st.session_state.names_input.split('\n') if n.strip()]

# 3. ส่วนแสดงผลวงล้อ (ฝั่งขวา)
if name_list:
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; display: flex; flex-direction: column; align-items: center; background: white; margin: 0; overflow: hidden; }}
        .wheel-box {{ position: relative; width: 550px; height: 550px; margin-top: 20px; }}
        
        /* ลูกศรชี้ด้านข้างสีทอง */
        .arrow {{
            position: absolute; right: -15px; top: 50%; transform: translateY(-50%);
            width: 0; height: 0; 
            border-top: 20px solid transparent; border-bottom: 20px solid transparent;
            border-right: 45px solid #FFD700; z-index: 100;
            filter: drop-shadow(-2px 2px 3px rgba(0,0,0,0.3));
        }}

        button#spin-btn {{
            margin-top: 30px; padding: 15px 60px; font-size: 24px; font-weight: bold;
            background: #ff4b4b; color: white; border: none; border-radius: 50px;
            cursor: pointer; box-shadow: 0 4px 15px rgba(255,75,75,0.4);
        }}

        /* Popup */
        #modal {{
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.85); display:
