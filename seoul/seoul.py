from flask import Blueprint, render_template, request, session, g
from flask import current_app
from datetime import timedelta
import os, folium, json
import numpy as np
import pandas as pd
import matplotlib as mpl 
import matplotlib.pyplot as plt

seoul_bp = Blueprint('seoul_bp', __name__)
menu = {'ho':0, 'da':1, 'ml':0, 
        'se':1, 'co':0, 'cg':0, 'cr':0, 'wc':0,
        'cf':0, 'ac':0, 're':0, 'cu':0, 'nl':0}

@seoul_bp.route('/park', methods=['GET', 'POST'])
def park():
    park_new = pd.read_csv('./static/data/park_info.csv')
    park_gu = pd.read_csv('./static/data/park_gu.csv')
    park_gu.set_index('지역', inplace=True)
    if request.method == 'GET':
        map = folium.Map(location=[37.5502, 126.982], zoom_start=11)
        for i in park_new.index:
            folium.CircleMarker([park_new.lat[i], park_new.lng[i]], 
                                radius=int(park_new['size'][i]),
                                tooltip=f"{park_new['공원명'][i]}({int(park_new.area[i])}㎡)",
                                color='#3186cc', fill_color='#3186cc').add_to(map)
        html_file = os.path.join(current_app.root_path, 'static/img/park.html')
        map.save(html_file)
        mtime = int(os.stat(html_file).st_mtime)
        return render_template('seoul/park.html', menu=menu,
                                park_list=list(park_new['공원명'].sort_values()), 
                                gu_list=list(park_gu.index), mtime=mtime)
    else:
        gubun = request.form['gubun']        if gubun == 'park':
            park_name = request.form['name']
            df = park_new[park_new['공원명'] == park_name].reset_index()
            park_result = {'name':park_name, 'addr':df['공원주소'][0], 
                            'area':int(df.area[0]), 'desc':df['공원개요'][0]}
            map = folium.Map(location=[37.5502, 126.982], zoom_start=11)
            for i in park_new.index:
                folium.CircleMarker([park_new.lat[i], park_new.lng[i]], 
                                    radius=int(park_new['size'][i]),
                                    tooltip=f"{park_new['공원명'][i]}({int(park_new.area[i])}㎡)",
                                    color='#3186cc', fill_color='#3186cc').add_to(map)
            folium.CircleMarker([df.lat[0], df.lng[0]], radius=int(df['size'][0]),
                                    tooltip=f"{df['공원명'][0]}({int(df.area[0])}㎡)",
                                    color='crimson', fill_color='crimson').add_to(map)
            html_file = os.path.join(current_app.root_path, 'static/img/park_res.html')
            map.save(html_file)
            mtime = int(os.stat(html_file).st_mtime)
            return render_template('seoul/park_res.html', menu=menu, 
                                    park_result=park_result, mtime=mtime)
        else:
            gu_name = request.form['gu']
            df = park_gu[park_gu.index == gu_name].reset_index()
            park_result = {'gu':df['지역'][0], 
                            'area':int(df['공원면적'][0]), 'm_area':int(park_gu['공원면적'].mean()),
                            'count':df['공원수'][0], 'm_count':round(park_gu['공원수'].mean(),1),
                            'area_ratio':round(df['공원면적비율'][0],2), 'm_area_ratio':round(park_gu['공원면적비율'].mean(),2),
                            'per_person':round(df['인당공원면적'][0],2), 'm_per_person':round(park_gu['인당공원면적'].mean(),2)}
            df = park_new[park_new['지역'] == gu_name].reset_index()
            map = folium.Map(location=[df.lat.mean(), df.lng.mean()], zoom_start=13)
            for i in df.index:
                folium.CircleMarker([df.lat[i], df.lng[i]], 
                                    radius=int(df['size'][i])*3,
                                    tooltip=f"{df['공원명'][i]}({int(df.area[i])}㎡)",
                                    color='#3186cc', fill_color='#3186cc').add_to(map)
            html_file = os.path.join(current_app.root_path, 'static/img/park_res.html')
            map.save(html_file)
            mtime = int(os.stat(html_file).st_mtime)
            return render_template('seoul/park_res2.html', menu=menu, 
                                    park_result=park_result, mtime=mtime)