%matplotlib inline
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
#
# Reflect Tables into SQLAlchemy ORM
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
#
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)
#
# reflect an existing database into a new model
Base = automap_base()
Base.metadata.create_all(engine)
#
# reflect the tables
Base.prepare(engine, reflect = True)
#
# Create our session (link) from Python to the DB
session = Session(bind=engine)
# View all of the classes that automap found
Base.classes.keys()
#
inspector = inspect(engine)
inspector.get_table_names()
#
# Get a list of column names and types from measurement
measure_columns = inspector.get_columns('measurement')
for c in measure_columns:
    print(c['name'], c['type'])
#
# Get a list of column names and types from station
station_columns = inspector.get_columns('station')
for c in station_columns:
    print(c['name'], c['type'])
#
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
#
#
# Exploratory Precipitation Analysis
#Find the total dates
session.query(func.count(Measurement.date)).all()
#
# Find the earliest date
session.query(Measurement.date).order_by(Measurement.date).first()
#
# Find the most recent date in the data set.
session.query(Measurement.date).order_by(Measurement.date.desc()).first()
#
# Combine percpitation values across stations
# Design a query to retrieve the last 12 months of precipitation data and plot the results.
# okay we don't need the other part of the greater than because the end date is inclusive and doesnt need to be called
last_year_dates = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > '2016-08-23').\
    group_by(Measurement.date).\
    all()
#
#last_year_dates
#
# Save the query results as a Pandas DataFrame and set the index to the date column
df = pd.DataFrame(last_year_dates, columns=['date', 'prcp'])
df.set_index('date', inplace=True)
df.plot.bar()
plt.title("Year to Date Rainfall")
plt.xlabel("Date")
plt.ylabel("Inches")
plt.tight_layout()
plt.show()
#
# Exploratory Station Analysis
# Design a query to calculate the total number stations in the dataset
station_number = session.query(Station.station).group_by(Station.station).all()
station_number
# Design a query to find the most active stations (i.e. what stations have the most rows?)
most_active = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).\
        order_by(Measurement.station).\
        all()
most_active
#
# List the stations and the counts in descending order.
descending = session.query(Measurement.station).order_by(Measurement.station.desc())
descending
#
# Close Session
session.close()