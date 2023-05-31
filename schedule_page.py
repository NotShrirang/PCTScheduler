import streamlit as st
from utils.scheduler import Schedule, schedule
import pandas as pd
from utils.file_downloader import to_excel

@st.cache_data(experimental_allow_widgets=True)
def render_schedule_page():
    st.header("Scheduler Page")
    month = st.selectbox("Select Month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
    year = st.selectbox("Select Year", [2021, 2022, 2023, 2024, 2025, 2026, 2027])
    uploaded_file = st.file_uploader("Upload Coaches' schedule file here...", type=["xlsx", "csv"])
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
            st.dataframe(schedule_obj.updated_schedule2[str(schedule_group)], use_container_width=True)
            df_xlsx = to_excel([schedule_obj.updated_schedule2[str(schedule_group)]], ["Final Schedule"])
            st.download_button("⬇️ Download Schedule", data=df_xlsx, file_name="{}{} - {}.xlsx".format(month, year, schedule_group), mime="application/vnd.ms-excel")