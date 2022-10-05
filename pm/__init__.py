from fileinput import filename
import os
import sys
from os import listdir
from os.path import isfile, join
# from flask import request,redirect, url_for,send_from_directory, send_file
from flask import Flask,current_app,render_template,flash,request,\
        redirect, url_for,send_from_directory, send_file, \
        Blueprint, make_response, jsonify
import json
from werkzeug.utils import secure_filename
from io import StringIO
import pandas as pd
from zipfile import ZipFile
from glob import glob
import datetime


# from . import config

# cwd = os.getcwd()
# sys.path.insert(0, cwd + '/services')

# from services.pbiembedservice import PbiEmbedService
from . import utils, rptconverter as rpt, geo_counts as gc

from .services import pbiembedservice

app = Flask(__name__, static_url_path='/pm')
app.debug = True

# Load configuration
app.config.from_object('config.BaseConfig')

ALLOWED_EXTENSIONS = ['RPT']

DIRECTORY = 'hpms-site/static'

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/pm/')
def index():
    return render_template('home.html')

@app.route('/pm/chart')
def chart():
    df = pd.read_csv('static/DataItem52_Cracking_Percent_non_interstate_NHS.csv', sep='|')
    return render_template('charts/chart.html', tables=[df.to_html(classes='data')], titles=df.columns.values)

@app.route('/pm/tools')
def tools():
    return render_template('tools.html')

@app.route('/pm/rpt_convert')
def rpt_convert():
    return render_template('rpt_converter.html')

@app.route('/pm/rpt_convert/converter',methods=['POST'])
def convert_file():
    print(request.files)
    f = request.files['filename']
    # f.save(secure_filename('./static/a.txt'))
    f.save('pm/static/a.txt')
    rpt.rpt_converter('pm/static/a.txt','pm/static/out.xlsx')
    # return redirect('hpms-site/out.xlsx')
    return send_file('static/out.xlsx')

@app.route('/pm/landslide_risk')
def landslide():
    return render_template('landslide_risk.html')

@app.route('/pm/geo_counts_converter')
def geo_counts_conversion():
    return render_template('geo_count.html')

@app.route('/pm/traffic_dashboard')
def traffic_dashboard():
    return render_template('traffic_dashboard.html')

@app.route('/pm/traffic_dashboard/aadt')
def aadt_dashboard():
    return render_template('aadt_dashboard.html')

@app.route('/pm/traffic_dashboard/gas_price')
def gas_dashboard():
    return render_template('gas_price.html')

@app.route('/pm/traffic_dashboard/tourism')
def tourism_dashboard():
    return render_template('tourism.html')

@app.route('/pm/hpms_dashboard')
def hpms_dashboard():
    return render_template('hpms_dashboard.html')


@app.route('/pm/geo_counts_converter/convert',methods=['POST'])
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


@app.route('/pm/getembedinfo', methods=['GET'])
def get_embed_info():
    '''Returns report embed configuration'''

    config_result = utils.Utils.check_config(app)
    if config_result is not None:
        return json.dumps({'errorMsg': config_result}), 500

    try:
        embed_info = pbiembedservice.PbiEmbedService().get_embed_params_for_single_report(app.config['WORKSPACE_ID'], app.config['REPORT_ID'])
        embed_json = jsonify(json.loads(embed_info))
        embed_json.headers.add('Access-Control-Allow-Origin', '*')
        return embed_json
    except Exception as ex:
        return json.dumps({'errorMsg': str(ex)}), 500

@app.route('/pm/favicon.ico', methods=['GET'])
def getfavicon():
    '''Returns path of the favicon to be rendered'''

    return send_from_directory(os.path.join(app.root_path, 'static'), 'img/favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/pm/power_bi_dashboard')
def power_bi_dashboard():
    response = make_response(render_template('power_bi_dashboard.html'))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/', methods=['GET', 'POST'])
def dropdown():
    worksheet=pd.read_excel(os.path.expanduser('~') + r"\Downloads\activity codes.xlsx", sheet_name=1)
    my_dict={}
    today=datetime.date.today().strftime('%Y-%m-%d')
    for i in range(1, len(worksheet)):
        row = worksheet.iloc[i]
        my_dict[row[0]] = [row[1],row[2]]

    if request.method == 'POST':
        activity = request.form.get('activity')
        activity = {activity: my_dict.get(int(activity))}
        date = request.form.get('planned_date')
        dates = {'today':today, 'planned_date':date}
        print(dates)                
       
        return render_template('kortni2.html', data=my_dict, activity=activity, dates=dates)

    print(my_dict)
    dates = {'today':today}

    return render_template('kortni.html',data=my_dict, dates=dates)