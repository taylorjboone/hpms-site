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


# cwd = os.getcwd()
# sys.path.insert(0, cwd + '/services')

# from services.pbiembedservice import PbiEmbedService
from . import utils, rptconverter as rpt, geo_counts as gc

app = Flask(__name__, static_url_path='/pm')
app.debug = True

# Load configuration
app.config.from_object('config.BaseConfig')

ALLOWED_EXTENSIONS = ['RPT']

DIRECTORY = 'hpms-site/static'

app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///C:\Users\E025205\Documents\GitHub\hpms-site\database.db'
db = SQLAlchemy(app)

from pm.index.routes import mod

app.register_blueprint(mod)
