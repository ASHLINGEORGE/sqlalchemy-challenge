
# Climate Analysis and Flask API

## Overview

The Climate Analysis and Flask API project is a comprehensive exploration of climate data using Python and associated libraries, along with the development of a user-friendly Flask API for accessing this data. This project aims to provide insights into climate patterns and make climate-related data accessible through a web interface.

### Part 1: Analyze and Explore the Climate Data

In the first part of the project, we conduct a detailed analysis of climate data from an SQLite database. Key steps include:

- Establishing a database connection using SQLAlchemy.
- Precipitation analysis to find recent precipitation trends.
- Station analysis to determine the most-active weather stations.
- Visualizing data using Matplotlib and summarizing findings with Pandas.

### Part 2: Design Your Climate App

In the second part, we design a Flask API based on the insights gained from the data analysis. The API offers several routes to access climate data, making it user-friendly. These routes include:

- Retrieving precipitation data for the last 12 months.
- Accessing information about weather stations.
- Obtaining temperature observations for specific time periods.
- Calculating summary statistics for temperature data.

### Available Routes

- `/`: Start at the homepage. Lists all available routes.
- `/api/v1.0/precipitation`: Retrieve the last 12 months of precipitation data as a JSON dictionary with date as the key and prcp as the value.
- `/api/v1.0/stations`: Return a JSON list of stations from the dataset.
- `/api/v1.0/tobs`: Query the dates and temperature observations of the most-active station for the previous year of data. Return a JSON list of temperature observations.
- `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`: Return a JSON list of the minimum temperature (TMIN), average temperature (TAVG), and maximum temperature (TMAX) for a specified start or start-end date range.

### Author
#### Ashlin Shinu George
