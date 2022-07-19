import os
from flask import request,redirect, url_for,send_from_directory, send_file
from flask import Flask,current_app,render_template,flash
import json
from werkzeug.utils import secure_filename
from io import StringIO

from wow_updated import rpt_converter

app = Flask(__name__)

ALLOWED_EXTENSIONS = ['RPT']

DIRECTORY = 'hpms-site/static'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/chart')
def chart():
    return render_template('charts/chart.html')

@app.route('/')
def index():
    return render_template('/home.html')

@app.route('/landslide_risk')
def landslide():
    return render_template('/landslide_risk.html')

@app.route('/rpt_convert')
def rpt_convert():
    # return current_app.send_static_file('serve_this.html')
    return render_template('serve_this.html')

@app.route('/rpt_convert/converter',methods=['POST'])
def convert_file():
    print(request.files)
    f = request.files['filename']
    # f.save(secure_filename('./static/a.txt'))
    f.save('C:/Users/E025205/Documents/Python_Scripts/hpms-site/static/a.txt')
    rpt_converter('C:/Users/E025205/Documents/Python_Scripts/hpms-site/static/a.txt','C:/Users/E025205/Documents/Python_Scripts/hpms-site/static/out.xlsx')
    # return redirect('hpms-site/out.xlsx')
    return send_file('C://Users/e025205/Documents/Python_Projects/hpms-site/static/out.xlsx')

@app.route('/traffic_dashboard')
def traffic_dashboard():
    return render_template('traffic_dashboard.html')