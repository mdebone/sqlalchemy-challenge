# import dependencies
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

######################################################
# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database and tables
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

################################
# session = Session(engine)

# Use the function `calc_temps` to calculate the tmin, tavg, and tmax 
# for a year in the data set
# def calc_temps(start_date, end_date):
#     """TMIN, TAVG, and TMAX for a list of dates.
    
#     Args:
#         start_date (string): A date string in the format %Y-%m-%d
#         end_date (string): A date string in the format %Y-%m-%d
        
#     Returns:
#         TMIN, TAVE, and TMAX
#     """
    
#     return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
#         filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

# session.close()
################################

# Create an app
app = Flask(__name__)

################################
# Flask Routes
# Define what to do when user hits the index route
@app.route("/")
def home():
    """List all available api routes."""
    return(
        f"Welcome to the Hawaii Weather API<br/> "
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]/[end_date format:yyyy-mm-dd]<br/>"
    )
###########################################################

# create precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create the session link
    session = Session(engine)

    """Return the dictionary for date and precipitation info"""
    # Query precipitation and date values 
    prec_results = session.query(Measurement.date, Measurement.prcp).all()
        
    session.close()
    
    # Create a dictionary as date the key and prcp as the value
    precipitation = []
    for result in prec_results:
        precipitation_dict = {}
        precipitation_dict[result[0]] = result[1]
        precipitation.append(precipitation_dict)

    return jsonify(precipitation )

#################################################################

# create stations route    
@app.route("/api/v1.0/stations")
def stations():
    # Create the session link
    session = Session(engine)
    
    """Return a JSON list of stations from the dataset."""
    # Query data to get stations list
    station_results = session.query(Station.station, Station.name).all()
    
    session.close()

    # Convert list of tuples into list of dictionaries for each station and name
    station_list = []
    for result in station_results:
        station_dict = {}
        station_dict["station"]= result[0]
        station_dict["name"] = result[1]
        station_list.append(station_dict)
    
    # jsonify the list
    return jsonify(station_list)

##################################################################

# create temperatures route
@app.route("/api/v1.0/tobs")
def tobs():
    # create session link
    session = Session(engine)
    
    """Return a JSON list of Temperature Observations (tobs) for the previous year."""
    # query tempratures from a year from the last data point. 
    #query_date  is "2016-08-23" for the last year query
    tobs_results = session.query(Measurement.tobs, Measurement.date).\
        filter(Measurement.date >= '2016-08-23').\
        all()

    session.close()

    # convert list of tuples to show date and temprature values
    tobs_list = []
    for result in tobs_results:
        tobs_dict = {}
        tobs_dict["date"] = result[1]
        tobs_dict["temprature"] = result[0]
        tobs_list.append(tobs_dict)

    # jsonify the list
    return jsonify(tobs_list)

######################################################################

# create start route
@app.route("/api/v1.0/<start>")
def start(start):
    # create session link
    session = Session(engine)

    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start date."""

    # take any date and convert to yyyy-mm-dd format for the query
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')

    # query data for the start date value
    start_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        all()

    session.close()

    # Create a list to hold results
    start_date_tobs = []
    for result in start_results:
        start_date_dict = {}
        start_date_dict["start_date"] = start_date
        start_date_dict["TMIN"] = result[0]
        start_date_dict["TAVG"] = result[1]
        start_date_dict["TMAX"] = result[2]
        start_date_tobs.append(start_date_dict)

    # jsonify the result
    return jsonify(start_date_tobs)

##################################################################
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    # create session link
    session = Session(engine)

    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start and end dates."""

    # take start and end dates and convert to yyyy-mm-dd format for the query
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    end_date = dt.datetime.strptime(end, "%Y-%m-%d")

    # query data for the start date value
    start_end_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        filter(Measurement.date <= end_date).\
        all()

    session.close()

    # Create a list to hold results
    start_end_date_tobs = []
    for result in start_end_results:
        start_end_dict = {}
        start_end_dict["start_date"] = start_date
        start_end_dict["end_date"] = end_date
        start_end_dict["TMIN"] = result[0]
        start_end_dict["TAVG"] = result[1]
        start_end_dict["TMAX"] = result[2]
        start_end_date_tobs.append(start_end_dict)

    # jsonify the result
    return jsonify(start_end_date_tobs)

##########################################################
#run the app
if __name__ == "__main__":
    app.run(debug=True)