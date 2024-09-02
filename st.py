import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

b_list = {
    "sphere": 0.47,
    "hemisphere": 0.42,
    "cone": 0.50,
    "cube": 1.06,
    "rotated_cube": 0.80,
    "cylinder": 0.62,
    "short_cylinder": 1.15,
    "drop": 0.04,
    "half_drop": 0.09
}

g = 9.80665

if 'objects' not in st.session_state:
    st.session_state.objects = [{"shape": "sphere", "v_0": 10, "theta": 45}]


with st.sidebar:
    st.title("Object Manager")

    shape = st.selectbox("Shape", list(b_list.keys()), index=0)
    v_0 = st.number_input("Initial Velocity", min_value=0, value=10, step=1)
    theta = st.number_input("Angle", min_value=0, max_value=90, value=45, step=1)

    object_count = len(st.session_state.objects)
    add_object = st.button("Add Object")

    if add_object:
        st.session_state.objects.append({"shape": shape, "v_0": v_0, "theta": theta})
        st.rerun()

    
    st.write("Objects:")
    for idx, obj in enumerate(st.session_state.objects):
        st.text(f"{idx+1} {obj['shape']}")
        st.latex(fr"\qquad v_0 = {obj['v_0']} \, \text{{m/s}}\;/\;\theta = {obj['theta']}^\circ")

    object_count = len(st.session_state.objects)
    if object_count > 0:
        delete_index = st.number_input("Delete Object Index", min_value=1, max_value=object_count, step=1, value=1) - 1
        if st.button("Delete Object"):
            if 0 <= delete_index < len(st.session_state.objects):
                st.session_state.objects.pop(delete_index)
                st.experimental_rerun()
    else:
        st.write("No objects to delete.")
    

st.title("Projectile Motion Graph")

fig, ax = plt.subplots(figsize=(20, 13))
for obj in st.session_state.objects:
    b = b_list[obj["shape"]]
    v_0 = obj["v_0"]
    theta = np.deg2rad(obj["theta"])

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

    ax.plot(X(timeline_T0, 0), Y(timeline_T0, 0), label=f"{obj['shape']} b=0", alpha=0.3)
    ax.plot(X(timeline_T, b), Y(timeline_T, b), label=f"{obj['shape']} b={b}")

ax.set_xlim(left=0)
ax.set_ylim(bottom=0)

ax.legend()
ax.set_xlabel("Distance")
ax.set_ylabel("Height")

st.pyplot(fig)