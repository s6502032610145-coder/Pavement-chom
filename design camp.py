import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.title("Pile Cap Reaction Calculator")

st.write("Pile Capacity = 40 ton / pile")
st.write("Total Load = 150 ton")

P = st.number_input("Load P (ton)", value=150.0)
ex = st.number_input("ex (cm)", value=0.0)
ey = st.number_input("ey (cm)", value=0.0)

capacity = 40

piles = [
{"pile":1,"x":-60,"y":95},
{"pile":2,"x":60,"y":95},
{"pile":3,"x":-60,"y":-95},
{"pile":4,"x":60,"y":-95}
]

n=len(piles)

Mx=P*ey
My=P*ex

sumx2=sum(p["x"]**2 for p in piles)
sumy2=sum(p["y"]**2 for p in piles)

results=[]

for p in piles:

    R=(P/n)+(Mx*p["y"]/sumy2)+(My*p["x"]/sumx2)

    status="SAFE"
    if R>capacity:
        status="OVER"

    results.append({
    "Pile":p["pile"],
    "Reaction (ton)":round(R,2),
    "Status":status
    })

df=pd.DataFrame(results)

st.subheader("Pile Reaction")

st.dataframe(df)

# ---------------- DIAGRAM ----------------

st.subheader("Pile Cap Diagram")

svg="""
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
<text x="180" y="190">2 cm</text>
<text x="400" y="190">3 cm</text>
<text x="180" y="410">1 cm</text>
<text x="400" y="410">6 cm</text>

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
