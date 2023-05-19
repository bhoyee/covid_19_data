-- 1. Retrieve the total confirmed, death, and recovered cases

SELECT SUM(confirmed) AS total_confirmed, SUM(deaths) AS total_deaths, SUM(recovered) AS total_recovered
FROM covid_19_data;


/* 2. Retrieve the total confirmed, deaths and recovered cases for the first quarter
of each year of observation.*/


SELECT EXTRACT(YEAR FROM observation_date) AS year, 
       SUM(CASE WHEN EXTRACT(MONTH FROM observation_date) <= 3 THEN confirmed ELSE 0 END) AS q1_confirmed,
       SUM(CASE WHEN EXTRACT(MONTH FROM observation_date) <= 3 THEN deaths ELSE 0 END) AS q1_deaths,
       SUM(CASE WHEN EXTRACT(MONTH FROM observation_date) <= 3 THEN recovered ELSE 0 END) AS q1_recovered
FROM covid_19_data
GROUP BY year;



/*  3. Retrieve a summary of all the records. This should include the following
information for each country:
● The total number of confirmed cases
● The total number of deaths
● The total number of recoveries */


SELECT region AS country,
       SUM(confirmed) AS total_confirmed,
       SUM(deaths) AS total_deaths,
       SUM(recovered) AS total_recovered
FROM covid_19_data
GROUP BY region;



/* 4. Retrieve the percentage increase in the number of death cases from 2019 to
2020.

Ans -- */

SELECT 
  (SUM(CASE WHEN EXTRACT(year FROM observation_date) = 2020 THEN deaths ELSE 0 END) - 
   SUM(CASE WHEN EXTRACT(year FROM observation_date) = 2019 THEN deaths ELSE 0 END)) / 
   SUM(CASE WHEN EXTRACT(year FROM observation_date) = 2019 THEN deaths ELSE 0 END) * 100 AS percentage_increase
FROM covid_19_data;

/* 5. Retrieve information for the top 5 countries with the highest confirmed cases.

Ans--- */
SELECT
    region AS country,
    SUM(confirmed) AS total_confirmed_cases
FROM
    covid_19_data
GROUP BY
    region
ORDER BY
    total_confirmed_cases DESC
LIMIT 5;


/* 6. Compute the total number of drop (decrease) or increase in the confirmed
cases from month to month in the 2 years of observation.

Ans---- */

SELECT 
    DATE_TRUNC('month', observation_date) AS year_month, 
    SUM(confirmed) AS total_confirmed,
    SUM(confirmed) - LAG(SUM(confirmed), 1, 0) OVER (ORDER BY DATE_TRUNC('month', observation_date)) AS confirmed_change
FROM 
    covid_19_data
WHERE 
    observation_date >= '2020-01-01' AND observation_date < '2022-01-01'
GROUP BY 
    year_month
ORDER BY 
    year_month ASC;

