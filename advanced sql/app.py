# Import the dependencies.
import numpy as np
import sqlalchemy
import datetime as dt
import pandas as pd
from datetime import datetime, timedelta  
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, desc
from sqlalchemy import and_
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# Create a SQLAlchemy engine to connect to the SQLite database.
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect the existing database into an SQLAlchemy ORM model.
Base = automap_base()
Base.prepare(autoload_with=engine)

# Save references to the tables we'll be working with.
station = Base.classes.station
measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################

# Initialize the Flask app.
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    session = Session(engine)
    """Homepage with available routes"""
    return (
        f"Welcome to the Climate API!<br/><br/>"
        f"Available Routes:<br/>"
        f"<a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>/api/v1.0/stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>/api/v1.0/tobs</a><br/>"
        f"Dynamic Route:/api/v1.0/&lt;start&gt;</a><br/>"  
        f"Dynamic Route:<a>/api/v1.0/&lt;start&gt;/&lt;end&gt;</a><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Query and return precipitation data for the last 12 months"""
    session = Session(engine)
    # Find the most recent date in the data set.
    recent_date = session.query(measurement.date).order_by(measurement.date.desc()).first()

    # Calculate the date one year from the last date in data set.
    most_recent_date = pd.to_datetime(recent_date[0])
    query_date = most_recent_date - dt.timedelta(days=365)

    # Convert query_date to a regular datetime object
    query_date = query_date.date()

    # Convert recent_date to a regular datetime object
    recent_date = recent_date[0]

    # Perform a query to retrieve the data and precipitation scores
    retrieve_data = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= query_date, measurement.date <= recent_date).\
        order_by(measurement.date.desc()).all()

    # Convert the SQLAlchemy result to a list of dictionaries
    precipitation_data = [{"date": date, "prcp": prcp} for date, prcp in retrieve_data]
    session.close()
    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    """Return a list of stations"""
    stations= session.query(station.station).all()
    session.close()
    
    # Convert the SQLAlchemy result to a list of dictionaries
    station_list = [row._asdict() for row in stations]

    # Convert the station list to a JSON response
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    most_active_station_id = 'USC00519281'
    session = Session(engine)
    # Find the most recent date in the data set.
    latest_date = session.query(measurement.date).order_by(measurement.date.desc()).first()

    # Calculate the date one year from the last date in data set.
    most_latest_date = pd.to_datetime(latest_date[0])
    max_date = most_latest_date - dt.timedelta(days=365)

    # Convert query_date to a regular datetime object
    max_date = max_date.date()

    # Convert recent_date to a regular datetime object
    latest_date = latest_date[0]

    # Query temperature data for the previous year
    temperature_data = session.query(measurement.date, measurement.tobs).\
        filter(measurement.station == most_active_station_id).\
        filter(measurement.date >= max_date, measurement.date <= latest_date).\
        order_by(measurement.date.desc()).all()
    
    # Convert the SQLAlchemy result to a list of dictionaries
    temp_data = [{"date": date, "tobs": tobs} for date, tobs in temperature_data]

    # Convert the list to a JSON response
    return jsonify(temp_data)

@app.route('/api/v1.0/<start>', methods=['GET'])
def start_date_stats(start):
    session = Session(engine)

   # Query the maximum date in the dataset
    max_date = session.query(func.max(measurement.date)).scalar()
    max_date = datetime.strptime(max_date, '%Y-%m-%d')
    
    # Define your start_date and end_date as datetime objects
    
    start_date = datetime.strptime(f'{start}', '%Y-%m-%d').date()
    # Query temperature data for the last 12 months
    # Query the minimum, maximum, and average temperatures from start_date to max_date
    temperature_stats_end = session.query(
        func.min(measurement.tobs).label('min_temp'),
        func.max(measurement.tobs).label('max_temp'),
        func.avg(measurement.tobs).label('avg_temp')
    ).filter(and_(measurement.date >=start_date, measurement.date <=max_date)).all()

    # Extract temperature statistics from the query result (first row)
    temperature_stat_dict = {
        'min_temp': temperature_stats_end[0].min_temp,
        'avg_temp': temperature_stats_end[0].avg_temp,
        'max_temp': temperature_stats_end[0].max_temp
    }

    return jsonify(temperature_stat_dict)

@app.route('/api/v1.0/<start>/<end>', methods=['GET'])
def start_end_date_stats(start, end):
    session = Session(engine)
    
    # Define your start_date and end_date as datetime objects
    start_date = datetime.strptime(f'{start}', '%Y-%m-%d').date()
    end_date = datetime.strptime(f'{end}', '%Y-%m-%d').date()
    
    
    # Query the minimum, maximum, and average temperatures from start_date to end_date
    temperature_stats_end = session.query(
        func.min(measurement.tobs).label('min_temp'),
        func.max(measurement.tobs).label('max_temp'),
        func.avg(measurement.tobs).label('avg_temp')
    ).filter(and_(measurement.date >=start_date, measurement.date <=end_date)).all()
   
    # Close the session
    session.close()
    
    # Extract temperature statistics from the query result (first row)
    temperature_stat_end_dict = {
        'min_temp': temperature_stats_end[0].min_temp,
        'avg_temp': temperature_stats_end[0].avg_temp,
        'max_temp': temperature_stats_end[0].max_temp
    }
    return jsonify(temperature_stat_end_dict)

if __name__ == "__main__":
    app.run(debug=True)
