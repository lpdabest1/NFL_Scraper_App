# NFL_Scraper_App
 A web based application that serves as providing quick access to NFL Player Statistics across various categories (including Fantasy Football). The data collected for this app was done through web scraping of Pro Football reference (\https://www.pro-football-reference.com/). I used the basic template provided by a yputuber I found known as Data Professor. You can find the coded template at git hub repo link: https://github.com/dataprofessor/code/tree/master/streamlit/part9

The Statistical Categories I data scraped for are passing, rushing, receiving, defense, kicking, returning, scoring, and fantasy.
Each of these separate pages were scraped and have been reformatted to include necessary and distinguishable data representing the player under such category. Furthermore, Each Page has it's own table. In addition, depending on what the user is wanting, they can filter the data based on year, and position. The user can also download the desired filtered data as a csv file, so they can carryout more data analytics on the data collected. Lastly, the user can view a Intercorrelation Heatmap of the filtered data. 

In the future, I will probably add another statistical section that is separate from players (team data). I would like to have the season averages alongside the selected year that is selected by the user when viewing the team data for that season. 
I am also just in the beginning stages of adding more independent analytical testing on the data, so keep an eye out for more in the future!
