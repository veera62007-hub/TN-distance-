import streamlit as st
import pandas as pd

CSV_FILE = "tamilnadu.csv"

st.set_page_config(page_title="TN Distance Finder", page_icon="🚗")

st.markdown("""
<style>
#MainMenu, footer, header {visibility: hidden;}
.stApp {background: linear-gradient(160deg,#0f172a 0%,#1e293b 55%,#312e81 100%);}
.block-container {padding-top: 2rem; max-width: 720px;}
.hero {text-align:center; padding:28px 16px; border-radius:24px; color:white;
  background: linear-gradient(135deg,#f97316,#ec4899,#8b5cf6);
  box-shadow:0 12px 40px rgba(236,72,153,.35); margin-bottom:24px;}
.hero h1 {margin:0; font-size:2rem; color:white;}
.hero p {margin:6px 0 0; opacity:.9;}
.stSelectbox label p {color:#e2e8f0 !important; font-weight:600;}
div.stButton > button {width:100%; border:0; border-radius:14px; padding:.8rem 1rem;
  font-weight:700; font-size:1.05rem; color:white;
  background:linear-gradient(90deg,#f97316,#ec4899); transition:transform .15s;}
div.stButton > button:hover {transform:translateY(-2px); color:white;}
div[role="dialog"] {background:#1e293b; color:#f1f5f9; border-radius:24px;}
.big {font-size:3.4rem; font-weight:800; text-align:center; line-height:1.1;
  background:linear-gradient(90deg,#f97316,#ec4899);
  -webkit-background-clip:text; -webkit-text-fill-color:transparent;}
.route {text-align:center; font-size:1.1rem; margin:8px 0 14px;}
.pills {text-align:center;}
.pill {display:inline-block; padding:6px 14px; margin:4px; border-radius:999px;
  background:rgba(139,92,246,.25); font-weight:600;}
.note {text-align:center; font-size:.8rem; opacity:.6; margin-top:14px;}
</style>
<div class="hero">
  <h1>🚗 Tamil Nadu Distance Finder</h1>
  <p>Estimated road distance between district headquarters</p>
</div>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv(CSV_FILE, encoding="utf-8-sig")

df = load_data()

distances, hq = {}, {}
for _, r in df.iterrows():
    a, b, d = r["From_District"], r["To_District"], r["Estimated_Road_Distance_KM"]
    distances[(a, b)] = d
    distances[(b, a)] = d
    hq[a] = r["From_Headquarters"]
    hq[b] = r["To_Headquarters"]

districts = sorted(hq.keys())

if "from_d" not in st.session_state:
    st.session_state.from_d = "Chennai" if "Chennai" in districts else districts[0]
if "to_d" not in st.session_state:
    st.session_state.to_d = "Madurai" if "Madurai" in districts else districts[1]

def swap():
    st.session_state.from_d, st.session_state.to_d = (
        st.session_state.to_d, st.session_state.from_d)

@st.dialog("Estimated Road Distance")
def show_result(a, b, km):
    st.markdown(f'<div class="big">{km} km</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="route">📍 <b>{hq[a]}</b> → <b>{hq[b]}</b></div>',
                unsafe_allow_html=True)
    st.markdown(
        f'<div class="pills"><span class="pill">🕒 ~{km/50:.1f} hrs at 50 km/h</span>'
        f'<span class="pill">🛣️ Road estimate</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="note">Estimate (straight-line × 1.22), not an exact route.</div>',
                unsafe_allow_html=True)

st.selectbox("📍 From District", districts, key="from_d")
st.button("⇅ Swap", on_click=swap)
st.selectbox("🏁 To District", districts, key="to_d")

st.write("")
if st.button("Find Distance 🚀"):
    a, b = st.session_state.from_d, st.session_state.to_d
    if a == b:
        st.warning("Please choose two different districts.")
    else:
        km = distances.get((a, b))
        if km is None:
            st.error("Distance not found for this pair.")
        else:
            show_result(a, b, km)
