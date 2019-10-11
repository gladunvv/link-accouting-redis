from flask import Flask, jsonify
import redis
from flask import make_response, abort
from flask import request, make_response
import time
import json
from urllib.parse import urlparse

app = Flask(__name__)
app.debug = True

db = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def url_parce(list_links):
    print(list_links)

    for link in list_links:
        u = urlparse(link)
        result = '{uri.netloc}'.format(uri=u)
        return result




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
    domain = []
    date_from = request.args.get('from', None)
    date_to = request.args.get('to', None)
    list_keys = db.keys()
    for key in list_keys:
        if int(date_from) <= int(key) <= int(date_to):
            list_links.append(db.get(key))

    print(list_links)
    for link in list_links:
        dict_link = json.loads(link)
        domain.append(url_parce(dict_link['links']))

    res = {
        'domain': '{}'.format(domain),
        'status': 'ok',
    }
    return jsonify(res), 200


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/del', methods=['GET'])
def delete_all():
    db.flushall()
    res = {
        'status': 'ok'
    }
    return jsonify(res), 200

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

if __name__ == '__main__':
    app.run(debug=True)


# 1570818868