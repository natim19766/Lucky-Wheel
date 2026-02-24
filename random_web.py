import streamlit as st
import streamlit.components.v1 as components
import random

# ตั้งค่าหน้าเว็บให้เหมือนเว็บแอป
st.set_page_config(page_title="Wheel of Names Clone", layout="wide", page_icon="🎡")

# 1. ส่วนของ CSS ตกแต่ง Layout ให้เหมือนต้นฉบับ
st.markdown("""
<style>
    /* ปรับพื้นหลังและฟอนต์ */
    .main { background-color: #ffffff; }
    
    /* สไตล์ของ Layout หลัก */
    .container { display: flex; flex-direction: row; gap: 20px; }
    
    /* สไตล์ลูกศรชี้ (อยู่ด้านขวาของวงล้อ) */
    .pointer-container {
        position: absolute;
        right: -10px;
        top: 50%;
        transform: translateY(-50%);
        width: 0; height: 0;
        border-top: 25px solid transparent;
        border-bottom: 25px solid transparent;
        border-right: 40px solid #FFD700; /* สีทอง */
        filter: drop-shadow(2px 2px 5px rgba(0,0,0,0.3));
        z-index: 100;
    }

    /* Popup ผู้ชนะ */
    .modal-overlay {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0,0,0,0.85); display: none;
        justify-content: center; align-items: center; z-index: 9999;
    }
    .modal-content {
        background: white; padding: 50px; border-radius: 20px;
        text-align: center; max-width: 500px; width: 90%;
        animation: pop 0.4s cubic-bezier(0.68, -0.55, 0.27, 1.55);
    }
    @keyframes pop { from { transform: scale(0); } to { transform: scale(1); } }

    /* ปุ่มสไตล์สวยๆ */
    .stButton>button {
        width: 100%; border-radius: 10px; height: 45px;
        font-weight: bold; text-transform: uppercase;
    }
</style>
""", unsafe_allow_html=True)

# 2. ส่วนเมนูด้านข้าง (Sidebar/Input)
with st.sidebar:
    st.subheader("รายการชื่อ")
    input_names = st.text_area("ใส่ชื่อ (1 ชื่อต่อบรรทัด)", 
                              "Ali\nBeatriz\nCharles\nDiya\nEric\nFatima\nGabriel\nHanna", 
                              height=400)
    
    name_list = [n.strip() for n in input_names.split('\n') if n.strip()]
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🔀 สลับชื่อ"):
            random.shuffle(name_list)
            # หมายเหตุ: ใน Streamlit การ Shuffle text_area ต้องอาศัย session_state แต่เบื้องต้นให้รันใหม่ได้
    with col_btn2:
        if st.button("🗑️ ล้างทั้งหมด"):
            name_list = []

# 3. ส่วนการแสดงผลวงล้อ (Main Area)
if len(name_list) > 0:
    wheel_html = f"""
    <div style="position: relative; width: 600px; margin: auto; display: flex; justify-content: center;">
        <div class="pointer-container"></div>
        
        <canvas id="wheel" width="550" height="550"></canvas>
    </div>

    <div style="text-align: center; margin-top: 30px;">
        <button onclick="spinWheel()" style="background: #ff4b4b; color: white; border: none; padding: 15px 60px; font-size: 24px; border-radius: 50px; cursor: pointer; box-shadow: 0 4px 15px rgba(255,75,75,0.4);">
            กดเพื่อหมุน หรือกด Ctrl + Enter
        </button>
    </div>

    <div id="winnerModal" class="modal-overlay">
        <div class="modal-content">
            <h3 style="color: #666;">ผู้โชคดีคือ...</h3>
            <h1 id="winnerName" style="font-size: 4em; color: #ff4b4b; margin: 20px 0;"></h1>
            <button onclick="closeModal()" style="background: #36A2EB; color: white; border: none; padding: 10px 40px; border-radius: 10px; cursor: pointer;">ปิด</button>
        </div>
    </div>

    <script>
        const names = {name_list};
        const colors = ['#3366cc', '#dc3912', '#ff9900', '#109618', '#990099', '#3b3eac', '#0099c6', '#dd4477'];
        const canvas = document.getElementById('wheel');
        const ctx = canvas.getContext('2d');
        let currentAngle = 0;

        function draw() {{
            const arc = (Math.PI * 2) / names.length;
            names.forEach((name, i) => {{
                const angle = currentAngle + i * arc;
                ctx.fillStyle = colors[i % colors.length];
                ctx.beginPath();
                ctx.moveTo(275, 275);
                ctx.arc(275, 275, 260, angle, angle + arc);
                ctx.fill();
                ctx.save();
                ctx.translate(275 + Math.cos(angle + arc/2) * 180, 275 + Math.sin(angle + arc/2) * 180);
                ctx.rotate(angle + arc/2);
                ctx.fillStyle = "white";
                ctx.font = "bold 22px Arial";
                ctx.fillText(name, 0, 0);
                ctx.restore();
            }});
        }}

        function spinWheel() {{
            let start = null;
            const duration = 5000;
            const totalRotation = Math.PI * 2 * (10 + Math.random() * 5);

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
                    const finalAngle = currentAngle % (Math.PI * 2);
                    const arc = (Math.PI * 2) / names.length;
                    // คำนวณผู้ชนะตามตำแหน่งลูกศรด้านขวา (0 องศา)
                    const index = Math.floor((names.length - (finalAngle / arc)) % names.length);
                    showWinner(names[index]);
                }}
            }}
            requestAnimationFrame(animate);
        }}

        function showWinner(name) {{
            document.getElementById('winnerName').innerText = name;
            document.getElementById('winnerModal').style.display = 'flex';
        }}

        function closeModal() {{
            document.getElementById('winnerModal').style.display = 'none';
        }}

        draw();
    </script>
    """
    components.html(wheel_html, height=800)
else:
    st.info("กรุณาใส่รายชื่อที่เมนูด้านข้างก่อนครับ")
