# coding=utf-8
"""
@author: YANG WANG
@file: app.py
@time: 2020/09/08
"""
from autotrading import data_handler
from flask import Flask, jsonify, render_template, url_for
from flask_googlecharts import GoogleCharts, BarChart, MaterialLineChart
from flask_googlecharts.utils import prep_data


app = Flask(__name__)


@app.route('/')
def index():
    df = data_handler.read_stock_table_from_db("GOOG")
    data = df.to_dict(orient='records')
    return render_template('index.html', {'data': data})


if __name__ == '__main__':
    app.run(debug=True)
