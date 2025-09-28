import streamlit as st
import pandas as pd
from datetime import datetime
import os

SYMPTOM_FILE = "symptom_reports.csv"
SENSOR_FILE = "sensor_readings.csv"

# --- Helper Functions ---
def save_symptom(name, village, symptom):
    with open(SYMPTOM_FILE, "a") as f:
        f.write(f"{name},{village},{symptom},{datetime.now().isoformat()}\n")

def latest_sensor_status():
    if not os.path.exists(SENSOR_FILE):
        return None
    df = pd.read_csv(SENSOR_FILE, names=["village", "pH", "turbidity", "tds", "timestamp"])
    if df.empty:
        return None
    last_row = df.iloc[-1]
    pH = float(last_row["pH"])
    turbidity = float(last_row["turbidity"])
    tds = float(last_row["tds"])
    issues = []
    if pH < 6.5 or pH > 8.5:
        issues.append(f"pH out of range ({pH})")
    if turbidity > 5:
        issues.append(f"High turbidity ({turbidity})")
    if tds > 1000:
        issues.append(f"High TDS ({tds})")
    return issues

st.set_page_config(page_title="Community Health App", page_icon="🌍", layout="centered")

st.markdown("""
    <style>
    .big-button button {
        width: 100%;
        padding: 30px;
        font-size: 24px;
        margin: 10px 0;
        border-radius: 14px;
        background: #eaf5ff;
        font-weight: bold;
        border: 2px solid #90cdf4;
    }
    </style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state["page"] = "home"

def go_to(page):
    st.session_state["page"] = page

if st.session_state["page"] == "home":
    st.title("Smart Community Health")
    st.markdown("## Choose an action:")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="big-button">', unsafe_allow_html=True)
        if st.button("📝 Report Symptoms"):
            go_to("report")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="big-button">', unsafe_allow_html=True)
        if st.button("🚰 Check Water Alerts"):
            go_to("water")
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="big-button">', unsafe_allow_html=True)
        if st.button("📖 Awareness & Tips"):
            go_to("awareness")
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state["page"] == "report":
    st.header("📝 Report Symptoms")
    name = st.text_input("Name (optional)")
    village = st.text_input("Village")
    symptom = st.selectbox("Symptom", ["Diarrhea", "Fever", "Vomiting", "Other"])
    if st.button("Submit"):
        if village and symptom:
            save_symptom(name, village, symptom)
            st.success("Symptom reported!")
        else:
            st.error("Please enter your village and select a symptom.")
    if st.button("⬅️ Back to Home"):
        go_to("home")

elif st.session_state["page"] == "water":
    st.header("🚰 Water Alerts")
    issues = latest_sensor_status()
    if issues is None:
        st.info("No water quality data available yet.")
    elif not issues:
        st.success("✅ Water is SAFE")
    else:
        st.error("⚠️ Water is UNSAFE: " + ", ".join(issues))
    if st.button("⬅️ Back to Home"):
        go_to("home")

elif st.session_state["page"] == "awareness":
    st.header("📖 Awareness & Tips")
    tips = [
        ("💧 Boil Water", "Boil for at least 3 minutes before drinking."),
        ("🧼 Wash Hands", "After toilet & before eating."),
        ("🥤 Use ORS", "If diarrhea occurs, give ORS solution."),
    ]
    for title, desc in tips:
        st.markdown(f"""
        <div style="background:#f9f9f9;padding:20px;margin:10px 0;border-radius:12px;box-shadow:0px 2px 4px rgba(0,0,0,0.06);">
            <h4>{title}</h4>
            <p>{desc}</p>
        </div>
        """, unsafe_allow_html=True)
    if st.button("⬅️ Back to Home"):
        go_to("home")
