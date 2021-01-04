# Database of Villager Attributes From *Animal Crossing* Video Game
This project automatically updates a MySQL database of villager data from the video game *Animal Crossing: New Horizons*. Villager popularity data is scraped using Beautiful Soup on Animal Crossing Portal's popularity tier list. Villager attributes are obtained from a Kaggle dataset. Both sources are joined and appended to MySQL table automatically every two weeks using a CRON job via WSL on a Windows computer.

## Methods Used
* ETL
* Web Scraping
* Data Cleansing

## Technologies Used
* Python
* Linux (WSL)

## Packages Used
* Selenium
* bs4
* Pandas
* Kaggle
* sqlalchemy
* mysql-connector-python

## How To Run
On the command line of your operating system, navigate to the repository directory (ideally using a Python virtual environment).

Run the following code on the command line to install requirements:
```
pip install -r requirements.txt 
```

Run the following code on the command line to run this project:
```
Python ac_pop.py
```

# Featured Scripts or Deliverables
* [```acnh_pop.py```](acnh_pop.py)

# Other Repository Contents
* [```ACNH_tier_rank_queries.sql```](ACNH_tier_rank_queries.sql) - Example queries for villager analysis
* [```chromedriver.exe```](chromedriver.exe) - Chrome Driver used to Operate JavaScript on website before scraping 
* [```config.ini```](config.ini) -  Configurations for MySQL connection
* [```requirements.txt```](requirements.txt) - Python package requirements
* [```villagers.csv```](villagers.csv) - Kaggle dataset of *Animal Crossing* villager data

# Sources
* [Animal Crossing Portal - Popularity Tier List](https://www.animalcrossingportal.com/games/new-horizons/guides/villager-popularity-list.php#/)
* [Kaggle - Animal Crossing Data](https://www.kaggle.com/jessicali9530/animal-crossing-new-horizons-nookplaza-dataset)
* [Web Scraping Using Beautiful Soup and Selenium](https://medium.com/ymedialabs-innovation/web-scraping-using-beautiful-soup-and-selenium-for-dynamic-page-2f8ad15efe25)
* [Visual Studio Code WSL](https://code.visualstudio.com/docs/remote/wsl)
