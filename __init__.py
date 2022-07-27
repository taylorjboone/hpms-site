from fileinput import filename
import os
from flask import request,redirect, url_for,send_from_directory, send_file
from flask import Flask,current_app,render_template,flash
import json
from werkzeug.utils import secure_filename
from io import StringIO
import pandas as pd

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
    f.save('static/a.txt')
    rpt.rpt_converter('static/a.txt','static/out.xlsx')
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
    f=request.files['filename']
    f.save(r'static\geo_count_conversion\b.txt')
    gc.geo_count_process(r'static\geo_count_conversion\b.txt')
    return send_file(r'static\geo_count_conversion\geo_count_out.xlsx')
