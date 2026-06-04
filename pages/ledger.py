import streamlit as st
from datetime import datetime

from utils.db import (
    get_customers,
    get_customer_summary,
    get_customer_work_records,
    get_customer_payments
)

st.title("📒 Customer Ledger")

customers = get_customers()

if not customers:
    st.warning("Please add customers first.")
    st.stop()

customer_options = {
    customer["name"]: customer["id"]
    for customer in customers
}

selected_customer = st.selectbox(
    "Select Customer",
    list(customer_options.keys())
)

customer_id = customer_options[selected_customer]

summary = get_customer_summary(customer_id)

# =========================
# WORK STATISTICS
# =========================

st.subheader("🚜 Work Statistics")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Rotavator Hours",
        f"{summary['rot_hours']:.2f}"
    )

    st.metric(
        "Rotavator Income",
        f"₹{summary['rot_amount']:.2f}"
    )

    st.metric(
        "Nangarat Hours",
        f"{summary['nangarat_hours']:.2f}"
    )

    st.metric(
        "Nangarat Income",
        f"₹{summary['nangarat_amount']:.2f}"
    )

with col2:
    st.metric(
        "Fanadi Hours",
        f"{summary['fanadi_hours']:.2f}"
    )

    st.metric(
        "Fanadi Income",
        f"₹{summary['fanadi_amount']:.2f}"
    )

    st.metric(
        "Trolley Trips",
        summary["trolley_trips"]
    )

    st.metric(
        "Trolley Income",
        f"₹{summary['trolley_amount']:.2f}"
    )

st.metric(
    "Water Tanker Trips",
    summary["tanker_trips"]
)

st.metric(
    "Water Tanker Income",
    f"₹{summary['tanker_amount']:.2f}"
)

# =========================
# FINANCIAL SUMMARY
# =========================

st.divider()

st.subheader("💰 Financial Summary")

st.metric(
    "Total Work Amount",
    f"₹{summary['total_work_amount']:.2f}"
)

st.metric(
    "Advance Received",
    f"₹{summary['total_credit']:.2f}"
)

st.metric(
    "Payments Received",
    f"₹{summary['total_payments']:.2f}"
)

st.metric(
    "Balance",
    f"₹{summary['balance']:.2f}"
)

# =========================
# WORK HISTORY
# =========================

st.divider()

st.subheader("📋 Work History")

work_records = get_customer_work_records(customer_id)

if work_records:

    work_data = []

    for row in work_records:

        formatted_date = datetime.strptime(
            row["work_date"],
            "%Y-%m-%d"
        ).strftime("%d-%m-%Y")

        if row["work_type"] in [
            "Rotavator",
            "Nangarat",
            "Fanadi"
        ]:
            quantity = f"{row['hours']}h {row['minutes']}m"
        else:
            quantity = f"{row['trips']} Trips"

        work_data.append({
            "Date": formatted_date,
            "Work Type": row["work_type"],
            "Quantity": quantity,
            "Amount": f"₹{row['amount']:.2f}",
            "Advance Received": f"₹{row['credit_given']:.2f}"
        })

    st.dataframe(
        work_data,
        use_container_width=True
    )

else:
    st.info("No work records found.")



# =========================
# PAYMENT HISTORY
# =========================

from datetime import datetime

st.divider()

st.subheader("💵 Payment History")

payments = get_customer_payments(customer_id)

if payments:

    payment_data = []

    for row in payments:

        formatted_date = datetime.strptime(
            row["payment_date"],
            "%Y-%m-%d"
        ).strftime("%d-%m-%Y")

        payment_data.append({
            "Date": formatted_date,
            "Amount": f"₹{row['amount']:.2f}",
            "Notes": row["notes"]
        })

    st.dataframe(
        payment_data,
        use_container_width=True
    )

else:
    st.info("No payments found.")