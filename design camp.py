import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(layout="wide")

# -----------------------------
# TITLE
# -----------------------------

st.title("Pile Cap Reaction Calculator")

st.success(
"""
จงหาแรงปฏิกิริยาของเสาเข็ม เนื่องจากเกิดการเยื้องศูนย์ดังแสดงในรูป
เมื่อกำหนดให้เสาเข็มรับน้ำหนักปลอดภัย 40 ตัน/ต้น
และเกิดน้ำหนักกระทำต่อฐานราก เท่ากับ 150 ตัน
"""
)

# -----------------------------
# INPUT
# -----------------------------

st.subheader("📌 ข้อมูลนำเข้า")

c1,c2,c3 = st.columns(3)

with c1:
    P = st.number_input("น้ำหนักรวม P (ตัน)", value=150.0)

with c2:
    ex = st.number_input("ระยะเยื้องศูนย์ X (cm)", value=2.0)

with c3:
    ey = st.number_input("ระยะเยื้องศูนย์ Y (cm)", value=3.0)

st.info("ขนาดฐานราก (Pile Cap) = 120 cm (X) × 190 cm (Y)")

# -----------------------------
# PILE DATA
# -----------------------------

piles = {
"P1":(-60,95),
"P2":(60,95),
"P3":(-60,-95),
"P4":(60,-95)
}

n = len(piles)

Ix = sum([y**2 for x,y in piles.values()])
Iy = sum([x**2 for x,y in piles.values()])

# -----------------------------
# CALCULATION
# -----------------------------

data=[]

for name,(x,y) in piles.items():

    R = P/n + (P*ey*x)/Iy + (P*ex*y)/Ix

    status="SAFE"

    if R>40:
        status="OVER"

    data.append([name,x,y,round(R,2),status])

df = pd.DataFrame(
data,
columns=["เสาเข็ม","X","Y","แรงปฏิกิริยา (ตัน)","สถานะ"]
)

# -----------------------------
# LAYOUT
# -----------------------------

left,right = st.columns([1,1])

# -----------------------------
# TABLE
# -----------------------------

with left:

    st.subheader("📊 ผลการคำนวณแรงปฏิกิริยาเสาเข็ม")

    st.dataframe(df,use_container_width=True)

    maxR = df["แรงปฏิกิริยา (ตัน)"].max()

    if maxR > 40:
        st.error(f"แรงปฏิกิริยามากที่สุด = {maxR} ตัน/ต้น  (เกินค่าปลอดภัย 40)")
    else:
        st.success(f"แรงปฏิกิริยามากที่สุด = {maxR} ตัน/ต้น  (SAFE)")

    st.markdown("### สรุปผล")

    st.write(f"- ค่ารับน้ำหนักปลอดภัยเสาเข็ม = 40 ตัน/ต้น")
    st.write(f"- น้ำหนักกระทำรวม P = {P} ตัน")
    st.write(f"- ex = {ex} cm")
    st.write(f"- ey = {ey} cm")

    if maxR > 40:
        st.error("❌ ผลการออกแบบ : ไม่ปลอดภัย")
    else:
        st.success("✔ ผลการออกแบบ : ปลอดภัย")


# -----------------------------
# DRAW DIAGRAM
# -----------------------------

with right:

    st.subheader("🗺 แผนผังฐานรากและตำแหน่งเสาเข็ม")

    fig,ax = plt.subplots()

    width = 120
    height = 190

    rect = plt.Rectangle((-60,-95),120,190,fill=False,linewidth=2)

    ax.add_patch(rect)

    for name,(x,y) in piles.items():

        ax.scatter(x,y,s=300)

        ax.text(x,y-10,name,ha="center")

    ax.axhline(0,linestyle="--")
    ax.axvline(0,linestyle="--")

    ax.text(0,100,"120 cm",ha="center")
    ax.text(-70,0,"190 cm",rotation=90)

    ax.set_xlim(-80,80)
    ax.set_ylim(-120,120)

    ax.set_aspect("equal")

    ax.set_xticks([])
    ax.set_yticks([])

    st.pyplot(fig)

st.caption("หมายเหตุ : ระยะทั้งหมดหน่วย cm")
