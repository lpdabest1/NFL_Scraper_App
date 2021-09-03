import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def app():
    st.title('NFL Football Stats (Kicking) Explorer')

    st.markdown("""
This app performs simple webscraping of NFL Football player stats data (focusing on Kicking)!
* **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, seaborn
* **Data source:** [pro-football-reference.com](https://www.pro-football-reference.com/).
Data is from 1940 to 2020.
""")

    st.sidebar.header('User Customization')
    selected_year = st.sidebar.selectbox('Year', list(reversed(range(1940,2021))))

# Web scraping of NFL player stats
# https://www.pro-football-reference.com/years/2019/rushing.htm
    @st.cache
    def load_data(year):
        url = "https://www.pro-football-reference.com/years/" + str(year) + "/kicking.htm"
        html = pd.read_html(url, header = 1)
        df = html[0]
        raw = df.drop(df[df.Rk == 'Rk'].index) # Deletes repeating headers in content
        raw = raw.assign(Pos='P/K')
        raw = raw.fillna(0)
        playerstats = raw.drop(['Rk'], axis=1)
        playerstats['Pos'] = playerstats['Pos'].str.upper()
        # Converting Columns Data Type to int Type
        playerstats = playerstats.astype({'FGA':'int',
                                          'FGM':'int',
                                          'FGA.1':'int',
                                          'FGM.1':'int',
                                          'FGA.2':'int',
                                          'FGM.2':'int',
                                          'FGA.3':'int',
                                          'FGM.3':'int',
                                          'FGA.4':'int',
                                          'FGM.4':'int',
                                          'FGA.5': 'int',
                                          'FGM.5': 'int',
                                          'Lng': 'int',
                                          'FG%': 'str',
                                          'XPA':'int',
                                          'XPM':'int',
                                          'XP%':'str',
                                          'KO':'int',
                                          'KOYds':'int',
                                          'TB':'int',
                                          'TB%':'str',
                                          'KOAvg':'float64',
                                          'Pnt':'int',
                                          'Yds': 'int',
                                          'Lng.1': 'int',
                                          'Blck': 'int',
                                          'Y/P': 'float64'
                                            })




        # Renaming/Reformatting Certain Columns under incorrect naming
        playerstats.rename(columns={      'FGA':'FGA (0-19yds)',
                                          'FGM':'FGM (0-19yds)',
                                          'FGA.1':'FGA (20-29yds)',
                                          'FGM.1':'FGM (20-29yds)',
                                          'FGA.2':'FGA (30-39yds)',
                                          'FGM.2':'FGM (30-39yds)',
                                          'FGA.3':'FGA (40-49yds)',
                                          'FGM.3':'FGM (40-49yds)',
                                          'FGA.4':'FGA (50+ yds)',
                                          'FGM.4':'FGM (50+ yds)',
                                          'FGA.5': 'Total FGA',
                                          'FGM.5': 'Total FGM',
                                          'Lng': 'FG Lng',
                                          'KOYds':'KO Yds',
                                          'KOAvg':'KO Avg',
                                          'Pnt':'Punt',
                                          'Yds': 'Punt Yds',
                                          'Lng.1': 'Punt Lng',
                                    }, inplace= True)

        return playerstats
    playerstats = load_data(selected_year)


# Sidebar - Team selection
    sorted_unique_team = sorted(playerstats.Tm.unique())
    selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

# Sidebar - Position selection
    unique_pos = ['P/K']
    selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

# Sidebar - Player selection
#sorted_unique_player = sorted(playerstats.Player.unique())
#selected_player = st.sidebar.multiselect('Player', sorted_unique_player, sorted_unique_player) 


# Filtering data
# Team
    df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]

# Player
#df_selected_player = playerstats[(playerstats.Player.isin(selected_player)) & (playerstats.Pos.isin(selected_pos))]

# Team Data
    if st.button('Kicking Statistics'):
        st.header('Display Player Stats of Selected Team(s)')
        st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
        st.dataframe(df_selected_team)


# Player Data
#st.header('Display Stats of Selected Players')
#st.write('Data Dimension: ' + str(df_selected_player.shape[0]) + ' rows and ' + str(df_selected_player.shape[1]) + ' columns.')
#st.dataframe(df_selected_player)




# Download NBA player stats data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
    def filedownload(df):
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
        href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
        return href

    st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)

# Heatmap
    if st.button('Intercorrelation Heatmap'):
        st.header('Intercorrelation Matrix Heatmap')
        df_selected_team.to_csv('output.csv',index=False)
        df = pd.read_csv('output.csv')

        corr = df.corr()
        mask = np.zeros_like(corr)
        mask[np.triu_indices_from(mask)] = True
        with sns.axes_style("white"):
            f, ax = plt.subplots(figsize=(7, 5))
            ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
        st.pyplot(f)




