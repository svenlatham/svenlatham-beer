from flask import Flask, request, send_from_directory, url_for, redirect, render_template
from flask import Blueprint
from .db import *

standard = Blueprint('standard', __name__)



@standard.route('/')
def index():
    beers = get_all()
    return render_template('index.html', beers=beers)

@standard.route('/beer-thumbs/<path:path>')
def send_thumb(path):
    return send_from_directory('/app/beer-thumbs/', path)

@standard.route('/f/<path:path>')
def send_furniture(path):
    return send_from_directory('/app/f/', path)

@standard.route('/flags/<path:path>')
def send_flag(path):
    file = ("%s.png" % (path.upper()))
    return send_from_directory('/app/flags/', file)

