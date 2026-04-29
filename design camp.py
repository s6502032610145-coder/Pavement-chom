import streamlit as st
import pandas as pd

st.title("Pile Reaction Analysis")

st.write("Pile Cap Size : 120 cm × 190 cm")
st.write("Number of Piles : 4")

# Load
P = st.number_input("Total Load P (ton)", value=150.0)

capacity = 40

# pile coordinates (cm)
piles = [
    {"pile":1, "x":-60, "y":95},
    {"pile":2, "x":60, "y":95},
    {"pile":3, "x":-60, "y":-95},
    {"pile":4, "x":60, "y":-95}
]

st.subheader("Eccentricity")

ex = st.number_input("ex (cm)", value=0.0)
ey = st.number_input("ey (cm)", value=0.0)

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
        "Pile": p["pile"],
        "X (cm)": p["x"],
        "Y (cm)": p["y"],
        "Reaction (ton)": round(R,2),
        "Status": status
    })

df = pd.DataFrame(results)

st.subheader("Pile Reaction Result")

st.dataframe(df)

max_load = df["Reaction (ton)"].max()

st.write("Maximum Load on Pile =", round(max_load,2), "ton")

if max_load > capacity:
    st.error("Pile Capacity Exceeded")
else:
    st.success("Design is Safe")
