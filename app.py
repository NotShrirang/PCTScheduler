import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import datetime
from utils import schedule_page, generate_blank_schedule

st.set_page_config(
    page_title="Scheduler",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="auto",)

st.markdown("<center><h1 Style='overflow: visible; padding-bottom: 50px; padding-top: 0px;'>Scheduler</h1></center>", unsafe_allow_html=True)

selected = option_menu(
        menu_title=None,
        options=["Scheduler", "Generate PDF"],
        icons=['Schedule', 'info'],
        default_index=0,
        orientation = "horizontal",
        styles={
        "container": {"padding": "5!important", "background-color": "gray"},
        "icon": {"color": "#2ECC71", "font-size": "25px"},
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "light-grey"},
        "nav-link-selected": {"background-color": "#2ECC71"},
        }
)
if selected == "Scheduler":
    schedule_page.render_schedule_page()
elif selected == "Generate PDF":
    generate_blank_schedule.render_generate_schedule()
        
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden; }
        footer {visibility: hidden;}
        </style>
        """

st.markdown(hide_menu_style, unsafe_allow_html=True)