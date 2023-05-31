import streamlit as st
import pandas as pd
import numpy as np
import datetime
from utils.file_downloader import to_excel

@st.cache_data(experimental_allow_widgets=True)
def render_fen_schedule():
    st.header("Generate FEN Schedule Page")
    MONTH = st.selectbox("Select Month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
    year = st.selectbox("Select Year", [2021, 2022, 2023, 2024, 2025, 2026, 2027])

    generate_button = st.button("Generate Schedule")
    if generate_button:
        MONTHS_COUNTER = {'January' : 1, 'February' : 2, 'March' : 3, 'April' : 4, 'May' : 5, 'June' : 6, 'July' : 7, 'August' : 8, 'September' : 9, 'October' : 10, 'November' : 11, 'December' : 12}
        if year % 4 == 0:
            MONTHS = {1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
        else:
            MONTHS = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}

        TRAINING_GAMES = {"GROUP 3 DATE" : "", "DAY": "", "TIME": "", "TITLE" : "", "FEN": ""}

        month = MONTHS_COUNTER[MONTH]
        month_days = MONTHS[month]

        fen_schedule23 = pd.DataFrame()
        fen_schedule1 = pd.DataFrame()
        
        day_counter = 1

        for day_counter in range(1, month_days+1):
            current_date = datetime.date(year, month, day_counter)
            next_date = (current_date + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            current_day = current_date.strftime("%A")
            next_day = (current_date + datetime.timedelta(days=1)).strftime("%A")

            if current_day == "Tuesday":
                entry = TRAINING_GAMES.copy()
                entry["GROUP 3 DATE"] = current_date.strftime("%Y-%m-%d")
                entry["GROUP 2 DATE"] = next_date
                entry["DAY"] = current_day
                entry["TIME"] = datetime.time(20, 0).strftime("%H:%M")
                fen_schedule23 = pd.concat([fen_schedule23, pd.DataFrame([entry])], ignore_index=True, axis=0)

                entry = TRAINING_GAMES.copy()
                entry.pop("GROUP 3 DATE")
                entry["GROUP 1 DATE"] = next_date
                entry["DAY"] = next_day
                entry["TIME"] = datetime.time(20, 0).strftime("%H:%M")
                fen_schedule1 = pd.concat([fen_schedule1, pd.DataFrame([entry])], ignore_index=True, axis=0)
                continue
            elif current_day == "Friday":
                entry = TRAINING_GAMES.copy()
                entry["GROUP 3 DATE"] = current_date.strftime("%Y-%m-%d")
                entry["GROUP 2 DATE"] = next_date
                entry["DAY"] = current_day
                entry["TIME"] = datetime.time(5, 30).strftime("%H:%M")
                fen_schedule23 = pd.concat([fen_schedule23, pd.DataFrame([entry])], ignore_index=True, axis=0)

                entry = TRAINING_GAMES.copy()
                entry.pop("GROUP 3 DATE")
                entry["GROUP 1 DATE"] = current_date + datetime.timedelta(days=1)
                entry["DAY"] = next_day
                entry["TIME"] = datetime.time(5, 30).strftime("%H:%M")
                fen_schedule1 = pd.concat([fen_schedule1, pd.DataFrame([entry])], ignore_index=True, axis=0)
                continue

        fen_schedule23.columns = ["GROUP 2 DATE", "GROUP 3 DATE", "GROUP 3 DAY", "TIME", "TITLE", "FEN"]
        fen_schedule1 = fen_schedule1[["GROUP 1 DATE", "DAY", "TIME", "TITLE", "FEN"]]
        fen_schedule23 = fen_schedule23[["GROUP 2 DATE", "GROUP 3 DATE", "GROUP 3 DAY", "TIME", "TITLE", "FEN"]]
        st.success("Blank Schedule generated successfully!")
        st.subheader("FEN Schedule for Group 1")
        st.dataframe(fen_schedule1, use_container_width=True)
        st.subheader("FEN Schedule for Group 2 and 3")
        st.dataframe(fen_schedule23, use_container_width=True)

        df_xlsx = to_excel([fen_schedule1, fen_schedule23], ["Group 1", "Group 2 and 3"])
        st.download_button("⬇️ Download Schedule", data=df_xlsx, file_name="{}{} - FENs.xlsx".format(MONTH, year), mime="application/vnd.ms-excel")

                
