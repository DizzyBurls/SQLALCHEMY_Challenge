#################################################
# Useful Dependencies
#################################################

import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Engine and Database Setup
#################################################

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station


#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

# This page shows all of the other pages that a user may access on this site.

@app.route("/")
def welcome():
    return (
        f"Welcome to the Surf's Up Assignment API!<br/><br/>"
        f"Available Routes:<br/><br/>"
        f"/api/v1.0/precipitation<br/><br/>"
        f"/api/v1.0/stations<br/><br/>"
        f"/api/v1.0/tobs<br/><br/>"
        f"/api/v1.0/yyyy-mm-dd<br/>"
        f"(Where you see yyyy-mm-dd please enter a START date in the prescribed format.)<br/><br/>" 
        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd<br/>"
        f"(Please enter a START date followed by an END date in the prescribed format.)"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)
        
    # Query all of the dates and the precipitation amounts from the Measurement database.
    
    results = session.query(Measurement.date, Measurement.prcp).all()
    
    session.close()
    
    # Create a dictionary from each row of data in 'results'.
    # Append each dictionary to a list called precipitation_all.
    # Express precipitation_all in JSON form.
    
    precipitation_all = []
    for date, prcp in results:
        precipitation_dictionary = {}
        precipitation_dictionary["date"] = date
        precipitation_dictionary["prcp"] = prcp
        precipitation_all.append(precipitation_dictionary)

    return jsonify(precipitation_all)

@app.route("/api/v1.0/stations")
def station():

    session = Session(engine)
      
    # Query all of the ids, stations, names, latitudes, longitudes and elevations from the Stations database.
    
    results = session.query(Station.id, Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()
    
    session.close()
    
    # Create a dictionary from each row of data in 'results'.
    # Append each dictionary to a list called stations_all.
    # Express stations_all in JSON form.

    stations_all = []
    for id, station, name, latitude, longitude, elevation in results:
        stations_dictionary = {}
        stations_dictionary["id"] = id
        stations_dictionary["station"] = station
        stations_dictionary["name"] = name
        stations_dictionary["latitude"] = latitude
        stations_dictionary["longitude"] = longitude
        stations_dictionary["elevation"] = elevation
        stations_all.append(stations_dictionary)

    return jsonify(stations_all)

@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)
    
    # Set up the approprate starting_date and last_date for the query.
    # This code was largely taken from my earlier work in the climate_starter file.
    
    most_recent_date = session.query(Measurement.date).\
    order_by(Measurement.date.desc()).first()
    last_date = dt.datetime.strptime(most_recent_date.date, '%Y-%m-%d').date()
    last_date
    
    starting_date = last_date - dt.timedelta(days=365)
    starting_date

    # Determine the most_active_station in terms of observations taken.
    # Again, largely taken from climate_starter.
    
    most_active_station = session.query(Measurement.station, func.count(Measurement.station)).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.station).desc()).first().station
    
    # Query all temperature observations at the most_active_station between the starting_date and last_date established earlier
    
    results = session.query(Measurement.date, Measurement.station, Measurement.tobs).\
    filter(Measurement.station == most_active_station).\
    filter(Measurement.date >= starting_date).\
    order_by((Measurement.date).asc()).all()
    
    session.close()
    
    # Create a dictionary from each row of data in 'results'.
    # Append each dictionary to a list called most_active_all.
    # Express most_active_all in JSON form.
    
    most_active_all = []
    for date, station, tobs in results:
        most_active_dictionary = {}
        most_active_dictionary["date"] = date
        most_active_dictionary["station"] = station
        most_active_dictionary["tobs"] = tobs
        most_active_all.append(most_active_dictionary)

    return jsonify(most_active_all)


@app.route("/api/v1.0/<start>")
def date_start(start):
    
    session = Session(engine)
    
    # Set up a custom_starting_date.
    
    custom_starting_date = dt.datetime.strptime(start, '%Y-%m-%d').date()
    

    # Query maximum, minimum and average temperature observations between the custom_starting_date and last recored observation.
    
    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= custom_starting_date).all()
    
    session.close()
    
    # Create a dictionary from each row of data in 'results'.
    # Append each dictionary to a list called range_summary_list.
    # Express range_summary_list in JSON form.
    
    range_summary_list = []
    for min, max, avg in results:
        range_summary_dict = {}
        range_summary_dict["min"] = min
        range_summary_dict["max"] = max
        range_summary_dict["avg"] = avg
        range_summary_list.append(range_summary_dict)

    return jsonify(range_summary_list)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):

    session = Session(engine)
    
    # Establish a custom starting_date and a custom last_date.

    starting_date = dt.datetime.strptime(start, '%Y-%m-%d')
    last_date = dt.datetime.strptime(end, '%Y-%m-%d')

    # Query maximum, minimum and average temperature observations between the custom starting_date and the custom last_date.

    results = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
    filter(Measurement.date >= starting_date).\
    filter(Measurement.date <= last_date).all()

    session.close()

    # Create a dictionary from each row of data in 'results'.
    # Append each dictionary to a list called range_summary_list2.
    # Express range_summary_list2 in JSON form.
    
    range_summary_list2 = []
    for min, max, avg in results:
        range_summary_dict2 = {}
        range_summary_dict2["min"] = min
        range_summary_dict2["max"] = max
        range_summary_dict2["avg"] = avg
        range_summary_list2.append(range_summary_dict2)

    return jsonify(range_summary_list2)

if __name__ == "__main__":
    app.run(debug=True)
