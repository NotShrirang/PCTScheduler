import streamlit as st
from .scheduler import Schedule, schedule
import pandas as pd
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb

def to_excel(df: pd.DataFrame):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.close()
    processed_data = output.getvalue()
    return processed_data

def render_schedule_page():
    st.header("Schedule Page")
    month = st.selectbox("Select Month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
    year = st.selectbox("Select Year", [2021, 2022, 2023, 2024, 2025, 2026, 2027])
    uploaded_file = st.file_uploader("Upload a Excel / CSV file", type=["xlsx", "csv"])
    if uploaded_file is not None:
        if uploaded_file.name[-4:] == "xlsx":
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)
        schedule_group = st.radio("Select Schedule", ["Group 1", "Group 2", "Group 3", "Elite"])
        schedule_button = st.button("Schedule")
        if schedule_button:
            schedule_obj = schedule(df, year, month)
            st.success("Schedule Generated")
            st.table(schedule_obj.updated_schedule2[str(schedule_group)])
            df_xlsx = to_excel(schedule_obj.updated_schedule2[str(schedule_group)])
            st.download_button("⬇️ Download Schedule", data=df_xlsx, file_name="{}{} - {}.xlsx".format(month, year, schedule_group), mime="application/vnd.ms-excel")