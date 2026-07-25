"""
Streamlit UI — upload a medicine label photo, enter patient info,
get interaction advice from the Flask backend.
"""
import requests
import streamlit as st

BACKEND_URL = "http://127.0.0.1:5000"

st.set_page_config(page_title="MedSafer AI", page_icon="💊")
st.title("💊 MedSafer AI")
st.caption("Upload a medicine label photo to check for interaction warnings.")

with st.form("scan_form"):
    image_file = st.file_uploader("Medicine label photo", type=["jpg", "jpeg", "png"])
    age = st.number_input("Patient age", min_value=0, max_value=120, value=30)
    conditions = st.text_input("Known conditions (comma-separated)", value="")
    submitted = st.form_submit_button("Analyze")

if submitted:
    if image_file is None:
        st.error("Please upload an image first.")
    else:
        with st.spinner("Extracting text and checking interactions..."):
            files = {"image": (image_file.name, image_file.getvalue())}
            data = {"age": age, "conditions": conditions}
            try:
                response = requests.post(
                    f"{BACKEND_URL}/api/scan", files=files, data=data, timeout=30
                )
                response.raise_for_status()
                result = response.json()

                st.subheader("Extracted Label Text")
                st.text(result["label_text"])

                st.subheader("Interaction Advice")
                st.write(result["advice"])
            except requests.RequestException as exc:
                st.error(f"Request failed: {exc}")

st.divider()
st.subheader("Recent Scans")
try:
    history = requests.get(f"{BACKEND_URL}/api/history", timeout=10).json()
    for scan in history:
        with st.expander(f"{scan['created_at']} — age {scan['age']}"):
            st.text(scan["label_text"])
            st.write(scan["advice"])
except requests.RequestException:
    st.caption("Could not load history — is the backend running?")