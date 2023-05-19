'''
python script to download the Covid_19_data.csv file 
and load into a Postgresql database.
'''
import os
import requests
import csv
import psycopg2
import dotenv

dotenv.load_dotenv()

# Download the CSV file from the Google Drive link
url = 'https://drive.google.com/uc?id=1SzmRIwlpL5PrFuaUe_1TAcMV0HYHMD_b'
response = requests.get(url)
csv_data = response.content.decode('utf-8')

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host=os.environ['MY_DB_SERVER'],
    port=os.environ['MY_DB_SERVER_PORT'],
    dbname=os.environ['MY_DB_DB'],
    user=os.environ['MY_DB_USER'],
    password=os.environ['MY_DB_PASS'],
)
cur = conn.cursor()