# coding=utf-8
"""
@author: YANG WANG
@file: app.py
@time: 2020/09/08
"""
from autotrading import data_handler
from flask import Flask, jsonify, render_template, url_for
import pandas as pd
# from flask_googlecharts import GoogleCharts, BarChart, MaterialLineChart
# from flask_googlecharts.utils import prep_data

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data', methods=["GET"])
def request():
    #data = pd.read_json("./GOOG.json", orient="split")
    choose_cols = ["Close"]
    df = data_handler.read_stock_table_from_db("GOOG")[choose_cols]
    df = df.reset_index(drop=False, inplace=False)
    df["Date"] = df["Date"].apply(lambda x: pd.to_datetime(x).date())

    list_data = df.values.tolist()
    # Add column name
    list_data.insert(0, df.columns.tolist())
    json_data = {
        "data": list_data
    }

    return jsonify(json_data)

if __name__ == "__main__":
    app.run(debug=True)
