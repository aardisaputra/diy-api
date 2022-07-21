import pandas as pd
import flask
from flask import request

df = pd.read_csv("collegeadmissions.csv", header = 0)
app = flask.Flask(__name__)

@app.route("/")
def test():
    return "hello world"

@app.route("/in-state", methods = ["GET"])
def state():
    s = request.args.get("s")
    return in_state(df, s).to_string()

@app.route("/high-admin")
def high_admin():
    return highest_admissions(df).to_string()

@app.route("/high-part-time")
def high_part_time():
    return highest_part_time_enrollment(df).to_string()

# dataframe of universities in a specfic state
def in_state(dataframe, state):
    dataframe = dataframe[dataframe["FIPS state code"].notna()]
    return dataframe[dataframe["FIPS state code"] == state]["Name"]

# college with the highest admissions yield
def highest_admissions(dataframe):
    dataframe = dataframe[dataframe["Admissions yield - total"].notna()]
    highestYield = dataframe["Admissions yield - total"].max()
    return dataframe[dataframe["Admissions yield - total"] == highestYield][["Name", "Admissions yield - total"]]

# colleges with highest percentage of part-time enrollment
def highest_part_time_enrollment(dataframe):
    dataframe = dataframe[dataframe["Part-time enrollment"].notna()]
    dataframe["part_time_percent"] = dataframe["Part-time enrollment"] / dataframe["Total  enrollment"]
    highestPercent = dataframe["part_time_percent"].max()
    return dataframe[dataframe["part_time_percent"] == highestPercent][["Name", "part_time_percent"]]

if __name__ == "__main__":
    app.run()