from selenium import webdriver        
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import kaggle
import os
import zipfile
import glob
import time
from datetime import datetime as dt
from sqlalchemy import create_engine
from shutil import copyfile, rmtree
import configparser

class AC_Pop:
    
    def __init__(self, *args, **kwargs):
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.configs = {}
        Config = configparser.ConfigParser()
        Config.read(self.path+"/config.ini")
        config_list = Config.options('MySQL')
    
        for config in config_list:
            self.configs[config] = Config.get('MySQL', config)

    def create_df(self, *args, **kwargs):
        path = self.path
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(executable_path = rf'{path}{"/chromedriver.exe"}', options=options)

        url = 'https://www.animalcrossingportal.com/games/new-horizons/guides/villager-popularity-list.php'
        driver.get(url)
        classes = driver.find_elements_by_class_name("c-villager-name")

        for x in range(len(classes)):
            if classes[x].is_displayed():
                driver.execute_script("arguments[0].click();", classes[x])
                time.sleep(2)
                
        page_source = driver.page_source

        soup = BeautifulSoup(page_source, 'lxml')

        tier_data = soup.find_all(class_="c-tier")
        tier_list = list(tier_data)

        villager_tier = []
        villager_name = []
        villager_rank = []
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
            
        villager_field_dict = {
        'villager_name': villager_name,
        'villager_tier_rank': villager_rank,
        'villager_tier': villager_tier,
        'villager_value': villager_value}
        
        # Create df
        self.df = pd.DataFrame(villager_field_dict)
        df = self.df

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
        df['Date_Pulled'] = datetime.date.today()

        # Name Changes for Join
        def name_change(x):
            
            name_dict = {
            'Renee': 'Renée',
            'OHare': "O'Hare",
            'Buck(Brows)': 'Buck',
            'WartJr': 'Wart Jr.',
            'Crackle(Spork)': 'Spork'}
            
            if x in list(name_dict.keys()):
                name = name_dict[x]
            else:
                name = x
            return name

        df['villager_name'] = df['villager_name'].apply(lambda x: name_change(x))
        
    def kaggle_data(self, *args, **kwargs):
        
        path = self.path
        
        # Check Directory for villagers.csv
        acdir = glob.glob(path + '/*')
        
        file_check = any('villagers.csv' in file for file in acdir)

        
        if file_check == False:
            # Kaggle Setup
            kaggle.api.authenticate()
            kaggle.api.dataset_download_files('jessicali9530/animal-crossing-new-horizons-nookplaza-dataset', path = path)
        
            # Unzip Download
            path_before = path + '/animal-crossing-new-horizons-nookplaza-dataset.zip'
            path_after = path + '/animal-crossing-new-horizons-nookplaza-dataset'
        
            with zipfile.ZipFile(path_before, 'r') as zip_ref:
                zip_ref.extractall(path_after)
        
            # Copy Villager File to Root
            copyfile(path_after + '/villagers.csv', path + '/villagers.csv')# Move villagers.csv to project directory
            
            # Remove Other Downloaded Files
            os.remove(path_before)
            rmtree(path_after)
        
    def join_tables(self, *args, **kwargs):

            path = self.path
            
            # Import Dataframes to Python and Merge
            self.df_kag = pd.read_csv(path + '/villagers.csv')
            self.df_final = pd.merge(self.df, self.df_kag, how='left', left_on=['villager_name'], right_on=['Name'])
            df_final = self.df_final
            
            # Clean Birthday field
         
            def birthday_clean(x):
                x = str(x)
                try:
                    bdate = dt.strptime(x, '%d-%b')
                    bdate = bdate.replace(year = 2020)
                    bdate = bdate.date()
                except:
                    bdate = 'N/A'
                
                return bdate
         
            df_final['Birthday'] = df_final['Birthday'].apply(lambda x: birthday_clean(x))
         
            # Clean Column Names - No Spaces
         
            for column in list(df_final.columns):
                old = column
                new = column.replace(' ', '_')
                
                if old == new:
                    continue
                else:
                   df_final.rename(columns={old:new}, inplace=True)
            

    def send_mysql(self, *args, **kwargs):
        # Import Dataframe and Configs
        df_final = self.df_final
        configs = self.configs
        
        # Set-Up Query for Create Table (If Not Exists)
        column_attributes = {
            'villager_name': 'varchar(50)',
            'villager_tier_rank': 'int',
            'villager_tier': 'varchar(50)',
            'villager_value': 'varchar(50)',
            'villager_tier_num': 'int',
            'villager_rank': 'int',
            'Date_Pulled': 'date',
            'Name': 'varchar(50)',
            'Species': 'varchar(50)',
            'Gender': 'varchar(50)',
            'Personality': 'varchar(50)',
            'Hobby': 'varchar(50)',
            'Birthday': 'date',
            'Catchphrase': 'varchar(50)',
            'Favorite_Song': 'varchar(50)',
            'Style_1': 'varchar(50)',
            'Style_2': 'varchar(50)',
            'Color_1': 'varchar(50)',
            'Color_2': 'varchar(50)',
            'Wallpaper':'varchar(50)',
            'Flooring':'varchar(50)',
            'Furniture_List': 'varchar(200)',
            'Filename': 'varchar(50)',
            'Unique_Entry_ID':'varchar(50)'
            }

        statement_details = []

        for column in list(df_final.columns):

            string = f'{column} {column_attributes[column]}'
            statement_details.append(string)
            
        statement = ', '.join(statement_details)

        create_query = f"""CREATE TABLE IF NOT EXISTS acnh_villagers ({statement})"""

        # Connect to SQL

        #conn = create_engine('mysql+mysqlconnector://root:password@127.0.0.1:3306/erika_python', echo=False)
        
        engine = create_engine(f"""mysql://{configs['user']}:{configs['password']}@localhost/{configs['database']}?autocommit=true""")
 
        cur = engine.connect()

        # Create Table (If Not Exists)
        cur.execute(create_query)

        # Remove Potential Duplicates
        cur.execute(f"""DELETE FROM acnh_villagers where Date_Pulled = '{datetime.date.today()}';""")

        # Send df to MySQL
        df_final.to_sql(name='acnh_villagers', con = engine, if_exists = 'append', index=False)

        # Close connection
        cur.close()
        
#%%

# Procedure
print(f'Villager data collection started at {datetime.datetime.now()}')
ac = AC_Pop()
ac.create_df()
ac.kaggle_data()
ac.join_tables()
ac.send_mysql()
print(f'Villager data collection completed at {datetime.datetime.now()}')
