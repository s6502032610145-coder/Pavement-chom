import streamlit as st
import pandas as pd

st.title("Pile Cap Reaction Calculator")

st.write("Pile Cap Size : 120 cm x 190 cm")
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
        "X":p["x"],
        "Y":p["y"],
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

# simple pile layout
st.subheader("Pile Layout")

layout = """
      P1           P2

      ●------------●

      |            |

      |   PILE     |

      |    CAP     |

      |            |

      ●------------●

      P3           P4
"""

st.text(layout)
