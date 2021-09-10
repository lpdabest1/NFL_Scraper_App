from pandas.core.indexes.base import Index
from seaborn.matrix import _index_to_label
import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import matplotlib_inline as ln
import seaborn as sns
import numpy as np



def app():
    st.title('NFL Football Stats (Passing) Explorer')

    st.markdown("""
This app performs simple webscraping of NFL Football player stats data (focusing on Passing)!
* **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, seaborn
* **Data source:** [pro-football-reference.com](https://www.pro-football-reference.com/).
Data is from 2006 to 2020.
""")

    st.sidebar.header('User Customization')
    selected_year = st.sidebar.selectbox('Year', list(reversed(range(2006,2021))))

# Web scraping of NFL player stats
# https://www.pro-football-reference.com/years/2019/passing.htm
    @st.cache
    def load_data(year):
        url = "https://www.pro-football-reference.com/years/" + str(year) + "/passing.htm"
        html = pd.read_html(url, header = 0)
        df = html[0]
        raw = df.drop(df[df.Rk == 'Rk'].index) # Deletes repeating headers in content
        raw = raw.fillna(0)
        playerstats = raw.drop(['Rk', 'QBrec','Y/C','QBR','4QC','GWD'], axis=1)

           # converting columns data types
            # unique columns (categorical columns)
                # Converting Columns Data Type to int Type
        playerstats = playerstats.astype({'Cmp':'int',
                                          'Att':'int',
                                          'Cmp%':'str',
                                          'Yds':'int',
                                          'TD':'int',
                                          'TD%':'str',
                                          'Int':'int',
                                          'Int%':'str',
                                          '1D':'int',
                                          'Lng':'int',
                                          'Y/A':'str',
                                          'AY/A':'str',
                                          'Y/G':'str',
                                          'Rate':'str',
                                          'Sk':'int',
                                          'Yds.1':'int',
                                          'NY/A':'str',
                                          'ANY/A':'str',
                                          'Sk%':'str'
                                                                               
                                            })


        # Renaming/Reformatting Certain Columns under incorrect naming
        playerstats.rename(columns={'Yds.1': 'Sack Yds',
                                    'Tm': 'Team'}, inplace= True)
        return playerstats
    playerstats = load_data(selected_year)

# Sidebar - Team selection
    sorted_unique_team = sorted(playerstats.Team.unique())
    selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

# Sidebar - Position selection
    unique_pos = ['RB','QB','WR','FB','TE']
    selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

# Sidebar - Player selection
#sorted_unique_player = sorted(playerstats.Player.unique())
#selected_player = st.sidebar.multiselect('Player', sorted_unique_player, sorted_unique_player) 


# Filtering data
# Team And Position
    df_selected_team = playerstats[(playerstats.Team.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]

# Player
#df_selected_player = playerstats[(playerstats.Player.isin(selected_player)) & (playerstats.Pos.isin(selected_pos))]

# Team Data
    if st.button('Passing Statistics'):
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


        unique_columns = ['Player','Team','Pos','Cmp','Att','Cmp%','Yds','TD','TD%','Int','Int%','1D','Lng','Y/A','AY/A','Y/G','Rate','Sk','Sack Yds','NY/A','ANY/A','Sk%']
        statistical_columns = ['Cmp','Att','Cmp%','Yds','TD','TD%','Int','Int%','1D','Lng','Y/A','AY/A','Y/G','Rate','Sk','Sack Yds','NY/A','ANY/A','Sk%']

        # Selectable columns
        st.sidebar.info('Select two variables on the sidebar to conduct categorical plot(s)')
        df_columns = st.sidebar.selectbox("Select first variable/column",unique_columns)
        df_stats = st.sidebar.selectbox("Select second variable/column", statistical_columns)

        # Sort Values for X axis
        

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


        unique_columns = ['Player','Team','Pos','Cmp','Att','Cmp%','Yds','TD','TD%','Int','Int%','1D','Lng','Y/A','AY/A','Y/G','Rate','Sk','Sack Yds','NY/A','ANY/A','Sk%']
        statistical_columns = ['Cmp','Att','Cmp%','Yds','TD','TD%','Int','Int%','1D','Lng','Y/A','AY/A','Y/G','Rate','Sk','Sack Yds','NY/A','ANY/A','Sk%']

        # Selectable columns
        st.sidebar.info('Select two variables on the sidebar to conduct distribution/relational plot(s)')
        df_columns = st.sidebar.selectbox("Dist/Relationa Plot: Select first variable/column",unique_columns)
        df_stats = st.sidebar.selectbox("Dist/Relationa Plot: Select second variable/column", statistical_columns)

        if st.checkbox('Scatter Plot'):
            st.subheader('Scatter Plot')
            

            #Graphing Scatter Plot
            with sns.axes_style("white"):
            
                f, ax = plt.subplots(figsize=(12,5))
                plt.xticks(rotation=90)
                #ax = sns.histplot(df[df_stats])
                ax = sns.scatterplot(x=df[df_columns] , y=df[df_stats])
            st.pyplot(f)

            



        if st.checkbox('Line Plot'):
            st.subheader('Line Plot')

            #Graphing Line Plot
            with sns.axes_style("white"):
            
                f, ax = plt.subplots(figsize=(12,5))
                plt.xticks(rotation=90)
                #ax = sns.histplot(df[df_stats])
                ax = sns.lineplot(x=df[df_columns] , y=df[df_stats])
            st.pyplot(f)





        if st.checkbox('Histogram Plot'):
            st.subheader('Histogram Plot')

            #Graphing Hist Plot
            with sns.axes_style("white"):
            
                f, ax = plt.subplots(figsize=(12,5))
                plt.xticks(rotation=90)
                #ax = sns.histplot(df[df_stats])
                ax = sns.histplot(x=df[df_columns] , y=df[df_stats], cbar=True, cbar_kws=dict(shrink=.75)) #change this back to histplot
            st.pyplot(f)


        if st.checkbox('KDE Plot'):
            st.subheader('KDE Plot')

            #Graphing KDE Plot
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


        unique_columns = ['Cmp','Att','Cmp%','Yds','TD','TD%','Int','Int%','1D','Lng','Y/A','AY/A','Y/G','Rate','Sk','Sack Yds','NY/A','ANY/A','Sk%']
        statistical_columns = ['Cmp','Att','Cmp%','Yds','TD','TD%','Int','Int%','1D','Lng','Y/A','AY/A','Y/G','Rate','Sk','Sack Yds','NY/A','ANY/A','Sk%']

        # Selectable columns
        st.sidebar.info('Select two variables on the sidebar to conduct regession plot(s)')
        df_columns = st.sidebar.selectbox("Select first variable/column to test",unique_columns)
        df_stats = st.sidebar.selectbox("Select second variable/column to test", statistical_columns)

        if st.checkbox('Regression Plot'):
            st.subheader('Regression Plot')
            

            #Graphing Reg Plot
            with sns.axes_style("white"):
            
                f, ax = plt.subplots(figsize=(12,5))
                plt.xticks(rotation=90)
                
                ax = sns.regplot(x=df[df_columns] , y=df[df_stats])
            st.pyplot(f)

        if st.checkbox('Residual Plot'):
            st.subheader('Residual Plot')

            #Graphing Residual Plot
            with sns.axes_style("white"):
            
                f, ax = plt.subplots(figsize=(12,5))
                plt.xticks(rotation=90)
                ax = sns.residplot(x=df[df_columns] , y=df[df_stats])
            st.pyplot(f)
