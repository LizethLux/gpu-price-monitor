import os # reads api key
import requests # comunicate with the api prices api
from dotenv import load_dotenv # loads the api key from the .env file
import pandas as pd #organize the data into a table
from datetime import datetime #get the current date and time

#load the api key from the .env file
load_dotenv()

#retrieve the api key without showing it
api_key = os.getenv("prices_api_key")

#check that the api exists
if not api_key:
    raise ValueError("API Key is not found. Check .env files")

#pricesAPI endpoint.
url = "https://api.pricesapi.io/api/v1/products/search"


#send our API key securely in the request header.
headers = {
    "Authorization": f"Bearer {api_key}"  #tells the api who i am. (my api key)
}


#read the catalog
gpu_catalog = pd.read_csv("gpu_catalog.csv")



#search for one GPU in the US market.
#params = {
    #"q": "NVIDIA GeForce RTX 5090",
   # "market": "us",
   # "limit": 3
#}

#we need to know WHEN the prices were collected
#comparing prices over time is how we can see if the price is going up or down

collection_time = datetime.now().astimezone().isoformat(timespec="seconds") 

#datetime gives tool for working with dates and times
# now() gets current time and date
# astimezone() includes local timezone
#isoformat() formats the date and time into a stanardized string format
#ex: 2023-03-15T14:30:00-07:00
#now every price record can have a timestamp


#create a list to store the gpu prices
price_records = []  

#search for each gpu in the uis market
for index, gpu in gpu_catalog.iterrows():

   manufacturer = gpu["manufacturer"]
   model = gpu["model"]

   #combine manufacturer and model for the search

   search_query = f"{manufacturer} {model}"

   params = {
      "q": search_query,
      "market": "us",
      "limit": 3
   }

   #send the request to PricesAPI.
   response = requests.get(  # tells python to send a get request
      url,  # tell python WHERE to send the request. to the pricesapi address
      params=params,  # tells api WHAT info i want.
      headers=headers,  # tells api WHO i am. (my api key)
      timeout=95  # tells python to not wait for more than 95 seconds for a response from the api
   )

   # check whether the request succeeded.
   response.raise_for_status()  # raises an error if the request failed
   
   #convert the response into Python data.
   data = response.json() # converts the JSON response into a Python dictionary
   
   #get the gpu products from the api repsonse
   products = data["data"]["products"]

   
   
   #go through each product and extract the relevant information
   for product in products:
     for offer in product.get("offers", []):  # get the offers for the product, default to empty list if not found
        # Store the useful information in one record.
        price_records.append({ #add something to the end of the list
           "collection_date": collection_time,
           "gpu_model": search_query,
           "seller": offer.get("seller"),
           "price": offer.get("price"),
           "currency": offer.get("currency"),
           "condition": product.get("condition_label"),
           "stock_status": offer.get("stock_status"),
           "product_title": offer.get("product_title"),
           "product_url": offer.get("url")
           })


#convert the record into a pandas tabel
gpu_prices = pd.DataFrame(price_records)

#screening limits
#check if the price is valid (greater than 0)
#gpu_prices["valid_price"] = gpu_prices["price"].between(500,6000)
#print(gpu_prices[["gpu_model", "seller", "price", "valid_price"]])


#instead classify the prices

#checking if the price is valid (greater than 0)
gpu_prices["valid_price"] = gpu_prices["price"] > 0

#classify the prices into ranges
gpu_prices["price_category"] = "Normal Range"

#below normal range
gpu_prices.loc[gpu_prices["price"] < 500, "price_category"] = "Below Normal Range"

#above normal range
gpu_prices.loc[gpu_prices["price"] > 6000, "price_category"] = "Above Normal Range"

# outlier range
gpu_prices.loc[gpu_prices["price"] > 15000, "price_category"] = "Extreme Outlier"

#identify out of stock items
gpu_prices["out_of_stock"] = ( gpu_prices["stock_status"].str.lower() == "out of stock" )


#save the gpu prices as a csv file
#gpu_prices.to_csv("gpu_prices.csv",index=False)
#print("\nGPU prices were saved")

#replace ^
gpu_prices.to_csv("gpu_prices.csv", mode="a",header=not os.path.exists("gpu_prices.csv"), index=False)
print("\nGPU prices were saved to gpu_prices.csv")
#MODE="a" means append, so new records will be added to the bottom of the file instead of overwriting it.
#header=not.os.path.exists (..) writes column name only when the file is created for the first time. If the file already exists, it will not write the column names again.
#indes=False prevents pandas from adding an uneccessary row-number column to the csv file.
#os is  python moule that interacts with my windows system, it checks if the csv file already exists ion my project folder, if it does exists it retuns true, if it does not exist it returns false. The not inverts the value, so if the file exists it will return false, and if it does not exist it will return true.




