import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.title("Pile Cap Reaction Calculator")

st.write("Pile Cap Size : 120 cm × 190 cm")
st.write("Pile Capacity : 40 ton / pile")

# -----------------------------
# INPUT
# -----------------------------

P = st.number_input("Total Load P (ton)", value=150.0)
ex = st.number_input("Eccentricity ex (cm)", value=0.0)
ey = st.number_input("Eccentricity ey (cm)", value=0.0)

capacity = 40

# -----------------------------
# PILE DATA
# -----------------------------

piles = [
    {"pile":1,"x":-60,"y":95},
    {"pile":2,"x":60,"y":95},
    {"pile":3,"x":-60,"y":-95},
    {"pile":4,"x":60,"y":-95}
]

n = len(piles)

Mx = P * ey
My = P * ex

sum_x2 = sum(p["x"]**2 for p in piles)
sum_y2 = sum(p["y"]**2 for p in piles)

results = []

for p in piles:

    R = (P/n) + (Mx*p["y"]/sum_y2) + (My*p["x"]/sum_x2)

    status = "SAFE"
    if R > capacity:
        status = "OVER"

    results.append({
        "Pile":p["pile"],
        "X (cm)":p["x"],
        "Y (cm)":p["y"],
        "Reaction (ton)":round(R,2),
        "Status":status
    })

df = pd.DataFrame(results)

# -----------------------------
# RESULT TABLE
# -----------------------------

st.subheader("Pile Reaction Table")

st.dataframe(df)

max_load = df["Reaction (ton)"].max()

if max_load > capacity:
    st.error(f"Maximum pile load = {max_load} ton (OVER CAPACITY)")
else:
    st.success(f"Maximum pile load = {max_load} ton (SAFE)")

# -----------------------------
# PILE CAP DIAGRAM
# -----------------------------

st.subheader("Pile Cap Diagram")

svg = """
<svg width="400" height="500" viewBox="0 0 400 500">

<!-- pile cap -->
<rect x="100" y="100" width="200" height="300"
stroke="black" stroke-width="3" fill="none"/>

<!-- piles -->
<circle cx="120" cy="120" r="8" fill="black"/>
<circle cx="280" cy="120" r="8" fill="black"/>
<circle cx="120" cy="380" r="8" fill="black"/>
<circle cx="280" cy="380" r="8" fill="black"/>

<!-- labels -->
<text x="105" y="110">P1</text>
<text x="265" y="110">P2</text>
<text x="105" y="410">P3</text>
<text x="265" y="410">P4</text>

<!-- load arrow -->
<line x1="200" y1="40" x2="200" y2="100"
stroke="red" stroke-width="3"/>
<polygon points="195,100 205,100 200,115"
fill="red"/>

<text x="190" y="30">P</text>

<!-- dimensions -->
<text x="170" y="450">120 cm</text>
<text x="40" y="260" transform="rotate(-90 40,260)">190 cm</text>

</svg>
"""

components.html(svg, height=520)
