from fileinput import filename
import os
from os import listdir
from os.path import isfile, join
# from flask import request,redirect, url_for,send_from_directory, send_file
from flask import Flask,current_app,render_template,flash,request,redirect, url_for,send_from_directory, send_file
import json
from werkzeug.utils import secure_filename
from io import StringIO
import pandas as pd
from zipfile import ZipFile
from glob import glob

from . import rptconverter as rpt

from . import geo_counts as gc

app = Flask(__name__)

ALLOWED_EXTENSIONS = ['RPT']

DIRECTORY = 'hpms-site/static'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/chart')
def chart():
    df = pd.read_csv('static/DataItem52_Cracking_Percent_non_interstate_NHS.csv', sep='|')
    return render_template('charts/chart.html', tables=[df.to_html(classes='data')], titles=df.columns.values)

@app.route('/tools')
def tools():
    return render_template('tools.html')

@app.route('/rpt_convert')
def rpt_convert():
    return render_template('rpt_converter.html')

@app.route('/rpt_convert/converter',methods=['POST'])
def convert_file():
    print(request.files)
    f = request.files['filename']
    # f.save(secure_filename('./static/a.txt'))
    f.save('hpms-site/static/a.txt')
    rpt.rpt_converter('hpms-site/static/a.txt','hpms-site/static/out.xlsx')
    # return redirect('hpms-site/out.xlsx')
    return send_file('static/out.xlsx')

@app.route('/landslide_risk')
def landslide():
    return render_template('landslide_risk.html')

@app.route('/geo_counts_converter')
def geo_counts_conversion():
    return render_template('geo_count.html')

@app.route('/traffic_dashboard')
def traffic_dashboard():
    return render_template('traffic_dashboard.html')

@app.route('/traffic_dashboard/aadt')
def aadt_dashboard():
    return render_template('aadt_dashboard.html')

@app.route('/traffic_dashboard/gas_price')
def gas_dashboard():
    return render_template('gas_price.html')

@app.route('/traffic_dashboard/tourism')
def tourism_dashboard():
    return render_template('tourism.html')

@app.route('/hpms_dashboard')
def hpms_dashboard():
    return render_template('hpms_dashboard.html')


@app.route('/geo_counts_converter/convert',methods=['POST'])
def geo_counts_convert():
    cent_number=1
    metro_number=1
    meh=request.files.getlist("file[]")
    file_list_in=[]
    file_list_out=[]
    for file in meh:
        new_path = r'static\geo_count_conversion\%s' % file.filename
        file.save(new_path)
        cent_number,metro_number,out_file=gc.geo_count_process(new_path,cent_number,metro_number)
        # ZipFile.write(r'static\geo_count_conversion\geo_count_out.xlsx',arcname=r'static\geo_count_conversion\zip_geo_count.zip')
        file_list_in.append(new_path)
        if out_file != '':
            file_list_out.append(out_file)
        print(file_list_in,file_list_out)
    # mypath=r'static\geo_count_conversion'
    # onlyfiles = [os.path.join(mypath,f) for f in listdir(mypath) if isfile(join(mypath, f)) if f.endswith('.xlsx')]
    # print(onlyfiles)
    
    with ZipFile(r'static\geo_count_conversion\zip_geo_count.zip','w') as zpf:
        for file in file_list_out:
            zpf.write(file)
    zp=zip(file_list_in,file_list_out)
    for a,b in zp:
        os.remove(a)
        os.remove(b)
    return send_file(r'static\geo_count_conversion\zip_geo_count.zip')

# def upload():
#     uploaded_files = Flask.request.files.getlist("file[]")
#     print(uploaded_files)
#     return ""
