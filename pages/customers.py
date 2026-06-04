import streamlit as st
from utils.db import add_customer, get_customers, delete_customer

st.set_page_config(page_title="Customers", page_icon="👤")

st.title("👤 Customer Management")

# =========================
# ADD CUSTOMER
# =========================

st.subheader("Add New Customer")

with st.form("add_customer_form"):
    name = st.text_input("Customer Name")
    mobile = st.text_input("Mobile Number")

    submit = st.form_submit_button("Add Customer")

    if submit:
        if not name.strip():
            st.error("Customer name is required")
        else:
            add_customer(name.strip(), mobile.strip())
            st.success("Customer added successfully!")
            st.rerun()

# =========================
# CUSTOMER LIST
# =========================

st.divider()

st.subheader("Customer List")

customers = get_customers()

if customers:

    for customer in customers:

        col1, col2, col3 = st.columns([4, 3, 1])

        with col1:
            st.write(f"**{customer['name']}**")

        with col2:
            st.write(customer["mobile"])

        with col3:
            if st.button(
                "🗑️",
                key=f"delete_{customer['id']}"
            ):
                delete_customer(customer["id"])
                st.rerun()

else:
    st.info("No customers found.")