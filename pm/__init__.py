from fileinput import filename
import os
import sys
from os import listdir
from os.path import isfile, join
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
from datetime import timedelta

SECRET_KEY = 'secret key'
PERMANENT_SESSION_LIFETIME=  timedelta(minutes=600)


# cwd = os.getcwd()
# sys.path.insert(0, cwd + '/services')

# from services.pbiembedservice import PbiEmbedService
from . import utils, rptconverter as rpt, geo_counts as gc

app = Flask(__name__, static_url_path='/pm/static')
app.debug = True
app.secret_key = 'secret key'

# Load configuration
app.config.from_object('config.BaseConfig')

ALLOWED_EXTENSIONS = ['RPT']

DIRECTORY = 'hpms-site/static'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database.db'
db = SQLAlchemy(app)

from pm.index.routes import mod

app.register_blueprint(mod)
