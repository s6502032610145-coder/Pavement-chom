import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Pile Cap Analysis", layout="wide")

st.title("Pile Cap Reaction Analysis")

st.write("Pile Cap Size : 120 cm × 190 cm")
st.write("Pile Capacity : 40 ton / pile")

# -------------------------
# INPUT
# -------------------------

col1, col2, col3 = st.columns(3)

with col1:
    P = st.number_input("Total Load P (ton)", value=150.0)

with col2:
    ex = st.number_input("Eccentricity ex (cm)", value=0.0)

with col3:
    ey = st.number_input("Eccentricity ey (cm)", value=0.0)

capacity = 40

# -------------------------
# PILE DATA
# -------------------------

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
        "X":p["x"],
        "Y":p["y"],
        "Reaction (ton)":round(R,2),
        "Status":status
    })

df = pd.DataFrame(results)

# -------------------------
# TABLE
# -------------------------

st.subheader("Pile Reaction Table")

st.dataframe(df)

max_load = df["Reaction (ton)"].max()

if max_load > capacity:
    st.error(f"Maximum pile load = {round(max_load,2)} ton (OVER CAPACITY)")
else:
    st.success(f"Maximum pile load = {round(max_load,2)} ton (SAFE)")

# -------------------------
# PILE CAP DIAGRAM
# -------------------------

st.subheader("Pile Cap Layout")

fig = go.Figure()

# rectangle pile cap
cap_x = [-60,60,60,-60,-60]
cap_y = [-95,-95,95,95,-95]

fig.add_trace(go.Scatter(
    x=cap_x,
    y=cap_y,
    mode="lines",
    name="Pile Cap"
))

# piles
fig.add_trace(go.Scatter(
    x=df["X"],
    y=df["Y"],
    mode="markers+text",
    text=["P"+str(p) for p in df["Pile"]],
    textposition="top center",
    marker=dict(size=12),
    name="Piles"
))

# load arrow
fig.add_annotation(
    x=ex,
    y=ey,
    ax=0,
    ay=0,
    showarrow=True,
    arrowhead=3
)

fig.update_layout(
    xaxis_title="X (cm)",
    yaxis_title="Y (cm)",
    width=700,
    height=600
)

st.plotly_chart(fig)

# -------------------------
# LOAD GRAPH
# -------------------------

st.subheader("Pile Load Distribution")

fig2 = go.Figure()

fig2.add_bar(
    x=df["Pile"],
    y=df["Reaction (ton)"]
)

fig2.update_layout(
    xaxis_title="Pile",
    yaxis_title="Reaction (ton)"
)

st.plotly_chart(fig2)
