import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy.orm import Session
from flask import Flask, jsonify


engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def home():
    return (
        f'Available Routes: <br>' 
        f'Precipitation: /api/v1.0/precipitation <br>'
        f'Stations: /api/v1.0/stations <br>'
        f'Temperature: /api/v1.0/tobs <br>'
        f'Temperature from Start Date: /api/v1.0/start <br>'
        f'Temperature from Start to End Date: /api/v1.0/start_end <br>'
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    query_results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    prcp_list = []
    for date, prcp in query_results:
        prcp_dict = {}
        prcp_dict['date'] = date
        prcp_dict['prcp'] = prcp
        prcp_list.append(prcp_dict)

    return jsonify(prcp_list)

@app.route("/api/v1.0/stations")
def station():
    session = Session(engine)
    query_results = session.query(Station.name, Station.station).all()
    session.close()

    station_list = []
    for name, station in query_results:
        station_dict = {}
        station_dict['name'] = name
        station_dict['station'] = station
        station_list.append(station_dict)

    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def temperature():
    session = Session(engine)

    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = dt.datetime.strptime(last_date[0], '%Y-%m-%d')
    query_date = dt.date(last_date.year -1, last_date.month, last_date.day)
    query_result = session.query(Measurement.date,Measurement.tobs).filter(Measurement.date >= query_date).all()
    
    session.close()

    tobs_list = []
    for date, tobs in query_result:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Tobs"] = tobs
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)

@app.route("/api/v1.0/start")
def temperature_start():
    session = Session(engine)

    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = dt.datetime.strptime(last_date[0], '%Y-%m-%d')
    query_date = dt.date(last_date.year -1, last_date.month, last_date.day)

    query_result = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= query_date).all()

    tobs_list = []
    for min, max, avg in query_result:
        tobs_dict = {}
        tobs_dict['Min'] = min
        tobs_dict['Max'] = max
        tobs_dict['Avg'] = avg
        tobs_list.append(tobs_dict)
    
    return jsonify(tobs_list)

@app.route("/api/v1.0/start_end")
def temperature_start_end():
    session = Session(engine)

    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = dt.datetime.strptime(last_date[0], '%Y-%m-%d')
    query_date = dt.date(last_date.year -1, last_date.month, last_date.day)

    query_result = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= query_date, Measurement.date <= last_date).all()

    tobs_list = []
    for min, max, avg in query_result:
        tobs_dict = {}
        tobs_dict['Min'] = min
        tobs_dict['Max'] = max
        tobs_dict['Avg'] = avg
        tobs_list.append(tobs_dict)
    
    return jsonify(tobs_list)

if __name__ == "__main__":
    app.run(debug=False)
