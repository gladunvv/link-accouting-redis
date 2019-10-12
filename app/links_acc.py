from flask import Flask, jsonify
from flask import make_response, abort
from flask import request, make_response
import time
import json
from urllib.parse import urlparse
from flask import Flask
import redis

app = Flask(__name__)
HOST = 'localhost'
PORT = 6379
DB = 0
DEC_RES = True

db = redis.Redis(
    host=HOST,
    port=PORT,
    db=DB,
    decode_responses=DEC_RES
    )

def url_parce(list_links):
    domains = []
    for link in list_links:
        uri = urlparse(link)
        if uri.netloc:
            result = '{uri.netloc}'.format(uri=uri)
        elif uri.path:
            result = link
        else:
            result = None
        domains.append(result)
    return domains

def unique_list(domains):
    unique_list = []
    for x in domains:
        if x not in unique_list:
            unique_list.append(x)
    return unique_list

@app.route('/api/v1.0/visited_links', methods=['POST'])
def add_links():
    if not request.json or not 'links' in request.json:
        abort(400)
    date = int(time.time())
    print(date)
    links = json.dumps(request.json)
    db.set(date, links)
    res = {
        'status': 'ok'
    }
    return jsonify(res), 200


@app.route('/api/v1.0/visited_domains', methods=['GET'])
def get_links():
    list_links = []
    domains = []
    date_from = request.args.get('from', None)
    date_to = request.args.get('to', None)

    list_keys = db.keys()
    for key in list_keys:
        if int(date_from) <= int(key) <= int(date_to):
            list_links.append(db.get(key))

    for link in list_links:
        dict_link = json.loads(link)
        domains += url_parce(dict_link['links'])
    unique_domains = unique_list(domains)

    res = {
        'domains': unique_domains,
        'status': 'ok',
    }
    return jsonify(res), 200


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

@app.route('/del', methods=['GET'])
def delete_all():
    db.flushall()
    res = {
        'status': 'ok'
    }
    return jsonify(res), 200

if __name__ == '__main__':
    app.run(debug=True)

