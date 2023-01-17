# DataAnalysis_and_PowerBi_DashBoard || Data wrangling / Data Analysis:
- In this repo i have used:
  - Exploratory Data analysis (EDA): For understanding the data, i performed some EDA.
  - Data Wrangling: For organizing the differentes segments in each column, for further analysis i have to do some wrangling
  - Data Cleansing: For cleaning and excluding outliers (not needed in this case) i used some techniques as IQR(inter quartile range), so i could work on a more realiable data, also doing some distributions, for further understanding of the data i was dealing with at each moment of the process.
  - DashBoards: Creating an interactive Power Bi dashboard with the data generated as a final product.
- Tools Used:
  - Laguage: Python
  - Libs: Pandas, matplotlib, seaborn and scipy
  - Dependencies managing: Poetry
  - Metrics and Dashboard: Power Bi

The Proyect was generated with the intention of showing some statistics about properties in Capital Federal, Buenos Aires, Argentina. The data was gathered by a scrapper that i developed (that helped me to move to an apartment below the average price for that time)

- Conclusion: As a result of all the analysis, we can observe that there is a big correlation between the price of the properties, and the squared meters. At higher squared meters, higher is the price. 
  Meanwhile we can also observed, that there are neighborhoods, that have higher prices. With the dashboard we could easily find the cheapest neighborhoods, and get advantage of that. Knowing that maybe paying a 1 room property in "Las Cañitas" would be the equivalent, to the rent of 2 or 3 rooms properties in "Constitución" or "Boca".
  In the Second page "Serie temporal" (Time series), there is not enough information maybe to show the fluctuation of prices (in Argentina the inflation is right now around 90% yearly), but we can observe some trend for prices, that are higher while days pass by.

[ Link to Power Bi Dashboard](https://app.powerbi.com/view?r=eyJrIjoiOTI5NDI1ZjItMGVjZi00OGU3LTk3ZGUtNTgwMThlNzkzYmU2IiwidCI6ImRmODY3OWNkLWE4MGUtNDVkOC05OWFjLWM4M2VkN2ZmOTVhMCJ9&pageName=ReportSection)
![image](https://user-images.githubusercontent.com/75091406/212995853-0a52fa00-c4e2-4267-801f-55808ea24229.png)
![image](https://user-images.githubusercontent.com/75091406/212995906-efc4228a-5b77-4ac1-9611-6032fcaf6ffa.png)

