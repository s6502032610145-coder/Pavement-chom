import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Pile Cap Reaction Calculator")

st.write("Pile Cap Size : 120 cm x 190 cm")
st.write("Number of piles : 4")

# Load input
P = st.number_input("Total Load P (ton)", value=150.0)

# Eccentricity
st.subheader("Eccentricity")
ex = st.number_input("ex (cm)", value=0.0)
ey = st.number_input("ey (cm)", value=0.0)

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
        "X":p["x"],
        "Y":p["y"],
        "Reaction (ton)":round(R,2),
        "Status":status
    })

df = pd.DataFrame(results)

st.subheader("Pile Reaction Table")
st.dataframe(df)

max_load = df["Reaction (ton)"].max()

st.write("Maximum pile load =",round(max_load,2),"ton")

if max_load > capacity:
    st.error("Pile capacity exceeded")
else:
    st.success("Design is SAFE")

# ----------------------
# Pile layout diagram
# ----------------------

st.subheader("Pile Layout")

fig, ax = plt.subplots()

x = df["X"]
y = df["Y"]

ax.scatter(x,y)

for i in range(len(df)):
    ax.text(x[i],y[i],f"P{df['Pile'][i]}")

ax.set_xlim(-80,80)
ax.set_ylim(-120,120)

ax.set_xlabel("X (cm)")
ax.set_ylabel("Y (cm)")
ax.set_title("Pile Cap Layout")

st.pyplot(fig)

# ----------------------
# Load graph
# ----------------------

st.subheader("Pile Load Distribution")

fig2, ax2 = plt.subplots()

ax2.bar(df["Pile"],df["Reaction (ton)"])

ax2.set_xlabel("Pile")
ax2.set_ylabel("Reaction (ton)")
ax2.set_title("Pile Load")

st.pyplot(fig2)
