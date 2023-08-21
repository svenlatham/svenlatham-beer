from flask import Flask, request, send_from_directory, url_for, redirect, render_template
from flask import Blueprint
from .db import *

standard = Blueprint('standard', __name__)



@standard.route('/')
def index():
    beers = get_all()
    # Sort by name for unsubscribable lists
    beers.sort(key=lambda x: x.name.upper())
    # Check the request GET fields for name, description, trappist, strength, and country
    # And make sure we filter if they exist
    if request.args.get('name'):
        beers = [beer for beer in beers if request.args.get('name').lower() in beer.name.lower()]
    if request.args.get('description'):
        beers = [beer for beer in beers if request.args.get('description').lower() in beer.description.lower()]
    if request.args.get('trappist'):
        if request.args.get('trappist') == '0':
            beers = [beer for beer in beers if beer.trappist is False]
        elif request.args.get('trappist') == '1':
            beers = [beer for beer in beers if beer.trappist is True]
    if request.args.get('strength'):
        beers = [beer for beer in beers if beer.strength is not None and beer.strength >= request.args.get('strength')]
    if request.args.get('country'):
        beers = [beer for beer in beers if beer.country == request.args.get('country')]

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

