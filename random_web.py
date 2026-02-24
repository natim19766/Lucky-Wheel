import streamlit as st
import streamlit.components.v1 as components
import random

st.set_page_config(page_title="Wheel of Names", layout="wide")

# --- 1. ระบบจัดการ Session State (ล็อกค่าไม่ให้หาย) ---
if 'names_input' not in st.session_state:
    st.session_state.names_input = "Ali\nBeatriz\nCharles\nDiya\nEric\nFatima\nGabriel\nHanna"

# ฟังก์ชันจัดการปุ่ม
def handle_shuffle():
    names = st.session_state.names_input.split('\n')
    names = [n.strip() for n in names if n.strip()]
    random.shuffle(names)
    st.session_state.names_input = "\n".join(names)

def handle_clear():
    st.session_state.names_input = ""

# --- 2. ส่วนของ Sidebar (เมนูซ้ายมือ) ---
with st.sidebar:
    st.header("รายการชื่อ")
    
    # ช่องกรอกชื่อ (เชื่อมกับ Session State)
    # ใช้ key="names_area" เพื่อให้ Streamlit จำค่าได้แม่นยำ
    names_area = st.text_area(
        "1 ชื่อต่อบรรทัด", 
        value=st.session_state.names_input, 
        height=400, 
        key="main_input"
    )
    
    # อัปเดตค่ากลับเข้า State เมื่อมีการพิมพ์
    st.session_state.names_input = names_area

    # ปุ่มกดใต้รายการชื่อ
    col1, col2 = st.columns(2)
    with col1:
        st.button("🔀 สลับชื่อ", on_click=handle_shuffle, use_container_width=True)
    with col2:
        st.button("🗑️ ล้างข้อมูล", on_click=handle_clear, use_container_width=True)

    # รายชื่อที่จะส่งไปที่วงล้อ
    name_list = [n.strip() for n in st.session_state.names_input.split('\n') if n.strip()]

# --- 3. ส่วนแสดงผลวงล้อ (ฝั่งขวา) ---
if name_list:
    # ระวัง: f-string ต้องเปิดด้วย f""" และปิดด้วย """ ให้ครบถ้วน
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; display: flex; flex-direction: column; align-items: center; background: white; margin: 0; overflow: hidden; }}
        .wheel-box {{ position: relative; width: 550px; height: 550px; margin-top: 20px; }}
        
        /* ลูกศรสีทองชี้จากทางขวา */
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

        /* Popup ผู้ชนะ */
        #modal {{
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.85); display: none; justify-content: center; align-items: center; z-index: 1000;
        }}
        .modal-content {{
            background: white; padding: 50px; border-radius: 25px; text-align: center;
            min-width: 350px; box-shadow: 0 0 30px rgba(0,0,0,0.5);
        }}
        .winner-name {{ color: #ff4b4b; font-size: 4rem; font-weight: bold; margin: 20px 0; }}
    </style>
    </head>
    <body>

    <div class="wheel-box">
        <div class="arrow"></div>
        <canvas id="wheel" width="550" height="550"></canvas>
    </div>

    <button id="spin-btn" onclick="spin()">กดเพื่อหมุน!</button>

    <div id="modal">
        <div class="modal-content">
            <h2 style="color: #666;">ยินดีด้วย! ผู้ชนะคือ</h2>
            <div id="winner-text" class="winner-name"></div>
            <button onclick="closeModal()" style="padding: 10px 30px; cursor: pointer; border-radius: 10px;">ปิด</button>
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
                ctx.beginPath();
                ctx.moveTo(275, 275);
                ctx.arc(275, 275, 260, angle, angle + arc);
                ctx.fill();
                ctx.stroke();

                ctx.save();
                ctx.translate(275 + Math.cos(angle + arc/2) * 180, 275 + Math.sin(angle + arc/2) * 180);
                ctx.rotate(angle + arc/2);
                ctx.fillStyle = "white";
                ctx.font = "bold 18px Arial";
                ctx.textAlign = "center";
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

                if (progress < 1) {{
                    requestAnimationFrame(animate);
                }} else {{
                    const arc = (Math.PI * 2) / names.length;
                    const normalizedAngle = (currentAngle % (Math.PI * 2));
                    // 0 องศาคือด้านขวาที่ลูกศรชี้
                    const index = Math.floor((names.length - (normalizedAngle / arc)) % names.length);
                    
                    document.getElementById('winner-text').innerText = names[index];
                    document.getElementById('modal').style.display = 'flex';
                }}
            }}
            requestAnimationFrame(animate);
        }}

        function closeModal() {{
            document.getElementById('modal').style.display = 'none';
        }}

        draw();
    </script>
    </body>
    </html>
    """
    # ปิด f-string ด้วยเครื่องหมายฟันหนู 3 อันเสมอ
    components.html(html_code, height=800)
else:
    st.info("กรุณาใส่รายชื่อที่แถบด้านซ้ายเพื่อเริ่มสนุก!")
