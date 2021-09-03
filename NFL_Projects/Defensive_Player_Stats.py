import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def app():
    st.title('NFL Football Stats (Defense) Explorer')

    st.markdown("""
This app performs simple webscraping of NFL Football player stats data (focusing on Defense)!
* **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, seaborn
* **Data source:** [pro-football-reference.com](https://www.pro-football-reference.com/).
Data is from 1980 to 2020.
""")

    st.sidebar.header('User Customization')
    selected_year = st.sidebar.selectbox('Year', list(reversed(range(1980,2021))))

# Web scraping of NFL player stats
# https://www.pro-football-reference.com/years/2019/defense.htm
    @st.cache
    def load_data(year):
        url = "https://www.pro-football-reference.com/years/" + str(year) + "/defense.htm"
        html = pd.read_html(url, header = 1)
        df = html[0]
        raw = df.drop(df[df.Rk == 'Rk'].index) # Deletes repeating headers in content
   
        raw = raw.fillna(0)

        playerstats = raw.drop(['Rk'], axis=1)

        # Converting Columns Data Type to int Type
        playerstats['Int'] = playerstats['Int'].astype(int)
        playerstats['Yds'] = playerstats['Yds'].astype(int)
        playerstats['TD'] = playerstats['TD'].astype(int)
        playerstats['Lng'] = playerstats['Lng'].astype(int)
        playerstats['PD'] = playerstats['PD'].astype(int)
        playerstats['FF'] = playerstats['FF'].astype(int)
        playerstats['Fmb'] = playerstats['Fmb'].astype(int)
        playerstats['FR'] = playerstats['FR'].astype(int)
        playerstats['Yds.1'] = playerstats['Yds.1'].astype(int)
        playerstats['TD.1'] = playerstats['TD.1'].astype(int)
        playerstats['Sk'] = playerstats['Sk'].astype(float)
        playerstats['Comb'] = playerstats['Comb'].astype(int)
        playerstats['Solo'] = playerstats['Solo'].astype(int)
        playerstats['Ast'] = playerstats['Ast'].astype(int)
        playerstats['TFL'] = playerstats['TFL'].astype(int)
        playerstats['QBHits'] = playerstats['QBHits'].astype(int)
        playerstats['Sfty'] = playerstats['Sfty'].astype(int)


        # Renaming/Reformatting Certain Columns under incorrect naming
        playerstats.rename(columns={'Yds.1': 'Fmb Yds',
                                    'TD.1': 'Fmb TD'
                                    }, inplace= True)




        # Return Data Frame Titled playerstats
        return playerstats
    playerstats = load_data(selected_year)

# Sidebar - Team selection
    sorted_unique_team = sorted(playerstats.Tm.unique())
    selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

# Sidebar - Position selection
    unique_pos = ['LILB','RILB','SS','CB','RCB','LLB','FS','MLB','RLB','LCB','DB','ROLB','LOLB','OLB','DE','LDE','RDE','NT','DT','LDT','RDT']
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
    if st.button('Defensive Statistics'):
        st.header('Display Player Stats of Selected Team(s)')
        st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
        st.dataframe(df_selected_team)


# Player Data
#st.header('Display Stats of Selected Players')
#st.write('Data Dimension: ' + str(df_selected_player.shape[0]) + ' rows and ' + str(df_selected_player.shape[1]) + ' columns.')
#st.dataframe(df_selected_player)




# Download NFL player stats data
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




