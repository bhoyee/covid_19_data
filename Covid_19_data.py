import os
import requests
import csv
import psycopg2
import dotenv
from datetime import datetime

dotenv.load_dotenv()

# Data Extraction
def download_csv_file(url, folder_path):
    response = requests.get(url)
    if response.status_code == 200:
        csv_data = response.content.decode('utf-8')
        timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M')
        file_name = f"data_{timestamp}.csv"
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'w', newline='') as file:
            file.write(csv_data)
        print(f"Data downloaded successfully: {file_path}")
        return file_path
    else:
        print('Failed to download the CSV file.')
        return None

# Data Transformation
def transform_csv_data(csv_file):
    transformed_data = []
    with open(csv_file, 'r') as file:
        csv_reader = csv.reader(file, delimiter=',')
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            # Check that the row is not empty
            if row:
                # Check that the row contains the expected number of columns
                if len(row) == 8:
                    transformed_data.append(row)
                else:
                    print(f'Warning: row {row} does not contain the expected number of columns')
            else:
                print('Warning: empty row')
    return transformed_data

# Data Loading
def load_data_to_postgres(data, db_user, db_password, db_name, host, port):
    conn = psycopg2.connect(
        host=host,
        port=port,
        dbname=db_name,
        user=db_user,
        password=db_password
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
            recovered INT,
            PRIMARY KEY (serial_number)
        )
    ''')
    conn.commit()

    # Load the data into the COVID-19 data table
    for row in data:
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
            ON CONFLICT (serial_number) DO NOTHING
        ''', row)
    conn.commit()
    print('Data loaded successfully!')

    # Close the database connection
    cur.close()
    conn.close()

def main():
    # Create a folder for the downloaded data
    download_folder = "downloaded_data"
    os.makedirs(download_folder, exist_ok=True)

    # Download the CSV file
    url = 'https://drive.google.com/uc?id=1SzmRIwlpL5PrFuaUe_1TAcMV0HYHMD_b'
    csv_file = download_csv_file(url, download_folder)

    # Check if the CSV file was downloaded successfully
    if csv_file:
        # Create a folder for the transformed data

        transformed_folder = "transformed_data"
        os.makedirs(transformed_folder, exist_ok=True)

        # Transform the CSV data
        transformed_data = transform_csv_data(csv_file)

        # Save the transformed data to a file
        transformed_file = os.path.join(transformed_folder, f"transformed_data_{datetime.now().strftime('%Y-%m-%d-%H-%M')}.csv")
        with open(transformed_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(transformed_data)
        print(f"Transformed data saved successfully: {transformed_file}")

        # Connect to the PostgreSQL database and load the data
        db_user = os.environ.get('MY_DB_USER')
        db_password = os.environ.get('MY_DB_PASS')
        db_name = os.environ.get('MY_DB_DB')
        host = os.environ.get('MY_DB_SERVER')
        port = os.environ.get('MY_DB_SERVER_PORT')

        load_data_to_postgres(transformed_data, db_user, db_password, db_name, host, port)
    else:
        print('Failed to download the CSV file.')

# Execute the script
if __name__ == '__main__':
    main()

