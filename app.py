import streamlit as st
import pandas as pd

CSV_FILE = "tamilnadu2.csv"

st.set_page_config(page_title="TN Distance Finder", page_icon="🚗")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;800&display=swap');
#MainMenu, footer, header {visibility: hidden;}
.stApp {font-family:'Poppins',sans-serif;
  background: radial-gradient(circle at 15% 0%, #4c1d95 0%, transparent 45%),
              radial-gradient(circle at 90% 15%, #9d174d 0%, transparent 40%),
              #0f172a;}
.block-container {padding-top: 1.5rem; max-width: 720px;}

.hero {text-align:center; padding:26px 16px; border-radius:26px; color:white;
  background: linear-gradient(120deg,#f97316,#ec4899,#8b5cf6,#f97316);
  background-size:300% 300%; animation: flow 8s ease infinite;
  box-shadow:0 14px 40px rgba(236,72,153,.35); margin-bottom:18px;}
.hero h1 {margin:0; font-size:1.7rem; font-weight:800; color:white;}
.hero p {margin:6px 0 0; opacity:.92; font-size:.9rem;}
@keyframes flow {0%{background-position:0% 50%} 50%{background-position:100% 50%} 100%{background-position:0% 50%}}

.glass {background:rgba(255,255,255,.07); border:1px solid rgba(255,255,255,.14);
  backdrop-filter: blur(14px); border-radius:22px; padding:18px; margin:10px 0;
  color:#f1f5f9; animation: pop .4s ease;}
@keyframes pop {from{opacity:0; transform:translateY(10px) scale(.97)} to{opacity:1; transform:none}}

.rt {display:flex; align-items:center; gap:8px;}
.stop {width:30%; text-align:center; font-weight:600; font-size:.85rem; line-height:1.2;}
.dot {width:14px; height:14px; border-radius:50%; margin:0 auto 6px;}
.dot.a {background:#22c55e; box-shadow:0 0 12px #22c55e;}
.dot.b {background:#ef4444; box-shadow:0 0 12px #ef4444;}
.track {position:relative; flex:1; height:30px;}
.line {position:absolute; top:14px; left:0; right:0; border-top:3px dashed rgba(255,255,255,.4);}
.car {position:absolute; top:0; font-size:1.3rem; animation: drive 3.2s linear infinite;}
@keyframes drive {from{left:0} to{left:calc(100% - 26px)}}
.kmrow {text-align:center; margin-top:10px; font-size:1rem; opacity:.9;}
.kmbig {font-size:2.6rem; font-weight:800;
  background:linear-gradient(90deg,#f97316,#ec4899);
  -webkit-background-clip:text; -webkit-text-fill-color:transparent;}

.stSelectbox label p, .stNumberInput label p {color:#e2e8f0 !important; font-weight:600;}
div[data-baseweb="select"] > div {background:rgba(255,255,255,.08) !important;
  border:1px solid rgba(255,255,255,.18) !important; border-radius:14px !important; color:white !important;}

div.stButton > button {width:100%; border-radius:14px; padding:.55rem .8rem; font-weight:600;
  color:#f1f5f9; background:rgba(255,255,255,.08); border:1px solid rgba(255,255,255,.18);
  transition:all .15s;}
div.stButton > button:hover {transform:translateY(-2px); border-color:#ec4899; color:white;}
[class*="st-key-go"] button {border:0 !important; font-size:1.05rem; padding:.8rem 1rem;
  background:linear-gradient(90deg,#f97316,#ec4899) !important;
  box-shadow:0 8px 24px rgba(236,72,153,.4);}
[class*="st-key-swap"] button {border-radius:999px; font-size:.9rem;}

button[data-baseweb="tab"] {color:#cbd5e1; font-weight:600;}
button[data-baseweb="tab"][aria-selected="true"] {color:white;}
div[role="dialog"] {background:#1e293b; color:#f1f5f9; border-radius:24px;}

.big {font-size:3.6rem; font-weight:800; text-align:center; line-height:1.1;
  background:linear-gradient(90deg,#f97316,#ec4899);
  -webkit-background-clip:text; -webkit-text-fill-color:transparent;}
.route {text-align:center; font-size:1.05rem; margin:8px 0 14px;}
.note {text-align:center; font-size:.75rem; opacity:.6; margin-top:12px;}
</style>
<div class="hero">
  <h1>🚗 Tamil Nadu Distance Finder</h1>
  <p>Road distance and trip cost between districts</p>
</div>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    return pd.read_csv(CSV_FILE, encoding="utf-8-sig")


df = load_data()

distances, city = {}, {}
for _, r in df.iterrows():
    a, b = r["From_District"], r["To_District"]
    d = int(r["Estimated_Road_Distance_KM"])
    distances[(a, b)] = d
    distances[(b, a)] = d
    city[a] = r["From_City"]
    city[b] = r["To_City"]

districts = sorted(city.keys())


def label(d):
    return d if city[d] == d else f"{d} ({city[d]})"


# ---------- state ----------
if "from_d" not in st.session_state:
    st.session_state.from_d = "Chennai" if "Chennai" in districts else districts[0]
if "to_d" not in st.session_state:
    st.session_state.to_d = "Madurai" if "Madurai" in districts else districts[1]


def swap():
    st.session_state.from_d, st.session_state.to_d = (
        st.session_state.to_d, st.session_state.from_d)


@st.dialog("Trip Details")
def show_result(a, b, km):
    st.markdown(f'<div class="big">{km} km</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="route">📍 <b>{city[a]}</b> → <b>{city[b]}</b></div>',
                unsafe_allow_html=True)
    st.markdown(f'<div class="route">🔁 Round trip: <b>{km*2} km</b></div>',
                unsafe_allow_html=True)
    st.caption("Copy & share:")
    st.code(f"{city[a]} → {city[b]}: ~{km} km by road", language=None)
    st.markdown('<div class="note">Estimate (straight-line × 1.22), not an exact route.</div>',
                unsafe_allow_html=True)


tab1, tab2 = st.tabs(["📍 Distance", "⛽ Trip Cost"])

# ================= TAB 1 =================
with tab1:
    st.selectbox("📍 From", districts, key="from_d", format_func=label)
    st.button("⇅  Swap", key="swap1", on_click=swap)
    st.selectbox("🏁 To", districts, key="to_d", format_func=label)

    a, b = st.session_state.from_d, st.session_state.to_d
    if a == b:
        st.warning("Please choose two different places.")
    else:
        km = distances.get((a, b))
        if km is None:
            st.error("Distance not found for this pair.")
        else:
            st.markdown(
                f'<div class="glass"><div class="rt">'
                f'<div class="stop"><div class="dot a"></div>{city[a]}</div>'
                f'<div class="track"><div class="line"></div><div class="car">🚗</div></div>'
                f'<div class="stop"><div class="dot b"></div>{city[b]}</div>'
                f'</div><div class="kmrow"><span class="kmbig">{km}</span> km</div></div>',
                unsafe_allow_html=True)

            if st.button("View Trip Details 🚀", key="go1"):
                show_result(a, b, km)

# ================= TAB 2 =================
with tab2:
    a, b = st.session_state.from_d, st.session_state.to_d
    km = distances.get((a, b)) if a != b else None
    if km is None:
        st.info("Pick two different districts in the Distance tab first.")
    else:
        st.markdown(f'<div class="glass"><b>{city[a]} → {city[b]}</b> · {km} km</div>',
                    unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        mileage = c1.number_input("Mileage (km/l)", 5.0, 60.0, 15.0, 0.5)
        price = c2.number_input("Fuel price (₹/l)", 50.0, 200.0, 105.0, 0.5)
        round_trip = st.toggle("Round trip", value=False)
        total_km = km * (2 if round_trip else 1)
        litres = total_km / mileage
        cost = litres * price
        st.markdown(
            f'<div class="glass"><div class="kmrow">Estimated fuel cost</div>'
            f'<div class="big">₹{cost:,.0f}</div>'
            f'<div class="kmrow">{total_km} km · {litres:.1f} litres</div></div>',
            unsafe_allow_html=True)
        st.caption("Fuel price default is approximate, please edit it to today's price.")
