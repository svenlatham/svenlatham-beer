from flask import Flask, request, send_from_directory, url_for, redirect, render_template
from flask import Blueprint
from .db import *

standard = Blueprint('standard', __name__)

# Create a lookup table that we can use for lookups and call for rendering
# We'll need to show the country names for NL, BE, FR and UK
country_lookup = {
    'NL': 'Netherlands',
    'BE': 'Belgium',
    'FR': 'France',
    'UK': 'United Kingdom',
    'GB': 'United Kingdom',
    'US': 'United States',
    'DE': 'Germany',
    'ES': 'Spain',
    'DK': 'Denmark',
    'IT': 'Italy',
    'IE': 'Ireland',
    'CZ': 'Czech Republic',
    'AT': 'Austria',
    'CA': 'Canada',
    'PL': 'Poland',
    'SE': 'Sweden',
    'PT': 'Portugal',
    'CH': 'Switzerland',
    'AU': 'Australia',
    'NO': 'Norway',
    'JP': 'Japan',
    'RU': 'Russia',
    'BR': 'Brazil',
    'FI': 'Finland',
    'HU': 'Hungary',
    'AR': 'Argentina',
    'RO': 'Romania',
    'HR': 'Croatia',
    'SK': 'Slovakia',
    'MX': 'Mexico',
    'EE': 'Estonia',
    'LT': 'Lithuania',
    'CN': 'China',
    'GR': 'Greece',
    'IS': 'Iceland',
    'NZ': 'New Zealand',
    'LV': 'Latvia',
    'ZA': 'South Africa',
    'UA': 'Ukraine',
    'CL': 'Chile',
    'IN': 'India',
    'BG': 'Bulgaria',
    'TR': 'Turkey',
    'TH': 'Thailand',
    'KR': 'South Korea',
    'VN': 'Vietnam',
    'ID': 'Indonesia',
    'RS': 'Serbia',
    'SI': 'Slovenia',
    'PH': 'Philippines',
    'CY': 'Cyprus',
    'LU': 'Luxembourg',
    'SG': 'Singapore',
    'MY': 'Malaysia',
    'HK': 'Hong Kong',
    'PE': 'Peru',
    'UY': 'Uruguay',
    'MD': 'Moldova',
    'CR': 'Costa Rica',
    'BY': 'Belarus',
    'CO': 'Colombia',
    'TW': 'Taiwan',
    'BA': 'Bosnia and Herzegovina'
}

@standard.context_processor
def gen_processor():
        
    def get_country_name(lookup):
        lookup=lookup.upper()
        if lookup in country_lookup.keys():
            return country_lookup[lookup]
        else:
            return lookup
    return dict(get_country_name=get_country_name)


@standard.route('/')
def index():
    beers = get_all()

    # Sort by name for unsubscribable lists
    beers.sort(key=lambda x: x.name.upper())
    # Check the request GET fields for name, description, trappist, strength, and country
    # And make sure we filter if they exist
    if request.args.get('name'):
        beers = [beer for beer in beers if request.args.get('name').lower() in beer.name.lower() or request.args.get('name').lower() in beer.description.lower()]
    if request.args.get('trappist'):
        if request.args.get('trappist') == '0':
            beers = [beer for beer in beers if beer.trappist is False]
        elif request.args.get('trappist') == '1':
            beers = [beer for beer in beers if beer.trappist is True]
    if request.args.get('strength'):
        beers = [beer for beer in beers if beer.strength is not None and beer.strength >= request.args.get('strength')]
    if request.args.get('country'):
        beers = [beer for beer in beers if beer.country is not None and beer.country.lower() == request.args.get('country').lower()]



            
    # translate this into a country list, using the lookup table
    countries = []
    beer_countries = {}
    for beer in beers:  
        if beer.country is None:
            country_key = ''
        else:   
            country_key = beer.country.upper()

        if country_key in beer_countries.keys():
            beer_countries[country_key] += 1
        else:
            beer_countries[country_key] = 1

    print(str(beer_countries))

    # Merge this with the countries_lookup table so we can send something to the template   
    for country in beer_countries.keys():
        if country in country_lookup.keys():
            countries.append({'name': country_lookup[country], 'code': country, 'count': beer_countries[country]})
        else:
            countries.append({'name': country, 'count': beer_countries[country]})
    countries.sort(key=lambda x: x['name'].upper())



    # create a list of trappist
    trappist = []
    trappist.append({'name': 'Trappist', 'value': '1'})
    trappist.append({'name': 'Non-Trappist', 'value': '0'})
    # populate the count of trappist from beer
    for t in trappist:
        t['count'] = 0
        for beer in beers:
            if t['value'] == '1' and beer.trappist is True:
                t['count'] += 1
            elif t['value'] == '0' and beer.trappist is False:
                t['count'] += 1


    
    return render_template('index.html', beers=beers, countries=countries, trappists=trappist)

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

