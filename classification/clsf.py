from flask import Blueprint, render_template, request, session, g
from flask import current_app
# from fbprophet import Prophet
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler
import os, joblib
import pandas as pd

clsf_bp = Blueprint('clsf_bp', __name__)
menu = {'ho':0, 'da':0, 'ml':1, 
            'se':0, 'co':0, 'cg':0, 'cr':0, 'wc':0,
            'cf':1, 'ac':0, 're':0, 'cu':0, 'nl':0}


@clsf_bp.route('/titanic', methods=['GET', 'POST'])
def titanic():
    if request.method == 'GET':
        return render_template('classification/titanic.html', menu=menu)
    else:
        index = int(request.form['index'] or '0')
        df = pd.read_csv('static/data/titanic_test.csv')
        scaler = joblib.load('static/model/titanic_scaler.pkl')
        test_data = df.iloc[index, :-1].values.reshape(1,-1)
        test_scaled = scaler.transform(test_data)
        label = df.iloc[index, 0]
        lrc = joblib.load('static/model/titanic_lr.pkl')
        svc = joblib.load('static/model/titanic_sv.pkl')
        rfc = joblib.load('static/model/titanic_rf.pkl')
        pred_lr = lrc.predict(test_scaled)
        pred_sv = svc.predict(test_scaled)
        pred_rf = rfc.predict(test_scaled)
        result = {'index':index, 'label':label,
                  'pred_lr':pred_lr[0], 'pred_sv':pred_sv[0], 'pred_rf':pred_rf[0]}

        tmp = df.iloc[index, 1:].values
        value_list = []
        int_index_list = [0, 1, 3, 4, 6, 7]
        for i in range(8):
            if i in int_index_list:
                value_list.append(int(tmp[i]))
            else:
                value_list.append(tmp[i])
        org = dict(zip(df.columns[1:], value_list))
        return render_template('classification/titanic_res.html', menu=menu, 
                                res=result, org=org)

@clsf_bp.route('/cancer', methods=['GET', 'POST'])
def cancer():
    if request.method == 'GET':
        return render_template('classification/cancer.html', menu=menu)
    else:
        index = int(request.form['index'])
        df = pd.read_csv('static/data/cancer_test.csv')
        scaler = MinMaxScaler()
        scaled_test = scaler.fit_transform(df.iloc[:, :-1])
        test_data = scaled_test[index, :].reshape(1,-1)
        label = df.iloc[index, -1]
        lrc = joblib.load('static/model/cancer_lr.pkl')
        svc = joblib.load('static/model/cancer_sv.pkl')
        rfc = joblib.load('static/model/cancer_rf.pkl')
        pred_lr = lrc.predict(test_data)
        pred_sv = svc.predict(test_data)
        pred_rf = rfc.predict(test_data)
        result = {'index':index, 'label':label,
                  'pred_lr':pred_lr[0], 'pred_sv':pred_sv[0], 'pred_rf':pred_rf[0]}
        org = dict(zip(df.columns[:-1], df.iloc[index, :-1]))
        return render_template('classification/cancer_res.html', menu=menu, 
                                res=result, org=org)

@clsf_bp.route('/iris', methods=['GET', 'POST'])
def iris():
    if request.method == 'GET':
        return render_template('classification/iris.html', menu=menu)
    else:
        index = int(request.form['index'] or '0')
        df = pd.read_csv('static/data/iris_test.csv')
        scaler = joblib.load('static/model/iris_scaler.pkl')
        test_data = df.iloc[index, :-1].values.reshape(1,-1)
        test_scaled = scaler.transform(test_data)
        label = df.iloc[index, -1]
        lrc = joblib.load('static/model/iris_lr.pkl')
        svc = joblib.load('static/model/iris_sv.pkl')
        rfc = joblib.load('static/model/iris_rf.pkl')
        pred_lr = lrc.predict(test_scaled)
        pred_sv = svc.predict(test_scaled)
        pred_rf = rfc.predict(test_scaled)

        species = ['Setosa', 'Versicolor', 'Virginica']
        result = {'index':index, 'label':f'{label} ({species[label]})',
                  'pred_lr':f'{pred_lr[0]} ({species[pred_lr[0]]})', 
                  'pred_sv':f'{pred_sv[0]} ({species[pred_sv[0]]})', 
                  'pred_rf':f'{pred_rf[0]} ({species[pred_rf[0]]})'}
        org = dict(zip(df.columns[:-1], df.iloc[index, :-1]))
        return render_template('classification/iris_res.html', menu=menu, 
                                res=result, org=org)