import streamlit as st
import pandas as pd

st.title("Pile Cap Reaction Calculator")

st.write("Pile Cap Size : 120 cm x 190 cm")
st.write("Number of piles : 4")

# Load
P = st.number_input("Total Load P (ton)", value=150.0)

# eccentricity
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
        "X (cm)":p["x"],
        "Y (cm)":p["y"],
        "Reaction (ton)":round(R,2),
        "Status":status
    })

df = pd.DataFrame(results)

st.subheader("Pile Reaction Result")
st.dataframe(df)

max_load = df["Reaction (ton)"].max()

st.write("Maximum pile load =",round(max_load,2),"ton")

if max_load > capacity:
    st.error("Pile capacity exceeded")
else:
    st.success("Design is SAFE")
