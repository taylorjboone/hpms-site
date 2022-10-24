import json
from datetime import date
import collections
import pandas as pd
#import pyodbc
import requests

from flask import (Blueprint, Flask, flash, jsonify, logging, redirect,
                   render_template, request, session, url_for)
from flask_sqlalchemy import SQLAlchemy
from pandas.io.json import json_normalize
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
from flask_sqlalchemy import SQLAlchemy
from pm.models.work_plan_api import Task, apply_edits, query_tasks

from flask_cors import CORS # Apparently we don't need this upon deployment

from .. import utils, rptconverter as rpt, geo_counts as gc
DIRECTORY = 'hpms-site/static'

mod = Blueprint('index',__name__,template_folder='templates',static_url_path='pm/static')
CORS(mod)

# Load configuration

ALLOWED_EXTENSIONS = ['RPT']


user_dir = os.path.expanduser('~')

users = {'District1':'District1', 'District2':'District2', 'District3':'District3', 'District4':'District4', 'District5':'District5', 'District6':'District6', 'District7':'District7', 'District8':'District8', 'District9':'District9', 'District10':'District10'}



def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@mod.route('/pm/')
def index():
    return render_template('home.html')

@mod.route('/pm/tools')
def tools():
    return render_template('tools.html')

@mod.route('/pm/rpt_convert')
def rpt_convert():
    return render_template('rpt_converter.html')

@mod.route('/pm/rpt_convert/converter',methods=['POST'])
def convert_file():
    print(request.files)
    f = request.files['filename']
    # f.save(secure_filename('./static/a.txt'))
    f.save('pm/static/a.txt')
    rpt.rpt_converter('pm/static/a.txt', 'pm/static/out.xlsx')
    # return redirect('hpms-site/out.xlsx')
    return send_file('static/out.xlsx')

@mod.route('/pm/landslide_risk')
def landslide():
    return render_template('landslide_risk.html')

@mod.route('/pm/geo_counts_converter')
def geo_counts_conversion():
    return render_template('geo_count.html')

@mod.route('/pm/geo_counts_converter/convert',methods=['POST'])
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


@mod.route('/pm/work_plan', methods=['GET', 'POST'])
def work_plan():
    if session.get('user', False):
        return send_from_directory('react_test/build', 'index.html')
    else:
        return redirect(url_for('index.login'))


@mod.route('/pm/work_plan/apply_edits', methods=['POST'])
def work_plan_api():
    edits = json.loads(request.data)
    return jsonify(apply_edits(edits))


@mod.route('/pm/login', methods = ['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if users.get(request.form['username'], False) and (request.form['password'] == users.get(request.form['username'], False)):
            session['user'] = request.form['username']
            session['login'] = datetime.datetime.now()
            return redirect(url_for('index.work_plan'))
        else:
            error = 'Invalid Credentials. Please try again'
    return render_template('work_plan_login.html', error = error)


@mod.route('/pm/api/query')
def query_tasks_route():
    args = request.args
    args = args.to_dict()
    ids = args.get('ids',[])
    if '[' in ids and ',' in ids:
        ids = json.loads(ids)
    print(ids)

    tasks = query_tasks(ids)

    return jsonify(tasks)