# Pile Reaction Calculator (Eccentric Load)

# รับค่าแรงรวม
P = float(input("กรอกแรงรวม P (ตัน): "))

# ระยะเยื้องศูนย์
ex = float(input("Eccentricity X (cm): "))
ey = float(input("Eccentricity Y (cm): "))

# ตำแหน่งเสาเข็ม (cm)
piles = [
    {"pile": 1, "x": -60, "y": 95},
    {"pile": 2, "x": 60, "y": 95},
    {"pile": 3, "x": -60, "y": -95},
    {"pile": 4, "x": 60, "y": -95}
]

n = len(piles)

# โมเมนต์
Mx = P * ey
My = P * ex

# คำนวณ Σx² และ Σy²
sum_x2 = sum(p["x"]**2 for p in piles)
sum_y2 = sum(p["y"]**2 for p in piles)

print("\nผลการคำนวณแรงปฏิกิริยาเสาเข็ม")
print("----------------------------------")

for p in piles:

    R = (P/n) + (Mx*p["y"]/sum_y2) + (My*p["x"]/sum_x2)

    print(f"Pile {p['pile']} = {R:.2f} ton")

    if R > 40:
        print("  ⚠ เกินกำลังรับ 40 ตัน/ต้น")
