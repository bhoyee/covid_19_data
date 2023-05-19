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

# Create the COVID-19 data table if it doesn't exist
cur.execute('''
    CREATE TABLE IF NOT EXISTS covid_19_data (
        serial_number INT,
        observation_date DATE,
        state VARCHAR(255),
        region VARCHAR(255),
        last_updated VARCHAR(255),
        confirmed VARCHAR(255),
        deaths INT,
        recovered INT
    )
''')
conn.commit()

# Load the data from the CSV file into the COVID-19 data table
csv_reader = csv.reader(csv_data.split('\n'), delimiter=',')
next(csv_reader)  # Skip the header row
for row in csv_reader:
    # Check that the row is not empty
    if row:
        # Check that the row contains the expected number of columns
        if len(row) == 8:
            cur.execute('''
                INSERT INTO covid_19_data (
                    serial_number,
                    observation_date,
                    state,
                    region,
                    last_updated,
                    confirmed,
                    deaths,
                    recovered
                ) VALUES (%s, TO_DATE(%s, 'MM/DD/YYYY'), %s, %s, %s, %s, %s, %s)
            ''', row)
        else:
            print(f'Warning: row {row} does not contain the expected number of columns')
    else:
        print('Warning: empty row')
conn.commit()
print('Data loaded successfully!')

# Close the database connection
cur.close()
conn.close()