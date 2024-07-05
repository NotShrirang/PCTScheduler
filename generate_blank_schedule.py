import streamlit as st
import pandas as pd
import numpy as np
import datetime
from utils.file_downloader import to_excel


@st.cache_data(experimental_allow_widgets=True)
def render_generate_schedule():
    st.header("Generate Blank Schedule Page")
    month = st.selectbox("Select Month", ["January", "February", "March", "April",
                         "May", "June", "July", "August", "September", "October", "November", "December"])
    MONTH = month
    year = st.selectbox(
        "Select Year", [2021, 2022, 2023, 2024, 2025, 2026, 2027])
    generate_button = st.button("Generate Schedule")
    if generate_button:
        MONTHS_COUNTER = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
                          'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}
        if year % 4 == 0:
            MONTHS = {1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30,
                      7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
        else:
            MONTHS = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
                      7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}

        SEMINAR = {"GROUP": "", "DATE": "", "TIME": "",
                   "DAY": "", "COACH": "", "TITLE": "SEMINAR"}
        CLASS = {"GROUP": "", "DATE": "", "TIME": "",
                 "DAY": "", "COACH": "", "TITLE": ""}
        EXERCISE_REVIEWS = {"GROUP": "", "DATE": "", "TIME": datetime.time(
            19, 0).strftime("%H:%M"), "DAY": "", "COACH": "", "TITLE": "Exercise Reviews"}

        ALL_SEMINARS = {"Group 1 + 2": {}, "Group 2 + 3": {}}

        month = MONTHS_COUNTER[month]
        month_days = MONTHS[month]

        final_schedules = {}
        grp1_schedule = pd.DataFrame()
        grp2_schedule = pd.DataFrame()
        grp3_schedule = pd.DataFrame()
        elite_schedule = pd.DataFrame()
        super_gm_schedule = pd.DataFrame()
        seminar_schedule = pd.DataFrame()
        exercise_review = pd.DataFrame()

        temp = SEMINAR.copy()
        temp["GROUP"] = "Group"
        temp["DATE"] = "Date"
        temp["TIME"] = "Time"
        temp["DAY"] = "Day"
        temp["COACH"] = "Coach"
        temp["TITLE"] = "Title"
        temp = pd.DataFrame([temp])
        seminar_schedule = pd.concat(
            [seminar_schedule, temp], ignore_index=True, axis=0)
        exercise_review = pd.concat(
            [exercise_review, temp], ignore_index=True, axis=0)

        week_counter = 1

        for day in range(1, month_days+1):
            current_date = datetime.date(year, month, day)
            current_day = current_date.strftime("%A")
            current_date = current_date.strftime("%Y-%m-%d")
            if current_day == "Monday":
                entry = CLASS.copy()
                entry["DATE"] = current_date
                entry["DAY"] = current_day
                entry["TIME"] = datetime.time(20, 0).strftime("%H:%M")
                entry["GROUP"] = "Elite"
                elite_schedule = pd.concat(
                    [elite_schedule, pd.DataFrame([entry])], ignore_index=True, axis=0)
                entry["TIME"] = datetime.time(20, 30).strftime("%H:%M")
                entry["GROUP"] = "Group 3"
                grp3_schedule = pd.concat(
                    [grp3_schedule, pd.DataFrame([entry])], ignore_index=True, axis=0)
                continue
            elif current_day == "Tuesday":
                entry = CLASS.copy()
                entry["DATE"] = current_date
                entry["DAY"] = current_day
                entry["TIME"] = datetime.time(20, 0).strftime("%H:%M")
                entry["GROUP"] = "Group 1"
                grp1_schedule = pd.concat(
                    [grp1_schedule, pd.DataFrame([entry])], ignore_index=True, axis=0)
                entry["GROUP"] = "Group 2"
                grp2_schedule = pd.concat(
                    [grp2_schedule, pd.DataFrame([entry])], ignore_index=True, axis=0)
                continue
            elif current_day == "Wednesday":
                entry = CLASS.copy()
                entry["DATE"] = current_date
                entry["DAY"] = current_day
                entry["TIME"] = datetime.time(20, 0).strftime("%H:%M")
                entry["GROUP"] = "Elite"
                elite_schedule = pd.concat(
                    [elite_schedule, pd.DataFrame([entry])], ignore_index=True, axis=0)
                continue
            elif current_day == "Thursday":
                entry = CLASS.copy()
                entry["DATE"] = current_date
                entry["DAY"] = current_day
                entry["TIME"] = datetime.time(5, 30).strftime("%H:%M")
                entry["GROUP"] = "Group 3"
                grp3_schedule = pd.concat(
                    [grp3_schedule, pd.DataFrame([entry])], ignore_index=True, axis=0)
                continue
            elif current_day == "Friday":
                entry = CLASS.copy()
                entry["DATE"] = current_date
                entry["DAY"] = current_day
                entry["TIME"] = datetime.time(5, 30).strftime("%H:%M")
                entry["GROUP"] = "Group 1"
                grp1_schedule = pd.concat(
                    [grp1_schedule, pd.DataFrame([entry])], ignore_index=True, axis=0)
                entry["GROUP"] = "Group 2"
                grp2_schedule = pd.concat(
                    [grp2_schedule, pd.DataFrame([entry])], ignore_index=True, axis=0)
                entry["TIME"] = datetime.time(20, 0).strftime("%H:%M")
                entry["GROUP"] = "Group 3"
                grp3_schedule = pd.concat(
                    [grp3_schedule, pd.DataFrame([entry])], ignore_index=True, axis=0)
                entry["GROUP"] = "Elite"
                elite_schedule = pd.concat(
                    [elite_schedule, pd.DataFrame([entry])], ignore_index=True, axis=0)
                continue
            elif current_day == "Saturday":
                entry = SEMINAR.copy()
                entry["DATE"] = current_date
                entry["DAY"] = current_day
                entry["TIME"] = datetime.time(20, 0).strftime("%H:%M")
                entry["GROUP"] = "Group 1"
                grp1_schedule = pd.concat(
                    [grp1_schedule, pd.DataFrame([entry])], ignore_index=True, axis=0)
                entry["GROUP"] = "Group 2"
                grp2_schedule = pd.concat(
                    [grp2_schedule, pd.DataFrame([entry])], ignore_index=True, axis=0)
                entry["GROUP"] = "Group 1 + 2"
                entry['TITLE'] = ""
                seminar_schedule = pd.concat(
                    [seminar_schedule, pd.DataFrame([entry])], ignore_index=True, axis=0)
                ALL_SEMINARS["Group 1 + 2"][current_date] = entry
                entry = CLASS.copy()
                entry["DATE"] = current_date
                entry["DAY"] = current_day
                entry["TIME"] = datetime.time(20, 0).strftime("%H:%M")
                entry["GROUP"] = "Group 3"
                grp3_schedule = pd.concat(
                    [grp3_schedule, pd.DataFrame([entry])], ignore_index=True, axis=0)
                entry["GROUP"] = "Elite"
                elite_schedule = pd.concat(
                    [elite_schedule, pd.DataFrame([entry])], ignore_index=True, axis=0)
                if week_counter in [2, 4]:
                    entry = EXERCISE_REVIEWS.copy()
                    entry["DATE"] = current_date
                    entry["DAY"] = current_day
                    entry["GROUP"] = "Group 1"
                    exercise_review = pd.concat(
                        [exercise_review, pd.DataFrame([entry])], ignore_index=True, axis=0)
                continue
            elif current_day == "Sunday":
                entry = CLASS.copy()
                entry["DATE"] = current_date
                entry["DAY"] = current_day
                entry["TIME"] = datetime.time(20, 0).strftime("%H:%M")
                entry["GROUP"] = "Group 1"
                grp1_schedule = pd.concat(
                    [grp1_schedule, pd.DataFrame([entry])], ignore_index=True, axis=0)
                entry = SEMINAR.copy()
                entry["DATE"] = current_date
                entry["DAY"] = current_day
                entry["TIME"] = datetime.time(20, 0).strftime("%H:%M")
                entry["GROUP"] = "Group 2"
                grp2_schedule = pd.concat(
                    [grp2_schedule, pd.DataFrame([entry])], ignore_index=True, axis=0)
                entry["GROUP"] = "Group 3"
                grp3_schedule = pd.concat(
                    [grp3_schedule, pd.DataFrame([entry])], ignore_index=True, axis=0)
                entry["GROUP"] = "Group 2 + 3"
                entry['TITLE'] = ""
                seminar_schedule = pd.concat(
                    [seminar_schedule, pd.DataFrame([entry])], ignore_index=True, axis=0)
                ALL_SEMINARS["Group 2 + 3"][current_date] = entry
                entry = CLASS.copy()
                if week_counter in [2, 4]:
                    entry = EXERCISE_REVIEWS.copy()
                    entry["DATE"] = current_date
                    entry["DAY"] = current_day
                    entry["GROUP"] = "Group 2 + 3"
                    exercise_review = pd.concat(
                        [exercise_review, pd.DataFrame([entry])], ignore_index=True, axis=0)
                week_counter += 1
                continue
        final_schedules["Group 1"] = grp1_schedule
        final_schedules["Group 2"] = grp2_schedule
        final_schedules["Group 3"] = grp3_schedule
        final_schedules["Elite"] = elite_schedule
        # final_schedules["Super GM"] = super_gm_schedule

        final_schedules["Group 1"].sort_values(
            by=["DATE", "TIME"], inplace=True)
        final_schedules["Group 2"].sort_values(
            by=["DATE", "TIME"], inplace=True)
        final_schedules["Group 3"].sort_values(
            by=["DATE", "TIME"], inplace=True)
        final_schedules["Elite"].sort_values(
            by=["DATE", "TIME"], inplace=True)
        # final_schedules["Super GM"].sort_values(
        #     by=["DATE", "TIME"], inplace=True)

        final_schedule_df = pd.DataFrame()
        for _, schedule in final_schedules.items():
            final_schedule_df = pd.concat(
                [final_schedule_df, schedule], ignore_index=True, axis=1)

        final_schedule_df.columns = ["Group 1", "Group 1 Date", "Group 1 Time", "Group 1 Day", "Group 1 Coach", "Group 1 Topic", "Group 2", "Group 2 Date", "Group 2 Time", "Group 2 Day", "Group 2 Coach",
                                     "Group 2 Topic", "Group 3", "Group 3 Date", "Group 3 Time", "Group 3 Day", "Group 3 Coach", "Group 3 Topic", "Elite", "Elite Date", "Elite Time", "Elite Day", "Elite Coach", "Elite Topic", ]
                                    #  "Super GM", "Super GM Date", "Super GM Time", "Super GM Day", "Super GM Coach", "Super GM Topic"]
        seminar_schedule23 = seminar_schedule[seminar_schedule["GROUP"]
                                              == "Group 2 + 3"]
        seminar_schedule12 = seminar_schedule[seminar_schedule["GROUP"]
                                              == "Group 1 + 2"]
        seminar_schedule = pd.concat(
            [temp, seminar_schedule23, temp, seminar_schedule12], ignore_index=True, axis=0)
        seminar_schedule.columns = [
            "Group 2", "Group 2 Date", "Group 2 Time", "Group 2 Day", "Group 2 Coach", "Group 2 Topic"]
        exercise_review.columns = ["Group 1", "Group 1 Date",
                                   "Group 1 Time", "Group 1 Day", "Group 1 Coach", "Group 1 Topic"]

        exercise_review_and_seminar = pd.concat(
            [exercise_review, seminar_schedule], ignore_index=True, axis=1)
        exercise_review_and_seminar.columns = ["Group 1", "Group 1 Date", "Group 1 Time", "Group 1 Day", "Group 1 Coach",
                                               "Group 1 Topic", "Group 2", "Group 2 Date", "Group 2 Time", "Group 2 Day", "Group 2 Coach", "Group 2 Topic"]

        final_schedule_df = pd.concat(
            [final_schedule_df, exercise_review_and_seminar], ignore_index=True, axis=0)

        st.success("Blank Schedule generated successfully!")
        st.subheader("Final Schedule")
        st.dataframe(final_schedule_df, use_container_width=True)
        st.subheader("Seminar Schedule")
        st.dataframe(seminar_schedule, use_container_width=True)

        df_xlsx = to_excel([final_schedule_df], ["Final Schedule"])
        st.download_button("⬇️ Download Schedule", data=df_xlsx,
                           file_name="{}{} - Coaches Schedule.xlsx".format(MONTH, year), mime="application/vnd.ms-excel")
