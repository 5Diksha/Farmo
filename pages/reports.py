import streamlit as st

from utils.pdf_generator import (
    create_invoice_pdf
)

from utils.db import (
    get_customer_monthly_summary,
    get_monthly_work_records,
    get_monthly_payments,
    get_monthly_summary,
    get_customers,
    get_customer_monthly_work_records,
    get_customer_monthly_payments,
    get_customer_monthly_summary

)

from utils.excel_export import (
    create_monthly_excel_report,
    create_customer_monthly_report
)

st.title("📈 Reports")

months = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
}

selected_month = st.selectbox(
    "Month",
    list(months.keys())
)

selected_year = st.number_input(
    "Year",
    min_value=2024,
    max_value=2100,
    value=2026
)

if st.button("Generate Monthly Excel Report"):

    month_number = months[selected_month]

    work_records = get_monthly_work_records(
        month_number,
        selected_year
    )

    payments = get_monthly_payments(
        month_number,
        selected_year
    )

    summary = get_monthly_summary(
        month_number,
        selected_year
    )

    file_path = create_monthly_excel_report(
        selected_month,
        selected_year,
        work_records,
        payments,
        summary
    )

    st.success("Excel Report Generated Successfully!")

    with open(file_path, "rb") as file:

        st.download_button(
            label="⬇ Download Excel Report",
            data=file,
            file_name=file_path.name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )




st.divider()

st.subheader("👤 Customer Monthly Report")

customers = get_customers()

customer_options = {
    customer["name"]: customer["id"]
    for customer in customers
}

selected_customer = st.selectbox(
    "Customer",
    list(customer_options.keys())
)

customer_month = st.selectbox(
    "Customer Report Month",
    list(months.keys()),
    key="cust_month"
)

customer_year = st.number_input(
    "Customer Report Year",
    min_value=2024,
    max_value=2100,
    value=2026,
    key="cust_year"
)

if st.button("Generate Customer Report"):
    
    customer_id = customer_options[
        selected_customer
    ]

    month_number = months[
        customer_month
    ]

    work_records = (
        get_customer_monthly_work_records(
            customer_id,
            month_number,
            customer_year
        )
    )

    payments = (
        get_customer_monthly_payments(
            customer_id,
            month_number,
            customer_year
        )
    )

    summary = (
        get_customer_monthly_summary(
            customer_id,
            month_number,
            customer_year
        )
    )

    file_path = (
        create_customer_monthly_report(
            selected_customer,
            customer_month,
            customer_year,
            work_records,
            payments,
            summary
        )
    )

    st.success(
        "Customer Report Generated!"
    )

    with open(file_path, "rb") as file:

        st.download_button(
            label="⬇ Download Customer Report",
            data=file,
            file_name=file_path.name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )



st.divider()

st.subheader("📄 PDF Invoice")

invoice_customer = st.selectbox(
    "Customer",
    list(customer_options.keys()),
    key="invoice_customer"
)

invoice_month = st.selectbox(
    "Invoice Month",
    list(months.keys()),
    key="invoice_month"
)

invoice_year = st.number_input(
    "Invoice Year",
    min_value=2024,
    max_value=2100,
    value=2026,
    key="invoice_year"
)

if st.button("Generate PDF Invoice"):
    
    customer_id = customer_options[
        invoice_customer
    ]

    month_number = months[
        invoice_month
    ]

    summary = get_customer_monthly_summary(
        customer_id,
        month_number,
        invoice_year
    )

    pdf_path = create_invoice_pdf(
        invoice_customer,
        invoice_month,
        invoice_year,
        summary
    )

    st.success(
        "PDF Invoice Generated!"
    )

    with open(pdf_path, "rb") as pdf_file:

        st.download_button(
            label="⬇ Download PDF Invoice",
            data=pdf_file,
            file_name=pdf_path.name,
            mime="application/pdf"
        )

        