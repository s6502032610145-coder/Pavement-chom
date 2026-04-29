import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="Pile Cap Reaction Calculator", layout="wide")

st.title("Pile Cap Reaction Calculator")

st.markdown("""
จงหาแรงปฏิกิริยาของเสาเข็ม เนื่องจากเกิดการเยื้องศูนย์ดังแสดงในรูป  
กำหนดให้เสาเข็มรับน้ำหนักปลอดภัย **40 ตัน/ต้น**  
และน้ำหนักกระทำต่อฐานราก **150 ตัน**
""")

# -----------------------------
# INPUT
# -----------------------------

col1,col2,col3 = st.columns(3)

with col1:
    P = st.number_input("น้ำหนักรวม P (ตัน)", value=150.0)

with col2:
    ex = st.number_input("ระยะเยื้องศูนย์ X (cm)", value=2.0)

with col3:
    ey = st.number_input("ระยะเยื้องศูนย์ Y (cm)", value=3.0)


st.info("ขนาดฐานราก = 120 cm (X) × 190 cm (Y)")


# -----------------------------
# pile coordinates
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
# reaction calculation
# -----------------------------

results = []

for name,(x,y) in piles.items():

    R = P/n + (P*ey*x)/Iy + (P*ex*y)/Ix

    status = "SAFE"
    if R > 40:
        status = "OVER"

    results.append([name,x,y,round(R,2),status])

df = pd.DataFrame(results,columns=["Pile","X","Y","Reaction (ton)","Status"])


# -----------------------------
# layout
# -----------------------------

left,right = st.columns(2)

# -----------------------------
# TABLE
# -----------------------------

with left:

    st.subheader("ผลการคำนวณ")

    st.dataframe(df,use_container_width=True)

    maxR = df["Reaction (ton)"].max()

    if maxR > 40:
        st.error(f"แรงปฏิกิริยามากที่สุด = {maxR} ตัน/ต้น  (เกิน 40)")
    else:
        st.success(f"แรงปฏิกิริยามากที่สุด = {maxR} ตัน/ต้น  (SAFE)")


# -----------------------------
# DIAGRAM
# -----------------------------

with right:

    st.subheader("แผนผังฐานราก")

    fig,ax = plt.subplots()

    width = 120
    height = 190

    rect = plt.Rectangle((-60,-95),120,190,fill=False,linewidth=2)

    ax.add_patch(rect)

    for name,(x,y) in piles.items():

        ax.scatter(x,y,s=200)

        ax.text(x,y-10,name,ha='center')

    ax.axhline(0,linestyle="--")
    ax.axvline(0,linestyle="--")

    ax.set_xlim(-80,80)
    ax.set_ylim(-120,120)

    ax.set_aspect('equal')

    st.pyplot(fig)
