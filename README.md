# SQLAlchemy  Surfs Up!


Before taking a long holiday vacation in Honolulu, Hawaii! we need trip planning. To help with trip planning, need to perform some climate analysis on the area. The following outlines what was covered

## Step 1 - Climate Analysis and Exploration

To begin, Python and SQLAlchemy were used to do basic climate analysis and data exploration of climate database. Analysise completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.

* Already have [hawaii.sqlite](Resources/hawaii.sqlite) file to complete climate analysis and data exploration.

* Choose a start date and end date for trip. Make sure that vacation range is approximately 3-15 days total.

* Used SQLAlchemy `create_engine` to connect to sqlite database.

* Used SQLAlchemy `automap_base()` to reflect tables into classes and saved a reference to those classes called `Station` and `Measurement`.

### Precipitation Analysis - Followinng was performed 

* Design a query to retrieve the last 12 months of precipitation data.

* Select only the `date` and `prcp` values.

* Load the query results into a Pandas DataFrame and set the index to the date column.

* Sort the DataFrame values by `date`.

* Plot the results using the DataFrame `plot` method.

  ![precipitation](Images/precipitation.png)

* Use Pandas to print the summary statistics for the precipitation data.

### Station Analysis - Following was performed 

* Design a query to calculate the total number of stations.

* Design a query to find the most active stations.

  * List the stations and observation counts in descending order.

  * Which station has the highest number of observations?

  	* Used a function such as `func.min`, `func.max`, `func.avg`, and `func.count` in queries.

* Design a query to retrieve the last 12 months of temperature observation data (TOBS).

  * Filter by the station with the highest number of observations.

  * Plot the results as a histogram with `bins=12`.

    ![station-histogram](Images/station-histogram.png)

- - -

## Step 2 - Climate App

Now that initial analysis completed, design a Flask API based on the queries that we just developed.

* Use Flask to create different routes.

### Routes

* `/`

  * Home page.

  * List all routes that are available.

* `/api/v1.0/precipitation`

  * Convert the query results to a dictionary using `date` as the key and `prcp` as the value.

  * Return the JSON representation of the dictionary.

* `/api/v1.0/stations`

  * Return a JSON list of stations from the dataset.

* `/api/v1.0/tobs`
  * Query the dates and temperature observations of the most active station for the last year of data.
  
  * Return a JSON list of temperature observations (TOBS) for the previous year.

* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

  * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.

  * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.

  * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.

## Details

* Joined the station and measurement tables for some of the queries.

* Used  Flask `jsonify` to convert API data into a valid JSON response object.

- - -

## Bonus: Other bonus Analyses performed

### Temperature Analysis I

* Hawaii is reputed to enjoy mild weather all year. Is there a meaningful difference between the temperature in, for example, June and December?

* used SQLAlchemy to perform this portion.

* Identify the average temperature in June at all stations across all available years in the dataset. Do the same for December temperature.

* Use the t-test to determine whether the difference in the means, if any, is statistically significant. Used unpaired t-test.

### Temperature Analysis II

* A function called `calc_temps` that will accept a start date and end date in the format `%Y-%m-%d`. The function will return the minimum, average, and maximum temperatures for that range of dates.

* Used the `calc_temps` function to calculate the min, avg, and max temperatures for trip using the matching dates from the previous year (i.e., use "2017-01-01" if trip start date was "2018-01-01").

* Plot the min, avg, and max temperature from previous query as a bar chart.

  * Use the average temperature as the bar height.

  * Use the peak-to-peak (TMAX-TMIN) value as the y error bar (YERR).

    ![temperature](Images/temperature.png)

### Daily Rainfall Average

* Calculate the rainfall per weather station using the previous year's matching dates.

* Calculate the daily normals. Normals are the averages for the min, avg, and max temperatures.

* A function called `daily_normals` that will calculate the daily normals for a specific date. This date string will be in the format `%m-%d`. All historic TOBS that match that date string were retrieved.

* Create a list of dates for trip in the format `%m-%d`. Use the `daily_normals` function to calculate the normals for each date string and append the results to a list.

* Load the list of daily normals into a Pandas DataFrame and set the index equal to the date.

* Use Pandas to plot an area plot (`stacked=False`) for the daily normals.

  ![daily-normals](Images/daily-normals.png)


