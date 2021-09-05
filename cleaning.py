import pandas as pd
import re

FILE_VANS_TYPE = open("vans_type.txt","r")
vans_type = FILE_VANS_TYPE.read().split(',')

# SHOPEE
def shopee_cleaning(dataframe):
    def handling_na(df):
        try:
            #drop row for shop_name
            cleaned1 = df.dropna(axis=0,subset=['shop_name'])
            #'' for discount
            cleaned = cleaned1.copy()
            cleaned[['discount']] = cleaned1[['discount']].fillna('0',axis=1)
            return cleaned
        except:
            print("Failed to handling nan value")

    def clean_product_name(names):
        try:
            list_name=[]
            for n in names:
                string_encode = n.encode("ascii", "ignore")
                string_decode = string_encode.decode()
                list_name.append(string_decode.strip())
            return list_name
        except:
            print("Failed to extract product names")

    def extract_city(locs):
        try:
            location = []
            for loc in locs:
                head, sep, tail = loc.partition('-')
                city = re.sub(r'kab. ','Kabupaten ',head.strip().lower())
                city = re.sub(r'kota ','',city)
                location.append(city.title())
            return location
        except:
            print("Failed to extract cities")

    def clean_price(prices):
        try:
            price_list = []
            for p in prices:
                if '-' in p: 
                    head, sep, tail = p.partition('-')
                    p = head.strip()
                price = re.sub(r'[Rp]','',re.sub(r'[].[]','',p))
                price_list.append(price)
            return price_list
        except:
            print("Failed to clean product price")

    def clean_discount(numbers):
        try:
            dc_list = []
            for p in numbers:
                dc_list.append(re.sub(r'[^0-9]+','',p))
            return dc_list
        except:
            print("failed to clean discount")

    def clean_amount(amounts):
        try:
            as_list=[]
            for asd in amounts:
                plus = re.sub(r'[^a-zA-Z0-9]','',asd)
                head, sep, tail = plus.partition(',')
                n_tail =  len(tail)-2 if len(tail)-2 >0 else 0
                as_list.append(re.sub(r'[RB]+','0'*(3-n_tail),re.sub(r'[],[]','',plus)))
            return as_list
        except:
            print("Failed to clean amount")


    def get_category(products):
        try:
            category = []
            for product in products:
                cat = ''
                for vtype in vans_type:
                    product0 = re.sub(r'[^a-zA-Z0-9 ]+',' ',product)
                    vtype0 = re.sub(r'[^a-zA-Z0-9 ]+',' ',vtype)
                    #print(product0+'---'+vtype0)
                    if vtype0.lower() in product0.lower():
                        if vtype == 'OldSkool':
                            cat = 'Old Skool'
                        else:
                            cat =vtype
                category.append(cat)
            return category
        except:
            print("Failed to create category")
    
    
    #json to dataframe
    
    # delete duplicate data
    dataframe.drop_duplicates(subset=['product_name'],keep=False, inplace = True)
    #Handling missing value
    cleaned = handling_na(dataframe)
    #extract city names
    cleaned['location'] = extract_city(cleaned.location)
    #clean product price
    cleaned['price'] = clean_price(cleaned.price)
    #clean product discount
    cleaned['discount'] = clean_discount(cleaned.discount)
    #clean number of rating
    cleaned['no_of_rating'] = clean_amount(cleaned.no_of_rating)
    #clean number of sold
    cleaned['amount_sold'] = clean_amount(cleaned.amount_sold)
    #create category
    cleaned['category'] = get_category(cleaned.product_name)
    #clean product_name
    cleaned['product_name'] = clean_product_name(cleaned.product_name)
    # transform data type
    td_shopee = cleaned.astype({'price':'int','discount':'int','amount_sold':'int','rating':'float','no_of_rating':int})
    return td_shopee


# TOKOPEDIA
def tokped_cleaning(dataframe):
    def handling_na(df):
        try:
            #'' for discount
            cleaned = df.copy()
            cleaned[['discount']] = df[['discount']].fillna('0',axis=1)
            return cleaned
        except:
            print("Failed to handling nan value")

    def clean_product_name(names):
        try:
            list_name=[]
            for n in names:
                string_encode = n.encode("ascii", "ignore")
                string_decode = string_encode.decode()
                list_name.append(string_decode.strip())
            return list_name

        except:
            print("Failed to extract product names")

    def clean_location(locs):
        location_list = []
        for loc in locs:
            city = re.sub(r'kab. ','Kabupaten ',loc.lower())
            city = re.sub(r'kota ','',city)
            location_list.append(city.title())
        return location_list

    def clean_number(numbers):
        try:
            price_list = []
            for p in numbers:
                price_list.append(re.sub(r'[^0-9]+','',p))
            return price_list
        except:
            print("failed to clean price")

    def get_category(products):
        try:
            category = []
            for product in products:
                cat = ''
                for vtype in vans_type:
                    product0 = re.sub(r'[^a-zA-Z0-9 ]+',' ',product)
                    vtype0 = re.sub(r'[^a-zA-Z0-9 ]+',' ',vtype)
        #             print(product0+'---'+vtype0)
                    if vtype0.lower() in product0.lower():
                        if vtype == 'OldSkool':
                            cat = 'Old Skool'
                        else:
                            cat =vtype
                category.append(cat)
            return category
        except:
            print("Failed to create category")

    # json to dataframe

    # delete duplicate data
    dataframe.drop_duplicates(subset=['product_name'],keep=False, inplace = True)
    #handling missing values
    cleaned = handling_na(dataframe)
    #clean location
    cleaned['location'] = clean_location(cleaned.location)
    #clean price
    cleaned['price'] = clean_number(cleaned.price)
    #clean discount
    cleaned['discount'] = clean_number(cleaned.discount)
    #clean amount_sold
    cleaned['amount_sold'] = clean_number(cleaned.amount_sold)
    #clean no_of_rating
    cleaned['no_of_rating'] = clean_number(cleaned.no_of_rating)
    #get product category
    cleaned['category'] = get_category(cleaned.product_name)
    #clean product name
    cleaned['product_name'] = clean_product_name(cleaned.product_name)
    

    # transform data type
    td_tokped = cleaned.astype({'price':'int','discount':'int','amount_sold':'int','rating':'float','no_of_rating':int})
    return td_tokped

