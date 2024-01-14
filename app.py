from flask import Flask, Response
from sqlalchemy import create_engine
import pandas as pd
import json

app = Flask(__name__)

db_url = 'sqlite:///spotify.db'
engine = create_engine(db_url)

@app.route('/api/data', methods=['GET'])
def pribavi_podatke():
    df_db = pd.read_sql('podaci', engine)
    
    df_db['ukupno_vrijeme_koristenja'] = pd.to_timedelta(df_db['ukupno_vrijeme_koristenja'], unit='s')
    df_db['ukupno_vrijeme_koristenja'] = df_db['ukupno_vrijeme_koristenja'].astype(str)
    df_db['pocetak_koristenja'] = df_db['pocetak_koristenja'].astype(str)
    df_db['pretplacen'] = df_db['pretplacen'].map({1: 'Yes', 0: 'No'})


    columns_order = ["ime", "broj_mobitela", "e-mail", "drzava", "pocetak_koristenja", "pretplacen", "starost", "ukupno_vrijeme_koristenja"]

    data_list_ordered = df_db[columns_order].to_dict(orient='records')

    response = Response(json.dumps({'data': data_list_ordered}, indent=2), content_type='application/json; charset=utf-8')

    return response

if __name__ == '__main__':
    app.run(debug=True)