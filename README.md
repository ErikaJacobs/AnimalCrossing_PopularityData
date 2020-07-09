# Database of Villager Attributes From *Animal Crossing* Video Game
This project automatically updates a MySQL database of villager data from the video game *Animal Crossing: New Horizons*. Villager popularity data is scraped using Beautiful Soup on Animal Crossing Portal's popularity tier list. Villager attributes are obtained from a Kaggle dataset. Both sources are joined and appended to MySQL table automatically every two weeks using Airflow via WSL on a Windows computer.

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
* [```acnh_pop.py```](https://github.com/ErikaJacobs/Animal-Crossing-Popularity-Data/blob/master/acnh_pop.py)

# Other Repository Contents
* [```acnh_dag.py```](https://github.com/ErikaJacobs/Animal-Crossing-Popularity-Data/blob/master/acnh_dag.py) - Airflow DAG that processes acnh_pop.py functions every two weeks
* [```chromedriver.exe```](https://github.com/ErikaJacobs/Animal-Crossing-Popularity-Data/blob/master/chromedriver.exe) - Chrome Driver used to Operate JavaScript on website before scraping 
* [```villagers.csv```](https://github.com/ErikaJacobs/Animal-Crossing-Popularity-Data/blob/master/villagers.csv) - Kaggle dataset of *Animal Crossing* villager data

# Sources
* [Animal Crossing Portal - Popularity Tier List](https://www.animalcrossingportal.com/games/new-horizons/guides/villager-popularity-list.php#/)
* [Kaggle - Animal Crossing Data](https://www.kaggle.com/jessicali9530/animal-crossing-new-horizons-nookplaza-dataset)
* [Web Scraping Using Beautiful Soup and Selenium](https://medium.com/ymedialabs-innovation/web-scraping-using-beautiful-soup-and-selenium-for-dynamic-page-2f8ad15efe25)
* [Installing Apache Airflow - Windows](https://medium.com/@ryanroline/installing-apache-airflow-on-windows-10-5247aa1249ef)
* [Visual Studio Code WSL](https://code.visualstudio.com/docs/remote/wsl)
