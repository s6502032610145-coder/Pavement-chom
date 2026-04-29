import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.title("Pile Cap Reaction Calculator")

# ---------------- INPUT ----------------

capacity = st.number_input("Pile Capacity (ton/pile)", value=40.0)
P = st.number_input("Total Load P (ton)", value=150.0)

ex = st.number_input("ex (cm)", value=0.0)
ey = st.number_input("ey (cm)", value=0.0)

st.subheader("Pile Offset (cm)")

col1,col2,col3,col4 = st.columns(4)

with col1:
    off1 = st.number_input("Pile1 offset", value=2.0)

with col2:
    off2 = st.number_input("Pile2 offset", value=3.0)

with col3:
    off3 = st.number_input("Pile3 offset", value=1.0)

with col4:
    off4 = st.number_input("Pile4 offset", value=6.0)

# ---------------- PILE DATA ----------------

piles = [
{"pile":1,"x":-60,"y":95,"off":off1},
{"pile":2,"x":60,"y":95,"off":off2},
{"pile":3,"x":-60,"y":-95,"off":off3},
{"pile":4,"x":60,"y":-95,"off":off4}
]

n=len(piles)

Mx=P*ey
My=P*ex

sumx2=sum(p["x"]**2 for p in piles)
sumy2=sum(p["y"]**2 for p in piles)

results=[]

# ---------------- CALCULATION ----------------

for p in piles:

    R=(P/n)+(Mx*p["y"]/sumy2)+(My*p["x"]/sumx2)

    status="SAFE"
    if R>capacity:
        status="OVER"

    results.append({
    "Pile":p["pile"],
    "Reaction (ton)":round(R,2),
    "Offset (cm)":p["off"],
    "Status":status
    })

df=pd.DataFrame(results)

st.subheader("Pile Reaction")

st.dataframe(df)

maxR=df["Reaction (ton)"].max()

if maxR>capacity:
    st.error(f"Maximum reaction = {maxR} ton (OVER)")
else:
    st.success(f"Maximum reaction = {maxR} ton (SAFE)")

# ---------------- DIAGRAM ----------------

st.subheader("Pile Cap Diagram")

svg=f"""
<svg width="600" height="600">

<!-- pile cap -->
<rect x="150" y="150" width="300" height="300"
stroke="black" stroke-width="3" fill="none"/>

<!-- center lines -->
<line x1="300" y1="150" x2="300" y2="450"
stroke="red" stroke-dasharray="5,5"/>

<line x1="150" y1="300" x2="450" y2="300"
stroke="red" stroke-dasharray="5,5"/>

<!-- piles -->
<circle cx="210" cy="210" r="12" fill="pink" stroke="black"/>
<circle cx="390" cy="210" r="12" fill="pink" stroke="black"/>
<circle cx="210" cy="390" r="12" fill="pink" stroke="black"/>
<circle cx="390" cy="390" r="12" fill="pink" stroke="black"/>

<!-- pile offsets -->
<text x="180" y="190">{off1} cm</text>
<text x="400" y="190">{off2} cm</text>
<text x="180" y="410">{off3} cm</text>
<text x="400" y="410">{off4} cm</text>

<!-- dimension top -->
<line x1="150" y1="120" x2="450" y2="120"
stroke="black"/>

<text x="200" y="100">35 cm</text>
<text x="285" y="100">120 cm</text>
<text x="380" y="100">35 cm</text>

<!-- vertical dimension -->
<line x1="120" y1="150" x2="120" y2="450"
stroke="black"/>

<text x="80" y="310">190 cm</text>

</svg>
"""

components.html(svg,height=620)
