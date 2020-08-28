import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"/api/v1.0/precipitation <br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    last_year_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation_scores = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > last_year_date).all()

    

    session.close()

    # Convert list of tuples into normal list
    prcp = dict(precipitation_scores)

    return jsonify(prcp)

@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    station_list = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    sta = list(np.ravel(station_list))

    return jsonify(sta)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    last_year_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    last_12months_temp_observation = session.query(Measurement.tobs).\
    filter(Measurement.date >= last_year_date).\
    filter(Measurement.station == "USC00519281").all()

    session.close()

    # Convert list of tuples into normal list
    tobs = list(np.ravel(last_12months_temp_observation))

    return jsonify(tobs) 

@app.route("/api/v1.0/<start>")
def start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    T_observation = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).all()

    session.close()

    T_ob = list(np.ravel(T_observation))

    return jsonify(T_ob) 

@app.route("/api/v1.0/<start>/<end>")
def date(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    T_observation = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

    T_ob = list(np.ravel(T_observation))

    return jsonify(T_ob) 





if __name__ == '__main__':
    app.run(debug=True)