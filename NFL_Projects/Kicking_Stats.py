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
# https://www.pro-football-reference.com/years/2019/kicking.htm
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
                                          'Tm':'Team'
                                    }, inplace= True)

        return playerstats
    playerstats = load_data(selected_year)


# Sidebar - Team selection
    sorted_unique_team = sorted(playerstats.Team.unique())
    selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

# Sidebar - Position selection
    unique_pos = ['P/K']
    selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

# Sidebar - Player selection
#sorted_unique_player = sorted(playerstats.Player.unique())
#selected_player = st.sidebar.multiselect('Player', sorted_unique_player, sorted_unique_player) 


# Filtering data
# Team
    df_selected_team = playerstats[(playerstats.Team.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]

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

    # User Personal Visualization Choices
    st.title('Data Visualizations')
    st.markdown('Select an option/checkbox on the left sidebar under the section Data visualizations to see the various Data Visualizations.')
    st.sidebar.subheader('Data Visualizations')

    # Categorical Plots Section
    if st.sidebar.checkbox('Categorical Plots'):
        st.subheader('Categorical Plots')
        st.info('Below are all of the categorical plots available to try and test out. Choose a few of them (if not all), you can customize the data you want to examine to see specific results or behaviors/trends')

        # if 'Histogram' button is selected
        df_selected_team.to_csv('categorical_plots.csv', index=False)
        df = pd.read_csv('categorical_plots.csv')


        unique_columns = ['Team','Pos','FGA (0-19yds)','FGM (0-19yds)','FGA (20-29yds)','FGM (20-29yds)','FGA (30-39yds)','FGM (30-39yds)','FGA (40-49yds)','FGM (40-49yds)','FGA (50+ yds)','FGM (50+ yds)',
                          'Total FGA','Total FGM','FG Lng','FG%','XPA','XPM','XP%','KO','KO Yds','TB','TB%','KO Avg','Punt','Punt Yds','Punt Lng','Blck','Y/P']
        statistical_columns = ['FGA (0-19yds)','FGM (0-19yds)','FGA (20-29yds)','FGM (20-29yds)','FGA (30-39yds)','FGM (30-39yds)','FGA (40-49yds)','FGM (40-49yds)','FGA (50+ yds)','FGM (50+ yds)',
                          'Total FGA','Total FGM','FG Lng','FG%','XPA','XPM','XP%','KO','KO Yds','TB','TB%','KO Avg','Punt','Punt Yds','Punt Lng','Blck','Y/P']

        # Selectable columns
        st.sidebar.info('Select two variables on the sidebar to conduct categorical plot(s)')
        df_columns = st.sidebar.selectbox("Select first variable/column",unique_columns)
        df_stats = st.sidebar.selectbox("Select second variable/column", statistical_columns)

        if st.checkbox('Bar Plot'):
            st.subheader('Bar Plot')
            

            #Graphing Bar Plot
            with sns.axes_style("white"):
            
                f, ax = plt.subplots(figsize=(12,5))
                plt.xticks(rotation=90)
                #ax = sns.histplot(df[df_stats])
                ax = sns.barplot(x=df[df_columns] , y=df[df_stats])
            st.pyplot(f)

        if st.checkbox('Strip Plot'):
            st.subheader('Strip Plot')

            #Graphing Strip Plot
            with sns.axes_style("white"):
            
                f, ax = plt.subplots(figsize=(12,5))
                plt.xticks(rotation=90)
                #ax = sns.histplot(df[df_stats])
                ax = sns.stripplot(x=df[df_columns] , y=df[df_stats])
            st.pyplot(f)


        if st.checkbox('Box Plot'):
            st.subheader('Box Plot')

            #Graphing Box Plot
            with sns.axes_style("white"):
            
                f, ax = plt.subplots(figsize=(12,5))
                plt.xticks(rotation=90)
                #ax = sns.histplot(df[df_stats])
                ax = sns.boxplot(x=df[df_columns] , y=df[df_stats])
            st.pyplot(f)


        if st.checkbox('Violin Plot'):
            st.subheader('Violin Plot')

            #Graphing Violin Plot
            with sns.axes_style("white"):
            
                f, ax = plt.subplots(figsize=(12,5))
                plt.xticks(rotation=90)
                #ax = sns.histplot(df[df_stats])
                ax = sns.violinplot(x=df[df_columns] , y=df[df_stats])
            st.pyplot(f)



    # Distribution/Relational Plots Section
    if st.sidebar.checkbox('Distribution & Relational Plots'):
        st.subheader('Distibution/Relational Plots')
        st.info('Below are all of the distribution/relational plots available to try and test out. Choose a few of them (if not all), you can customize the data you want to examine to see specific results or behaviors/trends')

        # if 'Histogram' button is selected
        df_selected_team.to_csv('dist_plots.csv', index=False)
        df = pd.read_csv('dist_plots.csv')


        unique_columns = ['Team','Pos','FGA (0-19yds)','FGM (0-19yds)','FGA (20-29yds)','FGM (20-29yds)','FGA (30-39yds)','FGM (30-39yds)','FGA (40-49yds)','FGM (40-49yds)','FGA (50+ yds)','FGM (50+ yds)',
                          'Total FGA','Total FGM','FG Lng','FG%','XPA','XPM','XP%','KO','KO Yds','TB','TB%','KO Avg','Punt','Punt Yds','Punt Lng','Blck','Y/P']
        statistical_columns = ['FGA (0-19yds)','FGM (0-19yds)','FGA (20-29yds)','FGM (20-29yds)','FGA (30-39yds)','FGM (30-39yds)','FGA (40-49yds)','FGM (40-49yds)','FGA (50+ yds)','FGM (50+ yds)',
                          'Total FGA','Total FGM','FG Lng','FG%','XPA','XPM','XP%','KO','KO Yds','TB','TB%','KO Avg','Punt','Punt Yds','Punt Lng','Blck','Y/P']

        # Selectable columns
        st.sidebar.info('Select two variables on the sidebar to conduct distribution/relational plot(s)')
        df_columns = st.sidebar.selectbox("Dist/Relationa Plot: Select first variable/column",unique_columns)
        df_stats = st.sidebar.selectbox("Dist/Relationa Plot: Select second variable/column", statistical_columns)

        if st.checkbox('Scatter Plot'):
            st.subheader('Scatter Plot')
            

            #Graphing Bar Plot
            with sns.axes_style("white"):
            
                f, ax = plt.subplots(figsize=(12,5))
                plt.xticks(rotation=90)
                #ax = sns.histplot(df[df_stats])
                ax = sns.scatterplot(x=df[df_columns] , y=df[df_stats])
            st.pyplot(f)

        if st.checkbox('Line Plot'):
            st.subheader('Line Plot')

            #Graphing Strip Plot
            with sns.axes_style("white"):
            
                f, ax = plt.subplots(figsize=(12,5))
                plt.xticks(rotation=90)
                #ax = sns.histplot(df[df_stats])
                ax = sns.lineplot(x=df[df_columns] , y=df[df_stats])
            st.pyplot(f)


        if st.checkbox('Histogram Plot'):
            st.subheader('Histogram Plot')

            #Graphing Box Plot
            with sns.axes_style("white"):
            
                f, ax = plt.subplots(figsize=(12,5))
                plt.xticks(rotation=90)
                #ax = sns.histplot(df[df_stats])
                ax = sns.histplot(x=df[df_columns] , y=df[df_stats])
            st.pyplot(f)


        if st.checkbox('KDE Plot'):
            st.subheader('KDE Plot')

            #Graphing Violin Plot
            with sns.axes_style("white"):
            
                f, ax = plt.subplots(figsize=(12,5))
                plt.xticks(rotation=90)
                #ax = sns.histplot(df[df_stats])
                ax = sns.kdeplot(x=df[df_columns] , y=df[df_stats])
            st.pyplot(f)


    # Regression Plots Section
    if st.sidebar.checkbox('Regression Plots'):
        st.subheader('Regression Plots')
        st.info('Below are all of the regession plots available to try and test out. Choose a few of them (if not all), you can customize the data you want to examine to see specific results or behaviors/trends')

        # if 'Histogram' button is selected
        df_selected_team.to_csv('regression_plots.csv', index=False)
        df = pd.read_csv('regression_plots.csv')


        unique_columns = ['FGA (0-19yds)','FGM (0-19yds)','FGA (20-29yds)','FGM (20-29yds)','FGA (30-39yds)','FGM (30-39yds)','FGA (40-49yds)','FGM (40-49yds)','FGA (50+ yds)','FGM (50+ yds)',
                          'Total FGA','Total FGM','FG Lng','FG%','XPA','XPM','XP%','KO','KO Yds','TB','TB%','KO Avg','Punt','Punt Yds','Punt Lng','Blck','Y/P']
        statistical_columns = ['FGA (0-19yds)','FGM (0-19yds)','FGA (20-29yds)','FGM (20-29yds)','FGA (30-39yds)','FGM (30-39yds)','FGA (40-49yds)','FGM (40-49yds)','FGA (50+ yds)','FGM (50+ yds)',
                          'Total FGA','Total FGM','FG Lng','FG%','XPA','XPM','XP%','KO','KO Yds','TB','TB%','KO Avg','Punt','Punt Yds','Punt Lng','Blck','Y/P']

        # Selectable columns
        st.sidebar.info('Select two variables on the sidebar to conduct regession plot(s)')
        df_columns = st.sidebar.selectbox("Select first variable/column to test",unique_columns)
        df_stats = st.sidebar.selectbox("Select second variable/column to test", statistical_columns)

        if st.checkbox('Regression Plot'):
            st.subheader('Regression Plot')
            

            #Graphing Bar Plot
            with sns.axes_style("white"):
            
                f, ax = plt.subplots(figsize=(12,5))
                plt.xticks(rotation=90)
                #ax = sns.histplot(df[df_stats])
                ax = sns.regplot(x=df[df_columns] , y=df[df_stats])
            st.pyplot(f)

        if st.checkbox('Residual Plot'):
            st.subheader('Residual Plot')

            #Graphing Strip Plot
            with sns.axes_style("white"):
            
                f, ax = plt.subplots(figsize=(12,5))
                plt.xticks(rotation=90)
                #ax = sns.histplot(df[df_stats])
                ax = sns.residplot(x=df[df_columns] , y=df[df_stats])
            st.pyplot(f)


