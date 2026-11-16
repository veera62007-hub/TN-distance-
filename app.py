import streamlit as st
import pandas as pd

CSV_FILE = "tamilnadu.csv"

st.set_page_config(page_title="Tamil Nadu Distance Finder", page_icon="🚗")
st.title("🚗 Tamil Nadu District Distance Finder")
st.caption("Estimated road distance between district headquarters")

@st.cache_data
def load_data():
    return pd.read_csv(CSV_FILE, encoding="utf-8-sig")

df = load_data()

distances = {}
hq = {}
for _, row in df.iterrows():
    a = row["From_District"]
    b = row["To_District"]
    d = row["Estimated_Road_Distance_KM"]
    distances[(a, b)] = d
    distances[(b, a)] = d
    hq[a] = row["From_Headquarters"]
    hq[b] = row["To_Headquarters"]

districts = sorted(hq.keys())

@st.dialog("Estimated Road Distance")
def show_result(from_d, to_d, km):
    st.success(f"Estimated road distance: {km} km")
    st.write(f"From **{hq[from_d]}** to **{hq[to_d]}**")
    st.write(f"Approx. driving time at 50 km/h: {km/50:.1f} hours")
    st.caption("This is an estimate (straight-line distance x 1.22), not an exact route distance.")

col1, col2 = st.columns(2)
with col1:
    from_d = st.selectbox("From District", districts,
                          index=districts.index("Chennai") if "Chennai" in districts else 0)
with col2:
    to_d = st.selectbox("To District", districts,
                        index=districts.index("Madurai") if "Madurai" in districts else 1)

if st.button("Find Distance"):
    if from_d == to_d:
        st.warning("Please choose two different districts.")
    else:
        km = distances.get((from_d, to_d))
        if km is None:
            st.error("Distance not found for this pair.")
        else:
            show_result(from_d, to_d, km)
