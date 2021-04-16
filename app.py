from flask import Flask, Blueprint, render_template, request, session, g
from classification.clsf import clsf_bp
import os, json

app = Flask(__name__)
app.register_blueprint(clsf_bp, url_prefix='/classification')

@app.route('/')
def index():
    menu = {'ho':1, 'da':0, 'ml':0, 
            'se':0, 'co':0, 'cg':0, 'cr':0, 'wc':0,
            'cf':0, 'ac':0, 're':0, 'cu':0}
    return render_template('index.html', menu=menu)


if __name__ == '__main__':
    app.run(debug=True)