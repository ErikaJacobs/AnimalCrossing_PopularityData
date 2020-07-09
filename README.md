# Database of Villager Attributesfrom video game *Animal Crossing*
This project automatically updates a MySQL database of villager data from the video game *Animal Crossing: New Horizons*. Villager popularity data is scraped using Beautiful Soup on Animal Crossing Portal's Popularity Tier List. Villager attributes are obtained from a Kaggle dataset. Both sources are joined and appended to MySQL table automatically every two weeks using Airflow via WSL on a Windows computer.

## Methods Used
* ETL
* Web Scraping
* Data Cleansing

## Technologies Used
* Python
* Airflow
* Linux (WSL)

## Packages Used
* Airflow
* Selenium
* bs4
* Pandas
* Kaggle
* sqlalchemy
* mysql-connector-python

# Featured Notebooks, Scripts, Analysis, or Deliverables
* [```acnh_dag.py```](https://github.com/ErikaJacobs/Animal-Crossing-Popularity-Data/blob/master/acnh_dag.py) - 
* [```acnh_pop.py```](https://github.com/ErikaJacobs/Animal-Crossing-Popularity-Data/blob/master/acnh_pop.py) - 

# Other Repository Contents
* [```chromedriver.exe```](https://github.com/ErikaJacobs/Animal-Crossing-Popularity-Data/blob/master/chromedriver.exe) - 
* [```villagers.csv```](https://github.com/ErikaJacobs/Animal-Crossing-Popularity-Data/blob/master/villagers.csv) - 

# Sources
* [Animal Crossing Villager Popularity Tier List](https://www.animalcrossingportal.com/games/new-horizons/guides/villager-popularity-list.php#/)
