import sqlalchemy
import numpy as np
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Create an app, being sure to pass __name__
app = Flask(__name__)

# engine = create_engine("sqlite:///hawaii.sqlite")
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
conn = engine.connect()
# Declare a Base using `automap_base()`
Base = automap_base()

# reflect an existing database into a new model
Base.prepare(engine, reflect=True)

# reflect the tables
Base.metadata.create_all(conn)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(bind=engine)

# define one year ago date
#recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date

one_year_ago = '2016-08-23'



# Home Route 
@app.route("/")
def welcome_page():
           return (
        f"<p>You've reached Hawaii Weather Station!!</p>"
        f"/api/v1.0/precipitation<br/>Returns a JSON file of precipitation for data between 8/23/16 and 8/23/17<br/>"
        f"/api/v1.0/stations<br/>Return a JSON list of stations from the dataset<br/>"
        f"/api/v1.0/tobs<br/>Returns a JSON list of the Temperature Observations (tobs) for each station for the dates between 8/23/16 and 8/23/17<br/>"
        f"/api/v1.0/start<br/>Return a JSON list of the minimum temperature, the average temperature, and the max temperature for the dates between the given start date<br/>."
        f"/api/v1.0/start/end<br/>Returns a JSON list of the minimum temperature, the average temperature, and the max temperature for the dates between the given start date and end date<br/>."
    )
# /api/v1.0/precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    # 
    precip_data_scores = session.query(Measurement.date, func.avg(Measurement.prcp)).\
    filter(Measurement.date >= one_year_ago).\
    group_by(Measurement.date).\
    all()
    return jsonify(precip_data_scores)


#/api/v1.0/stations
@app.route("/api/v1.0/stations")
def stations():
    station_names = session.query(Station.station, Station.name).all()
    return jsonify(station_names)


#/api/v1.0/tobs
@app.route("/api/v1.0/tobs")
def tobs():
    tobs_previous_year = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= one_year_ago).all()
    return jsonify(tobs_previous_year)

#/api/v1.0/<start> and /api/v1.0/<start>/<end>
@app.route("/api/v1.0/start")
def startDateOnly(start):
    date_temp_queries = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    return jsonify(date_temp_queries)

@app.route("/api/v1.0/start/end")
def startDateEndDate(start,end):

    start_end_temp_queries = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(start_end_temp_queries)


if __name__ == "__main__":
    app.run(debug=True)
