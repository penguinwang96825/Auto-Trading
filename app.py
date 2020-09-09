import datetime
import pandas as pd
from autotrading import data_handler
from flask import Flask
from flask import render_template, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data', methods=["GET"])
def request():
    choose_cols = ["Close"]
    df = data_handler.read_stock_table_from_db("GOOG")[choose_cols]
    df = df.reset_index(drop=False, inplace=False)
    df["Date"] = df["Date"].apply(lambda x: pd.to_datetime(x).date())
    print(df)
    df_json = df.to_json(orient="split")
    data = pd.read_json(df_json, orient="split")
    list_data = data.values.tolist()
    # Add column name
    list_data.insert(0, df.columns.tolist())
    json_data = {
        "data": list_data
    }
    return jsonify(json_data)


if __name__ == "__main__":
    app.run(debug=True)
