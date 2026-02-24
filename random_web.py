import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Wheel of Names", layout="wide")

# 1. ส่วนของ Sidebar (ฝั่ง Python)
with st.sidebar:
    st.header("รายการชื่อ")
    # ใส่ชื่อเริ่มต้นไว้ให้เลย
    default_names = "Ali\nBeatriz\nCharles\nDiya\nEric\nFatima\nGabriel\nHanna"
    input_names = st.text_area("1 ชื่อต่อบรรทัด", value=default_names, height=400)
    
    # แปลงจาก Text เป็น List สำหรับส่งให้ JavaScript
    name_list = [n.strip() for n in input_names.split('\n') if n.strip()]

# 2. ส่วนแสดงผลวงล้อและปุ่มควบคุม (ฝั่ง HTML/JS)
if name_list:
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; display: flex; justify-content: center; padding-top: 20px; background-color: white; }}
        .main-layout {{ display: flex; gap: 50px; align-items: flex-start; }}
        
        .wheel-box {{ position: relative; width: 550px; height: 550px; }}
        
        /* ลูกศรชี้ด้านข้าง (สีทอง) */
        .arrow {{
            position: absolute; right: -10px; top: 50%; transform: translateY(-50%);
            width: 0; height: 0; 
            border-top: 20px solid transparent; border-bottom: 20px solid transparent;
            border-right: 40px solid #FFD700; z-index: 100;
        }}

        .controls {{ display: flex; flex-direction: column; gap: 10px; align-items: center; }}
        
        button {{
            padding: 12px 25px; border: none; border-radius: 5px; cursor: pointer;
            font-weight: bold; font-size: 16px; width: 150px;
        }}
        .btn-spin {{ background: #ff4b4b; color: white; font-size: 20px; width: 200px; border-radius: 50px; }}
        .btn-shuffle {{ background: #3498db; color: white; }}

        /* Popup ผู้ชนะ */
        #winner-modal {{
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.8); display: none; justify-content: center; align-items: center; z-index: 1000;
        }}
        .modal-content {{
            background: white; padding: 50px; border-radius: 20px; text-align: center;
            box-shadow: 0 0 30px rgba(0,0,0,0.5); min-width: 350px;
        }}
        .winner-name {{ color: #ff4b4b; font-size: 4rem; font-weight: bold; margin: 20px 0; }}
    </style>
    </head>
    <body>

    <div class="main-layout">
        <div class="wheel-box">
            <div class="arrow"></div>
            <canvas id="wheel" width="550" height="550"></canvas>
        </div>

        <div class="controls">
            <button class="btn-spin" onclick="spin()">หมุน!</button>
            <button class="btn-shuffle" onclick="shuffleNames()">🔀 สลับชื่อ</button>
        </div>
    </div>

    <div id="winner-modal">
        <div class="modal-content">
            <h2 style="color: #666;">ผู้ชนะคือ...</h2>
            <div id="winner-text" class="winner-name"></div>
            <button onclick="closeModal()" style="background:#ddd; width: 100px;">ปิด</button>
        </div>
    </div>

    <script>
        let items = {name_list};
        const colors = ['#e74c3c', '#3498db', '#f1c40f', '#2ecc71', '#9b59b6', '#e67e22', '#1abc9c', '#34495e'];
        const canvas = document.getElementById('wheel');
        const ctx = canvas.getContext('2d');
        let currentAngle = 0;

        function draw() {{
            const arc = (Math.PI * 2) / items.length;
            ctx.clearRect(0,0,550,550);
            items.forEach((name, i) => {{
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
                ctx.font = "bold 20px Arial";
                ctx.textAlign = "center";
                ctx.fillText(name, 0, 0);
                ctx.restore();
            }});
        }}

        function shuffleNames() {{
            for (let i = items.length - 1; i > 0; i--) {{
                const j = Math.floor(Math.random() * (i + 1));
                [items[i], items[j]] = [items[j], items[i]];
            }}
            draw();
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
                    const arc = (Math.PI * 2) / items.length;
                    const normalizedAngle = (currentAngle % (Math.PI * 2));
                    // 0 องศาคือด้านขวาที่ลูกศรชี้
                    const index = Math.floor((items.length - (normalizedAngle / arc)) % items.length);
                    
                    document.getElementById('winner-text').innerText = items[index];
                    document.getElementById('winner-modal').style.display = 'flex';
                }}
            }}
            requestAnimationFrame(animate);
        }}

        function closeModal() {{
            document.getElementById('winner-modal').style.display = 'none';
        }}

        draw();
    </script>
    </body>
    </html>
    """
    components.html(html_code, height=700)
else:
    st.warning("กรุณาใส่ชื่อที่แถบด้านซ้ายก่อนครับ")
