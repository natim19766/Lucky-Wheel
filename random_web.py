import streamlit as st
import streamlit.components.v1 as components
import random

st.set_page_config(page_title="Wheel of Names Clone", layout="wide")

# ส่วนเมนูด้านข้าง
with st.sidebar:
    st.header("รายการชื่อ")
    input_names = st.text_area("ใส่ชื่อ (1 ชื่อต่อบรรทัด)", 
                              "Ali\nBeatriz\nCharles\nDiya\nEric\nFatima\nGabriel\nHanna", 
                              height=400)
    name_list = [n.strip() for n in input_names.split('\n') if n.strip()]

# ส่วนแสดงผลหลัก
if len(name_list) > 0:
    # เราจะรวม HTML, CSS และ JS ไว้ในก้อนเดียวเพื่อให้ทำงานร่วมกันได้แม่นยำ
    wheel_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {{ font-family: sans-serif; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; overflow: hidden; }}
        
        .wheel-wrapper {{
            position: relative;
            width: 500px;
            height: 500px;
        }}

        /* --- ลูกศรชี้ (Pointer) --- */
        .arrow {{
            position: absolute;
            right: -20px;
            top: 50%;
            transform: translateY(-50%);
            width: 0; 
            height: 0; 
            border-top: 25px solid transparent;
            border-bottom: 25px solid transparent;
            border-right: 50px solid #FFD700; /* สีทองชี้จากขวาเข้าหาล้อ */
            z-index: 100;
            filter: drop-shadow(-2px 2px 3px rgba(0,0,0,0.5));
        }}

        /* --- Popup (Modal) --- */
        #modal {{
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.8); display: none;
            justify-content: center; align-items: center; z-index: 1000;
        }}
        .modal-content {{
            background: white; padding: 40px; border-radius: 20px;
            text-align: center; box-shadow: 0 0 20px rgba(255,255,255,0.2);
            min-width: 300px;
        }}
        .winner-name {{ color: #ff4b4b; font-size: 3rem; margin: 20px 0; font-weight: bold; }}
        
        button#spin-btn {{
            margin-top: 20px; padding: 15px 40px; font-size: 20px;
            background: #ff4b4b; color: white; border: none; border-radius: 50px;
            cursor: pointer; transition: 0.2s;
        }}
        button#spin-btn:hover {{ background: #ff2b2b; transform: scale(1.05); }}
    </style>
    </head>
    <body>

    <div class="wheel-wrapper">
        <div class="arrow"></div>
        <canvas id="wheel" width="500" height="500"></canvas>
    </div>

    <button id="spin-btn" onclick="spin()">กดเพื่อหมุน!</button>

    <div id="modal">
        <div class="modal-content">
            <h2>ยินดีด้วย! ผู้ชนะคือ</h2>
            <div id="winner-text" class="winner-name"></div>
            <button onclick="closeModal()" style="padding: 10px 20px; cursor:pointer;">ตกลง</button>
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
            ctx.clearRect(0,0,500,500);
            names.forEach((name, i) => {{
                const angle = currentAngle + i * arc;
                ctx.fillStyle = colors[i % colors.length];
                ctx.beginPath();
                ctx.moveTo(250, 250);
                ctx.arc(250, 250, 240, angle, angle + arc);
                ctx.fill();
                ctx.stroke();

                ctx.save();
                ctx.translate(250 + Math.cos(angle + arc/2) * 160, 250 + Math.sin(angle + arc/2) * 160);
                ctx.rotate(angle + arc/2);
                ctx.fillStyle = "white";
                ctx.font = "bold 20px Arial";
                ctx.textAlign = "center";
                ctx.fillText(name, 0, 0);
                ctx.restore();
            }});
        }}

        function spin() {{
            let duration = 4000;
            let start = null;
            let totalRotation = Math.PI * 2 * (8 + Math.random() * 5);

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
                    // คำนวณผู้ชนะ (ตำแหน่ง 0 องศาคือด้านขวาที่ลูกศรชี้)
                    const normalizedAngle = (currentAngle % (Math.PI * 2));
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
    # ขยาย height เป็น 800 เพื่อให้ Popup ไม่โดนตัดขอบ
    components.html(wheel_html, height=800)
else:
    st.info("เพิ่มชื่อที่ด้านซ้ายเพื่อเริ่มสนุก!")
