import streamlit as st
from datetime import date

from utils.db import (
    get_customers,
    add_payment
)

st.title("💰 Payments")

customers = get_customers()

if not customers:
    st.warning("Please add customers first.")
    st.stop()

customer_options = {
    customer["name"]: customer["id"]
    for customer in customers
}

payment_date = st.date_input(
    "Payment Date",
    value=date.today()
)

selected_customer = st.selectbox(
    "Customer",
    list(customer_options.keys())
)

amount = st.number_input(
    "Amount Received",
    min_value=0.0,
    value=0.0
)

notes = st.text_area("Notes")

if st.button("Save Payment"):

    if amount <= 0:
        st.error("Amount must be greater than zero")
    else:

        add_payment(
            customer_options[selected_customer],
            str(payment_date),
            amount,
            notes
        )

        st.success("Payment saved successfully!")