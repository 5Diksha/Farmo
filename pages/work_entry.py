import streamlit as st
from datetime import date

from utils.db import (
    get_customers,
    get_rate,
    add_work_record
)

st.title("🚜 Work Entry")

customers = get_customers()

if not customers:
    st.warning("Please add customers first.")
    st.stop()

customer_options = {
    customer["name"]: customer["id"]
    for customer in customers
}

selected_customer = st.selectbox(
    "Customer",
    list(customer_options.keys())
)

work_date = st.date_input(
    "Work Date",
    value=date.today()
)

work_type = st.selectbox(
    "Work Type",
    [
        "Rotavator",
        "Nangarat",
        "Fanadi",
        "Trolley Trip",
        "Water Tanker Trip"
    ]
)

rate = get_rate(work_type)

st.info(f"Rate: ₹{rate}")

hours = 0
minutes = 0
trips = 0

if work_type in ["Rotavator", "Nangarat", "Fanadi"]:

    hours = st.number_input(
        "Hours",
        min_value=0,
        value=0
    )

    minutes = st.number_input(
        "Minutes",
        min_value=0,
        max_value=59,
        value=0
    )

    total_hours = hours + (minutes / 60)

    amount = total_hours * rate

else:

    trips = st.number_input(
        "Trips",
        min_value=0,
        value=0
    )

    amount = trips * rate

credit_given = st.number_input(
    "Advance Received",
    min_value=0.0,
    value=0.0
)

notes = st.text_area("Notes")

st.subheader(f"Amount: ₹{amount:.2f}")

if st.button("Save Work Record"):

    add_work_record(
        customer_options[selected_customer],
        str(work_date),
        work_type,
        hours,
        minutes,
        trips,
        rate,
        amount,
        credit_given,
        notes
    )

    st.success("Work record saved successfully!")