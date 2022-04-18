
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


@app.route("/")
def welcome():
    return (
        f"Welcome to the Surf's Up assignment API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start> and /api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data as json"""

    return (
        f"Hello!"
    )

@app.route("/api/v1.0/stations")
def precipitation():
    """Return the station data as json"""

    return (
        f"Hi there!"
    )

@app.route("/api/v1.0/tobs")
def precipitation():
    """Return the station data as json"""

     return (
        f"Good day!"
    )

@app.route("/api/v1.0/<start> and /api/v1.0/<start>/<end>")
def precipitation():
    """Return the station data as json"""

        return (
        f"Make yourseld at home!"
    )


if __name__ == "__main__":
    app.run(debug=True)
