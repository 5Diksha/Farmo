import streamlit as st
from utils.db import get_dashboard_stats

st.title("📊 Dashboard")

stats = get_dashboard_stats()

# =========================
# FINANCIAL SUMMARY
# =========================

st.subheader("💰 Financial Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Work Amount",
        f"₹{stats['total_work_amount']:.2f}"
    )

with col2:
    st.metric(
        "Advance Received",
        f"₹{stats['total_advance']:.2f}"
    )

with col3:
    st.metric(
        "Payments Received",
        f"₹{stats['total_payments_received']:.2f}"
    )

with col4:
    st.metric(
        "Pending Balance",
        f"₹{stats['pending_balance']:.2f}"
    )

# =========================
# WORK STATISTICS
# =========================

st.divider()

st.subheader("🚜 Work Statistics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Rotavator Hours",
        f"{stats['rot_hours']:.2f}"
    )

with col2:
    st.metric(
        "Nangarat Hours",
        f"{stats['nangarat_hours']:.2f}"
    )

with col3:
    st.metric(
        "Fanadi Hours",
        f"{stats['fanadi_hours']:.2f}"
    )

col4, col5 = st.columns(2)

with col4:
    st.metric(
        "Trolley Trips",
        stats["trolley_trips"]
    )

with col5:
    st.metric(
        "Water Tanker Trips",
        stats["tanker_trips"]
    )

# =========================
# BUSINESS STATISTICS
# =========================

st.divider()

st.subheader("📈 Business Statistics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Customers",
        stats["total_customers"]
    )

with col2:
    st.metric(
        "Work Entries",
        stats["total_work_entries"]
    )

with col3:
    st.metric(
        "Payments",
        stats["total_payments"]
    )



    