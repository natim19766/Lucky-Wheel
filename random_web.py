import streamlit as st
import streamlit.components.v1 as components
import random

st.set_page_config(page_title="Wheel of Names", layout="wide")

# --- 1. ระบบจัดการรายชื่อ (Session State) ---
if 'names_input' not in st.session_state:
    st.session_state.names_input = "Ali\nBeatriz\nCharles\nDiya\nEric\nFatima\nGabriel\nHanna"

def shuffle_names():
    names = st.session_state.names_input.split('\n')
    names = [n.strip() for n in names if n.strip()]
    random.shuffle(names)
    st.session_state.names_input = "\n".join(names)

def clear_names():
    st.session_state.names_input = ""

# --- 2. ส่วนเมนูด้านซ้าย (Sidebar) ---
with st.sidebar:
    st.header("รายการชื่อ")
    # ช่องกรอกชื่อ
    input_text = st.text_area("1 ชื่อต่อบรรทัด", 
                              value=st.session_state.names_input, 
                              height=400, 
                              key="names_area")
    st.session_state.names_input = input_text

    # ปุ่มกดใต้รายการชื่อ
    col1, col2 = st.columns(2)
    with col1:
        st.button("🔀 สลับชื่อ", on_click=shuffle_names, use_container_width=True)
    with col2:
        st.button("🗑️ ล้างข้อมูล", on_click=clear_names, use_container_width=True)

    name_list = [n.strip() for n in st.session_state.names_input.split('\n') if n.strip()]

# --- 3. ส่วนแสดงผลวงล้อ (Main Content) ---
if name_list:
    # แก้ไข Syntax Error โดยการเช็คการปิด f""" ให้ครบถ้วน
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {{ font-family: sans-serif; display: flex; flex-direction: column; align-items: center; background: #fff; margin: 0; }}
        .wheel-container {{ position: relative; width: 550px; height: 550px; margin-top: 20px; }}
        
        /* ลูกศรชี้ด้านข้างสีทอง */
        .pointer {{
            position: absolute; right: -15px; top: 50%; transform: translateY(-50%);
            width: 0; height: 0; border-top: 20px solid transparent; border-bottom: 20px solid transparent;
            border-right: 45px solid #FFD700; z-index: 100;
        }}

        #spin-btn {{
            margin-top: 30px; padding: 15px 60px; font-size: 24px; font-weight: bold;
            background: #ff4b4b; color: white; border: none; border-radius: 50px;
            cursor: pointer; box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }}

        /* Popup ผู้ชนะ */
        #modal {{
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.85); display: none; justify-content: center; align-items: center; z-index: 1000;
        }}
        .modal-content {{ background: white; padding: 50px; border-radius: 25px; text-align: center; min-width: 350px; }}
        .winner-name {{ color: #ff4b4b; font-size: 4rem; font-weight: bold; margin: 20px 0; }}
    </style>
    </head>
    <body>

    <div class="wheel-container">
        <div class="pointer"></div>
        <canvas id="wheel" width="550" height="550"></canvas>
    </div>
    <button id="spin-btn" onclick="spin()">กดเพื่อหมุน!</button>

    <div id="modal">
        <div class="modal-content">
            <h2 style="color:#666">ยินดีด้วย!</h2>
            <div id="winner-display" class="winner-name"></div>
            <button onclick="closeModal()" style="padding:10px 30px; cursor:pointer">ปิด</button>
        </div>
    </div>

    <script>
        const names = {name_list};
        const colors = ['#e74c3c', '#3498db', '#f1c40f', '#2ecc71', '#9b59b6', '#e67e22', '#1abc9c', '#34495e'];
        const canvas = document.getElementById('wheel');
        const ctx = canvas.getContext('2d');
        let currentAngle = 0;

        function draw() {{
            const arc = (Math.PI * 2) / names.length;
            ctx.clearRect(0,0,550,550);
            names.forEach((name, i) => {{
                const angle = currentAngle + i * arc;
                ctx.fillStyle = colors[i % colors.length];
                ctx.beginPath(); ctx.moveTo(275, 275);
                ctx.arc(275, 275, 260, angle, angle + arc);
                ctx.fill(); ctx.stroke();
                ctx.save();
                ctx.translate(275 + Math.cos(angle + arc/2) * 180, 275 + Math.sin(angle + arc/2) * 180);
                ctx.rotate(angle + arc/2);
                ctx.fillStyle = "white"; ctx.font = "bold 18px Arial"; ctx.textAlign = "center";
                ctx.fillText(name, 0, 0);
                ctx.restore();
            }});
        }}

        function spin() {{
            let duration = 5000;
            let start = null;
            let totalRotation = Math.PI * 2 * (10 + Math.random() * 5);
            function animate(now) {{
                if (!start) start = now;
                const elapsed = now - start;
                const progress = Math.min(elapsed / duration, 1);
                const easeOut = 1 - Math.pow(1 - progress, 3);
                currentAngle = easeOut * totalRotation;
                draw();
                if (progress < 1) {{ requestAnimationFrame(animate); }}
                else {{
                    const arc = (Math.PI * 2) / names.length;
                    const index = Math.floor((names.length - (currentAngle % (Math.PI * 2) / arc)) % names.length);
                    document.getElementById('winner-display').innerText = names[index];
                    document.getElementById('modal').style.display = 'flex';
                }}
            }}
            requestAnimationFrame(animate);
        }}

        function closeModal() {{ document.getElementById('modal').style.display = 'none'; }}
        draw();
    </script>
    </body>
    </html>
    """
    # ปิด f-string ด้วยเครื่องหมาย """ ให้เรียบร้อย
    components.html(html_code, height=800)
else:
    st.info("กรุณาใส่ชื่อที่เมนูด้านซ้าย")
