import streamlit as st

from utils.db import (
    get_monthly_work_records,
    get_monthly_payments,
    get_monthly_summary
)

from utils.excel_export import (
    create_monthly_excel_report
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


        