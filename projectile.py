import numpy as np
import matplotlib.pyplot as plt

b_list = {
    "sphere": 0.47,
    "semisphere": 0.42,
    "cone": 0.50,
    "cube": 1.06,
    "rotated_cube": 0.80,
    "cylinder": 0.62,
    "short_cylinder": 1.15,
    "drop": 0.04,
    "half_drop": 0.09
}

g = 9.81
v_0 = int(input("Initial Velocity: "))
theta = np.deg2rad(int(input("Angle: ")))
b = b_list[input("Shape: ")]

U = v_0 * np.cos(theta)
V = v_0 * np.sin(theta)

T_0 = (2 * V) / g
T = ((2 * V) / g) * (1 - b * V / (3 * g))

def X(t, b):
    if b == 0:
        return U * t
    return (U / b) * (1 - np.exp(-b * t))

def Y(t, b):
    if b == 0:
        return V * t - 0.5 * g * t**2
    return (b * V + g) / (b**2) * (1 - np.exp(-b * t)) - (g / b) * t

timeline_T0 = np.linspace(0, T_0, 10000)
timeline_T = np.linspace(0, T, 10000)

plt.plot(X(timeline_T0, 0), Y(timeline_T0, 0), label="b=0")
plt.plot(X(timeline_T, b), Y(timeline_T, b), label=f"b={b}", alpha=0.3)
plt.legend()
plt.show()
