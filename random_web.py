import streamlit as st
import streamlit.components.v1 as components
import random
# --- ส่วนของโค้ดตกแต่ง (CSS) ---
st.markdown("""
<style>
/* สำหรับหน้าจอปกติ (คอมพิวเตอร์) */
.main-layout {
    display: flex;
    flex-direction: row; 
}

/* สำหรับมือถือ (หน้าจอแคบกว่า 768px) */
@media (max-width: 768px) {
    .main-layout {
        flex-direction: column; /* เปลี่ยนจากแนวนอนเป็นแนวตั้ง */
    }
    
    .wheel-container {
        width: 80vw; /* ปรับขนาดวงล้อให้พอดีกับหน้าจอมือถือ */
    }
}
</style>
""", unsafe_allow_html=True)
st.set_page_config(page_title="Lucky Wheel", page_icon="🎡")
st.title("🎡 วงล้อเสี่ยงโชค (Animated Wheel)")

# ส่วนรับข้อมูลชื่อ
names_input = st.text_input("ใส่ชื่อรายการ (คั่นด้วยจุลภาค ,)", "รางวัลที่ 1, รางวัลที่ 2, แห้ว, โชคดี, ลองใหม่")
names = [n.strip() for n in names_input.split(",")]

# สร้างสีสุ่มให้แต่ละช่องของวงล้อ
colors = ["#ff595e", "#ffca3a", "#8ac926", "#1982c4", "#6a4c93"]

# โค้ด HTML + JavaScript สำหรับสร้างวงล้อหมุน
wheel_html = f"""
<div class="wheel-container" style="text-align:center;">
    <canvas id="wheel" width="400" height="400"></canvas>
    <br>
    <button onclick="spin()" style="padding: 15px 30px; font-size: 20px; cursor: pointer; background: #2ecc71; color: white; border: none; border-radius: 10px; margin-top: 20px;">หมุนเลย!</button>
    <h2 id="winner" style="color: #2c3e50; font-family: sans-serif;"></h2>
</div>

<script>
    const names = {names};
    const colors = {colors};
    const canvas = document.getElementById('wheel');
    const ctx = canvas.getContext('2d');
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const radius = 180;

    let startAngle = 0;
    const arc = Math.PI / (names.length / 2);

    function drawWheel() {{
        names.forEach((name, i) => {{
            const angle = startAngle + i * arc;
            ctx.fillStyle = colors[i % colors.length];
            ctx.beginPath();
            ctx.moveTo(centerX, centerY);
            ctx.arc(centerX, centerY, radius, angle, angle + arc);
            ctx.lineTo(centerX, centerY);
            ctx.fill();
            
            ctx.save();
            ctx.fillStyle = "white";
            ctx.translate(centerX + Math.cos(angle + arc / 2) * radius * 0.7, centerY + Math.sin(angle + arc / 2) * radius * 0.7);
            ctx.rotate(angle + arc / 2 + Math.PI / 2);
            ctx.fillText(name, -ctx.measureText(name).width / 2, 0);
            ctx.restore();
        }});
    }}

    function spin() {{
        let spinAngleStart = Math.random() * 10 + 10;
        let spinTime = 0;
        let spinTimeTotal = Math.random() * 3 + 4 * 1000;

        function rotateWheel() {{
            spinTime += 30;
            if (spinTime >= spinTimeTotal) {{
                const index = Math.floor(names.length - (startAngle % (Math.PI * 2)) / (Math.PI * 2) * names.length) % names.length;
                document.getElementById('winner').innerHTML = "ผลที่ได้คือ: " + names[index];
                return;
            }}
            const spinAngle = spinAngleStart - (spinTime / spinTimeTotal) * spinAngleStart;
            startAngle += (spinAngle * Math.PI / 180);
            drawWheel();
            requestAnimationFrame(rotateWheel);
        }}
        rotateWheel();
    }}
    drawWheel();
</script>
"""

# แสดงผลวงล้อใน Streamlit
components.html(wheel_html, height=600)

st.info("💡 เคล็ดลับ: คุณสามารถเปลี่ยนชื่อในช่องด้านบน แล้ววงล้อจะอัปเดตเองทันที!")
