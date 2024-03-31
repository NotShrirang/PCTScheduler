import pandas as pd
import numpy as np
import datetime
import sys
import streamlit as st


class Schedule:
    def __init__(self) -> None:
        self.final_schedule = pd.DataFrame()
        self.EST_schedules = {}
        self.schedules = {}
        self.portal_schedules = {}
        self.updated_schedule2 = {}
        self.new_format = {}


def schedule(raw_schedule, YEAR, MONTH_NAME):
    GROUPS = ['Group 1', 'Group 2', 'Group 3', 'Elite']
    MONTHS_COUNTER = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
                      'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}
    DAYS = {'Monday': 1, 'Tuesday': 2, 'Wednesday': 3,
            'Thursday': 4, 'Friday': 5, 'Saturday': 6, 'Sunday': 7}
    INT_TO_DAYS = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday',
                   3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}

    if YEAR % 4 == 0:
        MONTHS = {1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30,
                  7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    else:
        MONTHS = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
                  7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}

    # raw_schedule = pd.read_excel(f"{MONTH_NAME} Coaches' Schedule - {YEAR}.xlsx")

    raw_group3_schedule = pd.DataFrame(raw_schedule[[
                                       'Group 3 (1800 - 2300)', 'Unnamed: 1', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4']])
    Promotional_INDEX = raw_group3_schedule.loc[raw_group3_schedule['Group 3 (1800 - 2300)']
                                                == 'Special psychological class for all. Parents are also invited'].index
    if len(Promotional_INDEX) != 0:
        raw_group3_schedule.drop(
            range(Promotional_INDEX[0], raw_group3_schedule.index[-1]), inplace=True)
    Homework_INDEX = raw_group3_schedule.loc[raw_group3_schedule[
        'Group 3 (1800 - 2300)'] == 'Exercise Reviews'].index
    if len(Homework_INDEX) != 0:
        raw_group3_schedule.drop(
            range(Homework_INDEX[0], raw_group3_schedule.index[-1]), inplace=True)
    raw_group3_schedule.rename(columns={'Group 3 (1800 - 2300)': "Date", 'Unnamed: 1': "Day",
                               'Unnamed: 2': "IST Time", 'Unnamed: 3': 'Coach Name', 'Unnamed: 4': 'Topic'}, inplace=True)
    raw_group3_schedule.drop(raw_group3_schedule.index[0], inplace=True)
    Grp3_schedule = raw_group3_schedule.reset_index().drop(['index'], axis=1)
    Grp3_schedule.drop(
        [Grp3_schedule.index[-1], Grp3_schedule.index[-2]], inplace=True)
    null_list = Grp3_schedule.loc[Grp3_schedule['Date'].isnull()].index
    Grp3_schedule.drop(null_list, inplace=True)
    del null_list

    Grp1_schedule = raw_schedule[[
        'Group 1', 'Unnamed: 6', 'Unnamed: 7', 'Unnamed: 8', 'Unnamed: 9']].drop([0], axis=0)
    Grp1_schedule = Grp1_schedule.rename(columns={
                                         'Group 1': "Date", 'Unnamed: 6': "Day", 'Unnamed: 7': "IST Time", 'Unnamed: 8': 'Coach Name', 'Unnamed: 9': 'Topic'})
    SEMINARS_INDEX = Grp1_schedule.loc[Grp1_schedule['Day']
                                       == 'SEMINARS G2-3'].index[0]
    Grp1_schedule.drop(
        range(SEMINARS_INDEX-2, Grp1_schedule.index[-1]-1), inplace=True)
    Grp1_schedule.drop(Grp1_schedule.index[-1]-1, inplace=True)
    Grp1_schedule = Grp1_schedule.reset_index().drop(['index'], axis=1)
    Grp1_schedule.drop(Grp1_schedule.index[-1], inplace=True)
    Grp1_schedule.dropna(how='all', inplace=True)

    Grp2_schedule = raw_schedule[[
        'Group 1', 'Unnamed: 6', 'Unnamed: 7', 'Group 2', 'Unnamed: 11']].drop([0], axis=0)
    Grp2_schedule = Grp2_schedule.rename(columns={
                                         'Group 1': "Date", 'Unnamed: 6': "Day", 'Unnamed: 7': "IST Time", 'Group 2': 'Coach Name', 'Unnamed: 11': 'Topic'})
    Grp2_schedule.drop(
        range(SEMINARS_INDEX-2, Grp2_schedule.index[-1]-1), inplace=True)
    Grp2_schedule.drop(Grp2_schedule.index[-1]-1, inplace=True)
    Grp2_schedule = Grp2_schedule.reset_index().drop(['index'], axis=1)
    Grp2_schedule.drop(Grp2_schedule.index[-1], inplace=True)
    Grp2_schedule.dropna(how='all', inplace=True)

    Elite_schedule = raw_schedule[[
        'Elite Group (2300+)', 'Unnamed: 13', 'Unnamed: 14', 'Unnamed: 15', 'Unnamed: 16']].drop([0], axis=0)
    Elite_schedule = Elite_schedule.rename(columns={'Elite Group (2300+)': "Date", 'Unnamed: 13': "Day",
                                           'Unnamed: 14': "IST Time", 'Unnamed: 15': 'Coach Name', 'Unnamed: 16': 'Topic'})
    null_list = Elite_schedule.loc[Elite_schedule['Date'].isnull()].index
    Elite_schedule.drop(null_list, inplace=True)
    del null_list

    Grp1_schedule.insert(len(Grp1_schedule.columns), column='Group', value=[
                         "Group 1"]*len(Grp1_schedule.index))
    Grp2_schedule.insert(len(Grp2_schedule.columns), column='Group', value=[
                         "Group 2"]*len(Grp2_schedule.index))
    Grp3_schedule.insert(len(Grp3_schedule.columns), column='Group', value=[
                         "Group 3"]*len(Grp3_schedule.index))
    Elite_schedule.insert(len(Elite_schedule.columns), column='Group', value=[
                          "Elite"]*len(Elite_schedule.index))

    final_schedule = pd.concat([Grp1_schedule, Grp2_schedule, Grp3_schedule, Elite_schedule], axis=0, ignore_index=True, keys=[
                               'Freshers Group', 'Group 1', 'Group 2', 'Group 3', 'Elite Group'])

    # with pd.ExcelWriter(f'{MONTH_NAME} {YEAR} - Parsed Schedule.xlsx', datetime_format='YYYY-MM-DD HH:MM:SS') as writer:
    #     final_schedule.to_excel(writer, sheet_name='Schedule')

    REVIEW_TESTS = {"CLASS TYPE": "Review Tests", "GROUP": "",
                    "COACH": "", "DATE": "", "TIME": "", "TITLE": "Review Test"}
    TRAINING_GAMES = {"CLASS TYPE": "Training Games", "GROUP": "", "COACH": "",
                      "DATE": "", "TIME": "", "TITLE": "Training Games - 4 rounds - 10 + 2"}
    RAPID_TOURNAMENTS = {"CLASS TYPE": "Tournaments", "GROUP": "", "COACH": "",
                         "DATE": "", "TIME": "", "TITLE": "Rapid Tournament - 4 rounds - 10 + 2"}
    BLITZ_TOURNAMENTS = {"CLASS TYPE": "Tournaments", "GROUP": "", "COACH": "",
                         "DATE": "", "TIME": "", "TITLE": "Blitz Tournament - 7 rounds - 3 + 2"}
    SEMINAR = {"CLASS TYPE": "Seminars", "GROUP": "",
               "COACH": "", "DATE": "", "TIME": "", "TITLE": ""}
    EXERCISE_REVIEWS = {"GROUP": "", "DATE": "", "TIME": datetime.time(
        19, 0), "DAY": "", "COACH": "", "TITLE": "Exercise Review"}

    upload_schedule = pd.DataFrame()

    days = MONTHS[raw_group3_schedule['Date'].iloc[0].month]

    schedules: dict[str, pd.DataFrame] = {}
    EST_schedules = {}

    def ist_to_est(ist_series):
        est_df = pd.DataFrame(columns=['EST Date', 'EST Day', 'EST Time'])
        for count, entry in enumerate(list(ist_series[['TIME', 'DATE']].iloc)):
            diff = datetime.timedelta(hours=9, minutes=30)
            time = entry['TIME']
            date = entry['DATE']
            date_time = datetime.datetime(
                date.year, date.month, date.day, time.hour, time.minute)
            est_time = date_time - diff
            day = INT_TO_DAYS[est_time.weekday()]
            est_df.loc[len(est_df.index)] = (
                est_time.date(), day, est_time.time())
        return est_df

    for group in GROUPS:
        upload_schedule = pd.DataFrame()
        group_schedule = final_schedule.loc[final_schedule['Group'] == group]
        group_schedule = group_schedule.reset_index().drop(['index'], axis=1)
        month_span = group_schedule['Date'][0]
        curr_month = month_span.month
        curr_year = month_span.year
        week_count = 1
        temp_df = group_schedule[group_schedule['Coach Name'] != 'SEMINAR']
        temp_df = temp_df.rename(columns={'Date': "DATE", 'Day': "DAY", 'IST Time': "TIME",
                                 'Coach Name': 'COACH', 'Topic': 'TITLE', 'Group': 'GROUP'})
        temp_df.insert(len(temp_df.columns), column='CLASS TYPE',
                       value=["Lessons"]*len(temp_df.index))
        upload_schedule = pd.concat(
            [upload_schedule, temp_df], ignore_index=True)
        blitz = True
        had_tournament = False
        review_test = False
        for date_day_number in range(1, days):
            entry = {}
            curr_date = datetime.datetime(
                curr_year, curr_month, date_day_number, 00, 00, 00)
            day = INT_TO_DAYS[curr_date.weekday()]
            if (day == 'Monday' and group in ['Group 1', 'Group 2', 'Group 3']):
                if review_test:
                    entry = REVIEW_TESTS
                    entry['GROUP'] = group
                    entry['DATE'] = curr_date
                    entry['TIME'] = datetime.time(18, 30)
                    entry['DAY'] = day
                    temp_df = pd.DataFrame(entry, index=[0])
                    upload_schedule = pd.concat(
                        [upload_schedule, temp_df], ignore_index=True)
                    review_test = False
                else:
                    review_test = True
            if (day == 'Tuesday' and group == 'Group 3'):
                entry = TRAINING_GAMES
                entry['GROUP'] = group
                entry['DATE'] = datetime.datetime(
                    YEAR, MONTHS_COUNTER[MONTH_NAME], date_day_number)
                entry['TIME'] = datetime.time(20, 00)
                entry['DAY'] = day
                temp_df = pd.DataFrame(entry, index=[0])
                upload_schedule = pd.concat(
                    [upload_schedule, temp_df], ignore_index=True)
            if (day == 'Wednesday'):
                if group in ['Group 1', 'Group 2', 'Group 3']:
                    had_tournament = True
                    if blitz:
                        entry = BLITZ_TOURNAMENTS
                    else:
                        entry = RAPID_TOURNAMENTS
                    entry['GROUP'] = group
                    entry['DATE'] = datetime.datetime(
                        YEAR, MONTHS_COUNTER[MONTH_NAME], date_day_number)
                    entry['TIME'] = datetime.time(6, 30)
                    entry['DAY'] = day
                    temp_df = pd.DataFrame(entry, index=[0])
                    upload_schedule = pd.concat(
                        [upload_schedule, temp_df], ignore_index=True)
                if group in ['Group 1', 'Group 2']:
                    entry = TRAINING_GAMES
                    entry['GROUP'] = group
                    entry['DATE'] = datetime.datetime(
                        YEAR, MONTHS_COUNTER[MONTH_NAME], date_day_number)
                    entry['TIME'] = datetime.time(20, 00)
                    entry['DAY'] = day
                    temp_df = pd.DataFrame(entry, index=[0])
                    upload_schedule = pd.concat(
                        [upload_schedule, temp_df], ignore_index=True)
            if (day == 'Thursday' and group in ['Group 1', 'Group 2', 'Group 3']):
                had_tournament = True
                if blitz:
                    entry = BLITZ_TOURNAMENTS
                else:
                    entry = RAPID_TOURNAMENTS
                entry['GROUP'] = group
                entry['DATE'] = datetime.datetime(
                    YEAR, MONTHS_COUNTER[MONTH_NAME], date_day_number)
                entry['TIME'] = datetime.time(20, 00)
                entry['DAY'] = day
                temp_df = pd.DataFrame(entry, index=[0])
                upload_schedule = pd.concat(
                    [upload_schedule, temp_df], ignore_index=True)
            if (day == 'Friday' and group == 'Group 3'):
                entry = TRAINING_GAMES
                entry['GROUP'] = group
                entry['DATE'] = datetime.datetime(
                    YEAR, MONTHS_COUNTER[MONTH_NAME], date_day_number)
                entry['TIME'] = datetime.time(5, 30)
                entry['DAY'] = day
                temp_df = pd.DataFrame(entry, index=[0])
                upload_schedule = pd.concat(
                    [upload_schedule, temp_df], ignore_index=True)
            if (day == 'Saturday' and group in ['Group 1', 'Group 2']):
                if group in ['Group 1', 'Group 2']:
                    entry = TRAINING_GAMES
                    entry['GROUP'] = group
                    entry['DATE'] = datetime.datetime(
                        YEAR, MONTHS_COUNTER[MONTH_NAME], date_day_number)
                    entry['TIME'] = datetime.time(5, 30)
                    entry['DAY'] = day
                    temp_df = pd.DataFrame(entry, index=[0])
                    upload_schedule = pd.concat(
                        [upload_schedule, temp_df], ignore_index=True)
                    entry = SEMINAR
                    entry['GROUP'] = 'Group 1;Group 2'
                    entry['DATE'] = datetime.datetime(
                        YEAR, MONTHS_COUNTER[MONTH_NAME], date_day_number)
                    entry['TIME'] = datetime.time(20, 00)
                    entry['TITLE'] = "Seminar"
                    entry['DAY'] = day
                    temp_df = pd.DataFrame(entry, index=[0])
                    if group == 'Group 1':
                        if week_count in [2, 4]:
                            exercise_review = EXERCISE_REVIEWS.copy()
                            exercise_review['GROUP'] = group
                            exercise_review['DATE'] = datetime.datetime(
                                YEAR, MONTHS_COUNTER[MONTH_NAME], date_day_number)
                            exercise_review['TIME'] = datetime.time(
                                19, 30)
                            exercise_review['DAY'] = day
                            temp_df = pd.concat([temp_df, pd.DataFrame(
                                exercise_review, index=[0])], ignore_index=True)
                    upload_schedule = pd.concat(
                        [upload_schedule, temp_df], ignore_index=True)
            if (day == 'Sunday'):
                if group in ['Group 2', 'Group 3']:
                    entry = SEMINAR
                    entry['GROUP'] = 'Group 2;Group 3'
                    entry['DATE'] = datetime.datetime(
                        YEAR, MONTHS_COUNTER[MONTH_NAME], date_day_number)
                    entry['TIME'] = datetime.time(20, 00)
                    entry['TITLE'] = "Seminar - Group 2 & 3"
                    entry['DAY'] = day
                    temp_df = pd.DataFrame(entry, index=[0])
                    if week_count in [2, 4]:
                        exercise_review = EXERCISE_REVIEWS.copy()
                        exercise_review['GROUP'] = group
                        exercise_review['DATE'] = datetime.datetime(
                            YEAR, MONTHS_COUNTER[MONTH_NAME], date_day_number)
                        exercise_review['DAY'] = day
                        temp_df = pd.concat([temp_df, pd.DataFrame(
                            exercise_review, index=[0])], ignore_index=True)
                    upload_schedule = pd.concat(
                        [upload_schedule, temp_df], ignore_index=True)
                if had_tournament:
                    if blitz:
                        blitz = False
                    else:
                        blitz = True
                week_count += 1
        upload_schedule = upload_schedule[upload_schedule['COACH'] != 'Seminar']
        upload_schedule.sort_values(
            by=['DATE', 'TIME'], ignore_index=True, inplace=True)
        est_upload_schedule = upload_schedule.copy()
        est_df = ist_to_est(upload_schedule)
        est_upload_schedule.drop(['DATE', 'DAY', 'TIME'], axis=1, inplace=True)
        est_upload_schedule.insert(
            0, column='EST Date', value=est_df['EST Date'])
        est_upload_schedule.insert(
            1, column='EST Day', value=est_df['EST Day'])
        est_upload_schedule.insert(
            2, column='EST Time', value=est_df['EST Time'])
        schedules[group] = upload_schedule
        EST_schedules[group] = est_upload_schedule

    # with pd.ExcelWriter(f'{MONTH_NAME} {YEAR} - PDF EST.xlsx', datetime_format='YYYY-MM-DD') as writer:
    #     EST_schedules['Group 1'].to_excel(writer, sheet_name='Group 1')
    #     EST_schedules['Group 2'].to_excel(writer, sheet_name='Group 2')
    #     EST_schedules['Group 3'].to_excel(writer, sheet_name='Group 3')
    #     EST_schedules['Elite'].to_excel(writer, sheet_name='Elite')

    # with pd.ExcelWriter(f'{MONTH_NAME} {YEAR} - PDF IST.xlsx', datetime_format='YYYY-MM-DD') as writer:
    #     schedules['Group 1'].to_excel(writer, sheet_name='Group 1')
    #     schedules['Group 2'].to_excel(writer, sheet_name='Group 2')
    #     schedules['Group 3'].to_excel(writer, sheet_name='Group 3')
    #     schedules['Elite'].to_excel(writer, sheet_name='Elite')

    portal_schedules = {}
    for group, schedule in schedules.items():
        temp = schedule.drop("DAY", axis=1)
        temp = temp[['CLASS TYPE', 'GROUP', 'COACH', 'DATE', 'TIME', 'TITLE']]
        temp['DATE'] = pd.to_datetime(temp['DATE']).dt.strftime('%Y-%m-%d')
        temp['TIME'] = pd.to_datetime(
            temp['TIME'], format='%H:%M:%S').dt.strftime('%I:%M')
        portal_schedules[group] = temp

    # with pd.ExcelWriter(f'{MONTH_NAME} {YEAR} - Upload on Portal.xlsx', datetime_format='YYYY-MM-DD') as writer:
    #     portal_schedules['Group 1'].to_excel(writer, sheet_name='Group 1')
    #     portal_schedules['Group 2'].to_excel(writer, sheet_name='Group 2')
    #     portal_schedules['Group 3'].to_excel(writer, sheet_name='Group 3')
    #     portal_schedules['Elite'].to_excel(writer, sheet_name='Elite')

    updated_schedule2 = {}
    for group in GROUPS:
        curr_sch = schedules[group].copy()
        est_data = EST_schedules[group][['EST Time', 'EST Day', 'EST Date']]
        curr_sch.insert(3, column='EST Date', value=est_data['EST Date'])
        curr_sch.insert(4, column='EST Day', value=est_data['EST Day'])
        curr_sch.insert(5, column='EST Time', value=est_data['EST Time'])
        curr_sch.drop(columns=['GROUP', 'CLASS TYPE'], inplace=True)
        updated_schedule2[group] = curr_sch.copy()

    def convert(df):
        converted_str = df['DAY'] + " " + str(df['DATE'].day) + " | " + str(datetime.datetime.strptime(str(df['TIME']), "%H:%M:%S").strftime("%I:%M %p")) + " IST " + \
            " " + df['EST Day'] + " " + str(df['EST Date'].day) + " | " + str(
                datetime.datetime.strptime(str(df['EST Time']), "%H:%M:%S").strftime("%I:%M %p")) + " EST "
        return converted_str

    updated_schedule3 = {}
    for group in GROUPS:
        curr_sch = updated_schedule2[group].copy()
        curr_sch['DATE AND TIME'] = curr_sch[['DATE', 'DAY', 'TIME', 'EST Date',
                                              'EST Day',	'EST Time']].apply(lambda x: convert(x), axis=1)
        curr_sch.drop(columns=['DATE', 'DAY', 'TIME',
                      'EST Date', 'EST Day', 'EST Time'], inplace=True)
        curr_sch = curr_sch[['DATE AND TIME', 'COACH', 'TITLE']]
        updated_schedule3[group] = curr_sch.copy()

    # with pd.ExcelWriter(f'{MONTH_NAME} {YEAR} - IST EST Combined.xlsx', datetime_format='YYYY-MM-DD') as writer:
    #     updated_schedule2['Group 1'].to_excel(writer, sheet_name='Group 1')
    #     updated_schedule2['Group 2'].to_excel(writer, sheet_name='Group 2')
    #     updated_schedule2['Group 3'].to_excel(writer, sheet_name='Group 3')
    #     updated_schedule2['Elite'].to_excel(writer, sheet_name='Elite')

    sch = Schedule()
    sch.final_schedule = final_schedule
    sch.EST_schedules = EST_schedules
    sch.schedules = schedules
    sch.portal_schedules = portal_schedules
    sch.updated_schedule2 = updated_schedule2
    sch.new_format = updated_schedule3

    return sch, portal_schedules
