import mysql.connector
from mysql.connector import Error
import sqlalchemy
from mongodb import *
from cleaning import *
import pandas as pd

def check_if_valid_data(df: pd.DataFrame) -> bool:
    # check if dataframe is empty
    boolean = True
    if df.empty:
        print('No file downloaded. Finishing execution')
        boolean = False
    else:
        #Unique check
        if pd.Series(df['product_name']).is_unique:
            boolean = True
        else:
            boolean = False
            raise Exception('Unique check is violated')
            

        #Check missing value
        if df.isnull().values.any():
            boolean = False
            raise Exception("Null values found")
    return boolean
            

# Retrieve data
shopee = retrieve_shopee()
tokopedia = retrieve_tokopedia()

# transform data to dataframe
df_shopee = pd.DataFrame.from_dict(shopee,orient='index')
df_tokopedia = pd.DataFrame.from_dict(tokopedia,orient='index')

#delete duplicate data
df_shopee_cleaned = shopee_cleaning(df_shopee)
df_tokopedia_cleaned = tokped_cleaning(df_tokopedia)

if check_if_valid_data(df_shopee_cleaned):
    print("Data shopee valid")
if check_if_valid_data(df_tokopedia_cleaned):
    print("Data tokopedia valid")

df_shopee_cleaned['ecommerce_name'] = 'shopee'
df_tokopedia_cleaned['ecommerce_name'] = 'tokopedia' 
df_ecommerce = pd.concat([df_shopee_cleaned.sample(n=100, random_state=1234).reset_index(drop=True),df_tokopedia_cleaned.sample(n=100, random_state=1234).reset_index(drop=True)],axis=0,ignore_index=False).rename(columns={'_id':'id'})


try:
    connection = mysql.connector.connect(host='127.0.0.1',
                                         database='ecommerce',
                                         user='root',
                                         password='password')
    engine = sqlalchemy.create_engine("mysql://root:password@127.0.0.1/ecommerce")
    if connection.is_connected():
        cursor = connection.cursor()
        query_table = """
        CREATE TABLE IF NOT EXISTS vans_products(
            id VARCHAR(255) NOT NULL,
            product_name VARCHAR(255),
            shop_name VARCHAR(100),
            location VARCHAR(100),
            price INT,
            discount INT(3),
            amount_sold INT,
            rating DECIMAL,
            no_of_rating INT,
            link_product TEXT,
            category VARCHAR(100),
            ecommerce_name VARCHAR(50),
            CONSTRAINT primary_key_constraint PRIMARY KEY (id)
        )
        """
        try:
            cursor.execute("USE ecommerce")
            cursor.execute(query_table)
            print("table vans_product successfully opened ")
        except Error as e:
            print("Error while opening table", e)

        try:
            df_ecommerce.to_sql("vans_products",engine,index=False, if_exists='append')
            print("insert data successfuly")
        except:
            print('Data already exists in the database')

except Error as e:
    print("Error while connecting to MySQL", e)

