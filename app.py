import streamlit as st
from utils.db import init_db

# Create tables automatically
init_db()

st.set_page_config(
    page_title="Farmo",
    page_icon="🚜",
    layout="wide"
)

st.title("🚜 Farmo")
st.subheader("Farm Management & Tractor Ledger System")

st.success("Database initialized successfully!")