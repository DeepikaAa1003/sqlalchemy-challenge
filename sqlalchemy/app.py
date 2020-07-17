import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



def Calculatedate():
    session = Session(engine)
    for row in session.query(Measurement.date).order_by(Measurement.date.desc()).limit(1):
        print(dt.datetime.strptime(row.date, '%Y-%m-%d').date())
    
    session.close()
    
    Latest_date = dt.datetime.strptime(row.date, '%Y-%m-%d').date()
    
    Date_12MonthsBack = Latest_date - dt.timedelta(days=366)
    print(Date_12MonthsBack)
    
    return(Date_12MonthsBack)
#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
        )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create ession (link) from Python to the DB
    session = Session(engine)

    
    # Query all Measurement
    results = session.query(Measurement.date, Measurement.prcp).\
                order_by(Measurement.date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_measurements
    all_measurements = []
    for mdate, mprcp in results:
        measurements_dict = {}
        measurements_dict[mdate] = mprcp
        all_measurements.append(measurements_dict)

    return jsonify(all_measurements)
    
@app.route("/api/v1.0/stations")
def stations():
    # Create session (link) from Python to the DB
    session = Session(engine)

    
    # Query all stations
    results = session.query(Station.station, Station.name).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_stations
    all_stations = []
    for station, name in results:
        stations_dict = {}
        stations_dict[station] = name
        all_stations.append(stations_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    Date_12MonthsBack = Calculatedate()
    # Create session (link) from Python to the DB
    session = Session(engine)

    
    # Query all Measurement for last 1 year
    results = session.query(Measurement.tobs, Measurement.date).\
                filter(Measurement.date > Date_12MonthsBack).\
                order_by(Measurement.date).all()
    
    session.close()

    # Create a dictionary from the row data and append to a list of all_tobs
    all_tobs = []
    for tobs, date in results:
        tobs_dict = {}
        tobs_dict[date] = tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)   

@app.route("/api/v1.0/<start>")
def averageData(start):
    session = Session(engine)

    # Query all Measurement data greater than start date passed
    results = session.query(  Measurement.date,\
                                func.min(Measurement.tobs), \
                                func.avg(Measurement.tobs), \
                                func.max(Measurement.tobs)).\
                        filter(Measurement.date >= start).\
                        group_by(Measurement.date).all()
    
    session.close()
    new_list = []
    for mdate, mmin, mavg, mmax in results:
        new_dict = {}
        new_dict["Date"] = mdate
        new_dict["TMIN"] = mmin
        new_dict["TAVG"] = mavg
        new_dict["TMAX"] = mmax
        new_list.append(new_dict)
    return jsonify(new_list)

@app.route("/api/v1.0/<start>/<end>")
def averageDataDateRange(start, end):
    session = Session(engine)

     # Query all Measurement data for a date range
    results = session.query(  Measurement.date,\
                                func.min(Measurement.tobs), \
                                func.avg(Measurement.tobs), \
                                func.max(Measurement.tobs)).\
                        filter(Measurement.date >= start).\
                        filter(Measurement.date <= end).\
                        group_by(Measurement.date).all()
    
    session.close()
    new_list = []
    for mdate, mmin, mavg, mmax in results:
        new_dict = {}
        new_dict["Date"] = mdate
        new_dict["TMIN"] = mmin
        new_dict["TAVG"] = mavg
        new_dict["TMAX"] = mmax
        new_list.append(new_dict)
    return jsonify(new_list) 


if __name__ == "__main__":
    app.run(debug=True)
