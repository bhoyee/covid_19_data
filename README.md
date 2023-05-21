# COVID-19 Data Processing

This script downloads a CSV file containing COVID-19 data, transforms the data, and loads it into a PostgreSQL database.

## Prerequisites

Before running the script, ensure that you have the following installed:

- Python (3.x)
- `requests` library (install using `pip install requests`)
- `psycopg2` library (install using `pip install psycopg2`)
- PostgreSQL database

## Usage

1. Clone the repository or download the script file.

2. Install the required libraries by running the following command:

3. Set up the PostgreSQL database and create a table to store the COVID-19 data. Modify the table creation query in the script according to your requirements.

4. Set the necessary environment variables in a `.env` file or directly in your system environment. The required variables are:
- `MY_DB_USER`: PostgreSQL database username
- `MY_DB_PASS`: PostgreSQL database password
- `MY_DB_DB`: PostgreSQL database name
- `MY_DB_SERVER`: PostgreSQL server hostname
- `MY_DB_SERVER_PORT`: PostgreSQL server port

5. Run the script using the following command:

6. The script will download the CSV file, transform the data, save it to a file, and load it into the PostgreSQL database.

7. Check the console output for progress and any error messages.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
