st.set_page_config(
    page_title="NFL Web Scraper App",
    page_description="",

    layout="wide",
    initial_sidebar_state="expanded",
)

import Passing_Stats
import Rushing_Stats
import Receiving_Stats
import Defensive_Player_Stats
import Kicking_Stats
import Kick_Returning_Stats
import Scoring_Stats
import Fantasy_Stats
import streamlit as st
import streamlit.components.v1 as components


#components.html(
#'''
#<!DOCTYPE html>
#<html lang="en">
#    <head>
#    <title>NFL Web Scraper App</title>
#
#    <meta name="social-image" property="og:image" content="%PUBLIC_URL%/nfl_app_scraper_web.png" />
#    </head>
#</html>
#''' 
#)

Pages = {
    "Passing Stats": Passing_Stats,
    "Rushing Stats": Rushing_Stats,
    "Receiving Stats": Receiving_Stats,
    "Defensive Stats": Defensive_Player_Stats,
    "Kicking Stats": Kicking_Stats,
    "Kick/Punt Returner Stats": Kick_Returning_Stats,
    "Player Scoring Stats": Scoring_Stats,
    "Fantasy Stats": Fantasy_Stats

}

st.title('Pro Football Web Scraper')
st.sidebar.title('Pro Football Statistics')

selection = st.sidebar.selectbox("Select One Of The Following Individual Categories",list(Pages.keys()))
page = Pages[selection]

if page:
    page.app()