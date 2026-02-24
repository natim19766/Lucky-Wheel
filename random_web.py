import streamlit as st
import streamlit.components.v1 as components

# 1. ตั้งค่าหน้าเว็บให้กว้างและสวยงาม
st.set_page_config(page_title="Wheel of Names Clone", layout="wide")

# 2. ใส่ CSS ที่คุณต้องการ (เพื่อให้รองรับมือถือและจัดกลาง)
st.markdown("""
<style>
    .main { background-color: #f0f2f6; }
    .wheel-container {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }
    @media (max-width: 768px) {
        .wheel-container { width: 100%; }
    }
</style>
""", unsafe_allow_html=True)

st.title("🎡 วงล้อสุ่มชื่อ (Wheel of Names)")

# 3. ส่วนรับข้อมูลชื่อ (เหมือนเว็บจริง)
col1, col2 = st.columns([1, 2])
with col1:
    names_text = st.text_area("ใส่ชื่อรายการที่นี่ (1 ชื่อต่อ 1 บรรทัด)", 
                             "แจ็ค\nมานี\nชูใจ\nสมชาย\nจอย", height=300)
    names = [n.strip() for n in names_text.split("\n") if n.strip()]

# 4. โค้ด HTML/JS สำหรับวงล้อ (มีเสียงและกราฟิกหมุน)
with col2:
    if len(names) > 0:
        wheel_html = f"""
        <div class="wheel-container">
            <canvas id="wheel" width="500" height="500"></canvas>
            <br>
            <button onclick="spin()" style="padding: 15px 50px; font-size: 24px; border-radius: 30px; border: none; background: #ff4b4b; color: white; cursor: pointer; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">กดหมุน!</button>
            <h1 id="winner-display" style="text-align: center; color: #ff4b4b; margin-top: 20px; font-family: sans-serif;"></h1>
        </div>

        <script>
            const names = {names};
            const colors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'];
            const canvas = document.getElementById('wheel');
            const ctx = canvas.getContext('2d');
            let startAngle = 0;
            const arc = Math.PI / (names.length / 2);

            function drawWheel() {{
                ctx.clearRect(0, 0, 500, 500);
                names.forEach((name, i) => {{
                    const angle = startAngle + i * arc;
                    ctx.fillStyle = colors[i % colors.length];
                    ctx.beginPath();
                    ctx.moveTo(250, 250);
                    ctx.arc(250, 250, 230, angle, angle + arc);
                    ctx.lineTo(250, 250);
                    ctx.fill();
                    ctx.stroke();

                    ctx.save();
                    ctx.translate(250 + Math.cos(angle + arc/2) * 150, 250 + Math.sin(angle + arc/2) * 150);
                    ctx.rotate(angle + arc/2);
                    ctx.fillStyle = "white";
                    ctx.font = "bold 18px Arial";
                    ctx.fillText(name, 0, 0);
                    ctx.restore();
                }});
            }}

            function spin() {{
                let duration = 5000;
                let startTime = null;
                let finalRotation = Math.random() * 360 + 1440; // หมุนอย่างน้อย 4 รอบ

                function animate(timestamp) {{
                    if (!startTime) startTime = timestamp;
                    let progress = timestamp - startTime;
                    let easeOut = 1 - Math.pow(1 - progress / duration, 3);
                    startAngle = (easeOut * finalRotation) * Math.PI / 180;
                    
                    drawWheel();

                    if (progress < duration) {{
                        requestAnimationFrame(animate);
                    }} else {{
                        const index = Math.floor(names.length - (startAngle % (Math.PI * 2)) / (Math.PI * 2) * names.length) % names.length;
                        document.getElementById('winner-display').innerHTML = "✨ ผู้ชนะคือ: " + names[index] + " ✨";
                    }}
                }}
                requestAnimationFrame(animate);
            }}
            drawWheel();
        </script>
        """
        components.html(wheel_html, height=700)
    else:
        st.warning("กรุณาใส่ชื่ออย่างน้อย 1 ชื่อครับ")
