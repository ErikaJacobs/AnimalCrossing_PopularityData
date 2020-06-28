
#%%

from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome("C://Users/cluel/Documents/GitHub/Animal-Crossing-Popularity-Data/chromedriver.exe", chrome_options=options)

import time

url = 'https://www.animalcrossingportal.com/games/new-horizons/guides/villager-popularity-list.php'
driver.get(url)
classes = driver.find_elements_by_class_name("c-villager-name")

for x in range(len(classes)):
    if classes[x].is_displayed():
        driver.execute_script("arguments[0].click();", classes[x])
        time.sleep(2)
        
page_source = driver.page_source
#%%

from bs4 import BeautifulSoup

soup = BeautifulSoup(page_source, 'lxml')
villagers = []

#%%
tier_data = soup.find_all(class_="c-tier")
tier_list = list(tier_data)

villager_tier = []
villager_name = []
villager_rank = []
villager_message = []
villager_value = []

for i in tier_list:
    index = tier_list.index(i)
    tier = list(tier_list[index].find(class_="u-grow u-flex").find('p'))
    value = list(tier_list[index].find(class_="u-margin-left c-badge c-badge--gray"))
    villager_data = list(tier_list[index].find_all(class_="c-villager"))
    
    for i in villager_data:
        soup = villager_data[villager_data.index(i)]
        
        # Get Data
        villager_tier.append(tier[0])
        villager_value.append(value[0])
        villager_name.append(soup.find(class_="c-villager-name").get_text())
        villager_rank.append(soup.find(class_="c-villager-rank").get_text())
        
        # Reset Soup at End
        if villager_data[-1] == i:
            soup = BeautifulSoup(page_source, 'lxml')
#%%

# Create Pandas Dataframe
            
import pandas as pd

df = pd.DataFrame({
    'villager_name': villager_name,
    'villager_tier_rank': villager_rank,
    'villager_tier': villager_tier,
    'villager_value': villager_value})

# Clean Up

tier_dict = {'TIER 1': 1, 
             'TIER 2': 2, 
             'TIER 3': 3, 
             'TIER 4': 4, 
             'TIER 5': 5, 
             'TIER 6': 6}

df['villager_tier_num'] = df['villager_tier'].apply(lambda x: tier_dict[x])

df.sort_values(by=['villager_tier_num', 'villager_tier_rank'])

df['villager_rank'] = df.index+1

df.head(10)
            
 #%%
            
# Get Table from Kaggle

import kaggle
import os
import zipfile
import pandas as pd

# Download From Kaggle
kaggle.api.authenticate()
kaggle.api.dataset_download_files('jessicali9530/animal-crossing-new-horizons-nookplaza-dataset', path='C:/Users/cluel/Downloads')

# Unzip Download

path_before = 'C:/Users/cluel/Downloads/animal-crossing-new-horizons-nookplaza-dataset.zip'
path_after = 'C:/Users/cluel/Downloads/animal-crossing-new-horizons-nookplaza-dataset'

with zipfile.ZipFile(path_before, 'r') as zip_ref:
    zip_ref.extractall(path_after)

# Move villagers.csv to project directory
csv_before = 'C:/Users/cluel/Downloads/animal-crossing-new-horizons-nookplaza-dataset/villagers.csv'
csv_after = 'C:/Users/cluel/Documents/GitHub/Animal-Crossing-Popularity-Data/villagers.csv'

os.rename(csv_before, csv_after)

# Import Kaggle Data to Python

df_kag = pd.read_csv(csv_after)

#%%

# Join Kaggle and Popularity together

df_final = pd.merge(df, df_kag, how='left', left_on=['villager_name'], right_on=['Name'])
                  
# Connect to MySQL
            

# Upload Both Tables, Join together
        
        

# https://medium.com/ymedialabs-innovation/web-scraping-using-beautiful-soup-and-selenium-for-dynamic-page-2f8ad15efe25