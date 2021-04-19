from flask import Blueprint, render_template, request, session, g
from flask import current_app
# from fbprophet import Prophet
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as pdr
# from my_util.weather import get_weather

rgrs_bp = Blueprint('rgrs_bp', __name__)
menu = {'ho':0, 'da':0, 'ml':1, 
        'se':0, 'co':0, 'cg':0, 'cr':0, 'wc':0,
        'cf':0, 'ac':0, 're':1, 'cu':0, 'nl':0}

@rgrs_bp.route('/boston', methods=['GET', 'POST'])
def boston():
    if request.method == 'GET':
        feature_list = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 
                        'TAX', 'PTRATIO', 'B', 'LSTAT']
        return render_template('regression/boston.html', feature_list=feature_list,
                               menu=menu)
    else:
        index = int(request.form['index'] or '0')
        feature_list = request.form.getlist('feature')
        if len(feature_list) == 0:
            feature_list = ['RM', 'LSTAT']
        df = pd.read_csv('static/data/boston_train.csv')
        X = df[feature_list].values
        y = df.target.values

        lr = LinearRegression()
        lr.fit(X, y)
        weight, bias = lr.coef_, lr.intercept_

        df_test = pd.read_csv('static/data/boston_test.csv')
        X_test = df_test[feature_list].values[index, :]
        y_test = df_test.target[index]
        pred = np.dot(X_test, weight.T) + bias      # tmp = lr.predict(X_test.reshape(1,-1))
        pred = np.round(pred, 2)                    # pred = np.round(tmp[0])

        result_dict = {'index':index, 'feature':feature_list, 'y':y_test, 'pred':pred}
        org = dict(zip(df.columns[:-1], df_test.iloc[index, :-1]))
        return render_template('regression/boston_res.html', res=result_dict, org=org,
                               menu=menu)


@rgrs_bp.route('/diabetes', methods=['GET', 'POST'])
def diabetes():
    if request.method == 'GET':
        return render_template('regression/diabetes.html', menu=menu)
    else:
        index = int(request.form['index'] or '0')
        feature = request.form['feature']
        df = pd.read_csv('static/data/diabetes_train.csv')
        X = df[feature].values.reshape(-1,1)
        y = df.target.values

        lr = LinearRegression()
        lr.fit(X, y)
        weight, bias = lr.coef_, lr.intercept_

        df_test = pd.read_csv('static/data/diabetes_test.csv')
        X_test = df_test[feature][index]
        y_test = df_test.target[index]
        pred = np.round(X_test * weight[0] + bias, 2)

        y_min = np.min(X) * weight[0] + bias
        y_max = np.max(X) * weight[0] + bias
        plt.figure()
        plt.scatter(X, y, label='train')
        plt.plot([np.min(X), np.max(X)], [y_min, y_max], 'r', lw=3)
        plt.scatter([X_test], [y_test], c='r', marker='*', s=100, label='test')
        plt.grid()
        plt.legend()
        plt.title(f'Diabetes target vs. {feature}')
        img_file = os.path.join(current_app.root_path, 'static/img/diabetes.png')
        plt.savefig(img_file)
        mtime = int(os.stat(img_file).st_mtime)

        result_dict = {'index':index, 'feature':feature, 'y':y_test, 'pred':pred}
        return render_template('regression/diabetes_res.html', res=result_dict, mtime=mtime,
                                menu=menu)