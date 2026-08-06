import sqlite3

import requests
import streamlit as st

API_URL = "http://localhost:8000"
RATE_LIMIT = 10

st.set_page_config(page_title="Rate Limiter Demo", layout="centered")
st.title("Rate Limiter Demo")
st.caption("Tests the `/rate-limited` endpoint from main.py (10 requests/min per user).")

st.sidebar.header("Settings")
user_id = st.sidebar.text_input("User ID", value="alice")
host = st.sidebar.text_input("API URL", value=API_URL).rstrip("/")


def fetch_status() -> int:
    try:
        return requests.get(f"{host}/rate-limited", params={"user_id": user_id}, timeout=10).status_code
    except requests.RequestException as e:
        st.error(f"Could not reach the API: {e}")
        st.stop()


col_a, col_b, col_c = st.columns(3)
with col_a:
    single = st.button("Send 1 Request")
with col_b:
    burst = st.button("Burst 12 Requests")
with col_c:
    reset = st.button("Reset (wait 60s)")

if single:
    status = fetch_status()
    if status == 200:
        st.success(f"Request accepted ({status})")
    else:
        st.warning(f"Denied ({status})")

if burst:
    codes = []
    for i in range(12):
        status = fetch_status()
        codes.append(status)
    st.write(f"Results: {codes}")
    st.info(
        f"{codes.count(200)} allowed, {codes.count(429)} denied "
        f"(expected: first {RATE_LIMIT} = 200, rest = 429)."
    )

if reset:
    st.warning("Limit resets automatically 60s after the first request in the window.")

st.divider()
st.subheader("Prediction (GET /predict)")

x = st.number_input("Input value x", value=1.0, step=0.1)
if st.button("Predict"):
    try:
        resp = requests.get(f"{host}/predict", params={"x": x}, timeout=10)
        if resp.status_code == 200:
            st.success(f"Result: {resp.json()['result']}")
        else:
            st.error(f"Prediction failed ({resp.status_code}): {resp.text}")
    except requests.RequestException as e:
        st.error(f"Could not reach the API: {e}")

st.divider()
st.subheader("Request Log (SQLite)")
if st.button("Refresh Log"):
    try:
        conn = sqlite3.connect("requests.db")
        rows = conn.execute("SELECT * FROM request_logs ORDER BY id DESC LIMIT 20").fetchall()
        conn.close()
        if rows:
            st.dataframe(rows, columns=["id", "user_id", "endpoint", "status", "created_at (unix)"])
        else:
            st.write("No logs yet.")
    except sqlite3.Error as e:
        st.error(f"Failed to read DB: {e}")
