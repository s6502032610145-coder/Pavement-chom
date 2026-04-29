import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Pile Cap Analysis")

st.title("Pile Cap Reaction Calculator")

st.write("Pile Cap Size : 120 cm × 190 cm")
st.write("Pile Capacity : 40 ton / pile")

# INPUT
P = st.number_input("Total Load P (ton)", value=150.0)
ex = st.number_input("Eccentricity ex (cm)", value=0.0)
ey = st.number_input("Eccentricity ey (cm)", value=0.0)

capacity = 40

# pile coordinates
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

st.subheader("Pile Reaction Table")
st.dataframe(df)

max_load = df["Reaction (ton)"].max()

if max_load > capacity:
    st.error(f"Maximum pile load = {max_load} ton (OVER CAPACITY)")
else:
    st.success(f"Maximum pile load = {max_load} ton (SAFE)")

# -----------------------
# PILE CAP DIAGRAM
# -----------------------

st.subheader("Pile Layout")

fig = go.Figure()

# pile cap rectangle
fig.add_shape(
    type="rect",
    x0=-60, y0=-95,
    x1=60, y1=95,
    line=dict(color="black")
)

# piles
fig.add_trace(go.Scatter(
    x=df["X (cm)"],
    y=df["Y (cm)"],
    mode="markers+text",
    text=df["Pile"],
    textposition="top center",
    marker=dict(size=14)
))

fig.update_layout(
    xaxis_title="X (cm)",
    yaxis_title="Y (cm)",
    width=600,
    height=500
)

st.plotly_chart(fig)

# -----------------------
# LOAD GRAPH
# -----------------------

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
